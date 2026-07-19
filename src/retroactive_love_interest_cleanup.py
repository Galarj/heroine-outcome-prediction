import os
import re
import sys
import time
import pandas as pd
import pydantic
import google.generativeai as genai

# Reconfigure stdout to UTF-8
sys.stdout.reconfigure(encoding='utf-8')

# Paths
CANDIDATES_FILE = "data/candidates_cleaned.xlsx"
STORIES_FILE = "data/stories_cleaned.xlsx"
CONSOLIDATED_REVIEW_FILE = "data/consolidated_order_review.xlsx"

class RetroactiveCandidate(pydantic.BaseModel):
    candidate_name: str
    is_love_interest: bool = pydantic.Field(description="Set to true if they are a legitimate romantic interest of the protagonist. Set to false for family members (unless incestuous/romantic interest), pets, background characters, or friends who have absolutely no romantic storylines or feelings with/for the protagonist.")

class RetroactiveStoryResult(pydantic.BaseModel):
    story_title: str
    candidates: list[RetroactiveCandidate]

def load_all_api_keys():
    script_dir = os.path.dirname(os.path.abspath(__file__))
    keys = []
    current_dir = script_dir
    for _ in range(4):
        env_path = os.path.join(current_dir, ".env")
        if os.path.exists(env_path):
            try:
                with open(env_path, "r", encoding="utf-8") as f:
                    content = f.read()
                    # Only load standard keys starting with AIzaSy
                    found = re.findall(r"(AIzaSy[A-Za-z0-9_\-]+)", content)
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
        # Clear legacy client cache to prevent gRPC hangs
        try:
            genai.client._client_manager.clients.clear()
        except Exception:
            pass
        return genai.GenerativeModel(self.model_name)
        
    def rotate(self):
        self.current_idx = (self.current_idx + 1) % len(self.keys)
        print(f"   [API Key Pool] Switched to key index {self.current_idx + 1}/{len(self.keys)}")

def clean_json_string(text):
    text = text.strip()
    if text.startswith("```json"):
        text = text[7:]
    if text.endswith("```"):
        text = text[:-3]
    return text.strip()

