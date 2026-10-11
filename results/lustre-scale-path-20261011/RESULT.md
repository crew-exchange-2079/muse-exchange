# Lustre + IBM Storage Scale (GPFS) — Practical 8-Week Self-Study Path
## For a Linux sysadmin strong on tape archives, RHEL and Ansible — target: HPC Storage Engineer roles in 2026

**Research date: 11 October 2026.** All version claims below were checked against the live/indexed sources cited for each claim. Where a source could not be opened or a 2026 version could not be confirmed, that is flagged in *Honest Gaps* — do not treat flagged items as verified.

---

## Summary — read this first

| Question | Verified answer (Oct 2026) |
|---|---|
| Lustre LTS | **2.15.8, released 2 Dec 2025** — current LTS maintenance release |
| Lustre current major | **2.17.0, released 29 Dec 2025**; 2.18.0 in development |
| Lustre Manual | Always-latest Operations Manual at doc.lustre.org (HTML/PDF/ePub) — see §1 |
| IBM Storage Scale classic stream | **5.2.3.x** — IBM recommends 5.2.3.8 (Jun 2026), latest listed 5.2.3.9 (Jul 2026). **Avoid 5.2.3.0/.1 — withdrawn** |
| IBM Storage Scale new major | **6.0.x** — Developer Edition installer in IBM's current Vagrant lab is **6.0.1.0**; Container Native 6.0.1.1 listed Aug 2026. Headline 6.0 feature is the Data Acceleration Tier for AI inference |
| Scale Developer Edition | **Yes, free, but gated.** Free for non-production test, **12 TB per cluster, RHEL on x86_64, no IBM support, no production use**, obtained only after an IBM registration form (IBM ID). There is also a separate 90-day prospective-customer trial via an IBM sales rep |
| Best-proven Lustre VM lab combo | **Rocky 9.4 + Lustre 2.16.1, ldiskfs, patched server kernel 5.14.0-427.x_lustre** — a complete, exercised 3-VM guide exists (July 2026). This is *not* the LTS — see the version trap in §3 |
| Best Scale VM lab | **IBM's own StorageScaleVagrant** — single-node cluster (VirtualBox / libvirt-KVM / AWS), Developer 6.0.1.0. Multi-node quorum behaviour must be built by extending it yourself |
| Truly free training | Lustre: everything (manual, wiki, Lustre 101, LUG/LAD slides+YouTube) is open, no login. Scale: IBM Documentation + Redbooks are open; IBM/Coursera Scale courses are **paid / subscription / free-trial only — not free** |

**The pitch in one line for this candidate:** tape/archive experience is not a detour — it maps directly onto Lustre HSM, Storage Scale ILM-to-tape / Spectrum Archive, HPSS, policy engines, recall storms, and media/lifecycle discipline, which most pure-disk HPC candidates cannot talk about credibly. Weeks 7–8 exploit that deliberately.

---

## 1. Free Official Docs & Training

### 1.1 Lustre — all open, no login

- **Lustre Operations Manual (the Manual):**
  - Landing / documentation page: https://www.lustre.org/documentation/
  - HTML: http://doc.lustre.org/lustre_manual.xhtml
  - PDF: http://doc.lustre.org/lustre_manual.pdf
  - ePub: http://doc.lustre.org/lustre_manual.epub
  - Important nuance from the landing page (paraphrased): manual releases are independent of Lustre software releases, so those links always serve the newest manual, with sections tagged for the releases they apply to. Do not hunt for a "2.15 manual PDF" — use these and check the tags.
- **Release truth source:** https://wiki.lustre.org/Lustre_Release_Information — *verified live 11 Oct 2026.* Lists 2.15.8 (LTS, 2 Dec 2025), 2.17.0 (major, 29 Dec 2025), 2.18.0 (in development).
- **Community wiki (start page, Lustre 101, Systems Administration Guide, How-Tos, Benchmarking Guide, LNet Router Guide, Robinhood):** https://wiki.lustre.org/ — via the main-page revision found in search: https://wiki.lustre.org/index.php?title=Main_Page&diff=cur&oldid=4648
- **Whamcloud / DDN community wiki, Documentation page and Support Matrix:** https://wiki.whamcloud.com/display/PUB/Lustre+Support+Matrix?src=contextnavpagetreemode — **check this before every install**; it is the matrix of distro/kernel/ZFS/e2fsprogs combinations actually tested per release.
- **Downloads (open):** https://downloads.whamcloud.com/public/lustre/ and e2fsprogs https://downloads.whamcloud.com/public/e2fsprogs/ (linked from the wiki main page above).
- **Build-from-source walkthrough (RHEL/Rocky 8.10, master):** https://wiki.whamcloud.com/spaces/PUB/pages/258179277/Walk-thru-+Build+Lustre+MASTER+on+RHEL+Rocky+linux+8.10+from+Git — useful in Week 2 to understand *why* the server kernel is patched; do not use it as your first lab (use prebuilt RPMs).
- **Lustre 101 / new-user training (free PDFs):**
  - New User Training, LUG 2019: https://wiki.lustre.org/images/4/48/LUG2019-New-User-Class.07.pdf
  - Sysadmin Tutorial, LUG 2019 (ORNL authors; tuning, monitoring, recovery, striping/QoS/PFL/DoM): http://wiki.lustre.org/images/0/0d/LUG2019-Sysadmin-tutorial.pdf
  - Dated but still the best free structured intro set. Pair with the current Manual for commands.
- **LUG (Lustre User Group) archives:**
  - Conference index (agendas, slides, videos per year): https://wiki.lustre.org/index.php?title=Lustre_Conferences&oldid=5187
  - LUG 2025 (Stanford, 1–2 Apr 2025; presentations + videos linked from wiki): https://www.opensfs.org/lug-2025/
  - Past-events index incl. **LUG 2026 (Indiana University, Indianapolis, 28–29 Apr 2026)** and LAD24: https://www.opensfs.org/past-events/
  - LUG 2026 YouTube examples (OpenSFS channel — search "LUG 2026" there for the full set): Community Update https://www.youtube.com/watch?v=tuqmP62xoqo ; MLPerf Storage & Lustre https://www.youtube.com/watch?v=nMTmhT4S7wY ; Hybrid I/O https://www.youtube.com/watch?v=cm95yMEcu1w
