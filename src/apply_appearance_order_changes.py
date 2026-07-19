import os
import sys
import pandas as pd
import subprocess

# Paths
CANDIDATES_FILE = "data/candidates_cleaned.xlsx"
REVIEW_REPORT_FILE = "data/appearance_order_review.xlsx"
POST_CLEAN_SCRIPT = "src/post_clean_shoujo.py"

def main():
    print("=== Apply Approved appearance_order Changes ===")
    
    # 1. Load data
    if not os.path.exists(REVIEW_REPORT_FILE):
        print(f"Error: Review report {REVIEW_REPORT_FILE} not found. Please run the validation utility first.")
        sys.exit(1)
        
    if not os.path.exists(CANDIDATES_FILE):
        print(f"Error: Candidates file {CANDIDATES_FILE} not found.")
        sys.exit(1)
        
    review_df = pd.read_excel(REVIEW_REPORT_FILE, keep_default_na=False)
    candidates_df = pd.read_excel(CANDIDATES_FILE, keep_default_na=False)
    
    # Ensure new columns exist in candidates_df
    if "appearance_order" not in candidates_df.columns:
        print("Adding 'appearance_order' column to candidates table.")
        candidates_df["appearance_order"] = pd.NA
    if "first_chapter_or_episode" not in candidates_df.columns:
        print("Adding 'first_chapter_or_episode' column to candidates table.")
        candidates_df["first_chapter_or_episode"] = pd.NA
        
    # Check for approval column
    if "approved" not in review_df.columns:
        print("Note: 'approved' column not found in review report. Defaulting to applying all rows where changed is 'Yes'.")
        apply_mask = review_df["changed"].astype(str).str.lower() == "yes"
    else:
        apply_mask = review_df["approved"].astype(str).str.lower() == "yes"
        
    approved_changes = review_df[apply_mask]
    
    if approved_changes.empty:
        print("No approved changes found to apply.")
        sys.exit(0)
        
    print(f"Found {len(approved_changes)} approved changes to apply.")
    
    applied_count = 0
    # 2. Apply updates in memory
    for _, row in approved_changes.iterrows():
        sid = row["story_id"]
        c_name = row["candidate_name"]
        new_order = row["proposed_appearance_order"]
        new_chap = row["proposed_first_chapter_or_episode"]
        
        # Match in candidates_df
        cond = (candidates_df["story_id"] == sid) & (candidates_df["candidate_name"].str.lower() == c_name.lower())
        if cond.any():
            orig_order = candidates_df.loc[cond, "appearance_order"].values[0]
            candidates_df.loc[cond, "appearance_order"] = int(new_order)
            candidates_df.loc[cond, "first_chapter_or_episode"] = str(new_chap)
            
            print(f"   -> Story ID {sid} | {c_name}: appearance_order {orig_order} -> {new_order} ({new_chap})")
            applied_count += 1
        else:
            print(f"   [Warning] Could not find candidate '{c_name}' in Story ID {sid} to update.")
            
    if applied_count == 0:
        print("No changes could be successfully matched and applied.")
        sys.exit(0)
        
    # 3. Save updated candidates dataframe
    try:
        candidates_df.to_excel(CANDIDATES_FILE, index=False)
        print(f"\nSuccessfully saved updated candidates to: {CANDIDATES_FILE}")
    except PermissionError:
        print(f"\n[Permission Error] Could not write to {CANDIDATES_FILE}. Ensure it is closed in Excel and try again.")
        sys.exit(1)
        
    # 4. Trigger post-cleaning script to regenerate IDs, validate, and update report
    if os.path.exists(POST_CLEAN_SCRIPT):
        print(f"\nTriggering post-cleaning script: {POST_CLEAN_SCRIPT}...")
        try:
            result = subprocess.run([sys.executable, POST_CLEAN_SCRIPT], capture_output=True, text=True, check=True)
            print(result.stdout)
            print("Successfully completed post-cleaning and validation checks.")
        except subprocess.CalledProcessError as e:
            print(f"\n[Error] post-cleaning script failed:\n{e.stderr}")
            sys.exit(1)
    else:
        print(f"\n[Warning] Post-cleaning script {POST_CLEAN_SCRIPT} not found. Skipping re-indexing and validation.")

if __name__ == "__main__":
    main()
