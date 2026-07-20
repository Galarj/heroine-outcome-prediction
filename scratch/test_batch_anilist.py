import requests
import pandas as pd

df_backup = pd.read_excel('data/candidates_raw_backup.xlsx')
mal_ids = [int(x) for x in df_backup['mal_character_id'].dropna().unique() if x > 0]
print(f"Total candidate MAL IDs: {len(mal_ids)}")

query = '''
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

url = 'https://graphql.anilist.co'
batch = mal_ids[:50]
r = requests.post(url, json={'query': query, 'variables': {'ids': batch}})
print('Status:', r.status_code)
if r.status_code == 200:
    chars = r.json()['data']['Page']['characters']
    print(f'Fetched {len(chars)} characters in 1 single request!')
    for c in chars[:10]:
        print(f"  ID {c['id']}: {c['name']['full']} - {c['favourites']} favourites")
