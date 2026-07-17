# Project Scope

This dataset contains Japanese romance media with multiple viable romantic candidates.

Included media:
- Anime
- Manga
- Light Novels
- Visual Novels

Excluded:
- Western media
- Fan fiction
- Dating simulators with no canonical route
- Stories with no romance
- Stories with multiple official endings/routes
- Stories with no confirmed canonical winner

## Inclusion Criteria

A story must satisfy ALL of the following:

- Has a clear romantic subplot or primary romance.
- Has at least two viable romantic candidates.
- Has one canonical romantic outcome.
- The canonical winner can be verified from official material.
- The romantic outcome is established by the original source material.

---

# Units of Observation

One row represents one heroine.

Example:

Nisekoi

- Chitoge
- Onodera
- Tsugumi
- Marika

4 heroines = 4 rows

---

# Target Variable

## Won

Won = 1

The heroine canonically ends up with the protagonist.

Won = 0

Every other heroine.

Rules:

- Exactly ONE heroine may have `Won = 1`.
- Every other heroine must have `Won = 0`.

---

# Heroine Inclusion Rules

A heroine is included if she satisfies at least ONE of the following:

- Explicitly expresses romantic interest.
- Is treated by the story as a legitimate romantic candidate.
- Is recognized by the narrative as part of the central romance.

Excluded:

- Joke candidates
- One-episode crushes
- Purely comedic affection
- Characters with no realistic romantic possibility

---
# Target Audience

Represents the intended primary audience of the original work.

Allowed values:

- Male
- Female
- General
- Unknown

Definitions:

**Male**
- Works primarily marketed toward a male audience.
- Includes shounen manga, seinen manga, and most male-oriented light novels and visual novels.

Examples:
- Nisekoi
- Oregairu
- Saekano
- The Quintessential Quintuplets

---

**Female**
- Works primarily marketed toward a female audience.
- Includes shoujo manga, josei manga, and most female-oriented romance works.

Examples:
- Fruits Basket
- Kimi ni Todoke
- Nana

---

**General**
- Works intended for a broad audience without a clearly defined primary gender demographic.

Examples:
- Family-oriented romance
- Some anime-original productions

---

**Unknown**
- Insufficient information exists to determine the intended audience.

Rules:

- Every story must have exactly one `target_audience`.
- Classification should follow the original source material whenever possible.
- Never infer the audience solely from genre or fan demographics.

---

# Demographic

Represents the official demographic classification of the original source material.

Allowed values:

- Shounen
- Shoujo
- Seinen
- Josei
- Kodomo
- Unknown

Definitions:

**Shounen**
- Originally serialized in a magazine primarily targeting teenage boys.

**Shoujo**
- Originally serialized in a magazine primarily targeting teenage girls.

**Seinen**
- Originally serialized in a magazine primarily targeting adult men.

**Josei**
- Originally serialized in a magazine primarily targeting adult women.

**Kodomo**
- Originally created for children.

**Unknown**
- No official demographic exists or the work does not use demographic classifications (e.g., many Light Novels, Visual Novels, and Anime Originals).

Rules:

- Use only official demographic classifications.
- Never guess or infer a demographic.
- If no official demographic exists, record `Unknown`.
- Demographic should always refer to the original source material, not an adaptation.

# Feature Engineering Rules

## First Girl

First Girl = 1

The first major romantic heroine introduced in the story.

Not counted:

- Background characters
- Flashback-only appearances
- Minor characters
- Non-romantic introductions

Rules:

- Exactly ONE heroine may have `First Girl = 1`.

---

# Canon Source

Whenever possible, labels should be based on the original source material.

Priority:

1. Original Manga
2. Original Light Novel
3. Original Visual Novel (single-route only)
4. Anime Original

Anime adaptations should not override the original canon unless the anime itself is the original work.

---

# Missing Data

Unknown information should be recorded as:

- Unknown (categorical)
- NA (not applicable)

Never leave cells blank.

---

# Naming Convention

Story titles should use official English titles whenever available.

Character names should use the most common romanization.

Example:

Correct:
- Chitoge Kirisaki
- Yui Yuigahama

Avoid:
- Kirisaki Chitoge
- Yuigahama Yui (unless consistently used throughout the dataset)

---

# Data Quality Rules

Every story should be reviewed before being added.

Checklist:

✓ Canonical winner verified

✓ Heroine count verified

✓ Source material verified

✓ No duplicate stories

✓ All categorical values follow the allowed categories

---

# Data Sources

Preferred sources:

- Original Manga
- Original Light Novel
- Original Visual Novel
- Official Anime
- MyAnimeList
- AniList
- VNDB
- Official Wikis (for factual verification only)

Community forums may be used for discussion but should never be used as the primary source for factual labels.