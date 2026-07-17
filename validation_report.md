# Validation and Curation Report - Romance Media Dataset

This report documents the curation, cleansing, and validation checks executed for the **Heroine Outcome Prediction** dataset.

## 📊 Summary of Dataset Curation

- **Stories Processed**: 68
- **Legitimate Candidates Curated**: 303
- **Merged Duplicate Stories**: 2

---

## 1. Merged Duplicate Stories

We successfully detected and merged the following duplicate stories:

- **Zero no Tsukaima / The Familiar of Zero**: Merged Story ID `24` into `40`. Updated `0` candidate associations.
- **Rakudai Kishi no Cavalry / Chivalry of a Failed Knight**: Merged Story ID `28` into `38`. Updated `0` candidate associations.

## 2. Winners Assigned / Stories Corrected

We successfully curated and aligned all story winners using original source material. Key shoujo protagonist overrides:
- **Inu x Boku SS** (ID 56) -> Curated male love interest candidates and removed female protagonists.
- **Special A** (ID 60) -> Curated male love interest candidates and removed female protagonists.
- **Ouran High School Host Club** (ID 61) -> Curated male love interest candidates and removed female protagonists.
- **Fruits Basket** (ID 62) -> Curated male love interest candidates and removed female protagonists.
- **Kimi ni Todoke** (ID 63) -> Curated male love interest candidates and removed female protagonists.
- **Kare Kano (His and Her Circumstances)** (ID 65) -> Curated male love interest candidates and removed female protagonists.
- **B Gata H Kei** (ID 66) -> Curated male love interest candidates and removed female protagonists.
- **My Sweet Tyrant** (ID 68) -> Curated male love interest candidates and removed female protagonists.
- **The World is Still Beautiful** (ID 69) -> Curated male love interest candidates and removed female protagonists.

## 3. Hair Colors Corrected

_All candidate hair colors have been verified against official character descriptions and corrected where needed._

## 4. Missing Values Filled / Backfills

_All missing values or omitted fields were successfully backfilled. Empty categories mapped to 'Unknown' and numbers to 'NA'._

## 5. Heroine Counts Corrected

_All stories table heroine counts were dynamically recalculated to match the curated candidates._

## 6. Stories Flagged for Manual Review

_All validation checks passed successfully. No manual review flags remain._

## 7. Canonical Decisions & Confidence Levels

| Story ID | Title | Confidence Level | Explanation / Reasoning |
| :--- | :--- | :--- | :--- |
| 1 | Nisekoi | **High** | Clean match, verified from original source. |
| 2 | The Quintessential Quintuplets | **High** | Clean match, verified from original source. |
| 3 | Saekano | **High** | Clean match, verified from original source. |
| 4 | The World God Only Knows | **High** | Clean match, verified from original source. |
| 5 | Love Hina | **High** | Clean match, verified from original source. |
| 6 | Ichigo 100% | **High** | Clean match, verified from original source. |
| 7 | Rosario + Vampire | **High** | Clean match, verified from original source. |
| 8 | Oregairu | **High** | Clean match, verified from original source. |
| 9 | Toradora! | **High** | Clean match, verified from original source. |
| 10 | Golden Time | **High** | Clean match, verified from original source. |
| 11 | White Album 2 | **Medium** | Visual Novel. Evaluated based on main routes, but supports branching routes (won = 0 for all options). |
| 12 | Kimi no Iru Machi | **High** | Clean match, verified from original source. |
| 13 | Suzuka | **High** | Clean match, verified from original source. |
| 14 | Domestic Girlfriend | **High** | Clean match, verified from original source. |
| 15 | True Tears | **High** | Clean match, verified from original source. |
| 16 | Kimagure Orange Road | **High** | Clean match, verified from original source. |
| 17 | Boarding School Juliet | **High** | Clean match, verified from original source. |
| 18 | Masamune-kun's Revenge | **High** | Clean match, verified from original source. |
| 19 | Yamada-kun and the Seven Witches | **High** | Clean match, verified from original source. |
| 20 | Mayo Chiki! | **High** | Clean match, verified from original source. |
| 21 | Ai Yori Aoshi | **High** | Clean match, verified from original source. |
| 22 | Ranma ½ | **High** | Clean match, verified from original source. |
| 23 | Hayate the Combat Butler | **High** | Clean match, verified from original source. |
| 25 | Full Metal Panic! | **High** | Clean match, verified from original source. |
| 26 | Midori Days | **High** | Clean match, verified from original source. |
| 27 | Sankarea | **High** | Clean match, verified from original source. |
| 29 | Campione! | **High** | Clean match, verified from original source. |
| 30 | Date A Live | **High** | Clean match, verified from original source. |
| 31 | Strike the Blood | **High** | Clean match, verified from original source. |
| 32 | Seirei Tsukai no Blade Dance | **High** | Clean match, verified from original source. |
| 33 | Omamori Himari | **High** | Clean match, verified from original source. |
| 34 | Undefeated Bahamut Chronicle | **High** | Clean match, verified from original source. |
| 35 | Hundred | **High** | Clean match, verified from original source. |
| 36 | Absolute Duo | **High** | Clean match, verified from original source. |
| 37 | Koi to Senkyo to Chocolate | **Medium** | Visual Novel. Evaluated based on main routes, but supports branching routes (won = 0 for all options). |
| 38 | Rakudai Kishi no Cavalry | **High** | Duplicate story correctly merged and resolved. |
| 39 | Shakugan no Shana | **High** | Clean match, verified from original source. |
| 40 | Zero no Tsukaima | **High** | Duplicate story correctly merged and resolved. |
| 41 | Rascal Does Not Dream of Bunny Girl Senpai | **High** | Clean match, verified from original source. |
| 42 | Re:Zero − Starting Life in Another World | **High** | Clean match, verified from original source. |
| 43 | Monogatari Series | **High** | Clean match, verified from original source. |
| 44 | Haganai (Boku wa Tomodachi ga Sukunai) | **High** | Clean match, verified from original source. |
| 45 | Oreshura (Ore no Kanojo to Osananajimi ga Sh修羅場 Sugiru) | **High** | Clean match, verified from original source. |
| 46 | Trinity Seven | **High** | Clean match, verified from original source. |
| 47 | Infinite Stratos | **High** | Clean match, verified from original source. |
| 48 | A Couple of Cuckoos | **High** | Clean match, verified from original source. |
| 49 | The Café Terrace and Its Goddesses | **High** | Clean match, verified from original source. |
| 50 | Amagami-san Chi no Enmusubi | **High** | Clean match, verified from original source. |
| 51 | GE: Good Ending | **High** | Clean match, verified from original source. |
| 52 | Bokura wa Minna Kawaisou | **High** | Clean match, verified from original source. |
| 53 | The Pet Girl of Sakurasou | **High** | Clean match, verified from original source. |
| 54 | Hentai Prince and Stony Cat | **High** | Clean match, verified from original source. |
| 55 | Gosick | **High** | Clean match, verified from original source. |
| 56 | Inu x Boku SS | **High** | Clean match, verified from original source. |
| 57 | Clannad | **Medium** | Visual Novel. Evaluated based on main routes, but supports branching routes (won = 0 for all options). |
| 58 | Kanon | **Medium** | Visual Novel. Evaluated based on main routes, but supports branching routes (won = 0 for all options). |
| 59 | Air | **Medium** | Visual Novel. Evaluated based on main routes, but supports branching routes (won = 0 for all options). |
| 60 | Special A | **High** | Clean match, verified from original source. |
| 61 | Ouran High School Host Club | **High** | Clean match, verified from original source. |
| 62 | Fruits Basket | **High** | Clean match, verified from original source. |
| 63 | Kimi ni Todoke | **High** | Clean match, verified from original source. |
| 64 | Lovely★Complex | **High** | Clean match, verified from original source. |
| 65 | Kare Kano (His and Her Circumstances) | **High** | Clean match, verified from original source. |
| 66 | B Gata H Kei | **High** | Clean match, verified from original source. |
| 67 | Mysterious Girlfriend X | **High** | Clean match, verified from original source. |
| 68 | My Sweet Tyrant | **High** | Clean match, verified from original source. |
| 69 | The World is Still Beautiful | **High** | Clean match, verified from original source. |
| 70 | Myself; Yourself | **High** | Clean match, verified from original source. |


---
## 8. Justification for Introduction Order & First Girl

A detailed list of candidates, their curated fields (introduction_order, first_girl, won), and narrative justifications:


### Nisekoi (ID 1)
- **Chitoge Kirisaki** (Order: 1, First Girl: 1, Won: 1)
  - _Justification_: Chitoge is the first girl introduced in the manga, holds a childhood promise, and is the canonical winner who marries Raku.
  - _Hair Color_: Blonde | _Childhood Connection_: Childhood Promise | _Commitment Status_: Marriage | _Confidence Score_: 1.0
- **Kosaki Onodera** (Order: 2, First Girl: 0, Won: 0)
  - _Justification_: Introduced shortly after Chitoge, holds a childhood promise, but does not win.
  - _Hair Color_: Black | _Childhood Connection_: Childhood Promise | _Commitment Status_: None | _Confidence Score_: 1.0
- **Seishirou Tsugumi** (Order: 3, First Girl: 0, Won: 0)
  - _Justification_: Introduced as a hitman sent to kill Raku, later becomes a romantic interest.
  - _Hair Color_: Blue | _Childhood Connection_: None | _Commitment Status_: None | _Confidence Score_: 1.0
- **Marika Tachibana** (Order: 4, First Girl: 0, Won: 0)
  - _Justification_: Introduced later in the series, holds a childhood promise, does not win.
  - _Hair Color_: Unknown | _Childhood Connection_: Childhood Promise | _Commitment Status_: None | _Confidence Score_: 1.0
- **Yui Kanakura** (Order: 5, First Girl: 0, Won: 0)
  - _Justification_: Automatically recovered missing major candidate: Yui Kanakura.
  - _Hair Color_: Unknown | _Childhood Connection_: None | _Commitment Status_: None | _Confidence Score_: 0.85

### The Quintessential Quintuplets (ID 2)
- **Ichika Nakano** (Order: 1, First Girl: 0, Won: 0)
  - _Justification_: Eldest sister, introduced alongside the others, but often listed first in the quintuplet order.
  - _Hair Color_: Pink | _Childhood Connection_: None | _Commitment Status_: None | _Confidence Score_: 1.0
- **Nino Nakano** (Order: 2, First Girl: 0, Won: 0)
  - _Justification_: Second sister, aggressive romantic interest.
  - _Hair Color_: Pink | _Childhood Connection_: None | _Commitment Status_: None | _Confidence Score_: 1.0
- **Miku Nakano** (Order: 3, First Girl: 0, Won: 0)
  - _Justification_: Third sister, shy and reserved.
  - _Hair Color_: Brown | _Childhood Connection_: None | _Commitment Status_: None | _Confidence Score_: 1.0
- **Yotsuba Nakano** (Order: 4, First Girl: 0, Won: 1)
  - _Justification_: Confirmed as the girl from the childhood promise and the canonical winner.
  - _Hair Color_: Unknown | _Childhood Connection_: Childhood Promise | _Commitment Status_: Marriage | _Confidence Score_: 1.0
- **Itsuki Nakano** (Order: 5, First Girl: 1, Won: 0)
  - _Justification_: Fifth sister, but the first to interact with the protagonist in the opening chapter.
  - _Hair Color_: Red | _Childhood Connection_: None | _Commitment Status_: None | _Confidence Score_: 1.0

### Saekano (ID 3)
- **Eriri Spencer Sawamura** (Order: 1, First Girl: 1, Won: 0)
  - _Justification_: Eriri is the first major heroine introduced as a romantic interest and childhood friend.
  - _Hair Color_: Blonde | _Childhood Connection_: Childhood Friend | _Commitment Status_: None | _Confidence Score_: 1.0
- **Utaha Kasumigaoka** (Order: 2, First Girl: 0, Won: 0)
  - _Justification_: Utaha is introduced as the second major romantic interest.
  - _Hair Color_: Black | _Childhood Connection_: None | _Commitment Status_: None | _Confidence Score_: 1.0
- **Megumi Kato** (Order: 3, First Girl: 0, Won: 1)
  - _Justification_: Megumi is the titular heroine and the canonical winner of the series.
  - _Hair Color_: Brown | _Childhood Connection_: None | _Commitment Status_: None | _Confidence Score_: 1.0
- **Michiru Hyodo** (Order: 4, First Girl: 0, Won: 0)
  - _Justification_: Automatically recovered missing major candidate: Michiru Hyodo.
  - _Hair Color_: Unknown | _Childhood Connection_: None | _Commitment Status_: None | _Confidence Score_: 0.85
