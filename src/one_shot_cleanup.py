import google.generativeai as genai
import os
import sys
import re
import time
import pandas as pd
import pydantic
from dotenv import load_dotenv

# Reconfigure stdout to use UTF-8 globally to prevent Windows console encoding crashes
sys.stdout.reconfigure(encoding='utf-8')

# Paths
STORIES_FILE = "data/stories_cleaned.xlsx"
CANDIDATES_FILE = "data/candidates_cleaned.xlsx"
CONSOLIDATED_REVIEW_FILE = "data/consolidated_order_review.xlsx"

# Pydantic schema for structured output from Gemini
class CandidateValidation(pydantic.BaseModel):
    candidate_name: str
    is_love_interest: bool = pydantic.Field(description="Set to true if they are a legitimate romantic interest of the protagonist in the original source material. Set to false for family members (unless incestuous/romantic interest), pets, background/classmate characters who never have any romantic path, chemistry, or feelings for/from the protagonist.")
    proposed_introduction_order: int = pydantic.Field(description="Consecutive unique index starting from 1 based on when they become romantic interest.")
    introduction_reason: str = pydantic.Field(description="Brief 1-sentence explanation of their romantic interest debut.")
    proposed_appearance_order: int = pydantic.Field(description="Chronological index starting from 1 of when they first visually debut.")
    proposed_first_chapter_or_episode: str = pydantic.Field(description="First chapter or episode name/number where they debut.")
    appearance_reason: str = pydantic.Field(description="Brief 1-sentence explanation of their first debut.")

class StoryValidationResult(pydantic.BaseModel):
    general_explanation: str = pydantic.Field(description="A brief general explanation or overview of the candidate introductions and appearances.")
    candidates: list[CandidateValidation]

def load_all_api_keys():
    """
    Parse the .env file at project root, parent root, or grandparent root,
    and extract all unique Gemini API keys.
    """
    script_dir = os.path.dirname(os.path.abspath(__file__))
    keys = []
    current_dir = script_dir
    for _ in range(4):
        env_path = os.path.join(current_dir, ".env")
        if os.path.exists(env_path):
            try:
                with open(env_path, "r", encoding="utf-8") as f:
                    content = f.read()
                    found = re.findall(r"(AQ\.[A-Za-z0-9_\-]+|AIzaSy[A-Za-z0-9_\-]+)", content)
                    for k in found:
                        if k not in keys:
                            keys.append(k)
            except Exception:
                pass
        current_dir = os.path.dirname(current_dir)
        
    return keys

class RotatingModelPool:
    def __init__(self, keys, model_name="gemini-3.1-flash-lite"):
        self.keys = keys
        self.model_name = model_name
        self.current_idx = 0
        if not self.keys:
            print("Error: No API keys loaded!")
            sys.exit(1)
            
    def get_model(self):
        key = self.keys[self.current_idx]
        genai.configure(api_key=key)
        return genai.GenerativeModel(self.model_name)
        
    def rotate(self):
        self.current_idx = (self.current_idx + 1) % len(self.keys)
        from google.generativeai import client
        client._client_manager.clients.clear()
        print(f"   [API Key Pool] Switched to key index {self.current_idx + 1}/{len(self.keys)}")

def clean_json_string(text):
    text = text.strip()
    if text.startswith("```"):
        newline_idx = text.find("\n")
        if newline_idx != -1:
            text = text[newline_idx:].strip()
        if text.endswith("```"):
            text = text[:-3].strip()
    return text

