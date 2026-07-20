import os
import sys
import re
import time
import requests
import pandas as pd
from concurrent.futures import ThreadPoolExecutor, as_completed

# Reconfigure stdout to use UTF-8 globally to prevent Windows console encoding crashes
sys.stdout.reconfigure(encoding='utf-8')

CANDIDATES_CLEANED_FILE = "data/candidates_cleaned.xlsx"
STORIES_CLEANED_FILE = "data/stories_cleaned.xlsx"

query_media = '''
query ($idMal: Int, $type: MediaType) {
  Media (idMal: $idMal, type: $type) {
    id
    idMal
    title {
      romaji
      english
    }
    characters (perPage: 50) {
      nodes {
        id
        name {
          full
          userPreferred
        }
        favourites
      }
    }
  }
}
'''

query_char_search = '''
query ($search: String) {
  Character (search: $search) {
    id
    name {
      full
    }
    favourites
  }
}
'''

url = 'https://graphql.anilist.co'
headers = {'Content-Type': 'application/json', 'Accept': 'application/json'}

def fetch_media_characters(mal_id, medium):
    if pd.isna(mal_id):
        return []
    
    primary_type = 'MANGA' if str(medium).lower() in ['manga', 'light novel', 'novel', 'visual novel'] else 'ANIME'
    types_to_try = [primary_type, 'ANIME' if primary_type == 'MANGA' else 'MANGA']
    
    nodes = []
    for mtype in types_to_try:
        for attempt in range(2):
            try:
                r = requests.post(url, json={'query': query_media, 'variables': {'idMal': int(mal_id), 'type': mtype}}, headers=headers, timeout=6)
                if r.status_code == 200 and r.json().get('data', {}).get('Media'):
                    res_nodes = r.json()['data']['Media']['characters']['nodes']
                    if res_nodes:
                        nodes = res_nodes
                        break
            except Exception:
                time.sleep(0.5)
        if nodes:
            break
            
    return [{'id': n['id'], 'full_name': n['name']['full'], 'favs': n['favourites'] or 0} for n in nodes]

def main():
    print("=== Candidate Popularity & Favorites Enrichment Pipeline ===")
    
    if not os.path.exists(CANDIDATES_CLEANED_FILE):
        print(f"Error: {CANDIDATES_CLEANED_FILE} not found!")
        return
    if not os.path.exists(STORIES_CLEANED_FILE):
        print(f"Error: {STORIES_CLEANED_FILE} not found!")
        return

    df_clean = pd.read_excel(CANDIDATES_CLEANED_FILE)
    df_stories = pd.read_excel(STORIES_CLEANED_FILE)
    story_dict = df_stories.set_index('story_id').to_dict(orient='index')

    story_groups = list(df_clean.groupby('story_id'))
    print(f"Enriching {len(df_clean)} candidates across {len(story_groups)} stories...")

    candidate_favs = {}

    def process_story(story_id, group):
        s_info = story_dict.get(story_id, {})
        mal_id = s_info.get('mal_id')
        medium = s_info.get('medium', 'Manga')
        
        chars = fetch_media_characters(mal_id, medium)
        
        story_res = []
        for _, c_row in group.iterrows():
            cand_id = c_row['candidate_id']
            cand_name = str(c_row['candidate_name']).strip()
            cand_words = set(re.findall(r'\w+', cand_name.lower()))
            
            favs = None
            
            # Match within story characters
            for c in chars:
                c_words = set(re.findall(r'\w+', c['full_name'].lower()))
                if cand_words == c_words or cand_words.issubset(c_words) or c_words.issubset(cand_words) or (cand_words & c_words and len(cand_words & c_words) >= 1 and not (len(cand_words & c_words) == 1 and list(cand_words & c_words)[0] in ['a', 'the', 'of', 'no', 'de', 'san', 'chan'])):
                    favs = c['favs']
                    break
                    
            # Fallback search if unmatched
            if favs is None:
                try:
                    r_c = requests.post(url, json={'query': query_char_search, 'variables': {'search': cand_name}}, headers=headers, timeout=5)
                    if r_c.status_code == 200 and r_c.json().get('data', {}).get('Character'):
                        favs = r_c.json()['data']['Character']['favourites'] or 0
                except Exception:
                    pass
                    
            if favs is None:
                favs = 0
                
            story_res.append((cand_id, favs))
            
        time.sleep(0.2)
        return story_res

    start_t = time.time()
    with ThreadPoolExecutor(max_workers=5) as executor:
        futures = [executor.submit(process_story, s_id, group) for s_id, group in story_groups]
        for future in as_completed(futures):
            res = future.result()
            for cid, favs in res:
                candidate_favs[cid] = favs

    print(f"Retrieved popularity metrics in {time.time() - start_t:.1f} seconds!")

    # Attach columns
    df_clean['favorites'] = df_clean['candidate_id'].map(candidate_favs).fillna(0).astype(int)
    df_clean['story_favorites_rank'] = df_clean.groupby('story_id')['favorites'].rank(ascending=False, method='min').astype(int)

    print("\nSummary Statistics of 'favorites':")
    print(df_clean['favorites'].describe())
    print(f"\nCandidates with >0 favorites: {(df_clean['favorites'] > 0).sum()} / {len(df_clean)} ({(df_clean['favorites'] > 0).mean()*100:.1f}%)")

    # Try saving to candidates_cleaned.xlsx
    try:
        df_clean.to_excel(CANDIDATES_CLEANED_FILE, index=False)
        print(f"\n[SUCCESS] Updated {CANDIDATES_CLEANED_FILE} successfully!")
    except PermissionError:
        backup_file = "data/candidates_cleaned_updated.xlsx"
        df_clean.to_excel(backup_file, index=False)
        print(f"\n[WARNING] Could not overwrite {CANDIDATES_CLEANED_FILE} because it is open in Excel.")
        print(f"Saved to backup file: {backup_file}")

if __name__ == "__main__":
    main()
