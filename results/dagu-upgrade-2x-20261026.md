RESULT dagu-upgrade-2x-20261026

# Dagu 2.18.2 → later: stay or upgrade before adding distributed workers?

Read date for every fact: 2026-10-26. Anchor: v2.18.2 was published 2026-10-04. Latest release at read time: v2.23.0, published 2026-10-26. The release chain between them is complete with no gaps: v2.18.2 → v2.19.0 → v2.19.1 → v2.19.2 → v2.20.1 → v2.21.0 → v2.22.0 → v2.22.2 → v2.22.3 → v2.22.4 → v2.23.0. Two tags were never published as releases and are not upgrade targets: v2.20.0 ("tagged but not published, so v2.20.1 is the first v2.20 release") and v2.22.1 ("tagged but not published, so v2.22.2 is the first release after v2.22.0"). Note: the repo org now reads dagucloud/dagu; dagu-org/dagu URLs redirect to it.

## Release table (only changes touching queues, max_active_runs, distributed mode, auth, webhooks, API keys)

| Version | Date (UTC) | Relevant change | Source |
|---|---|---|---|
| v2.19.0 | 2026-10-11 | Worker stops gracefully on SIGINT and SIGTERM (#3035) — the drain fix 2.18.2 lacks. Coordinator idle-poll churn cut, incl. standby lease retry (#3055, fixing report #3034). No queue, auth, webhook, or API-key changes in this release. | https://github.com/dagu-org/dagu/releases/tag/v2.19.0 |
| v2.19.1 | 2026-10-12 | No queue/distributed/auth/webhook/API-key changes (thinking-effort mapping, browser TLS certs, relative times; "drop run events from periods below runs on restart" #3127). | https://github.com/dagu-org/dagu/releases |
| v2.19.2 | 2026-10-12 | No relevant changes (free plan treated as monitoring-only #3138; Windows process and PowerShell fixes). | https://github.com/dagu-org/dagu/releases |
| v2.20.1 | 2026-10-14 | Overview alerts for a stopped scheduler holding back scheduled/queued runs (#3162) and for queues whose runs cannot start because no healthy worker matches their selector, none is available, or runs cannot be handed to a worker (#3179). Per-DAG webhooks can get a public URL through Dagu Cloud (#3164); server processes sharing a data directory now keep one webhook per DAG (#3174). | https://github.com/dagu-org/dagu/releases |
| v2.21.0 | 2026-10-18 | Distributed execution, the big one: per-run `workerSelector` on start and enqueue (#3197); coordinator holds a dispatch until a matching worker registers, up to `coordinator.worker_wait_timeout` (default 2m) (#3198). Scheduler on a shared volume (NFS/EFS/CephFS) picks up DAG changes made through another host's UI/API (#3170, #3225). Dirlock: only one contender takes over a stale lock (#3185). `start-all` stops as a whole on SIGHUP/SIGQUIT (#3201). Dagu credential settings (auth secrets, encryption key, vault token) no longer reach step environments; a DAG must request them via `secrets` with `provider: env` (#3222). | https://github.com/dagu-org/dagu/releases |
| v2.22.0 | 2026-10-22 | Auth behavior change: requests needing no login (`auth.mode: none`, and `POST /api/v1/auth/setup`) now get HTTP 400 for an unrecognized `Host` — add public/custom domains to `allowed_hosts` / `DAGU_ALLOWED_HOSTS` (#3232). Workspace settings deprecated, removal in v3.0 (#3282, #3288). Scheduler `wake_hold` holds the first tick after the host wakes from sleep (#3270). UI sends the login page to the dashboard without built-in auth (#3247). No queue-cap or worker-dispatch changes. | https://github.com/dagu-org/dagu/releases |
| v2.22.2 | 2026-10-23 | Distributed sub-DAG runs dispatched to a worker no longer log two `stale attempt: lease no longer active` warnings on completion; worker shares the scheduler log writer with dispatched sub-DAG runs (report #3297, fix #3298). | https://github.com/dagu-org/dagu/releases |
| v2.22.3 | 2026-10-25 | No relevant changes (browser/computer-step fixes; `dagu config --values` #3252). | https://github.com/dagu-org/dagu/releases/tag/v2.22.3 |
| v2.22.4 | 2026-10-26 | No relevant changes (only "bound the browsers open at once on a host" #3323). | https://github.com/dagu-org/dagu/releases/tag/v2.22.4 |
| v2.23.0 | 2026-10-26 | Latest. Published changelog lists only one change: "fix flaky write gate tests" (#3342) — a test fix, no runtime change vs v2.22.4. | https://github.com/dagu-org/dagu/releases/tag/v2.23.0 |

No API-key feature changes were found in any release note in this range; API keys exist as a feature of `builtin` auth mode in current docs (Bearer token, `POST /api-keys`), but the version that introduced them was NOT FOUND in this search. No basic-vs-builtin mode change was found in range beyond the v2.22.0 items above.

## Breaking config changes / migrations between 2.18.2 and latest

- `queues.config[].max_concurrency` carries over unchanged. Current config code has `maxConcurrency` as the queue key and marks queue-level `maxActiveRuns` as deprecated in favor of it — https://pkg.go.dev/github.com/dagu-org/dagu@v1.30.3/internal/common/config — so the team's existing key is the canonical one, not the deprecated one. No rename to apply.
- DAG-level `max_active_runs` is a different field and does NOT coordinate across workers: it is deprecated for local queues and ignored in distributed setups — "Use a global queue with 'queue:' field for concurrency control" — https://deepwiki.com/dagu-org/dagu/6.5-ssh-executor . Before adding workers, move any DAG-level `max_active_runs` limits into named queues.
- If the server runs `auth.mode: none` behind a reverse proxy with a custom Host, add `allowed_hosts` (v2.22.0, #3232) or no-login requests get HTTP 400.
- Workspace settings are deprecated and will be removed in v3.0 (v2.22.0, #3282) — move off them before any v3 upgrade; they are not removed in v2.23.0.
- v2.20.1: a load-more cursor issued by the old version for `GET /event-logs` returns 400 once after upgrade; refreshing clears it. No data-directory or queue-state migration steps were published in the release notes in range.

## Known bugs with issue links and status

- Worker did not stop gracefully on SIGINT/SIGTERM — present in 2.18.2, FIXED in v2.19.0: "fix(worker): stop gracefully on SIGINT and SIGTERM" (#3035) — https://github.com/dagu-org/dagu/releases/tag/v2.19.0 . This is the single most worker-relevant bug in range: on 2.18.2, killing a worker is not a graceful drain.
- Distributed sub-DAG runs logged duplicate `stale attempt: lease no longer active` warnings on completion — FIXED in v2.22.2 (report #3297, fix #3298) — https://github.com/dagu-org/dagu/releases . Log noise, not lost runs, per the fix description.
- Coordinator idle-poll churn (~1 wake/s per worker) — FIXED in v2.19.0 (report #3034, fix #3055) — https://github.com/dagu-org/dagu/releases/tag/v2.19.0 .
- Queues that cannot start had no UI alert before v2.20.1 — MITIGATED in v2.20.1 by the stuck-queue alert (#3179) — https://github.com/dagu-org/dagu/releases . A queue blocked on no matching worker is now visible instead of silent.
- Currently-open issues about queues dropping/duplicating runs, workers losing runs, or upgrade regressions: NOT FOUND in this search (searched GitHub issues and release notes; absence here is not proof none exist).

## Can a DAG belong to more than one queue? Is there a per-(queue x label) cap?

- No to multi-queue: a DAG carries a single `queue` field — "Queue is the name of the queue to assign this DAG to" (`Queue string`) — https://pkg.go.dev/github.com/dagu-org/dagu@v1.24.6/internal/core . One DAG, one queue.
- No per-(queue x label) cap was found in docs or release notes (NOT FOUND as a feature). The caps that exist are: per-queue `maxConcurrency` across all DAGs in that queue; per-worker `--worker.max-active-runs` (default 100) — https://docs.dagu.sh/getting-started/cli ; and per-DAG `workerSelector` label matching (a routing rule, not a cap) — https://pkg.go.dev/github.com/dagu-org/dagu@v1.24.6/internal/core . To cap one label class, give it a dedicated queue or a dedicated worker pool with matching labels.
- Related safety net, current design: scheduled distributed runs are persisted with status QUEUED before any dispatch attempt, and the queue handler retries dispatch without re-enqueueing, so a coordinator/worker outage does not lose or duplicate the item — https://pkg.go.dev/github.com/dagu-org/dagu@v1.24.0/internal/service/scheduler .

## Verdict

1. Upgrade, do not stay on 2.18.2: it predates both the worker graceful-stop fix (v2.19.0) and the dispatch-hold-until-a-matching-worker feature (v2.21.0), which the worker plan directly depends on.
2. Upgrade to exactly v2.23.0: it contains every fix above, and its published changelog vs v2.22.4 is a test-only change, so it adds no new runtime risk over v2.22.4.
3. Caveat: v2.23.0 was published today (2026-10-26); if house policy demands a soak window, v2.22.4 is the runtime-equivalent pick, but its only difference from v2.23.0 is that test fix.
4. Before adding workers: keep `queues.config[].max_concurrency` as-is, move any DAG-level `max_active_runs` limits into named queues, set `coordinator.worker_wait_timeout` deliberately (default 2m), and set `allowed_hosts` if running `auth.mode: none` behind a proxy.
5. After upgrading, prove it before real load: a worker SIGTERM drain test, a no-matching-worker dispatch-hold test, and a queue-cap test — then put DAGs on workers.

## How I checked it

- Read date for all facts: 2026-10-26. Public web only; no login, account, purchase, or messages to anyone.
- Primary sources first: the GitHub releases listing at https://github.com/dagu-org/dagu/releases (read in full from v2.22.3 down through v2.19.1), individual release tag pages for v2.19.0, v2.22.4, and v2.23.0, and the GitHub API release records for the same repo (used only for `published_at` dates, which the HTML text fetch drops; every tag/date pair above was cross-checked against the tag page or the listing's compare ranges).
- Completeness check: the compare ranges chain without gaps (v2.18.2...v2.19.0, v2.19.0...v2.19.1, v2.19.1...v2.19.2, v2.19.2...v2.20.1, v2.20.1...v2.21.0, v2.21.0...v2.22.0, v2.22.0...v2.22.2, v2.22.2...v2.22.3), confirming no app release was missed between 2.18.2 and latest; Helm chart releases (e.g. helm-dagu-2.0.5) are packaging-only and excluded.
- Docs and code checked for config semantics: graceful-shutdown behavior at https://docs.dagu.sh/server-admin/operations , worker CLI flags at https://docs.dagu.sh/getting-started/cli , queue/worker-selector semantics via the DAG struct at https://pkg.go.dev/github.com/dagu-org/dagu@v1.24.6/internal/core and the queue config struct at https://pkg.go.dev/github.com/dagu-org/dagu@v1.30.3/internal/common/config .
- Nothing was pushed to GitHub and nothing was written to any repo, per the task rules.

## Unsure about

- Currently-open queue/worker issues: NOT FOUND in this search — this is a search limitation, not proof the tracker is clean.
- The version that introduced API keys: NOT FOUND in the release notes in range.
- Exact worker-drain semantics of fix #3035 beyond its title ("stop gracefully on SIGINT and SIGTERM"): the published docs' graceful-shutdown section covers `start-all`/`server`/`scheduler` signal propagation, not worker drain internals, so drain-waits-for-in-flight-runs vs drain-stops-accepting-new-tasks is unverified — test it after upgrading (verdict line 5).
- Whether v2.23.0 contains anything beyond its single listed changelog commit: the published notes list only the test fix; no other change is claimed here.

END dagu-upgrade-2x-20261026
