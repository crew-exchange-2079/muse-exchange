RESULT muse-sm2-dream-20261121

# Dreaming up unorthodox uses for one old server

**The machine:** Intel S2600GZ board, 2x Xeon E5-2670 v2 (20 cores / 40 threads total), 188 GB ECC RAM, 3x 240 GB SAS SSDs, 5x 500 GB SAS spinning disks, 4x 1 GbE, 1x Mellanox ConnectX-3 (InfiniBand/40–56 Gb), basic onboard VGA, no GPU. It sits in a home basement and runs 24/7.

**The brief:** think freely — weird, playful, ambitious and practical are all welcome; nothing has to be sensible. Skip the obvious (generic NAS, plain VM host) unless there is a twist on it.

**One honest caveat before the fun starts:** this box is a space heater. Each E5-2670 v2 is a 115 W TDP part ([Intel](https://www.intel.com/content/www/us/en/products/compare.html?productIds=75275,75277,75279), read 2026-11-21), and community reports put dual E5-2600 v1/v2 systems at roughly 80–160 W idle and 250–500 W under load, with forum users reporting 160–300 W idle for similar dual-socket builds ([bigiron.cc](https://www.bigiron.cc/guides/how-much-electricity-does-a-typical-homelab-actually-use); [ServeTheHome forums](https://forums.servethehome.com/index.php?threads/replacing-the-e5-2670-space-heater.12108/), read 2026-11-21). At 24/7 that is real money on the power bill — and real heat in the basement. Every idea below should be weighed against that. (Or embraced: see idea 12.)

---

## The ideas

### 1. The CPU-only LLM lab — a 70-billion-parameter brain with no GPU at all
- **What it is:** Run large language models entirely on the CPUs with llama.cpp, using the RAM as the model's home.
- **Why this box suits it:** A 70B model at Q4 quantisation is about 40 GB, and pure-CPU inference needs roughly 64 GB of RAM for it ([tensorrigs.com](https://tensorrigs.com/blog/ram-for-local-llm/); [tyolab.com](https://www.tyolab.com/blog/2025/03/03-building-your-own-ai-rig-more-memory-more-power/), read 2026-11-21) — this box has 188 GB, so it can hold a 70B model, a second model, and a fat KV cache all at once. The 8 memory channels of a dual-socket board help, since CPU inference speed is largely memory-bandwidth-bound.
- **How hard:** Afternoon. Install llama.cpp, download a GGUF model, serve it. Expect 1–3 tokens/second for a 70B — slow, but free, private, and perfect for overnight batch jobs like summarising a pile of documents while you sleep.

### 2. The volunteer-science furnace
- **What it is:** Donate the box's idle cycles to BOINC projects (Einstein@Home hunting pulsars, Rosetta@Home folding proteins, LHC@Home) or Folding@home.
- **Why this box suits it:** 40 threads doing nothing at 3 a.m. is a waste; BOINC is built exactly for that, and Folding@home and Einstein@Home are long-running, peer-reviewed projects ([en.wikipedia.org](http://en.wikipedia.org/wiki/List_of_distributed_computing_projects); [vcomp.org](https://www.vcomp.org/en/projects), read 2026-11-21). A 24/7 basement box is the ideal volunteer — it never sleeps, never gets rebooted for a Zoom call.
- **How hard:** Afternoon. Install the client, pick projects, set a CPU cap so the fans don't wake the house.

### 3. The basement stratum-1 time server
- **What it is:** Your house's own atomic-grade clock: a GPS receiver with a PPS (pulse-per-second) output feeding chrony, making the box a stratum-1 NTP server for the whole LAN.
- **Why this box suits it:** A GPS receiver gives time straight from satellites (stratum 0), so anything fed by it is stratum 1 ([tashian.com](https://tashian.com/guides/gpsd-time-server-manjaro/); [w5isp.com](https://w5isp.com/blog/gps-ntp-pi/), read 2026-11-21). The box is already on 24/7, has ECC RAM (no silent bit-flips in the clock discipline), and serves time to every device in the house with sub-microsecond bragging rights.
- **How hard:** Weekend. Needs a USB GPS receiver with PPS output and an antenna with a view of the sky — the basement location is the real boss fight here; a long antenna cable run to a window or outside is likely required.

### 4. The personal air-traffic control tower
- **What it is:** An ADS-B receiver that tracks every aircraft overhead on a live map, fed by a cheap USB software-defined radio.
- **Why this box suits it:** ADS-B aircraft broadcast their position twice a second on 1090 MHz, and a home station needs only an antenna, an RTL-SDR dongle and a decoder like readsb or dump1090-fa ([adsbhive.org](https://adsbhive.org/learn/build-an-ads-b-receiver), read 2026-11-21). The box is always on, has the SAS SSDs for logging years of flight tracks, and the 5 spinning disks are perfect for a "every plane that ever flew over my house" archive.
- **How hard:** Afternoon, plus antenna wrangling. Same basement-sky problem as idea 3 — the antenna wants height and a clear horizon, so this one lives or dies on a cable run upstairs.

### 5. A capsule on the small web — Gemini (and Gopher) server
- **What it is:** Host a Gemini capsule (and a Gopher hole for the true retro crowd) serving plain-text pages on port 1965 — a tiny corner of the internet that has no ads, no tracking, no JavaScript.
- **Why this box suits it:** Gemini is deliberately lightweight; "practically any computer produced in the past 30 years can host a Gemini capsule," and a Raspberry Pi Zero is considered plenty ([makeuseof.com](https://www.makeuseof.com/build-a-gemini-server-linux/), read 2026-11-21). Running it on 188 GB of ECC RAM and 40 threads is gloriously, deliberately absurd — like using a freight train to deliver a postcard. The Geminispace has only around 2,750 capsules ([john.soban.ski](https://john.soban.ski/gemini.html), read 2026-11-21), so one more is a real contribution.
- **How hard:** Afternoon. A Gemini server like Agate plus a folder of text files, and you are live.

### 6. The one-node "distributed storage" laboratory
- **What it is:** Learn Ceph — the distributed storage system that normally demands a cluster — by running a deliberately wrong, single-node Ceph lab, plus a ZFS pool with an enormous ARC cache, just to see what breaks and why.
- **Why this box suits it:** Ceph's rule of thumb is about 1 GB of RAM per TB of storage and a minimum of 3 nodes ([people.redhat.com](https://people.redhat.com/bhubbard/nature/nature-new/start/hardware-recommendations); [datazone.de](https://datazone.de/en/aktuelles/ceph-vs-zfs-wann-was/), read 2026-11-21) — this box has the RAM (188 GB for only ~3 TB of disks is wildly over-provisioned) and the SAS SSDs for journals, but only one node, which is exactly what makes it a good lab: you learn the failure modes without risking real data. Meanwhile ZFS wants about 1 GB RAM per TB too ([proxmox.com](https://www.proxmox.com/en/products/proxmox-virtual-environment/requirements), read 2026-11-21), so the ARC cache could swallow the entire pool.
- **How hard:** Project. Ceph on one node is a weekend of cursing; understanding it is a month. Keep it a lab — do not store anything you love in it.

### 7. The InfiniBand RDMA playground — 56 Gb/s in a basement
- **What it is:** A test bench for RDMA (Remote Direct Memory Access): NVMe-over-Fabrics, RDMA-accelerated storage, MPI cluster computing, and kernel-bypass networking — datacentre tech, at home, for fun.
- **Why this box suits it:** The ConnectX-3 does InfiniBand FDR at 56 Gb/s (14 Gb/s per lane) or 40 Gb Ethernet, with sub-microsecond latency via RDMA ([lenovopress.lenovo.com](https://lenovopress.lenovo.com/tips0872.pdf); [theregister.com](https://www.theregister.com/off-prem/2011/06/06/mellanox-forges-switch-hitting-connectx-3-adapters/943278?page=2), read 2026-11-21). That is 56x the speed of its own 1 GbE ports. Pair it with a second cheap ConnectX-3 box (or even a laptop with a Thunderbolt adapter) and you have a fabric most small companies don't own.
- **How hard:** Project. RDMA tooling is fiddly, old Mellanox drivers on modern kernels can fight you, and you need a peer at the other end of the cable. But the day `ib_write_bw` prints 50+ Gb/s between two machines in your house is a great day.

### 8. The family Matrix homeserver — your own private chat network
- **What it is:** A self-hosted Matrix (Synapse) homeserver with Element clients, so family and crew chat lives on your own hardware, federated with the wider Matrix network if you want.
- **Why this box suits it:** Synapse needs only about 1 GB of free RAM to join large public rooms, and 2 GB is comfortable for a small deployment ([matrix-org.github.io](https://matrix-org.github.io/synapse/v1.42/setup/installation.html); [dev.to](https://dev.to/selfhostingsh/how-to-self-host-matrix-synapse-with-docker-compose-4on8), read 2026-11-21) — this box has roughly 90x that, so it can run Synapse, PostgreSQL, a TURN server for voice/video calls, and bridges to other chat networks all at once without noticing. ECC RAM matters here too: chat history is the kind of data that quietly corrupts.
- **How hard:** Weekend. Docker Compose, a domain, TLS, and Postgres instead of SQLite. The ongoing work is moderation and backups, not compute.

### 9. The personal Wayback Machine
- **What it is:** An ArchiveBox-style web archive that saves full copies of pages you care about — the articles, manuals, forum threads and docs that vanish when a site dies — plus a full-text search index over all of it.
- **Why this box suits it:** 40 threads can crawl and render pages in parallel, 188 GB of RAM can hold a huge search index in memory, and the 5 spinning disks are exactly the right shape for a write-once, read-rarely archive (slow, cheap per byte, always spinning). The SAS SSDs hold the index; the spinners hold the history.
- **How hard:** Weekend. Set up the archiver, point it at a bookmark list, let it chew. The project part is curating what to save — the web is big, your disks are not.

### 10. The retro-computing time machine — 40 simultaneous vintage machines
- **What it is:** A museum of computing history running live: DOS, Windows 95/98/XP, classic Mac OS, Amiga, IRIX, VMS, OS/2 — one VM per era, all booted at once, accessible from any browser in the house.
- **Why this box suits it:** 40 threads means one thread per vintage machine with room to spare, and each old OS needs comically little RAM — you could give every VM 2 GB and still have 100 GB left. The board's 24 DIMM slots and 768 GB ceiling ([intel.com](https://www.intel.com/content/www/us/en/products/compare.html?productIds=/56260&e=t), read 2026-11-21) mean the only limit is your patience for floppy-disk images.
- **How hard:** Weekend to get the first few running; project to build the full museum with networking, shared files and a nice front page. The VGA-only output doesn't matter — it's all remote console.

### 11. The compile farm — a build server that eats code for breakfast
- **What it is:** A distcc / ccache / Nix remote-builder box: point every laptop in the house at it and watch multi-minute builds finish in seconds.
- **Why this box suits it:** Compiling is embarrassingly parallel, and 20 cores / 40 threads at 2.5–3.3 GHz ([intel.com](https://www.intel.com/content/www/us/en/products/compare.html?productIds=75275,75277,75279), read 2026-11-21) will chew through a Linux kernel or a Chromium build while your laptop stays cool and quiet. The 188 GB of RAM means ccache can hold an enormous cache, and the SSDs are where the object files want to live.
- **How hard:** Afternoon for distcc on one project; weekend to wire it into every machine's workflow properly. The payoff is daily and immediate.

### 12. The heater that pays rent — basement climate control, honestly labelled
- **What it is:** Stop pretending the server is "just a server" and manage it as what it physically is: a 200–400 W heater that happens to compute. Put it on a smart plug with a power meter, schedule heavy jobs (backups, BOINC, compiles, model runs) for cold nights, throttle it on warm days, and let it take over from the basement's actual heater in winter.
- **Why this box suits it:** Dual E5-2600 v1/v2 systems idle around 80–160 W and hit 250–500 W under load ([bigiron.cc](https://www.bigiron.cc/guides/how-much-electricity-does-a-typical-homelab-actually-use), read 2026-11-21) — that is a small space heater's worth of heat, 24/7, in a basement that probably wants it for half the year. The 4x 1 GbE ports even let you segment it so the "heater" traffic never touches the rest of the LAN.
- **How hard:** Afternoon. A smart plug, a temperature sensor, and a cron job that pauses BOINC when the basement hits 25 °C. The philosophical shift — budgeting the power bill as heating, not computing — is free.

### 13. The honeypot and security playground
- **What it is:** A deliberately vulnerable network in a box: old unpatched VMs, a fake NAS full of tempting files, an SSH server that logs every break-in attempt — a safe place to learn attack and defence, and to watch what the internet actually does to an exposed machine.
- **Why this box suits it:** 40 threads and 188 GB can run a whole fake company at once (domain controller, file server, workstations, web server), isolated on its own VLAN via one of the four 1 GbE ports, while the SAS SSDs snapshot everything for rollback after each "incident". ECC RAM keeps the logs trustworthy.
- **How hard:** Project. The setup is a weekend; the learning is endless. One rule: it must never be reachable from the real internet except through a tightly controlled front door, or the playground becomes someone else's.

---

## My three favourites

### 1. The CPU-only LLM lab (idea 1)
It is the purest expression of what this specific box is good at: absurd amounts of RAM, no GPU, always on. A 70B model at Q4 needs about 40 GB and 64 GB of system RAM ([tensorrigs.com](https://tensorrigs.com/blog/ram-for-local-llm/), read 2026-11-21) — this box clears that bar three times over. It turns the machine's two biggest "flaws" (old CPUs, no GPU) into irrelevant details, and it produces something genuinely useful: a private, free, offline brain that works while you sleep. Slow is fine when the job runs overnight.

### 2. The InfiniBand RDMA playground (idea 7)
This is the one idea almost nobody with a home server can do, because almost nobody has a 56 Gb/s FDR InfiniBand card sitting in their basement. The ConnectX-3's 56 Gb/s ([lenovopress.lenovo.com](https://lenovopress.lenovo.com/tips0872.pdf), read 2026-11-21) is the single most exotic thing in the whole machine, and leaving it idle would be a waste of the best toy in the box. It is also the idea most likely to teach something genuinely rare and employable — RDMA, NVMe-oF, HPC fabrics — rather than something a $50 Raspberry Pi could already do.

### 3. The basement stratum-1 time server (idea 3)
It is small, it is silly, and it is perfect. Nobody in the house will ever notice that their clocks are now disciplined to GPS time within a few hundred nanoseconds ([w5isp.com](https://w5isp.com/blog/gps-ntp-pi/), read 2026-11-21) — and you will mention it at every available opportunity anyway. It costs almost nothing, uses almost no resources, and converts the server from "old box in the basement" into "the reason every clock in the house is right." The antenna-cable adventure through the basement ceiling is a feature, not a bug.

---

## How I checked it

- **CPU:** Xeon E5-2670 v2, 10 cores / 20 threads per socket, 2.5 GHz base / 3.3 GHz turbo, 115 W TDP, launched Q3 2013 — [Intel product comparison](https://www.intel.com/content/www/us/en/products/compare.html?productIds=75275,75277,75279) and [Technical City](https://technical.city/en/cpu/Xeon-E5-2670-v2), read 2026-11-21.
- **Board:** Intel S2600GZ, 24 DIMM slots, DDR3 ECC up to 1866, 768 GB maximum memory, 2x PCIe x16 Gen 3 — [Intel product comparison](https://www.intel.com/content/www/us/en/products/compare.html?productIds=/56260&e=t), read 2026-11-21.
- **InfiniBand:** Mellanox ConnectX-3, FDR 56 Gb/s (14 Gb/s per lane), FDR10 40 Gb/s, PCIe 3.0 x8 — [Lenovo Press product guide](https://lenovopress.lenovo.com/tips0872.pdf) and [The Register](https://www.theregister.com/off-prem/2011/06/06/mellanox-forges-switch-hitting-connectx-3-adapters/943278?page=2), read 2026-11-21.
- **Power draw:** dual E5-2600 v1/v2 systems, roughly 80–160 W idle and 250–500 W under load; forum users report 160–300 W idle for similar builds — [bigiron.cc](https://www.bigiron.cc/guides/how-much-electricity-does-a-typical-homelab-actually-use) and [ServeTheHome forums](https://forums.servethehome.com/index.php?threads/replacing-the-e5-2670-space-heater.12108/), read 2026-11-21.
- **LLM RAM needs:** 70B at Q4 is ~40 GB; pure-CPU inference needs ~64 GB system RAM and runs at ~1–3 tokens/second — [tensorrigs.com](https://tensorrigs.com/blog/ram-for-local-llm/) and [tyolab.com](https://www.tyolab.com/blog/2025/03/03-building-your-own-ai-rig-more-memory-more-power/), read 2026-11-21.
- **Volunteer computing:** BOINC hosts ~30 projects; Folding@home (protein folding, since 2000), Einstein@Home (pulsar/gravitational-wave search), Rosetta@home, LHC@home are active — [Wikipedia list of volunteer computing projects](http://en.wikipedia.org/wiki/List_of_distributed_computing_projects) and [vcomp.org](https://www.vcomp.org/en/projects), read 2026-11-21.
- **Ceph / ZFS:** Ceph rule of thumb ~1 GB RAM per TB of storage, minimum 3 nodes; ZFS ~1 GB RAM per TB — [Red Hat Ceph hardware recommendations](https://people.redhat.com/bhubbard/nature/nature-new/start/hardware-recommendations), [datazone.de](https://datazone.de/en/aktuelles/ceph-vs-zfs-wann-was/), [Proxmox hardware requirements](https://www.proxmox.com/en/products/proxmox-virtual-environment/requirements), read 2026-11-21.
- **ADS-B:** aircraft broadcast on 1090 MHz about twice a second; a home station needs a 1090 MHz antenna, an RTL-SDR dongle and a decoder (readsb / dump1090-fa); range is line-of-sight, typically 150–250 nautical miles from a good antenna — [adsbhive.org](https://adsbhive.org/learn/build-an-ads-b-receiver), read 2026-11-21.
- **Stratum-1 NTP:** a GPS receiver is a stratum-0 source, so equipment fed directly by it is stratum 1; gpsd + chrony with a PPS signal is the standard home build — [tashian.com](https://tashian.com/guides/gpsd-time-server-manjaro/) and [w5isp.com](https://w5isp.com/blog/gps-ntp-pi/), read 2026-11-21.
- **Matrix:** Synapse needs at least 1 GB of free RAM to join large public rooms; 2 GB minimum for a small deployment — [Synapse installation docs](https://matrix-org.github.io/synapse/v1.42/setup/installation.html) and [dev.to guide](https://dev.to/selfhostingsh/how-to-self-host-matrix-synapse-with-docker-compose-4on8), read 2026-11-21.
- **Gemini:** Gemini sites are called capsules on port 1965; practically any computer from the past 30 years can host one; the Geminispace has roughly 2,750 capsules — [makeuseof.com](https://www.makeuseof.com/build-a-gemini-server-linux/) and [john.soban.ski](https://john.soban.ski/gemini.html), read 2026-11-21.
- All research was done with public web pages only. No logins, no accounts, no purchases, no messages or comments to anyone.

## Unsure about

- **The exact power draw of this specific box.** The 80–160 W idle / 250–500 W load figures are community reports for similar dual E5-2600 v1/v2 systems, not measurements of this machine. The only way to know is a wall-plug meter (e.g. Kill-A-Watt) on this box, with its actual disks and fans.
- **Whether the ConnectX-3 card in this box is the FDR (56 Gb/s) variant or a 40 GbE/QDR variant.** The task says InfiniBand/40–56 Gb; I could not verify the exact model from the task description alone. The link speed should be checked with `ibstat` / `ethtool` on the box itself.
- **Whether a GPS antenna can get a sky view from this basement.** Ideas 3 and 4 both depend on it, and I have no information about the house layout, window placement, or how long a cable run would be.
- **Whether the Mellanox ConnectX-3 still has working drivers on a current Linux kernel.** The card is from ~2011 and its vendor support has ended; I did not verify driver availability for any specific distribution or kernel version.
- **Exact CPU inference speed for a 70B model on this hardware.** The 1–3 tokens/second figure is a general guide for CPU-only 70B inference, not a benchmark on dual E5-2670 v2 with DDR3-1866. Real speed depends on memory bandwidth, thread count, quantisation and context length.
- **Whether single-node Ceph will actually run usefully on this box.** Ceph is designed for 3+ nodes; a single-node setup is a lab exercise, and I did not verify that current Ceph versions still support or tolerate a one-node deployment.
- **The exact RAM ceiling and DIMM population rules for this board revision.** Intel lists 768 GB maximum for the S2600GZ family, but the achievable maximum depends on DIMM type (RDIMM vs LRDIMM), rank and BIOS version, which I did not verify for this specific board.
- **Anything about the current software state of the box** — what OS it runs, what is already installed, disk health, or whether the SAS controller is in IT mode (needed for ZFS/Ceph). None of that was in the task description, so I did not assume it.
