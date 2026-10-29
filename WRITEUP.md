# Write-up: AI Proposal Triage

## 1. AI vs rules
**AI:** reading messy proposal text and pulling out facts (way easier and i do not miss the relevant details although i am never too satisfied by an AI's answer but yk everything written in either a tabular or a proper form where you can read everything in an instant makes everything breathable) (licence, price, weeks, warranties, team details), and optionally writing the one-line reason like i said before (why rank one proposal better than the other)

**Rules/code:** loading the admin's criteria, mandatory pass/fail, all scoring maths, ranking, flagging, and logging.

**Why there:** language is fuzzy (no offense), so AI helps there. Pass/fail and arithmetic must be exact and repeatable, so code does them. The AI should never get the final decision anywhere *begging emoji*, only what the document says.

## 2. Consistency and explainability
- Each proposal is extracted once at temperature 0 into a fixed JSON schema, and the result is stored.
- Scoring is code over the stored facts, so ranking the same proposals twice gives the same result. Only re-extraction could vary, so it is cached and only repeated on request.
- Every extracted value carries an exact quote and page. A rule checks the quote really exists in the source text; if not, the value is discarded.
- The reviewer sees a table per proposal: each criterion, its score, its weight, and the quote behind it. "Why is A above E?" is answered by comparing those rows.

## 3. Human in the loop
- **Before scoring:** the reviewer sees extracted facts next to their quotes and can correct any value.
- **Flags:** unclear mandatory criteria, missing data (no schedule), suspected injection, and quotes that fail verification all go to the reviewer instead of being auto-decided, or dates- timeline matching 
- **After ranking:** the reviewer can override any score, status or rank, and must give a reason.
- **Award:** a human makes the final decision. The tool only recommends.
- **Audit log:** who uploaded what, criteria version, prompt version, model name, raw AI output, verification results, every score, every override (who, when, why), and the final decision.

## 4. Changing criteria
Criteria are versioned. An edit creates a new version and never changes old ones. Existing results stay linked to the version that produced them and are labelled "scored under v2, current is v3".
The reviewer can re-score with one click. Because extraction is stored, this is only code and needs no new AI call, unless the new criterion needs a fact we never extracted. Then only the missing field is re-extracted. Both results are kept, and the reviewer sees what changed. Awarded decisions are never silently altered.


## 5. Risks
| Risk | Guard |
|---|---|
| Wrong extraction | Quote required and verified against source; reviewer confirms key facts; cannot-confirm items are flagged. |
| Made-up facts | "Not stated" is allowed and expected; no guessing; unverifiable values dropped. |
| Vague or conditional claims (B's subcontractor, D's missing schedule) | Strict definitions in code: licence must be held by the bidder; no schedule means no timeline score and a flag. |
| Window of dates | "Since 2021" may include installs outside the 5-year window; the extraction records the date wording and the reviewer confirms. |
| Bias | Company names and reputation are not scoring inputs; the criteria are the only basis; periodic audit of overrides and outcomes. |
| Gaming the format | Page limits, file type checks, and scanning for hidden text. |
| Cost | Extract once and cache; small model; scoring is free code. |
| Criteria drift | Versioning (see 4). |

