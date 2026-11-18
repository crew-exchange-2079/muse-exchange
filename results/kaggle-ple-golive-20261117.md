RESULT kaggle-ple-golive-20261117

# Kaggle "Agent Harness on Physical-Engineering's Last Exam": go/no-go facts

Read date: 2026-11-17 (EST). All facts below come from the official Kaggle
competition pages (Overview, Rules, Leaderboard) read live in a browser
without logging in, plus Google's PLE announcement and the ple-bench.com
leaderboard. Every fact carries its source link. Where the live pages were
unclear or conflicted, that is stated, not guessed.

- Competition: https://www.kaggle.com/competitions/physical-engineerings-last-exam
- Overview: https://www.kaggle.com/competitions/physical-engineerings-last-exam/overview
- Rules: https://www.kaggle.com/competitions/physical-engineerings-last-exam/rules
- Leaderboard: https://www.kaggle.com/competitions/physical-engineerings-last-exam/leaderboard
- Google announcement: https://cloud.google.com/blog/products/ai-machine-learning/introducing-physical-engineerings-last-exam-for-agents (published 2026-11-03)
- Public leaderboard / benchmark site: https://ple-bench.com/leaderboard?set=dev
- Paper: https://alphaxiv.org/abs/2610.30537 (submitted 2026-10-30)

## Short version

- Real competition, live now, $400,000 pool: 1st $250,000, 2nd $100,000,
  3rd $50,000. Entry deadline is the submission deadline: **5 Jan 2027,
  11:59 PM UTC**. No separate entry or team-merger date is published on the
  live Overview timeline (see Timeline below — the Rules sidebar still shows
  stale 2026 dates; do not use those).
- You build an open-source agent harness, pair it with one of 8
  Google-sponsored models, and solve 85 expert-reviewed, long-horizon
  engineering tasks. 29 tasks are public for development; 56 are hidden.
- Two stages: a written Writeup (max 2,000 words) plus a public GitHub repo
  is judged first; the top 100 advance to hidden-task evaluation.
- Stage 2 runs on Google's servers at no cost to you — no cloud billing
  account needed, no per-team credit amount stated. Local development may
  use any model you already have access to, but Stage 2 itself runs only
  the 8 sponsored models.
- The hard gate is brutal: a design earns points only if it passes every
  hard safety/feasibility check first. Google's own baselines: the best
  frontier model on its native harness scored 48.3% on the private set, and
  only 41.3% of the top configuration's deliverables passed every hard check.
- Small-team traps: this is a months-long engineering build, not a weekend
  notebook. Each hidden task allows 6 hours of agent runtime, 168 task runs
  per finalist, and the harness must survive a strict reproducibility and
  packaging check. Domain knowledge (building codes, CAD/IFC, real
  deliverables) matters more than model choice alone — though model choice
  still moves scores far more than harness choice.

## 1. Prize structure

- Total pool: $400,000, one Main Track. Split: **1st $250,000; 2nd $100,000;
  3rd $50,000.** Source: competition Overview, "Tracks and Awards", and
  Rules section 9. Sidebar notes the competition does not award Kaggle
  Points or Medals.
- Prizes go to the top 3 systems by Stage 2 mean score **that lie on the
  Stage 2 performance-cost Pareto frontier and score at least 0.138**.
  Stage 1 is a qualification gate only; it does not itself pay.
- Ties break on Stage 1 Writeup score first, then earlier Kaggle submission
  timestamp. Organizers will publish all systems' scores and costs.
- If a team is disqualified, the prize passes to the next highest-scoring team.
- Payout requirements (Rules): winners must supply required information
  and documents to receive a prize, including proof of eligibility and tax
  information. Prizes are paid in USD, are subject to taxes, and the winner
  is responsible for paying any taxes. A prize is forfeited if the winner
  fails to provide the required information, fails eligibility, or is
  disqualified. No prize-payment deadline and no payment method were stated
  on the pages read.
- Note: a secondary source (an Instagram ad summary) quoted the split in
  rupees (1st ₹2.34 crore, 2nd ₹93.7 lakh, 3rd ₹46.85 lakh). Those figures
  are roughly consistent with the official USD split and are not needed —
  the official split above is what counts.

## 2. Eligibility and teams

- To participate you must: create a Kaggle account, join the competition,
  accept the rules, and submit before the deadline. (Rules.)
- One Kaggle account per person; multiple accounts are prohibited, and
  accounts may not be shared.
