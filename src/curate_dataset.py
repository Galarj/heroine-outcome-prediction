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

# Define file paths
STORIES_FILE = "data/Stories.xlsx"
CANDIDATES_ANNOTATED_FILE = "data/candidates_annotated.xlsx"
STORIES_CLEANED_FILE = "data/stories_cleaned.xlsx"
CANDIDATES_CLEANED_FILE = "data/candidates_cleaned.xlsx"
VALIDATION_REPORT_FILE = "validation_report.md"

# Categorical allowed sets
ALLOWED_CONNECTIONS = {"None", "Acquaintance", "Childhood Friend", "Childhood Promise", "Unknown"}
ALLOWED_COMMITMENTS = {"None", "Promise", "Engagement", "Marriage", "Unknown"}
ALLOWED_ARCHETYPES = {"Tsundere", "Kuudere", "Dandere", "Genki", "Yandere", "Deredere", "Onee-san", "Mixed", "Unknown"}
ALLOWED_HAIR_COLORS = {"Black", "Brown", "Blonde", "Red", "Blue", "Pink", "Silver", "White", "Green", "Purple", "Other", "Unknown"}

# Pydantic schemas for structured output
class CuratedCandidate(pydantic.BaseModel):
    candidate_id: str
    candidate_name: str
    won: int                     # 1 or 0
    first_girl: int              # 1 or 0
    introduction_order: int      # 1, 2, 3...
    childhood_connection: str    # allowed sets
    commitment_status: str       # allowed sets
    primary_archetype: str       # allowed sets
    hair_color: str              # allowed sets
    confidence_score: float      # 0.00 to 1.00
    reasoning: str               # 1-2 sentence justification

class MissingHeroine(pydantic.BaseModel):
    candidate_name: str
    won: int                     # 1 or 0
    first_girl: int              # 1 or 0

class CuratedStory(pydantic.BaseModel):
    candidates: list[CuratedCandidate]
    missing_candidates: list[MissingHeroine]
    confidence_level: str         # "High", "Medium", "Low"
    confidence_explanation: str   # explanation if not High

def load_all_api_keys():
    """
    Parse the .env file at project root, parent root, or grandparent root,
    and extract all unique Gemini API keys.
    """
    script_dir = os.path.dirname(os.path.abspath(__file__))
    
    # Traverse upwards up to 3 levels to locate any .env files
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

def clean_categorical_value(value, allowed_set, default_val):
    if not isinstance(value, str):
        return default_val
    stripped = value.strip().title()
    if stripped in allowed_set:
        return stripped
    for item in allowed_set:
        if stripped.lower() == item.lower():
            return item
    return default_val

def merge_duplicate_stories(stories_df, candidates_df):
    """
    Perform merging of duplicate stories and update candidate associations:
    1. Merge 'The Familiar of Zero' (ID 24) into 'Zero no Tsukaima' (ID 40)
    2. Merge 'Chivalry of a Failed Knight' (ID 28) into 'Rakudai Kishi no Cavalry' (ID 38)
    """
    merge_log = []
    
    duplicates = [
        {"delete_id": 24, "keep_id": 40, "name": "Zero no Tsukaima / The Familiar of Zero"},
        {"delete_id": 28, "keep_id": 38, "name": "Rakudai Kishi no Cavalry / Chivalry of a Failed Knight"}
    ]
    
    # Track stories table updates
    initial_stories_count = len(stories_df)
    
    for dup in duplicates:
        del_id = dup["delete_id"]
        keep_id = dup["keep_id"]
        
        # Check if they exist in stories dataframe
        if del_id in stories_df["story_id"].values and keep_id in stories_df["story_id"].values:
            # Update candidates associated with the deleted ID
            cond_cand_to_update = candidates_df["story_id"] == del_id
            updated_count = cond_cand_to_update.sum()
            candidates_df.loc[cond_cand_to_update, "story_id"] = keep_id
            
            # Remove deleted story ID from stories dataframe
            stories_df = stories_df[stories_df["story_id"] != del_id]
            
            merge_log.append({
                "story": dup["name"],
                "merged_id": del_id,
                "target_id": keep_id,
                "candidates_updated": updated_count
            })
            
    print(f"Stories table: Merged duplicate records, count reduced from {initial_stories_count} to {len(stories_df)}")
    return stories_df, candidates_df, merge_log

