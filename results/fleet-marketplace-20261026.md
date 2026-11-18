RESULT fleet-marketplace-20261026

# Cheap used computers for a small home-lab fleet — north-central WV / shipped cheap

Read date for every fact: 2026-10-26. Home base for distances: Bridgeport, WV. "Shipped" listings have no meaningful drive distance; road miles below are approximate. Every price below is the asking price as shown on the linked page on the read date — eBay text fetches do not always show a live "ended" flag, so confirm availability before paying, especially where a listing's last revision is months old (flagged in the table).

Headline: the local tiers are dry again. No current Facebook Marketplace, Craigslist, GovDeals, or r/homelabsales computer listing for the I-79 corridor surfaced in public text search on 2026-10-26 (details under "Source tiers checked"). Everything in the table is eBay, shipped free or under $25 — except the two rack servers, where freight-scale shipping is the point. No RTX 3090, A4000, or P40 exists anywhere near the $350 cap: the Oct 2026 used floor for a 3090 is $1,350, and A4000s run $800–$850.

## Best listings

### (a) Used enterprise gear

| # | Listing | Price + shipping | Location / distance | Key specs | Est. idle watts | Post date / read date | Link | Verdict |
|---|---|---|---|---|---|---|---|---|
| A1 | Mellanox ConnectX-3 Pro MCX312C-XCCT, dual-port 10GbE SFP+ | $19.45, free shipping | Dover, NJ — shipped | 2× SFP+ 10GbE, PCIe x8, high profile | ~5 W (unsure) | Last revised Mar 6, 2026; read 2026-10-26 | https://www.ebay.com/itm/168190629285 | Good deal — the standard cheap 10GbE NIC at the usual $20–25 level, but note ConnectX-3 drivers were dropped from ESXi 8.0 and RHEL 10, so this is a Linux/Proxmox part, not a long-horizon one. |
| A2 | Dell PowerEdge R630 CTO chassis, 2× PSUs | $199 or Best Offer, free shipping | Walnut, CA — shipped | Bare chassis: no CPUs, no RAM, no HDDs, no cards | n/a (no parts) | Last revised May 11, 2026; read 2026-10-26 | https://www.ebay.com/itm/286304149618 | Skip as a fleet node — $199 buys an empty shell; CPUs + RAM + drives push it past a complete used R630. Fair only if you already hold spare E5 v3/v4 parts. |
| A3 | Dell PowerEdge R630, 2× E5-2630 v4, 64 GB DDR4, 2× 1.2 TB SAS, H730 | $445, free shipping | Prior Lake, MN — shipped | 2× 10-core 2.2 GHz, 64 GB, H730, 1U | ~80 W (estimated, unsure) | Last revised Apr 6, 2026; read 2026-10-26 | https://www.ebay.com/itm/168265208356 | Fair — complete and free-shipped, but $445 is well above the ~$257 complete-R630 benchmark price, and the listing data is from April. Offer low or wait. |
| A4 | Dell PowerEdge R730 8SFF, 2× E5-2637 v3, 2× 1100 W PSUs | $300 or Best Offer + $40.78 shipping | Liberty Hill, TX — shipped | 2× 4-core 3.5 GHz, RAM/storage not stated in fetched text | ~90 W (estimated, unsure) | Read 2026-10-26 (index crawl 137 days ago) | https://www.ebay.com/itm/376870981941 | Fair — good 2U box with 10GbE-capable X540 mentioned in the title, but $40.78 shipping breaks the $25 cheap-shipping bar and the RAM/drive spec is not in the fetched text. |
| A5 | APC Back-UPS Pro BX1500M, 1500 VA / 900 W | $215 or Best Offer, free shipping | Kennesaw, GA — shipped | 10 outlets, AVR, LCD | n/a | Last revised Jan 10, 2026; read 2026-10-26 | https://www.ebay.com/itm/196780034842 | Skip — a used UPS at $215 with unknown battery age is poor value against the old small-UPS ceiling of $30; budget a replacement battery on top if you buy it at all. |