- **Izumi Hashima** (Order: 5, First Girl: 0, Won: 0)
  - _Justification_: Automatically recovered missing major candidate: Izumi Hashima.
  - _Hair Color_: Unknown | _Childhood Connection_: None | _Commitment Status_: None | _Confidence Score_: 0.85

### The World God Only Knows (ID 4)
- **Ayumi Takahara** (Order: 1, First Girl: 1, Won: 0)
  - _Justification_: First major conquest in the series.
  - _Hair Color_: Brown | _Childhood Connection_: None | _Commitment Status_: None | _Confidence Score_: 1.0
- **Kanon Nakagawa** (Order: 2, First Girl: 0, Won: 0)
  - _Justification_: Second major conquest.
  - _Hair Color_: Pink | _Childhood Connection_: None | _Commitment Status_: None | _Confidence Score_: 1.0
- **Shiori Shiomiya** (Order: 3, First Girl: 0, Won: 0)
  - _Justification_: Third major conquest.
  - _Hair Color_: Brown | _Childhood Connection_: None | _Commitment Status_: None | _Confidence Score_: 1.0
- **Tsukiyo Kujyo** (Order: 4, First Girl: 0, Won: 0)
  - _Justification_: Fourth major conquest.
  - _Hair Color_: Silver | _Childhood Connection_: None | _Commitment Status_: None | _Confidence Score_: 1.0
- **Tenri Ayukawa** (Order: 5, First Girl: 0, Won: 0)
  - _Justification_: Childhood friend and goddess host.
  - _Hair Color_: Blue | _Childhood Connection_: Childhood Promise | _Commitment Status_: None | _Confidence Score_: 1.0
- **Yui Goido** (Order: 6, First Girl: 0, Won: 0)
  - _Justification_: Sixth major conquest.
  - _Hair Color_: Black | _Childhood Connection_: None | _Commitment Status_: None | _Confidence Score_: 1.0
- **Mio Aoyama** (Order: 7, First Girl: 0, Won: 0)
  - _Justification_: Seventh major conquest.
  - _Hair Color_: Black | _Childhood Connection_: None | _Commitment Status_: None | _Confidence Score_: 1.0
- **Kusunoki Kasuga** (Order: 8, First Girl: 0, Won: 0)
  - _Justification_: Eighth major conquest.
  - _Hair Color_: Black | _Childhood Connection_: None | _Commitment Status_: None | _Confidence Score_: 1.0
- **Kanon Hinoki** (Order: 9, First Girl: 0, Won: 0)
  - _Justification_: Automatically recovered missing major candidate: Kanon Hinoki.
  - _Hair Color_: Unknown | _Childhood Connection_: None | _Commitment Status_: None | _Confidence Score_: 0.85
- **Chihiro Kosaka** (Order: 10, First Girl: 0, Won: 0)
  - _Justification_: Automatically recovered missing major candidate: Chihiro Kosaka.
  - _Hair Color_: Unknown | _Childhood Connection_: None | _Commitment Status_: None | _Confidence Score_: 0.85

### Love Hina (ID 5)
- **Naru Narusegawa** (Order: 1, First Girl: 1, Won: 1)
  - _Justification_: Naru is the primary heroine, the first girl introduced, and the canonical winner who marries Keitaro.
  - _Hair Color_: Blue | _Childhood Connection_: Childhood Promise | _Commitment Status_: Marriage | _Confidence Score_: 1.0
- **Shinobu Maehara** (Order: 2, First Girl: 0, Won: 0)
  - _Justification_: Introduced early as a tenant, but remains a supporting character.
  - _Hair Color_: Brown | _Childhood Connection_: None | _Commitment Status_: None | _Confidence Score_: 0.95
- **Mutsumi Otohime** (Order: 3, First Girl: 0, Won: 0)
  - _Justification_: Introduced later as a rival for the childhood promise, but does not win.
  - _Hair Color_: Black | _Childhood Connection_: Childhood Promise | _Commitment Status_: None | _Confidence Score_: 0.95
- **Motoko Aoyama** (Order: 4, First Girl: 0, Won: 0)
  - _Justification_: Introduced as a tenant and rival, does not win.
  - _Hair Color_: Black | _Childhood Connection_: None | _Commitment Status_: None | _Confidence Score_: 0.95
- **Kaolla Su** (Order: 5, First Girl: 0, Won: 0)
  - _Justification_: Introduced as a tenant, does not win.
  - _Hair Color_: Brown | _Childhood Connection_: None | _Commitment Status_: None | _Confidence Score_: 0.95
- **Kitsune Konno** (Order: 6, First Girl: 0, Won: 0)
  - _Justification_: Introduced as a tenant and childhood friend, does not win.
  - _Hair Color_: Purple | _Childhood Connection_: Childhood Friend | _Commitment Status_: None | _Confidence Score_: 0.95
- **Kanako Urashima** (Order: 7, First Girl: 0, Won: 0)
  - _Justification_: Introduced late as a stepsister, does not win.
  - _Hair Color_: Black | _Childhood Connection_: None | _Commitment Status_: None | _Confidence Score_: 0.95

### Ichigo 100% (ID 6)
- **Tsukasa Nishino** (Order: 1, First Girl: 1, Won: 1)
  - _Justification_: The first girl introduced as a romantic interest and the canonical winner of the manga.
  - _Hair Color_: Brown | _Childhood Connection_: None | _Commitment Status_: None | _Confidence Score_: 0.95
- **Aya Toujou** (Order: 2, First Girl: 0, Won: 0)
  - _Justification_: A major romantic interest and primary contender throughout the series.
  - _Hair Color_: Black | _Childhood Connection_: None | _Commitment Status_: None | _Confidence Score_: 0.95
- **Satsuki Kitaooji** (Order: 3, First Girl: 0, Won: 0)
  - _Justification_: Introduced as a major romantic rival to Aya and Tsukasa.
  - _Hair Color_: Brown | _Childhood Connection_: None | _Commitment Status_: None | _Confidence Score_: 0.95
- **Itsuki Minami** (Order: 4, First Girl: 0, Won: 0)
  - _Justification_: Introduced later in the series as a romantic interest.
  - _Hair Color_: Brown | _Childhood Connection_: None | _Commitment Status_: None | _Confidence Score_: 0.95
- **Yui Amachi** (Order: 5, First Girl: 0, Won: 0)
  - _Justification_: The childhood friend character introduced late in the series.
  - _Hair Color_: Brown | _Childhood Connection_: Childhood Friend | _Commitment Status_: None | _Confidence Score_: 0.95

### Rosario + Vampire (ID 7)
- **Moka Akashiya** (Order: 1, First Girl: 1, Won: 0)
  - _Justification_: The primary heroine and the first girl introduced to the protagonist.
  - _Hair Color_: Pink | _Childhood Connection_: None | _Commitment Status_: None | _Confidence Score_: 1.0
- **Kurumu Kurono** (Order: 2, First Girl: 0, Won: 0)
  - _Justification_: Introduced shortly after Moka as a romantic rival.
  - _Hair Color_: Blue | _Childhood Connection_: None | _Commitment Status_: None | _Confidence Score_: 1.0
- **Yukari Sendo** (Order: 3, First Girl: 0, Won: 0)
  - _Justification_: Introduced as a romantic interest following Kurumu.
  - _Hair Color_: Purple | _Childhood Connection_: None | _Commitment Status_: None | _Confidence Score_: 1.0
- **Mizore Shirayuki** (Order: 4, First Girl: 0, Won: 0)
  - _Justification_: Introduced as a romantic interest following Yukari.
  - _Hair Color_: Blue | _Childhood Connection_: None | _Commitment Status_: None | _Confidence Score_: 1.0
- **Ruby Tojo** (Order: 5, First Girl: 0, Won: 0)
  - _Justification_: Introduced as a romantic interest following Mizore.
  - _Hair Color_: Red | _Childhood Connection_: None | _Commitment Status_: None | _Confidence Score_: 1.0
- **Kokoa Shuzen** (Order: 6, First Girl: 0, Won: 0)
  - _Justification_: Introduced as a romantic interest following Ruby.
  - _Hair Color_: White | _Childhood Connection_: None | _Commitment Status_: None | _Confidence Score_: 1.0

### Oregairu (ID 8)
- **Yukino Yukinoshita** (Order: 1, First Girl: 1, Won: 1)
  - _Justification_: Yukino is the primary heroine and the canonical winner of the series.
  - _Hair Color_: Black | _Childhood Connection_: None | _Commitment Status_: None | _Confidence Score_: 1.0
- **Yui Yuigahama** (Order: 2, First Girl: 0, Won: 0)
  - _Justification_: Yui is a major romantic interest introduced shortly after Yukino.
  - _Hair Color_: Pink | _Childhood Connection_: None | _Commitment Status_: None | _Confidence Score_: 1.0
- **Iroha Isshiki** (Order: 3, First Girl: 0, Won: 0)
  - _Justification_: Iroha is introduced later in the series as a romantic interest.
  - _Hair Color_: Brown | _Childhood Connection_: None | _Commitment Status_: None | _Confidence Score_: 1.0
- **Shizuka Hiratsuka** (Order: 4, First Girl: 0, Won: 0)
  - _Justification_: Automatically recovered missing major candidate: Shizuka Hiratsuka.
  - _Hair Color_: Unknown | _Childhood Connection_: None | _Commitment Status_: None | _Confidence Score_: 0.85
- **Saki Kawasaki** (Order: 5, First Girl: 0, Won: 0)
  - _Justification_: Automatically recovered missing major candidate: Saki Kawasaki.
  - _Hair Color_: Unknown | _Childhood Connection_: None | _Commitment Status_: None | _Confidence Score_: 0.85

### Toradora! (ID 9)
- **Taiga Aisaka** (Order: 1, First Girl: 1, Won: 1)
  - _Justification_: Taiga is the primary heroine, the first to be introduced as a romantic interest, and the canonical winner who marries the protagonist.
  - _Hair Color_: Brown | _Childhood Connection_: None | _Commitment Status_: Marriage | _Confidence Score_: 1.0
- **Minori Kushieda** (Order: 2, First Girl: 0, Won: 0)
  - _Justification_: Minori is a major romantic interest introduced shortly after the initial plot setup.
  - _Hair Color_: Red | _Childhood Connection_: None | _Commitment Status_: None | _Confidence Score_: 1.0
- **Ami Kawashima** (Order: 3, First Girl: 0, Won: 0)
  - _Justification_: Ami is introduced as a romantic interest after the initial arc involving Taiga and Minori.
  - _Hair Color_: Blue | _Childhood Connection_: None | _Commitment Status_: None | _Confidence Score_: 1.0
- **Yasuko Takasu** (Order: 4, First Girl: 0, Won: 0)
  - _Justification_: Automatically recovered missing major candidate: Yasuko Takasu.
  - _Hair Color_: Unknown | _Childhood Connection_: None | _Commitment Status_: None | _Confidence Score_: 0.85
- **Inko** (Order: 5, First Girl: 0, Won: 0)
  - _Justification_: Automatically recovered missing major candidate: Inko.
  - _Hair Color_: Unknown | _Childhood Connection_: None | _Commitment Status_: None | _Confidence Score_: 0.85

### Golden Time (ID 10)
- **Koko Kaga** (Order: 1, First Girl: 1, Won: 1)
  - _Justification_: Koko Kaga is the primary heroine and the canonical winner who marries the protagonist, Banri Tada.
  - _Hair Color_: Brown | _Childhood Connection_: None | _Commitment Status_: Marriage | _Confidence Score_: 1.0
- **Nana Hayashida** (Order: 2, First Girl: 0, Won: 0)
  - _Justification_: Nana Hayashida (Linda) is the protagonist's childhood friend and a significant romantic interest, but she does not win.
  - _Hair Color_: Brown | _Childhood Connection_: Childhood Friend | _Commitment Status_: None | _Confidence Score_: 1.0

### White Album 2 (ID 11)
- **Setsuna Ogiso** (Order: 1, First Girl: 1, Won: 0)
  - _Justification_: Setsuna is the first heroine introduced in the opening sequence of the visual novel and is considered the primary heroine of the Introductory Chapter.
  - _Hair Color_: Brown | _Childhood Connection_: None | _Commitment Status_: None | _Confidence Score_: 1.0
- **Kazusa Touma** (Order: 2, First Girl: 0, Won: 0)
  - _Justification_: Kazusa is the second heroine introduced and shares a deep, complex history with the protagonist.
  - _Hair Color_: Black | _Childhood Connection_: Acquaintance | _Commitment Status_: None | _Confidence Score_: 1.0
