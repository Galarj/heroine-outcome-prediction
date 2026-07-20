import requests
import json

query = '''
query ($idMal: Int) {
  Media (idMal: $idMal) {
    id
    title { english romaji }
    characters (perPage: 50) {
      edges {
        role
        node {
          id
          name { full native userPreferred }
          favourites
        }
      }
    }
  }
}
'''

# Test Nisekoi manga (MAL ID 31499) and Quintessential Quintuplets manga (MAL ID 103851)
for mal_id in [31499, 103851]:
    r = requests.post('https://graphql.anilist.co', json={'query': query, 'variables': {'idMal': mal_id}})
    print(f"\n--- Media MAL ID {mal_id} ---")
    if r.status_code == 200 and r.json().get('data', {}).get('Media'):
        media = r.json()['data']['Media']
        print(f"Title: {media['title']}")
        chars = media['characters']['edges']
        for c in chars:
            node = c['node']
            print(f"  {node['name']['full']} ({node['name']['userPreferred']}) -> Favs: {node['favourites']}")
