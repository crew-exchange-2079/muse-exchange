# Task: self-hosted task trackers for NON-code "life admin" work done by AI agents (public research)

Context (generic): a small team of AI agents helps one person with errands and life admin (booking
appointments, following up with HR/insurance/billing offices, tracking bills and deadlines, research
reports), alongside software work that already lives in a self-hosted Gitea. Gitea issues fit code well
but are only a plain to-do list for errands (no "waiting on X until date", reminders, recurring tasks,
phone-call outcomes, or calendar links).

Compare, for agent use over an API: Gitea/Forgejo issues (labels, milestones, due dates), Vikunja,
Plane, OpenProject, Focalboard/Mattermost Boards, Taiga, Kanboard, Nextcloud Deck, plus plain
markdown-in-git approaches. For each: API quality for agents (auth, webhooks, due dates, reminders,
recurring tasks, custom fields like "waiting on"), self-hosting weight (RAM, DB), maintenance status,
license, mobile app for the human, and privacy posture.
Recommend: one tool (or "just use Gitea issues + conventions") for this split, and a minimal label/field
schema for errands (waiting-on, follow-up-date, outcome, who-must-act). Cite sources. Output: markdown report.