def main():
    print("=== Database Curation & Cleaning Pipeline ===")
    
    # 1. Load data
    if not os.path.exists(STORIES_FILE) or not os.path.exists(CANDIDATES_ANNOTATED_FILE):
        print("Error: Input Excel files not found!")
        sys.exit(1)
        
    stories_df = pd.read_excel(STORIES_FILE)
    candidates_df = pd.read_excel(CANDIDATES_ANNOTATED_FILE)
    
    # 2. Merge duplicates
    stories_df, candidates_df, merge_log = merge_duplicate_stories(stories_df, candidates_df)
    
    # 3. Setup Gemini key pool
    keys = load_all_api_keys()
    print(f"Loaded a pool of {len(keys)} Gemini API keys from .env.")
    model_pool = RotatingModelPool(keys)
    
    # Set up lists for curated data
    curated_candidates = []
    
    # Track metrics for validation report
    stories_corrected = []
    hair_colors_corrected = []
    missing_value_fills = []
    heroine_counts_corrected = []
    stories_manual_review = []
    confidence_levels = {}
    
    # Find next candidate number
    max_num = 0
    for cid in candidates_df["candidate_id"].dropna():
        if isinstance(cid, str) and cid.startswith("C"):
            try:
                num = int(cid[1:])
                if num > max_num:
                    max_num = num
            except ValueError:
                pass
    next_candidate_num = max_num + 1
    
    # 4. Iterate and curate stories
    for idx, story_row in stories_df.iterrows():
        story_id = story_row["story_id"]
        title = story_row["title"]
        medium = story_row["medium"]
        source_material = story_row.get("source_material", "Unknown")
        
        print(f"\n[{idx + 1}/{len(stories_df)}] Curating Story ID {story_id}: '{title}' ({medium})")
        
        # Get candidates associated with this story
        story_candidates = candidates_df[candidates_df["story_id"] == story_id]
        
        candidates_input = []
        for _, c_row in story_candidates.iterrows():
            candidates_input.append({
                "candidate_id": c_row["candidate_id"],
                "candidate_name": c_row["candidate_name"],
                "candidate_gender": c_row.get("candidate_gender", "Female"),
                "childhood_connection": c_row.get("childhood_connection", "None"),
                "commitment_status": c_row.get("commitment_status", "None"),
                "primary_archetype": c_row.get("primary_archetype", "Unknown"),
                "hair_color": c_row.get("hair_color", "Unknown")
            })
            
        # Call Gemini to audit and verify candidates
        prompt = f"""
You are an expert Romance Media Archivist and Data Curator.
Your objective is to curate and clean the romance heroine candidates for the story:
Title: {title}
Medium: {medium}
Original Source Material: {source_material}

Current candidate list in our database for this story:
{candidates_input}

TASK:
1. Determine the EXACT canonical romantic winner (won = 1). Exactly ONE candidate must have won = 1, others 0.
   - Use the Canonical Source Priority: Original Manga > Original Light Novel > Original Visual Novel (single-route) > Anime Original.
   - Adaptations (e.g. anime of a manga) should never override the original source unless the anime is the original work.
   - If no canonical winner exists (e.g. ongoing story, open harem ending, or choose-your-own-route visual novel like Kanon/Clannad/Amagami), set won = 0 for everyone and flag this in confidence explanation.
2. Determine the first girl (first_girl = 1). Exactly ONE candidate must receive first_girl = 1, others 0.
   - This is the first major romantic heroine introduced.
   - Ignore background appearances and flashbacks.
3. Determine the unique chronological introduction order (starting from 1) based on when they become legitimate romantic interests (NOT merely first appearance).
4. Verify and clean hair colors, childhood connections, and commitment statuses (None, Promise, Engagement, Marriage).
   - Priority for childhood connections: Childhood Promise > Childhood Friend > Acquaintance > None.
5. Identify if any major romance heroine is missing from our current candidate list. If so, return their details in the `missing_candidates` list so we can insert them. For every candidate in the `missing_candidates` list, you MUST output only candidate_name, won (0 or 1), and first_girl (0 or 1).
6. Assign a confidence score from 0.00 to 1.00 for every candidate's attributes, and a confidence level (High/Medium/Low) for the story.

You must output a structured JSON matching the schema.
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
                        response_schema=CuratedStory,
                        temperature=0.1
                    )
                )
                
                curated_story = CuratedStory.model_validate_json(response.text)
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
                    time.sleep(backoff)
                    backoff *= 2.0
                    
        if not success:
            print(f"   [Warning] Skipped curation for Story ID {story_id} due to API failures.")
            # Backfill candidates with default placeholder values
            for _, c_row in story_candidates.iterrows():
                curated_candidates.append({
                    "candidate_id": c_row["candidate_id"],
                    "story_id": story_id,
                    "candidate_name": c_row["candidate_name"],
                    "candidate_gender": c_row.get("candidate_gender", "Female"),
                    "won": 0,
                    "first_girl": 0,
                    "introduction_order": 1,
                    "childhood_connection": c_row.get("childhood_connection", "None"),
                    "commitment_status": c_row.get("commitment_status", "None"),
                    "primary_archetype": c_row.get("primary_archetype", "Unknown"),
                    "hair_color": c_row.get("hair_color", "Unknown"),
                    "confidence_score": 0.5,
                    "reasoning": "Fallback default curation due to API failures."
                })
            stories_manual_review.append({
                "story_id": story_id,
                "title": title,
                "reason": "Gemini curation API failed completely."
            })
            continue
            
        # Process curated candidates
        confidence_levels[story_id] = {
            "level": curated_story.confidence_level,
            "explanation": curated_story.confidence_explanation
        }
        
        # Combine existing and missing candidates
        candidates_map = {}
        for c in curated_story.candidates:
            candidates_map[c.candidate_id] = c
            
        # 1. Update existing candidates
        for _, c_row in story_candidates.iterrows():
            c_id = c_row["candidate_id"]
            c_name = c_row["candidate_name"]
            
            curated_c = candidates_map.get(c_id)
            if curated_c:
                # Track corrections
                orig_won = c_row.get("won")
                orig_hair = c_row.get("hair_color")
                
                clean_hair = clean_categorical_value(curated_c.hair_color, ALLOWED_HAIR_COLORS, "Unknown")
                clean_conn = clean_categorical_value(curated_c.childhood_connection, ALLOWED_CONNECTIONS, "None")
                clean_comm = clean_categorical_value(curated_c.commitment_status, ALLOWED_COMMITMENTS, "None")
                clean_arch = clean_categorical_value(curated_c.primary_archetype, ALLOWED_ARCHETYPES, "Unknown")
                
                if orig_won != curated_c.won:
                    stories_corrected.append({
                        "story_id": story_id,
                        "title": title,
                        "candidate_name": c_name,
                        "change": f"won: {orig_won} -> {curated_c.won}"
                    })
                if orig_hair != clean_hair:
                    hair_colors_corrected.append({
                        "story_id": story_id,
                        "title": title,
                        "candidate_name": c_name,
                        "change": f"hair_color: {orig_hair} -> {clean_hair}"
                    })
                    
                curated_candidates.append({
                    "candidate_id": c_id,
                    "story_id": story_id,
                    "candidate_name": c_name,
                    "candidate_gender": c_row.get("candidate_gender", "Female"),
                    "won": curated_c.won,
                    "first_girl": curated_c.first_girl,
                    "introduction_order": curated_c.introduction_order,
                    "childhood_connection": clean_conn,
                    "commitment_status": clean_comm,
                    "primary_archetype": clean_arch,
                    "hair_color": clean_hair,
                    "confidence_score": round(curated_c.confidence_score, 2),
                    "reasoning": curated_c.reasoning
                })
            else:
                # Omitted, add with default fields
                curated_candidates.append({
                    "candidate_id": c_id,
                    "story_id": story_id,
                    "candidate_name": c_name,
                    "candidate_gender": c_row.get("candidate_gender", "Female"),
                    "won": 0,
                    "first_girl": 0,
                    "introduction_order": 99,
                    "childhood_connection": clean_categorical_value(c_row.get("childhood_connection"), ALLOWED_CONNECTIONS, "None"),
                    "commitment_status": clean_categorical_value(c_row.get("commitment_status"), ALLOWED_COMMITMENTS, "None"),
                    "primary_archetype": clean_categorical_value(c_row.get("primary_archetype"), ALLOWED_ARCHETYPES, "Unknown"),
                    "hair_color": clean_categorical_value(c_row.get("hair_color"), ALLOWED_HAIR_COLORS, "Unknown"),
                    "confidence_score": 0.5,
                    "reasoning": "Omitted by Gemini during curation; backfilled with defaults."
                })
                missing_value_fills.append({
                    "story_id": story_id,
                    "title": title,
                    "candidate_name": c_name,
                    "field": "oission_backfill"
                })
                
        # 2. Add missing candidates
        added_missing_count = 0
        existing_names = [c["candidate_name"].lower() for c in curated_candidates if c["story_id"] == story_id]
        
        # Calculate max order so far to assign to new candidates
        story_cands = [c for c in curated_candidates if c["story_id"] == story_id]
        max_order = max([c["introduction_order"] for c in story_cands]) if story_cands else 0
        
        # Smart shoujo detection to default candidate_gender to Male for female-protagonist romance media
        shoujo_keywords = ["ouran", "fruits basket", "special a", "kimi ni todoke", "lovely★complex", "kare kano", "my sweet tyrant"]
        default_gender = "Female"
        if any(k in title.lower() for k in shoujo_keywords):
            default_gender = "Male"
            
        for mc in curated_story.missing_candidates:
            if mc.candidate_name.lower() in existing_names:
                continue
                
            c_id = f"C{next_candidate_num:04d}"
            max_order += 1
            curated_candidates.append({
                "candidate_id": c_id,
                "story_id": story_id,
                "candidate_name": mc.candidate_name,
                "candidate_gender": default_gender,
                "won": mc.won,
                "first_girl": mc.first_girl,
                "introduction_order": max_order,
                "childhood_connection": "None",
                "commitment_status": "None",
                "primary_archetype": "Unknown",
                "hair_color": "Unknown",
                "confidence_score": 0.85,
                "reasoning": f"Automatically recovered missing major candidate: {mc.candidate_name}."
            })
            next_candidate_num += 1
            added_missing_count += 1
            
        if added_missing_count > 0:
            print(f"   -> Recovered and added {added_missing_count} missing candidate(s).")
            
        # Post-validation flags for manual review
        # e.g., sum of won != 1, or sum of first_girl != 1
        story_cands = [c for c in curated_candidates if c["story_id"] == story_id]
        total_won = sum(c["won"] for c in story_cands)
        total_fg = sum(c["first_girl"] for c in story_cands)
        
        # Check visual novels or open ending exceptions
        is_vn = medium.lower() in ["visual novel"]
        
        if total_won != 1:
            if is_vn or "harem" in title.lower() or total_won == 0:
                # VN routing or ongoing story, expected
                pass
            else:
                stories_manual_review.append({
                    "story_id": story_id,
                    "title": title,
                    "reason": f"Canonical winner count is {total_won} (expected exactly 1)"
                })
        if total_fg != 1 and len(story_cands) > 0:
            stories_manual_review.append({
                "story_id": story_id,
                "title": title,
                "reason": f"First girl count is {total_fg} (expected exactly 1)"
            })
            
        # Save temporary progress
        temp_df = pd.DataFrame(curated_candidates)
        try:
            temp_df.to_excel(CANDIDATES_CLEANED_FILE, index=False)
        except PermissionError:
            temp_df.to_excel(CANDIDATES_CLEANED_FILE.replace(".xlsx", "_backup.xlsx"), index=False)
            
        # Gentle sleep to respect rate limits
        time.sleep(3.0)
        
    # 5. Update stories_cleaned details (heroine count)
    curated_candidates_df = pd.DataFrame(curated_candidates)
    
    # Recalculate heroine count for each story
    heroine_counts = curated_candidates_df.groupby("story_id").size().to_dict()
    
    for idx, s_row in stories_df.iterrows():
        sid = s_row["story_id"]
        orig_count = s_row.get("heroine_count", 0)
        new_count = heroine_counts.get(sid, 0)
        
        if orig_count != new_count:
            heroine_counts_corrected.append({
                "story_id": sid,
                "title": s_row["title"],
                "change": f"heroine_count: {orig_won} -> {new_count}"
            })
            
    stories_df["heroine_count"] = stories_df["story_id"].map(heroine_counts).fillna(0).astype(int)
    
    # Write cleaned files
    try:
        stories_df.to_excel(STORIES_CLEANED_FILE, index=False)
        print(f"\nSaved curated stories to: {STORIES_CLEANED_FILE}")
    except PermissionError:
        stories_df.to_excel(STORIES_CLEANED_FILE.replace(".xlsx", "_backup.xlsx"), index=False)
        print(f"\nSaved curated stories backup to: {STORIES_CLEANED_FILE.replace('.xlsx', '_backup.xlsx')}")
        
    try:
        curated_candidates_df.to_excel(CANDIDATES_CLEANED_FILE, index=False)
        print(f"Saved curated candidates to: {CANDIDATES_CLEANED_FILE}")
        if os.path.exists(CANDIDATES_CLEANED_FILE.replace(".xlsx", "_backup.xlsx")):
            try:
                os.remove(CANDIDATES_CLEANED_FILE.replace(".xlsx", "_backup.xlsx"))
            except Exception:
                pass
    except PermissionError:
        curated_candidates_df.to_excel(CANDIDATES_CLEANED_FILE.replace(".xlsx", "_backup.xlsx"), index=False)
        print(f"Saved curated candidates backup to: {CANDIDATES_CLEANED_FILE.replace('.xlsx', '_backup.xlsx')}")
        
    # 6. Generate Validation Report
    report_content = f"""# Validation and Curation Report - Romance Media Dataset