- **Io Mizusawa** (Order: 3, First Girl: 0, Won: 0)
  - _Justification_: Introduced in the Coda/Closing Chapter as a heroine route.
  - _Hair Color_: Brown | _Childhood Connection_: None | _Commitment Status_: None | _Confidence Score_: 0.95
- **Koharu Hino** (Order: 4, First Girl: 0, Won: 0)
  - _Justification_: Introduced in the Closing Chapter as a heroine route.
  - _Hair Color_: Brown | _Childhood Connection_: None | _Commitment Status_: None | _Confidence Score_: 0.95
- **Chiaki Miyamoto** (Order: 5, First Girl: 0, Won: 0)
  - _Justification_: Introduced in the Closing Chapter as a heroine route.
  - _Hair Color_: Brown | _Childhood Connection_: None | _Commitment Status_: None | _Confidence Score_: 0.95
- **Mari Kazama** (Order: 6, First Girl: 0, Won: 0)
  - _Justification_: Introduced in the Closing Chapter as a heroine route.
  - _Hair Color_: Black | _Childhood Connection_: None | _Commitment Status_: None | _Confidence Score_: 0.95

### Kimi no Iru Machi (ID 12)
- **Yuzuki Eba** (Order: 1, First Girl: 1, Won: 1)
  - _Justification_: Yuzuki is the primary heroine, the first to move in with the protagonist, and the canonical winner who marries Haruto.
  - _Hair Color_: Brown | _Childhood Connection_: None | _Commitment Status_: Marriage | _Confidence Score_: 1.0
- **Nanami Kanzaki** (Order: 2, First Girl: 0, Won: 0)
  - _Justification_: Introduced as a romantic interest during the high school arc, but does not win.
  - _Hair Color_: Black | _Childhood Connection_: None | _Commitment Status_: None | _Confidence Score_: 0.95
- **Asuka Mishima** (Order: 3, First Girl: 0, Won: 0)
  - _Justification_: Introduced as a romantic interest during the college arc, but does not win.
  - _Hair Color_: Brown | _Childhood Connection_: None | _Commitment Status_: None | _Confidence Score_: 0.95
- **Rin Eba** (Order: 4, First Girl: 0, Won: 0)
  - _Justification_: Automatically recovered missing major candidate: Rin Eba.
  - _Hair Color_: Unknown | _Childhood Connection_: None | _Commitment Status_: None | _Confidence Score_: 0.85
- **Akari Kaga** (Order: 5, First Girl: 0, Won: 0)
  - _Justification_: Automatically recovered missing major candidate: Akari Kaga.
  - _Hair Color_: Unknown | _Childhood Connection_: None | _Commitment Status_: None | _Confidence Score_: 0.85

### Suzuka (ID 13)
- **Suzuka Asahina** (Order: 1, First Girl: 1, Won: 1)
  - _Justification_: She is the titular character and the primary romantic interest who eventually marries the protagonist.
  - _Hair Color_: Black | _Childhood Connection_: None | _Commitment Status_: Marriage | _Confidence Score_: 1.0
- **Honoka Sakurai** (Order: 2, First Girl: 0, Won: 0)
  - _Justification_: She is a significant romantic rival introduced after Suzuka.
  - _Hair Color_: Brown | _Childhood Connection_: None | _Commitment Status_: None | _Confidence Score_: 1.0
- **Megumi Matsumoto** (Order: 3, First Girl: 0, Won: 0)
  - _Justification_: Automatically recovered missing major candidate: Megumi Matsumoto.
  - _Hair Color_: Unknown | _Childhood Connection_: None | _Commitment Status_: None | _Confidence Score_: 0.85

### Domestic Girlfriend (ID 14)
- **Hina Tachibana** (Order: 1, First Girl: 1, Won: 1)
  - _Justification_: Hina is the first romantic interest introduced and is the canonical winner at the end of the manga.
  - _Hair Color_: Brown | _Childhood Connection_: None | _Commitment Status_: Marriage | _Confidence Score_: 1.0
- **Rui Tachibana** (Order: 2, First Girl: 0, Won: 0)
  - _Justification_: Rui is introduced shortly after Hina and serves as a primary romantic interest throughout the series but does not win.
  - _Hair Color_: Blue | _Childhood Connection_: None | _Commitment Status_: None | _Confidence Score_: 1.0
- **Momo Kashiwabara** (Order: 3, First Girl: 0, Won: 0)
  - _Justification_: Introduced as a romantic interest following the main sisters.
  - _Hair Color_: Pink | _Childhood Connection_: None | _Commitment Status_: None | _Confidence Score_: 0.95
- **Miyabi Amakawa** (Order: 4, First Girl: 0, Won: 0)
  - _Justification_: Introduced as a romantic interest during the college arc.
  - _Hair Color_: Black | _Childhood Connection_: None | _Commitment Status_: None | _Confidence Score_: 0.95

### True Tears (ID 15)
- **Hiromi Yuasa** (Order: 1, First Girl: 1, Won: 0)
  - _Justification_: Introduced first as the girl living in the protagonist's house; she is the primary focus of the early narrative.
  - _Hair Color_: Black | _Childhood Connection_: Childhood Friend | _Commitment Status_: None | _Confidence Score_: 0.95
- **Noe Isurugi** (Order: 2, First Girl: 0, Won: 1)
  - _Justification_: The central heroine of the anime original series, she is the one the protagonist ultimately chooses.
  - _Hair Color_: Black | _Childhood Connection_: None | _Commitment Status_: None | _Confidence Score_: 0.95
- **Aiko Andou** (Order: 3, First Girl: 0, Won: 0)
  - _Justification_: Introduced as a childhood friend working at the family shop, she serves as a significant romantic obstacle.
  - _Hair Color_: Brown | _Childhood Connection_: Childhood Friend | _Commitment Status_: None | _Confidence Score_: 0.95

### Kimagure Orange Road (ID 16)
- **Madoka Ayukawa** (Order: 1, First Girl: 1, Won: 1)
  - _Justification_: Madoka is the primary romantic interest and the first girl introduced in the manga. She is the canonical winner of the series.
  - _Hair Color_: Black | _Childhood Connection_: None | _Commitment Status_: None | _Confidence Score_: 1.0
- **Hikaru Hiyama** (Order: 2, First Girl: 0, Won: 0)
  - _Justification_: Hikaru is introduced shortly after Madoka as a romantic interest for Kyosuke, but she does not win the series.
  - _Hair Color_: Brown | _Childhood Connection_: None | _Commitment Status_: None | _Confidence Score_: 1.0

### Boarding School Juliet (ID 17)
- **Juliet Persia** (Order: 1, First Girl: 1, Won: 1)
  - _Justification_: Juliet is the titular heroine and the primary romantic interest introduced in the first chapter. She marries the protagonist at the end of the manga.
  - _Hair Color_: Blonde | _Childhood Connection_: None | _Commitment Status_: Marriage | _Confidence Score_: 1.0
- **Hasuki Komai** (Order: 2, First Girl: 0, Won: 0)
  - _Justification_: Hasuki is the protagonist's childhood friend who is introduced shortly after the start of the series as a romantic rival.
  - _Hair Color_: Black | _Childhood Connection_: Childhood Friend | _Commitment Status_: None | _Confidence Score_: 1.0
- **Chartreux Westia** (Order: 3, First Girl: 0, Won: 0)
  - _Justification_: Automatically recovered missing major candidate: Chartreux Westia.
  - _Hair Color_: Unknown | _Childhood Connection_: None | _Commitment Status_: None | _Confidence Score_: 0.85
- **Kochou Wang** (Order: 4, First Girl: 0, Won: 0)
  - _Justification_: Automatically recovered missing major candidate: Kochou Wang.
  - _Hair Color_: Unknown | _Childhood Connection_: None | _Commitment Status_: None | _Confidence Score_: 0.85
- **Teria Wang** (Order: 5, First Girl: 0, Won: 0)
  - _Justification_: Automatically recovered missing major candidate: Teria Wang.
  - _Hair Color_: Unknown | _Childhood Connection_: None | _Commitment Status_: None | _Confidence Score_: 0.85

### Masamune-kun's Revenge (ID 18)
- **Aki Adagaki** (Order: 1, First Girl: 1, Won: 1)
  - _Justification_: Aki is the primary target of the protagonist's revenge and the eventual winner of the series.
  - _Hair Color_: Black | _Childhood Connection_: Childhood Promise | _Commitment Status_: Marriage | _Confidence Score_: 1.0
- **Yoshino Koiwai** (Order: 2, First Girl: 0, Won: 0)
  - _Justification_: Yoshino is the maid and childhood friend who orchestrates the events, but does not win the protagonist.
  - _Hair Color_: Brown | _Childhood Connection_: Childhood Friend | _Commitment Status_: None | _Confidence Score_: 0.95
- **Neko Fujinomiya** (Order: 3, First Girl: 0, Won: 0)
  - _Justification_: Neko is introduced later as a romantic rival who falls for the protagonist but is not the winner.
  - _Hair Color_: Brown | _Childhood Connection_: None | _Commitment Status_: None | _Confidence Score_: 0.95
- **Tae Futaba** (Order: 4, First Girl: 0, Won: 0)
  - _Justification_: Automatically recovered missing major candidate: Tae Futaba.
  - _Hair Color_: Unknown | _Childhood Connection_: None | _Commitment Status_: None | _Confidence Score_: 0.85
- **Kojuurou Shuri** (Order: 5, First Girl: 0, Won: 0)
  - _Justification_: Automatically recovered missing major candidate: Kojuurou Shuri.
  - _Hair Color_: Unknown | _Childhood Connection_: None | _Commitment Status_: None | _Confidence Score_: 0.85

### Yamada-kun and the Seven Witches (ID 19)
- **Urara Shiraishi** (Order: 1, First Girl: 1, Won: 1)
  - _Justification_: She is the primary heroine, the first witch introduced, and the canonical winner who marries Yamada.
  - _Hair Color_: Black | _Childhood Connection_: None | _Commitment Status_: Marriage | _Confidence Score_: 1.0
- **Nene Odagiri** (Order: 2, First Girl: 0, Won: 0)
  - _Justification_: Introduced as a major rival/witch shortly after Shiraishi.
  - _Hair Color_: Black | _Childhood Connection_: None | _Commitment Status_: None | _Confidence Score_: 0.95
- **Miyabi Itou** (Order: 3, First Girl: 0, Won: 0)
  - _Justification_: Joins the club early on as a core member.
  - _Hair Color_: Brown | _Childhood Connection_: None | _Commitment Status_: None | _Confidence Score_: 0.95
- **Noa Takigawa** (Order: 4, First Girl: 0, Won: 0)
  - _Justification_: Introduced during the witch hunt arc.
  - _Hair Color_: Brown | _Childhood Connection_: None | _Commitment Status_: None | _Confidence Score_: 0.95
- **Leona Miyamura** (Order: 5, First Girl: 0, Won: 0)
  - _Justification_: Introduced as a key figure in the witch mystery.
  - _Hair Color_: Black | _Childhood Connection_: None | _Commitment Status_: None | _Confidence Score_: 0.95
- **Maria Sarushima** (Order: 6, First Girl: 0, Won: 0)
  - _Justification_: Introduced as a witch with the power of precognition.
  - _Hair Color_: Brown | _Childhood Connection_: None | _Commitment Status_: None | _Confidence Score_: 0.95
- **Meiko Otsuka** (Order: 7, First Girl: 0, Won: 0)
  - _Justification_: Automatically recovered missing major candidate: Meiko Otsuka.
  - _Hair Color_: Unknown | _Childhood Connection_: None | _Commitment Status_: None | _Confidence Score_: 0.85
- **Mikoto Asuka** (Order: 8, First Girl: 0, Won: 0)
  - _Justification_: Automatically recovered missing major candidate: Mikoto Asuka.
  - _Hair Color_: Unknown | _Childhood Connection_: None | _Commitment Status_: None | _Confidence Score_: 0.85

### Mayo Chiki! (ID 20)
- **Subaru Konoe** (Order: 1, First Girl: 1, Won: 1)
  - _Justification_: Subaru is the primary romantic interest and the first girl introduced in the series. She is the canonical winner in the light novel series.
  - _Hair Color_: Black | _Childhood Connection_: None | _Commitment Status_: None | _Confidence Score_: 1.0
