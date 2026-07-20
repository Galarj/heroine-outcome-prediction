import os
import sys
import re
import time
import requests
import pandas as pd

sys.stdout.reconfigure(encoding='utf-8')

CANDIDATES_FILE = "data/candidates_cleaned.xlsx"
STORIES_FILE = "data/stories_cleaned.xlsx"
BACKUP_FILE = "data/candidates_raw_backup.xlsx"

df_clean = pd.read_excel(CANDIDATES_FILE)
df_stories = pd.read_excel(STORIES_FILE)
df_backup = pd.read_excel(BACKUP_FILE)

# Map candidate_id -> mal_character_id from backup
cid_to_mal = dict(zip(df_backup['candidate_id'], df_backup['mal_character_id']))

# Map candidate_id to mal_id
df_clean['mal_character_id'] = df_clean['candidate_id'].map(cid_to_mal)

print(f"Loaded {len(df_clean)} candidates. Valid MAL IDs count: {df_clean['mal_character_id'].notna().sum()}")

query_batch = '''
query ($ids: [Int]) {
  Page (perPage: 50) {
    characters (id_in: $ids) {
      id
      name {
        full
      }
      favourites
    }
  }
}
'''

query_media = '''
query ($idMal: Int, $type: MediaType) {
  Media (idMal: $idMal, type: $type) {
    id
    characters (perPage: 50) {
      nodes {
        id
        name {
          full
        }
        favourites
      }
    }
  }
}
'''

url = 'https://graphql.anilist.co'
headers = {'Content-Type': 'application/json', 'Accept': 'application/json'}

char_favs = {}
char_names = {}

# 1. Batch query all candidate mal_character_ids
valid_cids = [int(x) for x in df_clean['mal_character_id'].dropna().unique() if x > 0]

print(f"Executing batch query for {len(valid_cids)} character IDs in batches of 50...")

for i in range(0, len(valid_cids), 50):
    batch = valid_cids[i:i+50]
    try:
        r = requests.post(url, json={'query': query_batch, 'variables': {'ids': batch}}, headers=headers, timeout=10)
        if r.status_code == 200 and r.json().get('data', {}).get('Page'):
            for c in r.json()['data']['Page']['characters']:
                char_favs[c['id']] = c['favourites'] or 0
                char_names[c['id']] = c['name']['full']
    except Exception as e:
        print(f"Batch query error: {e}")
    time.sleep(0.3)

print(f"Batch query retrieved {len(char_favs)} character records!")

# Check candidates missing from batch query
missing_candidates = []
for _, row in df_clean.iterrows():
    cid = row['candidate_id']
    mal_cid = row['mal_character_id']
    if pd.notna(mal_cid) and int(mal_cid) in char_favs:
        pass
    else:
        missing_candidates.append(row)

print(f"Missing candidates after batch query: {len(missing_candidates)}")

# 2. For missing candidates, query story media to resolve
story_dict = df_stories.set_index('story_id').to_dict(orient='index')
if missing_candidates:
    print(f"Resolving remaining {len(missing_candidates)} candidates via Story Media queries...")
    missing_df = pd.DataFrame(missing_candidates)
    for s_id, group in missing_df.groupby('story_id'):
        s_info = story_dict.get(s_id, {})
        mal_id = s_info.get('mal_id')
        medium = s_info.get('medium', 'Manga')
        
        mtype = 'MANGA' if str(medium).lower() in ['manga', 'light novel', 'novel', 'visual novel'] else 'ANIME'
        if pd.notna(mal_id):
            try:
                r = requests.post(url, json={'query': query_media, 'variables': {'idMal': int(mal_id), 'type': mtype}}, headers=headers, timeout=10)
                if r.status_code == 200 and r.json().get('data', {}).get('Media'):
                    nodes = r.json()['data']['Media']['characters']['nodes']
                    for _, c_row in group.iterrows():
                        cand_id = c_row['candidate_id']
                        cand_name = str(c_row['candidate_name']).strip()
                        cand_words = set(re.findall(r'\w+', cand_name.lower()))
                        
                        for node in nodes:
                            n_words = set(re.findall(r'\w+', node['name']['full'].lower()))
                            if cand_words == n_words or cand_words.issubset(n_words) or n_words.issubset(cand_words) or (cand_words & n_words):
                                char_favs[c_row['mal_character_id']] = node['favourites'] or 0
                                break
            except Exception as e:
                pass

# Populate candidates_cleaned dataframe
df_clean['favorites'] = df_clean['mal_character_id'].apply(lambda cid: char_favs.get(int(cid), 0) if pd.notna(cid) else 0)

# Drop temporary mal_character_id column so candidates_cleaned layout matches exact spec
df_clean = df_clean.drop(columns=['mal_character_id'])

# Rank popularity per story (1 = heroine with most favorites in story)
df_clean['story_favorites_rank'] = df_clean.groupby('story_id')['favorites'].rank(ascending=False, method='min').astype(int)

# Print Summary Statistics
print("\n=== Dataset Popularity Summary ===")
print(f"Total candidate rows: {len(df_clean)}")
print(f"Candidates with >0 favorites: {(df_clean['favorites'] > 0).sum()} / {len(df_clean)} ({(df_clean['favorites'] > 0).mean()*100:.1f}%)")
print(f"Max favorites: {df_clean['favorites'].max()}")
print(f"Average favorites: {df_clean['favorites'].mean():.1f}")

print("\nSample top candidate rows with favorites and popularity rank:")
print(df_clean[['candidate_id', 'story_id', 'candidate_name', 'won', 'first_girl', 'favorites', 'story_favorites_rank']].sort_values('favorites', ascending=False).head(15))

# Save to data/candidates_cleaned.xlsx (handling Excel permission lock)
try:
    df_clean.to_excel(CANDIDATES_FILE, index=False)
    print(f"\n[SUCCESS] Successfully updated {CANDIDATES_FILE}!")
except PermissionError:
    backup_path = "data/candidates_cleaned_updated.xlsx"
    df_clean.to_excel(backup_path, index=False)
    print(f"\n[WARNING] Permission denied on {CANDIDATES_FILE} (file is currently open in Excel).")
    print(f"Saved updated file to: {backup_path}")
