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
df_back = pd.read_excel('data/candidates_raw_backup.xlsx')
df_stories = pd.read_excel('data/stories_cleaned.xlsx').set_index('story_id').to_dict('index')

# Map by name and story_id
df_back['norm_name'] = df_back['candidate_name'].str.strip().str.lower()
df_clean['norm_name'] = df_clean['candidate_name'].str.strip().str.lower()

name_map = dict(zip(zip(df_back['story_id'], df_back['norm_name']), df_back['mal_character_id']))
df_clean['mal_character_id'] = df_clean.apply(lambda r: name_map.get((r['story_id'], r['norm_name'])), axis=1)

print(f"Mapped {df_clean['mal_character_id'].notna().sum()} / {len(df_clean)} candidates directly from backup.")

missing = df_clean[df_clean['mal_character_id'].isna()]
print(f"Missing {len(missing)} candidates across {missing['story_id'].nunique()} stories.")

story_mal_cache = {}

def get_story_characters_mal(sid):
    if sid in story_mal_cache:
        return story_mal_cache[sid]
    
    sinfo = df_stories.get(sid, {})
    mal_id = sinfo.get('mal_id')
    medium = str(sinfo.get('medium', 'Manga')).lower()
    
    if not mal_id or pd.isna(mal_id):
        story_mal_cache[sid] = []
        return []
    
    mal_id = int(mal_id)
    # Search anime first or manga first based on medium
    m_types = ['anime', 'manga'] if medium in ['anime', 'original anime'] else ['manga', 'anime']
    
    found_chars = []
    for mt in m_types:
        url = f'https://myanimelist.net/{mt}/{mal_id}/characters'
        try:
            r = requests.get(url, headers=headers, timeout=10)
            if r.status_code == 200:
                soup = BeautifulSoup(r.text, 'html.parser')
                links = soup.find_all('a', href=re.compile(r'/character/(\d+)'))
                seen = set()
                for a in links:
                    m = re.search(r'/character/(\d+)', a['href'])
                    if m:
                        cid = int(m.group(1))
                        cname = a.text.strip()
                        if cid not in seen and cname:
                            seen.add(cid)
                            found_chars.append({'cid': cid, 'name': cname})
                if found_chars:
                    break
        except Exception:
            pass
        time.sleep(0.5)
        
    story_mal_cache[sid] = found_chars
    return found_chars

# Let's test resolving missing candidates
resolved_count = 0
for idx, row in missing.iterrows():
    sid = row['story_id']
    cname = row['candidate_name']
    cwords = set(re.findall(r'\w+', cname.lower()))
    
    chars = get_story_characters_mal(sid)
    matched_id = None
    matched_name = None
    
    for c in chars:
        mwords = set(re.findall(r'\w+', c['name'].lower()))
        if cwords == mwords or cwords.issubset(mwords) or mwords.issubset(cwords) or (len(cwords & mwords) >= 1 and not (len(cwords & mwords) == 1 and list(cwords & mwords)[0] in ['a', 'the', 'of', 'no', 'de', 'so', 'to'])):
            matched_id = c['cid']
            matched_name = c['name']
            break
            
    if matched_id:
        resolved_count += 1
        df_clean.loc[idx, 'mal_character_id'] = matched_id
        print(f"[RESOLVED] {cname} (Story {sid}) -> MAL ID {matched_id} ({matched_name})")
    else:
        print(f"[UNRESOLVED] {cname} (Story {sid})")

print(f"\nTotal resolved missing: {resolved_count} / {len(missing)}")
print(f"Total candidates now with MAL ID: {df_clean['mal_character_id'].notna().sum()} / {len(df_clean)}")