- **Kanade Suzutsuki** (Order: 2, First Girl: 0, Won: 0)
  - _Justification_: Kanade is a major heroine and the primary antagonist/schemer, introduced shortly after Subaru.
  - _Hair Color_: Black | _Childhood Connection_: None | _Commitment Status_: None | _Confidence Score_: 1.0
- **Masamune Usami** (Order: 3, First Girl: 0, Won: 0)
  - _Justification_: Introduced as a rival/heroine later in the series.
  - _Hair Color_: Brown | _Childhood Connection_: None | _Commitment Status_: None | _Confidence Score_: 1.0
- **Nakuru Narumi** (Order: 4, First Girl: 0, Won: 0)
  - _Justification_: Introduced as a heroine later in the series.
  - _Hair Color_: Brown | _Childhood Connection_: None | _Commitment Status_: None | _Confidence Score_: 1.0

### Ai Yori Aoshi (ID 21)
- **Aoi Sakuraba** (Order: 1, First Girl: 1, Won: 1)
  - _Justification_: Aoi is the primary heroine, the childhood promise partner, and the canonical winner.
  - _Hair Color_: Black | _Childhood Connection_: Childhood Promise | _Commitment Status_: Engagement | _Confidence Score_: 1.0
- **Taeko Minazuki** (Order: 2, First Girl: 0, Won: 0)
  - _Justification_: Introduced early as a neighbor and romantic interest.
  - _Hair Color_: Brown | _Childhood Connection_: None | _Commitment Status_: None | _Confidence Score_: 0.95
- **Chika Minazuki** (Order: 3, First Girl: 0, Won: 0)
  - _Justification_: Taeko's younger sister, introduced shortly after.
  - _Hair Color_: Brown | _Childhood Connection_: None | _Commitment Status_: None | _Confidence Score_: 0.95
- **Miyabi Kagurazaki** (Order: 4, First Girl: 0, Won: 0)
  - _Justification_: Introduced as Aoi's attendant and rival.
  - _Hair Color_: Black | _Childhood Connection_: None | _Commitment Status_: None | _Confidence Score_: 0.95
- **Tina Foster** (Order: 5, First Girl: 0, Won: 0)
  - _Justification_: Introduced as a foreign exchange student and romantic rival.
  - _Hair Color_: Blonde | _Childhood Connection_: None | _Commitment Status_: None | _Confidence Score_: 0.95
- **Mayu Miyuki** (Order: 6, First Girl: 0, Won: 0)
  - _Justification_: Introduced later in the series.
  - _Hair Color_: Black | _Childhood Connection_: None | _Commitment Status_: None | _Confidence Score_: 0.95
- **Chizuru Aizawa** (Order: 7, First Girl: 0, Won: 0)
  - _Justification_: Introduced as a maid/caretaker figure.
  - _Hair Color_: Black | _Childhood Connection_: None | _Commitment Status_: None | _Confidence Score_: 0.95

### Ranma ½ (ID 22)
- **Akane Tendou** (Order: 1, First Girl: 1, Won: 1)
  - _Justification_: Akane is the primary heroine, the first to be introduced as a romantic interest, and the canonical winner in the manga.
  - _Hair Color_: Black | _Childhood Connection_: None | _Commitment Status_: Engagement | _Confidence Score_: 1.0
- **Ukyou Kuonji** (Order: 2, First Girl: 0, Won: 0)
  - _Justification_: Introduced as a childhood friend with a promise, does not win.
  - _Hair Color_: Brown | _Childhood Connection_: Childhood Promise | _Commitment Status_: None | _Confidence Score_: 0.95
- **Shampoo** (Order: 3, First Girl: 0, Won: 0)
  - _Justification_: Introduced as a romantic rival/pursuer, does not win.
  - _Hair Color_: Purple | _Childhood Connection_: None | _Commitment Status_: None | _Confidence Score_: 0.95
- **Kodachi Kuno** (Order: 4, First Girl: 0, Won: 0)
  - _Justification_: Automatically recovered missing major candidate: Kodachi Kuno.
  - _Hair Color_: Unknown | _Childhood Connection_: None | _Commitment Status_: None | _Confidence Score_: 0.85

### Hayate the Combat Butler (ID 23)
- **Nagi Sanzenin** (Order: 1, First Girl: 1, Won: 0)
  - _Justification_: Nagi is the first major heroine introduced and the primary focus of the series, though the manga ends without a definitive romantic winner.
  - _Hair Color_: Blonde | _Childhood Connection_: None | _Commitment Status_: None | _Confidence Score_: 1.0
- **Maria** (Order: 2, First Girl: 0, Won: 0)
  - _Justification_: Introduced shortly after Nagi as a primary household figure.
  - _Hair Color_: Brown | _Childhood Connection_: None | _Commitment Status_: None | _Confidence Score_: 1.0
- **Ayumu Nishizawa** (Order: 3, First Girl: 0, Won: 0)
  - _Justification_: One of the earliest classmates to develop a crush on Hayate.
  - _Hair Color_: Black | _Childhood Connection_: None | _Commitment Status_: None | _Confidence Score_: 1.0
- **Hinagiku Katsura** (Order: 4, First Girl: 0, Won: 0)
  - _Justification_: Becomes a major romantic interest after the student council arc.
  - _Hair Color_: Pink | _Childhood Connection_: None | _Commitment Status_: None | _Confidence Score_: 1.0
- **Isumi Saginomiya** (Order: 5, First Girl: 0, Won: 0)
  - _Justification_: Introduced as a recurring character who develops feelings for Hayate.
  - _Hair Color_: Black | _Childhood Connection_: None | _Commitment Status_: None | _Confidence Score_: 1.0
- **Izumi Segawa** (Order: 6, First Girl: 0, Won: 0)
  - _Justification_: A recurring character in the school setting.
  - _Hair Color_: Black | _Childhood Connection_: None | _Commitment Status_: None | _Confidence Score_: 1.0
- **Athena Tennousu** (Order: 7, First Girl: 0, Won: 0)
  - _Justification_: The primary childhood connection character introduced later in the series.
  - _Hair Color_: Blonde | _Childhood Connection_: Childhood Promise | _Commitment Status_: None | _Confidence Score_: 1.0
- **Ruka Suirenji** (Order: 8, First Girl: 0, Won: 0)
  - _Justification_: Introduced in the later stages of the manga.
  - _Hair Color_: Pink | _Childhood Connection_: None | _Commitment Status_: None | _Confidence Score_: 1.0
- **Sakuya Aizawa** (Order: 9, First Girl: 0, Won: 0)
  - _Justification_: Automatically recovered missing major candidate: Sakuya Aizawa.
  - _Hair Color_: Unknown | _Childhood Connection_: None | _Commitment Status_: None | _Confidence Score_: 0.85

### Full Metal Panic! (ID 25)
- **Kaname Chidori** (Order: 1, First Girl: 1, Won: 1)
  - _Justification_: Kaname is the primary heroine and the canonical romantic partner of Sousuke Sagara, culminating in their marriage in the light novel epilogue.
  - _Hair Color_: Blue | _Childhood Connection_: None | _Commitment Status_: Marriage | _Confidence Score_: 1.0
- **Teletha Testarossa** (Order: 2, First Girl: 0, Won: 0)
  - _Justification_: Teletha is a major romantic interest who develops feelings for Sousuke but does not end up with him.
  - _Hair Color_: Silver | _Childhood Connection_: None | _Commitment Status_: None | _Confidence Score_: 1.0

### Midori Days (ID 26)
- **Midori Kasugano** (Order: 1, First Girl: 1, Won: 1)
  - _Justification_: Midori is the titular character and the primary romantic interest who appears in the first chapter. She is the canonical winner as the story focuses on her relationship with Seiji.
  - _Hair Color_: Brown | _Childhood Connection_: None | _Commitment Status_: None | _Confidence Score_: 1.0
- **Takako Ayase** (Order: 2, First Girl: 0, Won: 0)
  - _Justification_: Introduced as a classmate and romantic rival/interest for Seiji, but does not win.
  - _Hair Color_: Black | _Childhood Connection_: None | _Commitment Status_: None | _Confidence Score_: 0.95
- **Nao Makinoha** (Order: 3, First Girl: 0, Won: 0)
  - _Justification_: Seiji's childhood friend who harbors feelings for him, but does not win.
  - _Hair Color_: Brown | _Childhood Connection_: Childhood Friend | _Commitment Status_: None | _Confidence Score_: 0.95
- **Rina** (Order: 4, First Girl: 0, Won: 0)
  - _Justification_: Automatically recovered missing major candidate: Rina.
  - _Hair Color_: Unknown | _Childhood Connection_: None | _Commitment Status_: None | _Confidence Score_: 0.85
- **Lucy Winfield** (Order: 5, First Girl: 0, Won: 0)
  - _Justification_: Automatically recovered missing major candidate: Lucy Winfield.
  - _Hair Color_: Unknown | _Childhood Connection_: None | _Commitment Status_: None | _Confidence Score_: 0.85

### Sankarea (ID 27)
- **Rea Sanka** (Order: 1, First Girl: 1, Won: 1)
  - _Justification_: Rea is the primary heroine and the focus of the romantic narrative throughout the manga.
  - _Hair Color_: Black | _Childhood Connection_: None | _Commitment Status_: None | _Confidence Score_: 1.0
- **Ranko Saouji** (Order: 2, First Girl: 0, Won: 0)
  - _Justification_: Ranko is the childhood friend who harbors feelings for the protagonist but does not win.
  - _Hair Color_: Brown | _Childhood Connection_: Childhood Friend | _Commitment Status_: None | _Confidence Score_: 1.0
- **Darin Arnschent Kurumiya** (Order: 3, First Girl: 0, Won: 0)
  - _Justification_: A secondary character introduced later in the series with limited romantic impact.
  - _Hair Color_: Blonde | _Childhood Connection_: None | _Commitment Status_: None | _Confidence Score_: 0.9

### Campione! (ID 29)
- **Erica Blandelli** (Order: 1, First Girl: 1, Won: 0)
  - _Justification_: Automatically recovered missing major candidate: Erica Blandelli.
  - _Hair Color_: Unknown | _Childhood Connection_: None | _Commitment Status_: None | _Confidence Score_: 0.85
- **Yuri Mariya** (Order: 2, First Girl: 0, Won: 0)
  - _Justification_: Automatically recovered missing major candidate: Yuri Mariya.
  - _Hair Color_: Unknown | _Childhood Connection_: None | _Commitment Status_: None | _Confidence Score_: 0.85
- **Liliana Kranjcar** (Order: 3, First Girl: 0, Won: 0)
  - _Justification_: Automatically recovered missing major candidate: Liliana Kranjcar.
  - _Hair Color_: Unknown | _Childhood Connection_: None | _Commitment Status_: None | _Confidence Score_: 0.85
- **Ena Seishuuin** (Order: 4, First Girl: 0, Won: 0)
  - _Justification_: Automatically recovered missing major candidate: Ena Seishuuin.
  - _Hair Color_: Unknown | _Childhood Connection_: None | _Commitment Status_: None | _Confidence Score_: 0.85

### Date A Live (ID 30)
- **Tooka Yatogami** (Order: 1, First Girl: 1, Won: 0)
  - _Justification_: She is the first spirit encountered and the primary heroine of the series.
  - _Hair Color_: Purple | _Childhood Connection_: None | _Commitment Status_: None | _Confidence Score_: 1.0
- **Origami Tobiichi** (Order: 2, First Girl: 0, Won: 0)
  - _Justification_: She is a classmate and childhood acquaintance of Shido.
  - _Hair Color_: White | _Childhood Connection_: Childhood Friend | _Commitment Status_: None | _Confidence Score_: 0.95
- **Kotori Itsuka** (Order: 3, First Girl: 0, Won: 0)
  - _Justification_: She is Shido's adoptive sister and childhood friend.
  - _Hair Color_: Red | _Childhood Connection_: Childhood Friend | _Commitment Status_: None | _Confidence Score_: 1.0
- **Kurumi Tokisaki** (Order: 4, First Girl: 0, Won: 0)
  - _Justification_: Introduced as a transfer student and major romantic interest.
  - _Hair Color_: Black | _Childhood Connection_: None | _Commitment Status_: None | _Confidence Score_: 0.95
- **Yoshino Himekawa** (Order: 5, First Girl: 0, Won: 0)
  - _Justification_: Introduced as the second spirit.
  - _Hair Color_: Blue | _Childhood Connection_: None | _Commitment Status_: None | _Confidence Score_: 0.95
- **Reine Murasame** (Order: 6, First Girl: 0, Won: 0)
  - _Justification_: Introduced as an analyst for Ratatoskr.
  - _Hair Color_: Blue | _Childhood Connection_: None | _Commitment Status_: None | _Confidence Score_: 0.9
