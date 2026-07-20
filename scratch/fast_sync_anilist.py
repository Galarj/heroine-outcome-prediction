import os
import sys
import re
import time
import requests
import pandas as pd
from concurrent.futures import ThreadPoolExecutor, as_completed

sys.stdout.reconfigure(encoding='utf-8')

print("=== STARTING FAST MULTITHREADED FAVORITES DATA GATHERING ===")

df_clean = pd.read_excel('data/candidates_cleaned.xlsx')
df_stories = pd.read_excel('data/stories_cleaned.xlsx')

print(f"Loaded {len(df_clean)} candidates across {len(df_stories)} stories.")

query_media = '''
query ($idMal: Int) {
  Media (idMal: $idMal) {
    id
    title { english romaji }
    characters (perPage: 100) {
      edges {
        role
        node {
          id
          name { full native userPreferred alternative }
          favourites
        }
      }
    }
  }
}
'''

query_char_search = '''
query ($search: String) {
  Character (search: $search) {
    id
    name { full native userPreferred }
    favourites
  }
}
'''

url = 'https://graphql.anilist.co'
headers = {'Content-Type': 'application/json', 'Accept': 'application/json'}

stories_dict = df_stories.set_index('story_id').to_dict('index')
story_chars_cache = {}

def fetch_story(s_id, s_info):
    mal_id = s_info.get('mal_id')
    if pd.isna(mal_id) or not mal_id:
        return s_id, []
    
    mal_id = int(mal_id)
    for attempt in range(3):
        try:
            r = requests.post(url, json={'query': query_media, 'variables': {'idMal': mal_id}}, headers=headers, timeout=8)
            if r.status_code == 200 and r.json().get('data', {}).get('Media'):
                edges = r.json()['data']['Media']['characters']['edges']
                char_list = []
                for edge in edges:
                    node = edge['node']
                    names = [node['name']['full'], node['name']['userPreferred'], node['name']['native']]
                    if node['name'].get('alternative'):
                        names.extend(node['name']['alternative'])
                    char_list.append({
                        'id': node['id'],
                        'names': [n for n in names if n],
                        'favs': node['favourites'] or 0
                    })
                return s_id, char_list
        except Exception:
            pass
        time.sleep(0.3)
    return s_id, []

print("Fetching story character catalogs via AniList GraphQL in parallel...")

with ThreadPoolExecutor(max_workers=10) as executor:
    futures = [executor.submit(fetch_story, s_id, s_info) for s_id, s_info in stories_dict.items()]
    for future in as_completed(futures):
        s_id, char_list = future.result()
        story_chars_cache[s_id] = char_list

print(f"Fetched character catalogs for {len(story_chars_cache)} stories!")

# Process matching
updated_rows = []
matched_count = 0

for idx, row in df_clean.iterrows():
    cand_id = row['candidate_id']
    s_id = row['story_id']
    cname = str(row['candidate_name']).strip()
    cwords = set(re.findall(r'\w+', cname.lower()))
    
    char_list = story_chars_cache.get(s_id, [])
    best_favs = None
    matched_name = None
    
    # 1. Exact/subset match
    for c in char_list:
        for name in c['names']:
            nwords = set(re.findall(r'\w+', name.lower()))
            if cwords == nwords or cwords.issubset(nwords) or nwords.issubset(cwords):
                best_favs = c['favs']
                matched_name = name
                break
        if best_favs is not None:
            break
            
    # 2. Word overlap match
    if best_favs is None:
        for c in char_list:
            for name in c['names']:
                nwords = set(re.findall(r'\w+', name.lower()))
                overlap = cwords & nwords
                if len(overlap) >= 1 and not (len(overlap) == 1 and list(overlap)[0] in ['a', 'the', 'of', 'no', 'de', 'so', 'to', 'la', 'von']):
                    best_favs = c['favs']
                    matched_name = name
                    break
            if best_favs is not None:
                break
                
    if best_favs is None:
        best_favs = 0
    else:
        matched_count += 1
        
    row_dict = row.to_dict()
    row_dict['favorites'] = int(best_favs)
    updated_rows.append(row_dict)

res_df = pd.DataFrame(updated_rows)

# Compute story_favorites_rank
res_df['story_favorites_rank'] = res_df.groupby('story_id')['favorites'].rank(ascending=False, method='min').astype(int)

print(f"\n=== FINAL FAVORITES DATA METRICS ===")
print(f"Total candidates: {len(res_df)}")
print(f"Candidates matched to character database: {matched_count} / {len(res_df)}")
print(f"Candidates with >0 favorites: {(res_df['favorites'] > 0).sum()} / {len(res_df)}")
print(f"Candidates with 0 favorites: {(res_df['favorites'] == 0).sum()} / {len(res_df)}")

print("\nTop 15 Most Popular Candidates:")
print(res_df.sort_values('favorites', ascending=False)[['candidate_id', 'story_id', 'candidate_name', 'favorites', 'story_favorites_rank']].head(15).to_string(index=False))

# Overwrite candidates_cleaned.xlsx
res_df.to_excel('data/candidates_cleaned.xlsx', index=False)
print("\nSuccessfully saved updated data/candidates_cleaned.xlsx!")
