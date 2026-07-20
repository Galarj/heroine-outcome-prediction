import os
import sys
import re
import time
import requests
import pandas as pd
from bs4 import BeautifulSoup
from concurrent.futures import ThreadPoolExecutor, as_completed

sys.stdout.reconfigure(encoding='utf-8')

print("=== EXECUTING COMPLETE MAL FAVORITES FETCH ===")

# Standard headers to prevent 405/403 block from MAL
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8',
    'Accept-Language': 'en-US,en;q=0.5'
}

df_clean = pd.read_excel('data/candidates_cleaned.xlsx')
df_back = pd.read_excel('data/candidates_raw_backup.xlsx')
df_stories = pd.read_excel('data/stories_cleaned.xlsx').set_index('story_id').to_dict('index')

# Normalize names for matching
df_back['norm_name'] = df_back['candidate_name'].astype(str).str.strip().str.lower()
df_clean['norm_name'] = df_clean['candidate_name'].astype(str).str.strip().str.lower()

# Map candidate (story_id, norm_name) -> mal_character_id from backup
backup_map = dict(zip(zip(df_back['story_id'], df_back['norm_name']), df_back['mal_character_id']))

df_clean['mal_character_id'] = df_clean.apply(lambda r: backup_map.get((r['story_id'], r['norm_name'])), axis=1)

print(f"Mapped {df_clean['mal_character_id'].notna().sum()} / {len(df_clean)} candidates directly from backup dataset.")

# Resolve missing MAL character IDs via story characters page
story_mal_cache = {}

def get_story_mal_chars(sid):
    if sid in story_mal_cache:
        return story_mal_cache[sid]
    sinfo = df_stories.get(sid, {})
    mal_id = sinfo.get('mal_id')
    medium = str(sinfo.get('medium', 'Manga')).lower()
    if not mal_id or pd.isna(mal_id):
        story_mal_cache[sid] = []
        return []
    
    mal_id = int(mal_id)
    m_types = ['anime', 'manga'] if medium in ['anime', 'original anime'] else ['manga', 'anime']
    
    found_chars = []
    for mt in m_types:
        url = f'https://myanimelist.net/{mt}/{mal_id}/characters'
        try:
            r = requests.get(url, headers=headers, timeout=10)
            if r.status_code == 200:
                soup = BeautifulSoup(r.text, 'html.parser')
                links = soup.find_all('a', href=re.compile(r'/character/(\d+)'))
                seen = set()
                for a in links:
                    m = re.search(r'/character/(\d+)', a['href'])
                    if m:
                        cid = int(m.group(1))
                        cname = a.text.strip()
                        if cid not in seen and cname:
                            seen.add(cid)
                            found_chars.append({'cid': cid, 'name': cname})
                if found_chars:
                    break
        except Exception:
            pass
        time.sleep(0.3)
    story_mal_cache[sid] = found_chars
    return found_chars

missing_mask = df_clean['mal_character_id'].isna()
missing_indices = df_clean[missing_mask].index

resolved = 0
for idx in missing_indices:
    sid = df_clean.loc[idx, 'story_id']
    cname = str(df_clean.loc[idx, 'candidate_name']).strip()
    cwords = set(re.findall(r'\w+', cname.lower()))
    
    chars = get_story_mal_chars(sid)
    matched_id = None
    
    for c in chars:
        mwords = set(re.findall(r'\w+', c['name'].lower()))
        if cwords == mwords or cwords.issubset(mwords) or mwords.issubset(cwords):
            matched_id = c['cid']
            break
            
    if not matched_id:
        for c in chars:
            mwords = set(re.findall(r'\w+', c['name'].lower()))
            overlap = cwords & mwords
            if len(overlap) >= 1 and not (len(overlap) == 1 and list(overlap)[0] in ['a', 'the', 'of', 'no', 'de', 'so', 'to', 'la', 'von']):
                matched_id = c['cid']
                break
                
    if matched_id:
        resolved += 1
        df_clean.loc[idx, 'mal_character_id'] = matched_id

print(f"Resolved {resolved} missing character IDs via MAL story character lookup.")

# Fetch MAL favorites for all valid MAL character IDs
char_fav_cache = {}

def fetch_mal_favs(cid):
    if not cid or pd.isna(cid):
        return 0
    cid = int(cid)
    if cid in char_fav_cache:
        return char_fav_cache[cid]
        
    url = f'https://myanimelist.net/character/{cid}'
    for attempt in range(3):
        try:
            r = requests.get(url, headers=headers, timeout=8)
            if r.status_code == 200:
                soup = BeautifulSoup(r.text, 'html.parser')
                fav = 0
                m = re.search(r'Member Favorites:\s*([\d,]+)', r.text)
                if m:
                    fav = int(m.group(1).replace(',', ''))
                char_fav_cache[cid] = fav
                return fav
            elif r.status_code == 404:
                char_fav_cache[cid] = 0
                return 0
        except Exception:
            pass
        time.sleep(0.4)
    char_fav_cache[cid] = 0
    return 0

unique_ids = [int(x) for x in df_clean['mal_character_id'].dropna().unique() if int(x) > 0]
print(f"Fetching MAL Favorites for {len(unique_ids)} unique character IDs using 12 worker threads...")

start_t = time.time()
with ThreadPoolExecutor(max_workers=12) as executor:
    futures = {executor.submit(fetch_mal_favs, cid): cid for cid in unique_ids}
    for future in as_completed(futures):
        pass

print(f"Scraped {len(char_fav_cache)} character pages in {time.time() - start_t:.1f}s!")

# Map favorites back
df_clean['favorites'] = df_clean['mal_character_id'].apply(lambda cid: char_fav_cache.get(int(cid), 0) if pd.notna(cid) else 0)

# Calculate story_favorites_rank
df_clean['story_favorites_rank'] = df_clean.groupby('story_id')['favorites'].rank(ascending=False, method='min').astype(int)

# Clean up helper columns
for col in ['norm_name', 'mal_character_id']:
    if col in df_clean.columns:
        df_clean.drop(columns=[col], inplace=True)

print("\n=== FINAL MAL FAVORITES METRICS ===")
print(f"Total candidates: {len(df_clean)}")
print(f"Candidates with >0 favorites: {(df_clean['favorites'] > 0).sum()} / {len(df_clean)}")
print(f"Candidates with 0 favorites: {(df_clean['favorites'] == 0).sum()} / {len(df_clean)}")

print("\nTop 15 Most Popular Candidates on MAL:")
print(df_clean.sort_values('favorites', ascending=False)[['candidate_id', 'story_id', 'candidate_name', 'favorites', 'story_favorites_rank']].head(15).to_string(index=False))

# Overwrite candidates_cleaned.xlsx
df_clean.to_excel('data/candidates_cleaned.xlsx', index=False)
print("\nSuccessfully updated and saved data/candidates_cleaned.xlsx!")
