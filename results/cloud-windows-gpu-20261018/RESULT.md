# cloud-windows-gpu-20261018

Task: the cheapest good way to rent a Windows machine with a strong GPU by the hour to run the Unreal Engine 5 editor, streamed to a home PC — current public pricing for Shadow PC, Paperspace, AWS EC2 G5/G6 Windows, Azure NV-series, Google Cloud GPU + Windows, Vast.ai, TensorDock, Lambda, and any others.

Read date for all pages: 2026-10-18. Public pages only; no login, no account, no purchase. Prices USD.

## Bottom line

The big GPU marketplaces are a dead end for Windows: **Vast.ai and Lambda are Linux-only in practice**, and **Paperspace retired Windows templates for new users in July 2024**. The real hourly-Windows options are **TensorDock** (marketplace Windows VMs with an RTX 4090 from $0.35/hr for the GPU — cheapest by a wide margin), the hyperscalers' Windows GPU instances (**GCP G2/L4 ≈ $0.89/hr, AWS G6 ≈ $0.99/hr, AWS G5 ≈ $1.19/hr** all-in with the Windows licence), and managed cloud PCs (**AirGPU from $0.65/hr; SensePC hourly; Shadow PC is monthly-only**). Azure's current NVads A10 v5 line works but is expensive ($2.43/hr for half an A10) and its older NVv3 series was **retired on 2026-09-30**. For a single ~4-hour Unreal editor session, expect roughly **$1.80 (TensorDock) to $4–5 (hyperscaler/AirGPU)**, plus a few dollars a month if you keep a project disk around.

## The table

