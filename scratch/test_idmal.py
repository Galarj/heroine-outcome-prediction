import requests

query = '''
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
            native
          }
          favourites
        }
      }
    }
  }
}
'''

url = 'https://graphql.anilist.co'
r = requests.post(url, json={'query': query, 'variables': {'idMal': 31499}})
if r.status_code == 200:
    data = r.json()['data']['Media']
    print(f"Matched MAL ID 31499 -> AniList Title: {data['title']}")
    for edge in data['characters']['edges']:
        node = edge['node']
        print(f"  {node['name']['full']}: {node['favourites']} favourites")
else:
    print("Status:", r.status_code)
