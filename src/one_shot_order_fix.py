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
    proposed_introduction_order: int = pydantic.Field(description="Consecutive unique index starting from 1 based on when they become romantic interest.")
    introduction_reason: str = pydantic.Field(description="Brief 1-sentence explanation of their romantic interest debut.")
    proposed_appearance_order: int = pydantic.Field(description="Chronological index starting from 1 of when they first visually debut.")
    proposed_first_chapter_or_episode: str = pydantic.Field(description="First chapter or episode name/number where they debut.")
    appearance_reason: str = pydantic.Field(description="Brief 1-sentence explanation of their first debut.")

class StoryValidationResult(pydantic.BaseModel):
    story_title: str
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
    def __init__(self, keys, model_name="gemini-2.5-flash"):
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
    print("=== One-Shot Consolidated Curation & Validation Utility ===")
    
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
        
    # 2. Setup Gemini
    keys = load_all_api_keys()
    print(f"Loaded a pool of {len(keys)} Gemini API keys from .env.")
    model_pool = RotatingModelPool(keys)
    
    # Group candidates by story_id
    grouped_candidates = candidates_df.groupby("story_id")
    
    review_rows = []
    
    # 3. Process each story
    for idx, (story_id, candidates_group) in enumerate(grouped_candidates):
        # Find story title
        story_rows = stories_df[stories_df["story_id"] == story_id]
        if story_rows.empty:
            print(f"[{idx+1}] Warning: Story ID {story_id} not found in stories table. Skipping.")
            continue
            
        story_title = story_rows.iloc[0]["title"]
        print(f"\n[{idx+1}/{len(grouped_candidates)}] Processing Story ID {story_id}: '{story_title}'...")
        
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
1. `introduction_order`: The chronological order in which a character becomes a legitimate romantic candidate in the ORIGINAL source material.
   - Rules:
     - Assign unique integers starting from 1.
     - Exactly one candidate must have introduction_order = 1.
     - Numbers must be consecutive (1, 2, 3, ...).
     - Judge based on when the candidate becomes a legitimate romantic interest, NOT simply their first visual appearance.
     - Ignore background cameos or non-romantic appearances.

2. `appearance_order`: The chronological order in which each major romantic candidate FIRST appears in the ORIGINAL source material.
   - Rules:
     - Assign appearance_order starting from 1.
     - Order candidates by their first appearance in the original source material.
     - If two or more candidates first appear in the SAME chapter (or the same episode when using an anime original), assign them the SAME appearance_order.
     - If multiple candidates share the same appearance_order, the next order should continue sequentially (e.g. Chapter 1 has Candidate A and B (order 1), Chapter 3 has Candidate C (order 2)).
     - Ignore flashbacks unless properly introduced as a major candidate.
     - Ignore unnamed cameos and background appearances.

Story:
{story_title}

Candidates to evaluate:
{c_list_str}

Please return the validated orders matching the requested JSON schema.
"""
        
        success = False
        api_retries = 3
        backoff = 4.0
        
        for attempt in range(api_retries):
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
                    time.sleep(2.0)
                else:
                    print(f"   [Error] Attempt {attempt + 1}/{api_retries} failed: {e}")
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
        for p_cand in parsed_output.candidates:
            c_name = p_cand.candidate_name
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
            curr_intro = match_row["introduction_order"]
            curr_app = match_row.get("appearance_order")
            curr_chap = match_row.get("first_chapter_or_episode")
            
            # Determine changes
            intro_changed = "No"
            if pd.isna(curr_intro) or str(curr_intro) == "" or int(curr_intro) != int(p_intro):
                intro_changed = "Yes"
                
            app_changed = "No"
            if pd.isna(curr_app) or str(curr_app) == "" or int(curr_app) != int(p_app):
                app_changed = "Yes"
                
            # If current chapter is empty, marked as changed
            if pd.isna(curr_chap) or str(curr_chap) == "" or str(curr_chap).strip().lower() != str(p_chap).strip().lower():
                app_changed = "Yes"
                
            review_rows.append({
                "candidate_id": c_id,
                "story_id": story_id,
                "story_title": story_title,
                "candidate_name": match_row["candidate_name"],
                "current_introduction_order": curr_intro,
                "proposed_introduction_order": p_intro,
                "introduction_changed": intro_changed,
                "introduction_reason": intro_reason,
                "current_appearance_order": curr_app if not pd.isna(curr_app) else "",
                "proposed_appearance_order": p_app,
                "proposed_first_chapter_or_episode": p_chap,
                "appearance_changed": app_changed,
                "appearance_reason": app_reason,
                "approved": "Yes" # Default to approved so it can be merged easily
            })
            
            # Update the candidate dataframe in-memory immediately
            row_idx = candidates_df[candidates_df["candidate_id"] == c_id].index
            if len(row_idx) > 0:
                candidates_df.loc[row_idx, "introduction_order"] = int(p_intro)
                candidates_df.loc[row_idx, "appearance_order"] = int(p_app)
                candidates_df.loc[row_idx, "first_chapter_or_episode"] = str(p_chap)
                
        print(f"   Processed.")
        
        # Save checkpoints after every 5 stories so we don't lose data
        if (idx + 1) % 5 == 0:
            try:
                candidates_df.to_excel(CANDIDATES_FILE, index=False)
                pd.DataFrame(review_rows).to_excel(CONSOLIDATED_REVIEW_FILE, index=False)
                print("   [Checkpoint Saved] Wrote progress to candidates_cleaned.xlsx and review report.")
            except PermissionError:
                print("   [Warning] Excel file locked. Could not write checkpoint. Please close candidates_cleaned.xlsx in Excel!")
                
    # 4. Save final output files
    try:
        candidates_df.to_excel(CANDIDATES_FILE, index=False)
        print(f"\nSuccessfully wrote final updates to: {CANDIDATES_FILE}")
    except PermissionError:
        print(f"\n[Error] Permission denied writing to {CANDIDATES_FILE}. Ensure it is closed in Excel!")
        
    try:
        review_df = pd.DataFrame(review_rows)
        review_df.to_excel(CONSOLIDATED_REVIEW_FILE, index=False)
        print(f"Successfully generated consolidated review report at: {CONSOLIDATED_REVIEW_FILE}")
    except PermissionError:
        print(f"[Error] Permission denied writing to {CONSOLIDATED_REVIEW_FILE}. Ensure it is closed in Excel!")
        
    # 5. Run post-cleaning validation pipeline
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