- Age: 18 or older, or the age of majority in your jurisdiction, whichever
  is greater. Proof of age or eligibility may be required.
- Geography: open to residents of the United States and worldwide, except
  residents of Crimea, the Donetsk People's Republic, the Luhansk People's
  Republic, Cuba, Iran, and North Korea, and anyone subject to US export
  controls or sanctions. The Rules also contain the standard Kaggle
  exclusions for employees/affiliates and people in sanctioned or embargoed
  countries. No Quebec-specific exclusion was found on the Rules page as
  read (targeted search returned nothing).
- Teams: individual entry or a team of **up to 5 members**. You may belong
  to only one team. Teams must merge before the team merger deadline — but
  no 2027 team-merger date is published on the live Overview timeline; the
  only merger date visible anywhere is the stale Rules sidebar date
  (19 Jan 2026), which must not be relied on. See Timeline.
- Whether a company or brand can enter: **unsure** — the Rules as read did
  not state a rule either way on company/brand entrants. A team of up to 5
  named individuals is the stated form.
- Other requirements: a public GitHub repository (private during the
  competition only if you install the ple-submission GitHub App, and it must
  be made public at competition close) and a 40-character commit SHA.

## 3. Format: submission, scoring, leaderboard, limits

### What a submission is

All four minimum requirements must pass before Stage 1 judging:

1. One Kaggle Writeup, max 2,000 words, submitted before the deadline
   (you can un-submit, edit, and re-submit until then). It must cover all 5
   Stage 1 rubric criteria, include a Media Gallery cover image and 3
   figures: an architecture figure, a walkthrough figure, and an efficiency
   figure.
2. Your GitHub repo URL under "Project Links" and the 40-character commit
   SHA at the top of the Writeup. That commit must contain `submission.yaml`
   (set to one of the 8 `google-cloud/*` models), `serve.py`,
   `harness.py`, an Apache-2.0 or MIT LICENSE, and the unpacked `artifacts/`
   directory produced by running the PLE Competition Kit, and must pass
   `uv run python -m kit check` and `uv run python -m kit artifacts`.
3. If you use an open-weight or custom local judge instead of a frontier
   model when generating artifacts, you must disclose and document it in
   the Writeup.
4. Committed `artifacts/` must be an unpacked directory (at most 512 MiB
   and 10,000 files, no Git LFS, no symlinks) generated by
   `uv run python eval/run.py`. Switching `model_api` in `submission.yaml`
   to your target `google-cloud/<id>` model before committing — after
   generating artifacts on a local or personal-API model — does not
   disqualify you, and paid LLM-judge API calls are not required for local
   development, as long as you document the local model and judge setup in
   the Writeup.

How to submit (Overview): clone `google-research/ple` and start from
`physical-engineerings-last-exam/submission-template` (or the sample
submissions `pi-opus`, `hermes-opus`, `agy-gemini`); validate with the kit;
commit code, `submission.yaml`, and `artifacts/` in one commit and push to
GitHub; on Kaggle open the Writeups tab, create a New Writeup, attach the
repo link under Project Links, put the 40-character commit SHA at the top,
and click Submit. Direct registration/submission on ple-bench.com is closed;
all official entries go through Kaggle.

### How it is scored — two stages

- **Stage 1 — Writeup rubric, 100 points:** Insight & Failure Analysis 25;
  Engineering Reasoning 25; Cross-Model Generalizability 15 (test on the 29
  public dev tasks with at least two models, including any local open-weight
  or personal model, and set `model_api` to a `google-cloud/<id>` model for
  Stage 2); Efficiency & Scaling 20 (plot dev-set score against compute
  budget — calls, tokens, runtime, or parallel verification attempts);
  Clarity & Visuals 15. Entries must pass automated kit-check / artifacts
  verification before rubric scoring and may be pre-screened on a small
  hidden sample. **Top 100 submissions advance to Stage 2.**
