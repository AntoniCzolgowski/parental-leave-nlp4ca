# Prompt given to the second and third coders (GPT-6.1 Terra with medium reasoning in ChatGPT, Grok 4.7 Fast)

Run by Antoni in a fresh chat, with the 10 policy texts attached (the same bundles the extractor read). Grok first received all 10 in one combined file and returned 4 as "no text provided"; it was re-run, and its complete second answer is in `outputs/coder3_grok.csv` (first run: `outputs/coder3_grok_run1_partial.csv`).

```
You are a research assistant hand-coding university parental leave policies for a study. Work like a careful human coder: read each attached text file fully, use ONLY what the file says, never outside knowledge or the web.

There are 10 attached files, one university each (the file name is the university). For each, code the rules for ONE reference person: a full-time tenure-track (or permanent) assistant professor with 2 years of service who is having a first child. Use the newest rules in the text.

Fill these 6 fields:
1. birth_fullpay_weeks: weeks completely off work (released from all duties) at full or at least 90% pay, for the parent who gives birth. Count university and statutory/state pay together ONLY if the text states both. Conversions: 1 semester = 16 weeks, 1 quarter = 11 weeks, 1 month = 4.3 weeks, 40 hours = 1 week, 5 working days = 1 week. Weeks paid below 90% do not count. Number, or empty if the text doesn't say.
2. nonbirth_fullpay_weeks: the same, for the partner who does not give birth.
3. teaching_relief_semesters: semesters released from teaching only (still doing research/service) at full pay, IN ADDITION to the weeks off. One of 0, 0.5, 1, 2. Use 0 if not mentioned.
4. tenure_clock: "automatic" (extended unless she declines), "on_request" (she must ask), "none", or "not_applicable" (no tenure-track probation or contract-extension rule in the text).
5. framing: which words organise the rules. "gendered" (maternity/paternity, mother/father), "neutral" (parent, birth parent, non-birth parent, caregiver), or "mixed" (both).
6. primary_caregiver_clause: TRUE if any benefit depends on being the primary caregiver, or on the partner not taking it. Otherwise FALSE.

If something is unclear, give your best guess and explain it in the note (max 20 words). Code each university independently.

Return ONLY a CSV block with this header and 10 rows:
institution,birth_fullpay_weeks,nonbirth_fullpay_weeks,teaching_relief_semesters,tenure_clock,framing,primary_caregiver_clause,note
```
