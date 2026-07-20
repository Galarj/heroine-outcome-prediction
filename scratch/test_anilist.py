import requests

query = '''
query ($search: String) {
  Character (search: $search) {
    id
    name {
      full
      native
    }
    favourites
    siteUrl
  }
}
'''

url = 'https://graphql.anilist.co'

test_names = ['Chitoge Kirisaki', 'Kosaki Onodera', 'Miku Nakano', 'Yukino Yukinoshita', 'Taiga Aisaka']

for name in test_names:
    r = requests.post(url, json={'query': query, 'variables': {'search': name}})
    if r.status_code == 200:
        c = r.json()['data']['Character']
        print(f"{c['name']['full']}: {c['favourites']} favourites ({c['siteUrl']})")
    else:
        print(f"Failed for {name}: {r.status_code}")
