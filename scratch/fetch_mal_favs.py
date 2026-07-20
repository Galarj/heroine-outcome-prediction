import os
import sys
import re
import time
import requests
import pandas as pd
from bs4 import BeautifulSoup
from concurrent.futures import ThreadPoolExecutor, as_completed

sys.stdout.reconfigure(encoding='utf-8')

headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'}

df_clean = pd.read_excel('data/candidates_cleaned.xlsx')
df_backup = pd.read_excel('data/candidates_raw_backup.xlsx')

cid_to_mal = dict(zip(df_backup['candidate_id'], df_backup['mal_character_id']))

df_clean['mal_character_id'] = df_clean['candidate_id'].map(cid_to_mal)

def fetch_char_info(row):
    cand_id = row['candidate_id']
    cand_name = row['candidate_name']
    mal_id = row['mal_character_id']
    
    if pd.isna(mal_id) or not mal_id:
        return {'candidate_id': cand_id, 'mal_character_id': None, 'mal_name': None, 'mal_favorites': 0, 'status': 'missing_id'}
    
    mal_id = int(mal_id)
    url = f'https://myanimelist.net/character/{mal_id}'
    
    for attempt in range(3):
        try:
            r = requests.get(url, headers=headers, timeout=8)
            if r.status_code == 200:
                soup = BeautifulSoup(r.text, 'html.parser')
                title_tag = soup.find('h1', class_='title-name')
                mal_name = title_tag.text.strip() if title_tag else ""
                
                fav = 0
                m = re.search(r'Member Favorites:\s*([\d,]+)', r.text)
                if m:
                    fav = int(m.group(1).replace(',', ''))
                
                return {
                    'candidate_id': cand_id,
                    'mal_character_id': mal_id,
                    'mal_name': mal_name,
                    'mal_favorites': fav,
                    'status': 'ok'
                }
            elif r.status_code == 404:
                return {'candidate_id': cand_id, 'mal_character_id': mal_id, 'mal_name': None, 'mal_favorites': 0, 'status': '404'}
        except Exception:
            pass
        time.sleep(1.0)
        
    return {'candidate_id': cand_id, 'mal_character_id': mal_id, 'mal_name': None, 'mal_favorites': 0, 'status': 'error'}

print(f"Starting fetch for {len(df_clean)} candidates...")
start_time = time.time()

results = []
rows = df_clean.to_dict('records')

with ThreadPoolExecutor(max_workers=20) as executor:
    futures = {executor.submit(fetch_char_info, r): r['candidate_id'] for r in rows}
    for future in as_completed(futures):
        res = future.result()
        results.append(res)
        if len(results) % 50 == 0 or len(results) == len(df_clean):
            print(f"Progress: {len(results)}/{len(df_clean)} fetched in {time.time() - start_time:.1f}s")

res_df = pd.DataFrame(results).sort_values('candidate_id')
print(f"\nCompleted in {time.time() - start_time:.1f}s!")
print(f"Status counts:\n{res_df['status'].value_counts()}")
print(f"Candidates with >0 favorites: {(res_df['mal_favorites'] > 0).sum()}")

# Check sample
print("\nSample results:")
print(res_df.head(20))

res_df.to_csv('scratch/mal_favs_direct.csv', index=False, encoding='utf-8-sig')