- **Kaguya Yamai** (Order: 7, First Girl: 0, Won: 0)
  - _Justification_: Automatically recovered missing major candidate: Kaguya Yamai.
  - _Hair Color_: Unknown | _Childhood Connection_: None | _Commitment Status_: None | _Confidence Score_: 0.85
- **Yuzuru Yamai** (Order: 8, First Girl: 0, Won: 0)
  - _Justification_: Automatically recovered missing major candidate: Yuzuru Yamai.
  - _Hair Color_: Unknown | _Childhood Connection_: None | _Commitment Status_: None | _Confidence Score_: 0.85
- **Miku Izayoi** (Order: 9, First Girl: 0, Won: 0)
  - _Justification_: Automatically recovered missing major candidate: Miku Izayoi.
  - _Hair Color_: Unknown | _Childhood Connection_: None | _Commitment Status_: None | _Confidence Score_: 0.85
- **Natsumi** (Order: 10, First Girl: 0, Won: 0)
  - _Justification_: Automatically recovered missing major candidate: Natsumi.
  - _Hair Color_: Unknown | _Childhood Connection_: None | _Commitment Status_: None | _Confidence Score_: 0.85

### Strike the Blood (ID 31)
- **Yukina Himeragi** (Order: 1, First Girl: 1, Won: 1)
  - _Justification_: Automatically recovered missing major candidate: Yukina Himeragi.
  - _Hair Color_: Unknown | _Childhood Connection_: None | _Commitment Status_: None | _Confidence Score_: 0.85
- **Asagi Aiba** (Order: 2, First Girl: 0, Won: 0)
  - _Justification_: Automatically recovered missing major candidate: Asagi Aiba.
  - _Hair Color_: Unknown | _Childhood Connection_: None | _Commitment Status_: None | _Confidence Score_: 0.85
- **Sayaka Kirasaka** (Order: 3, First Girl: 0, Won: 0)
  - _Justification_: Automatically recovered missing major candidate: Sayaka Kirasaka.
  - _Hair Color_: Unknown | _Childhood Connection_: None | _Commitment Status_: None | _Confidence Score_: 0.85

### Seirei Tsukai no Blade Dance (ID 32)
- **Claire Rouge** (Order: 1, First Girl: 1, Won: 0)
  - _Justification_: Claire is the first major heroine introduced and the primary romantic interest throughout the series.
  - _Hair Color_: Red | _Childhood Connection_: None | _Commitment Status_: None | _Confidence Score_: 0.95
- **Restia Ashdoll** (Order: 2, First Girl: 0, Won: 0)
  - _Justification_: Restia is the childhood friend and a central figure in the protagonist's past.
  - _Hair Color_: Black | _Childhood Connection_: Childhood Friend | _Commitment Status_: None | _Confidence Score_: 0.9
- **Rinslet Laurenfrost** (Order: 3, First Girl: 0, Won: 0)
  - _Justification_: Introduced early as a rival and romantic interest.
  - _Hair Color_: Blue | _Childhood Connection_: None | _Commitment Status_: None | _Confidence Score_: 0.9
- **Ellis Fahrengart** (Order: 4, First Girl: 0, Won: 0)
  - _Justification_: Introduced as a member of the team and romantic interest.
  - _Hair Color_: Blue | _Childhood Connection_: None | _Commitment Status_: None | _Confidence Score_: 0.9
- **Fianna Ray Ordesia** (Order: 5, First Girl: 0, Won: 0)
  - _Justification_: Introduced as a princess and romantic interest.
  - _Hair Color_: Blonde | _Childhood Connection_: None | _Commitment Status_: None | _Confidence Score_: 0.9
- **Terminus Est** (Order: 6, First Girl: 0, Won: 0)
  - _Justification_: A spirit partner who develops romantic feelings for the protagonist.
  - _Hair Color_: Silver | _Childhood Connection_: None | _Commitment Status_: None | _Confidence Score_: 0.9

### Omamori Himari (ID 33)
- **Himari Noihara** (Order: 1, First Girl: 1, Won: 1)
  - _Justification_: Himari is the titular character, the first to appear as a romantic interest, and marries the protagonist in the manga ending.
  - _Hair Color_: Black | _Childhood Connection_: Childhood Promise | _Commitment Status_: Marriage | _Confidence Score_: 1.0
- **Kuesu Jinguuji** (Order: 2, First Girl: 0, Won: 0)
  - _Justification_: Childhood friend and fiancee who appears early in the narrative.
  - _Hair Color_: Blonde | _Childhood Connection_: Childhood Friend | _Commitment Status_: Engagement | _Confidence Score_: 0.95
- **Shizuku** (Order: 3, First Girl: 0, Won: 0)
  - _Justification_: Introduced as an antagonist/rival before becoming a romantic interest.
  - _Hair Color_: Blue | _Childhood Connection_: None | _Commitment Status_: None | _Confidence Score_: 0.95
- **Lizlet L Chelsie** (Order: 4, First Girl: 0, Won: 0)
  - _Justification_: Introduced later in the manga series.
  - _Hair Color_: Silver | _Childhood Connection_: None | _Commitment Status_: None | _Confidence Score_: 0.95
- **Rinko Kuzaki** (Order: 5, First Girl: 0, Won: 0)
  - _Justification_: Childhood friend who is a romantic interest but does not win.
  - _Hair Color_: Brown | _Childhood Connection_: Childhood Friend | _Commitment Status_: None | _Confidence Score_: 0.95
- **Ageha** (Order: 6, First Girl: 0, Won: 0)
  - _Justification_: Automatically recovered missing major candidate: Ageha.
  - _Hair Color_: Unknown | _Childhood Connection_: None | _Commitment Status_: None | _Confidence Score_: 0.85

### Hundred (ID 35)
- **Emile Crossfode** (Order: 1, First Girl: 1, Won: 0)
  - _Justification_: Emile is the first heroine introduced and shares a childhood promise with the protagonist, Hayato Kisaragi.
  - _Hair Color_: Silver | _Childhood Connection_: Childhood Promise | _Commitment Status_: None | _Confidence Score_: 0.95
- **Claire Harvey** (Order: 2, First Girl: 0, Won: 0)
  - _Justification_: Claire is introduced shortly after Emile as the student council president.
  - _Hair Color_: Blonde | _Childhood Connection_: None | _Commitment Status_: None | _Confidence Score_: 0.9
- **Sakura Kirishima** (Order: 3, First Girl: 0, Won: 0)
  - _Justification_: Automatically recovered missing major candidate: Sakura Kirishima.
  - _Hair Color_: Unknown | _Childhood Connection_: None | _Commitment Status_: None | _Confidence Score_: 0.85
- **Karen Kisaragi** (Order: 4, First Girl: 0, Won: 0)
  - _Justification_: Automatically recovered missing major candidate: Karen Kisaragi.
  - _Hair Color_: Unknown | _Childhood Connection_: None | _Commitment Status_: None | _Confidence Score_: 0.85
- **Liddy Steinberg** (Order: 5, First Girl: 0, Won: 0)
  - _Justification_: Automatically recovered missing major candidate: Liddy Steinberg.
  - _Hair Color_: Unknown | _Childhood Connection_: None | _Commitment Status_: None | _Confidence Score_: 0.85

### Absolute Duo (ID 36)
- **Julie Sigtuna** (Order: 1, First Girl: 1, Won: 0)
  - _Justification_: Julie is the first heroine introduced and the primary partner of the protagonist, though the series remains an open harem.
  - _Hair Color_: Silver | _Childhood Connection_: None | _Commitment Status_: None | _Confidence Score_: 1.0
- **Lilith Bristol** (Order: 2, First Girl: 0, Won: 0)
  - _Justification_: Introduced shortly after Julie as a major romantic interest.
  - _Hair Color_: Blonde | _Childhood Connection_: None | _Commitment Status_: None | _Confidence Score_: 1.0
- **Miyabi Hotaka** (Order: 3, First Girl: 0, Won: 0)
  - _Justification_: Introduced as a classmate and romantic interest.
  - _Hair Color_: Black | _Childhood Connection_: None | _Commitment Status_: None | _Confidence Score_: 1.0
- **Tomoe Tachibana** (Order: 4, First Girl: 0, Won: 0)
  - _Justification_: Introduced as a classmate and romantic interest.
  - _Hair Color_: Black | _Childhood Connection_: None | _Commitment Status_: None | _Confidence Score_: 1.0
- **Rito Tsukimi** (Order: 5, First Girl: 0, Won: 0)
  - _Justification_: Automatically recovered missing major candidate: Rito Tsukimi.
  - _Hair Color_: Unknown | _Childhood Connection_: None | _Commitment Status_: None | _Confidence Score_: 0.85

### Koi to Senkyo to Chocolate (ID 37)
- **Chisato Sumiyoshi** (Order: 1, First Girl: 1, Won: 0)
  - _Justification_: The protagonist's childhood friend and the first heroine to be established as a romantic interest.
  - _Hair Color_: Brown | _Childhood Connection_: Childhood Friend | _Commitment Status_: None | _Confidence Score_: 0.95
- **Satsuki Shinonome** (Order: 2, First Girl: 0, Won: 0)
  - _Justification_: Student council president and major heroine, introduced shortly after the protagonist joins the club.
  - _Hair Color_: Brown | _Childhood Connection_: None | _Commitment Status_: None | _Confidence Score_: 0.95
- **Isara Aomi** (Order: 3, First Girl: 0, Won: 0)
  - _Justification_: A member of the food research club, introduced early as a core heroine.
  - _Hair Color_: Black | _Childhood Connection_: None | _Commitment Status_: None | _Confidence Score_: 0.95
- **Michiru Morishita** (Order: 4, First Girl: 0, Won: 0)
  - _Justification_: Introduced as a mysterious student who joins the club later in the narrative.
  - _Hair Color_: Blue | _Childhood Connection_: None | _Commitment Status_: None | _Confidence Score_: 0.95
- **Mifuyu Kiba** (Order: 5, First Girl: 0, Won: 0)
  - _Justification_: A senior member of the club, introduced as a key heroine.
  - _Hair Color_: Black | _Childhood Connection_: None | _Commitment Status_: None | _Confidence Score_: 0.95
- **Oba Michiru** (Order: 6, First Girl: 0, Won: 0)
  - _Justification_: Automatically recovered missing major candidate: Oba Michiru.
  - _Hair Color_: Unknown | _Childhood Connection_: None | _Commitment Status_: None | _Confidence Score_: 0.85

### Rakudai Kishi no Cavalry (ID 38)
- **Stella Vermillion** (Order: 1, First Girl: 1, Won: 1)
  - _Justification_: Stella is the primary heroine and the protagonist's fiancee, established early in the light novel.
  - _Hair Color_: Red | _Childhood Connection_: None | _Commitment Status_: Engagement | _Confidence Score_: 1.0
- **Shizuku Kurogane** (Order: 2, First Girl: 0, Won: 0)
  - _Justification_: Automatically recovered missing major candidate: Shizuku Kurogane.
  - _Hair Color_: Unknown | _Childhood Connection_: None | _Commitment Status_: None | _Confidence Score_: 0.85
- **Ayase Ayatsuji** (Order: 3, First Girl: 0, Won: 0)
  - _Justification_: Automatically recovered missing major candidate: Ayase Ayatsuji.
  - _Hair Color_: Unknown | _Childhood Connection_: None | _Commitment Status_: None | _Confidence Score_: 0.85
- **Nene Saikyo** (Order: 4, First Girl: 0, Won: 0)
  - _Justification_: Automatically recovered missing major candidate: Nene Saikyo.
  - _Hair Color_: Unknown | _Childhood Connection_: None | _Commitment Status_: None | _Confidence Score_: 0.85

### Shakugan no Shana (ID 39)
- **Shana** (Order: 1, First Girl: 1, Won: 1)
  - _Justification_: Shana is the primary heroine and the canonical romantic partner of Yuji Sakai in the light novel series.
  - _Hair Color_: Black | _Childhood Connection_: None | _Commitment Status_: None | _Confidence Score_: 1.0
- **Kazumi Yoshida** (Order: 2, First Girl: 0, Won: 0)
  - _Justification_: Kazumi is a major romantic rival introduced shortly after the start of the series, but she does not win.
  - _Hair Color_: Brown | _Childhood Connection_: None | _Commitment Status_: None | _Confidence Score_: 1.0

