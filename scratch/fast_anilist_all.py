import os
import sys
import re
import time
import requests
import pandas as pd
from concurrent.futures import ThreadPoolExecutor, as_completed

sys.stdout.reconfigure(encoding='utf-8')

df_clean = pd.read_excel('data/candidates_cleaned.xlsx')
df_stories = pd.read_excel('data/stories_cleaned.xlsx')
story_dict = df_stories.set_index('story_id').to_dict(orient='index')

query_media = '''
query ($idMal: Int) {
  Media (idMal: $idMal) {
    id
    idMal
    title {
      romaji
      english
    }
    characters (perPage: 50) {
      edges {
        role
        node {
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

def process_story_group(story_id, group):
    s_info = story_dict.get(story_id, {})
    mal_id = s_info.get('mal_id')
    s_title = s_info.get('title', '')
    
    anilist_chars = []
    if pd.notna(mal_id):
        for attempt in range(2):
            try:
                r = requests.post(url, json={'query': query_media, 'variables': {'idMal': int(mal_id)}}, timeout=5)
                if r.status_code == 200 and r.json().get('data', {}).get('Media'):
                    edges = r.json()['data']['Media']['characters']['edges']
                    for edge in edges:
                        node = edge['node']
                        anilist_chars.append({
                            'id': node['id'],
                            'full_name': node['name']['full'],
                            'favs': node['favourites'] or 0
                        })
                    break
            except Exception:
                time.sleep(0.5)
                
    story_results = []
    for _, c_row in group.iterrows():
        cand_id = c_row['candidate_id']
        cand_name = str(c_row['candidate_name']).strip()
        cand_words = set(re.findall(r'\w+', cand_name.lower()))
        
        best_match_favs = None
        best_match_name = ""
        
        # Exact/subset match
        for ac in anilist_chars:
            ac_words = set(re.findall(r'\w+', ac['full_name'].lower()))
            if cand_words == ac_words or cand_words.issubset(ac_words) or ac_words.issubset(cand_words):
                best_match_favs = ac['favs']
                best_match_name = ac['full_name']
                break
                
        # Overlap match
        if best_match_favs is None:
            for ac in anilist_chars:
                ac_words = set(re.findall(r'\w+', ac['full_name'].lower()))
                overlap = cand_words & ac_words
                if len(overlap) >= 1 and not (len(overlap) == 1 and list(overlap)[0] in ['a', 'the', 'of', 'no', 'de']):
                    best_match_favs = ac['favs']
                    best_match_name = ac['full_name']
                    break
                    
        # Character search fallback
        if best_match_favs is None:
            try:
                r_c = requests.post(url, json={'query': query_char_search, 'variables': {'search': cand_name}}, timeout=5)
                if r_c.status_code == 200 and r_c.json().get('data', {}).get('Character'):
                    node = r_c.json()['data']['Character']
                    best_match_favs = node['favourites'] or 0
                    best_match_name = node['name']['full']
            except Exception:
                pass
                
        if best_match_favs is None:
            best_match_favs = 0
            
        story_results.append({
            'candidate_id': cand_id,
            'favorites': best_match_favs,
            'matched_anilist_name': best_match_name
        })
        
    return story_results

story_groups = list(df_clean.groupby('story_id'))
print(f"Processing {len(story_groups)} stories across 10 threads...")
start_t = time.time()

all_results = []
with ThreadPoolExecutor(max_workers=10) as executor:
    futures = [executor.submit(process_story_group, s_id, group) for s_id, group in story_groups]
    for future in as_completed(futures):
        res = future.result()
        all_results.extend(res)

res_df = pd.DataFrame(all_results)
print(f"Finished in {time.time() - start_t:.2f} seconds! Total records: {len(res_df)}")

# Merge back into df_clean
fav_map = dict(zip(res_df['candidate_id'], res_df['favorites']))
df_clean['favorites'] = df_clean['candidate_id'].map(fav_map).fillna(0).astype(int)

# Calculate story_favorites_rank (1 = most favorites in story)
df_clean['story_favorites_rank'] = df_clean.groupby('story_id')['favorites'].rank(ascending=False, method='min').astype(int)

# Check candidates with 0 favorites to verify coverage
zero_favs = df_clean[df_clean['favorites'] == 0]
print(f"Candidates with >0 favorites: {(df_clean['favorites'] > 0).sum()} / {len(df_clean)}")
print(f"Candidates with 0 favorites: {len(zero_favs)}")
if len(zero_favs) > 0:
    print("Sample 0 favorites candidates:")
    print(zero_favs[['candidate_id', 'story_id', 'candidate_name']].head(10))

# Save output
df_clean.to_excel('data/candidates_cleaned.xlsx', index=False)
print("\nSuccessfully updated data/candidates_cleaned.xlsx!")
