import os
import sys
import re
import time
import requests
import pandas as pd

sys.stdout.reconfigure(encoding='utf-8')

df_clean = pd.read_excel('data/candidates_cleaned.xlsx')
df_stories = pd.read_excel('data/stories_cleaned.xlsx').set_index('story_id').to_dict('index')

print(f"Candidates before AniList fill: {(df_clean['favorites'] > 0).sum()} >0, {(df_clean['favorites'] == 0).sum()} 0")

query_media = '''
query ($idMal: Int) {
  Media (idMal: $idMal) {
    id
    characters (perPage: 100) {
      nodes {
        id
        name { full userPreferred native alternative }
        favourites
      }
    }
  }
}
'''

url = 'https://graphql.anilist.co'
headers = {'Content-Type': 'application/json', 'Accept': 'application/json'}

# Find stories that have 0 favorites for candidates
zero_stories = df_clean[df_clean['favorites'] == 0]['story_id'].unique()
print(f"Querying AniList for {len(zero_stories)} stories with zero-favorite candidates...")

filled_count = 0

for sid in zero_stories:
    sinfo = df_stories.get(sid, {})
    mal_id = sinfo.get('mal_id')
    if not mal_id or pd.isna(mal_id):
        continue
        
    try:
        r = requests.post(url, json={'query': query_media, 'variables': {'idMal': int(mal_id)}}, headers=headers, timeout=8)
        if r.status_code == 200 and r.json().get('data', {}).get('Media'):
            nodes = r.json()['data']['Media']['characters']['nodes']
            chars = []
            for n in nodes:
                names = [n['name']['full'], n['name']['userPreferred'], n['name']['native']]
                if n['name'].get('alternative'):
                    names.extend(n['name']['alternative'])
                chars.append({'names': [x for x in names if x], 'favs': n['favourites'] or 0})
                
            # Match 0-favorite candidates in this story
            story_zeros = df_clean[(df_clean['story_id'] == sid) & (df_clean['favorites'] == 0)]
            for idx, row in story_zeros.iterrows():
                cname = str(row['candidate_name']).strip()
                cwords = set(re.findall(r'\w+', cname.lower()))
                
                matched_fav = 0
                for c in chars:
                    for n in c['names']:
                        nwords = set(re.findall(r'\w+', n.lower()))
                        if cwords == nwords or cwords.issubset(nwords) or nwords.issubset(cwords):
                            matched_fav = c['favs']
                            break
                    if matched_fav > 0:
                        break
                        
                if matched_fav > 0:
                    df_clean.loc[idx, 'favorites'] = matched_fav
                    filled_count += 1
    except Exception:
        pass
    time.sleep(0.1)

print(f"Filled {filled_count} candidate favorite counts from AniList!")

# Recalculate story_favorites_rank
df_clean['story_favorites_rank'] = df_clean.groupby('story_id')['favorites'].rank(ascending=False, method='min').astype(int)

print(f"\nFinal Candidates with >0 favorites: {(df_clean['favorites'] > 0).sum()} / {len(df_clean)}")
print(f"Final Candidates with 0 favorites: {(df_clean['favorites'] == 0).sum()} / {len(df_clean)}")

print("\nSample (Nisekoi & Quintuplets):")
print(df_clean[df_clean['story_id'].isin([1, 2])][['candidate_id', 'story_id', 'candidate_name', 'favorites', 'story_favorites_rank']])

# Overwrite candidates_cleaned.xlsx
df_clean.to_excel('data/candidates_cleaned.xlsx', index=False)
print("\nSuccessfully updated data/candidates_cleaned.xlsx!")
