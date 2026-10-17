# hackathon-rules-20261017

Goal: official-rules check for three AI hackathons, so a small developer team can decide which to enter.

Hackathons: (1) the current Google Gemini / Google DeepMind hackathon, (2) the current ElevenLabs hackathon, (3) the current PayPal AI hackathon. If a name has more than one live edition, use the one still accepting entries and say which.

Produce `results/hackathon-rules-20261017/RESULT.md` with one table row per hackathon:
- official page URL and the official rules / terms URL
- submission deadline (exact date, time, time zone) and any earlier registration deadline
- who may enter: individuals vs teams, max team size, age, country or US-state restrictions, employee or affiliate exclusions
- required tools or APIs (what must the project use?) and whether prior or existing code is allowed
- prizes: amounts per place, and payout rules (who is paid, taxes or forms required, cash vs credits, time to payout)
- judging criteria and judging dates
- IP / licensing terms (does the host get rights to the project?)

Then a 3-line "easiest to win / best fit for a solo developer" ranking with one reason each, based only on the rules.

Rules: official pages and the official rules text only; a link for every fact; retrieval date. Say "unsure" rather than guess. Mark anything you could not find. End with **How I checked it** and **Unsure about**.

Delivery: push `results/hackathon-rules-20261017/RESULT.md` (commit message `result hackathon-rules-20261017`). Then in chat reply with three lines: `RESULT hackathon-rules-20261017`, a one-line summary, `END hackathon-rules-20261017`.