### Zero no Tsukaima (ID 40)
- **Louise Françoise Le Blanc de La Vallière** (Order: 1, First Girl: 1, Won: 1)
  - _Justification_: The primary protagonist and canonical wife of Saito Hiraga.
  - _Hair Color_: Pink | _Childhood Connection_: None | _Commitment Status_: Marriage | _Confidence Score_: 1.0
- **Siesta** (Order: 2, First Girl: 0, Won: 0)
  - _Justification_: Introduced shortly after Louise as a maid and romantic rival.
  - _Hair Color_: Black | _Childhood Connection_: None | _Commitment Status_: None | _Confidence Score_: 1.0
- **Henrietta de Tristain** (Order: 3, First Girl: 0, Won: 0)
  - _Justification_: The Queen of Tristain, introduced early as a romantic interest.
  - _Hair Color_: Blonde | _Childhood Connection_: None | _Commitment Status_: None | _Confidence Score_: 1.0
- **Charlotte Hélène d'Orléans** (Order: 4, First Girl: 0, Won: 0)
  - _Justification_: Introduced later in the series as a romantic interest.
  - _Hair Color_: Blonde | _Childhood Connection_: None | _Commitment Status_: None | _Confidence Score_: 0.95
- **Kirche Augusta Frederica von Anhalt-Zerbst** (Order: 5, First Girl: 0, Won: 0)
  - _Justification_: Classmate introduced as a romantic rival.
  - _Hair Color_: Red | _Childhood Connection_: None | _Commitment Status_: None | _Confidence Score_: 1.0
- **Tabitha** (Order: 6, First Girl: 0, Won: 0)
  - _Justification_: Automatically recovered missing major candidate: Tabitha.
  - _Hair Color_: Unknown | _Childhood Connection_: None | _Commitment Status_: None | _Confidence Score_: 0.85
- **Montmorency Margarita la Fère de Montmorency** (Order: 7, First Girl: 0, Won: 0)
  - _Justification_: Automatically recovered missing major candidate: Montmorency Margarita la Fère de Montmorency.
  - _Hair Color_: Unknown | _Childhood Connection_: None | _Commitment Status_: None | _Confidence Score_: 0.85

### Rascal Does Not Dream of Bunny Girl Senpai (ID 41)
- **Mai Sakurajima** (Order: 1, First Girl: 1, Won: 1)
  - _Justification_: Mai is the primary heroine and the canonical romantic partner of Sakuta Azusagawa throughout the series.
  - _Hair Color_: Black | _Childhood Connection_: None | _Commitment Status_: None | _Confidence Score_: 1.0
- **Tomoe Koga** (Order: 2, First Girl: 0, Won: 0)
  - _Justification_: Tomoe is a major heroine introduced in the second volume of the light novel series.
  - _Hair Color_: Brown | _Childhood Connection_: None | _Commitment Status_: None | _Confidence Score_: 0.95
- **Rio Futaba** (Order: 3, First Girl: 0, Won: 0)
  - _Justification_: Automatically recovered missing major candidate: Rio Futaba.
  - _Hair Color_: Unknown | _Childhood Connection_: None | _Commitment Status_: None | _Confidence Score_: 0.85
- **Kaede Azusagawa** (Order: 4, First Girl: 0, Won: 0)
  - _Justification_: Automatically recovered missing major candidate: Kaede Azusagawa.
  - _Hair Color_: Unknown | _Childhood Connection_: None | _Commitment Status_: None | _Confidence Score_: 0.85
- **Nodoka Toyohama** (Order: 5, First Girl: 0, Won: 0)
  - _Justification_: Automatically recovered missing major candidate: Nodoka Toyohama.
  - _Hair Color_: Unknown | _Childhood Connection_: None | _Commitment Status_: None | _Confidence Score_: 0.85
- **Shoko Makinohara** (Order: 6, First Girl: 0, Won: 0)
  - _Justification_: Automatically recovered missing major candidate: Shoko Makinohara.
  - _Hair Color_: Unknown | _Childhood Connection_: None | _Commitment Status_: None | _Confidence Score_: 0.85

### Re:Zero − Starting Life in Another World (ID 42)
- **Emilia** (Order: 1, First Girl: 1, Won: 0)
  - _Justification_: Emilia is the primary heroine and the first major romantic interest introduced in the series. The story is ongoing and features a harem dynamic, so no winner is declared.
  - _Hair Color_: Silver | _Childhood Connection_: None | _Commitment Status_: None | _Confidence Score_: 1.0
- **Rem** (Order: 2, First Girl: 0, Won: 0)
  - _Justification_: Automatically recovered missing major candidate: Rem.
  - _Hair Color_: Unknown | _Childhood Connection_: None | _Commitment Status_: None | _Confidence Score_: 0.85
- **Ram** (Order: 3, First Girl: 0, Won: 0)
  - _Justification_: Automatically recovered missing major candidate: Ram.
  - _Hair Color_: Unknown | _Childhood Connection_: None | _Commitment Status_: None | _Confidence Score_: 0.85

### Monogatari Series (ID 43)
- **Hitagi Senjougahara** (Order: 1, First Girl: 1, Won: 1)
  - _Justification_: She is the primary romantic interest and canonical partner of the protagonist, Koyomi Araragi, throughout the series.
  - _Hair Color_: Purple | _Childhood Connection_: None | _Commitment Status_: Marriage | _Confidence Score_: 1.0
- **Tsubasa Hanekawa** (Order: 2, First Girl: 0, Won: 0)
  - _Justification_: Introduced early as a close friend and love interest, but does not end up with the protagonist.
  - _Hair Color_: Black | _Childhood Connection_: None | _Commitment Status_: None | _Confidence Score_: 0.95
- **Suruga Kanbaru** (Order: 3, First Girl: 0, Won: 0)
  - _Justification_: A major character who develops feelings for the protagonist but remains a friend.
  - _Hair Color_: Black | _Childhood Connection_: None | _Commitment Status_: None | _Confidence Score_: 0.95
- **Nadeko Sengoku** (Order: 4, First Girl: 0, Won: 0)
  - _Justification_: A major character with a crush on the protagonist, but never enters a romantic relationship with him.
  - _Hair Color_: Brown | _Childhood Connection_: None | _Commitment Status_: None | _Confidence Score_: 0.95
- **Shinobu Oshino** (Order: 5, First Girl: 0, Won: 0)
  - _Justification_: Automatically recovered missing major candidate: Shinobu Oshino.
  - _Hair Color_: Unknown | _Childhood Connection_: None | _Commitment Status_: None | _Confidence Score_: 0.85
- **Mayoi Hachikuji** (Order: 6, First Girl: 0, Won: 0)
  - _Justification_: Automatically recovered missing major candidate: Mayoi Hachikuji.
  - _Hair Color_: Unknown | _Childhood Connection_: None | _Commitment Status_: None | _Confidence Score_: 0.85
- **Karen Araragi** (Order: 7, First Girl: 0, Won: 0)
  - _Justification_: Automatically recovered missing major candidate: Karen Araragi.
  - _Hair Color_: Unknown | _Childhood Connection_: None | _Commitment Status_: None | _Confidence Score_: 0.85
- **Tsukihi Araragi** (Order: 8, First Girl: 0, Won: 0)
  - _Justification_: Automatically recovered missing major candidate: Tsukihi Araragi.
  - _Hair Color_: Unknown | _Childhood Connection_: None | _Commitment Status_: None | _Confidence Score_: 0.85
- **Sodachi Oikura** (Order: 9, First Girl: 0, Won: 0)
  - _Justification_: Automatically recovered missing major candidate: Sodachi Oikura.
  - _Hair Color_: Unknown | _Childhood Connection_: None | _Commitment Status_: None | _Confidence Score_: 0.85

### Haganai (Boku wa Tomodachi ga Sukunai) (ID 44)
- **Yozora Mikazuki** (Order: 1, First Girl: 1, Won: 0)
  - _Justification_: The primary heroine and childhood friend of the protagonist, introduced first.
  - _Hair Color_: Black | _Childhood Connection_: Childhood Friend | _Commitment Status_: None | _Confidence Score_: 0.95
- **Sena Kashiwazaki** (Order: 2, First Girl: 0, Won: 0)
  - _Justification_: Introduced shortly after Yozora as a major romantic interest in the Neighbors Club.
  - _Hair Color_: Blonde | _Childhood Connection_: None | _Commitment Status_: None | _Confidence Score_: 0.95
- **Rika Shiguma** (Order: 3, First Girl: 0, Won: 0)
  - _Justification_: Joins the club later as a romantic interest.
  - _Hair Color_: Purple | _Childhood Connection_: None | _Commitment Status_: None | _Confidence Score_: 0.9
- **Yukimura Kusunoki** (Order: 4, First Girl: 0, Won: 0)
  - _Justification_: Joins the club later as a romantic interest.
  - _Hair Color_: Black | _Childhood Connection_: None | _Commitment Status_: None | _Confidence Score_: 0.9
- **Kobato Hasegawa** (Order: 5, First Girl: 0, Won: 0)
  - _Justification_: Automatically recovered missing major candidate: Kobato Hasegawa.
  - _Hair Color_: Unknown | _Childhood Connection_: None | _Commitment Status_: None | _Confidence Score_: 0.85
- **Maria Takayama** (Order: 6, First Girl: 0, Won: 0)
  - _Justification_: Automatically recovered missing major candidate: Maria Takayama.
  - _Hair Color_: Unknown | _Childhood Connection_: None | _Commitment Status_: None | _Confidence Score_: 0.85

### Oreshura (Ore no Kanojo to Osananajimi ga Sh修羅場 Sugiru) (ID 45)
- **Masuzu Natsukawa** (Order: 1, First Girl: 1, Won: 0)
  - _Justification_: Masuzu is the first heroine introduced and initiates the fake relationship that drives the plot.
  - _Hair Color_: Silver | _Childhood Connection_: None | _Commitment Status_: Engagement | _Confidence Score_: 1.0
- **Chiwa Harusaki** (Order: 2, First Girl: 0, Won: 0)
  - _Justification_: Chiwa is the childhood friend who re-enters the protagonist's life as a romantic interest early in the series.
  - _Hair Color_: Red | _Childhood Connection_: Childhood Friend | _Commitment Status_: None | _Confidence Score_: 1.0
- **Ai Fuyuumi** (Order: 3, First Girl: 0, Won: 0)
  - _Justification_: Ai is introduced later as a transfer student with a childhood promise connection.
  - _Hair Color_: Blue | _Childhood Connection_: Childhood Promise | _Commitment Status_: None | _Confidence Score_: 1.0
- **Himeka Akishino** (Order: 4, First Girl: 0, Won: 0)
  - _Justification_: Himeka is introduced as a romantic interest after the initial trio.
  - _Hair Color_: Brown | _Childhood Connection_: None | _Commitment Status_: None | _Confidence Score_: 1.0

### Trinity Seven (ID 46)
- **Lieselotte Sherlock** (Order: 4, First Girl: 0, Won: 0)
  - _Justification_: Lieselotte is a major heroine in the Trinity Seven series, introduced later in the story as a member of the Trinity Seven.
  - _Hair Color_: Silver | _Childhood Connection_: None | _Commitment Status_: None | _Confidence Score_: 0.95
- **Lilith Asami** (Order: 5, First Girl: 1, Won: 0)
  - _Justification_: Automatically recovered missing major candidate: Lilith Asami.
  - _Hair Color_: Unknown | _Childhood Connection_: None | _Commitment Status_: None | _Confidence Score_: 0.85
- **Arata Kasuga** (Order: 6, First Girl: 0, Won: 0)
  - _Justification_: Automatically recovered missing major candidate: Arata Kasuga.
  - _Hair Color_: Unknown | _Childhood Connection_: None | _Commitment Status_: None | _Confidence Score_: 0.85
- **Arin Kannazuki** (Order: 7, First Girl: 0, Won: 0)
  - _Justification_: Automatically recovered missing major candidate: Arin Kannazuki.
  - _Hair Color_: Unknown | _Childhood Connection_: None | _Commitment Status_: None | _Confidence Score_: 0.85
- **Levi Kazama** (Order: 8, First Girl: 0, Won: 0)
  - _Justification_: Automatically recovered missing major candidate: Levi Kazama.
  - _Hair Color_: Unknown | _Childhood Connection_: None | _Commitment Status_: None | _Confidence Score_: 0.85
- **Mira Yamana** (Order: 9, First Girl: 0, Won: 0)
  - _Justification_: Automatically recovered missing major candidate: Mira Yamana.
  - _Hair Color_: Unknown | _Childhood Connection_: None | _Commitment Status_: None | _Confidence Score_: 0.85