- **LAD (Lustre Administrators & Developers Workshop, Europe, CEA/EOFS/OpenSFS):** listed on the same conference index and past-events pages above. Most recent editions confirmed in sources: LAD24, Paris, 23–24 Sep 2024. **A dedicated LAD25 programme page was not found in this research — see Honest Gaps.** lustre.org listed "LAD 2025" as an event (via https://www.lustre.org/event/lug-2013/ search snippet — treat that as a pointer, not a programme).
- **Whamcloud paid training/support:** DDN/Whamcloud sell training and support; no free, open Whamcloud instructor course was found. The free substitute is: Manual + Lustre 101 PDFs + LUG/LAD talks + the lab in §3. State this honestly in interviews ("self-study via community materials") rather than claiming a certificate that does not exist.

### 1.2 IBM Storage Scale (GPFS) — docs open, software gated

- **Version truth source — IBM PSP / version recommendations:** https://www.ibm.com/support/pages/node/707017 — indexed Oct 2026: 5.2.x stream minimum 5.2.0.1 (Jun 2024), **recommended 5.2.3.8 (Jun 2026), latest 5.2.3.9 (Jul 2026)**; Container Native 6.0.1.0 (Jun 2026) / 6.0.1.1 (Aug 2026); CSI 3.1.1 (Aug 2026). Also carries the alert that **5.2.3.0 and 5.2.3.1 were removed** (NFS/SMB issues) and replaced by 5.2.3.2+.
  - ⚠️ So the mission's premise "5.2.x / 5.3.x" needs correction: **no 5.3.x stream was found in any Oct-2026 IBM source. The successor stream is 6.0.x.** Study 5.2.3 concepts (they carry into 6.0) and be able to say "6.0 is current, with DAT".
- **IBM Documentation (Knowledge Center successor):** IBM Docs URLs are versioned PDFs / doc sets. Directly confirmed:
  - Quick Start Guide 5.2.0 (install steps, editions pointer, Passport Advantage download note): https://www.ibm.com/docs/en/STXKQY_5.2.0/pdf/scale_qsg_520.pdf
  - Concepts, Planning & Installation Guide 5.2.2 (installer toolkit, quorum algorithm, NSD/GUI/protocol deployment): https://www.ibm.com/docs/en/STXKQY_5.2.2/pdf/scale_ins.pdf
  - Product editions page (edition/feature comparison, Developer Edition limits): https://ibm.com/docs/en/storage-scale/5.1.9?topic=overview-storage-scale-product-editions — *note: this is the 5.1.9 doc set as indexed; the edition limits quoted are from this page, re-check in the 5.2.3/6.0 doc set when you register.*
  - FAQ (authoritative for kernels, tuning, trial): https://www.ibm.com/docs/en/storage-scale?topic=STXKQY/pdf/gpfsclustersfaq.pdf
  - Container Native 5.2.3 docs (linked from IBM's own GitHub): https://www.ibm.com/docs/en/scalecontainernative/5.2.3 and 6.0.1: https://www.ibm.com/docs/en/scalecontainernative/6.0.1
  - *Access note: a direct fetch of an IBM Docs 5.2.3 landing URL returned HTTP 403 in this research session. IBM Docs is normally public in a browser, but expect bot/geo friction; the PDFs above and the PSP page are the reliable entry points.*
- **Developer Edition / trial — the exact answer:**
  - Signup: https://www.ibm.com/account/reg/us-en/signup?formid=urx-41728 — form asks email, first/last name, country. **Requires an IBM ID / registration. Not anonymous, not truly "no-login free".**
  - Limits (from the editions page, paraphrased): RHEL on x86_64 only; all Data Management Edition features; **12 TB per cluster**; free; **non-production only; no IBM support**.
  - Node limit: **none stated in the sources found** — do not quote a node cap. Capacity (12 TB) is the stated cap.
  - 90-day trial: per the FAQ, a free 90-day trial exists for prospective customers **via an IBM sales representative** — that is a sales-gated evaluation, different from the self-service Developer Edition signup.
  - 6.0.1.0 is the Developer build IBM's current Vagrant lab expects: installer filename `Storage_Scale_Developer-6.0.1.0-x86_64-Linux-install` (see §3.2).
- **IBM Redbooks (free PDFs, no login):**
  - **New and directly on-syllabus:** *IBM Storage Scale: Working With Abstract Data*, SG24-8602, published 2 Jul 2026: https://redbooks.ibm.com/abstracts/sg248602.html — storage pools, filesets, ILM, HSM, AFM, data acceleration, university use case. **Read this in Week 4 — it is the closest thing to a free Scale textbook in 2026.**
  - Older core book (Spectrum Scale 4.1 era — concepts still valid, commands/versions dated): SG24-8254 http://www.redbooks.ibm.com/abstracts/sg248254.html?Open
- **Free training — honest classification:**
  - *Truly open, no login:* IBM Documentation, FAQ, Redbooks above; Spectrum Scale User Group talks (example found: https://www.spectrumscaleug.org/wp-content/uploads/2020/07/SSUGDigital-2-Spectrum-Scale-stretched-cluster-best-practices.pdf).
  - *Free IBM ID required:* Developer Edition signup (above). IBM Training portal courses generally require an IBM ID.
  - * NOT free:* IBM Storage Scale courses on Coursera — e.g. https://www.coursera.org/learn/ibm-storage-scale-administration — Coursera's own FAQ (indexed) says certificate access requires purchase, a free trial, or financial aid. IBM's announcement https://www.ibm.com/new/training/elevate-your-data-management-skills-with-new-ibm-storage-scale-courses confirms the full courses sit in paid IBM Learning Subscriptions (SUBR040G/042G) or the paid Coursera Specialization "Learn Enterprise Data Storage with IBM Storage Scale". Budget for it only if an employer pays; the Redbook + docs + Vagrant lab cover the same syllabus for self-study.
- **ESS context (know the words, don't buy hardware):** ESS = IBM Storage Scale System, the appliance implementation; its numbering is +1 in the first digit vs Scale software (e.g. System 6.1.9.8 uses Scale 5.1.9.12 — per the PSP page). Protocol nodes / CES (Cluster Export Services) = the nodes serving NFS/SMB/S3/Object/HDFS in front of GPFS; in the Ansible collection these are the optional CES roles (§3.3). Interviewers use "ESS", "CES/protocol node", "NSD server" interchangeably with the software concepts — learn them as vocabulary in Week 4.

---

## 2. The 8-Week Plan

> Time assumption: ~8–12 hrs/week alongside a job. Every week ends with a **deliverable in a public GitHub repo** — that repo *is* the portfolio. Suggested repo name: `lustre-scale-lab` with `week-notes/`, `ansible/`, `benchmarks/`, `runbooks/`.

### Weeks 1–2 — Lustre foundations (no lab yet, or lab-lite)

**Reading:**
- Manual (doc.lustre.org HTML above): architecture (MGS/MGT, MDS/MDT, OSS/OST, client, LNet), file layout/striping, DNE, PFL, DoM, quotas, changelogs, HSM, recovery.
- Lustre 101 PDFs (§1.1), then LUG 2019 Sysadmin Tutorial.
- Release pages: contrast 2.15.8 LTS vs 2.17.0 (§1.1) and read the Support Matrix top-to-bottom — being able to explain the LTS/feature-release model is an interview question in itself.
- Watch: 3× LUG 2026 talks (§1.1) + 2× LUG 2025 talks via https://www.opensfs.org/lug-2025/

**Lab tasks:**
- Wk1: On a single throwaway VM, install *client-only* packages and practise `lfs`/`lctl` help, `modprobe`, LNet config syntax — no filesystem needed. Write the component diagram from memory until you can draw it cold.
- Wk2: Read the build walkthrough (RHEL 8.10, §1.1) and the lab guide (§3.1) end-to-end *before* building. Pre-provision the 3 VMs, snapshots at "clean OS".

**Deliverable:** `week-notes/lustre-architecture.md` — one-page diagram + glossary (MGT/MDT/OST, DNE, PFL, DoM, FLR, PCC, LNet NID/router, OST pool, changelog, copytool) + a version memo: "LTS is X, current is Y, matrix says server OS is Z, and here's why that dictates my lab OS."

### Week 3 — Lab build: Lustre

**Reading:** §3.1 in full; Manual chapters on installation, `mkfs.lustre`, `tunefs.lustre`, LNet configuration.

**Lab tasks:** Build the 3-VM cluster exactly as §3.1. Snapshot before `mkfs`. Then Exercises 1–3 (§4). Rebuild once from your own Ansible (Week 3 stretch: §3.3) — a scripted rebuild is worth more than a hand-built cluster that works once.

**Deliverable:** Working `labfs`, `lfs df -h` / `lfs osts` output pasted into the repo, plus `ansible/` or shell scripts that rebuild it, plus a "what broke and why" log (everyone's first build breaks on LNet or kernel mismatch — documenting it is the credible part).

### Week 4 — Scale foundations

**Reading:**
- Redbook SG24-8602 (§1.2) — pools, filesets, ILM/HSM, AFM chapters first.
- Install Guide 5.2.2 PDF (§1.2): cluster concepts — quorum/manager/NSD roles, CCR, `spectrumscale` installer toolkit, NSDs, failure groups.
- FAQ (§1.2): quorum, tiebreaker disks, kernel cautions. Note specifically: IBM warned that RHEL 9.4 kernel 5.14.0-427.87.1+ needs Scale ≥5.2.3.4 — a perfect example of the kernel-pinning discipline you already learned with Lustre. Source for that alert: https://www.ibm.com/support/pages/node/7244835
- Editions page (§1.2): know Data Access vs Data Management vs Erasure Code vs Developer cold.

**Lab tasks:** Register for Developer Edition (§1.2) *this week* — registration/download friction is the schedule risk, so start it before you need it. While waiting: learn the `mm*` command families on paper (`mmcr*`, `mmls*`, `mmch*`, `mmadd*`, `mmdel*`, `mmdf`, `mmhealth`, `mmpmon`) and map each to its Lustre analogue in a table.

**Deliverable:** `week-notes/scale-vs-lustre.md` — concept map (NSD≈OST target+disk, fileset≈directory+quota+pool placement, storage pool≈OST pool, ILM policy≈Robinhood/HSM policy, AFM≈—no clean Lustre analogue, CES≈gateway/NFS-Ganesha node) + Developer Edition download evidence (version + filename, *not* credentials).

### Week 5 — Lab build: Scale

**Reading:** StorageScaleVagrant README (§3.2); Install Guide chapters on `mmcrcluster`, NSD creation, `mmcrfs`.

**Lab tasks:** Single-node Vagrant cluster first (Exercises 8–9, single-node subset). Then extend to 3 VMs (§3.2) and redo cluster/filesystem creation *by hand with `mm*` commands*, not just the toolkit — interviewers ask for the `mm` commands. Create a second storage pool + fileset, write an ILM placement policy, run it with `mmapplypolicy` in preview mode.

**Deliverable:** `mmlscluster`, `mmlsfs`, `mmlsnsd`, `mmdf` outputs in repo; your hand-run command transcript; a paragraph on quorum: what happens when 1 of 3 quorum nodes dies vs 2.

### Week 6 — Performance & benchmarking

**Reading:** Manual benchmarking sections; IOR repo/docs (§4, Ex.7); LUG 2026 MLPerf talk (§1.1); Redbook performance/pool chapters.

**Lab tasks:** Exercises 2 (again, measured), 7 and 10. Vary *one* thing at a time: stripe count 1→2→all, stripe size, IOR transfer size, Scale block/pool placement. Record host, versions, exact command, result in a table — never a bare "it was faster".

**Deliverable:** `benchmarks/results.md` — IOR + mdtest tables for *both* filesystems on the *same* VM host, with a written explanation of why mdtest (metadata) and IOR (streaming) stress different servers (MDS/fileset manager vs OSS/NSD).

### Week 7 — Failure, HSM & day-2 ops

**Reading:** Manual: recovery, failover, LFSCK, HSM, changelogs, quotas. Redbook: HSM/ILM chapter again, now hands-on. Your tape background is the textbook here — read the HSM sections critically and note where vendor docs gloss over recall/queueing reality.

**Lab tasks:** Exercises 4, 5, 6, 9, 10. Deliberately: kill an OSS, deactivate an OST, fill an OST, archive/release/restore a file, break and repair LNet, run a health-check script on Scale (`mmhealth`) and Lustre (`lfs check`, `lctl`).

**Deliverable:** Two runbooks in the repo: `runbooks/lustre-ost-failure.md` and `runbooks/hsm-recall-storm.md` — written as if for an on-call colleague at 03:00. Runbooks are what hiring managers actually read.

### Week 8 — Interview prep & portfolio

**Reading:** §5 of this report; re-read your own week-notes;skim 5 current job ads (start with §5 sources) and highlight every keyword you cannot yet explain.

**Lab tasks:** Clean rebuild of *both* labs from your automation, timed. Mock-interview yourself out loud on the 24 questions in §5. Add a top-level repo README: architecture diagrams, versions used, what you built, benchmark table, runbook links, and an honest "lab limits" section (single client, TCP not IB, no real tape library — HSM backend was a directory/posix copytool).

**Deliverable:** Public repo + a 1-page "HPC storage — skills & evidence" summary mapping each §5 topic → where in the repo you proved it. That document is what you send with applications.

---

## 3. Lab Specs

### 3.1 Lustre lab — exact combo that works in 2026

**⚠️ The version trap (the single most important lab fact):** Lustre *servers* need a Lustre-patched kernel built for one exact distro point-release. The Support Matrix (https://wiki.whamcloud.com/display/PUB/Lustre+Support+Matrix?src=contextnavpagetreemode) shows, in summary:

| Lustre | Server OS (tested) | Client OS (tested) | ZFS |
|---|---|---|---|
| 2.15.8 (LTS) | RHEL 8.10 | RHEL 8.10 / 9.7, SLES15 SP6, Ubuntu 22.04 | 2.3.2 |
| 2.16.1 | RHEL 9.4 | RHEL 9.4, SLES15 SP6, Ubuntu 24.04 | 2.1.15 |
| 2.17.0 | RHEL 9.7 | RHEL 9.7 / 10.1, SLES15 SP7, Ubuntu 24.04 | 2.3.4 |

So "Rocky 9 + latest Lustre" fails unless the point-release matches. Pick ONE row and pin everything (disable distro updates / snapshot the VMs).

**Recommended primary path — the proven one:**
Source (exercised end-to-end, created Jul 2026, *verified live in this research*): https://github.com/pearapat-san/lustre-hpc-lab

| Item | Value in that lab |
|---|---|
| Hypervisor | VMware Workstation (same layout works in KVM/libvirt or VirtualBox — two NICs: host-only/internal for LNet + NAT for packages) |
| OS | Rocky Linux 9.4 Minimal, all VMs |
| Lustre | 2.16.1, Whamcloud el9.4 RPMs, **ldiskfs** backend |
| Server kernel | 5.14.0-427.31.1_lustre.el9 (patched, from Whamcloud repo) |
| Client kernel | 5.14.0-427.13.1.el9_4 (stock — client is patchless, `kmod-lustre-client`) |
| LNet | `tcp0` over host-only 192.168.100.0/24 |

| VM | Role | vCPU/RAM | Disks | Notes |
|---|---|---|---|---|
| `mgsmds` 192.168.100.10 | MGS+MDS (combined is fine at lab scale) | 2 / 2 GB (4 GB more comfortable) | 20 GB OS + 10 GB MDT (`/dev/sdb`) | `mkfs.lustre --fsname=labfs --mgs --mdt --index=0` |
| `oss` 192.168.100.11 | OSS | 2 / 2 GB | 20 GB OS + 10 GB OST0 + 10 GB OST1 | Two OSTs on one OSS is deliberate — it teaches striping without a 4th VM |
| `client` 192.168.100.12 | Client | 2 / 2 GB | 20 GB OS only | `mount -t lustre mgsmds@tcp0:/labfs /mnt/labfs` |

Lab rules taken from that guide's hard-won notes (paraphrased): confirm devices with `lsblk` before any `mkfs.lustre` (device letters changed across reboot in that build); persist server mounts by UUID in `/etc/fstab` with `_netdev`; lab-only shortcut — firewalld/SELinux disabled (learn to say in interviews that production would use proper rules/policy, not disabling); boot order MGS/MDS → OSS → client.

**ldiskfs vs ZFS — decision:** Start **ldiskfs**. Reasons: (1) the proven lab and most RHEL production sites use it; (2) it exercises `e2fsck`, LFSCK and the Whamcloud e2fsprogs you will be asked about; (3) ZFS adds a second learning curve (pools, datasets, `zpool` targets, different failure model) plus the exact ZFS version from the matrix (2.3.x for current releases). Do ZFS as a *Week 7 stretch rebuild* of one OST and write the comparison — that comparison is itself interview material. Do not start with ZFS.

**DKMS vs patched kernel — decision:** Servers: **patched kernel + prebuilt server RPMs** (the path above). Clients: prebuilt `kmod` for the exact stock kernel, or DKMS client where the distro offers it (e.g. Azure Managed Lustre offers both prebuilt kmod and DKMS — https://learn.microsoft.com/en-us/azure/azure-managed-lustre/connect-clients). Rule to memorise: *server = pin the kernel to Lustre; client = pin Lustre to the kernel (kmod) or rebuild it automatically (DKMS). Never `dnf update` a Lustre server casually.*

**Stretch path (LTS credibility):** After the primary lab works, note in your portfolio that production LTS today is 2.15.8 on RHEL 8.10 servers (matrix row above) — and optionally rebuild servers on Rocky 8.10 + 2.15.x. Do not start here: no comparably complete, current, free Rocky 8.10 step-by-step was verified in this research, and you would burn Week 3 on friction.

**Official install reference:** Manual installation chapters via http://doc.lustre.org/lustre_manual.xhtml plus the Whamcloud walkthrough in §1.1.

### 3.2 IBM Storage Scale lab — feasible, with honest caveats

**Official lab:** https://github.com/IBM/StorageScaleVagrant — *verified live in this research.* In summary: it provisions a **single-node** cluster on VirtualBox, libvirt (KVM/QEMU) or AWS; expects the Developer installer `Storage_Scale_Developer-6.0.1.0-x86_64-Linux-install` dropped into `software/` by you (it does **not** download it); creates filesystem `fs1` on 5 NSDs mounted at `/ibm/fs1`, plus a CES shared filesystem; GUI on host port 8888; CLI/REST API/GUI all enabled. That single-node box is the fastest route to real `mm*` commands, the GUI, and policies.

| VM plan (extend Vagrant to multi-node yourself) | Spec — *practical recommendation, not an IBM-published minimum (none was verified — see Gaps)* |
|---|---|
| `scale1` NSD + quorum + manager | 2–4 vCPU, 8 GB RAM (GUI is hungry; 4 GB without GUI), 25 GB OS + 3×10 GB NSD disks |
| `scale2` NSD + quorum | Same, 3×10 GB NSD disks |
| `scale3` NSD + quorum (+ client work) | Same, 2–3×10 GB NSD disks |
| Optional `scale-client` | 2 vCPU, 4 GB, 25 GB OS, no NSD disks — GPFS client / remote mount |

**Quorum — get this right:** Scale quorum is majority of *designated quorum nodes* (FAQ, §1.2). The installer toolkit's default (Install Guide 5.2.2, §1.2, paraphrased): <4 nodes → all nodes are quorum; 4–9 nodes → 3 quorum; 10–18 → 5; >18 → 7, preferring NSD nodes. Hence: **1 node works (Vagrant demo), 2 nodes is the fragile special case (needs tiebreaker disks to survive one loss), 3 nodes is the minimum sensible learning cluster.** A 4th VM as pure client is optional, not required.

**OS:** Developer Edition is RHEL x86_64 (§1.2). In practice the Vagrant project has historically used a CentOS/RHEL-family base box; for a hand-built 3-VM lab use RHEL 9.x / Rocky 9.x *only if your downloaded Developer build's FAQ/kernel list supports it* — check the FAQ for your exact build before installing, and heed the RHEL 9.4 kernel alert in Week 4. **Exact Rocky 9 support for the 6.0.1 Developer build was not verified in this research — see Gaps.** If the installer refuses a Rocky kernel, fall back to the Vagrant base box IBM ships the scripts for, rather than fighting the kernel module build on day one; then do the hand-built `mm*` cluster *inside* additional Vagrant-style VMs.

**Filesystem creation (hand-run, Week 5):** `mmcrcluster` → define NSDs (`mmcrnsd`) → `mmstartup` → `mmcrfs` → `mmmount` → verify with `mmlscluster / mmlsnsd / mmlsfs / mmdf`. Full syntax in the Install Guide (§1.2) — practise it, don't copy-paste it from this report.

**Caveats, stated plainly:**
1. Download is **registration-gated** (IBM ID form). It is free of charge, but it is not an anonymous open download like Lustre. Start registration in Week 4.
2. **No production use, no IBM support, 12 TB cap** (editions page).
3. The official Vagrant lab is **single-node by design** — quorum, NSD failure and restriping behaviour require your own multi-node extension. Budget Week 5 accordingly.
4. GUI + CES/Object stacks raise RAM sharply; learn CLI first, GUI second.
5. ESS is appliance hardware — you will learn its *concepts* (Week 4), you cannot lab it. Interviewers know this; claiming ESS hands-on from a VM lab would be a credibility error.

### 3.3 Ansible angle — leverage the candidate's strength

- **Scale — official, use this:** https://github.com/IBM/ibm-spectrum-scale-install-infra — IBM's install/config toolkit. In summary: a mandatory Core GPFS role set plus optional roles for GUI, NFS, SMB, Object, HDFS, Call Home, File Audit Logging, S3, with sample playbooks for storage/filesystems, node classes, CES and remote mounts. **Week 5 deliverable alternative:** deploy your 3-node lab with this, then diff what it did vs your hand-run `mm*` transcript.
- **Lustre — no single official community role; two honest options:**
  - NetApp E-Series Lustre collection (current, RHEL 9, HA-oriented, vendor-specific to E-Series backends): https://github.com/netapp/ansible-lustre — `ansible-galaxy collection install netapp_eseries.lustre`; roles for HA server, client, monitoring, tenant. Read it for structure even if you don't run E-Series.
  - Old client-only roles (e.g. https://github.com/jabl/ansible-role-lustre_client) are **EL7-era — flag as stale, do not present as current.**
  - **Best portfolio move:** write your *own* small role (repos → patched kernel + reboot handler → LNet config → `mkfs.lustre` guarded by a `blkid` check → mounts → client mounts) codifying §3.1. A small role you wrote and can explain beats a large downloaded one you cannot.

---

## 4. The 10 Hands-On Exercises

> Conventions: Lustre filesystem `labfs` mounted at `/mnt/labfs`; Scale filesystem `fs1` mounted at `/ibm/fs1`. Commands are the exercise targets — confirm flags in the current Manual / `man` pages in-lab (that checking habit is part of the exercise).

### Ex 1 — OST/MDT layout design (`mkfs.lustre`, `tunefs.lustre`)
**Goal:** Format MDT0 and OST0/OST1 with explicit fsname/index/MGS; inspect and change a persistent parameter with `tunefs.lustre --print` / a safe dry change; explain MGT vs MDT, index uniqueness, and why MDT sizing is inode-driven.
Commands: `mkfs.lustre --fsname=labfs --mgs --mdt --index=0 /dev/sdb` · `mkfs.lustre --fsname=labfs --ost --index=N --mgsnode=mgsmds@tcp0 /dev/sdX` · `tunefs.lustre --print /dev/sdb` · `lctl dl`
**Success check:** Client mount works; `lfs df -h` shows 1 MDT + 2 OSTs with expected capacity; you can state what breaks if two OSTs share an index.

### Ex 2 — Striping (`lfs setstripe`)
**Goal:** Prove stripe count/size/pool behaviour, not just set it.
Commands: `lfs setstripe -c 1|-c 2|-c -1 dir/` · `lfs setstripe -S 4M -c 2 file` (create *before* writing — striping is set at creation) · `lfs getstripe -v file` · pools: `lctl pool_create labfs.flash …`, `lctl pool_add …`, `lfs setstripe -p labfs.flash …`
**Success check:** `getstripe` shows objects on the expected `obdidx`s; a 1-stripe vs 2-stripe IOR/`dd oflag=direct` comparison is recorded (lab guide's own result, paraphrased: parallel writes across 2 OSTs were ~1.7× a single OST — reproduce your own number, don't quote theirs).

### Ex 3 — `lfs` day-2 commands
**Goal:** Fluency: capacity, health, finding hot/large data.
Commands: `lfs df -h` · `lfs df -i` · `lfs osts` · `lfs check servers` · `lfs find --type f --size +500M /mnt/labfs` · `lfs find --ost OST0001_UUID /mnt/labfs` · `lfs getstripe --ost-list`, `lfs path2fid` / `fid2path`
**Success check:** Given a planted large file on OST1, you find it, name its layout, and report per-OST free space/inodes without `find /` on the servers.

### Ex 4 — Quotas (user/group/project)
**Goal:** Enable, set, hit, and diagnose a quota.
Commands: `lctl conf_param` / quota enablement per Manual for your release · `lfs setquota -u alice -b 2G -B 3G -i 100k -I 110k /mnt/labfs` · `lfs quota -uh alice /mnt/labfs` · `lfs setquota -p <projid>` + `lfs project -s -p <id> -r dir/` (project quotas)
**Success check:** Writes fail with EDQUOT at the soft→hard boundary as predicted; `lfs quota` output explains block vs inode usage; you can explain why project quotas suit HPC group/scratch accounting (and the cross-project directory-rename gotcha: files rename atomically across projids since 2.15, directories return EXDEV — workaround is change projid first, then `mv`).

### Ex 5 — HSM / copytool basics — *your tape home turf*
**Goal:** Full archive → release → restore cycle with the POSIX copytool and a directory (or S3/file) backend standing in for tape.
Commands: enable HSM + changelog per Manual · `lhsmtool_posix --daemon --hsm-root /archive --bandwidth 0 /mnt/labfs` (flags per Manual) · `lfs hsm_set --exists --archived --archive-id 1 file` via copytool flow · `lfs hsm_archive`, `lfs hsm_state`, `lfs hsm_release`, `lfs hsm_restore` · changelog: `lctl changelog_register`, `lctl changelog_show`
**Success check:** Released file shows the released state, occupies ~no OST space, transparently restores on access, and the changelog shows the HSM events. **Write-up:** map each step to tape vocabulary (archive=recall candidate, copytool=data mover, archive-id≈pool/media set, changelog≈catalogue/journal) — this write-up is interview gold for this candidate.

### Ex 6 — Failover (MDT/OST, LNet)
**Goal:** Understand what failover *requires* (shared/replicated target + `--failnode`) vs what a single-disk VM lab can only simulate.
Commands (at format/tune time): `mkfs.lustre … --failnode=<partner>@tcp0` or `tunefs.lustre --failnode=… /dev/sdX` · `lctl --device <osc> deactivate/activate` · `lfs check servers` during an OSS power-off (VM stop) · LNet: `lnetctl net show`, `lctl ping <nid>`, `lnetctl route show`
**Success check:** With OSS VM stopped, client behaviour matches theory (hang/retry vs error, depending on mount/recovery); on OSS return, recovery completes and `lfs check` is clean. **Honest limit to state:** true HA failover needs shared storage visible to both partners + Pacemaker/Corosync — in this lab you demonstrate *deactivation, failnode config and recovery*, not production HA. Saying so is the correct interview answer.

### Ex 7 — Benchmarking: IOR + mdtest (both filesystems)
**Goal:** Reproducible streaming + metadata numbers on Lustre *and* Scale.
Install (IOR home: https://github.com/hpc/ior — as indexed via https://docs.cloud.google.com/parallelstore/docs/test-performance): `git clone https://github.com/hpc/ior.git && cd ior && ./bootstrap && ./configure && make && sudo make install` (needs MPI: OpenMPI devel packages).
Commands:
```bash
mpirun --oversubscribe -np 4 ior -a POSIX -w -r -e -F -t 1m -b 256m -o /mnt/labfs/ior-test/file   # then same on /ibm/fs1/
mpirun --oversubscribe -np 4 mdtest -a POSIX -d /mnt/labfs/mdtest -n 2000 -u -L -N 1              # then same on /ibm/fs1/
lfs setstripe -c 2 /mnt/labfs/ior-test   # before the Lustre run — layout first, benchmark second
```
**Success check:** Results table in repo with: filesystem, layout/pool, `-np`, transfer/block sizes, write+read BW, mdtest create/stat/remove rates — and a sentence explaining any result where Scale beats Lustre or vice-versa on *this* toy hardware (expect noise; the method, not the winner, is the deliverable).

### Ex 8 — Scale core `mm*` operations
**Goal:** Build by hand what the toolkit automates.
Commands: `mmcrcluster -N <nodes> …` · `mmcrnsd -F nsd.stanza` · `mmstartup -a` · `mmcrfs fs1 -F nsd.stanza -A yes -T /ibm/fs1 …` · `mmadddisk` (add an NSD to a live fs) · `mmchfs` (change an attribute, e.g. suppress atime / exact mtime — see FAQ) · `mmcrfileset` + `mmlinkfileset` · `mmrestripefs` is Ex 10.
**Success check:** `mmlscluster`, `mmlsnsd -L`, `mmlsfs fs1 -T`, `mmdf fs1` all coherent; a fileset appears under the mount with its own quota (`mmsetquota`, `mmlsquota`).

### Ex 9 — Health & troubleshooting (both stacks)
**Goal:** A repeatable health-check you could cron.
Lustre: `lctl get_param version` · `cat /proc/fs/lustre/health_check` (path per release — check Manual) · `lctl dl`, `lctl get_param obdfilter.*.stats` / `mds.*.stats` · `dmesg | grep -i lustre` · offline (unmounted, lab only): Whamcloud `e2fsck` on a target, and `lfsck` namespace/layout LFSCK from the MDT per Manual.
Scale: `mmhealth cluster show` · `mmhealth node show` · `mmlsfs`, `mmdf`, `mmpmon -s cpu,fs_io_s` basics · `mmfsadm dump` awareness (know it exists; don't cargo-cult it).
**Success check:** A single `health.sh` in the repo that prints version, target/node status, capacity, and last errors for whichever filesystem it's run against — and correctly reports RED when you stop a daemon/VM.

### Ex 10 — Data movement / migration
**Goal:** Move data *online* and prove nothing was lost.
Lustre: `lfs migrate -c 1 <file>` (re-layout off a hot/full OST) · directory migration / `lfs migrate -m` for MDT/DNE awareness · add OST2 → migrate → `lfs find --ost` before/after.
Scale: add NSD → `mmrestripefs fs1 -b` (rebalance) · ILM migrate: policy with MIGRATE rule → `mmapplypolicy fs1 -P policy --single-instance -m …` (preview first with the policy test/estimate mode per docs).
**Success check:** Checksums (`sha256sum`) identical before/after; per-target usage (`lfs df` / `mmdf`) visibly rebalances; you can explain migrate-vs-copy (layout/metadata, open-file and hardlink caveats) in both systems.

---

## 5. What Interviewers Ask — 24 questions, grouped

*Basis: current HPC/storage job ads found Oct 2026 — e.g. an HPC Linux & Lustre support role listing MDS/MDT, OSS/OST, LNet, quotas, recovery, performance, Slurm, InfiniBand/RDMA, ZFS, Ansible as required skills (https://www.upwork.com/freelance-jobs/apply/HPC-Linux-Lustre-File-System-Support-Engineer-Maintenance-for-year-Freelancer_~022104468695071214840/); HPC career guidance listing Lustre/GPFS, Linux and distributed-storage architecture as core requirements (https://www.computer.org/resources/hpc-careers); and an HPC Storage Engineer ad requiring deep experience in at least one of Ceph/Lustre/GPFS-Scale/ZFS, Linux internals, storage networking and observability (https://dailyremote.com/remote-job/hpc-storage-engineer-west-coast-5584584). National-lab/university/DDN/IBM ads vary in wording — these questions are the recurring substance, phrased as interviewers phrase them. No verbatim interview transcripts were found; treat this as a well-grounded synthesis, not a leaked question bank.*

**Architecture (1–5)**
1. Draw Lustre: MGS/MDS/OSS/client, MGT/MDT/OST, and what happens on file open (MDS gives layout, client talks direct to OSSs). Where does data *not* flow?
2. Same for Scale: cluster manager, quorum, NSD servers, token management, fileset vs filesystem vs storage pool. How is it *not* just "IBM Lustre"?
3. DNE, PFL, DoM, FLR — what problem does each solve, and what does each cost?
4. LNet: NIDs, networks (`tcp0`, `o2ib0`), routers, multi-rail. How do you debug a client that can't mount (`lctl ping` upwards)?
5. Scale quorum: majority of what? What do tiebreaker disks change, and why is 2-node special? (Also: ESS/CES — what is a protocol node actually doing?)

**Striping / performance tuning (6–10)**
6. A user says "Lustre is slow" for (a) one huge shared file, (b) 1M tiny files, (c) many clients, one file each. Stripe count/size, MDS load, and network diagnosis for each — they're three different problems.
7. When is `-c -1` (stripe over all) the *wrong* answer? What does over-striping cost in metadata, locking and failure blast-radius?
8. IOR vs mdtest: what does each prove, what are the classic ways people accidentally benchmark page cache / a single OST / the wrong layout?
9. OST is 95% full while the filesystem is 60% full — causes (allocator, striping, large files) and fixes (`lfs migrate`, pools, rebalancing). Scale equivalent: NSD/pool imbalance and `mmrestripefs`.
10. InfiniBand/RDMA basics: IPoIB vs native RDMA (`ko2iblnd`), RoCE, multi-rail LNet, and how you'd isolate "network vs OSS disk vs MDS" with evidence.

**Failure / recovery (11–15)**
11. OSS dies mid-write. What do clients see, what does recovery do, what is eviction, and when do you *not* force anything?
12. MDT corruption / `e2fsck` fails: LFSCK types (namespace, layout), backup MDT discipline, and why "restore from backup" is a last resort conversation.
13. Scale node loss: quorum retained vs lost — walk through 3-node cluster losing 1, then 2. What does `mmhealth` tell you first?
14. A disk/NSD fails in Scale vs an OST disk fails in Lustre-on-ldiskfs: where is redundancy actually provided in each (RAID/erasure/replication *below* or *in* the filesystem) — and what did ZFS-backed Lustre change?
15. Split-brain / fencing: why shared-storage Lustre HA needs STONITH/Pacemaker, and what Scale's quorum/CCR gives you instead.

**Day-2 ops (16–20)**
16. Quotas: user vs group vs project (Lustre) vs fileset quotas (Scale). A PI is over quota but `du` disagrees — released HSM files, sparse files, grace — explain it.
17. Monitoring: what do you graph/alert on day one (per-OST/MDT stats, `jobstats`, Scale `mmhealth`/perfmon, LNet health) and what's a vanity metric?
18. Upgrades: rolling Lustre upgrade order and interop (LTS↔feature), kernel pinning discipline; Scale rolling upgrade + why 5.2.3.0/.1's withdrawal is a lesson in checking PSP/flash alerts *before* upgrading.
19. Slurm integration: scratch vs home vs project filesystems, per-job striping defaults, purge policies, jobstats accounting, and what a scheduler-aware admin does about a metadata storm from 500 jobs starting at once.
20. Automation: how you'd Ansible-ise server builds, config drift (`lctl conf_param` / `mmchconfig`), health checks and benchmark baselines — with idempotence and "never auto-`mkfs`" guardrails.

**Tape / HSM crossover — this candidate's edge (21–24)**
21. Explain Lustre HSM end-to-end: coordinator, agent, copytool, archive-id, changelog-driven policy (Robinhood), states (exists/archived/released/dirty). *Pitch:* "This is a tape archive with a disk front-end — the copytool is the data mover, the changelog is the catalogue feed, and I've run the tape equivalent in production."
22. Scale ILM to tape: storage pools, placement vs migration policies, `mmapplypolicy`, external pool / Spectrum Archive (TSM/Storage Protect for Space Management lineage), premigration vs migration. *Pitch:* media lifecycle, recall ordering and drive contention are the same physics as your tape library — most disk-only candidates have never thought about mount/recall storms.
23. HPSS sites: what HPSS is (disk cache + tape, mover/core server model) and how sites pair HPSS with Lustre/Scale scratch — archive is *not* backup, and scratch purge ≠ data loss only if the archive path actually completed. How do you *prove* a file is safely archived before purge?
24. Recall storm scenario: a user restores 2 PB the morning a campaign starts. Throttling, staging order, partial recalls, bandwidth budgeting between archive and scratch — your tape incident experience, translated. This is the question where this candidate should out-score everyone.

**Skills-gap advice (be able to say what you're doing about each):**
- **InfiniBand/RDMA:** cannot be labbed on plain VMs. Mitigate with theory (Ex 6/Week 6 reading, LUG talks), TCP-vs-IB LNet fluency, and honesty: "TCP in lab, IB concepts + `o2ib` config understood, first IB exposure will be supervised." Don't claim IB hands-on.
- **Slurm:** install single-node Slurm on the client VM in Week 8 if time — even a toy `sbatch` writing to scratch with per-job striping closes most of the vocabulary gap.
- **ZFS:** Week 7 stretch OST rebuild (§3.1) + snapshot/send language from your tape/backup background.
- **Monitoring:** Week 7 `health.sh` → extend to Prometheus textfile / simple Grafana if time; jobstats is the HPC-specific piece.
- **Scale depth:** your Scale experience will be weeks deep, Lustre months-equivalent by comparison. Lead applications with Lustre + HSM/ILM; present Scale as "built, benchmarked, documented — early but real".

---

## 6. Honest Gaps / Unsure About

1. **No IBM Storage Scale 5.3.x found.** IBM's own PSP page (Oct 2026 index) lists 5.2.3.x as the 5.2 stream's current line and 6.0.x as the new major. If a job ad says "5.3", ask — it may be an error, an internal/ESS numbering confusion, or a release after this research.
2. **Developer Edition node limit and exact 6.0.1 FAQ/OS matrix not verified.** The editions page states capacity (12 TB), OS family (RHEL x86_64), non-production and no-support — no node cap was stated in sources found. Rocky 9 as a *supported* (vs merely working) host for the 6.0.1 Developer build was not confirmed; IBM Docs direct fetch returned 403 in this session, so the 5.2.3/6.0 doc-set equivalents of the 5.1.9 editions page could not be re-read line-by-line. Verify both on the signup/download page itself (Week 4 task).
3. **Scale multi-node VM sizing is my recommendation, not IBM's.** No IBM-published minimum RAM/disk for a DIY 3-VM Developer cluster was verified; the Vagrant project's own VM sizing lives in its Vagrantfiles, not its README. The §3.2 numbers are conservative practitioner sizing.
4. **LAD25 programme not located.** LAD24 (Paris, Sep 2024) and the LAD event listing on lustre.org were confirmed; a dedicated LAD 2025 agenda/slides page was not found in this research. Use the LUG archives, which are complete.
5. **Lustre 2.15.8-on-Rocky-8.10 step-by-step not verified.** The matrix confirms the combination is tested; the only complete, current, exercised VM guide verified is the Rocky 9.4 + 2.16.1 one. Hence the two-path advice in §3.1.
6. **Interview questions are a synthesis**, grounded in the Oct-2026 job ads cited in §5, not transcripts from named employers. Specific labs/vendors will weight Slurm, security (STIG/clearance-adjacent), or vendor gear differently.
7. **Coursera pricing changes.** "Not free" is based on Coursera's indexed FAQ (purchase / free trial / financial aid) and IBM's subscription announcement — audit options ("full course, no certificate") appear for some Coursera courses and change without notice; check at enrolment, but do not plan the 8 weeks around free Coursera access.
8. **YouTube LUG 2026 set is partial here.** Three talk URLs are given as entry points; the full playlist was not enumerated in this research — search the OpenSFS channel for "LUG 2026".

---

## Sources

All accessed / indexed 11 Oct 2026 unless a publication date is shown. "Verified live" = page opened and read in the research browser; "index" = search-index result read.

**Lustre**
- Lustre Release Information — https://wiki.lustre.org/Lustre_Release_Information — *verified live* (2.15.8 LTS 2025-12-02; 2.17.0 2025-12-29; 2.18.0 in dev)
- Lustre Support Matrix (Whamcloud) — https://wiki.whamcloud.com/display/PUB/Lustre+Support+Matrix?src=contextnavpagetreemode — index
- Lustre Documentation / Manual landing — https://www.lustre.org/documentation/ — index; Manual http://doc.lustre.org/lustre_manual.xhtml · http://doc.lustre.org/lustre_manual.pdf · http://doc.lustre.org/lustre_manual.epub
- Lustre wiki main — https://wiki.lustre.org/index.php?title=Main_Page&diff=cur&oldid=4648 — index
- Build walkthrough RHEL/Rocky 8.10 — https://wiki.whamcloud.com/spaces/PUB/pages/258179277/Walk-thru-+Build+Lustre+MASTER+on+RHEL+Rocky+linux+8.10+from+Git — index
- Lustre HPC Lab (Rocky 9.4, 2.16.1) — https://github.com/pearapat-san/lustre-hpc-lab — *verified live*
- LUG 2019 New User Training — https://wiki.lustre.org/images/4/48/LUG2019-New-User-Class.07.pdf — index
- LUG 2019 Sysadmin Tutorial — http://wiki.lustre.org/images/0/0d/LUG2019-Sysadmin-tutorial.pdf — index
- Lustre Conferences index — https://wiki.lustre.org/index.php?title=Lustre_Conferences&oldid=5187 — index
- LUG 2025 — https://www.opensfs.org/lug-2025/ — index; Past events (LUG26, LAD24) — https://www.opensfs.org/past-events/ — index
- LUG 2026 videos — https://www.youtube.com/watch?v=tuqmP62xoqo · https://www.youtube.com/watch?v=nMTmhT4S7wY · https://www.youtube.com/watch?v=cm95yMEcu1w — index
- Azure Managed Lustre client (kmod vs DKMS) — https://learn.microsoft.com/en-us/azure/azure-managed-lustre/connect-clients — index
- AWS FSx Lustre client install — https://docs.aws.amazon.com/fsx/latest/LustreGuide/install-lustre-client.html — index

**IBM Storage Scale**
- Version recommendations (PSP) — https://www.ibm.com/support/pages/node/707017 — index (5.2.3.8 rec. / 5.2.3.9 latest; 5.2.3.0/.1 withdrawn; CNS 6.0.1.1)
- RHEL 9.4 kernel alert — https://www.ibm.com/support/pages/node/7244835 — index
- Product editions — https://ibm.com/docs/en/storage-scale/5.1.9?topic=overview-storage-scale-product-editions — index (Developer Ed: 12 TB, RHEL x86_64, free, non-prod, no support)
- Developer Edition signup — https://www.ibm.com/account/reg/us-en/signup?formid=urx-41728 — index
- FAQ — https://www.ibm.com/docs/en/storage-scale?topic=STXKQY/pdf/gpfsclustersfaq.pdf — index (90-day trial via sales; quorum)
- Quick Start 5.2.0 — https://www.ibm.com/docs/en/STXKQY_5.2.0/pdf/scale_qsg_520.pdf — index
- Concepts/Planning/Install 5.2.2 — https://www.ibm.com/docs/en/STXKQY_5.2.2/pdf/scale_ins.pdf — index (quorum defaults, toolkit)
- Container Native docs — https://www.ibm.com/docs/en/scalecontainernative/5.2.3 · https://www.ibm.com/docs/en/scalecontainernative/6.0.1 — via IBM GitHub releases, index; CNS 6.0.1 release https://github.com/IBM/ibm-spectrum-scale-container-native/releases/tag/v6.0.1.0 — index
- StorageScaleVagrant — https://github.com/IBM/StorageScaleVagrant — *verified live* (single-node, Developer 6.0.1.0, fs1/5 NSDs)
- Redbook SG24-8602 (2026-07-02) — https://redbooks.ibm.com/abstracts/sg248602.html — index; SG24-8254 — http://www.redbooks.ibm.com/abstracts/sg248254.html?Open — index
- Scale 6.0 / DAT coverage — https://www.blocksandfiles.com/ai-ml/2025/10/20/storage-scale-accelerates-data-for-ai/1615704 — index
- Coursera Scale Administration — https://www.coursera.org/learn/ibm-storage-scale-administration — index; IBM training announcement — https://www.ibm.com/new/training/elevate-your-data-management-skills-with-new-ibm-storage-scale-courses — index
- SSUG stretched-cluster talk — https://www.spectrumscaleug.org/wp-content/uploads/2020/07/SSUGDigital-2-Spectrum-Scale-stretched-cluster-best-practices.pdf — index

**Ansible, benchmarking, jobs**
- IBM Scale Ansible toolkit — https://github.com/IBM/ibm-spectrum-scale-install-infra — index
- NetApp Lustre Ansible collection — https://github.com/netapp/ansible-lustre — index; stale EL7 client role — https://github.com/jabl/ansible-role-lustre_client — index
- IOR — https://github.com/hpc/ior (build/run as shown at https://docs.cloud.google.com/parallelstore/docs/test-performance) — index
- Jobs/careers — https://www.upwork.com/freelance-jobs/apply/HPC-Linux-Lustre-File-System-Support-Engineer-Maintenance-for-year-Freelancer_~022104468695071214840/ · https://www.computer.org/resources/hpc-careers · https://dailyremote.com/remote-job/hpc-storage-engineer-west-coast-5584584 — index
