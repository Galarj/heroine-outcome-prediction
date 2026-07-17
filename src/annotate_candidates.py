import os
import sys
import time
import pandas as pd
import pydantic
import google.generativeai as genai
from dotenv import load_dotenv

# Reconfigure stdout to use UTF-8 globally to prevent Windows console encoding crashes
sys.stdout.reconfigure(encoding='utf-8')

# Define file paths
STORIES_FILE = "data/Stories.xlsx"
CANDIDATES_RAW_FILE = "data/candidates_raw.xlsx"
CANDIDATES_RAW_BACKUP_FILE = "data/candidates_raw_backup.xlsx"
CANDIDATES_ANNOTATED_FILE = "data/candidates_annotated.xlsx"
CANDIDATES_ANNOTATED_BACKUP_FILE = "data/candidates_annotated_backup.xlsx"

# Allowed categorical values (for post-validation)
ALLOWED_GENDERS = {"Female", "Male", "Other", "Unknown"}
ALLOWED_CONNECTIONS = {"None", "Acquaintance", "Childhood Friend", "Childhood Promise"}
ALLOWED_COMMITMENTS = {"None", "Promise", "Engagement", "Marriage"}
ALLOWED_ARCHETYPES = {"Tsundere", "Kuudere", "Dandere", "Genki", "Yandere", "Deredere", "Onee-san", "Mixed", "Unknown"}
ALLOWED_HAIR_COLORS = {"Black", "Brown", "Blonde", "Red", "Blue", "Pink", "Silver", "White", "Green", "Purple", "Other", "Unknown"}
ALLOWED_DEVELOPMENT_STAGES = {"Early", "Middle", "Late", "Unknown"}

# 1. Define Pydantic schema for Gemini structured output
class CandidateDetail(pydantic.BaseModel):
    candidate_id: str
    candidate_name: str
    romantic_candidate: bool
    candidate_gender: str
    childhood_connection: str
    commitment_status: str
    primary_archetype: str
    hair_color: str
    romance_development_stage: str
    confidence_score: float
    reasoning: str

class StoryAnnotation(pydantic.BaseModel):
    candidates: list[CandidateDetail]

def load_gemini_api_key():
    """
    Robust function to load GEMINI_API_KEY from .env or environment,
    resolving the file relative to the project root.
    """
    load_dotenv()
    
    # Try locating .env in the parent directory of this script (project root)
    script_dir = os.path.dirname(os.path.abspath(__file__))
    project_root = os.path.dirname(script_dir)
    env_path = os.path.join(project_root, ".env")
    if os.path.exists(env_path):
        load_dotenv(env_path)
        
    # Try standard key
    key = os.getenv("GEMINI_API_KEY")
    if key:
        return key
        
    # Try key with space
    key = os.getenv("GEMINI API KEY")
    if key:
        return key
        
    # Manual parse fallback
    for path in [".env", env_path]:
        if os.path.exists(path):
            with open(path, "r", encoding="utf-8") as f:
                for line in f:
                    if "=" in line:
                        k, v = line.split("=", 1)
                        if k.strip() in ["GEMINI_API_KEY", "GEMINI API KEY"]:
                            return v.strip()
                            
    return None

def save_dataframe_to_excel(df, filepath, backup_filepath=CANDIDATES_ANNOTATED_BACKUP_FILE):
    """
    Saves a DataFrame to Excel, handling PermissionError gracefully.
    If the file is locked, writes to a consolidated backup file.
    """
    try:
        df.to_excel(filepath, index=False)
        if os.path.exists(backup_filepath):
            try:
                os.remove(backup_filepath)
            except Exception:
                pass
        return True
    except PermissionError:
        print(f"\n   [Permission Error] Cannot write to {filepath} (file is likely open in Excel).")
        print(f"   Saving progress to backup file: {backup_filepath}")
        try:
            df.to_excel(backup_filepath, index=False)
            return True
        except Exception as e:
            print(f"   Failed to save backup file: {e}")
            return False

def clean_categorical_value(value, allowed_set, default_val):
    """
    Validates a categorical value against an allowed set, returning the default if invalid.
    """
    if not isinstance(value, str):
        return default_val
    stripped = value.strip().title()
    if stripped in allowed_set:
        return stripped
    for item in allowed_set:
        if stripped.lower() == item.lower():
            return item
    return default_val

