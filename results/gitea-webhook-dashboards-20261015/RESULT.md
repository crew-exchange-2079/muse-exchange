# Self-hosted Gitea webhooks → personal dashboards & notifications

## Summary

- **Gitea's webhooks cover everything the scenario needs** — push, PRs, issues, labels, releases, and (on Gitea **1.25.0+**) Actions runs via a `workflow_run` webhook event. Deliveries are HMAC-SHA256 signed. The catch: **Gitea does not automatically retry failed deliveries** — recovery is a manual "Redelivery" click, so the receiving side has to be treated as lossy.
- **For notifications, ntfy is the standout.** A Gitea webhook can POST straight to an ntfy topic and ntfy will reformat the payload server-side with Go templates — no bridge program. Gotify cannot parse webhook payloads (needs a translator), Apprise is a fan-out sender rather than a listener, and **adnanh/webhook** is the generic receiver that fills the gaps (HMAC checking, field extraction, filtering). There is **no maintained purpose-built "Gitea → notification" relay**; the field is 0-star stubs.
- **For dashboards, only Homepage has a native Gitea widget** — and it shows counts (repositories / notifications / issues / pulls), not an activity stream. The practical activity wall is **Glance** (or Homarr) consuming Gitea's own built-in RSS/Atom feeds, or a custom-API widget against the Gitea REST API. Grafana's Gitea support is metrics-only.
- **Gitea Actions helps on the summary side, not the chaining side.** Cron-scheduled workflows exist (since 1.21.0), so a nightly digest can be a workflow that queries the API and posts to ntfy. But `workflow_run` is **not** an Actions trigger at any version — workflows cannot chain the GitHub way.
- Recommended minimal design (5 parts, §5): Gitea org/repo webhooks → ntfy with a custom template for the daily feed; one adnanh/webhook receiver that fires a high-priority ntfy alert only when the `needs-owner` label is applied; a nightly scheduled Actions workflow for the digest; Glance on the TV fed by Gitea's RSS feeds; optional Gatus for up/down status.

Versions/stars below were checked 2026-10-15/16 against the GitHub API and official docs.

## 1. Gitea webhooks: events, payloads, signing, delivery

