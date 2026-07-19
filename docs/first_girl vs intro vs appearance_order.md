1. first_girl (The Tropes Flag - Binary: 1 or 0)
What it is: Is this character framed as the main/primary heroine of the story from the start?
The Justification: "First Girl" is an official narrative trope in writing. It has less to do with the clock and more to do with who the author wants the audience to focus on.
Example (Nisekoi): Chitoge Kirisaki is the "First Girl" (first_girl = 1). Even though she isn't the first girl the protagonist knows, she is the main female lead who drives the plot from chapter 1.
2. introduction_order (The Narrative Staging - Integer: 1, 2, 3...)
What it is: The sequential order in which the characters are formally introduced to the audience as actual characters in the main storyline.
The Justification: This tells the model the "rivalry order." The 1st girl starts with a clean slate. The 2nd girl enters as a disruptor/rival to the 1st. The 3rd girl has to break through two pre-existing dynamics, and so on.
Example (Nisekoi):
Chitoge Kirisaki is 1 (introduced first on page 2 when she knees Raku in the face).
Kosaki Onodera is 2 (introduced shortly after in the classroom).
Seishirou Tsugumi is 3 (transfers in later).
Marika Tachibana is 4 (transfers in even later).
3. appearance_order (The Literal Chronology - Integer: 1, 2, 3...)
What it is: The literal, physical chronological order in which the character appears on a page or screen—even if it's just a 1-second flashback prologue or a cameo before the main story starts.
The Justification: Authors love to tease characters in prologue flashbacks (like childhood promises) before the main story begins. A character might physically appear on page 1, but not be formally "introduced" as a character until chapter 5.
Example (Nisekoi):
Kosaki Onodera is 1 because she physically appears on the very first panel of page 1 during the childhood promise flashback.
Chitoge Kirisaki is 2 because she doesn't physically show up until page 2.
Why this is huge for your Machine Learning model:
By separating these three, you can answer amazing questions like:

Does physically appearing first (appearance_order = 1) matter, or does the author's narrative framing (first_girl = 1) carry all the weight? (Spoiler: Usually, first_girl is a cheat code, but separating them proves it mathematically!).