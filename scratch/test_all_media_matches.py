import requests
import pandas as pd
import re

df_clean = pd.read_excel('data/candidates_cleaned.xlsx')
df_stories = pd.read_excel('data/stories_cleaned.xlsx')

story_dict = df_stories.set_index('story_id').to_dict(orient='index')

query = '''
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
        }
        favourites
      }
    }
  }
}
'''

url = 'https://graphql.anilist.co'

matched_candidates = 0
total_candidates = len(df_clean)

for s_id, group in df_clean.groupby('story_id'):
    s_info = story_dict.get(s_id, {})
    mal_id = s_info.get('mal_id')
    medium = str(s_info.get('medium', 'Manga')).lower()
    
    # Determine AniList MediaType priority
    primary_type = 'MANGA' if medium in ['manga', 'light novel', 'novel', 'visual novel'] else 'ANIME'
    types_to_try = [primary_type, 'ANIME' if primary_type == 'MANGA' else 'MANGA']
    
    nodes = []
    for mtype in types_to_try:
        if pd.notna(mal_id):
            r = requests.post(url, json={'query': query, 'variables': {'idMal': int(mal_id), 'type': mtype}})
            if r.status_code == 200 and r.json().get('data', {}).get('Media'):
                nodes = r.json()['data']['Media']['characters']['nodes']
                if nodes:
                    break
                    
    for _, c_row in group.iterrows():
        cand_name = str(c_row['candidate_name']).strip()
        cand_words = set(re.findall(r'\w+', cand_name.lower()))
        
        found = False
        for node in nodes:
            ac_words = set(re.findall(r'\w+', node['name']['full'].lower()))
            if cand_words == ac_words or cand_words.issubset(ac_words) or ac_words.issubset(cand_words) or (cand_words & ac_words and len(cand_words & ac_words) >= 1 and not (len(cand_words & ac_words) == 1 and list(cand_words & ac_words)[0] in ['a', 'the', 'of', 'no', 'de', 'san', 'chan'])):
                found = True
                matched_candidates += 1
                break

print(f"Matched candidates: {matched_candidates} / {total_candidates} ({matched_candidates/total_candidates*100:.1f}%)")
