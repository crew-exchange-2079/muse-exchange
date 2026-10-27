# hw-market-scan-20261026

Goal: a market-wide scan of used and refurbished compute (ex-mining GPUs, decommissioned enterprise and AI servers, workstations, consumer and prosumer AI boxes) with value-per-dollar and per-watt verdicts and three budget shortlists. Research only; this complements the local-listing task fleet-marketplace-20261026, so do not repeat its local listings.

A small homelab runs AI agents and local models. Today it has one RTX 3090 (24 GB) in a desktop and a few 2013-era dual-Xeon E5 v2 servers (DDR3, InfiniBand FDR). The owner will want a modern, quieter, more efficient machine (or a few) in the next 6-18 months. Find where the real value is in the used and refurbished market right now. Research only: no accounts, no purchases, no contacting sellers.

## Cover all of these
1. **Ex-mining GPU rigs and GPU lots:** what's being dumped (RTX 3090/3080/3060, A-series, older Teslas such as P40/V100), typical prices, and how to judge wear (fan bearings, repasting, VRAM temps, BIOS-flashed cards).
2. **Decommissioned enterprise and AI servers:** GPU servers (e.g. 4-8 GPU chassis, SXM2 V100 boxes, A100 or older DGX-class gear as it ages out), recent-gen CPU servers (Xeon Scalable 2nd/3rd gen, EPYC Rome/Milan), and storage servers. Where they're sold (refurbishers, server liquidators, eBay power sellers, government/university surplus auctions), real prices, and the hidden costs: power, noise, 240 V, rails, proprietary parts.
3. **Workstations:** used Threadripper / Xeon-W / EPYC towers (quiet, desk-friendly), and what they cost with 128-512 GB RAM.
4. **Consumer and prosumer PCs:** current best value for local AI: used 3090/4090 builds, multi-GPU consumer boards, Mac Studio / Mac mini (unified memory for large models), AMD Strix Halo-class mini PCs with large shared memory, small NVIDIA dev boxes. Price per GB of fast memory and tokens/sec per dollar.
5. **The cluster question:** is it ever worth buying several cheap old boxes (like an ex-mining farm or a rack of old servers) vs one modern machine, for running AI agents, small fine-tunes and local model serving? Include electricity at about $0.13/kWh and noise.

## For each recommendation give
- What it is, a typical price range today (with 2-3 real listing or source links), power draw idle and loaded, and noise level.
- What it's good for (serving 24-70B models, fine-tuning, many small agents, storage) and the main gotcha.
- A "best buys" shortlist at three budgets: ~$500, ~$1,500, ~$4,000.
- Local pickup sources near north-central West Virginia (within ~150 miles) where they exist: surplus auctions, universities, refurbishers.

## Output
A markdown report: a summary table first, then sections 1-5, then the three shortlists, then a "red flags when buying used" checklist. Cite sources with links. Dates matter: say when each price was seen.