### (b) GPUs with 12 GB+ VRAM under $350

| # | Listing | Price + shipping | Location / distance | Key specs | Est. idle watts | Post date / read date | Link | Verdict |
|---|---|---|---|---|---|---|---|---|
| B1 | Gigabyte GeForce RTX 3060 Gaming OC 12 GB | $299.99, free shipping | Houston, TX — shipped | RTX 3060, 12 GB GDDR6, PCIe 4.0, box included | ~12 W (estimated) | Last revised Jun 27, 2026; page served 2026-10-26 | https://www.ebay.com/itm/358728598511 | Good deal — under the Oct 2026 used floor of $320–$349.97 for a 3060 12 GB, from a 99.6% seller with 5.2K sales; confirm it is still live before paying, since the last revision is June. |
| B2 | Nvidia Tesla P100 16 GB HBM2 PCIe | $49.99 or Best Offer + $9.99 shipping | Eau Claire, WI — shipped | P100, 16 GB HBM2, PCIe 3.0 x16, passive heatsink only | ~25 W (unsure) | Read 2026-10-26 (index crawl 123 days ago) | https://www.ebay.com/itm/117267305999 | Good deal on price — well under the ~$112 current lowest-average for a P100, but it is passive (you must add airflow), has no display outputs, and is Pascal (no bf16). Inference-only part. |
| B3 | Nvidia Tesla P100 16 GB HBM2 PCIe, seller warranty | $117.50 or Best Offer, free shipping | Sunnyvale, CA — shipped | P100, 16 GB HBM2, PCIe 3.0 x16, passive heatsink only | ~25 W (unsure) | Last revised Jun 1, 2026; read 2026-10-26 | https://www.ebay.com/itm/306142524706 | Fair — right at the ~$112 market average with free shipping and a stated warranty, so it beats B2 only if B2 is gone; same passive-cooling and Pascal caveats. |

No RTX 3090 under $350: Oct 2026 used asking range $1,350–$1,539.99 — https://www.buysellram.com/blog/nvidia-consumer-gpu-market-update/ — against the Oct 2026 eBay sold median of ~$1,522 noted in prior work. No A4000 listing found at any price in this search; the going used range is $800–$850 — https://pcserverandparts.com/news/used-graphics-card-buying-guide-2026/ . No P40 listing found. No RTX 3060 12 GB under $299.99 verified live today besides B1; an EVGA 3060 12 GB at $259.99 with free shipping (Ontario, CA) appeared in the search index but its crawl is 262 days old, so it is not counted as a live listing — https://www.ebay.com/itm/406672158795 .

### (c) Cheap gaming PCs under $400 with a usable GPU

| # | Listing | Price + shipping | Location / distance | Key specs | Est. idle watts | Post date / read date | Link | Verdict |
|---|---|---|---|---|---|---|---|---|
| C1 | Custom PC, i5-8500, GTX 1660 Ti | $350 or Best Offer, free shipping | Akron, OH — ~210 mi / shipped free | i5-8500 (6-core), 12 GB RAM, 256 GB SSD, GTX 1660 Ti 6 GB, Win 11, tower | ~45 W (estimated) | Read 2026-10-26 (index crawl 167 days ago) | https://www.ebay.com/itm/358545322543 | Fair — the only complete sub-$400 gaming box found with free shipping, and the 1660 Ti is genuinely usable, but 12 GB RAM is thin and the listing data is months old; verify before paying. |
| C2 | Gaming PC bundle, MSI Z170A, i5-6600, GTX 1060 | $155 + $12.22 shipping | League City, TX — shipped | i5-6600, 16 GB RAM, GTX 1060 (VRAM not stated; assume 6 GB, unsure), tower | ~40 W (estimated) | Last revised Mar 17, 2026; read 2026-10-26 | https://www.ebay.com/itm/257395278386 | Fair — the cheapest route to a usable-GPU box at $167.22 all-in, but a 6th-gen platform is a dead end with no upgrade path; buy it as a disposable node, not a keeper. |

