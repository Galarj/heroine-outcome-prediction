import os
import sys
import re
import time
import requests
import pandas as pd
from concurrent.futures import ThreadPoolExecutor, as_completed

sys.stdout.reconfigure(encoding='utf-8')

CANDIDATES_FILE = "data/candidates_cleaned.xlsx"
STORIES_FILE = "data/stories_cleaned.xlsx"

df_clean = pd.read_excel(CANDIDATES_FILE)
df_stories = pd.read_excel(STORIES_FILE)
story_dict = df_stories.set_index('story_id').to_dict(orient='index')

query_media = '''
query ($idMal: Int, $type: MediaType) {
  Media (idMal: $idMal, type: $type) {
    id
    idMal
    title {
      romaji
      english
    }
    characters (perPage: 100) {
      nodes {
        id
        name {
          full
          userPreferred
          native
        }
        favourites
      }
    }
  }
}
'''

url = 'https://graphql.anilist.co'
headers = {'Content-Type': 'application/json', 'Accept': 'application/json'}

candidate_favs = {}
matched_names = {}

story_groups = list(df_clean.groupby('story_id'))
print(f"Starting ultra-fast story retrieval across {len(story_groups)} stories...")
start_t = time.time()

def fetch_and_match_story(story_id, group):
    s_info = story_dict.get(story_id, {})
    mal_id = s_info.get('mal_id')
    medium = s_info.get('medium', 'Manga')
    
    primary_type = 'MANGA' if str(medium).lower() in ['manga', 'light novel', 'novel', 'visual novel'] else 'ANIME'
    types_to_try = [primary_type, 'ANIME' if primary_type == 'MANGA' else 'MANGA']
    
    nodes = []
    if pd.notna(mal_id):
        for mtype in types_to_try:
            try:
                r = requests.post(url, json={'query': query_media, 'variables': {'idMal': int(mal_id), 'type': mtype}}, headers=headers, timeout=6)
                if r.status_code == 200 and r.json().get('data', {}).get('Media'):
                    res_nodes = r.json()['data']['Media']['characters']['nodes']
                    if res_nodes:
                        nodes = res_nodes
                        break
            except Exception:
                pass
                
    story_results = []
    for _, c_row in group.iterrows():
        cand_id = c_row['candidate_id']
        cand_name = str(c_row['candidate_name']).strip()
        cand_words = set(re.findall(r'\w+', cand_name.lower()))
        
        favs = 0
        matched_name = ""
        
        # 1. Exact or Subset match
        for n in nodes:
            full_n = n['name']['full']
            n_words = set(re.findall(r'\w+', full_n.lower()))
            if cand_words == n_words or cand_words.issubset(n_words) or n_words.issubset(cand_words):
                favs = n['favourites'] or 0
                matched_name = full_n
                break
                
        # 2. Meaningful name overlap match
        if not matched_name and nodes:
            for n in nodes:
                full_n = n['name']['full']
                n_words = set(re.findall(r'\w+', full_n.lower()))
                overlap = cand_words & n_words
                overlap_meaningful = [w for w in overlap if w not in ['a', 'the', 'of', 'no', 'de', 'san', 'chan', 'kun', 'sama', 'onee', 'imouto']]
                if overlap_meaningful:
                    favs = n['favourites'] or 0
                    matched_name = full_n
                    break
                    
        story_results.append((cand_id, favs, matched_name))
        
    return story_results

with ThreadPoolExecutor(max_workers=10) as executor:
    futures = [executor.submit(fetch_and_match_story, s_id, group) for s_id, group in story_groups]
    for future in as_completed(futures):
        res = future.result()
        for cid, favs, mname in res:
            candidate_favs[cid] = favs
            matched_names[cid] = mname

print(f"Finished in {time.time() - start_t:.2f} seconds!")

# Attach columns to df_clean
df_clean['favorites'] = df_clean['candidate_id'].map(candidate_favs).fillna(0).astype(int)

# Rank popularity per story (1 = heroine with most favorites in story)
df_clean['story_favorites_rank'] = df_clean.groupby('story_id')['favorites'].rank(ascending=False, method='min').astype(int)

# Summary
print(f"Total candidates: {len(df_clean)}")
print(f"Candidates with >0 favorites: {(df_clean['favorites'] > 0).sum()} / {len(df_clean)} ({(df_clean['favorites'] > 0).mean()*100:.1f}%)")

print("\nSample first 15 candidates:")
for idx, row in df_clean.head(15).iterrows():
    cid = row['candidate_id']
    print(f"{cid} (Story {row['story_id']}): {row['candidate_name']} -> {row['favorites']} favs (Rank {row['story_favorites_rank']}) [Matched: {matched_names.get(cid)}]")

# Save to data/candidates_cleaned.xlsx
try:
    df_clean.to_excel(CANDIDATES_FILE, index=False)
    print(f"\n[SUCCESS] Successfully updated {CANDIDATES_FILE}!")
except PermissionError:
    backup_file = "data/candidates_cleaned_updated.xlsx"
    df_clean.to_excel(backup_file, index=False)
    print(f"\n[WARNING] Permission denied on {CANDIDATES_FILE} (file open in Excel). Saved to {backup_file}.")
