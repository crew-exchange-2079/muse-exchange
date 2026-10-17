# Nebius x NVIDIA Global AI Hackathon — builder perks, credits, and "runs on Nebius" requirements

**Summary.** A hackathon entrant can stack **$50 in Nebius Token Factory credits** — $25 from the hackathon's own promo-code form (activation code `NEBIUS-DEVPOST-GLOBAL26`) plus $25 from the free Nebius Builder Program — and the Builder Program also includes **$25 in Tavily partner credits**. Builder Program credits **expire 90 days from issuance**. One catch matters before signing up: the Builder Program registration itself is just a web form plus email verification, but **using Token Factory requires completing its onboarding, and Token Factory's own docs state that billing setup is mandatory and requires a bank card**. The hackathon (Devpost: nebiusglobalaihackathon.devpost.com) runs a Submission Period of **August 26, 2026 (9:00 am PT) – October 30, 2026 (10:00 am PT)**; a project counts as "runs on Nebius" only if it makes a runtime call to the Token Factory inference API or runs on Nebius AI Cloud compute, and uses at least one NVIDIA open source model. All facts below are from Nebius's and Devpost's official pages, read 2026-10-17; a link follows each set of facts.

## 1. How to join the Nebius Builder Program as a hackathon entrant

The Official Rules (§4, "How To Enter") say: "Entrants can join the Nebius Builder Program and get credits for Nebius Token Factory, Tavily, and Nebius Academy — plus training, office hours, and access to the builder community." — https://nebiusglobalaihackathon.devpost.com/rules

Steps, in order:

1. **Register for the hackathon on Devpost** (free Devpost account, "Join Hackathon" button) — https://nebiusglobalaihackathon.devpost.com/ and rules §4: https://nebiusglobalaihackathon.devpost.com/rules
2. **Claim the hackathon's own $25 Token Factory credits** via the form linked from the hackathon's official Resources page, entering the activation code shown there (see §2 below) — https://nebiusglobalaihackathon.devpost.com/resources
3. **Join the Nebius Builder Program** at the official program page — https://dev.nebius.com/builders — by completing the registration form. Per the program's official Service-Specific Terms (§B.1), the form requires: "name, email address, company or university name, role, country, a description of what Customer is building, and acceptance of these Service-Specific Terms." — https://nebius.com/builders-terms-and-conditions
4. **Verify your email.** Terms §B.2: "Customer must verify its email address via the double opt-in verification email sent upon registration. Programme membership will not become active until email verification is complete." — https://nebius.com/builders-terms-and-conditions
5. **Receive and redeem the promo codes** issued on successful registration and verification (terms §C.1). Token Factory codes are redeemed inside the Token Factory console (balance → Top up → "With promo code"), per the Token Factory billing docs — https://docs.tokenfactory.nebius.com/other-capabilities/billing-new

Registration gotchas from the same terms (§B): one account per verified email address; Nebius may limit signups to one per IP address per 24 hours; "Registrations from disposable email domains will be blocked. Corporate and educational email addresses are preferred; registrations using personal email addresses may be subject to additional quality assurance review."; all registrations go through country-based screening and sanctions compliance checks. — https://nebius.com/builders-terms-and-conditions

## 2. Credits: amounts and how long they last

| Credit | Amount | Where from | Expiry |
|---|---|---|---|
| Token Factory (hackathon promo form) | $25 | Form linked from the Devpost Resources page; "Be sure to enter NEBIUS-DEVPOST-GLOBAL26 as your activation code" — https://nebiusglobalaihackathon.devpost.com/resources (form itself: https://nebius.com/promo-code?utm_promo_event_code=2026-devpost-global-ai-hack&utm_promo_code_type=Token_Factory&utm_promo_activation_code=NEBIUS-DEVPOST-GLOBAL26) | Not stated on the Resources page — see Unsure about |
| Token Factory (Builder Program) | $25 | Builder Program, terms §C.1: "promotional credit codes for: (i) USD $25 in Nebius Token Factory credits" — https://nebius.com/builders-terms-and-conditions | 90 days from issuance (terms §C.2) |
| Tavily (Builder Program) | $25 | Builder Program, terms §C.1: "(ii) USD $25 in Tavily partner credits" — https://nebius.com/builders-terms-and-conditions | 90 days from issuance (terms §C.2) |

