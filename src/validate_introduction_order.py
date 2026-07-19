import os
import sys
import re
import time
import pandas as pd
import pydantic
import google.generativeai as genai
from dotenv import load_dotenv

# Reconfigure stdout to use UTF-8 globally to prevent Windows console encoding crashes
sys.stdout.reconfigure(encoding='utf-8')

# Paths
STORIES_FILE = "data/stories_cleaned.xlsx"
CANDIDATES_FILE = "data/candidates_cleaned.xlsx"
REVIEW_REPORT_FILE = "data/introduction_order_review.xlsx"

# Pydantic schema for structured output from Gemini
class CandidateValidation(pydantic.BaseModel):
    candidate_name: str
    introduction_order: int
    reason: str

class StoryValidationResult(pydantic.BaseModel):
    story_title: str
    changes_made: bool
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
    def __init__(self, keys, model_name="gemini-flash-lite-latest"):
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
        print(f"   [API Key Pool] Switched to key index {self.current_idx + 1}/{len(self.keys)}")

def main():
    print("=== Automated introduction_order Validation Utility ===")
    
    # 1. Load data
    if not os.path.exists(STORIES_FILE) or not os.path.exists(CANDIDATES_FILE):
        print(f"Error: Required files not found. Ensure {STORIES_FILE} and {CANDIDATES_FILE} exist.")
        sys.exit(1)
        
    stories_df = pd.read_excel(STORIES_FILE, keep_default_na=False)
    candidates_df = pd.read_excel(CANDIDATES_FILE, keep_default_na=False)
    
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
            c_order = c_row["introduction_order"]
            c_list_str += f"- Name: {c_name} (Current introduction_order: {c_order})\n"
            c_map[c_name.lower()] = c_order
            
        prompt = f"""You are validating the `introduction_order` column for a romance media dataset.

Definition:

`introduction_order` is the chronological order in which a character becomes a legitimate romantic candidate in the ORIGINAL source material.

Rules:

- Assign unique integers starting from 1.
- Exactly one candidate must have introduction_order = 1.
- Numbers must be consecutive (1, 2, 3, ...).
- Judge based on when the candidate becomes a legitimate romantic interest, NOT simply their first visual appearance.
- Ignore background cameos or non-romantic appearances.
- Use the original manga/light novel/visual novel as the source of truth.
- If the current ordering is incorrect, return the corrected ordering.
- Briefly explain any changes.

Story:
{story_title}

Candidates:
{c_list_str}

Return ONLY valid JSON:
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
                        temperature=0.1
                    )
                )
                
                parsed_output = StoryValidationResult.model_validate_json(response.text)
                success = True
                break
            except Exception as e:
                err_str = str(e)
                if "429" in err_str or "quota" in err_str.lower() or "limit" in err_str.lower():
                    print(f"   [API Limit] Rate limited on key {model_pool.current_idx + 1}. Rotating...")
                    model_pool.rotate()
                    time.sleep(2.0)
                else:
                    print(f"   [Error] Attempt {attempt + 1}/{api_retries} failed for '{story_title}': {e}")
                    time.sleep(backoff)
                    backoff *= 2.0
                    
        if not success:
            print(f"   [API Failure] Skipped Story ID {story_id} due to persistent failures.")
            continue
            
        # Parse result and compare
        returned_names = [c.candidate_name.lower() for c in parsed_output.candidates]
        
        for p_cand in parsed_output.candidates:
            c_name = p_cand.candidate_name
            p_order = p_cand.introduction_order
            reason = p_cand.reason
            
            # Match current order
            curr_order = c_map.get(c_name.lower())
            if curr_order is None:
                # Try finding soft match
                soft_match = None
                for orig_name in c_map.keys():
                    if orig_name in c_name.lower() or c_name.lower() in orig_name:
                        soft_match = orig_name
                        break
                if soft_match:
                    curr_order = c_map[soft_match]
                    c_name = candidates_group[candidates_group["candidate_name"].str.lower() == soft_match].iloc[0]["candidate_name"]
                else:
                    curr_order = "N/A"
                    
            changed = "Yes" if str(curr_order) != str(p_order) else "No"
            approved = "Yes" if changed == "Yes" else "No"
            
            review_rows.append({
                "story_id": story_id,
                "story_title": story_title,
                "candidate_name": c_name,
                "current_introduction_order": curr_order,
                "proposed_introduction_order": p_order,
                "changed": changed,
                "approved": approved,
                "reason": reason
            })
            
        print(f"   Processed. Changes proposed: {'Yes' if parsed_output.changes_made else 'No'}")
        
        # Save temporary progress to avoid losing API runs
        if review_rows:
            temp_df = pd.DataFrame(review_rows)
            temp_df.to_excel(REVIEW_REPORT_FILE, index=False)
            
        time.sleep(2.0)
        
    if review_rows:
        final_df = pd.DataFrame(review_rows)
        final_df.to_excel(REVIEW_REPORT_FILE, index=False)
        print(f"\nSuccessfully generated review report at: {REVIEW_REPORT_FILE}")
    else:
        print("\nNo validation rows could be generated.")

if __name__ == "__main__":
    main()
