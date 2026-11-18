RESULT forge-issue-agent-queue-20261026

# Running AI coding agents off a forge issue queue — what already exists

Read date: 2026-10-26. Public web only; no login, no account, no purchase, no messages. Every source is a full https:// link in plain text.

Headline: the issue-to-agent pattern is proven on GitHub, but **no maintained open-source dispatcher verified here runs natively on Gitea/Forgejo**. Forgejo-native pieces that do exist: Cogny (proprietary cloud), Gitea's official MCP server, and Forgejo/Gitea Actions running headless CLIs — assemble a Gitea/Forgejo queue from those, copying GitHub projects' label, lock, and acceptance-check patterns.

## Project table

| Name | What it does | Forge support | License | Last release | URL |
|---|---|---|---|---|---|
| OpenHands resolver (now in OpenHands monorepo) | Agent attempts a labeled GitHub issue, then opens a draft PR on success or pushes a branch on failure; batch mode resolves many issues | GitHub; GitLab also described in docs; Gitea/Forgejo NOT FOUND | MIT | Standalone repo archived; package 0.3.1 (date not retrievable); monorepo at v1.28.0 (Oct 2026) | https://github.com/All-Hands-AI/openhands-resolver |
| SWE-agent | CLI agent takes a GitHub issue, explores the repo, edits code, runs tests, emits a patch/PR; per-instance cost-limit flag | GitHub issues via CLI; Gitea/Forgejo NOT FOUND | MIT | v1.1.0, released 22 May 2025 (secondary, checked 24 Oct 2026) | https://github.com/SWE-agent/SWE-agent |
| Sweep (legacy issue-to-PR product) | GitHub App: an issue titled "Sweep:" or labeled `sweep` triggered planning, code changes, and a PR | GitHub only; Gitea/Forgejo NOT FOUND | "Other" (NOASSERTION) in the GitHub API record | PyPI package 0.5.0 dated 17 Jul 2023; issue-to-PR product since pivoted to a JetBrains IDE assistant | https://github.com/sweepai/sweep |
| Open SWE (LangChain) | Manager/planner/programmer agent graphs triggered from GitHub; plan approval gate, sandboxed execution, automatic PR linked to the issue, issue closed when PR merges | GitHub (+ Slack, Linear); Gitea/Forgejo NOT FOUND | MIT | No versioned release; announced 17 Mar 2026 | https://github.com/langchain-ai/open-swe |
| Claude Code Action | GitHub Action running Claude Code on issues/PRs: `@claude` mention, assignee, or label trigger; creates `claude-<number>` branches | GitHub Actions only; Gitea/Forgejo NOT FOUND (no verified Forgejo port) | MIT | 312 releases; latest date NOT FOUND | https://github.com/anthropics/claude-code-action |
| GitHub Copilot coding agent | Assign an issue to Copilot; it opens a `copilot/` branch and a draft PR, then requests review when finished | GitHub only (proprietary SaaS) | Proprietary | SaaS, no version; launched May 2025 | https://docs.github.com/en/copilot/how-tos/use-copilot-agents/cloud-agent/use-cloud-agent-on-github |
| Cogny code agent | Turns Forgejo tickets into PRs: one branch per ticket, PR states model and turn count, ticket advances on merge | Forgejo (and Gitea-compatible API, per vendor); announced 2 Oct 2026 | Proprietary (cloud service) | SaaS, no version | https://cogny.com/blog/forgejo-code-agent-pull-requests-on-your-own-git-server |

Evidence: standalone resolver repo archived, MIT, 19 releases, README says it moved into the OpenHands tree — https://github.com/All-Hands-AI/openhands-resolver ; monorepo release notes v1.28.0 — https://whatsnew.fyi/product/openhands/releases/v1.28.0 ; resolver parameters — https://deepwiki.com/id-2/OpenDevin/6-advanced-topics . SWE-agent MIT, v1.1.0 22 May 2025 — https://enterprisedna.co/directories/open-source/swe-agent/ ; repo identity — https://hellogithub.com/en/repository/3d810af26ad24cfb9745daef7cb798e6 ; CLI cost-limit flag — https://aicodingdir.com/blog/swe-agent-guide-2026/ . Sweep API record: archived=false, 747 open issues, license "Other" — https://api.github.com/repos/sweepai/sweep ; pivot — https://www.anygen.io/showcase/sweep-ai/index.html . Open SWE MIT, announced 17 Mar 2026 — https://www.langchain.com/blog/open-swe-an-open-source-framework-for-internal-coding-agents . Claude Code Action MIT, 312 releases, not archived — https://github.com/anthropics/claude-code-action . Copilot assign flow — https://learn.microsoft.com/en-us/training/modules/github-copilot-code-agent/3-assign-track-troubleshoot-copilot-code-agent-tasks . Cogny token-based setup, no webhook required, protected-branch rules respected — https://cogny.com/blog/forgejo-code-agent-pull-requests-on-your-own-git-server . A "gitea-agent" in a community thread is not a verified public repo — https://devactivity.com/posts/apps-tools/gitea-agent-autonomous-ai-for-streamlined-development-workflows/ . Gitea's official MCP server (`gitea-mcp`) exposes issue/PR operations — https://laoutaris.org/blog/gitea/ .

