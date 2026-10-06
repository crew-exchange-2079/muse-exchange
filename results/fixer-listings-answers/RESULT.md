# Addendum to the listing scan: crew answers folded in

**Task:** `tasks/fixer-listings-answers/TASK.md` — read the crew's `ANSWERS.md` (checked 2026-10-05) against `results/fixer-listings-scan/RESULT.md`, say what changes, price flood insurance for a Zone AE house, and give a final top 3 with all-in costs. Short version below; the scan itself is not rewritten.

## What the answers settled

- **424 Spring Ave's price: $98,500 is most likely current.** The crew reconstructed the ladder — $139,900 → $119,900 → $104,900 → minus the $6.4K cut I saw = **exactly $98,500**. The $139,900 I costed against was the stale original/MLS-feed figure. Confidence medium (arithmetic inference, no single dated page). The house parcel itself is 0.11 acre per county records (taxes ≈$893/yr), so the 0.61 acre in my entry is the house **plus separate parcels** — their inclusion still rests on listing text only, and the garage apartment's zoning/legality is unverified. Title and survey checks move from "diligence" to "essential."
- **Flood zones (FEMA NFHL at geocoded points — parcel-exact checks still required):** 515 Center Ave, 106 E Main St and 103 Washington St are **Zone AE**; 424 Spring Ave and 194 Anglin Run are **Zone X (minimal hazard)**, clean within 75 m; 920 E Park Ave is X at the point but has AE within 75 m, and the state's risk report for a same-street address shows AE/floodway with 1.2 ft modelled depth — treat E Park as *unresolved*, leaning cautious; 38 Kitson St is X with an AE floodway within 25 m — likely affected in July 2026, unconfirmed.
- **515 Center Ave:** the street is confirmed in the July 2026 flood (city recovery lists include Center Ave; town water marks reached up to 7 ft on some buildings; ~30 Weston homes need demolition). No source gives this house's depth — the "price it as a possible gut job" advice stands, plus a new item: ask the Weston floodplain administrator about **substantial-damage rules** before assuming a like-for-like rebuild is even permitted.
- **751 Snider St:** the lease ($1,600/mo through July 2027) is confirmed as listing text — and the listing adds that it sells as-is **after city code-enforcement repair items are completed "over the next 60 days."** New flag: find out what the citations were before treating the discount as cosmetic.

## Does the ranking change? Yes — at positions 2–4

- **#1 strengthens.** Spring Ave at $98,500 in a Zone X location is exactly what the brief wanted: the lowest all-in in the scan *without* flood baggage.
- **106 E Main St drops from #2 to #4.** Zone AE doesn't change its repair budget, but it adds mandatory flood insurance on any federally backed mortgage, an annual carrying cost (below), and resale friction in a town that just watched Weston flood. Still the raw-value champion — just no longer the clean second pick.
- **103 Washington St drops out of the top 5 reckoning.** Zone AE *plus* an AE floodway within 25 m, on top of the seller's flood-insurance offer and the unhooked water — the crew is right to budget it at the high end plus insurance. My #5 (Anglin Run) passes it on risk alone.
- **194 Anglin Run moves up** — Zone X, clean surroundings, youngest house. **920 E Park Ave holds a top-3 spot provisionally**: X at the point, but if the parcel-exact check puts it in AE, swap it with Anglin Run (order between them is close either way).

## Flood insurance for a Zone AE house — rough cost

Under NFIP's Risk Rating 2.0, price is property-specific (elevation, distance to water, foundation, rebuild cost), and a **buyer is new business — priced at full risk from day one**, not on the seller's possibly subsidised legacy premium. Reference points (sources below): the typical NFIP policy nationally runs ≈**$1,100/yr** (AP's 2026 analysis of FEMA data); single-family homes in high-risk (SFHA/AE) zones commonly fall in a **$1,200–$4,000/yr** band, with inland, lower-value WV houses plausibly at the lower half. **Planning figure for these houses: ~$1,000–$2,500/yr — i.e. roughly $5K–$12.5K across a 5-year hold** — on top of the all-in cost, and effectively non-optional with a mortgage in Zone AE. Private flood insurance can undercut NFIP for some properties and is worth quoting both ways. An elevation certificate and the exact BFE gap move the number more than the zone label does, so this is a quote-before-offer item, not a rounding error.

## Final top 3 (price + typical repair = all-in)

| # | House | List | Typical repair | All-in | Flood |
|---|---|---|---|---|---|
| 1 | **424 Spring Ave, Clarksburg** | $98,500 | $48K | **≈$146.5K** | Zone X |
| 2 | **920 E Park Ave, Fairmont** | $124,900 | $34K | **≈$159K** | X at point, AE within 75 m — parcel check decides |
| 3 | **194 Anglin Run Rd, Philippi** | $145,500 | $31K | **≈$176.5K** | Zone X |

First reserve: 106 E Main St, Buckhannon — $75,000 + $56K ≈ **$131K all-in**, the cheapest of all, if the buyer accepts Zone AE plus ~$1K–$2.5K/yr flood insurance and gets eyes on the damaged room and the asbestos siding.

## How I checked it / unsure about

Read the task and `ANSWERS.md` in full; every change above traces to a crew finding (price ladder arithmetic, NFHL point queries, the Weston recovery lists, the Snider St listing text). Spring Ave's new all-in simply re-runs my scan's own repair budget ($48K) against the corrected price. Flood-insurance figures are from public reporting on NFIP/Risk Rating 2.0 — AP's analysis via Carrier Management (Sep 2026), a Neptune Flood research summary (2026), and an NFIP-vs-private comparison of SFHA premium ranges — they are planning ranges, not quotes. Still unresolved, and stated as such in both documents: the zone results are **point geocodes** (a lot can sit tens of metres off — parcel-exact WV Flood Tool checks remain necessary, E Park Ave above all); whether Spring Ave's extra parcels and apartment actually convey; Center Ave's water depth; and what Morgantown's code-enforcement items on Snider St actually were. Scanned for personal-data patterns before committing, per the repo's public-only rule. Commit message: `result fixer-listings-answers`.
