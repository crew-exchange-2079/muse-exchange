RESULT hw-market-scan-20261026

# Used and refurbished compute for a small AI homelab — market-wide scan

Read date for every fact: 2026-10-26. Prices are what was seen on that date unless a different date is stated. This complements the earlier local-listing task fleet-marketplace-20261026 and deliberately does NOT repeat its listings. The homelab today: one RTX 3090 (24 GB) in a desktop, plus 2013-era dual-Xeon E5 v2 servers (DDR3, InfiniBand FDR). The goal: a modern, quieter, more efficient machine (or a few) in the next 6–18 months.

Headline: it is a split market, not a dump. Consumer Ampere cards useful for local AI have risen on AI demand, not fallen. The genuine bargains are headless datacentre cards (above all the Tesla P40) and 2nd-gen Xeon Scalable nodes with cheap DDR4 — and the trap is the old rack: cheap to buy, expensive to run, loud forever. Buy one modern machine for AI work; cluster quiet mini PCs, not rack servers, if you must cluster at all.

## Summary table

| Option | Typical price, seen 2026-10-26 | Fast memory | Power (idle / loaded) | Noise | Good for | Main gotcha |
|---|---|---|---|---|---|---|
| Tesla P40, cooled | $250–$325 | 24 GB GDDR5 | ~25 W idle (unsure) / ~250 W TDP | Fan mod dependent | Cheapest 24 GB inference | Passive card, no display, old arch, int-quantised inference |
| RTX 3060 12 GB | $320–$350 budget | 12 GB GDDR6 | 8–20 W idle / 170 W TDP | Quiet tower card | Plug-and-play small models, agents | Only 12 GB; floor now equals new floor |
| RTX 3090, used | $1,350–$1,550 | 24 GB GDDR6X, 936 GB/s | Low idle / 350 W TGP | ~37 dB load (FE) | 7B–30B serving, small LoRA | Price up ~23% since August; ex-mining pool |
| RTX 4090, used | $2,271 sold value | 24 GB GDDR6X, 1,008 GB/s | Low idle / 450 W TGP | Tower card | Faster prompt processing, fine-tuning | Same 24 GB ceiling; no NVLink; discontinued |
| Tesla V100 32 GB PCIe | $645–$660 sold examples | 32 GB HBM2 | 300 W TDP | Passive, server airflow | 32 GB NVLink-era inference | SXM2 modules cheaper but need adapter/board |
| A100 40 GB, refurb | $4,000–$6,000 | 40 GB HBM2e | 300 W TDP | Server airflow | Large-model serving, training | Live asking far higher ($12,500+ for 80 GB) |
| DGX-1, 8x V100 16 GB | $6,499 eBay | 128 GB HBM2 total | 3,200 W max | 72–100 dBA | Only cheap way to hold a big model in VRAM | 200–240 V, freight, datacentre noise |
| Dell R640 barebones | $258.88 | 0 GB as listed (verify) | 75–150 W idle budget / 300–400 W loaded | Rack fans | Cheap DDR4 node, VMs, storage | Verify RAM; rails/caddies extra |
| HP Z8 G4, 128 GB | $2,145.86 refurb | 128 GB DDR4 | Tower, quiet-ish | Desk tower | Quiet dual-Xeon desk box + GPU | Fully loaded units cost far more than bare + used RAM |
| Threadripper P620, 128 GB | $1,795 | 128 GB DDR4 | Tower | Desk tower | Lanes + RAM for multi-GPU | 64-core PRO parts still carry a big premium |
| Mac Studio M4 Max 128 GB | $3,999–$4,499 | 128 GB unified, 546 GB/s | 30–120 W load | 24–31 dB | Silent 70B serving, always-on | No CUDA; soldered memory; outgoing model |
| Strix Halo mini PC 128 GB | $3,449–$3,999 | 128 GB unified, 256 GB/s | NOT FOUND | Near-silent | Cheapest x86 128 GB; 70B Q4 | Slowest bandwidth here; ROCm not CUDA |
| Jetson Orin Nano Super | $249 | 8 GB shared, 102 GB/s | 7–25 W | Silent | Edge, robotics, learning CUDA | 8 GB ceiling; Arm64 |
| NetApp DS4246 shelf | $349–$695, no drives | 24 bays | Shelf only | Rack shelf | Cheap bulk storage | 520-byte sectors, HBA + cables extra |
| 3 old rack servers | ~$600 (estimate) | 384 GB ECC total | 450 W idle realistic | 40–65 dBA | Many independent CPU jobs | Costs MORE than a 3090 tower over 3 years |

## 1. Ex-mining GPU rigs and GPU lots

The story in October 2026 is a split market. Consumer Ampere cards that are useful for local AI have risen: the RTX 3090 is up sharply on AI demand, and the RTX 3060 12 GB now asks more than the faster RTX 3060 Ti 8 GB because VRAM, not speed, is what buyers pay for. The genuine bargains are the headless datacentre cards — above all the Tesla P40 at roughly a sixth of a 3090's price for the same 24 GB — but they are projects (passive cooling, no display output, old architectures), not plug-and-play cards.

### Prices seen 2026-10-26