- **Akio Fudo** (Order: 10, First Girl: 0, Won: 0)
  - _Justification_: Automatically recovered missing major candidate: Akio Fudo.
  - _Hair Color_: Unknown | _Childhood Connection_: None | _Commitment Status_: None | _Confidence Score_: 0.85
- **Yui Kurata** (Order: 11, First Girl: 0, Won: 0)
  - _Justification_: Automatically recovered missing major candidate: Yui Kurata.
  - _Hair Color_: Unknown | _Childhood Connection_: None | _Commitment Status_: None | _Confidence Score_: 0.85

### Infinite Stratos (ID 47)
- **Houki Shinonono** (Order: 1, First Girl: 1, Won: 0)
  - _Justification_: Houki is the childhood friend and the first heroine introduced in the series.
  - _Hair Color_: Black | _Childhood Connection_: Childhood Friend | _Commitment Status_: None | _Confidence Score_: 1.0
- **Lingyin Huang** (Order: 2, First Girl: 0, Won: 0)
  - _Justification_: Introduced as the second childhood friend.
  - _Hair Color_: Brown | _Childhood Connection_: Childhood Friend | _Commitment Status_: None | _Confidence Score_: 1.0
- **Cecilia Alcott** (Order: 3, First Girl: 0, Won: 0)
  - _Justification_: Introduced as the British representative.
  - _Hair Color_: Blonde | _Childhood Connection_: None | _Commitment Status_: None | _Confidence Score_: 1.0
- **Charlotte Dunois** (Order: 4, First Girl: 0, Won: 0)
  - _Justification_: Introduced as the French representative.
  - _Hair Color_: Blonde | _Childhood Connection_: None | _Commitment Status_: None | _Confidence Score_: 1.0
- **Laura Bodewig** (Order: 5, First Girl: 0, Won: 0)
  - _Justification_: Introduced as the German representative.
  - _Hair Color_: Silver | _Childhood Connection_: None | _Commitment Status_: None | _Confidence Score_: 1.0
- **Tatenashi Sarashiki** (Order: 6, First Girl: 0, Won: 0)
  - _Justification_: Automatically recovered missing major candidate: Tatenashi Sarashiki.
  - _Hair Color_: Unknown | _Childhood Connection_: None | _Commitment Status_: None | _Confidence Score_: 0.85
- **Kanzashi Sarashiki** (Order: 7, First Girl: 0, Won: 0)
  - _Justification_: Automatically recovered missing major candidate: Kanzashi Sarashiki.
  - _Hair Color_: Unknown | _Childhood Connection_: None | _Commitment Status_: None | _Confidence Score_: 0.85

### A Couple of Cuckoos (ID 48)
- **Erika Amano** (Order: 1, First Girl: 1, Won: 0)
  - _Justification_: Erika is the first heroine introduced and is engaged to the protagonist due to the baby swap.
  - _Hair Color_: Blonde | _Childhood Connection_: None | _Commitment Status_: Engagement | _Confidence Score_: 1.0
- **Hiro Segawa** (Order: 2, First Girl: 0, Won: 0)
  - _Justification_: Introduced as the protagonist's academic rival and crush.
  - _Hair Color_: Black | _Childhood Connection_: None | _Commitment Status_: None | _Confidence Score_: 0.95
- **Sachi Umino** (Order: 3, First Girl: 0, Won: 0)
  - _Justification_: Introduced as the protagonist's younger sister figure.
  - _Hair Color_: Black | _Childhood Connection_: None | _Commitment Status_: None | _Confidence Score_: 0.95
- **Ai Mochizuki** (Order: 4, First Girl: 0, Won: 0)
  - _Justification_: Introduced later as a musician and romantic interest.
  - _Hair Color_: Brown | _Childhood Connection_: None | _Commitment Status_: None | _Confidence Score_: 0.9

### The Café Terrace and Its Goddesses (ID 49)
- **Shiragiku Ono** (Order: 1, First Girl: 1, Won: 0)
  - _Justification_: Shiragiku is the first heroine introduced in the manga and has a confirmed childhood connection.
  - _Hair Color_: Brown | _Childhood Connection_: Childhood Friend | _Commitment Status_: None | _Confidence Score_: 1.0
- **Akane Hououji** (Order: 2, First Girl: 0, Won: 0)
  - _Justification_: Introduced as part of the main group at the cafe.
  - _Hair Color_: Red | _Childhood Connection_: None | _Commitment Status_: None | _Confidence Score_: 1.0
- **Ouka Makuzawa** (Order: 3, First Girl: 0, Won: 0)
  - _Justification_: Introduced as part of the main group at the cafe.
  - _Hair Color_: Black | _Childhood Connection_: None | _Commitment Status_: None | _Confidence Score_: 1.0
- **Riho Tsukishima** (Order: 4, First Girl: 0, Won: 0)
  - _Justification_: Introduced as part of the main group at the cafe.
  - _Hair Color_: Brown | _Childhood Connection_: None | _Commitment Status_: None | _Confidence Score_: 1.0
- **Ami Tsuruga** (Order: 5, First Girl: 0, Won: 0)
  - _Justification_: Introduced as part of the main group at the cafe.
  - _Hair Color_: Black | _Childhood Connection_: None | _Commitment Status_: None | _Confidence Score_: 1.0

### Amagami-san Chi no Enmusubi (ID 50)
- **Yuna Amagami** (Order: 1, First Girl: 1, Won: 0)
  - _Justification_: Yuna is the eldest sister and the first of the three sisters to be introduced as a primary romantic interest in the manga.
  - _Hair Color_: Black | _Childhood Connection_: None | _Commitment Status_: None | _Confidence Score_: 1.0
- **Asahi Amagami** (Order: 2, First Girl: 0, Won: 0)
  - _Justification_: Asahi is the middle sister and is introduced as a romantic interest shortly after Yuna.
  - _Hair Color_: Brown | _Childhood Connection_: None | _Commitment Status_: None | _Confidence Score_: 1.0
- **Yae Amagami** (Order: 3, First Girl: 0, Won: 0)
  - _Justification_: Yae is the youngest sister and is introduced as a romantic interest after Yuna and Asahi.
  - _Hair Color_: Black | _Childhood Connection_: None | _Commitment Status_: None | _Confidence Score_: 1.0

### GE: Good Ending (ID 51)
- **Tsukasa Izumi** (Order: 1, First Girl: 1, Won: 1)
  - _Justification_: Tsukasa is the primary heroine and the canonical winner who marries the protagonist.
  - _Hair Color_: Brown | _Childhood Connection_: None | _Commitment Status_: Marriage | _Confidence Score_: 1.0
- **Yuki Kurokawa** (Order: 2, First Girl: 0, Won: 0)
  - _Justification_: Yuki is a significant romantic interest introduced later in the series.
  - _Hair Color_: Black | _Childhood Connection_: None | _Commitment Status_: None | _Confidence Score_: 0.95
- **Sho Iketani** (Order: 3, First Girl: 0, Won: 0)
  - _Justification_: Automatically recovered missing major candidate: Sho Iketani.
  - _Hair Color_: Unknown | _Childhood Connection_: None | _Commitment Status_: None | _Confidence Score_: 0.85
- **Misa Kawakami** (Order: 4, First Girl: 0, Won: 0)
  - _Justification_: Automatically recovered missing major candidate: Misa Kawakami.
  - _Hair Color_: Unknown | _Childhood Connection_: None | _Commitment Status_: None | _Confidence Score_: 0.85

### Bokura wa Minna Kawaisou (ID 52)
- **Ritsu Kawai** (Order: 1, First Girl: 1, Won: 1)
  - _Justification_: Ritsu is the primary romantic interest and the first girl introduced in the series. The manga concludes with them officially becoming a couple.
  - _Hair Color_: Black | _Childhood Connection_: None | _Commitment Status_: None | _Confidence Score_: 1.0
- **Sayaka Watanabe** (Order: 2, First Girl: 0, Won: 0)
  - _Justification_: Automatically recovered missing major candidate: Sayaka Watanabe.
  - _Hair Color_: Unknown | _Childhood Connection_: None | _Commitment Status_: None | _Confidence Score_: 0.85
- **Mayumi Nishikino** (Order: 3, First Girl: 0, Won: 0)
  - _Justification_: Automatically recovered missing major candidate: Mayumi Nishikino.
  - _Hair Color_: Unknown | _Childhood Connection_: None | _Commitment Status_: None | _Confidence Score_: 0.85

### The Pet Girl of Sakurasou (ID 53)
- **Mashiro Shiina** (Order: 1, First Girl: 1, Won: 1)
  - _Justification_: Mashiro is the primary heroine and the eventual romantic partner of Sorata Kanda in the light novel series.
  - _Hair Color_: Blonde | _Childhood Connection_: None | _Commitment Status_: None | _Confidence Score_: 1.0
- **Nanami Aoyama** (Order: 2, First Girl: 0, Won: 0)
  - _Justification_: Nanami is a major romantic interest who competes for Sorata's affection but does not win.
  - _Hair Color_: Brown | _Childhood Connection_: None | _Commitment Status_: None | _Confidence Score_: 1.0
- **Misaki Kamiigusa** (Order: 3, First Girl: 0, Won: 0)
  - _Justification_: Automatically recovered missing major candidate: Misaki Kamiigusa.
  - _Hair Color_: Unknown | _Childhood Connection_: None | _Commitment Status_: None | _Confidence Score_: 0.85
- **Rita Ainsworth** (Order: 4, First Girl: 0, Won: 0)
  - _Justification_: Automatically recovered missing major candidate: Rita Ainsworth.
  - _Hair Color_: Unknown | _Childhood Connection_: None | _Commitment Status_: None | _Confidence Score_: 0.85

### Hentai Prince and Stony Cat (ID 54)
- **Tsukiko Tsutsukakushi** (Order: 1, First Girl: 1, Won: 0)
  - _Justification_: Tsukiko is the primary heroine and the first to be introduced as a romantic interest. While the series ends with a strong focus on her, it remains an open-ended harem conclusion in the light novel.
  - _Hair Color_: Black | _Childhood Connection_: None | _Commitment Status_: None | _Confidence Score_: 0.95
- **Azusa Azuki** (Order: 2, First Girl: 0, Won: 0)
  - _Justification_: Introduced after Tsukiko as a major romantic interest. The series does not have a single canonical winner.
  - _Hair Color_: Brown | _Childhood Connection_: None | _Commitment Status_: None | _Confidence Score_: 0.95

### Gosick (ID 55)
- **Victorique de Blois** (Order: 1, First Girl: 1, Won: 1)
  - _Justification_: Victorique is the primary protagonist and romantic partner of Kazuya Kujo, eventually marrying him. She is the first major heroine introduced.
  - _Hair Color_: Blonde | _Childhood Connection_: None | _Commitment Status_: Marriage | _Confidence Score_: 1.0
- **Avril Bradley** (Order: 2, First Girl: 0, Won: 0)
  - _Justification_: Avril is a secondary character who develops a crush on Kazuya but is not the romantic winner.
  - _Hair Color_: Blonde | _Childhood Connection_: None | _Commitment Status_: None | _Confidence Score_: 0.95

### Inu x Boku SS (ID 56)
- **Soushi Miketsukami** (Order: 1, First Girl: 1, Won: 1)
  - _Justification_: He is Ririchiyo's devoted Secret Service agent and main love interest who eventually marries her.
  - _Hair Color_: Silver | _Childhood Connection_: Childhood Friend | _Commitment Status_: Marriage | _Confidence Score_: 1.0

### Clannad (ID 57)
- **Nagisa Furukawa** (Order: 1, First Girl: 1, Won: 1)
  - _Justification_: Nagisa is the primary heroine and the only one with a true route that leads to the After Story, resulting in marriage.
  - _Hair Color_: Brown | _Childhood Connection_: None | _Commitment Status_: Marriage | _Confidence Score_: 1.0
- **Tomoyo Sakagami** (Order: 2, First Girl: 0, Won: 0)
  - _Justification_: Introduced as a transfer student and potential romantic interest.
  - _Hair Color_: Silver | _Childhood Connection_: None | _Commitment Status_: None | _Confidence Score_: 1.0
- **Kyou Fujibayashi** (Order: 3, First Girl: 0, Won: 0)
  - _Justification_: Class representative introduced early in the school setting.
  - _Hair Color_: Purple | _Childhood Connection_: None | _Commitment Status_: None | _Confidence Score_: 1.0
- **Fuuko Ibuki** (Order: 4, First Girl: 0, Won: 0)
  - _Justification_: Introduced during the carving starfish arc.
  - _Hair Color_: Blue | _Childhood Connection_: None | _Commitment Status_: None | _Confidence Score_: 1.0
