import requests

query = '''
query ($search: String) {
  Media (search: $search) {
    id
    title {
      romaji
      english
    }
    characters (perPage: 25) {
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
r = requests.post(url, json={'query': query, 'variables': {'search': 'Nisekoi'}})
if r.status_code == 200:
    data = r.json()['data']['Media']
    print("Media:", data['title'])
    for edge in data['characters']['edges']:
        node = edge['node']
        print(f"  [{edge['role']}] {node['name']['full']} (ID: {node['id']}): {node['favourites']} favourites")
else:
    print("Status:", r.status_code, r.text)
