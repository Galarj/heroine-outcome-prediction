import os
import sys
import pandas as pd

sys.stdout.reconfigure(encoding='utf-8')

df_clean = pd.read_excel('data/candidates_cleaned.xlsx')
df_report = pd.read_csv('scratch/mal_favorites_full_report.csv')

fav_map = dict(zip(df_report['candidate_id'], df_report['favorites']))

df_clean['favorites'] = df_clean.apply(
    lambda r: max(r['favorites'], fav_map.get(r['candidate_id'], 0)),
    axis=1
)

df_clean['story_favorites_rank'] = df_clean.groupby('story_id')['favorites'].rank(ascending=False, method='min').astype(int)

print(f"Total candidates: {len(df_clean)}")
print(f"Candidates with >0 favorites: {(df_clean['favorites'] > 0).sum()} / {len(df_clean)}")

print("\nSample (Nisekoi & Quintuplets):")
print(df_clean[df_clean['story_id'].isin([1, 2])][['candidate_id', 'story_id', 'candidate_name', 'favorites', 'story_favorites_rank']])

df_clean.to_excel('data/candidates_cleaned.xlsx', index=False)
print("\nSuccessfully saved data/candidates_cleaned.xlsx!")
