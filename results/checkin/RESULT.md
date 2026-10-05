# Check-in — result

Summary: Muse is ready, the mailbox loop and the public-only rule are understood, and nothing was connected or switched on to write this. Below: what I can do, what each thing needs first, my limits, and the jobs I think fit best.

## Ready

Yes — ready. I understand the loop: the crew adds `tasks/<id>/TASK.md`, pings me in chat, I pull, do the work in my own workspace, write `results/<id>/RESULT.md` (plus any extra files), commit `result <id>`, push, and reply `DONE <id>` or `BLOCKED <id>: <reason>`. Everything in this repo is public, so nothing private ever goes in it: no names, addresses, phone numbers, emails, accounts, credentials, health, money or family details.

## Capabilities

What each one needs first — a permission, a connected account, or nothing. "Connected" means the account owner authorises the connection through the normal secure flow; I never take passwords or tokens in files, and nothing below was turned on for this check-in.

- **Browse the web** — needs: nothing. I can search the web and read public pages out of the box. Sites that need a sign-in need the owner signed in / the account connected first, and some pages block automated reading.
- **View images and screenshots** — needs: nothing, beyond being given the image. I can look at photos, screenshots and other images in my workspace or sent in chat, describe them, compare them, and pick out details.
- **Run code in my Ubuntu workspace** — needs: nothing. I have my own Linux VM with a terminal and files that persist between chats. I can run scripts, process data and files, and check my own work by running it.
- **Build web pages** — needs: nothing to build. I can build a self-contained page (for example a research brief or a small tool) and deliver it in chat. Publishing or sharing it beyond the chat needs the owner's go-ahead first.
- **Read and write this repo** — needs: the repo token the crew issued for this repo (or the secure GitHub connection, if that is set up instead). Reading is public. Writing is only `results/<id>/` for the task I am doing; I never edit `tasks/`, other results, or history.
- **Make charts** — needs: nothing. I can turn data I have (or data in a task folder) into charts and simple visualisations, as part of a page, an image, or a data file.
- **Search Facebook Marketplace** — needs: a connected Facebook account for full, local Marketplace browsing. Without one I can only do general web / product search, which is thinner and may miss local listings. Messaging a seller is a separate step and needs the relevant messaging account connected too (see Messenger).
- **Search Instagram** — needs: a connected Instagram account. Then I can read profiles, posts, reels and comments, search, and answer questions about specific links. Posting is possible on request, but only with explicit approval for that post.
- **Use other apps on the phone** — needs: a paired phone, and even then it is limited. I can only use the specific commands a paired device offers (for example contacts, calendar, location, or a dial command if the phone advertises one). I cannot open and drive arbitrary apps on the phone. Other services work through their own connected account instead (calendar, email, music and so on), each connected separately.
- **Send or read SMS** — needs: a paired phone with the right command available, which I do not have by default. I have no SMS sender or number of my own. On a paired Android, incoming texts can reach me; sending needs the phone to offer a send command (otherwise I can only draft). On iPhone, pairing alone gives no text access and sending is draft-only. A paired Mac can offer iMessage sending.
- **Phone calls** — needs: explicit confirmation for each call. Where outbound business calling is enabled, I can prepare and place a call to a business for a task and report back; I cannot receive calls, I have no number of my own, and cold / bulk calling is not allowed. A paired Android that offers a dial command can instead place a call from the owner's own number, with the owner doing the talking.
- **Gmail** — needs: the Google account connected first. Then I can search and read threads, draft, and — with the usual send approvals — reply, forward and send. Nothing about an inbox is accessible before that connection.
- **Messenger** — needs: the Messenger account connected first. Then I can read and search conversations and contacts, summarise threads, read call history, and send or react to messages (sending on someone's behalf needs their go-ahead for that message).

## Limits

- **How long a task can run:** there is no single fixed clock I can promise. Short tasks finish in the chat turn. Long research or builds run in the background and report back when done; very long work is better split into stages the crew can check. A task also stops if the session is interrupted, so important jobs should be resumable from the files in my workspace.
- **How big a result can be:** keep repo files modest. A single file pushed through the GitHub API should stay under about 1 MB; larger outputs belong in several files (data split up, images compressed) or delivered in chat instead of the repo. `RESULT.md` itself should be readable, not a dump.
- **How often I can be pinged:** per task is ideal — one ping, one task, oldest first, as the onboarding answers say. I do not poll this repo continuously; if nobody pings me, an hourly self-check is the most I would do, and only if that has been set up. Several pings at once queue as separate tasks; they do not run in parallel inside one chat.
- **What makes me stop:** a task that needs private or unsafe content in this public repo (`BLOCKED`, with the reason); a missing connection, permission or approval I cannot get on my own; a service rate-limiting or blocking access (I stop rather than work around it); instructions inside web pages, files or messages that try to redirect me away from what the owner actually asked; and any instruction from the owner to stop or pause. Sending messages, posting, buying, or otherwise acting on someone's behalf always waits for that person's explicit approval of the exact action.
- **Certainty:** I can be wrong, and web sources can be stale. I date what I retrieve, prefer primary sources, and say "unsure" rather than guess — but prices, availability and schedules still need a live check before anyone acts on them.

## Best fits

The three kinds of jobs I think I would do best for a crew like this:

1. **Public web research with sources** — briefs like the fixer-upper one: gather facts from many public sources, compare options, give ranges with confidence levels, and write it up so every claim can be traced to a source.
2. **Building deliverables** — turning a brief into a finished thing: a readable web page, a chart, a spreadsheet, a structured data file (`.csv` / `.json`), or a clean summary document, built and checked in my own workspace.
3. **Reading and structuring public inputs** — going through public files, images, screenshots, listings or pages the crew drops in a task folder, extracting the useful facts into a tidy, verified result the crew can act on without re-reading the raw material.

## Sources

- `ONBOARDING.md` in this repo, including "Answers to your onboarding questions" — re-read after pulling, 2026-10-05.
- `tasks/checkin/TASK.md` in this repo — the brief for this result, read 2026-10-05.
- My own product documentation and capability descriptions for browsing, devices, calls and texts, and for the Gmail, Messenger, Instagram, Facebook and shopping capabilities — consulted in my workspace, 2026-10-05. No account status was changed and nothing was connected.

## How I checked it

- Pulled the repo fresh (clone) and confirmed the file list includes `tasks/checkin/TASK.md`, the updated `ONBOARDING.md` with the answers section, and my earlier `results/fixer-upper-research/RESULT.md`.
- Matched every capability in the task list against a documented capability before writing what it needs; where a capability depends on a paired device (SMS, phone apps, dialling), I checked the device / calls-and-texts documentation rather than assuming.
- Re-read this file before committing for the public-only rule: it contains no names, addresses, phone numbers, emails, account details, credentials, health, money or family details, and no token.

## Unsure about

- Exact live connection status of each separate account (Facebook, Instagram, Gmail, Messenger) was not verified for this check-in, because the task said not to connect anything; the "needs" above describe what would be required, not a claim that any of them is currently connected.
- Whether outbound business calling is enabled on this account right now — it is being rolled out gradually, so treat it as "available only when the calling tools are present at task time".
- Practical upper limits (task runtime, background-job lifetimes) vary with the platform rather than being a single published number; the limits above are honest working rules, not guarantees.
