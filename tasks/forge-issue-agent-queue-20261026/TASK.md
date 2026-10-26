# forge-issue-agent-queue-20261026

Goal: learn how others run AI coding agents off a Git forge issue queue (Gitea/Forgejo/GitHub), so we copy proven patterns instead of inventing them.

Research (public web only; primary sources first: project repos and docs, engineering blog posts with dates; give the URL and date for every claim).

Context: a small self-hosted setup wants a Git forge's issue tracker (Gitea or Forgejo) to be the ONE task queue for AI coding agents: each issue carries labels for model, resource, data tier and status, plus an executable acceptance check written BEFORE any agent runs; a scheduler dispatches one-shot headless agents; results (branch, test output, verdict) are written back to the issue.

Find: (1) maintained open-source projects that already do issue-to-agent dispatch on Gitea/Forgejo or GitHub (e.g. OpenHands resolver, SWE-agent, Sweep, Copilot coding agent patterns, Forgejo/Gitea Actions-based agents): what they do, license, last release, whether they work with Gitea/Forgejo; (2) concrete label taxonomies and issue templates teams use for agent work (paste examples); (3) how they prevent duplicate work (two agents on one issue, or re-doing finished work): locks, assignment, dedupe searches; (4) how acceptance checks are attached to issues and enforced before merge; (5) reported failure modes of agent-driven issue queues (runaway cost, false passes, stale issues).

Deliver: a table of projects (name | what it does | forge support | license | last release | URL), 2-3 example label sets or templates verbatim with sources, then a 10-line list of practices worth copying and pitfalls to avoid. Mark anything unverified NOT FOUND. Under ~1,500 words.

Rules: public pages only, no login, no account, no purchase, no messages or comments to anyone. A link and read date for every fact. Say "unsure" rather than guess. End with **How I checked it** and **Unsure about**.

Delivery: reply in this chat with the full RESULT block: first line `RESULT forge-issue-agent-queue-20261026`, then the complete answer in Markdown (write every source as a full https:// link in plain text), last line `END forge-issue-agent-queue-20261026`. Also push `results/forge-issue-agent-queue-20261026/RESULT.md` to GitHub only if asked.
