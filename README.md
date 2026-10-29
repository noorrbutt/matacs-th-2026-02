# MATACS-TH-2026-02: AI Proposal Triage Design

- **Name:** Noor Butt
- **Reference:** MATACS-TH-2026-02
- **Time actually spent:**about 1.5 hours

## How I used AI tools
I used claude for a better understanding of the provided candidate brief, then I asked it to provide me a skeleton for each file, so that I can copy and paste them into my repo while also filling it with my relevant stuff. 
For a different opinion I asked ChatGPT and it said C is the best, hence I went to read C to check whether the claim justifies but C gives no monitoring or safety plan, I switched back to claude (limit was reset by then hehe), It said A is the best and I went to check A but found "since 2021" sounded vague?? but A claims 14 installs, so even if a few fall outside the window it still qualifies well, and A beats the other proposals on price, timeline and team plan.so A winss (hopefully)
-I also used claude in process flow diagram which it almost met my expectations in the third attempt :)

## Files
- [WRITEUP.md](WRITEUP.md): answers to the five questions
- [diagram/flow.png](diagram/flow.png): process flow, upload to ranked output
- [PROMPTS.md](PROMPTS.md): extraction prompt and optional reason prompt
- [ranking.json](ranking.json): expected ranking of A-E
- [prototype/](prototype/): optional script. `python prototype/score.py prototype/sample_extractions.json ranking.json` re-creates the ranking deterministically.