Docs: [Webhooks](https://docs.gitea.com/usage/repository/webhooks/) and the [config cheat sheet](https://docs.gitea.com/administration/config-cheat-sheet/#webhook-webhook).

### Event types that matter here

Events are grouped in the UI as Repository, Issue, Pull Request, and Workflow events. The exact event names (these are the `X-Gitea-Event-Type` values):

| Want | Event type(s) | Notes |
|---|---|---|
| Pushes | `push` | Plus `create` / `delete` for branch & tag creation/deletion |
| PR opened / closed / merged | `pull_request` | No separate merge event; merges arrive as `pull_request` with `action: closed` (see below) |
| PR updated with new commits | `pull_request_sync` | Action `synchronized` |
| Issue opened / closed | `issues` | Actions: `opened`, `closed`, `reopened`, `edited`, `deleted` |
| Label added / removed | `issue_label`, `pull_request_label` | **Labeling is its own event type**, not an action on `issues`/`pull_request`. Actions: `label_updated`, `label_cleared` |
| Assignments | `issue_assign`, `pull_request_assign` | Actions `assigned` / `unassigned` |
| Comments | `issue_comment`, `pull_request_comment` | |
| Reviews | `pull_request_review_approved`, `pull_request_review_rejected`, `pull_request_review_comment` | |
| Releases | `release` | Actions `published`, `updated`, `deleted` |
| Commit status | `status` | No `action`; the state is in `state`: `pending`, `success`, `error`, `failure` |
| Packages | `package` | Actions `created`, `deleted` |
| **Actions workflow runs** | **`workflow_run`**, `workflow_job` | Actions `queued`, `waiting`, `in_progress`, `completed`. **`workflow_run` was added in Gitea 1.25.0** (PR #33964, listed in that release's API section) — on 1.21–1.24 there is no workflow-run webhook. `workflow_job` predates it; its introduction version was not confirmed from official sources |

**Header nuance that matters for filtering:** grouped sub-events are normalized in the `X-Gitea-Event` header (an assignment delivery carries `X-Gitea-Event: issues`), while `X-Gitea-Event-Type` carries the specific type (`issue_assign`). Filter on `X-Gitea-Event-Type`, or you'll misclassify label/assign/comment deliveries.

**Merged vs closed:** a `pull_request` delivery with `action: closed` covers both merged and abandoned PRs. The embedded `pull_request` object distinguishes them: it carries `merged` (boolean), `merged_at`, `merge_commit_sha`, and `merged_by` (verified in Gitea's source, `modules/structs/pull.go`). So "PR merged" = `action == "closed"` **and** `pull_request.merged == true`.

### Payload shape

- `push`: `ref`, `before`, `after`, `compare_url`, `commits`, `total_commits`, `head_commit`, `repository`, `pusher`, `sender`. No `action` field.
- `pull_request` / `issues`: `action`, `number`, the embedded `pull_request` / `issue` object, `repository`, `sender`, plus optional `changes`, `commit_id` (and `review` / `requested_reviewer` on PR events).
- Delivery headers: `X-Gitea-Delivery` (unique delivery UUID — the natural dedupe key), `X-Gitea-Event`, `X-Gitea-Event-Type`, `X-Gitea-Signature`, and `X-Gitea-Hook-Installation-Target-Type` (`repository` / `organization` / `user` / `system`). GitHub-style mirrors (`X-GitHub-Event`, `X-Hub-Signature-256`, …) are also sent, which is why GitHub-oriented tooling often works on Gitea payloads.
- Generic hooks support POST (JSON body, or a form field named `payload`) and GET. Deliveries are asynchronous.

### Signing and auth

- Set a **Secret** on the webhook and Gitea HMAC-signs the **raw body** with **HMAC-SHA256**. `X-Gitea-Signature` is the hex digest (lowercase, no prefix); `X-Hub-Signature-256` carries the same digest with a `sha256=` prefix; a legacy SHA1 `X-Hub-Signature` (`sha1=…`) is sent for GitHub compatibility.
- Receiver recipe per the docs: read the body exactly as received, compute HMAC-SHA256 with the secret, constant-time compare against the signature header — **before** parsing any JSON.
- If no secret is configured, the signature headers are still sent but with **empty digests** — a receiver that doesn't enforce a secret will accept anything. Set one.
- Alternative auth: each webhook can also send a custom **`Authorization` header** (added in Gitea 1.19.0, PR #20926), independent of the HMAC secret — handy for receivers that want a bearer token (e.g. an ntfy topic protected by an access token).

### Delivery behavior — the weak point

- Per-delivery HTTP timeout: `[webhook] DELIVER_TIMEOUT`, default **5 seconds**. Slow receivers will fail deliveries.
- Deliveries run through a queue (`QUEUE_LENGTH` default 1000); undelivered hook tasks persist in the database and are re-queued without double-delivery.
- **No automatic retry count or backoff is documented anywhere in the official docs or config reference** — there is no retry setting in the `[webhook]` section. What exists: a **Recent Deliveries** log on each webhook's page (request/response detail), a **Redelivery** action to replay a past delivery, and **Test Delivery** (sends a synthetic `push`).
- Practical consequence: if your receiver is down, events are effectively lost until you redeliver by hand. Designs should re-derive anything important from the API (the nightly digest in §5 does exactly this) instead of trusting the event stream as complete.

### Types and scopes

- Hook types: `Gitea` (generic JSON), `Gogs`, `Slack`, `Discord`, `Dingtalk`, `Telegram`, `Microsoft Teams`, `Feishu`, `Matrix`, `Wechatwork`, `Packagist`. The chat types pre-format the event for that service — so for Discord/Slack/Telegram/Matrix notifications, **no third-party tool is needed at all**.
- Scopes: per-repository, per-organization (all its repos), per-user, and system-wide. Admin-defined *default webhooks* are copied into new repositories. A single org-level generic webhook is the low-maintenance choice for a personal instance.
- Per-webhook options include target URL, method, content type, secret, authorization header, trigger selection, an Active flag, and a glob **branch filter** (only applies to ref-carrying events like `push`/`create`/`delete`).

## 2. Existing open-source tools

### (a) Notifications

| Tool | Role in this design | Gitea fit | Maintenance (2026-10-15/16) | License | Self-host |
|---|---|---|---|---|---|
| [ntfy](https://github.com/binwiederhier/ntfy) | Push server; phones/desktops subscribe to topics | **Best native fit.** Webhook POSTs directly to a topic URL; server-side *message templating* (`?template=…` or `X-Template`) reformats JSON payloads into title/message via Go templates. Built-in templates: `github`, `grafana`, `alertmanager`; custom template files supported | 34,848★, v2.31.0 (2026-10-15), very active | Apache-2.0 | Single Go binary or Docker; public ntfy.sh also exists |
| [Gotify](https://github.com/gotify/server) | Self-hosted message server (Android/web clients, WebSocket) | **Needs a translator.** Its API is `POST /message` with an app token and a `{title, message, priority}` body; it cannot parse arbitrary webhook JSON and has no templating | 16,073★, v3.1.1 (2026-09-15), active | MIT | Single Go binary or Docker |
| [Apprise](https://github.com/caronc/apprise) | Fan-out library/CLI: one call → dozens of services (Telegram, Discord, Slack, email, Gotify, ntfy, …) | **Sender, not a listener.** It doesn't receive webhooks or parse Gitea payloads; the companion [Apprise API](https://github.com/caronc/apprise-api) server accepts `POST /notify/` in Apprise's own schema. Needs something (adnanh/webhook, a script) in front of it | 17,589★, v2.0.1 (2026-10-03), active; apprise-api 1,324★, MIT | BSD-2-Clause | `pip install apprise`, or one Docker container for the API server |
| [adnanh/webhook](https://github.com/adnanh/webhook) | Generic webhook receiver daemon | **The adapter.** Listens on configured endpoints, validates HMAC trigger rules (`payload-hmac-sha256` etc. — matches Gitea's `X-Hub-Signature-256`), extracts payload fields, runs a local command with them (curl to ntfy, `apprise`, a script) | 12,185★, v2.8.3 (2026-02-12), maintained at a slower cadence | MIT | Single Go binary + one hooks config file; lightest footprint of the set |

**Dedicated Gitea/Forgejo webhook→notification relays: effectively none.** GitHub searches (`gitea ntfy`, `gitea notify`, `forgejo notify`) surfaced only stubs — e.g. karoyqiu/gitea-ntfy and karoyqiu/gitea-notify (0★, two-line READMEs), dreamw4lker/gitea-webhook-notifier (0★, dormant since 2022, push→email), bziemons/webhook-matrix-notifier (archived). One near-miss: jmitech/ntfy-action is a Gitea *Actions step* that sends an ntfy message from CI — useful inside workflows (§4), not a webhook relay.

Caveat on ntfy's built-in `github` template: it's documented against **GitHub** payloads (PRs, issues, stars, comments). Gitea payloads are GitHub-shaped, but whether the template covers Gitea's dialect unchanged is **UNVERIFIED** — ntfy's documented custom-template-file mechanism is the safe path, and it's what the design in §5 assumes.

### (b) Activity feeds & status pages

The substrate is **Gitea itself**: it serves RSS/Atom feeds natively (verified live against gitea.com):

- User/org activity: `/{user}.rss` / `/{user}.atom`
- Repo activity: `/{owner}/{repo}.rss` / `.atom`
- Repo releases and tags: `/{owner}/{repo}/releases.rss`, `/tags.rss`

(User-action feeds arrived via PR #16002; basic-auth support for feeds was added in Gitea 1.24, so widgets that can send credentials can read feeds on a private instance. Feeds can be disabled instance-wide with `[other] ENABLE_FEED`.)

For **status** (up/down, not activity): [Gatus](https://github.com/TwiN/gatus) (12,319★, Apache-2.0, v5.37.0 2026-09-24) monitors HTTP/TCP/DNS endpoints from one YAML file — point it at Gitea's `GET /api/healthz` (verified 200 on gitea.com), the radio stream, etc. It has native widgets in both Homepage and Homarr. Gitea-specific feed tools are a thin field: charlottecroce/giteabot (1★, Slack poster) and an obsolete pre-native-feeds RSS workaround script were all that surfaced. **There is no established dedicated "Gitea activity wall" tool** — the standard pattern is native feeds → a dashboard widget.

### (c) Dashboards

| Dashboard | Native Gitea support | Realistic activity path | Maintenance | License | Self-host |
|---|---|---|---|---|---|
| [Homepage](https://github.com/gethomepage/homepage) | **Yes — the only one.** Widget shows **counts**: `repositories`, `notifications`, `issues`, `pulls` (needs a Gitea API token) | Counts via the widget; stream via its generic `customapi` or RSS widgets | 33,167★, v2.5.0 (2026-10-10) | GPL-3.0 | Docker; YAML config files, no UI editor |
| [Glance](https://github.com/glanceapp/glance) | No Gitea widget (its Releases widget supports Codeberg, and its Repository widget is GitHub-only) | **Strong DIY:** RSS widget merging Gitea feeds; Custom-API widget with custom headers (`Authorization: token …`) + Go-template rendering against the Gitea API; Monitor widget for up/down | 37,516★, v0.8.7 (2026-10-15) | AGPL-3.0 | Lightest here: single <20 MB Go binary or small container, one YAML file |
| [Homarr](https://github.com/homarr-labs/homarr) | No (its 92 documented integrations include zero Gitea entries) | RSS Feed widget on Gitea feeds; Custom API widget on the REST API; iFrame widget; Gatus integration for status | 5,110★, v2.6.0 (2026-10-15) | Apache-2.0 | Docker; deliberately UI-configured (drag-and-drop, own database, built-in auth) — no YAML |
| [Dashy](https://github.com/Lissy93/dashy) | No (its widget docs contain zero Gitea mentions; its GitHub widgets are GitHub-only) | API-response / iframe widgets. **Caveat:** Dashy's RSS widget fetches via the third-party api.rss2json.com service — a poor fit for private/authenticated feeds | 26,719★, v4.8.0 (2026-10-09) | MIT | Docker; `conf.yml` + UI editor |
| [Grafana](https://github.com/grafana/grafana) | No OSS Gitea activity datasource exists; Grafana Labs' official Gitea integration is **metrics only** (scrapes Gitea's `/metrics` Prometheus endpoint; prebuilt dashboard of app/CPU/memory stats) | Prometheus on `/metrics` for health history; [Infinity datasource](https://grafana.com/grafana/plugins/yesoreyeram-infinity-datasource/) can query the Gitea REST API / feeds into tables | 77,301★, v13.2.4 (2026-10-13) | AGPL-3.0 | Docker; heaviest option — right-sized for metrics history/alerting, overkill for an activity feed |

## 3. From raw events to human-readable one-liners

**Templating — three layers, pick one:**
1. **At the notifier (least code):** ntfy server-side templates. Gitea POSTs to `https://ntfy/<topic>?template=<file>` and ntfy renders title/message from the payload's fields. A one-liner is just plain text; metadata rides in headers — `X-Title`, `X-Priority` (1–5), `X-Tags` (known names render as emoji, e.g. `warning` → ⚠️), `X-Click` (tap opens the PR/issue URL), `X-Markdown`.
2. **At a receiver:** adnanh/webhook's `pass-arguments-to-command` / `pass-environment-to-command` pull named payload fields (`pusher.name`, `head_commit.message`, `pull_request.html_url`…) into a small script that formats the line; with `-template`, the hooks file itself is a Go template (with a `getenv` helper for injecting the HMAC secret).
3. **At the sender:** if a workflow or script generates the message (digests, CI results), format it there and POST the finished line to ntfy/Gotify/Apprise.

Write lines from the *actor + verb + object + link* pattern — e.g. "ada merged PR #42 'Fix login redirect' in homelab/infra" — using `sender.login`, the event `action`, and the object's `html_url`. Key the verb off `X-Gitea-Event-Type` (not the normalized `X-Gitea-Event`), and special-case `pull_request` `closed` + `merged == true` → "merged".

**Dedupe:** use `X-Gitea-Delivery` (a per-delivery UUID) as the idempotency key in whatever receives/stores events — redeliveries and test deliveries then collapse instead of double-posting. ntfy also has an `X-Sequence-ID` header that lets a later message update/replace an earlier one (useful for "CI running…" → "CI passed" in place).

**Batching (so a busy day isn't spam):** no tool above has a built-in "digest mode" — this is a pattern, not a feature. The workable version: per-event messages go only to a low-priority **feed topic** (silent on the phone, readable in the ntfy app / on the dashboard), and a **scheduled job** (a Gitea Actions cron workflow, §4, or plain cron) reads the day's state back from the Gitea API and posts **one** digest line-set to a normal-priority topic at night. Deriving the digest from the API — not from stored webhook events — also makes it immune to lost deliveries (§1).

**Quiet hours:** neither ntfy nor Gotify documents a server-side quiet-hours feature. The citable primitives: send at a priority clients treat as silent (ntfy priorities 1–2 are silent; Gotify priority 0 shows no notification, 1–3 icon only, 4–7 sound, 8–10 sound+vibration — the priority is set at push time, so the *sender* enforces quiet hours), or hold delivery with ntfy's `X-Delay` header (accepts durations/timestamps/natural language like "tomorrow, 3pm"; min 10 s, max 3 days). Client-side DND schedules on the phone are the other half.

## 4. Gitea Actions tricks

Docs: [Actions comparison](https://docs.gitea.com/usage/actions/comparison), [secrets](https://docs.gitea.com/usage/actions/secrets/), [token permissions](https://docs.gitea.com/usage/actions/token-permissions), [runner labels](https://docs.gitea.com/runner/labels/).

- **Scheduled workflows: yes, since Gitea 1.21.0** (PR #26655). Syntax mirrors GitHub (`on: schedule: - cron: '30 5 * * 1,3'`), `github.event.schedule` distinguishes which cron line fired, and Gitea additionally accepts `@yearly` / `@monthly` / `@weekly` / `@daily` / `@hourly`. **Caveat: schedules only fire from the repository's default branch.** No documented minimum interval or delay guarantee (an every-minute cron was observed firing in a bug report, so there's no GitHub-style 5-minute floor in practice — but don't build anything that needs minute precision).
- **`workflow_run` trigger: NOT supported.** A maintainer has stated `on: workflow_run` "is currently not supported" (future plans only); independent checks against 1.22.x confirm it. The GitHub pattern "run workflow B when workflow A finishes" does not port. Workarounds: react to the `workflow_run` **webhook event** (1.25+, §1) with an external receiver, poll the runs API from a scheduled workflow, or use reusable workflows (`workflow_call`, which does exist) to compose jobs inside one run.
- **Calling out from a workflow is just a shell step:** nothing restricts `run:` steps from outbound HTTP, so `curl -H "Title: …" -d "…" https://ntfy/<topic>` (or POSTing to a webhook/Apprise) works as-is; ready-made steps exist (e.g. an ntfy action for Gitea Actions). Keep the ntfy/topic credentials in secrets.
- **Secrets:** defined at user, organization, or repository level (since 1.19; repo wins name collisions), referenced as `${{ secrets.NAME }}`; names can't start with `GITHUB_`/`GITEA_` and are case-insensitive.
- **The automatic token:** every job gets `GITEA_TOKEN` (`${{ secrets.GITEA_TOKEN }}` / `${{ gitea.token }}`) for Git-over-HTTP and API calls — enough for a digest job reading its own repo's issues/PRs/runs. Permissions follow the GitHub-style `permissions:` model with Gitea scopes (`contents`, `issues`, `pull-requests`, `actions`, …); instance default mode is "Permissive" (read/write on the job's own repo) or "Restricted" (read-only). Gotchas: workflows from **fork PRs always get a read-only token** and never reach other private repos; by default the token reaches only its own repo (+ public repos read-only) unless cross-repo access is enabled; and `GITEA_TOKEN` **cannot publish to the package registry** — use a personal access token stored as a secret for that.
- **Runners (act_runner / "Gitea Runner"):** labels are `<name>[:<schema>[:<args>]]` — `docker` with an image arg (e.g. `ubuntu-latest:docker://docker.gitea.com/runner-images:ubuntu-latest`) or `host`; jobs select via `runs-on`, first label match wins. Labels are set at registration (`--labels`, stored in `.runner`) and later editable via config file or the UI. `runner.capacity` (default 1) caps concurrent jobs; default job timeout 3 h. There is **no documented "scheduled-jobs-only" runner mode** — the practical build is a repo-scoped registration token (runner serves only that repo) plus a unique label that only the scheduled workflows request. Ephemeral runners (`--ephemeral`, one job then exit) are typically launched from the `workflow_job` webhook.

## 5. Recommended minimal design — and the 3 biggest pitfalls

Scenario targets: a daily plain-English activity feed, a nightly summary, instant phone alerts **only** for `needs-owner` items, and an ambient TV board.

**Components (5):**
1. **Gitea** — one organization-level (or per-repo) generic webhook with a secret set, pointed at ntfy; a second webhook pointed at the alert receiver (or one webhook to the receiver, which fans out — see 3).
2. **ntfy (self-hosted)** — two topics: `feed` (every event, low priority, silent) rendered by a **custom template file** into one-liners; `alerts` (high priority). ntfy is the phone app, the searchable history, and the feed source of record.
3. **adnanh/webhook (one small receiver)** — verifies the HMAC, and its trigger rule fires **only** when `X-Gitea-Event-Type` is `issue_label`/`pull_request_label` and the payload's label is `needs-owner`; the command curls a high-priority message to ntfy's `alerts` topic. (ntfy templating formats messages but doesn't filter by label — filtering is the one job that genuinely needs this receiver.) If the chat apps are enough, Gitea's built-in Discord/Slack/Telegram hook types can bypass 2–3 for those channels.
4. **A nightly digest workflow** — an `on: schedule` cron workflow in a small ops repo (default branch!) that uses `GITEA_TOKEN` to query the day's issues/PRs/Actions runs from the API and POSTs one summary to ntfy. API-derived, so it doubles as the safety net for lost webhook deliveries.
5. **Glance on the TV/tablet** — RSS widget merging the org/user and key repo feeds (ambient activity), a Monitor widget for Gitea health, optionally a Custom-API widget for open-PR / `needs-owner` counts. (Homepage instead if simple counts suffice; add Gatus if a real status page is wanted.)

**The 3 biggest pitfalls:**
1. **Version traps around Actions.** `workflow_run` exists only as a *webhook event* and only from **Gitea 1.25.0**; as an *Actions trigger* it doesn't exist at all, and cron workflows silently do nothing if the workflow file isn't on the default branch. Check your Gitea version before designing anything CI-reactive — most blog posts assume GitHub semantics.
2. **Lost events.** No documented automatic retries, a 5-second delivery timeout, and empty signatures if you forget the secret. Mitigate: short/fast receivers, dedupe on `X-Gitea-Delivery`, enforce the HMAC, and make the nightly digest API-derived so a dead receiver degrades the feed, not the record.
3. **Noise and mis-filtering.** Firing a phone alert per raw event guarantees alert fatigue within a week; and the two easiest filters are both wrong — `X-Gitea-Event` is normalized (label events hide under `issues`/`pull_request`), and PR `closed` ≠ merged. Filter on `X-Gitea-Event-Type` + payload fields (label name, `pull_request.merged`), keep the firehose on a silent topic, and reserve push priority for the label.

## Sources

- Gitea docs — Webhooks: https://docs.gitea.com/usage/repository/webhooks/
- Gitea docs — Config cheat sheet (`[webhook]`): https://docs.gitea.com/administration/config-cheat-sheet/#webhook-webhook
- Gitea 1.25.0 release notes (`workflow_run` webhook, PR #33964): https://github.com/go-gitea/gitea/releases/tag/v1.25.0
- Gitea PR #20926 (webhook authorization header, shipped 1.19.0): https://github.com/go-gitea/gitea/pull/20926
- Gitea source — `PullRequest` struct (`merged`, `merged_at`, …): https://github.com/go-gitea/gitea/blob/main/modules/structs/pull.go
- Gitea docs — Actions comparison with GitHub: https://docs.gitea.com/usage/actions/comparison
- Gitea docs — Actions secrets: https://docs.gitea.com/usage/actions/secrets/ · Token permissions: https://docs.gitea.com/usage/actions/token-permissions
- Gitea docs — Runner: https://docs.gitea.com/runner/ · Labels: https://docs.gitea.com/runner/labels/ · Registration: https://docs.gitea.com/runner/registration/ · Configuration: https://docs.gitea.com/runner/configuration/
- Gitea PR #26655 (cron schedule support, 1.21.0): https://github.com/go-gitea/gitea/pull/26655 · PR #38154 discussion (`workflow_run` trigger unsupported): https://github.com/go-gitea/gitea/pull/38154
- ntfy docs (publish, message templating, install): https://github.com/binwiederhier/ntfy/blob/main/docs/publish.md · https://docs.ntfy.sh/publish/
- Gotify docs (push messages, priority): https://github.com/gotify/website/blob/HEAD/docs/pushmsg.md · https://github.com/gotify/website/blob/HEAD/docs/priority.md
- Apprise / Apprise API: https://github.com/caronc/apprise · https://github.com/caronc/apprise-api
- adnanh/webhook (README, hook rules, hook definition): https://github.com/adnanh/webhook
- Homepage Gitea widget: https://gethomepage.dev/widgets/services/gitea/ · Homarr integrations/widgets: https://homarr.dev/docs/integrations/ · https://homarr.dev/docs/widgets/rss-feed/
- Glance configuration/widgets: https://github.com/glanceapp/glance/blob/HEAD/docs/configuration.md · Dashy widgets: https://github.com/Lissy93/dashy/blob/master/docs/widgets.md
- Grafana Gitea integration (metrics): https://grafana.com/docs/grafana-cloud/observe-and-act/monitor-infrastructure/integrations/integration-reference/integration-gitea/ · Infinity datasource: https://grafana.com/grafana/plugins/yesoreyeram-infinity-datasource/
- Gatus: https://github.com/TwiN/gatus
- Repo metadata (stars, releases, licenses) via https://api.github.com/repos/<owner>/<repo> for each project named above

## How I checked it

- Webhook facts (events, headers, signing, delivery, types) were taken from the official Gitea docs pages and the 1.25.0 release notes, not from blog posts.
- The merged-vs-closed distinction was verified directly in Gitea's source (`modules/structs/pull.go`: `HasMerged bool json:"merged"`, `merged_at`, `merge_commit_sha`, `merged_by`).
- Tool facts (what each does, license, maintenance) come from each project's own docs/README plus live GitHub API metadata (stars, archived flag, latest release, last push) fetched 2026-10-15/16.
- Gitea's native feeds and the `/api/healthz` endpoint were verified live against the public gitea.com instance (HTTP 200 with feed content).
- Dashboard "native Gitea support" claims were checked against each project's official widget/integration documentation (including negative checks — e.g. searching Homarr's and Dashy's full widget docs for any Gitea entry).

## Unsure about

- **Automatic retries:** no retry count/backoff for failed deliveries is documented in the official docs or config reference reached. Absence of documentation is not proof no retry exists in code — only that none is documented/configurable.
- **`workflow_job` webhook introduction version:** it predates 1.25.0 (that release only changed its payload URL format); the exact version was not confirmed from official sources.
- **ntfy's built-in `github` template on Gitea payloads:** documented against GitHub payloads. Gitea's are GitHub-shaped, but field-for-field coverage is unverified — a custom template file is the documented fallback and is what §5 assumes.
- **Gitea secrets on fork-PR workflows / log masking:** the Gitea docs reached don't state whether user-defined secrets are withheld from fork-PR workflows or masked in logs (the always-read-only rule for fork-PR *tokens* is documented). Don't assume GitHub's documented behavior carries over.
- **Scheduled-workflow timing guarantees:** no documented minimum interval or delay bound; the every-minute observation comes from a bug report, not a spec.
- **Per-file / branch RSS feeds** (`/rss/branch/{branch}`): documented only in a third-party inventory; a live test returned a redirect rather than feed XML, so treat those specific feed URLs as partially verified. User/org/repo/releases/tags feeds are fully verified.