| Card | VRAM | Typical used price, Oct 2026 | $/GB approx. |
|---|---|---|---|
| RTX 3090 | 24 GB GDDR6X | $1,350–$1,550 (tracker median $1,199) | $56–$65 |
| RTX 3080 10 GB | 10 GB GDDR6X | $356–$390 | $36–$39 |
| RTX 3080 12 GB | 12 GB GDDR6X | $450–$600 | $38–$50 |
| RTX 3060 12 GB | 12 GB GDDR6 | $260–$350 (sources disagree; budget $320–$350) | $22–$29 |
| RTX A4000 | 16 GB GDDR6 ECC | $785–$983 | $49–$61 |
| RTX A5000 | 24 GB GDDR6 ECC | $1,499–$2,600; vetted $2,090–$2,360 | $62–$108 |
| RTX A6000 | 48 GB GDDR6 ECC | $2,200–$2,800 bargain claims vs $4,490–$4,999 vetted | $46–$104 |
| Tesla P40 | 24 GB GDDR5 | $220–$250 bare; $250–$325 cooled | $9–$14 |
| Tesla V100 16 GB | 16 GB HBM2 | $160–$310 (SXM2 at the low end) | $10–$19 |
| Tesla V100 32 GB | 32 GB HBM2 | $645–$1,100 (PCIe higher, SXM2 lower) | $20–$34 |
| Tesla P100 16 GB | 16 GB HBM2 | $150–$260 US; $70–$120 China before shipping | $9–$16 |

Sources for the table: https://www.buysellram.com/blog/nvidia-consumer-gpu-market-update/ , https://bestvaluegpu.com/history/new-and-used-rtx-3090-price-history-and-specs/ , https://bestvaluegpu.com/history/new-and-used-rtx-3080-price-history-and-specs/ , https://gpusold.com/gpu/rtx-3090-24 , https://gpupoet.com/gpu/shop/nvidia-tesla-p100 , https://gpupoet.com/gpu/shop/nvidia-tesla-v100-32gb , https://insiderllm.com/guides/used-server-gpus-local-ai/ , https://www.thundercompute.com/blog/nvidia-a5000-pricing

Disagreements, stated not smoothed: the 3090 tracker median ($1,199) sits below the $1,350–$1,550 a buyer should budget for a normal US used card, and the direction is up (+23% on August per one October market update). The 3060 12 GB has one guide at $260–$296 against a market update at $320–$349.97 with the used floor now equal to the new floor. The A6000 $2,200–$2,800 tier is unverified bargain claims; the vetted/refurb tier actually on show is $4,490–$4,999. V100's wide range is form-factor driven: PCIe cards cost more than SXM2 modules, and SXM2 modules need an adapter or baseboard — do not compare a $160 SXM2 module with an $850 PCIe card as if they were the same purchase.

Whole mining rigs are the weakest value in this scan: the fresh October 2026 evidence is one $35 garage anecdote (9 cards, 54 GB VRAM), not a liquid market of priced, current rig listings — https://www.tomshardware.com/pc-components/gpus/reddit-user-pays-usd35-for-a-crypto-mining-rig-left-in-a-garage-and-gets-54gb-of-vram-at-65-cents-per-gb-the-first-test-for-2017-era-gpus-a-35b-parameter-ai-model-running-locally-at-over-30-tokens-per-second — and rig motherboards bottleneck multi-GPU inference over PCIe x1 risers. Rigs are generally poor value vs singles for split-model inference.

### How to judge wear on an ex-mining card

Sellers rarely prove a card mined, and mining history alone does not prove damage. Price the card on condition and test results, not on the label.

- Before paying: photos of the card, serial numbers, seller return terms. A card that cannot be returned is a gamble, not a deal.
- On arrival: physical inspection — fan bearings (spin by hand; roughness, grinding, or wobble means replacement fans), dust, bent fins, missing screws, signs of rework.
- Software identity: GPU-Z — check the exact model, VRAM size, and BIOS version against the manufacturer's original. A BIOS-flashed card (wrong clocks, wrong VRAM size, mining BIOS) is a red flag; re-flash to stock only if you know the exact original BIOS.
- VRAM test, the mining-killer check: run a VRAM stress test (OCCT VRAM test is the cited tool). Any error is a fail — VRAM errors do not heal and will corrupt inference and training.
- Heat: core, hotspot, memory junction, VRM. A hotspot-to-edge delta around 25 °C indicates dried paste. For 3090 GDDR6X specifically: sustained memory-junction temperature above ~100 °C means a repad is coming; throttling sits around 110 °C.
- Repasting and repadding is normal maintenance, with a trap: pad thickness matters. Too thick or too thin pads leave the VRAM or VRM without contact and make temperatures worse, not better. Sources for wear checks: https://web3.gate.com/crypto-wiki/article/how-to-assess-the-condition-of-a-graphics-card-after-mining-20251227 , https://emcd.io/articles/mining/is-buying-a-used-mining-gpu-worth-it/ , https://nathankeilar.com/systems/repaste-worked-vram-got-hotter , https://www.displaycard-repair.com/blog/gpu-memory-junction-temperature-too-high-gddr6x-heat-cooling-guide/ , https://digitalplater.online/how-to-identify-mining-graphics-card-ultimate-2026/

Power and noise notes: per-card idle power is NOT FOUND except the RTX 3060 (8–20 W idle, 170 W TDP). The 3090 FE runs around 37 dB under load; the A6000 blower is sourced at 32–34 dBA idle / 48–52 dBA load; no verified dB figure was found for A4000/A5000 blowers alone. Tesla cards are passive — budget real server airflow or a fitted fan mod, and treat any passive card in a still-air desktop as a card that will throttle.

Good-for and gotchas per card: the 3090 is the cheapest 24 GB CUDA inference card that is also plug-and-play, good for 7B–30B serving and small LoRA; its gotcha is price momentum and the ex-mining pool. The P40 is the cheapest 24 GB of any kind, good for int-quantised inference on a budget; its gotcha is the fan mod, no display output, and slower inference. The V100 32 GB PCIe is the cheapest 32 GB with NVLink-era pedigree; its gotcha is form-factor confusion (SXM2 vs PCIe) and age. The A4000 is the single-slot, ECC, low-power professional pick; its gotcha is price per GB ($49–$61) against the P40's $9–$14. The 3060 12 GB is the plug-and-play small-model card; its gotcha is the 12 GB ceiling.