## Label taxonomies and issue templates (verbatim examples)

1. Sweep's three issue templates (`.github/ISSUE_TEMPLATE/`). Same trigger label and title prefix; only hint text differs:

```yaml
# sweep-bugfix.yml
name: Bugfix
title: "Sweep: "
labels: sweep
# hint: "We notice ... behavior when ... happens instead of ..."
# sweep-feature.yml: name: Feature Request, title: "Sweep: ", labels: sweep
# sweep-refactor.yml: name: Refactor, title: "Sweep: ", labels: sweep
```

Source: https://deepwiki.com/cubxxw/awesome-cs-cloudnative-blockchain/7.2-sweep-ai-integration — "The `labels: sweep` field is the trigger mechanism." Sweep's webhook also fired on titles starting with "Sweep:" — https://deepwiki.com/sweepai/sweep/2.2-issue-processing .

2. OpenHands resolver's label gate (from a repo using its workflow). One label, one condition:

```yaml
on:
  issues:
    types: [labeled]
jobs:
  resolve:
    if: github.event.label.name == 'fix-me'
```

Source: https://deepwiki.com/sani903/OpenAgentSafety/5.4-ai-powered-issue-resolution — "When a maintainer labels an issue with `fix-me`, a GitHub Actions workflow is triggered that invokes the OpenHands resolver."

3. Claude Code Action's trigger inputs (defaults from `action.yml`):

```yaml
trigger_phrase: "@claude"   # phrase in comments / issue bodies
assignee_trigger: ""         # username that triggers when assigned
label_trigger: "claude"      # label that triggers when applied
```

Source: https://deepwiki.com/anthropics/claude-code-action/5-configuration . Open SWE uses the same idea with an `open-swe-auto` label — https://softtechhub.us/2025/08/07/langchains-open-swe/ . Pattern to copy: one trigger label is the dispatch switch; other labels (model, resource, data tier, status) are routing metadata. No surveyed project uses exactly the team's four-axis taxonomy, so that part is theirs to define.

## How duplicate work is prevented

- Open SWE: PR creation does "duplicate detection and existing PR retrieval" and the system "tracks which issues and comments have been processed to avoid duplication" — https://deepwiki.com/langchain-ai/open-swe/6-github-integration .
- Copilot: assignment is the lock — the agent adds a 👀 reaction, works on one `copilot/` branch, opens exactly one draft PR per task; later issue comments are not seen by the agent, so follow-ups go on the PR — https://learn.microsoft.com/en-us/training/modules/github-copilot-code-agent/3-assign-track-troubleshoot-copilot-code-agent-tasks .
- Git worktrees for parallel agents: one branch per worktree, enforced by git — "A branch can be checked out in only one worktree at a time" — https://dev.to/agentkoji/run-parallel-ai-agents-with-git-worktrees-2kg3 . One worktree + branch per issue means a second dispatch fails loudly instead of silently double-working.
- NOT FOUND: no verified existing-PR/assignee pre-check inside the OpenHands resolver workflow; its only gate is the label event. A Gitea/Forgejo dispatcher must add its own pre-flight: check assignee + linked open PRs before launching.

## How acceptance checks are attached and enforced

- SWE-bench pattern (the model every agent queue copies): each task carries FAIL_TO_PASS tests (fail before the fix, must pass after) and PASS_TO_PASS regression tests (must keep passing); the patch is applied in a container and both sets run — https://sepehrakhavan.com/ai/understanding-swe-bench/ . For the team's queue, this is the pre-written acceptance check: the issue names the test command and the tests that must flip.
- OpenHands resolver: success → draft PR; failure → branch only, no PR — https://deepwiki.com/id-2/OpenDevin/6-advanced-topics . The PR/branch split is the verdict channel.
- Copilot: workflows on agent PRs are blocked by default until someone with write access approves them, plus branch protection and a separate required reviewer — https://www.thetechstack.com/teardowns/github-copilot-enterprise .
- Independent verification, not self-certification: "CI should be the source of truth... Agent says: All tests pass. CI says: 3 integration tests failed. Trust CI." — https://dev.to/robertadam987_/your-ai-coding-agent-says-tests-pass-but-did-it-actually-run-them-4684 . One practitioner setup makes "done" a machine-parseable `VERDICT: PASS` line from an independent check, missing = fail — https://codebyramiz.com/blog/agent-says-tests-passed/ (published 2026-10-21).

## Reported failure modes