### (d) Low-power mini PCs under $150

| # | Listing | Price + shipping | Location / distance | Key specs | Est. idle watts | Post date / read date | Link | Verdict |
|---|---|---|---|---|---|---|---|---|
| D1 | Lenovo ThinkCentre M720q Tiny, i5-8400T | $90 or Best Offer + $13.75 shipping | Sidney, NY — shipped | i5-8400T (6-core), 8 GB RAM, 256 GB SSD, Win 11 Pro, AC cord | ~11 W (estimated) | Read 2026-10-26 (index crawl 10 days ago) | https://www.ebay.com/itm/147638710050 | Good deal — $103.75 all-in for a 6-core 8th-gen Tiny is the cheapest real node in this sweep; 8 GB RAM is the only weak spot. |
| D2 | Lenovo ThinkCentre M920q, i5-8500T | $129.99, free shipping | Fairfield, US (state not shown) — shipped | i5-8500T (6-core), 8 GB RAM, 256 GB NVMe, Win 11, near-flawless chassis | ~11 W (estimated) | Read 2026-10-26 (index crawl 10 days ago) | https://www.ebay.com/itm/137848891417 | Good deal — free shipping, clean condition note, 8th-gen 6-core; same 8 GB RAM caveat as D1. |
| D3 | Dell OptiPlex 7060 Micro, i5-8500T | $140 or Best Offer, shipping varies (not shown) | Location not shown — shipped | i5-8500T (6-core), 16 GB RAM, 128 GB SSD, Win 11 Pro, Wi-Fi | ~13 W (measured for this class; see below) | Listed within 3 days before read date; page served 2026-10-26 | https://www.ebay.com/itm/920061209839 | Good deal if shipping is ≤$25 — the only mini PC here with 16 GB RAM under $150, and the freshest listing in the table; confirm the shipping quote before buying, since it is not shown. |
| D4 | Lenovo ThinkCentre M920q, i5-8500T | $145 or Best Offer + $14.45 shipping | Suffern, NY — shipped | i5-8500T (6-core), 8 GB RAM, 256 GB NVMe, Win 11 Pro, Wi-Fi/Bluetooth | ~11 W (estimated) | Read 2026-10-26 (index crawl 3 days ago) | https://www.ebay.com/itm/237138420784 | Fair — $159.45 all-in edges over the $150 line once shipping is added, so it only wins if D1–D3 are gone; otherwise identical hardware for more money. |

Price anchors for the verdicts: used i5 mini PCs with 16 GB / 256 GB typically trade at $100–$200 — https://www.howtogeek.com/self-hosted-stack-replaces-google-one-dropbox-plex-for-a-one-time-cost/ ; mini-PC idle power in this class is 11–13 W as measured by ServeTheHome for the EliteDesk 800 G4 Mini and OptiPlex 7070 Micro — https://computingforgeeks.com/best-used-tiny-pc-homelab/ ; RTX 3060 12 GB Oct 2026 used floor $320–$349.97 — https://www.buysellram.com/blog/nvidia-consumer-gpu-market-update/ ; Tesla P100 current lowest average $112 — https://gpupoet.com/gpu/learn/card/nvidia-tesla-p100 ; complete R630 benchmark ~$257 — https://pcserverandparts.com/news/best-used-server-for-home-lab-2026/ .

## The 3 to buy first

