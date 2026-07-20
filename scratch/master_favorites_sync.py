import os
import sys
import re
import time
import requests
import pandas as pd
from bs4 import BeautifulSoup
from concurrent.futures import ThreadPoolExecutor, as_completed

sys.stdout.reconfigure(encoding='utf-8')

print("=== STARTING MASTER FAVORITES DATA REFRESH ===")

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
}

# Load datasets
df_clean = pd.read_excel('data/candidates_cleaned.xlsx')
df_back = pd.read_excel('data/candidates_raw_backup.xlsx')
df_stories = pd.read_excel('data/stories_cleaned.xlsx').set_index('story_id').to_dict('index')

# Normalize names for backup matching
df_back['norm_name'] = df_back['candidate_name'].astype(str).str.strip().str.lower()
df_clean['norm_name'] = df_clean['candidate_name'].astype(str).str.strip().str.lower()

backup_map = dict(zip(zip(df_back['story_id'], df_back['norm_name']), df_back['mal_character_id']))

df_clean['mal_character_id'] = df_clean.apply(lambda r: backup_map.get((r['story_id'], r['norm_name'])), axis=1)
print(f"Mapped {df_clean['mal_character_id'].notna().sum()} / {len(df_clean)} candidates directly from backup dataset.")

# Query AniList GraphQL for candidate batch ID matching
query_batch = '''
query ($ids: [Int]) {
  Page (perPage: 50) {
    characters (id_in: $ids) {
      id
      name { full }
      favourites
    }
  }
}
'''

query_media = '''
query ($idMal: Int) {
  Media (idMal: $idMal) {
    id
    characters (perPage: 100) {
      nodes {
        id
        name { full native userPreferred alternative }
        favourites
      }
    }
  }
}
'''

url_anilist = 'https://graphql.anilist.co'
al_headers = {'Content-Type': 'application/json', 'Accept': 'application/json'}

char_favs = {}

# 1. Batch query AniList for known MAL character IDs (50 at a time)
valid_cids = [int(x) for x in df_clean['mal_character_id'].dropna().unique() if int(x) > 0]
print(f"Batch querying AniList for {len(valid_cids)} character IDs...")

for i in range(0, len(valid_cids), 50):
    batch = valid_cids[i:i+50]
    try:
        r = requests.post(url_anilist, json={'query': query_batch, 'variables': {'ids': batch}}, headers=al_headers, timeout=10)
        if r.status_code == 200 and r.json().get('data', {}).get('Page'):
            for c in r.json()['data']['Page']['characters']:
                char_favs[c['id']] = c['favourites'] or 0
    except Exception as e:
        pass
    time.sleep(0.2)

print(f"AniList batch query populated {len(char_favs)} character favorites!")

# 2. For remaining candidates, fetch story media characters from AniList
story_media_cache = {}

def get_story_media_chars(sid):
    if sid in story_media_cache:
        return story_media_cache[sid]
    sinfo = df_stories.get(sid, {})
    mal_id = sinfo.get('mal_id')
    if not mal_id or pd.isna(mal_id):
        return []
    try:
        r = requests.post(url_anilist, json={'query': query_media, 'variables': {'idMal': int(mal_id)}}, headers=al_headers, timeout=8)
        if r.status_code == 200 and r.json().get('data', {}).get('Media'):
            nodes = r.json()['data']['Media']['characters']['nodes']
            chars = []
            for n in nodes:
                names = [n['name']['full'], n['name']['userPreferred'], n['name']['native']]
                if n['name'].get('alternative'):
                    names.extend(n['name']['alternative'])
                chars.append({'id': n['id'], 'names': [x for x in names if x], 'favs': n['favourites'] or 0})
            story_media_cache[sid] = chars
            return chars
    except Exception:
        pass
    return []

# Fetch story media in parallel
with ThreadPoolExecutor(max_workers=10) as executor:
    sids = list(df_stories.keys())
    futures = {executor.submit(get_story_media_chars, sid): sid for sid in sids}
    for future in as_completed(futures):
        pass

# 3. Process candidate favorites mapping
final_rows = []
for idx, row in df_clean.iterrows():
    cand_id = row['candidate_id']
    sid = row['story_id']
    cname = str(row['candidate_name']).strip()
    cwords = set(re.findall(r'\w+', cname.lower()))
    mal_cid = row['mal_character_id']
    
    fav = 0
    
    # Priority A: Check batch query result for mal_cid
    if pd.notna(mal_cid) and int(mal_cid) in char_favs:
        fav = char_favs[int(mal_cid)]
    else:
        # Priority B: Check story media characters
        chars = story_media_cache.get(sid, [])
        matched_fav = None
        
        for c in chars:
            for n in c['names']:
                nwords = set(re.findall(r'\w+', n.lower()))
                if cwords == nwords or cwords.issubset(nwords) or nwords.issubset(cwords):
                    matched_fav = c['favs']
                    break
            if matched_fav is not None:
                break
                
        if matched_fav is None:
            for c in chars:
                for n in c['names']:
                    nwords = set(re.findall(r'\w+', n.lower()))
                    overlap = cwords & nwords
                    if len(overlap) >= 1 and not (len(overlap) == 1 and list(overlap)[0] in ['a', 'the', 'of', 'no', 'de', 'so', 'to', 'la', 'von']):
                        matched_fav = c['favs']
                        break
                if matched_fav is not None:
                    break
                    
        if matched_fav is not None:
            fav = matched_fav

    rdict = row.to_dict()
    rdict['favorites'] = int(fav)
    final_rows.append(rdict)

res_df = pd.DataFrame(final_rows)

# Drop temporary columns
for col in ['norm_name', 'mal_character_id']:
    if col in res_df.columns:
        res_df.drop(columns=[col], inplace=True)

# 4. Calculate story_favorites_rank
res_df['story_favorites_rank'] = res_df.groupby('story_id')['favorites'].rank(ascending=False, method='min').astype(int)

print(f"\n=== FINAL DATASET SUMMARY ===")
print(f"Total candidates: {len(res_df)}")
print(f"Candidates with >0 favorites: {(res_df['favorites'] > 0).sum()} / {len(res_df)}")
print(f"Candidates with 0 favorites: {(res_df['favorites'] == 0).sum()} / {len(res_df)}")

print("\nTop 15 Most Popular Candidates Across All Stories:")
print(res_df.sort_values('favorites', ascending=False)[['candidate_id', 'story_id', 'candidate_name', 'favorites', 'story_favorites_rank']].head(15).to_string(index=False))

# 5. Overwrite candidates_cleaned.xlsx
output_file = 'data/candidates_cleaned.xlsx'
res_df.to_excel(output_file, index=False)
print(f"\nSuccessfully updated and saved {output_file}!")