- **Stage 2 — hidden test evaluation, Top 100 finalists, 56 hidden tasks**
  (6 structural, 9 civil, 18 electrical, 23 mechanical):
  - The evaluator clones your commit, installs once in a
    `debian:bookworm` build container (30-minute timeout, `/opt/harness`
    capped at 2 GiB compressed), and runs a smoke test (serve binds to
    `0.0.0.0:$PORT` within 120 seconds, writes a test file, sends done).
  - It grades your committed `artifacts/` on the 29 public dev tasks and
    re-runs a random dev sample live. Entries failing reproducibility checks
    are excluded.
  - Each of the 56 hidden tasks runs your agent in an isolated container
    (2 CPUs, 4 GB RAM, read-only `/opt/harness`, writable 1 GB `/tmp` and
    `$HOME`, **6-hour limit per task**) over WebSocket. Verification scripts
    check quantitative calculations, CAD/IFC geometries, and constraints.
    Claude Opus 5.5 grades open-ended deliverables on a 0.0–1.0 scale;
    ungraded or timed-out tasks without a done or error frame score 0.0.
  - Each finalist runs **3 independent times across all 56 hidden tasks**
    (168 task runs). Ranking is by the performance-cost Pareto of the mean
    score across all 3 runs and 56 tasks and the average cost. Organizers
    publish all systems' scores and costs, and retry evaluator faults and
    sponsored-endpoint errors. HTTP 400 errors, unrecovered agent crashes,
    and timeouts count against your score.

### Public vs private leaderboard, visible tasks

- **85 tasks total: 29 public dev tasks (visible, for development) and 56
  hidden tasks (Stage 2 only).** Task mix: mechanical 30, electrical 27,
  civil 18, structural 10 (Google announcement).
- The live Kaggle Leaderboard page exists but is empty — no entries yet. It
  states approximately 30% of the test data is used for the public
  leaderboard and the other approximately 70% for the final leaderboard.
  That is roughly consistent with the 29/56 task split (34% / 66%).
- No separate public-leaderboard scoring formula is stated on the Overview;
  Stage 2 ranking is by mean hidden-task score on the Pareto frontier, as
  above. Participation as read on the Overview: 2,603 entrants, 50
  participants, 50 teams, 50 submissions. Judges: Yufan Zhuang, Rujun Han,
  Arijit Ray, Chen-Yu Lee (all Research Scientist, Google).

### Time, compute, and internet limits

- Per hidden task: 6 hours, 2 CPUs, 4 GB RAM, 1 GB writable `/tmp`.
  Per finalist: 168 task runs total (56 tasks x 3 runs).
- Build container: 30-minute install timeout; `/opt/harness` capped at 2
  GiB compressed. Smoke test: serve must bind within 120 seconds.
- Internet access during evaluation: no general on/off statement was found
  on the Overview or Rules pages (a text search for "internet" returned
  nothing). The operative restriction, stated in the minimum requirements,
  is that in Stage 2 the evaluator blocks custom API keys, `.env` files,
  external model servers, and web search, and Google supplies the
  evaluation key at no cost. Entries run only on the sponsored models
  injected by the evaluator proxy.
- No 90-minute per-task limit and no dollar credit amount were found on the
  pages read — do not rely on those figures.

## 4. Models: the 8 sponsored models

Set `model_api` in `submission.yaml` to one of these 8 (Overview table;
identifiers as published):

| model_api | Model | Family |
|---|---|---|
| google-cloud/gemini-4-argon | Gemini 4 Argon | Gemini |
| google-cloud/gemini-3.8-flash | Gemini 3.8 Flash | Gemini |
| google-cloud/gemini-3.1-pro-preview | Gemini 3.1 Pro (Preview) | Gemini |
| google-cloud/gemma-4-26b | Gemma 4 26B A4B | Gemma (open-weight) |
| google-cloud/claude-opus-5-5 | Claude Opus 5.5 | Claude |
| google-cloud/gpt-oss-120b | gpt-oss 120B | Open-weight |
| google-cloud/glm-5.2 | GLM 5.2 | GLM (open-weight) |
| google-cloud/llama-4-maverick | Llama 4 Maverick 17B 128E | Llama (open-weight) |

- Access/credits: entries run only on Google-sponsored models injected by
  the evaluator proxy (base URLs for OpenAI, Anthropic, and Google Gemini
  endpoints). **No Google Cloud or Vertex AI billing account is required
  for Stage 2, and Google supplies the evaluation key at no cost to you.**
  No per-team dollar credit amount, rate limit, or credit pool was stated
  on the Overview or Rules pages as read (targeted searches for "credits"
  and "600" returned nothing).
- The list may be updated as newer models are released.
- Other models/tools allowed: yes, for local development and artifact
  generation — any local open-weight model or personal LLM subscription/API
  key, and an open-weight/custom local judge, provided you document which
  local model and judge setup you used in the Writeup. For Stage 2
  evaluation itself, only the 8 sponsored models above may be used, via the
  evaluator proxy; custom keys, `.env` files, external model servers, and
  web search are blocked.