## 2. Decommissioned enterprise and AI servers

Best value overall for this homelab: a 2nd-gen Xeon Scalable (Cascade Lake) 1U/2U node such as a Dell R640/R740, or a dual-Xeon tower such as an HP Z8 G4, bought with modest RAM and upgraded from used DDR4 — because the chassis is now a few hundred dollars, idle draw is far below the old E5 v2 fleet, and it still takes cheap DDR4 and PCIe GPUs. Worst value trap: an 8-GPU A100-class system at 2026 asking prices — the GPUs alone cost more than a whole rack of V100 or CPU nodes, and the power, noise, and 240 V requirements rule it out as a first upgrade.

### GPU servers

| System | Price, seen 2026-10-26 | Notes |
|---|---|---|
| NVIDIA DGX-1 Volta, eBay used | $6,499 or Best Offer (listing updated Oct 05, 2026) | 2x Xeon E5-2698 v4, 8x V100 SXM2 16 GB, Fairport, NY, freight shipping — https://www.ebay.com/itm/168708756603 |
| NVIDIA DGX-1, CanServers (Canada) | CAD $7,975, in stock | SXM2 Volta, 128/256 GB HBM2 total, NVLink mesh, 3U, 4x PSUs totalling 3,200 W; rails +CAD $145 — https://canservers.com/nvidia-dgx-1.html |
| NVIDIA DGX Station, 4x V100 32 GB, liquid-cooled | CAD $12,750, in stock | 1x E5-2698 v4, 256 GB DDR4, 128 GB VRAM total, seller flushed coolant and repasted — https://canservers.com/nvidia-dgx-station-4x-v100-32gb-128gb-vram-nvlink-liquid-cooled.html |
| Supermicro SYS-4029GP-TRT, 8x Quadro P5000, refurb | Was $7,371.90, now $5,486.75, out of stock | 2x Xeon Gold 6148 (40 cores), 96 GB DDR4, 8x P5000 16 GB, 4U — https://pcserverandparts.com/ai-inference-cluster-supermicro-superserver-sys-4029gp-trt-2x-intel-xeon-gold-6148-2-40ghz-40c-96gb-ddr4-2x-960gb-ssd-8x-quadro-p5000-refurbished/ |
| Dell PowerEdge R750xa, refurb (ETB) | $13,891.36 / $22,768.05 | 3rd-gen Xeon, 64/128 GB, 2x RTX 5000 / 2x RTX 4000 Ada, dual 2,400 W PSUs, rails included, 3-year ETB warranty — https://www.etb-tech.com/dell-poweredge-r750xa-1x8-2-5-2-x-silver-4309y-2-8ghz-eight-core-64gb-4-x-1-6tb-sas-2-5-2-x-rtx-5000-h745-idrac9-enterprise-svr-r750xa-002.html |

If the single goal is serving a 24–70B model, a used DGX-1 (8x V100) or a 4-GPU PCIe V100/A100 box is the only class in this scan that plausibly holds a large model in VRAM at homelab prices — and only the V100 version is cheap. The A100 version is not cheap in 2026: A100 40 GB refurb $4,000–$6,000, 80 GB refurb $7,000–$9,500, but live asking from $12,500 (average $22,997 across 18 listings) — https://compute.exchange/hardware-market/refurbished-gpus , https://gpupoet.com/gpu/shop/nvidia-a100-pcie . No complete used 4x A100 node at a single verified homelab price was found (NOT FOUND); budget roughly $28,000+ in GPUs alone before chassis, CPUs, RAM, and PSUs. H100 is not a value buy at any figure in this scan ($16,000–$30,000 depending on form factor and source, conflicting).

### Recent-gen CPU servers

| System | Price, seen 2026-10-26 | Notes |
|---|---|---|
| Dell PowerEdge R640, eBay barebones | $258.88 each, 20 available, 70 sold (updated Oct 15, 2026) | 1U, 2x Xeon Gold 6150; title says 64 GB but item specifics say 0 GB RAM — verify RAM before buying — https://www.ebay.com/itm/188184679747 |
| Dell R740 16SFF, refurb (Servermall) | Base €311 excl. VAT; configured from €460 excl. VAT | 2U, 2x 2nd-gen Xeon Scalable, 16 SFF bays; base is only Xeon Bronze 3204 + 8 GB — the configured price is the honest comparison — https://servermall.com/catalog/servers/dell-poweredge-r740-16sff/ |
| Dell R750 24SFF, refurb (Servermall) | Base €4,360 excl. VAT; configured from €5,723 excl. VAT | 2U, 2x 3rd-gen Xeon Scalable, DDR4 — 3rd-gen still carries a large premium over 2nd-gen |
| Dell R6515, single-socket EPYC | $1,780 | 1U, EPYC 7702P, 64 GB, iDRAC9, 550 W Platinum — supplier marketplace listing, verify seller |
| EPYC Rome/Milan CPUs alone | 7282 (Rome 16-core) $45–$155; 7313P (Milan 16-core) $340–$790; 7763 (Milan 64-core) $850–$1,028 | SP3 socket; Milan is worth paying for (higher IPC, PCIe Gen4); check locked-vs-unlocked before buying |
| EPYC board + CPU combos | H12SSL-i + 7443 24-core $1,500–$1,945; + 7B13 64-core $1,974.99; + 7542 32-core + 384 GB RAM $3,699 | ATX SP3 board in a standard tower case is the cheapest route to a quiet EPYC desk box, but it is a build, not turnkey |

General guide ranges (undated guides, seen 2026-10-26): 14th-gen Dell (R640/R740 class) $200–$600 typical eBay; 15th-gen (R650/R750 class) $400–$1,000+ — https://homelabstarter.com/used-dell-poweredge-buying-guide/

