import pandas as pd
import os

def validate_curated():
    s_path = "data/stories_cleaned.xlsx"
    c_path = "data/candidates_cleaned.xlsx"
    
    if not os.path.exists(s_path) or not os.path.exists(c_path):
        print("Curated Excel files are missing!")
        return
        
    # Read files with keep_default_na=False so that string 'None' is not treated as null
    df_s = pd.read_excel(s_path, keep_default_na=False)
    df_c = pd.read_excel(c_path, keep_default_na=False)
    
    print(f"Loaded {len(df_s)} stories.")
    print(f"Loaded {len(df_c)} candidates.")
    
    # Check nulls
    nulls_s = df_s.isnull().sum().sum() + (df_s == "").sum().sum()
    nulls_c = df_c.isnull().sum().sum() + (df_c == "").sum().sum()
    print(f"Blank/empty cells in stories: {nulls_s}")
    print(f"Blank/empty cells in candidates: {nulls_c}")
    
    # Check constraints
    stories_without_single_winner = []
    stories_without_single_first_girl = []
    heroine_count_mismatches = []
    
    for _, s_row in df_s.iterrows():
        sid = s_row["story_id"]
        title = s_row["title"]
        medium = s_row["medium"]
        expected_hc = s_row["heroine_count"]
        
        cands = df_c[df_c["story_id"] == sid]
        won_sum = cands["won"].astype(int).sum()
        fg_sum = cands["first_girl"].astype(int).sum()
        
        if len(cands) != expected_hc:
            heroine_count_mismatches.append(f"- '{title}' (ID {sid}): expected={expected_hc}, candidates={len(cands)}")
            
        is_vn = medium.lower() in ["visual novel"]
        
        # We expect exactly 1 winner, unless it is a visual novel/choose-route or ongoing/no-winner
        if won_sum != 1:
            if not is_vn and won_sum != 0:
                stories_without_single_winner.append(f"- '{title}' (ID {sid}): won_sum={won_sum}")
        if fg_sum != 1 and len(cands) > 0:
            stories_without_single_first_girl.append(f"- '{title}' (ID {sid}): first_girl_sum={fg_sum}")
            
    print("\n--- Validation Results ---")
    if heroine_count_mismatches:
        print("Heroine count mismatches found:")
        for m in heroine_count_mismatches:
            print(m)
    else:
        print("Success: All heroine counts match perfectly!")
        
    if stories_without_single_winner:
        print("Stories without exactly one winner (excluding VNs):")
        for w in stories_without_single_winner:
            print(w)
    else:
        print("Success: All stories (excluding VNs) have exactly one canonical winner!")
        
    if stories_without_single_first_girl:
        print("Stories without exactly one first girl:")
        for fg in stories_without_single_first_girl:
            print(fg)
    else:
        print("Success: All stories have exactly one first girl!")

if __name__ == "__main__":
    validate_curated()