def main():
    print("=== Self-Healing Curation Cleanup Pass ===")
    
    # 1. Load data
    if not os.path.exists(STORIES_FILE) or not os.path.exists(CANDIDATES_FILE):
        print(f"Error: Required files not found. Ensure {STORIES_FILE} and {CANDIDATES_FILE} exist.")
        sys.exit(1)
        
    stories_df = pd.read_excel(STORIES_FILE, keep_default_na=False)
    candidates_df = pd.read_excel(CANDIDATES_FILE, keep_default_na=False)
    
    # Ensure validation columns exist in candidates_df
    if "appearance_order" not in candidates_df.columns:
        candidates_df["appearance_order"] = pd.NA
    if "first_chapter_or_episode" not in candidates_df.columns:
        candidates_df["first_chapter_or_episode"] = pd.NA
        
    # Load existing review rows to prevent overwriting successful progress
    review_rows = []
    if os.path.exists(CONSOLIDATED_REVIEW_FILE):
        try:
            old_review_df = pd.read_excel(CONSOLIDATED_REVIEW_FILE, keep_default_na=False)
            review_rows = old_review_df.to_dict(orient="records")
            print(f"Loaded {len(review_rows)} existing review rows from {CONSOLIDATED_REVIEW_FILE}.")
        except Exception as e:
            print(f"Could not load existing review report: {e}")
            
    # Find which story_ids are missing appearance_order
    # A story is missing if any of its candidates has an empty or null appearance_order
    missing_stories = []
    grouped_candidates = candidates_df.groupby("story_id")
    for story_id, candidates_group in grouped_candidates:
        has_missing = False
        for _, c_row in candidates_group.iterrows():
            curr_app = c_row.get("appearance_order")
            if pd.isna(curr_app) or str(curr_app) == "":
                has_missing = True
                break
        if has_missing:
            missing_stories.append(story_id)
            
    if not missing_stories:
        print("All stories have been fully validated! No missing records found.")
        # Trigger post-cleaning script just in case to make sure everything is completely in order
        run_post_cleaning()
        return
        
    print(f"Found {len(missing_stories)} stories missing validation data. Commencing cleanup pass...")
    
    # 2. Setup Gemini
    keys = load_all_api_keys()
    print(f"Loaded a pool of {len(keys)} Gemini API keys from .env.")
    model_pool = RotatingModelPool(keys)
    
    # 3. Process each missing story
    for idx, story_id in enumerate(missing_stories):
        # Find candidates for this story
        candidates_group = candidates_df[candidates_df["story_id"] == story_id]
        
        # Find story title
        story_rows = stories_df[stories_df["story_id"] == story_id]
        if story_rows.empty:
            print(f"[{idx+1}/{len(missing_stories)}] Warning: Story ID {story_id} not found in stories table. Skipping.")
            continue
            
        story_title = story_rows.iloc[0]["title"]
        print(f"\n[{idx+1}/{len(missing_stories)}] Processing Story ID {story_id}: '{story_title}'...")
        
        # Prepare candidate list for prompt
        c_list_str = ""
        c_map = {}
        for _, c_row in candidates_group.iterrows():
            c_name = c_row["candidate_name"]
            c_id = c_row["candidate_id"]
            curr_intro = c_row["introduction_order"]
            curr_app = c_row.get("appearance_order", "None")
            curr_chap = c_row.get("first_chapter_or_episode", "None")
            
            if pd.isna(curr_intro) or curr_intro == "": curr_intro = "None"
            if pd.isna(curr_app) or curr_app == "": curr_app = "None"
            if pd.isna(curr_chap) or curr_chap == "": curr_chap = "None"
            
            c_list_str += f"- ID: {c_id} | Name: {c_name} (Current introduction_order: {curr_intro}, Current appearance_order: {curr_app}, Current First Chapter/Episode: {curr_chap})\n"
            c_map[c_name.lower()] = c_row
            
        prompt = f"""You are an expert romance media archivist. Your task is to validate both `introduction_order` and `appearance_order` for the heroine candidates of a story.

Definitions:
1. `is_love_interest`: Identify whether the candidate is a legitimate romantic interest of the protagonist.
   - Set to `true` if they are a romantic candidate or have a legitimate romantic arc/feelings for the protagonist.
   - Set to `false` for family members (unless incestuous/romantic interest), pets, background classmates, or friends who have absolutely no romantic storylines or feelings with/for the protagonist.

2. `introduction_order`: The chronological order in which a character becomes a legitimate romantic candidate in the ORIGINAL source material.
   - Rules:
     - Assign unique consecutive integers starting from 1 for characters who are love interests (is_love_interest = true).
     - Exactly one candidate must have introduction_order = 1.
     - Numbers must be consecutive (1, 2, 3, ...).
     - Judge based on when the candidate becomes a legitimate romantic interest, NOT simply their first visual appearance.
     - For characters who are NOT love interests (is_love_interest = false), assign introduction_order = 99.

3. `appearance_order`: The chronological order in which each major romantic candidate FIRST appears in the ORIGINAL source material.
   - Rules:
     - Assign appearance_order starting from 1.
     - Order candidates by their first appearance in the original source material.
     - If two or more candidates first appear in the SAME chapter (or the same episode when using an anime original), assign them the SAME appearance_order.
     - If multiple candidates share the same appearance_order, the next order should continue sequentially (e.g. Chapter 1 has Candidate A and B (order 1), Chapter 3 has Candidate C (order 2)).
     - Ignore flashbacks unless properly introduced as a major candidate.
     - Ignore unnamed cameos and background appearances.
     - For characters who are NOT love interests (is_love_interest = false), assign appearance_order = 99.

Story:
{story_title}

Candidates to evaluate:
{c_list_str}

Please return the validated orders matching the requested JSON schema.

Crucial Schema Rules:
1. Put all general notes, explanations, or warnings about childhood friends or character drops in the `general_explanation` field.
2. You MUST return an entry in `candidates` for every single candidate listed in the input list, even if is_love_interest = false.
"""
        
        success = False
        attempts = 0
        max_attempts = 3
        backoff = 10.0
        response = None
        
        while attempts < max_attempts:
            try:
                model = model_pool.get_model()
                response = model.generate_content(
                    prompt,
                    generation_config=genai.GenerationConfig(
                        response_mime_type="application/json",
                        response_schema=StoryValidationResult,
                        temperature=0.2
                    ),
                    request_options={"timeout": 60.0}
                )
                
                cleaned_text = clean_json_string(response.text)
                parsed_output = StoryValidationResult.model_validate_json(cleaned_text)
                success = True
                break
            except Exception as e:
                err_str = str(e)
                if "429" in err_str or "quota" in err_str.lower() or "limit" in err_str.lower():
                    print(f"   [API Limit] Rate limited on key {model_pool.current_idx + 1}. Rotating...")
                    model_pool.rotate()
                    time.sleep(25.0)
                else:
                    attempts += 1
                    print(f"   [Error] Attempt {attempts}/{max_attempts} failed: {e}. Rotating key...")
                    model_pool.rotate()
                    if response is not None:
                        try:
                            print(f"   [Raw Response text]: {response.text}")
                        except Exception:
                            pass
                    time.sleep(backoff)
                    backoff *= 2.0
                    
        if not success:
            print(f"   [API Failure] Skipped Story ID {story_id} due to persistent failures.")
            continue
            
        # Parse result and compare
        returned_c_ids = set()
        valid_candidates = []
        
        for p_cand in parsed_output.candidates:
            c_name = p_cand.candidate_name
            is_li = p_cand.is_love_interest
            p_intro = p_cand.proposed_introduction_order
            p_app = p_cand.proposed_appearance_order
            p_chap = p_cand.proposed_first_chapter_or_episode
            intro_reason = p_cand.introduction_reason
            app_reason = p_cand.appearance_reason
            
            # Find the match
            match_row = c_map.get(c_name.lower())
            if match_row is None:
                # Try soft match
                for orig_name in c_map.keys():
                    if c_name.lower() in orig_name or orig_name in c_name.lower():
                        match_row = c_map[orig_name]
                        break
                        
            if match_row is None:
                print(f"   [Match Warning] Could not find candidate '{c_name}' in dataset. Skipping.")
                continue
                
            c_id = match_row["candidate_id"]
            returned_c_ids.add(c_id)
            
            if not is_li:
                print(f"   [Drop Candidate] Candidate '{match_row['candidate_name']}' (ID: {c_id}) is classified as NOT a love interest. Dropping from dataset.")
                candidates_df = candidates_df[candidates_df["candidate_id"] != c_id]
                review_rows = [r for r in review_rows if r["candidate_id"] != c_id]
                continue
                
            valid_candidates.append({
                "candidate_id": c_id,
                "candidate_name": match_row["candidate_name"],
                "match_row": match_row,
                "temp_intro": int(p_intro),
                "temp_app": int(p_app),
                "p_chap": str(p_chap),
                "intro_reason": intro_reason,
                "app_reason": app_reason
            })
            
        # Handle omitted candidates by dropping them (since they are likely not love interests)
        for _, c_row in candidates_group.iterrows():
            c_name = c_row["candidate_name"]
            c_id = c_row["candidate_id"]
            if c_id not in returned_c_ids:
                print(f"   [Drop Omitted Candidate] Candidate '{c_name}' (ID: {c_id}) was omitted by Gemini. Dropping from dataset.")
                candidates_df = candidates_df[candidates_df["candidate_id"] != c_id]
                review_rows = [r for r in review_rows if r["candidate_id"] != c_id]
                
        # Re-sequence introduction and appearance orders for remaining valid candidates
        if valid_candidates:
            # 1. Introduction Order re-sequencing
            valid_candidates.sort(key=lambda x: x["temp_intro"])
            for new_intro, item in enumerate(valid_candidates, start=1):
                item["final_intro"] = new_intro
                
            # 2. Appearance Order re-sequencing (preserving ties)
            valid_candidates.sort(key=lambda x: x["temp_app"])
            new_app = 1
            last_temp_app = None
            for item in valid_candidates:
                temp_app = item["temp_app"]
                if last_temp_app is not None and temp_app != last_temp_app:
                    new_app += 1
                item["final_app"] = new_app
                last_temp_app = temp_app
                
            # 3. Apply updates to candidates_df and generate review entries
            new_review_entries = []
            for item in valid_candidates:
                c_id = item["candidate_id"]
                final_intro = item["final_intro"]
                final_app = item["final_app"]
                p_chap = item["p_chap"]
                match_row = item["match_row"]
                
                curr_intro = match_row["introduction_order"]
                curr_app = match_row.get("appearance_order")
                curr_chap = match_row.get("first_chapter_or_episode")
                
                # Determine changes
                intro_changed = "No"
                if pd.isna(curr_intro) or str(curr_intro) == "" or int(curr_intro) != final_intro:
                    intro_changed = "Yes"
                    
                app_changed = "No"
                if pd.isna(curr_app) or str(curr_app) == "" or int(curr_app) != final_app:
                    app_changed = "Yes"
                    
                if pd.isna(curr_chap) or str(curr_chap) == "" or str(curr_chap).strip().lower() != p_chap.strip().lower():
                    app_changed = "Yes"
                    
                new_review_entries.append({
                    "candidate_id": c_id,
                    "story_id": story_id,
                    "story_title": story_title,
                    "candidate_name": item["candidate_name"],
                    "current_introduction_order": curr_intro,
                    "proposed_introduction_order": final_intro,
                    "introduction_changed": intro_changed,
                    "introduction_reason": item["intro_reason"],
                    "current_appearance_order": curr_app if not pd.isna(curr_app) else "",
                    "proposed_appearance_order": final_app,
                    "proposed_first_chapter_or_episode": p_chap,
                    "appearance_changed": app_changed,
                    "appearance_reason": item["app_reason"],
                    "approved": "Yes"
                })
                
                # Update candidate dataframe in memory immediately
                row_idx = candidates_df[candidates_df["candidate_id"] == c_id].index
                if len(row_idx) > 0:
                    candidates_df.loc[row_idx, "introduction_order"] = final_intro
                    candidates_df.loc[row_idx, "appearance_order"] = final_app
                    candidates_df.loc[row_idx, "first_chapter_or_episode"] = p_chap
                    
            # Append new entries to review report, removing any duplicates if they existed
            existing_ids = [r["candidate_id"] for r in review_rows]
            for entry in new_review_entries:
                if entry["candidate_id"] in existing_ids:
                    idx_to_replace = existing_ids.index(entry["candidate_id"])
                    review_rows[idx_to_replace] = entry
                else:
                    review_rows.append(entry)
                
        print(f"   Processed.")
        
        # Save checkpoints immediately after EVERY story to make it fully self-healing and progress-safe
        try:
            candidates_df.to_excel(CANDIDATES_FILE, index=False)
            pd.DataFrame(review_rows).to_excel(CONSOLIDATED_REVIEW_FILE, index=False)
        except PermissionError:
            print("   [Warning] Excel file locked. Could not write checkpoint. Please close candidates_cleaned.xlsx in Excel!")
            
        # Pacing sleep of 15.0 seconds to prevent hitting rate limits
        time.sleep(15.0)
        
    print("\nAll missing stories processed successfully!")
    run_post_cleaning()

def run_post_cleaning():
    print("\nTriggering post-cleaning script to re-sort, assign sequential candidate IDs, and run validation assertions...")
    import subprocess
    res = subprocess.run(["python", "src/post_clean_shoujo.py"], capture_output=True, text=True)
    if res.returncode == 0:
        print("=== Post-cleaning success ===")
        print(res.stdout)
    else:
        print("=== Post-cleaning failed ===")
        print(res.stderr)

if __name__ == "__main__":
    main()
