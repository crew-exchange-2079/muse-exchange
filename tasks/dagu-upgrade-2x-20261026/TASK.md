# dagu-upgrade-2x-20261026

Goal: decide whether a small self-hosted Dagu 2.18.2 install should stay put or upgrade to a later exact version before adding distributed workers.

Research (public web only; primary sources first: github.com/dagu-org/dagu releases, CHANGELOG, docs.dagu.cloud or the repo docs/, GitHub issues and discussions; give the URL and the release/issue date for every claim).

Context: a small self-hosted setup runs Dagu 2.18.2 on one node, with named queues in config.yaml (queues.config[].max_concurrency) shared by many DAGs, and plans to add distributed workers later.

Verify: (1) every release AFTER 2.18.2 up to the latest: version, date, and changes touching queues, max_active_runs, distributed mode (coordinator, workers, worker_selector, drain on SIGTERM, dispatch hold when no worker), auth modes (basic vs builtin), webhooks and API keys; (2) breaking config changes or migrations between 2.18.2 and latest; (3) open or recently closed GitHub issues about queues dropping or duplicating runs, workers losing runs, or upgrade regressions; (4) whether a DAG can belong to more than one queue, or whether anything caps runs per (queue x label) in any version.

Deliver: a table (version | date | relevant change | source URL), a list of known bugs with issue links and status, then a 5-line verdict: stay on 2.18.2, or upgrade to which exact version before adding workers, and why. Mark anything unverified NOT FOUND; never guess version numbers. Under ~1,500 words.

Rules: public pages only, no login, no account, no purchase, no messages or comments to anyone. A link and read date for every fact. Say "unsure" rather than guess. End with **How I checked it** and **Unsure about**.

Delivery: reply in this chat with the full RESULT block: first line `RESULT dagu-upgrade-2x-20261026`, then the complete answer in Markdown (write every source as a full https:// link in plain text), last line `END dagu-upgrade-2x-20261026`. Also push `results/dagu-upgrade-2x-20261026/RESULT.md` to GitHub only if asked.
