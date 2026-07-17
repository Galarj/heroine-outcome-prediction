# Project Scope
This dataset contains Japanese romance media with multiple viable romantic candidates.

This includes media such as:
- Anime
- Manga
- Visual Novels
- Light Novels

Excluded:
- Western media
- Fan fiction
- Dating simulators with no canonical route
- Stories with no romance

Criteria:
A story must satisfy ALL of the following:
- Has a clear romantic subplot or main Romance
- Has a canonical romantic outcome.
- Winner can be verified from official material

# Units of observation
One row represents one Heroine 
Example:

NISEKOI
- Chitoge
- Onodera
- Tsugumi
- Marika
4 heroines, 4 rows

Winner will be marked with boolean values

Won = 1

The heroine canonically ends up with the protagonist.

Won = 0

Every other heroine.

Only ONE heroine may have Won = 1.

# First Girl

First Girl = 1

The first major romantic heroine introduced.

Not:

- Random background girl
- Flashback child
- Minor character

Only ONE heroine may have First Girl = 1.

# Data Sources

Preferred sources:

- Original manga/light novel/visual novel
- Official anime
- MyAnimeList
- AniList
- VNDB
- Official wikis (for factual information only)

---
