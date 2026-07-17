import os
import sys
import time
import re
import urllib.parse
import pandas as pd
import requests
from bs4 import BeautifulSoup
from dotenv import load_dotenv

# Reconfigure stdout to use UTF-8 globally to prevent Windows console encoding crashes
sys.stdout.reconfigure(encoding='utf-8')

# Define file paths
STORIES_FILE = "data/Stories.xlsx"
CANDIDATES_RAW_FILE = "data/candidates_raw.xlsx"
CANDIDATES_RAW_BACKUP_FILE = "data/candidates_raw_backup.xlsx"

def save_dataframe_to_excel(df, filepath, backup_filepath=CANDIDATES_RAW_BACKUP_FILE):
    """
    Saves a DataFrame to Excel, handling PermissionError gracefully.
    If the file is locked (e.g. open in Excel), writes to a consolidated backup file.
    """
    try:
        df.to_excel(filepath, index=False)
        # If successfully written, and a backup exists, try to clean it up
        if os.path.exists(backup_filepath):
            try:
                os.remove(backup_filepath)
            except Exception:
                pass
        return True
    except PermissionError:
        print(f"\n   [Permission Error] Cannot write to {filepath} (file is likely open in Excel).")
        print(f"   Saving progress to backup file: {backup_filepath}")
        try:
            df.to_excel(backup_filepath, index=False)
            return True
        except Exception as e:
            print(f"   Failed to save backup file: {e}")
            return False

def make_jikan_request(url, params=None, max_retries=3):
    """
    Helper function to make requests to the Jikan API.
    Handles rate limits (429) and temporary server issues (5xx)
    using exponential backoff and retries.
    """
    time.sleep(2.0)  # Rate limit: wait 2 seconds between Jikan calls
    
    backoff = 2.0
    for attempt in range(max_retries):
        try:
            response = requests.get(url, params=params, timeout=10)
            if response.status_code == 200:
                return response.json()
            elif response.status_code == 429:
                sleep_time = backoff + 5.0
                print(f"   [Rate Limited (429)] Waiting {sleep_time:.1f}s before retry (Attempt {attempt + 1}/{max_retries})...")
                time.sleep(sleep_time)
                backoff *= 2
            elif response.status_code in [500, 502, 503, 504]:
                return None
            else:
                return None
        except requests.exceptions.RequestException:
            return None
            
    return None

def scrape_mal_directly(title, media_type):
    """
    Directly scrapes MyAnimeList search results and characters page
    if Jikan API is offline. Bypasses rate limits and outage issues.
    """
    headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko)"}
    
    # Map medium type from Stories.xlsx to MAL URL types (anime or manga)
    mal_type = "anime"
    if media_type.lower() in ["manga", "light novel", "novel", "visual novel"]:
        mal_type = "manga"
        
    print(f"   -> [Direct Scraper] Searching MyAnimeList {mal_type} search results for '{title}'...")
    search_url = f"https://myanimelist.net/{mal_type}.php?q={urllib.parse.quote(title)}"
    
    try:
        r = requests.get(search_url, headers=headers, timeout=10)
        if r.status_code != 200:
            return None
            
        soup = BeautifulSoup(r.text, "html.parser")
        matched_links = []
        for link in soup.find_all("a", href=True):
            href = link["href"]
            match = re.search(rf"https://myanimelist.net/{mal_type}/(\d+)/", href)
            if match:
                matched_links.append((match.group(1), href))
                
        if not matched_links:
            return None
            
        # Select first search result
        mal_id = matched_links[0][0]
        
        # Query characters page
        char_url = f"https://myanimelist.net/{mal_type}/{mal_id}/characters"
        print(f"   -> [Direct Scraper] Fetching characters directly from MAL: {char_url}")
        cr = requests.get(char_url, headers=headers, timeout=10)
        
        # If characters page doesn't return 200, try the main info page (some visual novels or novels have it there)
        if cr.status_code != 200:
            char_url = f"https://myanimelist.net/{mal_type}/{mal_id}"
            cr = requests.get(char_url, headers=headers, timeout=10)
            if cr.status_code != 200:
                return None
                
        csoup = BeautifulSoup(cr.text, "html.parser")
        chars = []
        for char_link in csoup.find_all("a", href=True):
            chref = char_link["href"]
            match = re.search(r"https://myanimelist.net/character/(\d+)/", chref)
            if match:
                char_id = int(match.group(1))
                char_name = char_link.text.strip()
                if char_name:
                    # Find role (Main/Supporting)
                    parent = char_link.find_parent("td")
                    role = "Supporting"
                    if parent:
                        parent_text = parent.get_text()
                        if "Main" in parent_text:
                            role = "Main"
                        elif "Supporting" in parent_text:
                            role = "Supporting"
                    chars.append({
                        "name": char_name,
                        "role": role,
                        "mal_id": char_id,
                        "url": chref
                    })
                    
        # De-duplicate preserving search/importance order
        seen = set()
        unique_chars = []
        for char in chars:
            if char["name"] not in seen:
                seen.add(char["name"])
                unique_chars.append(char)
                
        return unique_chars
    except Exception as e:
        print(f"      [Direct Scraper Error] Direct parse failed: {e}")
        return None

