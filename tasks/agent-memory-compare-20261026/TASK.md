# agent-memory-compare-20261026

Goal: find out whether any maintained self-hosted agent-memory system is clearly better than a plain Postgres keyword-search facts table for a small fleet of AI coding agents.

Research (public web only; primary sources first: each project's GitHub repo, docs, license file, release page, and any published benchmark paper or eval repo; give the URL and date for every number).

Context: a small team of AI coding agents needs one shared long-term memory ("facts" about hosts, decisions, prior work), self-hosted, read by many sessions through an MCP server. Current plan: a plain Postgres table with full-text keyword search (tsvector) plus optional pgvector. A blind test on our own questions found keyword search beat embedding search.

Compare: (1) Hindsight (agent memory system; find the canonical repo), (2) Beacon (agent memory; find the canonical repo; if several projects share the name, list them and pick the agent-memory one), (3) Postgres full-text + pgvector behind a small MCP server, (4) any one other maintained self-hosted agent-memory project with an MCP server that has real adoption (e.g. Graphiti/Zep CE, Letta, mem0 OSS: pick the strongest, say why).

For each: license, last release date, commit activity in the last 90 days, open-issue count, storage backend, self-host footprint (RAM, services), MCP support, update/versioning of facts (can it mark a fact superseded?), published retrieval benchmarks (LongMemEval, LoCoMo or similar) with numbers, and practitioner reports (blog posts, HN/Reddit threads) about failures in production.

Deliver: one comparison table, then a 5-line verdict: is any option clearly better than Postgres keyword search for a small fleet, and what A/B test would prove it. Mark anything unverified NOT FOUND. Under ~1,500 words.

Rules: public pages only, no login, no account, no purchase, no messages or comments to anyone. A link and read date for every fact. Say "unsure" rather than guess. End with **How I checked it** and **Unsure about**.

Delivery: reply in this chat with the full RESULT block: first line `RESULT agent-memory-compare-20261026`, then the complete answer in Markdown (write every source as a full https:// link in plain text), last line `END agent-memory-compare-20261026`. Also push `results/agent-memory-compare-20261026/RESULT.md` to GitHub only if asked.