def validate_and_clean_annotations(parsed_output, expected_ids, story_id):
    """
    Validates that the Gemini output conforms exactly to raw candidate inputs.
    Cleans up any invalid categorical labels or out-of-range confidence scores.
    """
    cleaned_candidates = []
    returned_ids = set()
    
    for candidate in parsed_output.candidates:
        c_id = candidate.candidate_id
        if c_id not in expected_ids:
            continue
        if c_id in returned_ids:
            continue
        returned_ids.add(c_id)
        
        gender = clean_categorical_value(candidate.candidate_gender, ALLOWED_GENDERS, "Unknown")
        connection = clean_categorical_value(candidate.childhood_connection, ALLOWED_CONNECTIONS, "None")
        commitment = clean_categorical_value(candidate.commitment_status, ALLOWED_COMMITMENTS, "None")
        archetype = clean_categorical_value(candidate.primary_archetype, ALLOWED_ARCHETYPES, "Unknown")
        hair = clean_categorical_value(candidate.hair_color, ALLOWED_HAIR_COLORS, "Unknown")
        stage = clean_categorical_value(candidate.romance_development_stage, ALLOWED_DEVELOPMENT_STAGES, "Unknown")
        
        score = max(0.0, min(1.0, float(candidate.confidence_score)))
        reasoning = candidate.reasoning.strip() if candidate.reasoning else "No reasoning provided."
        
        cleaned_candidates.append({
            "candidate_id": c_id,
            "story_id": story_id,
            "candidate_name": candidate.candidate_name,
            "candidate_gender": gender,
            "romantic_candidate": candidate.romantic_candidate,
            "childhood_connection": connection,
            "commitment_status": commitment,
            "primary_archetype": archetype,
            "hair_color": hair,
            "romance_development_stage": stage,
            "confidence_score": round(score, 2),
            "reasoning": reasoning
        })
        
    missing_ids = expected_ids - returned_ids
    if missing_ids:
        print(f"      [Validation Warning] Gemini omitted {len(missing_ids)} character(s). Backfilling with defaults.")
        
    return cleaned_candidates

