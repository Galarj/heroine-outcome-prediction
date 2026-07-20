import requests

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
for mtype in ['MANGA', 'ANIME']:
    r = requests.post(url, json={'query': query, 'variables': {'idMal': 31499, 'type': mtype}})
    if r.status_code == 200 and r.json().get('data', {}).get('Media'):
        data = r.json()['data']['Media']
        print(f"{mtype} -> Title: {data['title']} ({len(data['characters']['nodes'])} chars)")
        for c in data['characters']['nodes'][:5]:
            print(f"   {c['name']['full']}: {c['favourites']}")