### Storage servers

NetApp DS4246 24-bay JBOD, no drives: $349 or Best Offer (older crawl; same item relisted at $695, updated Sep 30, 2026) — https://www.ebay.com/itm/NetApp-DS4246-Disk-Array-Shelf-W-24x-SAS-Trays-2x-IOM6-SAS-Expansion-Array/202404952486 . DS212C 12-bay: $499 or Best Offer. EMC 15-bay: $295–$399.99. The honest template is $450 all-in (shelf + HBA + cables) for ~12 TB usable RAID6, from a verified-purchase review — not the shelf price alone. Gotchas: NetApp 520-byte sectors must be reformatted to 512 bytes; 6G IOM6 shelves cap link speed (12G IOM12 variant $629); an external SAS HBA in IT mode, SAS cables, and rails are not in the shelf price. No single verified complete used storage-server price (e.g. R740xd class) was found (NOT FOUND).

### Where they are sold

Refurbishers and server specialists: Servermall, PC Server & Parts, ETB, CanServers/UsedServers, Dell Refurbished, Acme, Compute Exchange (links in the tables above). Marketplaces: eBay power sellers (see item links), Newegg refurbished, PicClick aggregator pages. Surplus auctions: GovDeals, Public Surplus, Municibid, Proxibid, Auctions International — with buyer premiums that change the price (GSA none, GovDeals ~12.5%, Public Surplus ~10% in examples). Some refurbishers named in directory results (ServerMonkey, SaveMyServer, Techbuyer) had no store URL returned — verify before using; no URL is guessed here.

### Hidden costs — read before budgeting

- Power: sources disagree, so budget the higher figure. One guide claims R640-class hosts idle at 45–55 W; other sources put realistic homelab idle at 75–150 W, loaded 300–400 W. The DGX-1 is 3,200 W max. Meter your own node; do not budget on a SPECpower floor (44–55 W idle uses one PSU, one SSD, no spinning disks).
- Noise: DGX-1 72–100 dBA per the manufacturer guide. Rack nodes generally 40–65 dBA at idle, permanently. A bedroom is not a viable location; a basement, garage, or closed room is not optional for most homes.
- 240 V: DGX-1-class and multi-kW PSUs need 200–240 V circuits. Check your panel before buying, not after.
- Rails, caddies, proprietary parts: rails are often excluded (DGX-1 rails +CAD $145 in one listing); drive caddies $20–$40 per server if missing; iDRAC Enterprise licences and PERC cards are separate line items on Dell gear; SXM modules are not PCIe cards.
- RAM pricing, the 2026 twist: DDR4 RDIMM around $299–$325 new retail for 32 GB vs used-kit figures near $250, after a ~90% Q1 server-DRAM rise; DDR5 carries a 4–6x DDR4 memory-bill multiplier. That is the reason DDR4 nodes win in 2026: buy the chassis with modest RAM and upgrade from used DDR4.

## 3. Workstations: Threadripper / Xeon-W / EPYC towers

Quiet, desk-friendly, and the lane/RAM story is the point: a tower gives you PCIe lanes and DIMM slots a mini PC cannot, without rack noise.

| System | Price, seen 2026-10-26 | Configuration |
|---|---|---|
| Lenovo ThinkStation P620, Threadripper PRO 5945WX, eBay used | $1,795, free shipping (updated Jan 30, 2026) | 128 GB RAM, 2 TB NVMe, W3100 GPU, tested with cosmetic wear — https://www.ebay.com/itm/336385027621 |
| Lenovo P620, Threadripper PRO, UK eBay range | £1,679 (3945WX, 128 GB) to £4,500 (5975WX 32-core, 128 GB) | Tower, up to 1 TB RAM capacity; UK prices include VAT differences, not directly comparable to US prices |
| HP Z8 G4, dual Xeon Gold 6154, eBay Refurbished US | $2,145.86 or Best Offer, 5 available, 7 sold | 36 cores total, 128 GB RAM, 1 TB SSD, Quadro P4000, 1-year Allstate warranty via eBay Refurbished |
| HP Z8 G4, bare configs | 24-core 128 GB no GPU/HDD $2,296.56; 48-core no RAM/GPU/HDD $1,312.16; 44-core no RAM/GPU/HDD $1,127.74 | Buying a bare Z8 G4 and adding used RAM + a consumer GPU is usually cheaper than buying fully loaded — https://picclick.ca/HP-Z8-G4-Workstation-Tower-2-XEON-Gold-278232801052.html |
| Dell Precision 5820 tower, refurb (Newegg) | $1,249–$2,092 depending on GPU/SSD | i7-7820X 8-core, 128 GB DDR4, 500 GB–4 TB NVMe; listings crawled ~285 days before the read date, verify stock |
| Dell Precision T5820 chassis, build-your-own | From $144.98 | Tower, 1x LGA2066, 128 GB DDR4 ceiling stated; chassis only, CPU/RAM/GPU extra |
| Single-socket EPYC quiet tower, Acme AP-T08SG | Price NOT FOUND in listing text | Single EPYC 7002/7003, SP3, 8x DDR4 DIMMs up to 2 TB, 5x PCIe 4.0 x16 + 2x x8, 8 hot-swap bays, 900 W Platinum, marketed as quiet; CPU, memory, drives, GPU NOT included — https://www.acmemicro.com/Product/18636/Acme-AP-T08SG-quiet-workstation-DDR4-AMD-UP-SP3-7003-PCIe-GPU-ready-tower-10-drives-sell-complete-system-only?c_id=16 |
| EPYC self-build combos | H12SSL-i + 7542 32-core + 384 GB RAM $3,699; + 7532 32-core + 4x 32 GB RAM $2,499; + 7452 32-core $568–$713 | ATX SP3 board in a standard tower case: cheapest quiet EPYC desk box, but a build, not turnkey |