def main():
    print("=== Gemini Annotation Pipeline ===")
    
    # 2. Load API key and configure Gemini
    api_key = load_gemini_api_key()
    if not api_key:
        print("Error: GEMINI_API_KEY not found in environment or .env file!")
        print("Please check your .env file and ensure it contains: GEMINI_API_KEY=your_key")
        sys.exit(1)
        
    genai.configure(api_key=api_key)
    model = genai.GenerativeModel("gemini-flash-lite-latest")
    
    # 3. Check inputs
    if not os.path.exists(STORIES_FILE):
        print(f"Error: Parent stories file {STORIES_FILE} not found.")
        sys.exit(1)
        
    # Read from both RAW and RAW BACKUP to merge the compiled raw character list
    loaded_raw_dfs = []
    for filepath in [CANDIDATES_RAW_FILE, CANDIDATES_RAW_BACKUP_FILE]:
        if os.path.exists(filepath):
            try:
                df = pd.read_excel(filepath)
                if not df.empty:
                    loaded_raw_dfs.append(df)
            except Exception as e:
                print(f"Warning: Could not read {filepath}: {e}")
                
    if not loaded_raw_dfs:
        print("Error: No raw candidates Excel files found. Please run scraper.py first.")
        sys.exit(1)
        
    raw_candidates_df = pd.concat(loaded_raw_dfs, ignore_index=True).drop_duplicates(subset=["story_id", "candidate_name"])
    stories_df = pd.read_excel(STORIES_FILE)
    stories_df = stories_df.dropna(axis=1, how="all")
    
    print(f"Loaded {len(stories_df)} stories and {len(raw_candidates_df)} raw candidates.")
    
    # 4. Setup or resume annotated dataset
    processed_story_ids = set()
    annotated_candidates_list = []
    
    # Load existing annotations from main and backup annotation files to resume
    loaded_annotated_dfs = []
    for filepath in [CANDIDATES_ANNOTATED_FILE, CANDIDATES_ANNOTATED_BACKUP_FILE]:
        if os.path.exists(filepath):
            print(f"Found existing annotated candidates file: {filepath}")
            try:
                df = pd.read_excel(filepath)
                if not df.empty:
                    loaded_annotated_dfs.append(df)
            except Exception as e:
                print(f"Warning: Could not read {filepath}: {e}")
                
    if loaded_annotated_dfs:
        try:
            combined_annotated_df = pd.concat(loaded_annotated_dfs, ignore_index=True).drop_duplicates(subset=["story_id", "candidate_name"])
            annotated_candidates_list = combined_annotated_df.to_dict("records")
            processed_story_ids = set(combined_annotated_df["story_id"].dropna().unique())
            print(f"Resuming progress: Already annotated {len(processed_story_ids)} stories.")
        except Exception as e:
            print(f"Warning: Could not merge existing annotations: {e}. Starting fresh.")
            
    # Group candidates by story_id for processing
    grouped_candidates = raw_candidates_df.groupby("story_id")
    
    # 5. Process each story
    for story_id, candidates_group in grouped_candidates:
        if story_id in processed_story_ids:
            continue
            
        story_rows = stories_df[stories_df["story_id"] == story_id]
        if story_rows.empty:
            continue
            
        story_row = story_rows.iloc[0]
        title = story_row["title"]
        print(f"\nAnnotating Story ID {story_id}: '{title}'...")
        
        expected_ids = set(candidates_group["candidate_id"].tolist())
        
        candidates_str_list = []
        for _, c_row in candidates_group.iterrows():
            candidates_str_list.append(
                f"- Candidate ID: {c_row['candidate_id']} | Name: {c_row['candidate_name']} | Role: {c_row['role']}"
            )
        candidates_input_str = "\n".join(candidates_str_list)
        
        prompt = f"""
You are an expert anime, manga, and light novel research assistant. Your task is to analyze character metadata and classify romance heroine candidates for the project: "Heroine Outcome Prediction".

We are analyzing the romance story:
Title: {title}
Medium: {story_row.get('medium', 'Unknown')}
Release Year: {story_row.get('release_year', 'Unknown')}
Romance Type: {story_row.get('romance_type', 'Unknown')}
Setting: {story_row.get('setting', 'Unknown')}
Demographic: {story_row.get('demographic', 'Unknown')}
Target Audience: {story_row.get('target_audience', 'Unknown')}
Source Material: {story_row.get('source_material', 'Unknown')}

Here is the list of raw characters retrieved for this story. You MUST evaluate and return data for EVERY SINGLE character ID listed here:
{candidates_input_str}

Please evaluate each character in this list and classify them as a romance candidate.

CRITICAL DATASET DEFINITIONS & RULES (FOLLOW EXACTLY):

1. Attribute Scope:
   - Record attributes that describe the character DURING the main story, NOT after the ending. Do not infer commitments from the ending.

2. romantic_candidate (boolean):
   - TRUE only if the character is a legitimate romantic candidate (love interest) recognized by the narrative during the main story.
   - FALSE for protagonists, family members, platonic friends, joke candidates, background crushes, or characters with no realistic romantic route.

3. childhood_connection:
   - Allowed values: "None", "Acquaintance", "Childhood Friend", "Childhood Promise".
   - This describes the relationship BEFORE the main story begins. A single childhood meeting is NOT Childhood Friend (use "None").
   - Use Childhood Promise ONLY when an explicit promise about marriage, romance, or a future together exists before the story begins.
   - Priority order: Childhood Promise > Childhood Friend > Acquaintance > None.

4. commitment_status:
   - Allowed values: "None", "Promise", "Engagement", "Marriage".
   - This describes a formal romantic commitment that already exists DURING the main story.
   - Do NOT use information from the ending. A marriage occurring only in the epilogue/ending is NOT Marriage (use "None").
   - Arranged/fake engagements count as Engagement if treated as such in the narrative.
   - Examples to follow:
     * Chitoge Kirisaki -> Engagement (due to the fake relationship treated as engagement/dating)
     * Yotsuba Nakano -> None (do not record the ending marriage)
     * Marika Tachibana -> None (do not record her arranged marriage subplot as active romantic commitment during narrative)
     * Louise Françoise -> Marriage (if married during the story)

5. romance_development_stage:
   - Allowed values: "Early", "Middle", "Late", "Unknown".
   - Measures when the character becomes a legitimate romantic candidate, NOT first appearance.
   - Ignore ending outcomes. Winners are not automatically Late. Childhood friends are not automatically Early.

6. primary_archetype:
   - Allowed values: "Tsundere", "Kuudere", "Dandere", "Genki", "Yandere", "Deredere", "Onee-san", "Mixed", "Unknown".
   - Choose the dominant archetype. If multiple are equally strong, use "Mixed". Do not invent archetypes.

7. hair_color:
   - Allowed values: "Black", "Brown", "Blonde", "Red", "Blue", "Pink", "Silver", "White", "Green", "Purple", "Other", "Unknown".

8. General:
   - If uncertain or lack evidence, use "Unknown" or "None".
   - Keep reasoning to 1 or 2 concise sentences.

OUTPUT VALIDATION CHECKLIST:
- You must output a JSON object containing a "candidates" list.
- Every candidate_id from the input list must appear exactly once.
- No extra characters may be added, and no input characters may be omitted.
- Categorical values must match the allowed sets exactly.
- confidence_score is a float between 0.0 and 1.0.
"""

        success = False
        api_retries = 5
        backoff = 4.0
        
        for attempt in range(api_retries):
            try:
                response = model.generate_content(
                    prompt,
                    generation_config=genai.GenerationConfig(
                        response_mime_type="application/json",
                        response_schema=StoryAnnotation,
                        temperature=0.1
                    )
                )
                
                parsed_output = StoryAnnotation.model_validate_json(response.text)
                cleaned_data = validate_and_clean_annotations(parsed_output, expected_ids, story_id)
                
                annotated_count = 0
                for c_annotated in cleaned_data:
                    if not c_annotated["romantic_candidate"]:
                        continue
                        
                    final_record = {
                        "candidate_id": c_annotated["candidate_id"],
                        "story_id": story_id,
                        "candidate_name": c_annotated["candidate_name"],
                        "candidate_gender": c_annotated["candidate_gender"],
                        "won": "Needs Human Verification",
                        "introduction_order": None,
                        "childhood_connection": c_annotated["childhood_connection"],
                        "commitment_status": c_annotated["commitment_status"],
                        "primary_archetype": c_annotated["primary_archetype"],
                        "hair_color": c_annotated["hair_color"],
                        "romance_development_stage": c_annotated["romance_development_stage"],
                        "confidence_score": c_annotated["confidence_score"],
                        "reasoning": c_annotated["reasoning"]
                    }
                    annotated_candidates_list.append(final_record)
                    annotated_count += 1
                    
                print(f"   -> Annotated {annotated_count} legitimate candidates (filtered out non-candidates).")
                success = True
                break
                
            except Exception as e:
                err_str = str(e)
                if "429" in err_str or "quota" in err_str.lower() or "limit" in err_str.lower():
                    sleep_time = backoff + 5.0
                    print(f"   -> [API Rate Limit (429)] Waiting {sleep_time:.1f}s before retry (Attempt {attempt + 1}/{api_retries})...")
                    time.sleep(sleep_time)
                    backoff *= 2
                else:
                    print(f"   -> [API Error] Attempt {attempt + 1}/{api_retries} failed: {e}")
                    time.sleep(backoff)
                    backoff *= 2
                
        if not success:
            print(f"   -> [Warning] Skipped annotation for Story ID {story_id} due to API failures.")
            continue
            
        processed_story_ids.add(story_id)
        
        # Save progress after each story (using robust helper)
        df_to_save = pd.DataFrame(annotated_candidates_list)
        cols_order = [
            "candidate_id", "story_id", "candidate_name", "candidate_gender", 
            "won", "introduction_order", "childhood_connection", "commitment_status", 
            "primary_archetype", "hair_color", "romance_development_stage", 
            "confidence_score", "reasoning"
        ]
        
        if not df_to_save.empty:
            df_to_save = df_to_save.reindex(columns=cols_order)
            save_dataframe_to_excel(df_to_save, CANDIDATES_ANNOTATED_FILE)
            
        # Rate limit sleep: wait 4 seconds between stories to respect 15 RPM Free Tier limit
        time.sleep(4.0)
        
    print("\n=== Annotation Pipeline Completed! ===")
    print(f"Total annotated candidates saved: {len(annotated_candidates_list)}")
    print(f"Saved to: {CANDIDATES_ANNOTATED_FILE}")

if __name__ == "__main__":
    main()