| Provider | GPU + VRAM | CPU / RAM | Windows included? | Price/hr | Storage | Min. billing | Streaming | Setup |
|---|---|---|---|---|---|---|---|---|
| **TensorDock** (marketplace Windows VMs) | RTX 4090 24 GB (also 3090 24 GB $0.20, A6000 48 GB $0.45, RTX 6000 Ada $0.75) | à la carte (vCPU $0.003/hr, RAM $0.002/GB/hr) | Yes — Windows VMs (its customer AirGPU "relies on TensorDock's API to deploy Windows virtual machines") | **4090 from $0.35** GPU-only; a UE5 config (8 vCPU / 32 GB / 200 GB) adds ≈$0.10 → **≈$0.45/hr** | NVMe $0.00005/GB/hr (≈$0.01/hr for 200 GB) | Per-second from a prepaid balance; **VM auto-deleted at $0 balance** | Self-installed Parsec or Sunshine/Moonlight (TensorDock publishes a Parsec guide incl. virtual display driver) | Medium — pick host, deploy, install UE5 |
| **Google Cloud G2** | NVIDIA L4 24 GB | g2-standard-4: 4 vCPU / 16 GiB (also -8, -16) | Windows Server image, **+$0.046/vCPU/hr** | $0.7068 + $0.184 = **≈$0.89** (g2-standard-8 ≈$1.22) | Balanced PD $0.10/GB/mo (200 GB ≈ $20/mo; metered hourly, stops when deleted) | 1-min minimum, then per-second | Self-installed Parsec/Sunshine/RDP | High — GPU quota starts at 0 and must be requested; driver/vWS path for L4 on Windows not fully documented (see Unsure) |
| **AWS EC2 G6** | NVIDIA L4 24 GB | g6.xlarge: 4 vCPU / 16 GiB (2xlarge: 8/32) | Yes — licence-included Windows Server AMI | Linux $0.8048 + 4×$0.046 = **≈$0.99** (2xlarge ≈$1.35) | EBS gp3 $0.08/GB/mo (250 GB ≈ $20/mo) | Per-second, 60-s minimum | **Amazon DCV free on EC2**; or Parsec/Sunshine | Highest — VPC, AMI + drivers, DCV, stop/start discipline |
| **AWS EC2 G5** | NVIDIA A10G 24 GB | g5.xlarge: 4 vCPU / 16 GiB (2xlarge: 8/32) | Yes — same Windows component | Linux $1.006 + $0.184 = **≈$1.19** (2xlarge ≈$1.57) | Same EBS pricing | Per-second, 60-s minimum | DCV free; Parsec/Sunshine | Highest. Note: AWS offers RTX Enterprise **and gaming drivers** at no extra cost — a known-good UE5 path |
| **AirGPU** (managed cloud PC, runs on AWS/TensorDock) | L40S 48 GB ≈ RTX 4080 — $1.20/hr tier (also L4 24 GB $0.90, A10G 24 GB $1.05, A5000 24 GB $1.55, T4 16 GB $0.65) | from 8 vCPU / 32 GB on the gaming tiers | Full Windows desktop; licence inclusion **not stated** on AirGPU's pages (see Unsure) | **$0.65–$1.55** flat by tier | **$3.50/mo per 50 GB, 100 GB minimum (≥$7/mo)**, bills while off | None — prepaid credit, no subscription | Parsec or Moonlight (their guide) | Lowest of the hourly options — pick a machine, connect |
| **SensePC** (managed cloud PC) | NVIDIA L4 24 GB (≈RTX 4060-class) on all gaming tiers | Scales by tier (Core/Pro/Ultra) | Yes — full Windows 11 PC, persistent SSD, TPM 2.0 | Hourly plan exists; page shows a **$2.22 starting price** (exact tier rate shown only in its builder) | SSD keeps billing while stopped | Hourly/Daily/Monthly plans; compute bills only while running | Browser viewer or Amazon DCV client | Low |
| **Azure NVads A10 v5** | NVIDIA A10 — NV18ads = ½ A10, 12 GiB frame buffer; NV36ads = full A10 24 GiB | NV18ads: 18 vCPU / 220 GiB; NV36ads: 36 vCPU / 440 GiB | Yes — Windows price includes licence; NVIDIA GRID licence included | **NV18ads $2.428/hr; NV36ads $4.856/hr** (East US, from Azure's Retail Prices API) | Temp disk incl.; Managed Premium SSD 128 GiB $17.92/mo, 256 GiB $34.56/mo | Per-minute; must **deallocate** to stop billing | RDP built in; self-installed Parsec/Sunshine | High — GPU quota request normally required |
| **Shadow PC** | Power: RTX A4500 20 GB; Neo: RTX 2000 Ada 16 GB | 8 vCores EPYC / 28 GB (Power), 16 GB (Neo) | Yes — Windows 11 included, persistent PC | **Monthly only — no hourly plan.** Reported US prices (third-party, JS-hidden on Shadow's site): Neo Lite $29.99, Neo $37.99, Power $54.99/mo; hour caps 120–210 h/mo | 512 GB included (256 Lite); expandable, price not published | One month | Shadow's own client | Lowest overall — but a subscription |
| **Paperspace (DigitalOcean)** | RTX A4000 16 GB $0.76/hr; **A5000 24 GB $1.38/hr**; A6000 48 GB $1.89/hr (8 vCPU / 45 GB on A4000/A5000) | — | **NO for new users** — "As of 1 July 2024, Windows-based templates are retired and unavailable to new Paperspace users" (DigitalOcean docs) | Linux prices as listed | Block storage hourly, capped: 100 GB max $7/mo, 250 GB max $10/mo | Per-hour, billed only while powered on | Built-in browser streaming | Low — but Linux-only in practice now |

## Checked and ruled out

- **Vast.ai — no Windows path.** Hosts must run native Ubuntu; renters get Docker images or Ubuntu VMs (the only official VM template is Ubuntu 22.04), and Vast's own desktop offering is a *Linux* Virtual Desktop (Wine/Proton + Sunshine). No Windows template, image, or support statement exists in its docs. (Marketplace RTX 4090s run ≈$0.08–$0.59/hr per third-party trackers — moot, they'd be running Linux.)
- **Lambda — Linux only.** Its pricing page lists only datacenter GPUs (V100 $0.79/hr up to B200 $6.69/GPU/hr) and its docs describe Ubuntu-based images; no Windows option, and no consumer GPUs at all.
- **Azure NVv3 (Tesla M60)** — prices still listed (NV12s_v3 ≈$1.14/hr Linux) but the series was **retired 2026-09-30**; remaining VMs were deallocated. Do not plan around it.
- **Maximum Settings** — monthly plans with daily hour allowances, **Linux Mint by default**; Windows only as a bring-your-own ISO/licence VM on its Bare Metal tier; AMD GPUs. Not an hourly Windows service.
- **Cloudalize** — real GPU Windows DaaS for CAD/3D, but **no public pricing** (quote-only B2B sales). Specs/$/hr not found on public pages.
- **Oracle Cloud (OCI)** — Windows Server is supported on GPU shapes (VM.GPU.A10 series) with the licence billed on top, but it's enterprise-shaped (mostly 8-GPU bare metal; stopped GPU shapes keep billing until terminated). Poor fit for one desktop session.
- **OVHcloud** — GPU instances are hourly (L4 24 GB $1.00/hr, A10 24 GB $1.00, L40S 48 GB $1.80) but a Windows image for the GPU line was **not found** on its public pages; the line is positioned as Linux AI instances.
- **Hetzner** — no GPU cloud instances at all; GPUs are monthly dedicated servers only (no hourly product, no official Windows cloud image).
- **Simnet** — not found as a current provider. **Sixa** — no live offering found (coverage is from its ~2016 launch); presumed defunct.

## Top 3 for a ~4-hour Unreal Engine 5 editor session

**1. TensorDock — RTX 4090 Windows VM. ≈ $1.80 for 4 hours.**
$0.35/hr GPU + ≈$0.10/hr for an 8 vCPU / 32 GB / 200 GB configuration ≈ $0.45/hr, billed per-second from a prepaid balance. The 4090's 24 GB is the strongest editor GPU on this list at the lowest price. Streaming: follow TensorDock's own Parsec guide (install Parsec + the Virtual Display Driver, or Sunshine/Moonlight). Caveats: marketplace hosts vary — pick a well-rated US host near you; the price table on TensorDock's site is footnoted "Last Updated: July 24, 2024" (the $0.35 figure is also its current homepage "from" price; live dashboard prices vary by host); and **the VM is auto-deleted if your balance hits $0**, so keep a buffer and download/export your project.

**2. Google Cloud G2 (L4) with Windows Server. ≈ $3.60 for 4 hours.**
g2-standard-4 at ≈$0.89/hr all-in (GPU/VM $0.7068 + Windows $0.184), 1-minute minimum then per-second; a 200 GB Balanced boot disk adds ≈$0.11 for the session (≈$20/mo only if you keep it). Hyperscaler reliability and a fixed price list. Caveats: new accounts start with **zero GPU quota** (request it before you need the session — approval isn't instant); the OS is Windows Server, not Windows 11; and Google's pricing page documents the NVIDIA vWS (GRID) graphics licence for T4 but **no equivalent L4 line was found**, so confirm the Windows graphics-driver path on G2 before budgeting a big project on it. The fully documented fallback on GCP is T4 + vWS ($0.35 + $0.55/GPU/hr plus the VM) — weaker (16 GB) but licence-clear.

**3. AWS EC2 G6 (L4) Windows. ≈ $4.00 for 4 hours.**
g6.xlarge at ≈$0.99/hr licence-included, per-second with a 60-second minimum; a 250 GB gp3 disk adds ≈$0.11 for the session (≈$20/mo if kept). **Amazon DCV is free on EC2** and streams up to 4×4K, so no Parsec licence questions at all. Prefer the **G5** (A10G, ≈$1.19/hr → ≈$4.76/4h) if you want AWS's gaming-driver path, which is the known-good UE5 editor combination. Caveats: the most setup work of the three (AMI, drivers, security groups, stop-the-instance discipline — a forgotten running instance is the classic AWS bill), and new accounts may need a GPU quota increase.

**Managed alternative:** if setup time is worth more than the savings, **AirGPU's L40S tier** ($1.20/hr → **$4.80 for 4 hours**, plus ≥$7/mo storage) is a ready Windows desktop with Parsec/Moonlight guidance and nothing to administer — nearly the AWS G5 total with none of the AWS work. And if this becomes a *regular* habit rather than one session, **Shadow PC Power** (~$54.99/mo reported, 210 h/mo cap) beats every hourly option past roughly 50–120 hours a month — but it is a subscription, not an hourly rental.

**Streaming layer notes:** Parsec's Personal tier is **free**, and its licence covers personal non-commercial use including hosted machines — commercial use requires Teams/Enterprise ($30–45/user/mo) per Parsec's own pricing page; Warp ($9.99/mo) adds 4:4:4 colour and multi-monitor. Sunshine + Moonlight is the free open-source alternative with no licence tier at all. Budget note: UE5 itself and the Epic launcher install free on any of these; the project disk is the only persistent cost that follows you between sessions.

## Sources

- TensorDock — https://www.tensordock.com/cloud-gpus.html · Parsec-on-TensorDock guide: https://docs.tensordock.com/virtual-machines/using-parsec
- Google Cloud — https://cloud.google.com/products/compute/pricing/accelerator-optimized · https://cloud.google.com/compute/gpus-pricing · https://cloud.google.com/compute/disks-image-pricing
- AWS — https://aws.amazon.com/ec2/pricing/on-demand/ · https://aws.amazon.com/ec2/instance-types/g5/ · https://aws.amazon.com/ebs/features/ · Amazon DCV: https://docs.aws.amazon.com/dcv/latest/adminguide/enable-quic.html
- Azure — https://azure.microsoft.com/en-us/pricing/details/virtual-machines/ · https://learn.microsoft.com/azure/virtual-machines/nva10v5-series · NVv3 retirement: https://learn.microsoft.com/en-us/azure/virtual-machines/sizes/lifecycle/retirement/nvv3-series-retirement · https://azure.microsoft.com/en-us/pricing/details/managed-disks/ · Retail Prices API: https://prices.azure.com/api/retail/prices
- AirGPU — https://airgpu.com · SensePC — https://sensepc.com
- Shadow — https://shadow.tech/us/shadowpc/offers/ · https://support.shadow.tech/hc/en-us/articles/31001157820049-Shadow-PC-Gaming-Offers-Hardware-Specifications
- Paperspace — https://docs.digitalocean.com/products/paperspace/pricing/ · Windows retirement: https://docs.digitalocean.com/products/paperspace/machines/details/features/ · third-party tracker (labelled): https://getdeploying.com/paperspace
- Vast.ai — https://docs.vast.ai/linux-virtual-desktop · VM announcement: https://Vast.AI/article/announcing-virtual-machine-rental-on-vast-ai · host requirements: https://vast-ai.crisp.help/en/article/feasibility-of-machine-hosting-on-wsl-xr08ca/
- Lambda — https://lambda.ai/pricing · https://docs.lambda.ai/public-cloud/on-demand/creating-managing-instances/
- Parsec — https://parsec.app/pricing · Maximum Settings — https://maximumsettings.com · Cloudalize — https://www.cloudalize.com · OVHcloud — https://www.ovhcloud.com/en/lp/find-your-gpu/ · OCI — https://www.Oracle.com/ae/cloud/compute/faq/

## How I checked it

- Prices come from each provider's own public pricing/product pages or official price APIs (Azure's Retail Prices API), read 2026-10-18. Where a provider's price was only visible via JavaScript (Shadow's offers page, AWS's on-demand tables), the figure is either labelled third-party-reported (Shadow) or rebuilt transparently from the provider's own published components (AWS: published Linux list rates + AWS's stated $0.046/vCPU/hr Windows licence component — the same $0.046 figure Azure's and Google's official pages independently confirm).
- Windows availability was checked as a separate question from GPU availability for every provider — which is what killed Vast.ai (Ubuntu-only hosts/templates), Lambda (Linux images only), Paperspace (official 2024 Windows-template retirement) and OVHcloud's GPU line (no Windows image found).
- Session totals multiply the verified hourly figures by 4 and add the session-metered share of disk costs; monthly disk figures are shown separately so a kept project disk isn't hidden inside an hourly number.
- Nothing was signed up for, rented, or purchased; no provider was contacted.

## Unsure about

- **TensorDock live prices** vary by host in its dashboard; the $0.35/hr RTX 4090 figure is the official page/homepage "from" price (page footnoted July 2024). Minimum deposit: not found on public pages.
- **AWS Windows totals** are computed (Linux list + official Windows component), because AWS's on-demand tables didn't render as text; the arithmetic and both inputs are shown, but treat the totals as ≈.
- **GCP on L4/G2**: the NVIDIA vWS graphics-licence line for L4 was not found on Google's pricing page (only T4/P4/P100/V100 are listed) — confirm the supported Windows graphics-driver path before relying on G2 for the editor.
- **AirGPU's Windows licence position** is not stated on its own pages (a third-party review claims bring-your-own/extra fee; unverified). Its prices exclude VAT.
- **SensePC's exact hourly rate per tier** is shown only inside its builder; $2.22 is the starting figure from its page data.
- **Shadow's current US checkout prices and extra-storage price** are not readable on its public pages (JavaScript-rendered); the monthly figures are third-party reports of Shadow's pricing page plus Shadow's own 2025 press release ($37.99 Neo starting rate).
- **Paperspace**: whether a Gradient plan is strictly required to run paid Core machines is not stated unambiguously on its pricing page — moot for Windows given the template retirement.
- Azure NV12s_v3/NV24s_v3 Windows rates were not captured — the series is retired, so its remaining published figures are Linux-only.
