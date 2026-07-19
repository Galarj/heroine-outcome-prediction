## candidate_id

Unique identifier assigned to each romantic candidate.

Rules:
- Must be unique across the entire dataset.
- Cannot be reused.
- Has no ranking or meaning.
- Should not be used as a predictive feature.

Example:
C0001
C0002
C0003


## story_id

Identifier linking a romantic candidate to a story.

Rules:
- Must match exactly one story in the story dataset.
- Multiple candidates may share the same story_id.
- Cannot be empty.
- Does not represent popularity, ranking, or release order.
- Should not be used as a predictive feature in machine learning.

## story_id

Identifier linking a romantic candidate to a story.

Rules:
- Must match exactly one story in the story dataset.
- Multiple candidates may share the same story_id.
- Cannot be empty.
- Does not represent popularity, ranking, or release order.
- Should not be used as a predictive feature in machine learning.

## candidate_name

The official or most commonly used romanized name of the romantic candidate.

Rules:
- Use the most common English romanization.
- Use the format: Given Name + Family Name.
- Do not include honorifics.
- Do not include nicknames unless they are the official/common name.
- Names must be consistent across the dataset.

Examples:

Correct:
- Chitoge Kirisaki
- Yui Yuigahama
- Taiga Aisaka

Avoid:
- Kirisaki Chitoge
- Yuigahama Yui
- Chitoge-san

## candidate_gender

The gender identity of the romantic candidate.

Allowed values:

Female
Male
Other
Unknown

Rules:
- Use official character information whenever available.
- Do not infer gender based only on appearance.
- Unknown may be used when information is unavailable.

## won

Binary target variable indicating the canonical romantic outcome.

Allowed values:

1 = Candidate canonically ends up with protagonist
0 = Candidate does not end up with protagonist

Rules:
- Exactly ONE candidate per story must have won = 1.
- All other candidates in the same story must have won = 0.
- The label must be verified from canonical source material.
- Personal preference or popularity must never determine the value.
- Open-ended stories cannot have a confirmed winner.

## introduction_order

The chronological order in which a character becomes a legitimate romantic candidate.

Rules:
- Assign numbers starting from 1.
- Each candidate in a story must have a unique introduction order.
- The order should be based on romantic relevance, not first appearance.
- Only count major romantic candidates.
- Do not count background characters or non-romantic appearances.

## childhood_connection

Rules:
- Judge based on the relationship before the main story begins.
- A single childhood encounter does not qualify as Childhood Friend.
- Childhood Promise should only be used when an explicit romantic/future promise exists.

Priority:

Childhood Promise > Childhood Friend > Acquaintance > None

Describes whether the candidate has a meaningful childhood relationship with the protagonist.

Allowed values:

None
Acquaintance
Childhood Friend
Childhood Promise

## commitment_status

Describes whether the candidate has a pre-existing romantic commitment with the protagonist.

Allowed values:

None
Promise
Engagement
Marriage

## primary_archetype

The dominant personality archetype of the romantic candidate.

Allowed values:

Tsundere
Kuudere
Dandere
Genki
Yandere
Deredere
Onee-san
Mixed
Unknown

## hair_color

The primary hair color of the romantic candidate based on official character design.

Allowed values:

Black
Brown
Blonde
Red
Blue
Pink
Silver
White
Green
Purple
Orange
Other
Unknown

## romance_development_stage

### Definition

The point in the story where the candidate becomes a significant romantic possibility for the protagonist.

This measures when the romance develops, not when the character first appears.

---

### Allowed Values

Early  
Middle  
Late  
Unknown

---

### Rules

- Judge based on when the character becomes romantically important.
- Do not use the ending outcome when assigning this label.
- Do not confuse first appearance with romantic development.
- Use the original source material whenever possible.

---

### Values

## Early

The character becomes a romantic candidate during the beginning of the story.

Examples:
- Main heroine established immediately.
- Romantic tension exists from the start.
- Candidate is part of the initial romance setup.

---

## Middle

The character becomes a serious romantic candidate after the initial setup but before the final arcs.

Examples:
- Feelings develop later.
- A supporting character becomes a romantic rival.

---

## Late

The character becomes a romantic candidate near the final portion of the story.

Examples:
- Late introduction as a love interest.
- Romantic importance appears close to the ending.

---

### Important Notes

- First appearance does not determine this value.
- A childhood friend is not automatically Early.
- A winner is not automatically Late.