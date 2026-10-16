# Task: self-hosted Gitea webhooks -> personal dashboards & notifications (public research)

Context (generic): a homelab runs self-hosted Gitea with Gitea Actions (act_runner), plus a small
self-hosted home dashboard web app, an ntfy server, an internet radio stream, and a TV/tablet.
Several AI agents do work in Gitea (issues, pull requests, CI). The person wants to SEE what
happened without reading git: a daily plain-English activity feed, a nightly summary, instant
phone alerts only for items labeled "needs-owner", and an ambient status board for a TV.

Please research and report:
1. Gitea webhook event types and payloads relevant here (push, PR opened/merged, issue opened/closed/labeled,
   Actions workflow_run if available), webhook auth/signing (secret, HMAC header), and delivery/retry behavior.
   Cite Gitea docs with version notes (1.21+ / current).
2. Existing open-source tools that already turn Gitea/Forgejo/GitHub-style webhooks into:
   (a) notifications (ntfy, Gotify, Apprise, ntfy's built-in templates), (b) activity feeds/status pages,
   (c) dashboards (Homepage, Homarr, Glance, Dashy, Grafana) with Gitea widgets/integrations.
   For each: what it does, maintenance status, license, how hard to self-host.
3. Patterns for turning raw events into human-readable one-line summaries (templating approaches,
   dedupe/batching so a busy day isn't spammy, quiet hours).
4. Gitea Actions tricks useful for this: scheduled workflows, workflow_run triggers, calling a webhook/ntfy
   from a workflow, runner labels, secrets.
5. A recommended minimal design (3-5 components) and the 3 biggest pitfalls.

Output: a markdown report with links (no private data needed or wanted). Keep it practical.
