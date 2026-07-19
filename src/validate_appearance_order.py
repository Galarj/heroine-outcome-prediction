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
REVIEW_REPORT_FILE = "data/appearance_order_review.xlsx"

# Pydantic schema for structured output from Gemini
class CandidateAppearance(pydantic.BaseModel):
    candidate_name: str
    appearance_order: int
    first_chapter_or_episode: str = pydantic.Field(description="The first chapter or episode number/name where they appear.")
    reason: str = pydantic.Field(description="A short 1-sentence justification (max 15 words) explaining the first appearance.")

class StoryAppearanceResult(pydantic.BaseModel):
    story_title: str
    candidates: list[CandidateAppearance]

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
    def __init__(self, keys, model_name="gemini-flash-latest"):
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
    print("=== Automated appearance_order Validation Utility ===")
    
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
        c_chap_map = {}
        
        for _, c_row in candidates_group.iterrows():
            c_name = c_row["candidate_name"]
            
            # Fetch current values if the columns exist
            curr_order = c_row.get("appearance_order") if "appearance_order" in candidates_df.columns else None
            curr_chap = c_row.get("first_chapter_or_episode") if "first_chapter_or_episode" in candidates_df.columns else None
            
            if pd.isna(curr_order):
                curr_order = "None"
            if pd.isna(curr_chap):
                curr_chap = "None"
                
            c_list_str += f"- Name: {c_name} (Current appearance_order: {curr_order}, First Chapter/Episode: {curr_chap})\n"
            c_map[c_name.lower()] = curr_order
            c_chap_map[c_name.lower()] = curr_chap
            
        prompt = f"""You are an expert curator of Japanese romance media.

Your task is to validate the `appearance_order` column for a romance dataset.

## Definition

`appearance_order` is the chronological order in which each major romantic candidate FIRST appears in the ORIGINAL source material.

Use the original manga, light novel, visual novel, or anime (only if the anime is the original source).

This field measures FIRST APPEARANCE ONLY.
It does NOT measure romantic development, importance, screen time, or who wins.

---

## Rules

- Assign appearance_order starting from 1.
- Order candidates by their first appearance in the original source material.
- If two or more candidates first appear in the SAME chapter (or the same episode when using an anime original), assign them the SAME appearance_order.
- If multiple candidates share the same appearance_order, the next order should continue sequentially.

Example:

Chapter 1:
- Candidate A
- Candidate B

Chapter 3:
- Candidate C

Chapter 8:
- Candidate D

Output:

A → 1
B → 1
C → 2
D → 3

- Ignore flashbacks unless the character is properly introduced as a major romantic candidate.
- Ignore unnamed cameos and background appearances.
- Only consider major romantic candidates included in the dataset.
- Do not use the ending or romantic outcome when assigning values.

---

## Input

Story Title:
{story_title}

Candidates:
{c_list_str}

---

## Output

Return ONLY valid JSON:
"""
        
        def clean_json_string(text):
            text = text.strip()
            if text.startswith("```"):
                newline_idx = text.find("\n")
                if newline_idx != -1:
                    text = text[newline_idx:].strip()
                if text.endswith("```"):
                    text = text[:-3].strip()
            return text

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
                        response_schema=StoryAppearanceResult,
                        temperature=0.1
                    )
                )
                
                cleaned_text = clean_json_string(response.text)
                parsed_output = StoryAppearanceResult.model_validate_json(cleaned_text)
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
            p_order = p_cand.appearance_order
            p_chap = p_cand.first_chapter_or_episode
            reason = p_cand.reason
            
            # Match current values
            curr_order = c_map.get(c_name.lower())
            curr_chap = c_chap_map.get(c_name.lower())
            
            if curr_order is None:
                # Try finding soft match
                soft_match = None
                for orig_name in c_map.keys():
                    if orig_name in c_name.lower() or c_name.lower() in orig_name:
                        soft_match = orig_name
                        break
                if soft_match:
                    curr_order = c_map[soft_match]
                    curr_chap = c_chap_map[soft_match]
                    c_name = candidates_group[candidates_group["candidate_name"].str.lower() == soft_match].iloc[0]["candidate_name"]
                else:
                    curr_order = "None"
                    curr_chap = "None"
                    
            # Determine if changed
            changed = "No"
            if pd.isna(curr_order) or curr_order == "None" or str(curr_order) != str(p_order) or str(curr_chap) != str(p_chap):
                changed = "Yes"
                
            approved = "Yes" if changed == "Yes" else "No"
            
            review_rows.append({
                "story_id": story_id,
                "story_title": story_title,
                "candidate_name": c_name,
                "current_appearance_order": curr_order,
                "proposed_appearance_order": p_order,
                "proposed_first_chapter_or_episode": p_chap,
                "changed": changed,
                "approved": approved,
                "reason": reason
            })
            
        print(f"   Processed.")
        
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
