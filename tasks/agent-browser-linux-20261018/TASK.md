# agent-browser-linux-20261018

Goal: find the best current (late 2026) way to give an AI agent its OWN persistent web browser on a Linux home server, separate from a human's personal browser, that a person can also watch and take over live.

1. Compare these options, with current versions and maintenance status: (a) Chromium or Brave in a rootless Podman container with a persistent profile plus a live viewer (neko, noVNC/KasmVNC, Selkies); (b) Playwright or Puppeteer controlling that browser over CDP; (c) agent-focused browser projects (e.g. Browser Use, Stagehand, Steel Browser, Browserbase-style self-hosted, Skyvern, "browser MCP" servers); (d) a second profile in an existing desktop browser driven over CDP.
2. For each: how a person watches/takes over (captchas, phone checks); how logins and cookies persist; whether it runs headful without a desktop session; resource use; anti-bot friction (does the site see a normal browser?); security isolation from the host and from the human's browser.
3. Which ones expose an MCP server or a clean API an AI coding agent can call.
4. Recommend ONE setup for: rootless Podman on Fedora, a 16-thread desktop with 62 GB RAM that is also the human's workstation, a human who wants to watch from any device, and an agent that signs into ~10 social/maker sites (YouTube, GitHub, Bluesky, Printables, etc.) and sets up 2FA. Give the exact components and why.

Rules: public pages only, no login, no account, no purchase, no messages or comments to anyone. A link and read date for every fact. Say "unsure" rather than guess. End with **How I checked it** and **Unsure about**.

Delivery: reply in this chat with the full RESULT block: first line `RESULT agent-browser-linux-20261018`, then the complete answer in Markdown (write every source as a full https:// link in plain text), last line `END agent-browser-linux-20261018`. Also push `results/agent-browser-linux-20261018/RESULT.md` to GitHub only if asked.