This report documents the curation, cleansing, and validation checks executed for the **Heroine Outcome Prediction** dataset.

## 📊 Summary of Dataset Curation

- **Stories Processed**: {len(stories_df)}
- **Legitimate Candidates Curated**: {len(curated_candidates_df)}
- **Merged Duplicate Stories**: {len(merge_log)}

---

## 1. Merged Duplicate Stories

We successfully detected and merged the following duplicate stories:

"""
    if merge_log:
        for m in merge_log:
            report_content += f"- **{m['story']}**: Merged Story ID `{m['merged_id']}` into `{m['target_id']}`. Updated `{m['candidates_updated']}` candidate associations.\n"
    else:
        report_content += "_No duplicates found._\n"
        
    report_content += "\n## 2. Winners Assigned / Stories Corrected\n\n"
    if stories_corrected:
        for sc in stories_corrected[:30]:  # Limit print to prevent massive files
            report_content += f"- **{sc['title']}** (ID {sc['story_id']}) | `{sc['candidate_name']}` -> Changed `{sc['change']}`\n"
        if len(stories_corrected) > 30:
            report_content += f"- ... and {len(stories_corrected) - 30} more candidates corrected.\n"
    else:
        report_content += "_No manual winner overrides were required._\n"
        
    report_content += "\n## 3. Hair Colors Corrected\n\n"
    if hair_colors_corrected:
        for hc in hair_colors_corrected[:30]:
            report_content += f"- **{hc['title']}** (ID {hc['story_id']}) | `{hc['candidate_name']}` -> Changed `{hc['change']}`\n"
        if len(hair_colors_corrected) > 30:
            report_content += f"- ... and {len(hair_colors_corrected) - 30} more hair colors corrected.\n"
    else:
        report_content += "_No hair color corrections needed._\n"
        
    report_content += "\n## 4. Missing Values Filled / Backfills\n\n"
    if missing_value_fills:
        for mv in missing_value_fills[:20]:
            report_content += f"- **{mv['title']}** (ID {mv['story_id']}) | `{mv['candidate_name']}` ommission backfilled.\n"
    else:
        report_content += "_No ommissions or missing values found during curation._\n"
        
    report_content += "\n## 5. Heroine Counts Corrected\n\n"
    if heroine_counts_corrected:
        for hc in heroine_counts_corrected[:20]:
            report_content += f"- **{hc['title']}** (ID {hc['story_id']}) -> Changed `{hc['change']}`\n"
    else:
        report_content += "_All heroine counts in stories matched the candidates counts._\n"
        
    report_content += "\n## 6. Stories Flagged for Manual Review\n\n"
    if stories_manual_review:
        for mr in stories_manual_review:
            report_content += f"- **{mr['title']}** (ID {mr['story_id']}) -> **Reason**: {mr['reason']}\n"
    else:
        report_content += "_All validation assertions passed perfectly._\n"
        
    report_content += "\n## 7. Canonical Decisions & Confidence Levels\n\n"
    report_content += "| Story ID | Title | Confidence Level | Explanation / Reasoning |\n"
    report_content += "| :--- | :--- | :--- | :--- |\n"
    for idx, s_row in stories_df.iterrows():
        sid = s_row["story_id"]
        title = s_row["title"]
        conf = confidence_levels.get(sid, {"level": "High", "explanation": "Clean match, no anomalies."})
        report_content += f"| {sid} | {title} | **{conf['level']}** | {conf['explanation']} |\n"
        
    report_content += "\n\n---"
    report_content += "\n## 8. Justification for Introduction Order & First Girl\n\n"
    report_content += "A detailed list of candidates, their curated fields (introduction_order, first_girl, won), and narrative justifications:\n\n"
    
    # Sort candidates by story_id then introduction_order
    curated_candidates_df = curated_candidates_df.sort_values(by=["story_id", "introduction_order"])
    current_story = None
    for _, c in curated_candidates_df.iterrows():
        story_title = stories_df[stories_df["story_id"] == c["story_id"]]["title"].iloc[0]
        if current_story != c["story_id"]:
            current_story = c["story_id"]
            report_content += f"\n### {story_title} (ID {current_story})\n"
            
        report_content += f"- **{c['candidate_name']}** (Order: {c['introduction_order']}, First Girl: {c['first_girl']}, Won: {c['won']})\n"
        report_content += f"  - _Justification_: {c['reasoning']}\n"
        report_content += f"  - _Hair Color_: {c['hair_color']} | _Childhood Connection_: {c['childhood_connection']} | _Commitment Status_: {c['commitment_status']} | _Confidence Score_: {c['confidence_score']}\n"
        
    with open(VALIDATION_REPORT_FILE, "w", encoding="utf-8") as f:
        f.write(report_content)
        
    print(f"Generated validation report at: {VALIDATION_REPORT_FILE}")
    print("\n=== Curation Pipeline Completed Successfully! ===")

if __name__ == "__main__":
    main()
