import os
import sys
import re
import time
import requests
import pandas as pd

sys.stdout.reconfigure(encoding='utf-8')

df_clean = pd.read_excel('data/candidates_cleaned.xlsx')
df_stories = pd.read_excel('data/stories_cleaned.xlsx')
df_raw = pd.read_excel('data/candidates_raw_backup.xlsx')

story_dict = df_stories.set_index('story_id').to_dict(orient='index')

# Query to get up to 50 characters per media
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
print(f"Starting optimized batch retrieval across {len(story_groups)} stories...")

for idx, (story_id, group) in enumerate(story_groups):
    s_info = story_dict.get(story_id, {})
    mal_id = s_info.get('mal_id')
    s_title = s_info.get('title', '')
    
    anilist_chars = []
    if pd.notna(mal_id):
        try:
            r = requests.post(url, json={'query': query_media, 'variables': {'idMal': int(mal_id)}}, headers=headers, timeout=5)
            if r.status_code == 200 and r.json().get('data', {}).get('Media'):
                nodes = r.json()['data']['Media']['characters']['nodes']
                for node in nodes:
                    anilist_chars.append({
                        'id': node['id'],
                        'full_name': node['name']['full'],
                        'favs': node['favourites'] or 0
                    })
        except Exception:
            pass
            
    # For each candidate in group
    for _, c_row in group.iterrows():
        cand_id = c_row['candidate_id']
        cand_name = str(c_row['candidate_name']).strip()
        cand_words = set(re.findall(r'\w+', cand_name.lower()))
        
        found_favs = 0
        found_name = ""
        
        # Match against story characters
        for ac in anilist_chars:
            ac_words = set(re.findall(r'\w+', ac['full_name'].lower()))
            # exact or subset match
            if cand_words == ac_words or cand_words.issubset(ac_words) or ac_words.issubset(cand_words) or (cand_words & ac_words and len(cand_words & ac_words) >= 1 and not (len(cand_words & ac_words) == 1 and list(cand_words & ac_words)[0] in ['a', 'the', 'of', 'no', 'de', 'san', 'chan'])):
                found_favs = ac['favs']
                found_name = ac['full_name']
                break
                
        candidate_favs[cand_id] = found_favs
        matched_names[cand_id] = found_name

print("Done! Mapping results...")
df_clean['favorites'] = df_clean['candidate_id'].map(candidate_favs).fillna(0).astype(int)

# Rank popularity per story (1 = most favorites)
df_clean['story_favorites_rank'] = df_clean.groupby('story_id')['favorites'].rank(ascending=False, method='min').astype(int)

# Let's inspect coverage
print(f"Total candidates: {len(df_clean)}")
print(f"Candidates with >0 favorites: {(df_clean['favorites'] > 0).sum()} / {len(df_clean)} ({(df_clean['favorites'] > 0).mean()*100:.1f}%)")

df_clean.to_excel('data/candidates_cleaned.xlsx', index=False)
print("Saved to data/candidates_cleaned.xlsx successfully!")
