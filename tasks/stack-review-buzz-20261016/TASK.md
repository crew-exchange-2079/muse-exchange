# Task: self-hosted stack review for a human + AI-agent team, incl. where Block's Buzz is now (public research)

Context (generic): one person works with a small team of AI agents (2 lead agents on Claude and Codex/GPT,
plus Gemini review agents, a few free/open-model workers, and local models on one RTX 3090). Everything is
self-hosted on a homelab (rootless Podman/Quadlet on Fedora; Cloudflare Tunnel ingress; Authelia; Tailscale).
Draft target stack:
- Gitea (already running, Actions + runners) = code, documents, agent work tracking (issues/PRs/CI/webhooks)
- Vikunja = errands/life-admin tasks (recurring, reminders, next-action dates)
- a LIVE CONVERSATION layer for the human + agents (phone-first) — candidate: Block's Buzz
- a custom personal "home base" web app (reading room, radio player, daily page) — stays custom
- GitHub = public mirror/showcase only

Research:
1. **Buzz (github.com/block/buzz) today:** what it is now, release history since Sept 2026, architecture
   (Nostr relay, ACP agent harness?), self-host footprint, desktop + MOBILE client status (Android),
   which agent CLIs it can host/bridge (Claude Code, Codex, Gemini CLI, local models), auth model,
   maintenance activity (commits, issues, maintainers), license, maturity/known problems.
2. **Alternatives for the live-conversation layer**, compared to Buzz for "human on phone + several AI
   agents": Matrix (Synapse/Conduit + Element, bots/bridges), Zulip, Mattermost, Rocket.Chat, ntfy+Apprise
   (notify-only), Telegram/Signal bots, and agent-specific options (ACP-compatible hubs, MCP chat servers).
   For each: mobile app quality, bot/agent API, threads/rooms, self-host weight, E2EE, maintenance.
3. **Whole-stack sanity check:** overlaps/gaps between Gitea, Vikunja, the chat layer and a custom home
   base; webhook glue between them (Gitea/Vikunja webhooks -> chat rooms / phone notifications);
   simplest version that works; what to NOT build custom.
4. Recommend: keep/replace each layer, the minimal integration plan, and the top 5 pitfalls.
Cite sources (official docs, repos, release notes). Mark uncertain items. Output: markdown report.