No single verified 512 GB tower price was found (NOT FOUND). 512 GB is arithmetic, not a listing: a 128 GB tower above plus used DDR4 at used prices. Do not quote a 512 GB tower price without a real listing. The 64-core Threadripper PRO parts still carry a large premium over 12/16-core PRO parts (£4,336–£5,393 for 3995WX towers in the UK range) — core count is where the money goes, and for agents and serving it is mostly wasted.

Good-for: a P620 or Z8 G4 with 128 GB is the desk-friendly host for a 3090 or P40, for many-agent work (RAM for context and caches), and for a second GPU later (lanes). Gotcha: fully loaded workstations price the RAM and GPU at retail; buy bare and add used DDR4 + a consumer GPU yourself.

## 4. Consumer and prosumer PCs: best value for local AI

### Used 3090 / 4090, bare cards

- RTX 3090: conflicting October snapshots, disclosed not averaged — $1,522 US eBay sold median (329 sales, updated 2026-10-24) — https://gpusold.com/gpu/rtx-3090-24 — vs $1,400–$1,550 (2026-10-15 guide) vs $1,199 monthly median (tracker) — https://bestvaluegpu.com/history/new-and-used-rtx-3090-price-history-and-specs/ — with a $699–$999 figure flagged as a stale outlier. $63.42/GB at $1,522. 936 GB/s, 350 W TGP. Cheapest 24 GB CUDA inference + small LoRA. Gotcha: no 70B Q4 on one card; ex-mining pool; October prices moving fast.
- RTX 4090: $2,271 sold value through 2026-10-24 — https://www.getpcparts.com/market-prices/gpu-graphics-cards/rtx-4090 — vs $3,000 asking median rebuilt 2026-10-26 — https://dealhunter.io/prices/rtx-4090 . Sold vs asking is the whole story. $94.63/GB at $2,271, $125.00/GB at $3,000. 1,008 GB/s, 450 W TGP. Faster prompt processing than the 3090 (6,697 vs 3,536 tok/s prompt processing in one comparison; 127.7 vs 111.7 tok/s on 8B) — https://www.compute-market.com/blog/rtx-3090-vs-rtx-4090-for-ai-2026 . Gotcha: same 24 GB ceiling as the 3090; no NVLink on 40-series; discontinued, so asking prices run ahead of sold values.
- 2x RTX 3090 in one host: ~$3,044 for two cards at the sold median, plus host/board/PSU — the cheapest real 70B Q4 path (48 GB total, not pooled). Needs an x8/x8-or-better board, 1,200 W+ PSU, cooling gap between cards, PCIe-only split.
- Complete used 3090 PCs: all found listings sold out, $1,299.99–$1,999.99. Complete 4090 PC price: NOT FOUND.

### Multi-GPU consumer boards

Consumer X870E/Z890 boards at x8/x8: $250–$450. TRX50 at x16/x16: $700–$1,100. WRX90 with 7x PCIe 5.0 x16: $1,100–$1,600 guide band. PSU: 750–1,000 W for one 3090, 850–1,200 W for one 4090, 1,200 W+ for dual-GPU — https://www.compute-market.com/blog/best-motherboard-dual-gpu-local-llm-2026 , https://umatechnology.org/graphics-card-recommended-power-supply/ . No NVLink on 40/50-series: multi-GPU means PCIe tensor-split, not pooled memory.

### Mac Studio / Mac mini (unified memory)

- Mac Studio M4 Max 128 GB: $3,999–$4,499 (Sep 2026), 546 GB/s, 30–120 W under load, 24–31 dB in one review, 70B at ~22–25 tok/s in one roundup. $31.24–$35.15/GB. Silent 70B serving, always-on. Gotcha: no CUDA; soldered memory; outgoing model for M5 Max ($2,499 base, 128 GB reported $4,799–$5,400).
- Mac mini M4 Pro 64 GB: $2,199, 273 GB/s, $34.36/GB. 30B+, 70B at Q3. Gotcha: 64 GB ceiling; no CUDA.

### AMD Strix Halo-class mini PCs (large shared memory)

128 GB configurations, Sep 2026: $3,449 Framework / $3,649 GMKtec EVO-X2 / $3,799 Minisforum / $3,999 AMD box. 256 GB/s, $26.95–$31.24/GB — the cheapest per-GB 128 GB route, but the slowest bandwidth in this comparison. 70B tok/s figures conflict (about 5 vs 18–22) and both are reported, not resolved. Gotcha: ROCm, not CUDA; soldered memory. Sources: https://modelfit.io/blog/amd-strix-halo-local-ai-128gb/ , https://presenc.ai/research/amd-strix-halo-local-llm-benchmarks-2026

### Small NVIDIA dev boxes

- Jetson Orin Nano Super: $249, 8 GB shared, 102 GB/s, 7–25 W. Up to ~8B models. Edge, robotics, vision, learning CUDA. Gotcha: 8 GB ceiling; Arm64; not a homelab server.
- DGX Spark 128 GB: $6,950 list (from 2026-10-02), up from $3,999 launch / $4,699 Feb 2026 — a 74% jump. 273 GB/s, $54.30/GB, 140 W TDP / 240 W PSU. CUDA-first 128 GB dev, clustering. Gotcha: price jumped; soldered; slow bandwidth for its price. DGX Spark 64 GB from $4,999 (on sale 2026-10-23), $78.11/GB — half the memory for more than the old 128 GB price. Source: https://tech-insider.org/dgx-spark-64gb-on-sale-4999-vs-128gb-6950-2026/

