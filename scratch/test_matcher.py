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

print(f"Loaded {len(df_clean)} cleaned candidates across {len(df_stories)} stories.")

# Build lookup from df_backup: (story_id, lower_name) -> mal_character_id
backup_name_map = {}
for _, row in df_backup.iterrows():
    if pd.notna(row['mal_character_id']) and pd.notna(row['candidate_name']) and pd.notna(row['story_id']):
        s_id = int(row['story_id'])
        c_name = str(row['candidate_name']).strip().lower()
        backup_name_map[(s_id, c_name)] = int(row['mal_character_id'])

# Also candidate_id -> mal_character_id
backup_cid_map = {}
for _, row in df_backup.iterrows():
    if pd.notna(row['mal_character_id']) and pd.notna(row['candidate_id']):
        backup_cid_map[str(row['candidate_id'])] = int(row['mal_character_id'])

# Let's map candidate_id -> mal_character_id
candidate_mal_ids = {}

for _, row in df_clean.iterrows():
    cid = row['candidate_id']
    s_id = row['story_id']
    c_name = str(row['candidate_name']).strip()
    c_name_lower = c_name.lower()

    found_id = None
    if (s_id, c_name_lower) in backup_name_map:
        found_id = backup_name_map[(s_id, c_name_lower)]
    elif cid in backup_cid_map:
        found_id = backup_cid_map[cid]

    candidate_mal_ids[cid] = found_id

missing_ids = [cid for cid, m_id in candidate_mal_ids.items() if m_id is None]
print(f"Direct backup match: {len(df_clean) - len(missing_ids)} / {len(df_clean)} matched.")
print(f"Missing count needing online search: {len(missing_ids)}")
