import requests
import pandas as pd
import re
import time

df_clean = pd.read_excel('data/candidates_cleaned.xlsx')
df_stories = pd.read_excel('data/stories_cleaned.xlsx')

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
    characters (perPage: 50) {
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

candidate_favs = {}
matched_info = {}

for s_id, group in df_clean.groupby('story_id'):
    s_info = story_dict.get(s_id, {})
    mal_id = s_info.get('mal_id')
    medium = s_info.get('medium', 'Manga')
    
    primary_type = 'MANGA' if str(medium).lower() in ['manga', 'light novel', 'novel', 'visual novel'] else 'ANIME'
    types_to_try = [primary_type, 'ANIME' if primary_type == 'MANGA' else 'MANGA']
    
    nodes = []
    if pd.notna(mal_id):
        for mtype in types_to_try:
            try:
                r = requests.post(url, json={'query': query_media, 'variables': {'idMal': int(mal_id), 'type': mtype}}, headers=headers, timeout=5)
                if r.status_code == 200 and r.json().get('data', {}).get('Media'):
                    res_nodes = r.json()['data']['Media']['characters']['nodes']
                    if res_nodes:
                        nodes = res_nodes
                        break
            except Exception:
                pass
                
    for _, c_row in group.iterrows():
        cand_id = c_row['candidate_id']
        cand_name = str(c_row['candidate_name']).strip()
        cand_words = set(re.findall(r'\w+', cand_name.lower()))
        
        favs = None
        matched_name = ""
        
        # 1. First Pass: Exact or Subset word match in story characters
        for n in nodes:
            full_n = n['name']['full']
            n_words = set(re.findall(r'\w+', full_n.lower()))
            if cand_words == n_words or cand_words.issubset(n_words) or n_words.issubset(cand_words):
                favs = n['favourites'] or 0
                matched_name = full_n
                break
                
        # 2. Second Pass: Last name or First name match in story characters
        if favs is None:
            for n in nodes:
                full_n = n['name']['full']
                n_words = set(re.findall(r'\w+', full_n.lower()))
                overlap = cand_words & n_words
                # filter out generic terms
                overlap_meaningful = [w for w in overlap if w not in ['a', 'the', 'of', 'no', 'de', 'san', 'chan', 'kun', 'sama', 'onee', 'imouto']]
                if overlap_meaningful:
                    favs = n['favourites'] or 0
                    matched_name = full_n
                    break
                    
        # 3. Fallback Pass: Direct character search on AniList
        if favs is None:
            time.sleep(0.2)
            try:
                r_c = requests.post(url, json={'query': query_char_search, 'variables': {'search': cand_name}}, headers=headers, timeout=5)
                if r_c.status_code == 200 and r_c.json().get('data', {}).get('Character'):
                    node = r_c.json()['data']['Character']
                    favs = node['favourites'] or 0
                    matched_name = node['name']['full']
            except Exception:
                pass
                
        if favs is None:
            favs = 0
            
        candidate_favs[cand_id] = favs
        matched_info[cand_id] = matched_name

# Update df_clean
df_clean['favorites'] = df_clean['candidate_id'].map(candidate_favs).fillna(0).astype(int)
df_clean['story_favorites_rank'] = df_clean.groupby('story_id')['favorites'].rank(ascending=False, method='min').astype(int)

# Print first 20 candidates
print("Sample Results (First 20 candidates):")
for idx, row in df_clean.head(25).iterrows():
    cid = row['candidate_id']
    print(f"{cid} (Story {row['story_id']}): {row['candidate_name']} -> {row['favorites']} favs (Rank {row['story_favorites_rank']}) [Matched: {matched_info.get(cid)}]")
