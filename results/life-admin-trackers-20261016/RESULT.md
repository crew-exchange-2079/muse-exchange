# Self-hosted task trackers for agent-run "life admin" — comparison & recommendation

## Summary

- **Recommendation: Vikunja** for the errand/life-admin side, with Gitea kept for code. Vikunja is the only candidate that natively covers the three things errands need and code trackers lack — **recurring tasks, per-task reminders (multiple, relative to the due date), and a real "next action" date model** — while also giving agents a first-class token API and webhooks, in a **single container** with SQLite, with **every feature free** (AGPL-3.0, no open-core paywall). Its one structural gap is **no custom fields**, so "waiting on" and "outcome" are modelled with labels + a comment convention (§4) instead of typed fields.
- **Runner-up / zero-new-infrastructure option: Gitea issues + conventions.** Gitea has scoped API tokens, due dates, dependencies, and scoped labels — but **no reminders, no recurrence, and no custom fields** (the custom-fields request, #18210, has been open since 2022; earlier ones were closed as not planned). Choosing Gitea means the agent team itself becomes the reminder/recurrence engine via a scheduled scan. That's viable — the agents are already scheduled software — but it's machinery you own forever.
- **OpenProject** has the best data model for errands (free custom fields, per-item reminders, date alerts — free since v17.9) but is the heaviest thing here (PostgreSQL 16+, ≥4 GB RAM, Rails suite) and has no recurring tasks. Right if custom fields are non-negotiable; overkill for one person's errands.
- Avoid for this split: **Plane CE** (reminders and custom properties are paid tiers, the official mobile app doesn't work with free self-hosted instances, telemetry is on by default), **standalone Focalboard** (officially unmaintained since 2024), **Taiga** (capable, but a ~7-service stack with telemetry on by default), **Nextcloud Deck** (only sensible if Nextcloud is already running; no custom fields, no recurrence, webhooks not yet native).

All facts checked 2026-10-15/16 against official docs and the GitHub API.

## 1. At-a-glance (free self-hosted tiers)

| Capability | Vikunja | Gitea issues | OpenProject CE | Plane CE | Taiga | Kanboard | Nextcloud Deck | Focalboard / MM Boards |
|---|---|---|---|---|---|---|---|---|
| Agent API + token | ✅ REST v1/v2, per-user API tokens (Bearer) | ✅ REST, scoped PATs (since 1.20) | ✅ API v3, `apikey` Basic / OAuth2 | ✅ REST, `X-API-Key`, 60 req/min | ✅ REST, app tokens | ✅ JSON-RPC, app + user tokens | ✅ REST, app passwords / OAuth2 | ✅ REST v2, Mattermost tokens |
| Outgoing webhooks | ✅ project + user level, ~21 events, **no retries** | ✅ repo/org/system, issue events | ✅ project-scopable | ✅ workspace-level, retries | ✅ per project, with logs/resend | ✅ one global URL, ~19 events | ❌ not in Deck (Nextcloud 30 `webhook_listeners` + a Deck PR — merge unverified) | ❌ none found for board events |
| Due dates | ✅ | ✅ `deadline` field | ✅ start/finish | ✅ | ✅ | ✅ (+ start) | ✅ (+ start since 1.18) | ⚠️ generic Date property |
| Reminders | ✅ **per-task, multiple, relative**; email + UI; daily overdue summary | ❌ none — display + overdue flag only | ✅ per-item reminders (15.2+) + date alerts (free since 17.9) | ❌ project-level only, **paid** | ⚠️ not found in docs (UNVERIFIED) | ⚠️ overdue-only via daily cron | ✅ per-board due notifications | ❌ none found |
| Recurring tasks | ✅ **native repeat rules**, next occurrence on completion | ❌ (pattern: cron + API) | ❌ | ❌ | ❌ none found | ⚠️ native but event-triggered duplication, not calendar rules | ❌ | ❌ |
| Custom fields | ❌ labels/priority/relations only | ❌ labels + body only | ✅ **free**, many types, API-settable | ❌ **paid (Pro)** | ✅ custom attributes per project | ⚠️ arbitrary KV metadata on tasks | ❌ | ✅ rich card properties |
| Hosting weight | **1 container**, SQLite OK | already running | heaviest: PG16+, ≥4 GB, multi-service | ~12 containers, ≥4 GB | ~7 services (PG, RabbitMQ…) | **lightest**: PHP + SQLite, 1 image | needs a full Nextcloud | standalone unmaintained; or full Mattermost |
| License | AGPL-3.0 | MIT (Gitea) | GPL-3.0 + EE add-ons | AGPL-3.0 + paid tiers | MPL-2.0 | MIT | AGPL-3.0 | mixed (official binaries MIT) |
| Human's mobile app | ⚠️ official app is alpha (Android beta; iOS effectively unsupported); web UI works | ✅ Gitea apps exist; web UI | ✅ official app | ❌ **not for free self-hosted CE** | ⚠️ unofficial app only | ❌ none official | ✅ maintained Android app (community) | via Mattermost app |
| Telemetry default | none documented | none | UNVERIFIED | **on, opt-out** | **on, opt-out** | none found | none in Deck | standalone default on |
| Maintenance (Oct 2026) | 5,756★, v2.7.0 (2026-10-02), active | — | 16,435★, v17.9.2, very active | 60,905★, v1.4.2, very active | 857★ (back), 6.10.2, active | 9,907★, v1.2.54, active | 1,427★, v1.18.x, very active | standalone **unmaintained**; plugin active |

## 2. Per-tool notes (what decides it for errands)

**Vikunja** — Built as a to-do app, which is exactly the shape of life admin: projects/lists per life area, tasks with due dates, **multiple reminders per task (absolute or relative: "2 days before due")**, and **calendar-style repeat rules** that spawn the next occurrence when the current one is completed — bills and "call the office monthly" just work. Agent story is clean: per-user **API tokens** (Bearer), REST v1 (Swagger UI) and v2 (OpenAPI 3.1) APIs, **webhooks at project and user level** (~21 events, HMAC-SHA256 signed). Two webhook caveats: deliveries are **sent once with no retries** (30 s timeout), and the built-in SSRF guard blocks private-network targets by default — if your webhook receiver lives on the LAN, that's a config flag, not a surprise to debug later. No custom fields: "waiting on" is a label, "outcome" is a label + comment (§4). Official mobile app is alpha/Android-beta with iOS effectively unsupported — the human uses the web UI (installable as a PWA) or a third-party app. Sources: docs.vikunja.io (API, webhooks), GitHub API.

**Gitea / Forgejo issues** — Better than its reputation for this: real `deadline` field on issues (date-only, normalized to end of day), milestones with their own due dates, **native issue dependencies** (blocks/blocked-by, API-managed), multiple assignees, time tracking, YAML issue forms, and **scoped labels** (`waiting/…`, `outcome/…`) that enforce one value per scope — the closest thing to fields Gitea has. The API is deep (67 issue-group operations in the 1.22 docs) with **scoped personal access tokens** (`write:issue` is enough for an errand agent) and HMAC-signed webhooks. The three hard gaps, all verified: **no deadline reminders anywhere** (no notification, no webhook event — an external poller must read `deadline`), **no recurrence**, **no custom fields and no priority field** (binary open/closed status; workflow state lives in labels or board columns). Sources: docs.gitea.com (labels, webhooks, API, OAuth2 scopes), issue #18210.

**OpenProject** — The data-model winner: **custom fields are a free Community feature** (text, list, date, user, … — settable via API, scopable per type/project), work-package **reminders per item** since v15.2, and **date alerts** (approaching start/finish, recurring overdue alerts) that moved from Enterprise into the free edition in v17.9 (2026-09). API v3 (HAL+JSON, OpenAPI spec, `apikey` Basic auth or OAuth2), project-scoped webhooks, official mobile app. Costs: the heaviest install here (PostgreSQL 16+ required, quad-core/4 GB official minimums, Rails + worker + scheduler), **no recurring tasks** (external cron + API is the documented workaround), and a permanent Enterprise upsell surface (the official MCP server's write support is a Professional-tier add-on). Sources: openproject.org docs (system requirements, API, editions), GitHub API.

**Plane** — The polished one, and the wrong deal for self-hosting this use case: due-date **reminder automations are a paid "Business" feature** and **custom work-item properties are Pro** — the two errand features are exactly what's paywalled. The **official mobile apps don't connect to free self-hosted CE** (Cloud and Commercial Edition only). Self-hosted telemetry is **on by default** (admin name/email, instance ID, usage data; opt-out in God Mode). ~12 containers, 4 GB minimum. The API itself is good (180+ endpoints, `X-API-Key` tokens, 60 req/min/key cap, workspace-level webhooks with retry/backoff, an official MCP server) — if the team were paying for Plane anyway it'd compete, but as a free self-host it fails the brief. Sources: developers.plane.so / docs.plane.so (automations, mobile, telemetry), GitHub API + issue #6392.

**Taiga** — A real contender on features: full REST API with **dedicated Application Tokens** for service accounts, native per-project **webhooks with delivery logs and resend**, and **per-project custom attributes** on tasks/issues/stories — "waiting on" and "outcome" model natively. But: **no recurrence** found, a reminder-before-due feature was not found in the API reference (UNVERIFIED), the production stack is ~7 services (PostgreSQL, RabbitMQ, events/async/protected), **telemetry is on by default** (`ENABLE_TELEMETRY=True`, opt out in config), and there's no official mobile app (an unofficial one exists). MPL-2.0. Sources: docs.taiga.io (API, production setup), GitHub API.

**Kanboard** — The minimalist's option. Single PHP app, SQLite by default, one Docker image — the lightest thing here. Its **JSON-RPC API** is complete and agent-friendly (application token with full access, or per-user tokens), outgoing webhooks cover ~19 task/comment/subtask events (one global URL; receivers must answer in <1 s), and tasks carry **arbitrary key–value metadata** via API — `waiting_on` and `outcome` fit there, with tags/categories/columns for the rest. Recurrence exists but is **event-triggered duplication** (a fresh copy when the task leaves the first column / reaches the last / is closed), not "every 2nd Tuesday" — fine for "when I finish this, start the next round," wrong for calendar bills. Reminders are **overdue-only** via a daily cron mailer (before-due nudges need plugins). No official mobile app. MIT. Sources: docs.kanboard.org (API, webhooks, cronjob, recurring tasks), GitHub API.

**Nextcloud Deck** — Only enters the conversation if a Nextcloud server already exists (then marginal cost is ~zero and cards also surface in Nextcloud Calendar/search). REST API with app-password/OAuth2 auth is decent; **due-date notifications exist** (per-board `notify-due` setting). But **no custom fields**, **no recurring cards** (both are open, popular feature requests), and **Deck itself has no outgoing webhooks** — Nextcloud 30's `webhook_listeners` app plus a Deck PR to make card events webhook-compatible is the path, and the PR's merge/release status was **not verified**. Dedicated Android app is community-maintained and good. AGPL-3.0. Sources: github.com/nextcloud/deck (API docs, issues #6859/#7791, PR #7910), GitHub API.

**Focalboard / Mattermost Boards** — Two different things wearing one name. **Standalone Focalboard is officially unmaintained**: the repo moved to the mattermost-community org and its README has carried "This repository is currently not maintained" since 2024-08-28 — do not adopt it for new work. The living product is **Boards as a Mattermost plugin** (bundled since Mattermost v6.0), which means running a full Mattermost server. On features it's mixed: the **richest card-property model** here (text/number/select/date/person/… properties, which are also the kanban group-by) and Mattermost's mature token API — but **no board-event webhooks, no due reminders, no recurrence** found in official docs. Sources: github.com/mattermost-community/focalboard (README), mattermost-plugin-boards, focalboard.com guides.

**Plain markdown-in-git** — The credible minimalist baseline, with real prior art: the **todo.txt format** (one task per line; `(A)` priority, `+project`, `@context`, `due:YYYY-MM-DD` key:value tags), **git-issue** (one directory per issue inside a git repo; separate small files for description/due date/comments — per-task files keep merge conflicts rare), and **Taskwarrior's data model** as the design reference — it natively has exactly the fields errands want (`due`, `scheduled`, `wait`, `until`, `recur`, dependencies, user-defined attributes). Trade-offs are structural: git history is a perfect audit trail and hosting cost is zero (it rides the existing forge/repo), but **nothing reminds** — an agent or CI must scan dates and act; forge webhooks fire on `push`, not on "this task's date changed," so the agent diffs to learn anything; and single-file formats conflict under concurrent edits. As a *schema* it's excellent (§4 borrows from it); as a *system* it's Gitea-issues-minus-the-API.

## 3. Recommendation

**Adopt Vikunja for life admin; keep Gitea for code.** The deciding logic, in order:

1. **The errand features are native, not built.** Recurrence + per-task relative reminders + due dates are the entire difference between an errand system and a to-do list. Vikunja is the only tool here with all three in the free tier; every other option makes the agent team re-implement at least one of them (a deadline scanner, a recurrence spawner) and then maintain it.
2. **Agents are first-class.** Per-user API tokens, a documented REST API (v2/OpenAPI), and signed webhooks at project and user level. The one gap — no custom fields — is compensable with labels + a comment convention (§4) because agents, unlike humans, follow conventions perfectly.
3. **Operational fit.** One container, SQLite for a single user, AGPL-3.0 with no feature paywall, no documented telemetry, actively released (v2.7.0, Oct 2026).

**When to choose differently:** if adding any new service is worse than the gaps, use **Gitea issues + §4 conventions + one scheduled agent job** (daily: scan `deadline`s, post reminders to the human's notification channel, spawn recurring errands from templates). If typed custom fields are a hard requirement, **OpenProject** is the honest pick and the weight is the price. If a Nextcloud already runs, Deck + §4 costs nothing to try.

## 4. Minimal schema for errands (works in Vikunja; Gitea mapping in brackets)

One project/list per life area (`home`, `money`, `health`, `car`, `paperwork`). Each errand is one task/issue titled as an action: "Call insurer about claim 4821", not "Insurance".

**Labels — who must act (exactly one, always set):**
- `act/agent` — an agent can do the next step now
- `act/human` — only the human can (sign, appear, decide)
- `act/external` — ball is with an outside party (office, HR, insurer)

**Labels — waiting-on (set together with `act/external`):**
- `waiting/<short-name>` — free-form per counterparty (`waiting/insurer`, `waiting/hr`, `waiting/landlord`), or in Vikunja a single `waiting` label + the name in the task's waiting comment (below). [Gitea: use scoped labels `waiting/…` so only one can apply.]

**Dates — one rule:** the task's **due date is always the next-action / follow-up date**, never the "final" deadline (that goes in the description if it differs). This single convention is what makes reminders meaningful: due today = someone must act today.
- Vikunja: due date + reminders at creation (default: one reminder 1 day before, one on the day) + repeat rule for recurring errands.
- [Gitea: `deadline` field; an agent scanner sends the reminders.]

**Outcome — closed tasks get exactly one:**
- `outcome/done-booked`, `outcome/done-paid`, `outcome/approved`, `outcome/denied`, `outcome/info-only`, `outcome/no-response`, `outcome/escalated`, `outcome/abandoned`
- Plus a closing comment in a fixed shape: `OUTCOME <yyyy-mm-dd>: <one line>` — and for phone calls, log each call as it happens: `CALL <yyyy-mm-dd> <who/number>: <what was said / decided / promised>`. (Numbers stay in the private tracker, never in public repos.)

**Type labels (optional, for filtering/stats):** `type/appointment`, `type/bill`, `type/call`, `type/form`, `type/research`.

**Recurring errands:** Vikunja repeat rule on the task itself; name the series with a stable prefix (`↻ electric bill`) so agents can find the template. [Gitea: one template issue per series, kept closed, cloned by the scheduler.]

**Agent contract (the conventions that make it work):** an agent may create tasks, set `act/*` + `waiting/*`, move follow-up dates, and log calls — but only the human (or an agent with an explicit instruction) sets an `outcome/*` and closes. Every state change leaves a comment; nothing is silently edited.

## Sources

- Vikunja — API docs & webhooks: https://docs.vikunja.io/api-documentation · repo: https://api.github.com/repos/go-vikunja/vikunja
- Gitea — labels: https://docs.gitea.com/1.22/usage/labels/ · webhooks: https://docs.gitea.com/usage/repository/webhooks/ · API: https://docs.gitea.com/api/1.22/ · token scopes: https://docs.gitea.com/development/oauth2-provider/ · custom-fields request: https://github.com/go-gitea/gitea/issues/18210
- OpenProject — system requirements: https://www.openproject.org/docs/installation-and-operations/system-requirements/ · repo: https://api.github.com/repos/opf/openproject
- Plane — automations (paid reminders): https://github.com/makeplane/docs/blob/HEAD/docs/automations/overview.md · mobile (CE exclusion): https://github.com/makeplane/docs/blob/HEAD/docs/devices/mobile.md · issue #6392: https://github.com/makeplane/plane/issues/6392 · repo: https://api.github.com/repos/makeplane/plane
- Taiga — API (application tokens, webhooks, custom attributes): https://docs.taiga.io/api.html · production setup/telemetry: https://docs.taiga.io/setup-production.html
- Kanboard — API: https://docs.kanboard.org/en/latest/api/ · webhooks: https://github.com/kanboard/documentation/blob/HEAD/content/en/v1/dev/webhooks.md · cronjob/overdue mail: https://github.com/kanboard/documentation/blob/HEAD/content/en/v1/admin/cronjob.md
- Nextcloud Deck — API: https://github.com/nextcloud/deck/blob/HEAD/docs/API.md · custom-fields request: https://github.com/nextcloud/deck/issues/6859 · recurring request: https://github.com/nextcloud/deck/issues/7791 · webhook PR: https://github.com/nextcloud/deck/pull/7910
- Focalboard — unmaintained notice: https://github.com/mattermost-community/focalboard · plugin: https://api.github.com/repos/mattermost/mattermost-plugin-boards · user guide (card properties): https://www.focalboard.com/guide/user/
- Markdown prior art — todo.txt: https://github.com/todotxt/todo.txt · git-issue: https://github.com/dspinellis/git-issue · Taskwarrior: https://github.com/GothenburgBitFactory/taskwarrior

## How I checked it

- Every capability claim (reminders, recurrence, custom fields, webhooks, auth, paywalls) was taken from the tool's own documentation or repo, not comparison blogs; maintenance/license/star figures come from live GitHub API reads on 2026-10-15/16.
- Gaps were verified as gaps, not assumed: Gitea's webhook event catalogue (no deadline event), the issue API field list (no custom fields/priority), Deck's open feature requests for custom fields and recurrence, Focalboard's own README maintenance notice.
- Paywall claims (Plane reminders/properties/mobile, OpenProject's free custom fields and the v17.9 date-alert move) were checked against the vendors' own docs/issues.

## Unsure about

- **Vikunja webhook quirks:** deliveries have no retries per docs; a third-party report says the webhook-events listing endpoint returns 401 with API tokens — unverified. Vikunja server telemetry: none documented, not proven absent.
- **Taiga reminders:** no before-due reminder feature was found in the API reference — absence from docs, not proof of absence from the product.
- **Deck webhooks:** the PR making Deck events compatible with Nextcloud's `webhook_listeners` app — merge and release status unverified; as of checking, plan on polling/ETags.
- **Plane CE user limits:** Plane's own statements conflict (issue #9086); no hard-coded CE user cap could be confirmed either way.
- **RAM figures:** only Plane (4 GB min / 8 GB recommended) and OpenProject (4 GB minimum) publish official numbers; Vikunja/Kanboard footprints are described architecturally (single container / PHP+SQLite), not from vendor benchmarks.
- **OpenProject telemetry:** no definitive official statement captured in this pass.