The Resources page confirms the two Token Factory amounts stack: after the form's $25, it says to "Get another $25 Token Factory credits by joining the Nebius Builders Program." — https://nebiusglobalaihackathon.devpost.com/resources

Expiry wording (terms §C.2, quoted): "All promotional credits are nonrefundable, nontransferable, and expire 90 days from the date of issuance. Expired credits are forfeited and shall not be reinstated or exchanged for cash or any other consideration." — https://nebius.com/builders-terms-and-conditions

Also included with Builder Program membership (program page, https://dev.nebius.com/builders): $100 LangSmith credit, $100 Toloka credit, Nebius Academy member-only courses and certification at a member-only rate of $1 per certificate (terms §D), monthly office hours with Nebius engineers (terms §F). Separately, Token Factory gives every first-time sign-up "$1 in trial credit, valid for 30 days" (billing docs, link in §3). Attendees of the in-person Builders & Brews events "can also unlock additional Nebius AI Cloud, Token Factory, Tavily credits" (Resources page) — amounts not stated there.

Usage restriction to know (terms §H.2): members must not "use Programme credits for production workloads, large-scale commercial deployment, or any revenue-generating activity beyond prototyping and experimentation"; Nebius may auto-pause an account if monthly consumption exceeds the credit allocation by more than 30% (§H.4). After credits run out or expire, use continues pay-as-you-go (terms §C.3). — https://nebius.com/builders-terms-and-conditions

**Timing note:** because Builder credits die 90 days after issuance and submissions close October 30, 2026 (10:00 am PT), credits claimed on the read date (2026-10-17) would last until roughly mid-January 2027 — covering the deadline and the December 1–15, 2026 Judging Period, during which the project must stay available for testing (see §5). Dates: https://nebiusglobalaihackathon.devpost.com/rules

## 3. Is a credit card required? (exact wording)

**To join the Builder Program: no card is mentioned anywhere in its official terms.** Registration is the form plus double opt-in email verification (§B.1–B.2), and the terms describe the program as: "The Programme is a free, named membership layer for AI builders and developers…" (§A). — https://nebius.com/builders-terms-and-conditions

**To create a Token Factory account — which you need in order to redeem and spend the Token Factory credits: yes, a bank card is required.** Token Factory's official billing documentation states, verbatim:

> "When you sign up for Nebius Token Factory, you are prompted to create a billing account during onboarding. Billing setup is mandatory—you cannot complete onboarding without it. **Setting up a billing account requires a bank card.**"

— "Billing & Consumption," Nebius Token Factory documentation: https://docs.tokenfactory.nebius.com/other-capabilities/billing-new

The same page adds that with a bank card on file, Token Factory "debits your balance in real time" and auto-charges the card if the balance goes negative or a billing threshold is reached, and that a failed card charge suspends the account. A bank-transfer payment method exists but is "available to companies only and are not supported for individual accounts." Whether the separate hackathon promo-code form (nebius.com/promo-code) or Tavily's redemption of the $25 partner credit independently demands a card is not stated on the Nebius pages read — see Unsure about.

## 4. NVIDIA open models on Token Factory

The rules require "at least one NVIDIA open source model" but publish no closed eligibility list — any NVIDIA open source model served on Token Factory or Nebius AI Cloud qualifies (§5 below). The models Nebius's own pages name as the hackathon's core lineup are the Nemotron 3 family — the Devpost overview tells builders to "Power it with Nemotron models on Nebius through Token Factory. Reach for Nemotron 3 Ultra when you need serious reasoning, and let Nano or Super handle the fast, everyday calls." — https://nebiusglobalaihackathon.devpost.com/

| Model | On Token Factory (official source) | Context length | Price per 1M tokens on Nebius |
|---|---|---|---|
| NVIDIA Nemotron 3 Nano (30B total / 3B active) | Core hackathon lineup — Devpost overview and rules, links above | Up to 1M tokens (NVIDIA's Nemotron 3 family announcement) | Not published on Nebius's public pages — see note below |
| NVIDIA Nemotron 3 Super (120B total / 12B active) | Nebius blog: "NVIDIA Nemotron 3 Super is now available on Nebius Token Factory… 120B parameters, 12B active" — https://nebius.com/blog/posts/nemotron3-super-now-available | "Up to 1M token context" (same Nebius blog post) | Not published on Nebius's public pages — see note below |
| NVIDIA Nemotron 3 Ultra (550B total / 55B active) | Core hackathon lineup — Devpost overview and rules, links above | Unsure from the Nebius/Devpost pages read (not stated there) | Not published on Nebius's public pages — see note below |
| NVIDIA Nemotron 3.5 Lightning | Nebius Q3 release notes list it among models added to Token Factory: "The expanded model lineup includes… NVIDIA Nemotron 3.5 Lightning…" — https://nebius.com/release-notes/posts/q3-2026 | Not stated in the Nebius pages read | Not published on Nebius's public pages — see note below |
| NVIDIA Nemotron Nano 2 VL (multimodal) | Nebius October digest: Token Factory "supports a growing library of models, including the NVIDIA Nemotron Nano 2 VL" — https://nebius.com/blog/posts/digest-october-2025 | Not stated in the Nebius pages read | Not published on Nebius's public pages — see note below |

**About the missing prices:** Nebius does not publish a public per-model price table for Token Factory on the pages checked (the public prices page, https://nebius.com/prices, covers AI Cloud GPU/compute rates, not per-token model rates; per-model prices appear in the Token Factory console/catalog, which requires the account this task's rules say not to create). Third-party price trackers publish conflicting figures for Nebius's Nemotron rates (for example, two trackers disagree on Nemotron 3 Super's Nebius output price), so no third-party figure is quoted here as Nebius's price. Nebius's own developer cookbook does publish dated per-model prices for some non-NVIDIA Token Factory models (e.g. GLM/Qwen, "checked on September 5, 2026"), which confirms prices are model-specific and change over time — check the console catalog after sign-up for the live Nemotron rates: https://dev.nebius.com/cookbook/openhands-agent-canvas

Physical AI track entrants should note the overview also names NVIDIA GR00T, Cosmos and Sonic models, run with Nebius Serverless Jobs/Endpoints — https://nebiusglobalaihackathon.devpost.com/

## 5. What else an entrant must do so the project counts as "runs on Nebius"

The Official Rules (§4, "Project Requirements") define it exactly:

> "Entrants must create a working software application that runs on either Nebius Token Factory or Nebius AI Cloud and uses at least one NVIDIA open source model…" and "'Runs on Nebius Token Factory or Nebius AI Cloud' means the project makes a runtime call to the Token Factory inference API, or is deployed/run using Nebius AI Cloud compute (Serverless Jobs, Serverless Endpoints, or DevPods)."

— https://nebiusglobalaihackathon.devpost.com/rules

So a static mock-up, a local-only model, or calling a different provider's endpoint does not count: at runtime the project must actually hit the Token Factory inference API (base URL https://api.tokenfactory.nebius.com/v1/, per the Token Factory quickstart: https://docs.tokenfactory.nebius.com/) or run on Nebius AI Cloud compute, with at least one NVIDIA open source model in the loop. Deploying on Nebius Serverless Endpoints or Serverless Jobs is "encouraged… though neither is required" (Best Apps and Agents track text, rules §4).

Full submission checklist from the same rules (§4, "Submission Requirements"), all due by **October 30, 2026, 10:00 am PT**:

- Enter one of the four tracks (Coding and Agentic Engineering; Best Apps and Agents; Personal AI; Physical AI).
- Working demo / hosted app / test-build URL (not required for Physical AI).
- Text description of features and functionality.
- Public code repository (GitHub, GitLab, or Bitbucket) containing all source and instructions, with an open source license file (e.g. Apache 2.0, MIT, MPL 2.0) "detectable and visible at the top of the repository page (in the About section)," plus a README with setup instructions that highlights how NVIDIA Nemotron or other NVIDIA open source models were used, where Token Factory accelerated the workflow, and any other Nebius tools/services used.
- Demo video under 3 minutes, publicly visible on YouTube, showing the project functioning; no third-party trademarks or copyrighted music without permission. Physical AI: at least 1 minute of the hardware/robot operating, or of the key application modules in action.
- Feedback on Nebius Token Factory, AI Cloud, and any NVIDIA tools/models used (this is a required submission field — and separately prize-eligible).
- If the project existed before the Submission Period: a written explanation of what was significantly updated during the Submission Period (projects must be new or significantly updated after August 26, 2026).
- Keep the project available "free of charge and without any restriction, for testing, evaluation and use by the Sponsor, Administrator and Judges until the Judging Period ends" (Judging Period: December 1–15, 2026).
- All materials in English, or with English translations.
- Multiple submissions are allowed if each is unique and substantially different. Optional: Builders & Brews attendees select their city on the submission for the $500 City Winner Awards.

Eligibility basics (rules §3): individuals at least the age of majority where they reside, teams, and organizations may enter; residents/domiciles of Brazil, Quebec, Russia, Crimea, Cuba, Iran, North Korea and other comprehensively OFAC-sanctioned countries are excluded, as are Promotion Entities, their employees/agents and immediate family/household, judges and their employers, and conflict-of-interest cases. — https://nebiusglobalaihackathon.devpost.com/rules

## Sources

- Devpost hackathon overview — https://nebiusglobalaihackathon.devpost.com/ (read 2026-10-17)
- Devpost Official Rules — https://nebiusglobalaihackathon.devpost.com/rules (read 2026-10-17)
- Devpost Resources page (credit forms and activation code) — https://nebiusglobalaihackathon.devpost.com/resources (read 2026-10-17)
- Nebius Builder Program page — https://dev.nebius.com/builders (read 2026-10-17)
- Service-Specific Terms for Nebius Builder Program (last modified September 2026) — https://nebius.com/builders-terms-and-conditions (read 2026-10-17)
- Nebius Token Factory docs, "Billing & Consumption" (updated 2026-10-13) — https://docs.tokenfactory.nebius.com/other-capabilities/billing-new (read 2026-10-17)
- Nebius Token Factory docs, Quickstart — https://docs.tokenfactory.nebius.com/ (read 2026-10-17)
- Nebius blog, "NVIDIA Nemotron 3 Super now available on Nebius Token Factory" — https://nebius.com/blog/posts/nemotron3-super-now-available (read 2026-10-17)
- Nebius Q3 release notes — https://nebius.com/release-notes/posts/q3-2026 (read 2026-10-17)
- Nebius prices page (AI Cloud rates; checked for Token Factory rates) — https://nebius.com/prices (read 2026-10-17)

## How I checked it

Every fact above traces to an official Nebius or Devpost page listed in Sources, fetched and read on 2026-10-17. Credit amounts and expiry come from the Builder Program's own Service-Specific Terms (quoted verbatim) and are cross-confirmed by the program page's perk list ($25 Token Factory / $25 Tavily) and by the Devpost Resources page, which is also the source for the second, stackable $25 and its activation code. The credit-card answer quotes Token Factory's own billing documentation word for word. The "runs on Nebius" definition and the submission checklist are taken from the Official Rules §4, not from the marketing overview; where the overview and rules both speak, the rules' wording is used. Model availability is sourced per model to a Nebius page; no price or context figure is stated in §4 unless an official page states it. No account was created, nothing was purchased, and no one was contacted, per the task rules.

## Unsure about

- **Per-model prices for the Nemotron family on Token Factory** — not published on any public Nebius page found; they appear to live in the Token Factory console catalog (login required, out of scope for this task). Third-party trackers conflict with each other on Nebius's rates, so none is quoted. Unsure.
- **Context length for Nemotron 3 Ultra, Nemotron 3.5 Lightning, and Nemotron Nano 2 VL as served on Token Factory** — not stated on the Nebius/Devpost pages read (served context can differ from the model family's headline spec). Unsure.
- **Expiry of the hackathon form's $25 Token Factory credit** — the Resources page states no expiry for that code; the 90-day figure is documented only for Builder Program credits (terms §C.2). Unsure whether the same 90 days applies.
- **Whether the nebius.com/promo-code form itself asks for payment details** — the page is a JavaScript form whose fields could not be read from the public fetch; only its URL and the Resources page's instructions were verifiable. Unsure.
- **Whether Tavily requires a payment method to redeem the $25 partner credit** — redemption is governed by Tavily's own terms (per Builder terms §C.4); Tavily's pages were not part of this check. Unsure.
- **Whether Builder Program credits can be applied before Token Factory's mandatory billing setup** — the docs describe promo-code redemption inside the console after onboarding, and onboarding requires billing setup; no documented exception for promo users was found. Unsure.
- The Builder Program page's FAQ ("the program is free to join for everyone") and its full join-button target could not be read beyond the program page itself — https://dev.nebius.com/builders is the official entry point cited throughout.