- **Kotomi Ichinose** (Order: 5, First Girl: 0, Won: 0)
  - _Justification_: Revealed to be a childhood friend of Tomoya.
  - _Hair Color_: Purple | _Childhood Connection_: Childhood Friend | _Commitment Status_: None | _Confidence Score_: 1.0
- **Ryou Fujibayashi** (Order: 6, First Girl: 0, Won: 0)
  - _Justification_: Twin sister of Kyou, introduced alongside her.
  - _Hair Color_: Purple | _Childhood Connection_: None | _Commitment Status_: None | _Confidence Score_: 1.0
- **Yukine Miyazawa** (Order: 7, First Girl: 0, Won: 0)
  - _Justification_: Automatically recovered missing major candidate: Yukine Miyazawa.
  - _Hair Color_: Unknown | _Childhood Connection_: None | _Commitment Status_: None | _Confidence Score_: 0.85

### Kanon (ID 58)
- **Ayu Tsukimiya** (Order: 1, First Girl: 1, Won: 0)
  - _Justification_: Ayu is the primary heroine and the first to be introduced in the narrative structure of the visual novel.
  - _Hair Color_: Brown | _Childhood Connection_: Childhood Promise | _Commitment Status_: None | _Confidence Score_: 1.0
- **Nayuki Minase** (Order: 2, First Girl: 0, Won: 0)
  - _Justification_: The protagonist's cousin and childhood friend, introduced early in the story.
  - _Hair Color_: Blue | _Childhood Connection_: Childhood Friend | _Commitment Status_: None | _Confidence Score_: 1.0
- **Mai Kawasumi** (Order: 3, First Girl: 0, Won: 0)
  - _Justification_: Introduced as a major heroine in the school setting.
  - _Hair Color_: Blonde | _Childhood Connection_: None | _Commitment Status_: None | _Confidence Score_: 1.0
- **Makoto Sawatari** (Order: 4, First Girl: 0, Won: 0)
  - _Justification_: Introduced as a major heroine following the initial encounters.
  - _Hair Color_: Brown | _Childhood Connection_: None | _Commitment Status_: None | _Confidence Score_: 1.0
- **Shiori Misaka** (Order: 5, First Girl: 0, Won: 0)
  - _Justification_: Introduced as a major heroine later in the story.
  - _Hair Color_: Brown | _Childhood Connection_: None | _Commitment Status_: None | _Confidence Score_: 1.0

### Air (ID 59)
- **Misuzu Kamio** (Order: 1, First Girl: 1, Won: 0)
  - _Justification_: Misuzu is the primary heroine of the AIR visual novel and the first to be introduced in the Dream arc.
  - _Hair Color_: Brown | _Childhood Connection_: None | _Commitment Status_: None | _Confidence Score_: 1.0
- **Minagi Toono** (Order: 2, First Girl: 0, Won: 0)
  - _Justification_: Introduced as a major heroine in the Dream arc following Misuzu.
  - _Hair Color_: Black | _Childhood Connection_: None | _Commitment Status_: None | _Confidence Score_: 0.95
- **Michiru** (Order: 3, First Girl: 0, Won: 0)
  - _Justification_: Introduced as a major heroine in the Dream arc.
  - _Hair Color_: Brown | _Childhood Connection_: None | _Commitment Status_: None | _Confidence Score_: 0.95
- **Kano Kirishima** (Order: 4, First Girl: 0, Won: 0)
  - _Justification_: Introduced as a major heroine in the Dream arc.
  - _Hair Color_: Brown | _Childhood Connection_: None | _Commitment Status_: None | _Confidence Score_: 0.95

### Special A (ID 60)
- **Kei Takishima** (Order: 1, First Girl: 1, Won: 1)
  - _Justification_: He is Hikari's lifelong rival and primary love interest who eventually proposes marriage to her.
  - _Hair Color_: Brown | _Childhood Connection_: Childhood Friend | _Commitment Status_: Marriage | _Confidence Score_: 1.0
- **Yahiro Saiga** (Order: 2, First Girl: 0, Won: 0)
  - _Justification_: Hikari's childhood friend who harbor romantic feelings for her but loses to Kei.
  - _Hair Color_: Blonde | _Childhood Connection_: Childhood Friend | _Commitment Status_: None | _Confidence Score_: 0.95

### Ouran High School Host Club (ID 61)
- **Tamaki Suou** (Order: 1, First Girl: 1, Won: 1)
  - _Justification_: He is the host club president and the main love interest of Haruhi Fujioka whom he eventually marries.
  - _Hair Color_: Blonde | _Childhood Connection_: None | _Commitment Status_: Marriage | _Confidence Score_: 1.0
- **Hikaru Hitachiin** (Order: 2, First Girl: 0, Won: 0)
  - _Justification_: One of the Hitachiin twins who develops strong romantic feelings for Haruhi but ultimately steps back.
  - _Hair Color_: Brown | _Childhood Connection_: None | _Commitment Status_: None | _Confidence Score_: 0.95
- **Kaoru Hitachiin** (Order: 3, First Girl: 0, Won: 0)
  - _Justification_: Hikaru's twin who also has feelings for Haruhi but prioritizes his brother's and Tamaki's happiness.
  - _Hair Color_: Brown | _Childhood Connection_: None | _Commitment Status_: None | _Confidence Score_: 0.95
- **Kyouya Ootori** (Order: 4, First Girl: 0, Won: 0)
  - _Justification_: Haruhi's friend and co-manager of the club who shows subtle romantic interest.
  - _Hair Color_: Black | _Childhood Connection_: None | _Commitment Status_: None | _Confidence Score_: 0.9

### Fruits Basket (ID 62)
- **Kyou Souma** (Order: 1, First Girl: 1, Won: 1)
  - _Justification_: Cursed Cat of the Sohma family who develops a deep romantic bond with Tohru and eventually marries her.
  - _Hair Color_: Red | _Childhood Connection_: Acquaintance | _Commitment Status_: Marriage | _Confidence Score_: 1.0
- **Yuki Souma** (Order: 2, First Girl: 0, Won: 0)
  - _Justification_: Cursed Rat who initially acts as Tohru's prince but later realizes his feelings for her are maternal.
  - _Hair Color_: Silver | _Childhood Connection_: Acquaintance | _Commitment Status_: None | _Confidence Score_: 0.95

### Kimi ni Todoke (ID 63)
- **Shouta Kazehaya** (Order: 1, First Girl: 1, Won: 1)
  - _Justification_: Sawako's classmate and main love interest who eventually marries her in the manga ending.
  - _Hair Color_: Black | _Childhood Connection_: None | _Commitment Status_: Marriage | _Confidence Score_: 1.0
- **Ume Kurumizawa** (Order: 2, First Girl: 0, Won: 0)
  - _Justification_: Sawako's rival who actively pursues Kazehaya but is rejected.
  - _Hair Color_: Blonde | _Childhood Connection_: None | _Commitment Status_: None | _Confidence Score_: 0.95
- **Kento Miura** (Order: 3, First Girl: 0, Won: 0)
  - _Justification_: Sawako's classmate who briefly shows romantic interest but later supports her relationship with Kazehaya.
  - _Hair Color_: Brown | _Childhood Connection_: None | _Commitment Status_: None | _Confidence Score_: 0.9

### Lovely★Complex (ID 64)
- **Mimi Yoshioka** (Order: 2, First Girl: 0, Won: 0)
  - _Justification_: A minor romantic interest/rival for the protagonist, not the main heroine.
  - _Hair Color_: Brown | _Childhood Connection_: None | _Commitment Status_: None | _Confidence Score_: 0.9
- **Seishirou Kotobuki** (Order: 99, First Girl: 0, Won: 0)
  - _Justification_: Omitted by Gemini during curation; backfilled with defaults.
  - _Hair Color_: Black | _Childhood Connection_: None | _Commitment Status_: None | _Confidence Score_: 0.5
- **Kazuki Kohori** (Order: 99, First Girl: 0, Won: 0)
  - _Justification_: Omitted by Gemini during curation; backfilled with defaults.
  - _Hair Color_: Brown | _Childhood Connection_: None | _Commitment Status_: None | _Confidence Score_: 0.5
- **Maitake Kuniumi** (Order: 99, First Girl: 0, Won: 0)
  - _Justification_: Omitted by Gemini during curation; backfilled with defaults.
  - _Hair Color_: Black | _Childhood Connection_: None | _Commitment Status_: None | _Confidence Score_: 0.5
- **Haruka Fukagawa** (Order: 99, First Girl: 0, Won: 0)
  - _Justification_: Omitted by Gemini during curation; backfilled with defaults.
  - _Hair Color_: Brown | _Childhood Connection_: Childhood Friend | _Commitment Status_: None | _Confidence Score_: 0.5
- **Risa Koizumi** (Order: 100, First Girl: 1, Won: 1)
  - _Justification_: Automatically recovered missing major candidate: Risa Koizumi.
  - _Hair Color_: Unknown | _Childhood Connection_: None | _Commitment Status_: None | _Confidence Score_: 0.85

### Kare Kano (His and Her Circumstances) (ID 65)
- **Soichiro Arima** (Order: 1, First Girl: 1, Won: 1)
  - _Justification_: Yukino's rival and main love interest who she eventually marries during the main story.
  - _Hair Color_: Black | _Childhood Connection_: None | _Commitment Status_: Marriage | _Confidence Score_: 1.0
- **Tsubasa Shibahime** (Order: 2, First Girl: 0, Won: 0)
  - _Justification_: Soichiro's childhood acquaintance who has a crush on him but loses to Yukino.
  - _Hair Color_: Blonde | _Childhood Connection_: None | _Commitment Status_: None | _Confidence Score_: 0.95

### B Gata H Kei (ID 66)
- **Takashi Kosuda** (Order: 1, First Girl: 1, Won: 1)
  - _Justification_: Yamada's main love interest who she eventually marries.
  - _Hair Color_: Brown | _Childhood Connection_: None | _Commitment Status_: Marriage | _Confidence Score_: 1.0

### Mysterious Girlfriend X (ID 67)
- **Mikoto Urabe** (Order: 1, First Girl: 1, Won: 1)
  - _Justification_: Mikoto Urabe is the titular character and the sole primary romantic interest throughout the manga series. She is the first girl introduced and the canonical winner.
  - _Hair Color_: Black | _Childhood Connection_: None | _Commitment Status_: None | _Confidence Score_: 1.0

### My Sweet Tyrant (ID 68)
- **Non Katagiri** (Order: 1, First Girl: 1, Won: 1)
  - _Justification_: Akkun's extremely sweet and devoted girlfriend whom he eventually proposes to.
  - _Hair Color_: Brown | _Childhood Connection_: None | _Commitment Status_: Marriage | _Confidence Score_: 1.0
- **Chiho Kagari** (Order: 2, First Girl: 0, Won: 0)
  - _Justification_: Akkun's younger sister who acts tsundere towards Akkun and Non.
  - _Hair Color_: Blonde | _Childhood Connection_: None | _Commitment Status_: None | _Confidence Score_: 0.9

### The World is Still Beautiful (ID 69)
- **Livius I** (Order: 1, First Girl: 1, Won: 1)
  - _Justification_: The Sun King who marries Nike Remercier.
  - _Hair Color_: Black | _Childhood Connection_: None | _Commitment Status_: Marriage | _Confidence Score_: 1.0

### Myself; Yourself (ID 70)
- **Aoi Oribe** (Order: 1, First Girl: 1, Won: 0)
  - _Justification_: She is the first heroine introduced and the protagonist's childhood friend.
  - _Hair Color_: Brown | _Childhood Connection_: Childhood Friend | _Commitment Status_: None | _Confidence Score_: 1.0
- **Nanaka Yatsushiro** (Order: 2, First Girl: 0, Won: 1)
  - _Justification_: She is the primary romantic interest and the focus of the childhood promise plotline.
  - _Hair Color_: Purple | _Childhood Connection_: Childhood Promise | _Commitment Status_: None | _Confidence Score_: 1.0
- **Shuri Wakatsuki** (Order: 3, First Girl: 0, Won: 0)
  - _Justification_: Childhood friend introduced shortly after the main group is established.
  - _Hair Color_: Blue | _Childhood Connection_: Childhood Friend | _Commitment Status_: None | _Confidence Score_: 1.0
- **Asami Hoshino** (Order: 4, First Girl: 0, Won: 0)
  - _Justification_: Introduced later in the series as a classmate.
  - _Hair Color_: Black | _Childhood Connection_: None | _Commitment Status_: None | _Confidence Score_: 0.95
