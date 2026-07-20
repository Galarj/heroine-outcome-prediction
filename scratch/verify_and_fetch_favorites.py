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
df_stories = pd.read_excel('data/stories_cleaned.xlsx')
df_backup = pd.read_excel('data/candidates_raw_backup.xlsx')

story_dict = df_stories.set_index('story_id').to_dict(orient='index')

# Build initial candidate_id -> mal_character_id from backup
backup_cid_map = dict(zip(df_backup['candidate_id'], df_backup['mal_character_id']))

# We will cache character page results: char_id -> {'name': str, 'favorites': int}
char_cache = {}

def fetch_char_details(char_id):
    if not char_id or pd.isna(char_id):
        return None
    char_id = int(char_id)
    if char_id in char_cache:
        return char_cache[char_id]

    url = f'https://myanimelist.net/character/{char_id}'
    try:
        r = requests.get(url, headers=headers, timeout=10)
        if r.status_code == 200:
            soup = BeautifulSoup(r.text, 'html.parser')
            title_tag = soup.find('h1', class_='title-name')
            name = title_tag.text.strip() if title_tag else ""
            
            fav = 0
            m = re.search(r'Member Favorites:\s*([\d,]+)', r.text)
            if m:
                fav = int(m.group(1).replace(',', ''))
            
            res = {'char_id': char_id, 'name': name, 'favorites': fav}
            char_cache[char_id] = res
            return res
    except Exception as e:
        pass
    return None

def fetch_story_characters_mal(mal_id, medium):
    if pd.isna(mal_id):
        return []
    mal_id = int(mal_id)
    m_types = ['manga', 'anime'] if medium.lower() in ['manga', 'light novel', 'visual novel', 'novel'] else ['anime', 'manga']
    
    chars = []
    for m_type in m_types:
        url = f'https://myanimelist.net/{m_type}/{mal_id}/characters'
        try:
            r = requests.get(url, headers=headers, timeout=10)
            if r.status_code == 200:
                soup = BeautifulSoup(r.text, 'html.parser')
                for a in soup.find_all('a', href=re.compile(r'/character/(\d+)')):
                    m = re.search(r'/character/(\d+)', a['href'])
                    cid = int(m.group(1))
                    cname = a.text.strip()
                    if cname and (cid, cname) not in chars:
                        chars.append((cid, cname))
                if chars:
                    break
        except Exception:
            pass
    return chars

# Let's process stories in parallel
results = []
story_groups = list(df_clean.groupby('story_id'))

print(f"Starting verification and retrieval for {len(df_clean)} candidates across {len(story_groups)} stories...")

def process_story(story_id, group):
    s_info = story_dict.get(story_id, {})
    s_title = s_info.get('title', '')
    mal_id = s_info.get('mal_id')
    medium = str(s_info.get('medium', 'Manga'))

    # Fetch story character list from MAL for precise matching
    story_mal_chars = fetch_story_characters_mal(mal_id, medium)
    
    story_results = []
    for _, row in group.iterrows():
        cand_id = row['candidate_id']
        cand_name = str(row['candidate_name']).strip()
        cand_words = set(re.findall(r'\w+', cand_name.lower()))

        init_mal_id = backup_cid_map.get(cand_id)
        
        # Verify if init_mal_id matches candidate_name
        verified_id = None
        verified_favs = 0
        verified_mal_name = ""

        if init_mal_id and pd.notna(init_mal_id):
            details = fetch_char_details(init_mal_id)
            if details:
                mal_words = set(re.findall(r'\w+', details['name'].lower()))
                # Check if there is name overlap
                if cand_words & mal_words:
                    verified_id = int(init_mal_id)
                    verified_favs = details['favorites']
                    verified_mal_name = details['name']

        # If not verified from backup ID, search in story_mal_chars
        if verified_id is None and story_mal_chars:
            for sm_id, sm_name in story_mal_chars:
                sm_words = set(re.findall(r'\w+', sm_name.lower()))
                if cand_words == sm_words or cand_words.issubset(sm_words) or sm_words.issubset(cand_words) or (cand_words & sm_words and len(cand_words & sm_words) >= 1):
                    # Check details of this candidate
                    details = fetch_char_details(sm_id)
                    if details:
                        verified_id = int(sm_id)
                        verified_favs = details['favorites']
                        verified_mal_name = details['name']
                        break

        # Fallback if still no favs fetched
        if verified_id and verified_favs == 0:
            details = fetch_char_details(verified_id)
            if details:
                verified_favs = details['favorites']
                verified_mal_name = details['name']

        story_results.append({
            'candidate_id': cand_id,
            'story_id': story_id,
            'candidate_name': cand_name,
            'mal_character_id': verified_id,
            'mal_character_name': verified_mal_name,
            'mal_favorites': verified_favs
        })
    return story_results

with ThreadPoolExecutor(max_workers=10) as executor:
    futures = [executor.submit(process_story, s_id, group) for s_id, group in story_groups]
    for future in as_completed(futures):
        res = future.result()
        results.extend(res)

res_df = pd.DataFrame(results).sort_values('candidate_id')
print(f"\nDone processing! Total candidates: {len(res_df)}")
print(f"Candidates with verified mal_character_id: {res_df['mal_character_id'].notna().sum()}")
print(f"Candidates with >0 mal_favorites: {(res_df['mal_favorites'] > 0).sum()}")
print(res_df.head(15))

res_df.to_csv('scratch/favorites_retrieved.csv', index=False, encoding='utf-8-sig')
