# Leaving for Europe, or leaving science?

NLP for Cultural Analytics (CSCI 7000, CU Boulder, Fall 2026), proposal 3. Antoni Czolgowski.

**Question.** When women leave US science around their first child, do they go to Europe or out of science, and does the university's parental leave policy change that? Part 1 reads faculty parental leave policies with an LLM and a fixed codebook (US universities and matched European "twins"). Part 2 follows careers in OpenAlex (pilot) and, in the full study, the AARC faculty census.

This repo holds the feasibility test only. The proposal is in `proposal/`.

## Pipeline

| Step | Script | What it does |
|---|---|---|
| 1 | `src/01_pull_openalex.py` | Institutions for matching; random samples of US-affiliated authors (OpenAlex API, key in `OPENALEX_KEY`) |
| 2 | `src/02_match_twins.py` | 20 US universities (10 in states with paid family leave insurance, 10 without, CU Boulder fixed) matched one-to-one to European twins on field mix, size and citations per paper → `outputs/twins.csv` |
| 3 | `src/03_fetch_policies.py` | Downloads the official policy pages / PDFs listed in `data/urls_*.json` (found with LLM-assisted search); pages that block bots were taken from the Wayback Machine |
| 4 | `src/04_bundle_passages.py` | Keeps the leave-related passages of long documents (union contracts, handbooks) |
| 5 | `src/05_codebook_prompt.md` | The codebook and extraction prompt (10 fields, evidence quote and confidence per field) |
| 6 | `src/06_careers.py`, `src/07_rate_ratios.py` | Career table (name-based gender, last US year, destination), women-to-men rate ratios by career age with author-level bootstrap → `outputs/rr_dest.csv` |
| 7 | `src/07b_policy_panel.py` | Joins the extracted fields of each US university and its twin → `outputs/policy_fields_by_pair.csv` |
| 8 | `src/05b_coder_prompt.md`, `src/08_coder_agreement.py` | Second and third coders (GPT-6.1, Grok) on 10 universities; agreement with the extraction → `outputs/agreement_rows.csv` |
| 9 | `src/09_figure.py` | Figure 1 |

`outputs/wayback_cdx.json` counts Wayback captures and distinct versions for six US policy pages.

Policy texts are not redistributed here (they belong to the universities); the scripts re-download them. OpenAlex data are CC0.

## Feasibility numbers (26 Oct 2026)

- 92 policy documents, 551,000 words, eight languages; 4 of 20 European twins have no public staff-leave page.
- Extraction (Claude) vs GPT-6.1: 51 of 60 cells; vs Grok: 50 of 60; Claude matches at least one other coder on 58 of 60.
- Median weeks at full pay for a birth parent: 12 (US, 18 of 20 texts state it) vs 18 (European twins, 11 of 20).
- Careers: 8,943 OpenAlex authors (3,651 women); women-to-men rate ratio of moves to Europe 0.81 [0.50, 1.21] at career ages 6-8, of exits 1.29 [1.01, 1.60] at 12-14.