1. **D1 — M720q at $103.75 all-in.** Cheapest true node, 6-core 8th-gen, leaves budget for a RAM upgrade to 16 GB.
2. **D2 — M920q at $129.99 with free shipping.** Same class as D1 with a cleaner condition note and no shipping gamble; buy two of D1/D2 and you have a Proxmox pair for ~$234.
3. **B1 — Gigabyte RTX 3060 12 GB at $299.99 with free shipping.** The only 12 GB+ gaming GPU under $350 verified on a live page today, and it is below the October used floor; it turns any of the mini-PC-plus-dock or tower nodes into a 14B-model inference box. Confirm it is still listed before paying, given the June revision date.

## Source tiers checked

- **Facebook Marketplace (tier 1):** no public listing pages surfaced without login in any search on 2026-10-26; the search index returned no facebook.com marketplace item pages for Morgantown/Fairmont/Clarksburg computer queries. Consistent with the login wall observed in prior work. No sellers contacted, no login attempted.
- **Craigslist Morgantown / Huntington / Pittsburgh (tier 2):** text search returned only stale guides and aggregator pages, no current computer listings. A live browse of the three regions' for-sale pages would be needed to confirm a true zero — not available in this text-only pass.
- **GovDeals / surplus (tier 3):** no live WV computer lots found in text search. Watch items, not listings: WVU sells surplus via GovDeals — https://financialservices.wvu.edu/property-management/surplus/suplus-property-sales — and the WV State Agency for Surplus Property sells at its Dunbar warehouse (Mon–Fri 9 AM–4 PM) and via GovDeals, but states inventory is not viewable online — http://www.state.wv.us/admin/purchase/surplus/surplusFAQs.html . A Dunbar walk-in is the only way to see current stock.
- **eBay (tier 4):** all table listings above; shipping and location taken from each item page or its search-index record.
- **r/homelabsales, last 14 days (tier 5):** no posts surfaced in the search index for the last 14 days; nothing from this tier is in the table.

## How I checked it

- Read date for all facts: 2026-10-26. Public web only; no login, no account, no purchase, no messages or comments to anyone.
- Searched each tier in the brief's order (Marketplace, Craigslist, GovDeals/WV surplus, eBay, r/homelabsales), then ran item-specific eBay searches for each group (mini PCs, 3060/P100, R630/R730, 10GbE NICs, UPS, gaming desktops).
- Two eBay pages were opened live on the read date and their prices confirmed in the fetched text: the Gigabyte RTX 3060 12 GB ($299.99, free shipping) and the OptiPlex 7060 Micro ($140, "just listed" within 3 days). All other listings rest on search-index records, which is why their crawl/revision dates are shown and availability must be re-confirmed.
- Verdict prices were checked against October 2026 market trackers (buysellram, gpupoet, pcserverandparts) and the How-To Geek mini-PC price band, each linked above.
- Distances from Bridgeport, WV are approximate road miles for the one drivable candidate (Akron, OH); shipped items are marked shipped rather than given a drive distance.
- Nothing was pushed to GitHub and nothing was written to any repo, per the task rules.

## Unsure about

- Availability of every listing except the two opened live: eBay search-index records can lag the live site by days to months, so any listing with an old crawl or revision date may already be sold — re-check each link before paying.
- Post dates: eBay item pages fetched here do not show an original list date, so the table gives the last revision date or index-crawl date instead; true post dates are unsure.
- Locations: the OptiPlex 7060 Micro page does not show a seller location in fetched text, and the $129.99 M920q shows only "Fairfield" with no state — distances for those two are unsure.
- Idle watts: all watt figures are estimates from the cited class measurements or are marked unsure; none was measured on the exact unit listed.
- Craigslist and r/homelabsales: a zero from text search is not proof of zero live listings — both need a live browse to confirm.
- GovDeals: no live WV computer lot was found, but auctions open and close daily; the Dunbar warehouse stock is not published online, so a walk-in could hold something this search missed.
- RTX 3090 / A4000 / P40 at the cap: none found, and the price anchors say none should be expected — a sub-$350 3090 or A4000 listing should be treated as a scam or a mislabeled card until proven otherwise.

END fleet-marketplace-20261026