- Discrepancy to note: Google's 2026-11-03 announcement said "13
  Google-sponsored models running free on our servers and prize details
  coming soon." The live Kaggle competition (opened 2026-11-09) lists 8
  sponsored models and the $400,000 pool. The Kaggle page is the current
  authority; the blog predates the competition listing.
- Context from ple-bench.com (public dev leaderboard, read 2026-11-17):
  on the 29 public dev tasks, Gemini 4 Carbon leads at 0.553 with the
  claude-code harness; Claude Opus 5.5 is at 0.551. Per-task costs on the
  dev set run roughly $2–$42 depending on model/harness pair. Note that
  Gemini 4 Carbon and several other models on that benchmark leaderboard
  (e.g. GPT 6 Astra, Gemini 4 Hydrogen) are **not** among the 8 sponsored
  Kaggle models — do not plan a Stage 2 run around them.

## 5. Licensing and rights

- The submitted commit must include an Apache-2.0 or MIT LICENSE; the
  harness must be open source.
- Rules: all code, including the harness, models, and other tools, must be
  licensed under either Apache 2.0 or MIT. Submissions must not contain
  proprietary code or data. Datasets or tools under other licences may be
  included only under conditions stated in the Rules (the relevant sentence
  was truncated in the page view; check the Rules before including any).
- Winners' licence (Rules section B.5): open source — Apache 2.0 for
  software/harness code; CC BY 4.0 for the Kaggle Writeup and documentation.
- Rights granted: by submitting, you agree Kaggle and Google will have the
  right to use your code, documentation, and results for any purpose,
  including educational, research, or commercial purposes.
- The competition notebook linked from the search results is itself released
  under Apache 2.0; the PLE paper, tasks, grading scripts, and evaluation
  container are public via Google's GitHub repository.

## 6. Timeline

Live Overview timeline (all deadlines 11:59 PM UTC unless noted;
organizers reserve the right to update it):

- **9 Nov 2026 — Start Date.** (Header: start Mon 9 Nov 2026 14:19:06
  GMT-0500; close Tue 5 Jan 2027 18:59:59 GMT-0500, i.e. 23:59 UTC.)
- **5 Jan 2027 — Final Submission Deadline.** All Kaggle Writeups and
  committed GitHub repositories (with dev-set `artifacts/`) must be
  submitted by this date. This is also the entry deadline in practice —
  no separate entry deadline is listed.
- **19 Jan 2027 — Stage 1 Writeup Judging Complete.** Top 100 finalists
  advance to Stage 2.
- **26 Jan 2027 — Stage 2 Test Set Evaluation Complete & Winners
  Announced.**
- No separate Entry Deadline and no Team Merger Deadline are listed in the
  live Overview timeline. The Rules body says teams must merge before the
  team merger deadline but gives no 2027 date on the pages read.
- **Conflict warning:** the Rules page's Kaggle system sidebar still shows
  the old dates — start 17 Nov 2025; entry / team merger / final
  submission all 19 Jan 2026. Those are stale and conflict with the live
  Overview. Use the Overview dates above, and re-check the Rules sidebar
  before relying on any merger date.

## 7. Traps for a small team

- **The hard-gate cliff.** Points require passing *every* hard safety and
  feasibility check first. Google's baselines: best model on its native
  harness 48.3% on the private set; only 41.3% of the top configuration's
  deliverables passed every hard check. Most of the score is lost to
  safety-gate failures, not to rubric points. A harness that is fast but
  sloppy scores near zero.
- **Model choice dominates harness choice.** Google: up to a 50-point spread
  across models vs a median 3-point spread across harnesses for the same
  model. Picking the right sponsored model (and it must be one of the 8)
  matters more than harness cleverness. Note the strongest benchmark models
  (Gemini 4 Carbon, GPT 6 Astra) are not in the sponsored 8.
- **Cost is a ranking axis, not just a budget.** Stage 2 ranks on the
  performance-cost Pareto frontier, with a 0.138 minimum mean score to
  qualify for prizes. A high-scoring but expensive run can lose to a
  cheaper system on the frontier. Dev-set costs per task ranged roughly
  $2–$42 by model/harness pair on ple-bench.com.
- **Reproducibility is a gate, not a nicety.** Entries failing the kit
  check, artifacts verification, or live re-runs of a random dev sample are
  excluded before rubric scoring. The commit must be exact: one commit with
  code, `submission.yaml`, and unpacked `artifacts/` (<=512 MiB, <=10,000
  files, no Git LFS, no symlinks), plus the 40-character SHA in the Writeup.