### Price per GB and tokens/sec per dollar

Price per GB (calculated from the prices above): P40 $9–$14, V100 16 GB $10–$19, 3060 12 GB $22–$29, Strix Halo 128 GB $26.95–$31.24, Mac Studio 128 GB $31.24–$35.15, Jetson Orin Nano Super $31.13, 3090 $63.42, 4090 $94.63 sold / $125.00 asking, DGX Spark 128 GB $54.30. Tokens/sec per dollar: NOT FOUND as a single sourced figure for every option. Sources give tok/s for isolated setups (3090/4090 8B, Strix Halo 7B/120B/70B with conflicting 70B figures, Mac Studio 70B at 22–25 tok/s, Jetson 4B at 8–10 tok/s) but no source pairs those speeds with one agreed October price for the same configuration, and mixing them would invent the metric. Do not quote a tok/s-per-dollar figure that no source states.

## 5. The cluster question: several cheap old boxes vs one modern machine

Short answer, with the arithmetic below: almost never for a single model or a single job, sometimes for many independent jobs, and only if you already have the space, the circuit, and the noise tolerance. The purchase price is the cheap part; the watt is the subscription.

Formula: monthly cost = watts x 24 hours x 30 days / 1,000 x $0.13/kWh = watts x 0.0936 dollars per month. Check: 100 W = $9.36/month, $112.32/year; 150 W = $14.04/month, $168.48/year. Mixed-load case: 8 hours loaded, 16 hours idle per day.

| Option | Purchase (working figure) | Mixed-load power cost | 3-year total (purchase + mixed power) | Noise |
|---|---|---|---|---|
| Three old rack servers, realistic (150 W idle each) | ~$600 (estimate, before disks/caddies) | $56.16/month, $673.92/year | $2,621.76 | 40–65 dBA, permanent |
| Three old rack servers, SPEC floor (44.6 W idle each) | ~$600 (estimate) | $33.81/month, $405.70/year | $1,817.10 | 40–65 dBA, permanent |
| One modern 3090 tower (80 W idle / 550 W loaded, estimates) | ~$1,600 (estimate, bracketed by sold complete builds $1,299.99–$1,999.99) | $22.15/month, $265.84/year | $2,397.52 | Tower fans; quiet at idle |
| One Mac Studio M4 Max 128 GB (30–120 W, sourced) | $3,999 | $5.62/month, $67.39/year | $4,201.17 | 24–31 dB |
| Three modern mini PCs (15–30 W idle each, sourced) | NOT FOUND as a bundle price | $8.42/month idle-only at 30 W each | Not computed (no bundle price) | Near-silent |

Watt sources: https://sillectus.com/articles/best-used-server-for-home-lab/ , https://selfhosting.sh/hardware/used-enterprise-servers/ , https://homelabstarter.com/used-dell-poweredge-buying-guide/ , https://budgethomelab.com/articles/homelab-hardware-under-500-2026/ , https://lazyadmin.nl/home-network/7-homelab-decisions-that-actually-pay-off/ , https://ebungo.orem.in/field-digest-homelab-2026-09-17.html

The gap between SPECpower floors (44–55 W idle) and homelab reality (150–300 W idle) is the most important number in this section. SPECpower uses one PSU, one SSD, no spinning disks, no second PSU. A homelab server with 8 disks, a RAID card, and redundant PSUs does not idle at 44 W. The verdict does not depend on picking the flattering number: even on the SPEC floor, the three-year rack total ($1,817.10) is within sight of the 3090 tower ($2,397.52) before disks, caddies, rails, switch, UPS, and cooling — and the rack still cannot run the AI workloads a GPU tower can.

Why a cluster of old boxes loses for a single model: token generation is sequential and bandwidth-bound. Every token waits for a round-trip. A single node with NVLink does ~900 GB/s at 1–5 microseconds per hop; a multi-node cluster over InfiniBand/RoCE does 400 Gb/s (50 GB/s) at 5–50 microseconds per hop; a home cluster over 1 GbE is roughly 125 MB/s — about 7,000x slower than a 3090's own memory bandwidth. Sharding one model's layers across old boxes over home networking does not make it faster; it makes each token wait for the slowest network hop. Sources: https://lucaberton.com/blog/distributed-vs-multi-gpu-inference-2026/ , https://www.runpod.io/articles/guides/gpu-clusters-for-ai-training , https://thinksmart.life/research/posts/multi-gpu-setup-guide/ , https://gitpicks.dev/featured/exo-distributed-ai-inference-local-devices , https://www.clawdbytes.com/article/2026-10-22-show-hn-lumabri-run-large-ai-models-across-your-computers-and-serverspure-c

Partial exception: a mining-style host controlling MULTIPLE GPUs in ONE machine (one host, many cards on risers) is a single-node multi-GPU build, not a cluster, and it avoids the network bottleneck — https://www.gpux.us/ . The cheapest "cluster" that actually works for LLMs is not old servers at all: four RX 580 8 GB cards at $40–$60 each on eBay, in ONE mining-motherboard host with an 850–1,000 W PSU, running llama.cpp with tensor-split across the four cards — 32 GB total for roughly $160–$240 of GPUs — but it is ROCm/Vulkan on Polaris, with driver workarounds, a hobby build, not production serving — https://www.sitepoint.com/poverty-spec-ai-cluster-rx-580-local-llm/

Verdicts by workload:

