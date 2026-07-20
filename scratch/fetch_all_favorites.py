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
            native
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
headers = {'Content-Type': 'application/json', 'Accept': 'application/json'}

candidate_favs = {}
candidate_mal_names = {}

story_groups = df_clean.groupby('story_id')
print(f"Fetching favorites for {len(df_clean)} candidates across {len(story_groups)} stories...")

for s_id, group in story_groups:
    s_info = story_dict.get(s_id, {})
    mal_id = s_info.get('mal_id')
    s_title = s_info.get('title', '')
    
    anilist_chars = []
    if pd.notna(mal_id):
        try:
            r = requests.post(url, json={'query': query_media, 'variables': {'idMal': int(mal_id)}}, headers=headers, timeout=10)
            if r.status_code == 200 and r.json().get('data', {}).get('Media'):
                edges = r.json()['data']['Media']['characters']['edges']
                for edge in edges:
                    node = edge['node']
                    anilist_chars.append({
                        'id': node['id'],
                        'full_name': node['name']['full'],
                        'favs': node['favourites'] or 0
                    })
        except Exception as e:
            print(f"  Warning: failed to query AniList for story {s_id} ({s_title}): {e}")
            
    # Match each candidate in this story
    for _, c_row in group.iterrows():
        cand_id = c_row['candidate_id']
        cand_name = str(c_row['candidate_name']).strip()
        cand_words = set(re.findall(r'\w+', cand_name.lower()))
        
        best_match_favs = None
        best_match_name = ""
        
        # 1. Try matching within story characters
        for ac in anilist_chars:
            ac_words = set(re.findall(r'\w+', ac['full_name'].lower()))
            if cand_words == ac_words or cand_words.issubset(ac_words) or ac_words.issubset(cand_words):
                best_match_favs = ac['favs']
                best_match_name = ac['full_name']
                break
                
        # If no subset match, try overlap match if high overlap
        if best_match_favs is None:
            for ac in anilist_chars:
                ac_words = set(re.findall(r'\w+', ac['full_name'].lower()))
                overlap = cand_words & ac_words
                if len(overlap) >= 1 and not (len(overlap) == 1 and list(overlap)[0] in ['a', 'the', 'of', 'no', 'de']):
                    best_match_favs = ac['favs']
                    best_match_name = ac['full_name']
                    break
                    
        # 2. Fallback: Search character directly on AniList
        if best_match_favs is None:
            time.sleep(0.3)
            try:
                r_c = requests.post(url, json={'query': query_char_search, 'variables': {'search': cand_name}}, headers=headers, timeout=10)
                if r_c.status_code == 200 and r_c.json().get('data', {}).get('Character'):
                    node = r_c.json()['data']['Character']
                    best_match_favs = node['favourites'] or 0
                    best_match_name = node['name']['full']
            except Exception:
                pass
                
        if best_match_favs is None:
            best_match_favs = 0
            
        candidate_favs[cand_id] = best_match_favs
        candidate_mal_names[cand_id] = best_match_name

print(f"\nDone fetching! Total matched: {len(candidate_favs)} / {len(df_clean)}")

df_clean['favorites'] = df_clean['candidate_id'].map(candidate_favs).fillna(0).astype(int)

# Calculate story_favorites_rank for each story
df_clean['story_favorites_rank'] = df_clean.groupby('story_id')['favorites'].rank(ascending=False, method='min').astype(int)

print("\nSummary of favorites column:")
print(df_clean['favorites'].describe())

print("\nSample top candidates by favorites:")
print(df_clean[['candidate_id', 'story_id', 'candidate_name', 'won', 'first_girl', 'favorites', 'story_favorites_rank']].sort_values('favorites', ascending=False).head(15))

# Save output preview
df_clean.to_excel('scratch/candidates_cleaned_with_favs.xlsx', index=False)
