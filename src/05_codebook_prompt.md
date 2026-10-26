# Codebook and extraction prompt (v1, 26 Oct 2026)

You read the official leave rules that apply to one university's academic staff, as text excerpts (several sources may be given: university pages, collective agreements, and national rules). Code the rules for ONE reference person:

> A full-time, tenure-track (or permanent/tenure-track-equivalent) assistant professor with 2 years of service, who has her first child by birth (BIRTH PARENT), or whose partner gives birth (NON-BIRTH PARENT). Use the rules in force now (the newest version in the text).

Count statutory/state benefits together with university benefits when the text states them (e.g. UK Statutory Maternity Pay inside an occupational scheme, a US state paid family leave program that the university policy coordinates with, a European social insurance benefit that the university tops up). If the text does not state a statutory amount, do not add it from your own knowledge: code only what the text says and set `relies_on_outside_rules` to true.

Fields:

1. `birth_fullpay_weeks` (number or null): weeks of leave, released from ALL duties, paid at 90-100% of salary, for the birth parent. Convert units: 1 semester = 16 weeks, 1 quarter = 11 weeks, 1 month = 4.3 weeks, 1 day = 1/5 week (working days) unless calendar days are stated (then 1/7), 40 hours = 1 week. Paid at less than 90% does not count here.
2. `birth_paid_weeks_any` (number or null): weeks of leave with ANY pay (including partial statutory pay) for the birth parent.
3. `nonbirth_fullpay_weeks` (number or null): as field 1, for the non-birth parent.
4. `teaching_relief_semesters` (number: 0, 0.5, 1, 2, or null): semesters of release from teaching (modified duties) at full pay that come IN ADDITION to field 1 (the person still does research/service). 0 if none stated.
5. `tenure_clock` ("automatic" | "on_request" | "none" | "not_applicable" | null): extension of the probationary / tenure clock or fixed-term contract for a birth. "not_applicable" when there is no tenure-track probation in the text (common in Europe) and no contract extension rule.
6. `framing` ("gendered" | "neutral" | "mixed"): the language the policy uses for parents. gendered = maternity/paternity, mother/father, woman/man as the organising categories; neutral = parent, birth parent / non-birth parent, caregiver; mixed = both organise the rules.
7. `primary_caregiver_clause` (true | false): a benefit depends on being the primary caregiver or on the partner not taking the benefit.
8. `payer` ("university" | "state_or_insurance" | "mixed" | null): who pays most of field 2.
9. `service_requirement_months` (number or null): minimum months of service to get the full benefit.
10. `relies_on_outside_rules` (true | false).

For every field give a short verbatim `evidence` quote (max 25 words, from the text; null if none) and a `confidence` (high | medium | low).

Output: one JSON object per university:
{"institution": ..., "fields": {"birth_fullpay_weeks": {"value": ..., "evidence": ..., "confidence": ...}, ...}, "notes": "one sentence on anything ambiguous"}