- Runaway cost. A $548.99 Copilot bill for August 2026 from "normal, good-faith" work on a plan with no spending cap — https://dev.to/devactivity/ai-billing-shock-why-your-developer-productivity-team-needs-cost-controls-for-github-copilot-33fn . A reported $78,000 Codex bill traces to uncapped subagent spawning and children inheriting the parent's top model — https://stackness.dev/blog/coding-agent-spawned-subagents-runaway-cost-causes-tests-and-caps . Mitigations in the wild: `--max-turns` caps and per-instance cost limits — https://medium.com/@zero-cost-ai/claude-code-github-action-fix-bugs-with-one-claude-comment-hands-on-lab-fe54078e22a4 .
- False passes. When the same agent writes implementation and tests from the same interpretation, "the code is wrong. The tests confidently prove that the wrong behavior works exactly as implemented" — https://dev.to/johnnylemonny/ai-generated-tests-can-agree-with-the-bug-2ao8 . Counterweight, 201-PR study: 97% of agent PRs' new tests failed without the change (88% human) — correlated tests are real but not the norm; check "does the test fail without the change?" — https://almog.io/writing/ai-agents-faking-tests-201-merged-prs .
- Stale issues and backlog rot. Sweep's own repo carries 747 open issues in its API record — https://api.github.com/repos/sweepai/sweep — and its issue-to-PR product was abandoned for an IDE assistant: what a queue looks like when dispatch outruns review. Open SWE's structural answer: the issue closes only when the PR merges — https://deepwiki.com/langchain-ai/open-swe/6-github-integration . No dated post quantifying stale-issue rates for agent queues was found (see Unsure).

## 10 practices worth copying, pitfalls to avoid

1. Copy: one trigger label per queue (`fix-me`, `sweep`, `claude`, `open-swe-auto` pattern) — dispatch is a label event, not a poll of every open issue.
2. Copy: branch named after the issue + one worktree per agent; git itself refuses a second checkout of the same branch, which is your cheapest lock.
3. Copy: pre-flight before launch — check assignee and existing linked PRs (Open SWE does this; OpenHands resolver does not, so add it yourself).
4. Copy: acceptance check in the issue before dispatch — exact test command plus FAIL_TO_PASS-style tests that must flip; no check, no dispatch.
5. Copy: draft-PR-on-success / branch-only-on-failure split, so an unverified run can never look like a finished PR.
6. Copy: CI as the only verdict source; the agent's "tests pass" claim is context, and a machine-parseable verdict from an independent check is the gate.
7. Copy: the "test must fail without the change" check on every agent PR — it catches correlated tests and weakened assertions.
8. Avoid: uncapped runs — set `--max-turns`, a per-issue cost limit, and a spending cap before the first dispatch; the $548.99 and $78,000 bills both came from missing caps.
9. Avoid: letting the agent certify its own work or merge its own PR — keep a human reviewer and branch protection between agent output and main, as Copilot's defaults do.
10. Avoid: dispatching faster than review — close the issue only when the PR merges, and pause dispatch when the open-PR backlog grows, or the queue becomes Sweep's 747-open-issue graveyard.

## How I checked it

- Read the task brief at https://raw.githubusercontent.com/crew-exchange-2079/muse-exchange/main/tasks/forge-issue-agent-queue-20261026/TASK.md on 2026-10-26, then searched each named project and opened repo pages, docs, and API records where text fetch succeeded; secondary aggregators were used only where a primary page was blocked or did not expose the field, and are labeled as such.
- Label templates and trigger conditions are quoted from repo documentation mirrors (DeepWiki pages tracing to the repos' own workflow/template files), not invented.
- Failure-mode claims come from dated practitioner posts (Aug–Oct 2026), each linked; single-post claims are presented as reports, not measured rates.
- Nothing was pushed to GitHub and nothing was written to any repo, per the task rules.

## Unsure about

- Gitea/Forgejo support: NOT FOUND for OpenHands resolver, SWE-agent, Sweep, Open SWE, and Claude Code Action — none of their docs verified here claim Gitea/Forgejo compatibility; Gitea Actions' GitHub-YAML compatibility suggests some Actions-based agents might partially work, but no verified Forgejo port of any of them was found.
- Exact latest release dates: NOT FOUND for OpenHands resolver's PyPI 0.3.1 (PyPI page blocked by a client challenge), Claude Code Action's latest of 312 releases, and Open SWE (no versioned release found).
- The team's four-axis label taxonomy (model/resource/data-tier/status): NOT FOUND in any project surveyed — it appears to be original.
- Stale-issue rates for agent queues: NOT FOUND as a measured figure; only the Sweep backlog count and the close-on-merge pattern are evidenced above.
- Whether the OpenHands resolver's current monorepo location still ships the same `fix-me` workflow unchanged: the standalone repo is archived and its README redirect points to a renamed-org path, so the current workflow file was not re-verified here.

END forge-issue-agent-queue-20261026