def normalize_character_name(name_str):
    """
    Normalizes character name from Jikan's "Last, First" format to "First Last".
    Example: "Kirisaki, Chitoge" -> "Chitoge Kirisaki"
    """
    if not isinstance(name_str, str):
        return "Unknown"
    
    name_str = name_str.strip()
    if "," in name_str:
        parts = name_str.split(",", 1)
        last = parts[0].strip()
        first = parts[1].strip()
        return f"{first} {last}"
    
    return name_str

def main():
    print("=== Romance Media Scraper Pipeline (Jikan + Direct Fallback) ===")
    
    # 1. Load stories from Excel
    if not os.path.exists(STORIES_FILE):
        print(f"Error: {STORIES_FILE} not found!")
        return
        
    stories_df = pd.read_excel(STORIES_FILE)
    stories_df = stories_df.dropna(axis=1, how="all")
    print(f"Loaded {len(stories_df)} stories from {STORIES_FILE}.")
    
    # 2. Setup or resume raw candidates dataset
    processed_story_ids = set()
    candidates_list = []
    next_candidate_num = 1
    
    # Read from main raw file and backup raw file to determine starting point
    loaded_dfs = []
    for filepath in [CANDIDATES_RAW_FILE, CANDIDATES_RAW_BACKUP_FILE]:
        if os.path.exists(filepath):
            print(f"Found existing raw candidates file: {filepath}")
            try:
                df = pd.read_excel(filepath)
                if not df.empty:
                    loaded_dfs.append(df)
            except Exception as e:
                print(f"Warning: Could not read {filepath}: {e}")
                
    if loaded_dfs:
        try:
            combined_df = pd.concat(loaded_dfs, ignore_index=True).drop_duplicates(subset=["story_id", "candidate_name"])
            candidates_list = combined_df.to_dict("records")
            processed_story_ids = set(combined_df["story_id"].dropna().unique())
            print(f"Resuming progress: Already processed {len(processed_story_ids)} stories.")
            
            # Determine next candidate ID number (e.g. C0042 -> 43)
            max_num = 0
            for cid in combined_df["candidate_id"].dropna():
                if isinstance(cid, str) and cid.startswith("C"):
                    try:
                        num = int(cid[1:])
                        if num > max_num:
                            max_num = num
                    except ValueError:
                        pass
            next_candidate_num = max_num + 1
            print(f"Next candidate ID will start at C{next_candidate_num:04d}.")
        except Exception as e:
            print(f"Error combining existing files: {e}. Starting fresh.")
            
    # 3. Iterate through each story in Stories.xlsx
    for index, row in stories_df.iterrows():
        story_id = row["story_id"]
        title = row["title"]
        medium = row["medium"]
        
        # Skip if already processed (Resumability check)
        if story_id in processed_story_ids:
            continue
            
        print(f"\n[{index + 1}/{len(stories_df)}] Processing Story ID {story_id}: '{title}' ({medium})")
        
        # Try Jikan API search first
        search_types = [
            ("anime", "https://api.jikan.moe/v4/anime"),
            ("manga", "https://api.jikan.moe/v4/manga")
        ]
        
        mal_id = None
        media_type = None
        jikan_success = False
        
        for m_type, api_url in search_types:
            print(f" - Searching on MyAnimeList ({m_type} endpoint)...")
            search_results = make_jikan_request(api_url, params={"q": title, "limit": 1})
            
            if search_results and "data" in search_results and len(search_results["data"]) > 0:
                match = search_results["data"][0]
                mal_id = match["mal_id"]
                matched_title = match.get("title", title)
                media_type = m_type
                print(f"   -> Found Jikan match: '{matched_title}' (MAL ID: {mal_id})")
                jikan_success = True
                break
                
        # If Jikan search succeeded, try to fetch characters
        characters_list = []
        if jikan_success and mal_id:
            characters_url = f"https://api.jikan.moe/v4/{media_type}/{mal_id}/characters"
            print(f" - Fetching Jikan characters list...")
            char_data = make_jikan_request(characters_url)
            
            if char_data and "data" in char_data and len(char_data["data"]) > 0:
                for item in char_data["data"]:
                    char_node = item.get("character", {})
                    char_mal_id = char_node.get("mal_id")
                    char_url = char_node.get("url")
                    raw_name = char_node.get("name", "Unknown")
                    role = item.get("role", "Supporting")
                    
                    if not char_mal_id or raw_name == "Unknown":
                        continue
                        
                    candidate_name = normalize_character_name(raw_name)
                    characters_list.append({
                        "name": candidate_name,
                        "role": role,
                        "mal_id": char_mal_id,
                        "url": char_url
                    })
                    
        # If Jikan failed (e.g. 504 outage) or returned nothing, use Direct Web Scraper Fallback
        if not characters_list:
            print("   -> [Jikan Offline/Empty] Falling back to direct MyAnimeList web scraping...")
            mal_chars = scrape_mal_directly(title, medium)
            if mal_chars:
                for mc in mal_chars:
                    characters_list.append({
                        "name": normalize_character_name(mc["name"]),
                        "role": mc["role"],
                        "mal_id": mc["mal_id"],
                        "url": mc["url"]
                    })
                print(f"   -> Successfully retrieved {len(characters_list)} characters via direct scraping.")
            else:
                print("   -> [Error] Direct scraping fallback failed to retrieve characters.")
                
        if not characters_list:
            print(f" [Warning] Could not extract any characters for '{title}'. Skipping.")
            processed_story_ids.add(story_id)
            continue
            
        # Save raw characters to candidates list
        added_count = 0
        for char in characters_list:
            candidate_record = {
                "candidate_id": f"C{next_candidate_num:04d}",
                "story_id": story_id,
                "candidate_name": char["name"],
                "candidate_gender": "Unknown",
                "role": char["role"],
                "mal_character_id": char["mal_id"] if char["mal_id"] else "",
                "mal_character_url": char["url"] if char["url"] else ""
            }
            candidates_list.append(candidate_record)
            next_candidate_num += 1
            added_count += 1
            
        print(f"   -> Saved {added_count} raw characters for '{title}'.")
        processed_story_ids.add(story_id)
        
        # Save progress after each story (using robust helper)
        df_to_save = pd.DataFrame(candidates_list)
        save_dataframe_to_excel(df_to_save, CANDIDATES_RAW_FILE)
        
        # Polite delay to respect MAL website access
        time.sleep(2.0)
        
    print("\n=== Scraper Pipeline Completed! ===")
    print(f"Total raw candidates saved: {len(candidates_list)}")
    print(f"Saved to: {CANDIDATES_RAW_FILE}")

if __name__ == "__main__":
    main()