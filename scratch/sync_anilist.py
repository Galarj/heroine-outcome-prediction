import os
import sys
import re
import time
import requests
import pandas as pd

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

def make_request(query, variables):
    for attempt in range(4):
        try:
            r = requests.post(url, json={'query': query, 'variables': variables}, timeout=8)
            if r.status_code == 200:
                return r.json()
            elif r.status_code == 429:
                sleep_t = int(r.headers.get('Retry-After', 2)) + 1
                time.sleep(sleep_t)
            else:
                time.sleep(1.0)
        except Exception:
            time.sleep(1.0)
    return None

story_groups = list(df_clean.groupby('story_id'))
print(f"Processing {len(story_groups)} stories sequentially with rate limit protection...")

candidate_favs = {}
candidate_matched_names = {}

for idx, (story_id, group) in enumerate(story_groups):
    s_info = story_dict.get(story_id, {})
    mal_id = s_info.get('mal_id')
    s_title = s_info.get('title', '')
    
    anilist_chars = []
    if pd.notna(mal_id):
        res = make_request(query_media, {'idMal': int(mal_id)})
        if res and res.get('data', {}).get('Media'):
            edges = res['data']['Media']['characters']['edges']
            for edge in edges:
                node = edge['node']
                anilist_chars.append({
                    'id': node['id'],
                    'full_name': node['name']['full'],
                    'favs': node['favourites'] or 0
                })
                
    for _, c_row in group.iterrows():
        cand_id = c_row['candidate_id']
        cand_name = str(c_row['candidate_name']).strip()
        cand_words = set(re.findall(r'\w+', cand_name.lower()))
        
        best_match_favs = None
        best_match_name = ""
        
        # 1. Exact / subset match in story characters
        for ac in anilist_chars:
            ac_words = set(re.findall(r'\w+', ac['full_name'].lower()))
            if cand_words == ac_words or cand_words.issubset(ac_words) or ac_words.issubset(cand_words):
                best_match_favs = ac['favs']
                best_match_name = ac['full_name']
                break
                
        # 2. Overlap match
        if best_match_favs is None:
            for ac in anilist_chars:
                ac_words = set(re.findall(r'\w+', ac['full_name'].lower()))
                overlap = cand_words & ac_words
                if len(overlap) >= 1 and not (len(overlap) == 1 and list(overlap)[0] in ['a', 'the', 'of', 'no', 'de']):
                    best_match_favs = ac['favs']
                    best_match_name = ac['full_name']
                    break
                    
        # 3. Direct character search fallback
        if best_match_favs is None:
            res_c = make_request(query_char_search, {'search': cand_name})
            if res_c and res_c.get('data', {}).get('Character'):
                node = res_c['data']['Character']
                best_match_favs = node['favourites'] or 0
                best_match_name = node['name']['full']
                
        if best_match_favs is None:
            best_match_favs = 0
            
        candidate_favs[cand_id] = best_match_favs
        candidate_matched_names[cand_id] = best_match_name

    if (idx + 1) % 10 == 0 or (idx + 1) == len(story_groups):
        print(f"  Progress: {idx + 1}/{len(story_groups)} stories processed ({len(candidate_favs)} candidates)...")
        
    time.sleep(0.3)

df_clean['favorites'] = df_clean['candidate_id'].map(candidate_favs).fillna(0).astype(int)
df_clean['story_favorites_rank'] = df_clean.groupby('story_id')['favorites'].rank(ascending=False, method='min').astype(int)

# Verify statistics
print("\n--- Processing Results ---")
print(f"Total candidates: {len(df_clean)}")
print(f"Candidates with >0 favorites: {(df_clean['favorites'] > 0).sum()} ({(df_clean['favorites'] > 0).mean()*100:.1f}%)")
print(f"Max favorites: {df_clean['favorites'].max()}")
print(f"Median favorites: {df_clean['favorites'].median()}")

# Save to data/candidates_cleaned.xlsx
df_clean.to_excel('data/candidates_cleaned.xlsx', index=False)
print("\n[SUCCESS] Updated data/candidates_cleaned.xlsx with 'favorites' and 'story_favorites_rank'!")