- Agents (small-model inference plus API/tool latency): ONE MODERN MACHINE WINS. Agents are latency-sensitive and mostly wait on tools and model tokens, not on CPU core count. A cluster helps only for MANY independent agents in parallel, one per node — and even then three mini PCs beat three rack servers on power and noise.
- Small fine-tunes (LoRA/QLoRA on 7B–13B, occasionally 30B): ONE MODERN GPU WINS, by a wide margin. The job is GPU-memory-bandwidth-bound and needs CUDA (or ROCm on AMD) and fast VRAM, which old CPU servers do not have at all. A cluster of old CPU servers cannot fine-tune a 7B model in any reasonable time. The cluster case that DOES work is many INDEPENDENT LoRA jobs in parallel — a fine-tune farm, not a small fine-tune — and it still needs a GPU per node to be useful.
- Local model serving (one model, one or a few users): ONE MODERN MACHINE WINS for latency and for any model that fits on one machine. A single 3090 serves 7B–30B at full speed; a single 128 GB unified-memory machine serves 70B. A cluster wins only for (a) serving MANY DIFFERENT small models at once, one per node, or (b) redundancy/failover — and neither case needs old rack servers; mini PCs do both quieter and cheaper.

Overall cluster verdict: buy one modern machine for AI work and, if you must cluster, cluster quiet mini PCs for independent jobs — a rack of cheap old servers costs more over three years than a single 3090 tower, is far louder, and is slower for every single-model AI workload in this task.

## Best buys: three budget shortlists

### ~$500: the cheapest useful AI node

1. RTX 3060 12 GB ($320–$350 budget) — the plug-and-play pick: a real card, CUDA, 12 GB, quiet in a tower, runs small models and agents now. Leaves ~$150 for nothing else needed if the host already exists.
2. Cooled Tesla P40 ($250–$325) — the 24 GB pick on this budget, IF you accept the fan mod, no display output, and int-quantised inference. Pair with an existing host; do not buy a host for it at this budget.
3. Jetson Orin Nano Super ($249) — the learning/edge pick: 8 GB, 7–25 W, silent, CUDA-native. Not a homelab server, but the cheapest way to learn the NVIDIA stack and run vision/edge agents.

If the host does not already exist, the $500 budget does not buy a GPU node — it buys the host (used mini PC / tower) and the GPU comes later. Do not buy a rack server at this budget: its power bill eats the saving inside a year.

### ~$1,500: the real upgrade

1. A used RTX 3090 ($1,350–$1,550) into the existing desktop — the single biggest AI upgrade at this budget, if the desktop's PSU (750–1,000 W) and cooling can take it. 24 GB CUDA, 936 GB/s, 7B–30B serving and small LoRA.
2. A 2nd-gen Xeon node + a Tesla: Dell R640 barebones ($258.88, verify RAM) + used DDR4 + a Tesla V100 32 GB PCIe ($645–$660 sold examples) or a cooled P40 ($250–$325) — roughly $1,100–$1,500 all-in depending on RAM and drives. The node that replaces the E5 v2 fleet AND adds GPU memory, at the cost of rack noise.
3. HP Z8 G4 128 GB ($2,145.86) is over this budget alone; at ~$1,500 the honest version is a bare Z8 G4 ($1,127.74–$1,312.16) + used DDR4, with the GPU carried over or added next. Do not stretch to a 4090 at this budget: the card alone ($2,271 sold) breaks it.

### ~$4,000: the quiet large-model machine

1. AMD Strix Halo mini PC, 128 GB ($3,449–$3,999) — the headline pick: cheapest x86 128 GB route, near-silent, 70B Q4 on one quiet box. Accept 256 GB/s bandwidth and ROCm instead of CUDA, and the conflicting 70B speed figures (about 5 vs 18–22 tok/s, both reported).
2. Mac Studio M4 Max 128 GB ($3,999–$4,499, slightly over budget at the top) — the silent pick if the workflow tolerates no CUDA: 546 GB/s, 30–120 W, 24–31 dB, 70B at ~22–25 tok/s in one roundup. Outgoing model; M5 Max 128 GB is reported at $4,799–$5,400.
3. Threadripper P620 128 GB ($1,795) + used RTX 3090 ($1,350–$1,550) ≈ $3,150–$3,350 — the CUDA pick at this budget: lanes, RAM, and a real 24 GB card in a quiet tower, with budget left for RAM upgrades or a second card later. Not a 70B machine on its own, but the most flexible box in this shortlist.

What NOT to buy at any of these budgets: an A100 card alone ($4,000–$6,000 refurb for 40 GB) at the $4,000 budget — it leaves nothing for the host and still needs server airflow; a DGX-1 ($6,499) at any budget here — it breaks the budget before freight and needs 240 V and a room you can stand to be near; and a rack of old servers at the $500 budget — the power bill, not the purchase price, is the cost.

## Local pickup sources near north-central West Virginia (within ~150 miles)

Institutional sources only — no Marketplace listings are repeated here.

