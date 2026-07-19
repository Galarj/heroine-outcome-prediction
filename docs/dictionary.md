# Data Dictionary - Heroine Outcome Prediction Dataset

This document serves as the official data dictionary for the romance and harem media prediction datasets: [stories_cleaned.xlsx] and [candidates_cleaned.xlsx]candidates_cleaned.xlsx).

---

## 📖 1. Stories Table (`stories_cleaned.xlsx`)
This table contains record metadata for each individual romance/harem series.

| Column Name | Data Type | Description | Allowed Values / Formatting |
| :--- | :--- | :--- | :--- |
| **`story_id`** | Integer | Unique identifier for the story. | `1, 2, 3...` |
| **`title`** | String | The official title of the series (English translation preferred). | e.g. `Nisekoi`, `Fruits Basket` |
| **`medium`** | Category | The primary source material format of the series. | `Manga`, `Light Novel`, `Visual Novel`, `Anime` |
| **`demographic`** | Category | The target marketing demographic of the original work. | `Shounen`, `Seinen`, `Shoujo`, `Josei`, `Kids` |
| **`mal_id`** | Integer | The official database ID of the work on MyAnimeList. | e.g. `21703` |
| **`mal_score`** | Float | Average user review score on MyAnimeList. | `1.0` to `10.0` |
| **`mal_popularity`** | Integer | Popularity rank on MAL based on member count. | `1, 2, 3...` |
| **`mal_members`** | Integer | Total count of MAL members who added this title to their list. | e.g. `450000` |
| **`mal_favorites`** | Integer | Total count of MAL users who favorited this title. | e.g. `12500` |
| **`mal_genres`** | String | List of official MAL genres separated by semicolons. | e.g. `Comedy; Romance` |
| **`mal_themes`** | String | List of official MAL theme tags separated by semicolons. | e.g. `Harem; School; Love Polygon` |
| **`serialization`** | String | The publisher, magazine, or visual novel studio responsible for the work. | e.g. `Shounen Jump (Weekly)`, `Key` |
| **`heroine_count`** | Integer | The total number of candidates registered for this story in our dataset. | `1, 2, 3...` |

---

## ⚔️ 2. Candidates Table (`candidates_cleaned.xlsx`)
This table contains records for all romantic candidates/love interests within the stories.

| Column Name | Data Type | Description | Allowed Values / Formatting |
| :--- | :--- | :--- | :--- |
| **`candidate_id`** | String | Unique candidate ID, sequentially ordered by story and introduction. | Format: `C` + 4-digit code (e.g., `C0001`) |
| **`story_id`** | Integer | Foreign key linking the candidate to their story in the Stories Table. | `1, 2, 3...` |
| **`candidate_name`** | String | Name of the character (in English format: First Last). | e.g., `Chitoge Kirisaki` |
| **`candidate_gender`** | Category | The gender of the candidate. | `Female`, `Male` |
| **`won`** | Binary (Int) | Target label: whether the candidate won the romantic ending. | `1` = Won (Canonical ending), `0` = Lost |
| **`first_girl`** | Binary (Int) | Trope flag: whether the candidate is the narrative's "First Girl". | `1` = Yes (Primary heroine framing), `0` = No |
| **`introduction_order`** | Integer | The sequential order in which they are formally introduced as a candidate. | `1` = First introduced, `2` = Second, etc. |
| **`appearance_order`** | Integer | The chronological order in which they physically appear in the story. | `1` = Appears first, `2` = Appears second, etc. |
| **`childhood_connection`**| Category | The prior relationship status before the main story timeline. | `None`, `Childhood Friend`, `Childhood Promise`, `Acquaintance`, `Unknown` |
| **`commitment_status`** | Category | Romantic status anchors established during the story. | `None`, `Promise`, `Engagement`, `Marriage`, `Unknown` |
| **`primary_archetype`** | Category | The primary "Dere" personality archetype of the character. | `Tsundere`, `Kuudere`, `Dandere`, `Genki`, `Deredere`, `Onee-san`, `Yandere` |
| **`hair_color`** | Category | The primary hair color of the character. | `Black`, `Brown`, `Blonde`, `Red`, `Blue`, `Pink`, `Silver`, `White`, `Green`, `Purple`, `Other` |
| **`confidence_score`** | Float | Level of confidence in the curation details. | Range: `0.0` to `1.0` |
| **`reasoning`** | String | Brief narrative justification explaining their introduction, connection, and ending. | e.g. detailed narrative explanation text |
| **`first_chapter_or_episode`** | String | The exact chapter or episode of their first appearance. | e.g., `Chapter 1`, `Episode 1` |