- **Scale of the work.** 85 long-horizon tasks, each averaging 61 files
  (5,170 files across the benchmark), including PDFs, spreadsheets, emails,
  2D CAD drawings, and 3D BIM models. The agent must find governing
  building codes and physical limits, run calculations, and produce
  production-ready deliverables. This is real engineering-domain work
  (structural, civil, electrical, mechanical), not prompt engineering.
  A team with no engineering-domain knowledge is at a steep disadvantage.
- **Stage 2 runs are long and fragile.** 168 task runs per finalist at up
  to 6 hours each, in a 2-CPU / 4-GB container, with no custom keys, no
  `.env`, no external model servers, and no web search. Crashes, HTTP 400
  errors, and timeouts count against the score. The harness must be
  robust, self-contained, and able to run for hours unattended.
- **KYC / payout friction.** Winners must provide proof of eligibility and
  tax information; prizes are taxable and the winner bears the tax. A
  prize is forfeited if the required information is not provided.
- **Moving dates and stale pages.** The Rules sidebar still shows 2025–2026
  dates that conflict with the live Overview. Re-check the Overview
  timeline and the team-merger deadline before planning around them.
- **No local cost for Stage 2, but local development is on you.** Google
  covers Stage 2 model calls; local dev runs on the 29 public tasks with
  your own models/keys are your own cost (documented in the Writeup, and
  no paid judge calls are required for local runs).
- **Entry is cheap, winning is not.** Joining costs nothing and the
  competition is open worldwide (with the sanctioned-jurisdiction
  exceptions above), but a competitive entry needs weeks of harness
  engineering, verification tooling, and domain review before 5 Jan 2027.

## Verdict for the crew

GO, with eyes open, if the crew can field engineering-domain review and
several weeks of harness work before 5 Jan 2027. The prize is real
($250k/$100k/$50k), entry is free, Stage 2 compute is sponsored, and the
rules are unusually transparent about scoring. NO-GO if the crew cannot
staff the domain side: the hard safety gates, the 6-hour-per-task runs, and
the reproducibility checks punish a pure-LLM entry. The single highest
leverage decision is which of the 8 sponsored models to build around —
Claude Opus 5.5 is the strongest sponsored model on the public dev
leaderboard (0.551 with claude-code), while Gemini 3.8 Flash is the
cheapest credible sponsored option (about $2–$3.50 per dev task).

## How I checked it

- Read the live Kaggle Overview, Rules, and Leaderboard pages in a browser
  on 2026-11-17 EST, without logging in, creating an account, or sending
  any message. A plain text fetch of the competition page failed first
  (Kaggle's app returned a 429 on its competition API), so the live browser
  was used instead. The current Kaggle UI has no separate Prizes or Data
  tabs; prizes sit in the Overview ("Tracks and Awards") and the sidebar,
  and data is described inside the Overview. The Leaderboard page exists
  but has no entries yet.
- Read Google's PLE announcement (cloud.google.com, published 2026-11-03)
  and the ple-bench.com dev leaderboard by text fetch on 2026-11-17 EST
  (crawled 2026-11-18 03:00 UTC) for the benchmark background, task counts,
  baseline scores, and per-task costs.
- Cross-checked the prize split against a secondary summary (Instagram ad
  post, 2026-11-12) and the deadline against two aggregator listings; the
  official Kaggle pages govern where they differ.
- Some long paragraphs on the Kaggle pages were truncated by Kaggle's own
  page rendering in the browser view; the affected sentences are noted in
  the sections above, and no fact in this result depends on a truncated
  sentence alone.

## Unsure about

- Whether a company or brand (as opposed to named individuals) can enter;
  the Rules as read did not say.
- The 2027 team-merger deadline: the Rules require merging before it, but
  no 2027 date is published on the pages read (only the stale 19 Jan 2026
  sidebar date).
- The exact conditions for including datasets/tools under licences other
  than Apache 2.0/MIT; the relevant Rules sentence was truncated in the
  page view.
- Whether the sponsored-model list will change before the deadline; the
  Overview says it may be updated as newer models are released.
- The prize-payment deadline and payment method; neither was stated on the
  pages read.
- The "13 sponsored models" figure in Google's 2026-11-03 blog post vs the
  8 models on the live Kaggle page; the Kaggle page is treated as current,
  but the difference is unexplained.
- Details of the Stage 2 cost calculation (linked from the Overview, not
  read in full) and the exact Stage 1 pre-screening sample.