def main():
    print("=== Retroactive Non-Love-Interest Curation Sweep ===")
    
    if not os.path.exists(CANDIDATES_FILE) or not os.path.exists(STORIES_FILE):
        print("Error: Candidates and stories files not found.")
        sys.exit(1)
        
    candidates_df = pd.read_excel(CANDIDATES_FILE, keep_default_na=False)
    stories_df = pd.read_excel(STORIES_FILE, keep_default_na=False)
    
    review_rows = []
    if os.path.exists(CONSOLIDATED_REVIEW_FILE):
        review_rows = pd.read_excel(CONSOLIDATED_REVIEW_FILE, keep_default_na=False).to_dict(orient="records")
        
    keys = load_all_api_keys()
    print(f"Loaded {len(keys)} standard API keys.")
    model_pool = RotatingModelPool(keys)
    
    unique_stories = candidates_df["story_id"].unique()
    total_stories = len(unique_stories)
    print(f"Sweeping through all {total_stories} stories in the database...")
    
    dropped_any = False
    
    for idx, story_id in enumerate(unique_stories):
        story_rows = stories_df[stories_df["story_id"] == story_id]
        if story_rows.empty:
            continue
        story_title = story_rows.iloc[0]["title"]
        
        candidates_group = candidates_df[candidates_df["story_id"] == story_id]
        if candidates_group.empty:
            continue
            
        print(f"\n[{idx+1}/{total_stories}] Analyzing candidates of '{story_title}' (Story ID: {story_id})...")
        
        c_list_str = ""
        c_map = {}
        for _, c_row in candidates_group.iterrows():
            c_name = c_row["candidate_name"]
            c_list_str += f"- {c_name}\n"
            c_map[c_name.lower()] = c_row
            
        prompt = f"""You are an expert romance media archivist. Your task is to identify whether each of the candidates listed below is a legitimate romantic interest of the protagonist in '{story_title}'.
        
Guidelines:
- Set to `true` if they are a romantic candidate or have a legitimate romantic arc/feelings for the protagonist in the original source material.
- Set to `false` for family members (unless incestuous/romantic interest), pets, background classmates, or friends who have absolutely no romantic storylines or feelings with/for the protagonist.

Candidates to evaluate:
{c_list_str}

Please return the results matching the requested JSON schema.
"""
        
        success = False
        attempts = 0
        max_attempts = 3
        backoff = 5.0
        parsed_output = None
        
        while attempts < max_attempts:
            try:
                model = model_pool.get_model()
                response = model.generate_content(
                    prompt,
                    generation_config=genai.GenerationConfig(
                        response_mime_type="application/json",
                        response_schema=RetroactiveStoryResult,
                        temperature=0.1
                    ),
                    request_options={"timeout": 45.0}
                )
                cleaned_text = clean_json_string(response.text)
                parsed_output = RetroactiveStoryResult.model_validate_json(cleaned_text)
                success = True
                break
            except Exception as e:
                attempts += 1
                print(f"   [Error] Attempt {attempts}/{max_attempts} failed: {e}. Rotating key...")
                model_pool.rotate()
                time.sleep(backoff)
                backoff *= 2.0
                
        if not success or parsed_output is None:
            print(f"   [API Failure] Skipped Story ID {story_id} due to persistent failures.")
            continue
            
        returned_names = set()
        for p_cand in parsed_output.candidates:
            c_name = p_cand.candidate_name
            is_li = p_cand.is_love_interest
            
            # Match
            match_row = c_map.get(c_name.lower())
            if match_row is None:
                for orig_name in c_map.keys():
                    if c_name.lower() in orig_name or orig_name in c_name.lower():
                        match_row = c_map[orig_name]
                        break
                        
            if match_row is None:
                continue
                
            c_id = match_row["candidate_id"]
            returned_names.add(c_id)
            
            if not is_li:
                print(f"   [Retroactive Drop] Dropping candidate '{match_row['candidate_name']}' (ID: {c_id}) - Not a love interest.")
                candidates_df = candidates_df[candidates_df["candidate_id"] != c_id]
                review_rows = [r for r in review_rows if r["candidate_id"] != c_id]
                dropped_any = True
                
        # Drop any candidates omitted by Gemini as they are also likely background/non-love-interests
        for _, c_row in candidates_group.iterrows():
            c_id = c_row["candidate_id"]
            c_name = c_row["candidate_name"]
            if c_id not in returned_names:
                print(f"   [Retroactive Drop (Omitted)] Dropping candidate '{c_name}' (ID: {c_id}) - Omitted from evaluation.")
                candidates_df = candidates_df[candidates_df["candidate_id"] != c_id]
                review_rows = [r for r in review_rows if r["candidate_id"] != c_id]
                dropped_any = True
                
        # Re-sequence remaining candidates for this story to be consecutive
        remaining_group = candidates_df[candidates_df["story_id"] == story_id]
        if not remaining_group.empty:
            # 1. Introduction Order re-sequencing
            sorted_by_intro = remaining_group.sort_values(by="introduction_order")
            new_intro = 1
            for _, r_cand in sorted_by_intro.iterrows():
                c_id = r_cand["candidate_id"]
                candidates_df.loc[candidates_df["candidate_id"] == c_id, "introduction_order"] = new_intro
                new_intro += 1
                
            # 2. Appearance Order re-sequencing (preserving ties)
            # Skip if they are not validated yet (i.e. still null or empty)
            has_app_order = remaining_group["appearance_order"].apply(lambda x: str(x).strip() != "" and not pd.isna(x)).any()
            if has_app_order:
                # Convert appearance_order to numeric for proper sorting, treating empty as 99
                def clean_app(val):
                    try:
                        return int(val)
                    except Exception:
                        return 999
                
                remaining_group_app = remaining_group.copy()
                remaining_group_app["temp_app_sort"] = remaining_group_app["appearance_order"].apply(clean_app)
                sorted_by_app = remaining_group_app.sort_values(by="temp_app_sort")
                
                new_app = 1
                last_orig_app = None
                for _, r_cand in sorted_by_app.iterrows():
                    c_id = r_cand["candidate_id"]
                    orig_app = r_cand["temp_app_sort"]
                    if orig_app == 999:
                        # Keep it empty
                        continue
                    if last_orig_app is not None and orig_app != last_orig_app:
                        new_app += 1
                    candidates_df.loc[candidates_df["candidate_id"] == c_id, "appearance_order"] = new_app
                    last_orig_app = orig_app
                    
        # Save checkpoints immediately after every story
        try:
            candidates_df.to_excel(CANDIDATES_FILE, index=False)
            if review_rows:
                pd.DataFrame(review_rows).to_excel(CONSOLIDATED_REVIEW_FILE, index=False)
        except PermissionError:
            print("   [Warning] Excel file locked. Please close Excel.")
            
        time.sleep(2.0) # Pacing sleep
        
    print("\nSweep completed retroactively!")
    if dropped_any:
        print("Dropped non-love-interest candidates and re-sequenced remaining candidates successfully.")
    else:
        print("No non-love-interest candidates were found to drop.")
        
if __name__ == "__main__":
    main()