- WVU Surplus, Morgantown (via GovDeals): WVU sells surplus property through GovDeals — https://financialservices.wvu.edu/property-management/surplus/suplus-property-sales and https://facilitiesmanagement.wvu.edu/administrative-support-services/property-surplus/property-sales . No live WV computer/server lot was verified on 2026-10-26; GovDeals is the channel to watch, not a browsable shelf.
- WV State Agency for Surplus Property, Dunbar warehouse, 2700 Charles Avenue: sells at the warehouse (Mon–Fri 9 AM–4 PM per some pages) and via GovDeals, but inventory is not viewable online — http://www.state.wv.us/admin/purchase/surplus/surplusFAQs.html . Hours disagree across official pages — call (304) 766-2626 first. No cash/personal checks. A Dunbar walk-in is the only way to see current stock.
- Pitt Surplus, Pittsburgh (7500 Thomas Blvd): public surplus store, appointment/Wednesday drop-ins — https://newapps.fis.pitt.edu/surplusproperty/Site/About . Inside the radius from Morgantown; check hours before driving.
- Really Cheap Geeks, Parkersburg: refurbished computers, 1-year warranty per a secondary profile — https://aventure.vc/companies/really-cheap-geeks-parkersburg-wv-us . Inventory NOT FOUND in this scan; call before driving.
- NOT FOUND as standalone local sources: a dedicated Fairmont State surplus store (policy points to WVU/Marshall/state channels — https://www.fairmontstate.edu/_files/bog/policies/fsu_policy_33.pdf ), a dedicated Bridgeport/Clarksburg refurbisher, a Micro Center within radius, a live GovDeals GPU/server lot near Bridgeport on 2026-10-26.
- Outside the ~150-mile radius, listed separately so they are not misread as local: Penn State Lion Surplus, University Park, PA — https://surplus.psu.edu/ ; Marshall University, Huntington (surplus via state channels).

## Red flags when buying used

1. No returns, no tests: a seller who will not accept returns on a GPU or server is pricing in failure. Walk away unless the price already assumes a dead unit.
2. VRAM errors: any error in a VRAM stress test (OCCT or equivalent) is a fail. VRAM errors do not heal and will corrupt inference and training.
3. BIOS mismatch: GPU-Z showing the wrong model, wrong VRAM size, or a mining BIOS means the card was flashed. Do not pay a stock price for a flashed card.
4. 3090 GDDR6X heat: sustained memory-junction temperature above ~100 °C means a repad is coming; throttling around 110 °C. Budget pads + paste, and check pad thickness — wrong thickness makes temperatures worse.
5. Passive cards in still air: Tesla P40/V100/P100 cards are passive. In a desktop with no server airflow they throttle. Budget a fan mod or a server chassis, or do not buy.
6. SXM2 vs PCIe: SXM2 modules are cheaper for a reason — they need an adapter or baseboard. Do not compare an SXM2 module price with a PCIe card price.
7. "Barebones" that is not: R640-class listings whose titles state RAM the item specifics deny (0 GB). Verify RAM, drives, caddies, rails, and PSUs line by line before paying.
8. Base vs configured prices: refurbisher configurators advertise a Bronze CPU + 8 GB base. The configured price (R740 from €460 excl. VAT, not €311) is the honest comparison.
9. Locked EPYC CPUs: some EPYC parts are vendor-locked to one board vendor. Check locked-vs-unlocked before buying any Rome/Milan CPU or combo.
10. 520-byte sectors: NetApp/EMC shelves ship drives formatted 520 bytes per sector. They must be reformatted to 512 bytes before a normal HBA will use them.
11. DDR5 sticker shock: DDR5 carries a 4–6x DDR4 memory-bill multiplier in 2026. A cheap DDR5 chassis with a 512 GB RAM plan is not a cheap system.
12. 240 V and noise, checked last: multi-kW GPU servers need 200–240 V circuits and run at 72–100 dBA (DGX-1). Check your panel and your household's noise tolerance before buying, not after.
13. Asking vs sold: A100 80 GB "from $7,000" (refurb guides) vs live asking from $12,500 (average $22,997 across 18 listings) are different markets. Budget on sold examples, not the cheapest headline.
14. Stale listings: any listing whose last update is months old (e.g. the 3090 card last revised June 2026, or workstation listings crawled ~285 days before the read date) may already be sold. Re-check each link before paying.
15. Tracker disagreement: GPU price trackers disagree by hundreds of dollars on the same card in the same month (3090: $1,199 median vs $1,350–$1,550 budget range). Use the budget range, not the lowest tracker number.

## How I checked it

- Read date for all facts: 2026-10-26. Public web only; no login, no account, no purchase, no messages or comments to anyone.
- Three parallel research passes (ex-mining GPUs; enterprise servers + workstations; consumer/prosumer PCs + cluster question + local sources), each checking project repos, refurbisher pages, eBay listings, price trackers, and guides first, then practitioner reports. Each pass reported only URLs returned by search or page fetch, never guessed URLs.
- Every price in this report carries the 2026-10-26 read date plus listing dates where shown. Where sources disagreed (3090, 3060 12 GB, A6000, V100 form factors, A100 refurb vs asking, Strix Halo 70B speed, server idle watts), the disagreement is stated in the report rather than averaged away.
- This report synthesises the three staging passes (~/goblin/results-batch18-pub/hw-scan-part1.md, hw-scan-part2.md, hw-scan-part3.md); no listing from the earlier fleet-marketplace-20261026 task is repeated here.
- Nothing was pushed to any repo and nothing was written to any repo. This file is staging only.

## Unsure about

- Tokens/sec per dollar for every option: NOT FOUND as a single sourced figure — speeds and prices come from different sources and dates and were not mixed to invent the metric.
- Per-card idle power except the RTX 3060: NOT FOUND; whole-system 3090-tower watts are estimates, labelled as such.
- Measured dB for rack nodes, workstations, and shelves (only the DGX-1 has a manufacturer range) and for A4000/A5000 blowers alone: NOT FOUND.
- Single verified prices for: a complete 4x A100 node, a dual-socket Milan node, a complete storage server, a complete EPYC tower, a 512 GB tower, a complete 4090 PC: NOT FOUND.
- Live GovDeals GPU/server lots near Bridgeport, a dedicated Fairmont State surplus store, a dedicated Bridgeport/Clarksburg refurbisher, a Micro Center within radius: NOT FOUND on 2026-10-26.
- Strix Halo 70B speed (about 5 vs 18–22 tok/s), A6000 bargain-tier prices ($2,200–$2,800), and the causal claim for the 3090 price rise (AI buyers + RTX 30/40 AI unlock): reported, not independently verified.
- Availability of every eBay listing cited: search-index records and listing pages can lag the live site, so any listing may already be sold — re-check each link before paying.
