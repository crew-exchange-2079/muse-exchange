# Stack review: Buzz today, the live-conversation layer, and the whole human+agents stack

## Summary

- **Buzz is real, well-built, and moving extremely fast — but it is ~3 months past public launch, pre-1.0 on every component, and its phone story has a hole exactly where this stack can't afford one: Android push notifications are not end-to-end yet** (off by default, still an open issue; Play Store reviews corroborate). Buzz's architecture — agents as first-class members with their own identities on a relay you own — is the best long-term fit for the CLI-agent leads of anything reviewed. It is the right thing to *trial*, not yet the right thing to *depend on*.
- **Recommendation for the live-conversation layer today: Zulip** (self-hosted). Its mandatory stream+topic threading is the strongest model for parallel agent tasks, its bot system is purpose-built (per-agent bot accounts, outgoing-webhook wake-ups on @mention), it ships a documented Gitea integration, every feature is in the free self-hosted tier, and its push relay is free at this scale (≤10 users). Cost: it's the heaviest chat option and wants a dedicated VM.
- **Subscription lock-in (checked against current vendor terms — §2): OpenAI is officially fine** (ChatGPT-plan Codex in local third-party harnesses is now a supported program), **Claude works but is fragile** (subscription sign-in is permitted only into Anthropic's own unmodified binary/SDK; Anthropic already tried once in 2026 to move exactly this usage to API-rate billing, and reserves no-notice enforcement), and **consumer Gemini CLI is simply gone** (account access retired June 2026 — Gemini agents need an API key or enterprise license now).
- The rest of the draft stack holds up: Gitea stays the system of record for code/agent work, Vikunja stays for errands, the home-base app stays custom (but read-only — it must not grow its own task/chat/notification systems), ntfy stays as the alert transport. The missing piece none of the draft layers provides is a **notification/escalation router** (push → SMS → voice, with quiet hours in exactly one place). Build that small; build nothing else custom in this space.
- Rejected with reasons: Mattermost (v11 "Entry" free tier caps history at 10k messages; production-grade push is paid), Rocket.Chat (registration/Starter funnel, tier-capped apps), Telegram (bots structurally cannot see each other — not a shared multi-agent conversation), Signal (no official bot API at all), Matrix (right protocol, wrong fit today: weak threads, E2EE-vs-bots pain, fork churn in the light server lineage), ntfy+Apprise alone (a notification bus, not a conversation).

All facts checked 2026-10-16 against official docs, vendor terms pages, and live GitHub API reads.

## 1. Buzz today (github.com/block/buzz)

### 1.1 What it is, and how it's built

Buzz is Block's free, open-source (Apache-2.0), self-hostable workspace "where humans and agents build together, on a relay you own" (launched publicly 2026-07-21). The workspace unit is a **community** served by one relay; inside it: channels (public/private), threads, DMs, canvases, media, search, an audit log, YAML workflows, voice huddles, and git hosting. A hosted version of the same software runs at buzz.xyz.

Agents are **members, not bots**: each has its own Nostr keypair, channel memberships, and audit trail, and everything — messages, reactions, workflow steps, review approvals, git events — is a signed Nostr event in one log, with the same identity model for people and processes.

Architecture (from the repo's `docs/ARCHITECTURE.md`):
- **`buzz-relay`** (Rust/Axum) is the single source of truth: WebSocket + REST, NIP-01 wire format, NIP-42 (WebSocket) and NIP-98 (HTTP) auth, NIP-34 git events. No P2P/gossip/multi-relay replication in the shipped design.
- Backing stores: **PostgreSQL** (events, channels, tokens, workflows, audit log, full-text search), **Redis** (presence/typing/pub-sub), **S3/MinIO** (media).
- **The agent harness is `buzz-acp`**, a separate binary speaking **ACP (Agent Client Protocol)**: relay ──WS/NIP-42──→ buzz-acp ──stdio/JSON-RPC──→ agent subprocesses. It pools 1–32 subprocesses (default 1), queues @mentions per channel (one prompt in flight per channel), and respawns crashed agents. Agents run **wherever the CLIs are installed** — typically a workstation — not on the relay.
- Block's own **`buzz-agent`** is a model-direct agent (LLM backend = any OpenAI-compatible endpoint: Ollama, llama.cpp, vLLM, gateways) with tools via MCP.

### 1.2 Releases, clients, and the mobile gap

Three release lanes: desktop (GitHub Releases), relay (container images), mobile (store releases, no GitHub Releases). Desktop is at **v0.5.28 (2026-10-09)**, roughly weekly since launch (the Sept–Oct window alone: v0.5.22 → v0.5.28). Desktop is Tauri+React for macOS/Linux/Windows — the Windows installer is literally named `…_alpha-unsigned.exe` (not code-signed; SmartScreen warning documented).

**Mobile is shipped, not vaporware**: official Flutter apps on Google Play (`xyz.block.buzz.mobile`, 10K+ downloads, v0.20.0 updated 2026-10-05) and the iOS App Store (v0.22, ~2026-10-15). Mobile versioning (0.2x) is independent of desktop (0.5.x), and the README's status table still lists mobile as "being wired up."

The decisive gap: **push notifications are not end-to-end on mobile yet.** Push is off by default (`BUZZ_PUSH_ENABLED=false`), the README lists it as "pending code," Android FCM push is an open issue (#6092), and Play Store reviewers report no native notifications and agent messages not appearing until force-quit/reopen. For a phone-first team, that means the relay's live layer currently cannot reliably *reach* the human — agents can talk, but the tap on the shoulder is missing.

### 1.3 Which agents it can host

Documented as supported in `crates/buzz-acp/README.md` — "any agent that speaks ACP over stdio," naming **Goose**, **Codex** (via `codex-acp`), and **Claude Code** (via `claude-agent-acp`). Kimi Code and Grok Build appear in release-note setup/discovery code but their support tier is undocumented (UNVERIFIED). **Gemini CLI is not documented as a hosted CLI** (Gemini appears only as a model route for buzz-agent), and OpenCode hosting is not documented. Local models are supported as *endpoints for buzz-agent* (Ollama/llama.cpp/vLLM), not as hosted CLIs.

Two structural limits from the tracker: **managed agents are machine-local** — an agent is only mentionable/visible from the machine running it (#3277, #2508 and related), and relay-hosted agents are still an RFC (#4174), not a shipped model. Also from the architecture doc's own "verified gaps": **workflow approval gates are not wired end-to-end** (a run that hits a gate is marked Failed), some workflow actions return NotImplemented, and rate limiting exists as tiers on paper but only an always-allow stub is enforced.

### 1.4 Auth, footprint, maintenance, maturity

- **Auth:** Nostr keypairs everywhere (humans onboarded in the desktop app; agents via `BUZZ_PRIVATE_KEY`). Closed membership by default: the relay owner is an implicit operator, operators add members by pubkey (kind:13534 membership events); use-limited invite links exist. Access control = channel membership, enforced by the relay. **No SSO/OIDC in the OSS relay** — recent changelogs add *spec documents* for federated/enterprise identity adapters; implementation status UNVERIFIED.
- **Footprint:** one Docker Compose stack — relay (single Rust binary serving WS, REST, and web UI) + Postgres 17 + Redis 7 + MinIO. Pin image digests for production; optional Caddy/TLS overlay; a Railway one-click template exists. Trap: the community is keyed by the exact relay URL — change it and you seed a fresh, empty community. No documented RAM/CPU minimums (UNVERIFIED).
- **Maintenance (GitHub API, 2026-10-16):** 36,025★, 4,772 forks, Apache-2.0; **268 commits in the last 30 days, 1,309 in the last 90**; ≥100 contributors, top contributor ≈17–24% depending on window; multiple Block staff among top authors (Block-led and Block-governed). 1,656 open issues — the tracker itself is a maturity signal.
- **Maturity verdict:** pre-1.0 on every axis (desktop 0.5.x, relay 0.2.1, mobile 0.2x), built and governed by a single vendor ~3 months after launch, with its own docs candid about unwired pieces. None of that makes it a bad bet — Apache-2.0 + self-hosting caps the blast radius — but it prices the risk honestly: adopt it as a *trial with triggers* (§5), not as load-bearing infrastructure yet.

## 2. The subscription question: can a harness host a plan-based agent?

Buzz's hosting model spawns agent CLIs on the user's machines, so whether a *subscription* (not API key) may legally/technically power those agents is a gating question. Checked against each vendor's current terms/help pages (2026-10-16):

| Vendor | Verdict |
|---|---|
| **Anthropic / Claude** | **Restricted — works today, officially fragile.** OAuth sign-in is intended for Claude Code and native Anthropic apps; Anthropic's legal page bars third-party *developers* from offering Claude.ai login in their apps or routing requests through plan credentials, and reserves enforcement without prior notice. The explicit carve-out: an end user may sign in with their own subscription to the **unmodified** Claude Code binary, "including where a platform hosts" it. Server-side blocks on subscription OAuth outside the official client began 2026-01-09 and broke several third-party harnesses. The ACP adapter (`claude-agent-acp`, maintained in the ACP org) drives the Claude Agent SDK/binary, so Claude-in-Buzz today runs on the user's plan — but Anthropic announced in May 2026 that SDK/`claude -p` usage would move off subscription limits to metered API credits, **paused** that change before it took effect (2026-06-15), and its Oct 2026 help-center update keeps subscription-limit use "for now" while adding separate monthly API credits on Max/Team. Practical reading: permitted pattern = hosting the unmodified binary under the user's own login; the billing basis can change with advance-notice-but-unilateral action. |
| **OpenAI / Codex** | **Supported — the permissive outlier.** Codex documents "Sign in with ChatGPT" alongside API keys, and `codex-acp` documents ChatGPT login as a first-class auth mode. At DevDay 2026 (2026-09-29/30) OpenAI launched **"Sign in with ChatGPT" for third-party apps**: local/open-source apps may spend the user's plan allowance (per-app weekly caps set by the user); open-source harnesses are named launch partners; only paid or remotely *hosted* redistribution needs OpenAI approval. A locally-run open-source ACP host on a ChatGPT plan is an officially supported configuration. |
| **Google / Gemini** | **Gone, not locked.** Gemini CLI spoke ACP natively with Google-account auth — until Google's 2026-05-19 announcement retired consumer account access: on 2026-06-18 Gemini CLI stopped serving AI Pro/Ultra and free Code Assist individual tiers. What remains is paid API keys or Code Assist Standard/Enterprise licenses; the consumer successor (Antigravity CLI) is first-party-only with no official ACP route announced. Any Gemini seat in this stack must be budgeted as API-key usage. |

Consequence for §5: the stack must not *depend* on plan-based Claude harnessing. Budget an API-key fallback for the Claude lead, treat Codex-on-plan as safe, and treat Gemini as API spend.

## 3. Alternatives for the live-conversation layer

| Option | Mobile + push | Agent/bot story | Threads | E2EE | Weight | Verdict |
|---|---|---|---|---|---|---|
| **Zulip** (26,054★, Apache-2.0, v12.3) | Official apps; push **only via Zulip's relay** — free ≤10 users; no self-hosted relay | **Best-in-class**: bot accounts + API keys, incoming & outgoing webhook bots (wake on @mention), versioned API with feature levels, 200 req/min/user | **Streams + mandatory topics** — one topic per task; resolvable | None for messages (TLS + own server) | Heaviest: Django + PG + Redis + RabbitMQ + memcached; documented 2 GB floor; installer wants its own box/VM | **Adopt** |
| **Buzz** (§1) | Stores since Jul 2026; **push not end-to-end** | Agents are members via ACP harness — the only native agent hosting here | Channels + threads | Nostr-signed events; no E2EE rooms story | Relay + PG + Redis + MinIO | Trial, triggers in §5 |
| **Matrix** (Synapse 4,700★ AGPL; light fork Continuwuity 1,110★) | Element X; Android push can be fully self-hosted via UnifiedPush/**ntfy**; iOS needs Sygnal/APNs | Bots as plain accounts (nio/mautrix libs); appservices can puppet many agent identities; Hookshot for webhooks (generic only — no Gitea built-in) | Rooms; threads exist but optional/client-dependent — pattern is one room per task | Real E2EE, but **bots in encrypted rooms are a documented pain** (key handling, undecryptable events) → run agent rooms unencrypted | Synapse ~1–2 GB class; Continuwuity single Rust binary, tens of MB — but fork lineage churned (Conduit→conduwuit archived→Tuwunel/Continuwuity) and DB formats are incompatible between forks | Credible fallback; not now |
| **Mattermost** (39,343★, v11.11.1) | Store apps; HPNS push relay now requires a **paid license**; free = TPNS test service (no SLA) or own push proxy | Clean: bot accounts + tokens, REST + WebSocket, native incoming/outgoing webhooks, slash commands | Channels + threaded replies (default on) | No native E2EE (third-party plugin only) | Light: Go + PostgreSQL, documented 1 vCPU/2 GB | **Out** — v11 free "Entry" edition caps history at **10,000 messages** + 10k push/mo; Team Edition binaries capped at 250 users; in-place upgrades can silently convert a free server to Entry |
| **Rocket.Chat** (46,274★, v8.9.0) | Gateway push needs workspace registration; 10k/mo free on Community; own-certs push requires self-built apps | Bots = user accounts + REST/DDP, or Apps-Engine (app counts tier-capped); native incoming webhooks | Channels + threads + discussions | Native per-room E2EE, but encrypted content is unsearchable and bots may be unable to read it | Node + MongoDB replica set; heaviest baseline here | **Out** — registration funnel auto-provisions a Starter license (25-user cap per docs; some pages say 50 — UNVERIFIED) and exceeding it flips you to a trial |
| **Telegram bots** | Best phone UX of all; not self-hostable (Bot API server aside) | Forum topics, buttons, editing — **but bots cannot see other bots' messages**, so several agent-bots are not a shared conversation; one bot fronting all agents behind a relay is the only workable shape | Forum topics | No (group/bot chats are cloud chats) | None (their cloud) | Out for the agent room; fine as a human notification channel |
| **Signal** | Excellent app | **No official bot API exists.** signal-cli (4,985★, actively maintained) is an unofficial client on a real phone-number account — CAPTCHA/rate-limit friction documented; ban claims UNVERIFIED | Groups, no topics | Yes (its whole point) — but not via bots | signal-cli daemon | Out for agents |
| **ntfy + Apprise** | ntfy push is already this stack's alert channel | ntfy topics are symmetric pub/sub — a crude request/reply loop is possible, but there are no speakers, threads, search, presence, or read state; Apprise is one-way fan-out only | None | ntfy ACLs/TLS; no E2EE | Minimal (already running) | Keep as the **notification** layer, not the conversation layer |
| **ACP hubs / agent rooms** (Commonly 1,363★; agent-room 99★; MCP "chat" servers) | Varies; phone UX immature | ACP standardizes editor↔agent sessions — it has **no room/membership/fan-out semantics**; a group chat on ACP is a custom host (Buzz is one). MCP-chat projects bolt a shared message store onto MCP tools (agents poll) | Varies | Varies | Small | Watch Commonly; don't build on MCP-chat toys |

Two cross-cutting notes. First, **ACP is plumbing, not a chat layer**: whichever server is chosen, the CLI leads join it through an ACP-host-style runner (the buzz-acp pattern reused standalone) or vendor SDK runners, and every *other* participant (API workers, local models, computer-use agents, the repo-based agent) joins as a plain bot — which is why the server's bot API matters more than its agent branding. Second, of the agent-native projects, **Commonly** (open-source humans+agents rooms, agents with names/memory/workstations, pushed the day of this check) is the only one with real traction besides Buzz; the MCP-chat projects are weeks old with near-zero adoption.

## 4. Whole-stack review (including the team's wider setup)

The wider team context reviewed alongside the draft stack: two Android phones (the human's phone with ADB/SSH automation access, and a dedicated crew phone running an SMS text desk for family plus 2FA-code duties); computer-use agents (a browser-automation bridge driving the human's signed-in browser in isolated tab groups, and a desktop chat agent on a Windows PC); outbound voice calls via a telephony API; a phone-based AI agent on its own VM that exchanges work through a public GitHub repo; the internet-radio station (phone/Android Auto app, TV and kitchen-tablet ambient displays); Home Assistant; a camera-equipped 3D printer; and a local RTX 3090 serving models.

### 4.1 Overlaps

- **Gitea issues vs Vikunja** — two task systems is the right count, but only with a hard boundary: anything about code, documents, or agent work lives in Gitea; life-admin (appointments, bills, follow-ups) lives in Vikunja. Enforce by convention (and by where reminders exist — only Vikunja has them), not by building sync between them.
- **Buzz vs everything** — Buzz bundles chat + git hosting + workflows + canvases. If it is ever adopted beyond the trial, adopt it as *chat only*; migrating git or task tracking into it would tear the Gitea/Vikunja records that already work.
- **Home base vs chat** — the daily page and the chat inbox will drift into two "front doors." Rule: the home base *reads* (today's Vikunja dues, Gitea activity, chat unread counts, radio schedule); the chat is where conversation happens; neither stores the other's data.

### 4.2 Gaps in the draft stack

1. **No notification routing policy.** The pieces exist (chat push, ntfy, a crew phone that can SMS, a telephony API that can call) but nothing decides which channel a given event deserves. Without one router, every tool notifies at full volume and the human mutes the lot.
2. **No wake-up path for non-CLI participants.** The browser bridge, the desktop agent, API workers, and local-model agents can't be ACP subprocesses. They join as chat bots woken by outgoing webhooks/@mentions — available in Zulip today, custom in Buzz.
3. **No agent identity registry.** Each agent should exist exactly once as a named identity (bot account / keypair) with scoped tokens, listed in one Gitea-tracked registry. Buzz's keypair model does this elegantly; in Zulip it's bot accounts + a registry file. Skipping this is how you get shared tokens and mystery actors in the audit log.
4. **The SMS desk is not yet a chat citizen.** Inbound family SMS should land in a chat stream (via the crew phone) and replies should be sendable from chat — the family keeps texting a normal number; the team gains a record. Small bridge, high household value.
5. **Backups for the stateful trio** (Gitea, Vikunja DB, chat DB) as one job. Obvious, easy to postpone, painful exactly once.

### 4.3 Integration map

- **Gitea → chat:** Zulip ships a documented **Gitea incoming-webhook integration** (branch filtering included) — repo events into a `#dev` stream, one topic per repo/event class; review requests surface as topics, not scrollback.
- **Vikunja → chat + phone:** Vikunja's generic webhooks feed a due/overdue stream. But Vikunja webhooks are **delivered once with no retries**, so anything that must not be missed goes dual-path: webhook → chat (the record) *and* → ntfy (the tap), via one small relay service on the LAN/tailnet (Vikunja's SSRF guard blocks private targets by default — one config flag, noted in the earlier tracker review).
- **Chat → agents:** one bot account per agent; Zulip **outgoing-webhook bots** POST on @mention/DM to each agent's runner (ACP-host process for the CLI leads, plain service for API/local-model workers). The human talks in topics; agents reply in the same topic; outcomes get written back to Gitea/Vikunja by the agent that did the work.
- **Notifications — one router, three tiers, quiet hours in one place:**
  - *Tier 1 (record):* chat stream — everything lands here, no push by default.
  - *Tier 2 (tap):* ntfy at set priorities — due-today errands, CI failures, printer/HA alerts, agent "blocked on you" pings.
  - *Tier 3 (wake):* SMS via the crew phone when a Tier-2 item is critical and unacknowledged after a set interval; voice call via the telephony API only for the genuinely urgent class.
  - **Quiet hours (e.g. 23:00–07:00):** enforced in the router, not per-app: Tier 2 held to morning digest, Tier 3 passes only for the critical class. Chat and ntfy app settings stay permissive; the policy lives in exactly one config.
- **Phones:** the human's phone is the chat + ntfy client and an automation target (ADB/SSH) — nothing new to build. The crew phone stays an appliance (SMS desk + 2FA) and gains the Tier-3 sender role.
- **Ambient surfaces:** TV/kitchen tablet keep showing the home base and radio; chat does not need a TV client — the daily page already aggregates what a glance needs.
- **The repo-based phone agent** keeps its asynchronous GitHub lane (public tasks/results); its completions can mirror into a chat stream via the same Gitea webhook path, with the repo remaining the record.

### 4.4 Stays exactly as it is

Gitea (code, docs, agent work, Actions/runners) · Vikunja (errands) · GitHub (public mirror/showcase only) · the custom home base (reading room, radio player, daily page) · ntfy (alert transport) · the crew phone as SMS/2FA appliance · Authelia + Cloudflare Tunnel + Tailscale as the access layer · local models on the 3090 exposed as OpenAI-compatible endpoints. None of these has a better replacement in this review, and each is load-bearing for something the new layer shouldn't absorb.

## 5. Recommendations

### 5.1 Keep / replace, layer by layer

| Layer | Call |
|---|---|
| Gitea | **Keep** — system of record for code, documents, agent work |
| Vikunja | **Keep** — errands/life admin (recurrence + reminders are native; see the tracker review) |
| Live conversation | **Add Zulip now** (dedicated VM); **trial Buzz** in parallel for the CLI leads |
| Home base | **Keep custom, read-only** — aggregate, never originate tasks/chat/notifications |
| GitHub | **Keep** — public mirror/showcase + the repo-agent lane |
| Notifications | **Keep ntfy**; add the small router (§4.3); SMS/voice are router tiers, not new apps |
| Matrix / Mattermost / Rocket.Chat / Telegram / Signal | **Do not adopt** for this layer (reasons in §3) |

### 5.2 Minimal integration plan

1. Stand up Zulip on a dedicated VM (its installer expects to own the host; the homelab's Fedora/Podman pattern argues for isolating it rather than fighting the installer). Register the server for the push relay (free at ≤10 users). Create streams: `#dev`, `#errands`, `#ops`, `#family-desk`, one per project as needed.
2. Create one bot account per agent + an agent registry (names, owners, token scopes) tracked in Gitea. Wire the shipped **Gitea → Zulip** integration for repo events.
3. Build the one small **webhook relay/router**: inputs = Vikunja webhooks, Gitea events needing escalation, HA/printer alerts; outputs = Zulip streams, ntfy priorities, SMS via the crew phone, voice as last tier; quiet-hours + acknowledgement/escalation logic lives here and nowhere else.
4. Wire **outgoing-webhook bots** to the agent runners: ACP-host processes for the Claude/Codex leads (hosted unmodified binaries under the human's own logins, §2), plain HTTP services for API workers and 3090-backed local models.
5. Bridge the crew phone's SMS desk into `#family-desk` (inbound SMS → stream; replies → SMS).
6. **Trial Buzz** on one relay with the two CLI leads as members; use it for real agent chatter for 4–6 weeks. Re-evaluate against triggers: (a) Android push end-to-end shipped and on by default, (b) workflow approval gates wired (or relay at a 1.0 line), (c) remote/hosted-agent model (#4174) resolved or the machine-local limitation acceptable in practice. If the triggers land, Buzz may graduate to the agent room — with Zulip/ntfy keeping the human/family/notification roles regardless.
7. One backup job covering Gitea + Vikunja + Zulip state.

### 5.3 Top 5 pitfalls

1. **Building the agent room on fragile subscription auth.** Claude via ACP/SDK currently bills to plan limits, but that usage is precisely what Anthropic tried to re-bill in June 2026 and what its terms let it enforce against without notice; January 2026 already broke third-party harness logins once, overnight. Keep an API-key fallback budgeted for the Claude lead so a policy change is an inconvenience, not an outage. (Gemini is already past this point — API key or nothing.)
2. **Adopting Buzz as the phone-first layer before its push works.** The failure mode is silent: agents post, the phone doesn't buzz, the human stops trusting the room. Push E2E on Android is an open issue today — that's why Buzz is a trial with triggers, not the foundation.
3. **"Free" chat editions that aren't.** Mattermost v11's default free edition caps message history at 10k and push at 10k/month (and upgrades can convert a server silently); Rocket.Chat funnels self-hosters through registration into a capped Starter license and trials. Any future re-evaluation of either starts from their pricing pages, not their feature pages.
4. **Letting chat become the record.** Chat scrollback is where decisions go to be forgotten. The rule that keeps this stack sane: chat *links to* records; outcomes are written back to the Gitea issue or the Vikunja errand (with its outcome label) by whoever did the work. If it isn't in Gitea/Vikunja, it didn't happen.
5. **Notification sprawl.** Gitea, Vikunja, chat, ntfy, HA, and the printer can all ping the phone independently; left alone they will, at full volume, until everything is muted and the one critical alert drowns. One router, one quiet-hours config, one escalation ladder (chat → ntfy → SMS → voice) — and resist every request to add a second path "just for this one service."

*Runners-up worth one line each:* Zulip's installer owning its host (isolate it in a VM from day one); Vikunja's no-retry webhooks (dual-path anything critical); Matrix E2EE rooms + bots (if Matrix is ever adopted, agent rooms stay unencrypted); fork roulette in the light Matrix servers (DB formats incompatible between Conduit descendants — choosing one is a one-way door); single-vendor roadmap risk on Buzz (mitigated by Apache-2.0 and self-hosting, not eliminated).

## Sources

- Buzz — repo, README, ARCHITECTURE, RELEASING, CHANGELOG, buzz-acp/buzz-agent READMEs: https://github.com/block/buzz · launch post: https://block.xyz/inside/introducing-buzz-where-humans-and-agents-work-together · self-host guide: https://engineering.block.xyz/blog/run-your-own-buzz-relay · Play listing: https://play.google.com/store/apps/details?id=xyz.block.buzz.mobile · Android push issue: https://github.com/block/buzz/issues/6092
- Subscription terms — Anthropic legal & compliance (updated 2026-10-05): https://code.claude.com/docs/en/legal-and-compliance · Anthropic Help Center, Agent SDK with a plan (updates 2026-06-15, 2026-10-07): https://support.claude.com/en/articles/15036540-use-the-claude-agent-sdk-with-your-claude-plan · claude-agent-acp: https://github.com/agentclientprotocol/claude-agent-acp · OpenAI Sign in with ChatGPT: https://developers.openai.com/siwc · Codex auth: https://developers.openai.com/codex/auth · codex-acp: https://github.com/agentclientprotocol/codex-acp · Google, Gemini CLI → Antigravity transition (2026-05-19): https://developers.googleblog.com/an-important-update-transitioning-gemini-cli-to-antigravity-cli/
- Zulip — bots/integrations: https://zulip.com/help/bots-and-integrations · Gitea integration (in-repo): https://github.com/zulip/zulip/blob/HEAD/zerver/webhooks/gitea/doc.md · mobile push: https://zulip.readthedocs.io/en/9.0/production/mobile-push-notifications.html · requirements: https://github.com/zulip/zulip/blob/HEAD/docs/production/requirements.md · plans: https://zulip.com/plans
- Matrix — Hookshot: https://github.com/matrix-org/matrix-hookshot · Synapse rate limits/admin API: https://matrix-org.github.io/synapse/v1.40/admin_api/user_admin_api.html · Continuwuity: https://github.com/continuwuity/continuwuity · Tuwunel: https://github.com/matrix-construct/tuwunel
- Mattermost — v11 free-offerings changes: https://forum.mattermost.com/t/mattermost-v11-changes-in-free-offerings/25126 · push configuration (in-repo docs): https://github.com/mattermost/docs · E2EE status thread: https://forum.mattermost.com/t/your-input-needed-end-to-end-encryption-e2ee-in-mattermost/20590
- Rocket.Chat — plans: https://github.com/rocketchat/docs/blob/HEAD/readme/our-plans.md · push settings: https://docs.rocket.chat/docs/workspace-administration/settings/push · E2EE: https://docs.rocket.chat/docs/e2e-encryption · incoming webhooks: https://docs.rocket.chat/docs/integrations
- Telegram — Bot API: https://core.telegram.org/bots/api · bot FAQ (bots can't see bots; privacy mode; rate limits): https://core.telegram.org/bots/faq · Signal — protocol docs only: https://signal.org/docs/ · signal-cli: https://github.com/AsamK/signal-cli
- ntfy — publish/subscribe/config docs: https://docs.ntfy.sh/publish/ · https://docs.ntfy.sh/config/ · Apprise: https://github.com/caronc/apprise · ACP: https://agentclientprotocol.com/ · Commonly: https://github.com/Team-Commonly/commonly · A2A: https://github.com/a2aproject/A2A

## How I checked it

- Buzz facts come from the repo itself (README, architecture doc, crate READMEs, changelog, release pages, issue tracker) plus live GitHub API reads; commit counts were cross-validated three ways (API Link headers, search API, blobless clone). Store status was verified on the live Play/App Store listings, which is how the "mobile shipped but push not wired" split was caught — the README alone would have misreported both halves.
- The subscription section rests on the vendors' own pages, read directly (Anthropic's legal page's authentication section and its carve-out for the unmodified binary; OpenAI's Sign-in-with-ChatGPT developer docs; Google's transition post), with Zed's post used only to corroborate the ACP billing behaviour.
- Edition traps (Mattermost Entry caps, Rocket.Chat Starter funnel, Zulip push-relay terms) were taken from the vendors' own announcements/plans/docs, not forum complaints; where a figure conflicted (Rocket.Chat Starter 25 vs 50 users) it's flagged below instead of resolved by guess.

## Unsure about

- Buzz relay's current newest image tag (no relay GitHub Releases exist to check); Kimi Code / Grok Build support tier in Buzz (present in code, undocumented); whether Buzz's federated-identity specs (NIP-FA etc.) are implemented anywhere; Buzz hardware minimums (none documented).
- Rocket.Chat Starter user cap: official materials conflict (25 in the plans doc, 50 on some current pages).
- Matrix light-server lineage (Conduit/Continuwuity/Tuwunel) is moving fast; version numbering for Continuwuity was inconsistent across sources (formal GitHub latest release v26.7.2, 2026-08-07).
- Element X thread UX parity with Element Web (UNVERIFIED); the reported Element X Android UnifiedPush edge case (#6551) is a single-issue report.
- Whether Anthropic's paused Agent SDK billing split returns, and in what form — its help center says a revised version will come with advance notice; no date is published.
- Antigravity CLI third-party/ACP access: no official route announced; a third-party adapter's claim about its terms is UNVERIFIED against Google's own text.
