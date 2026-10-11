# IBM HPSS — Versions 9.3→11.x, Operations Lessons, Reading List

**Summary / method.** The only complete public per-version record found is the HPSS Collaboration's own release-summary pages — short feature lists, not the full customer release notes (older/full documentation is on the customer AdminWiki, per the documentation page). Release dates below are from the Collaboration's Product Releases index, accessed 2026-10-11: 9.3 Jun 2021, 10.1 Jan 2022, 10.2 Jan 2023, 10.3 Sep 2023, 11.1 Aug 2024, 11.2 Feb 2025, 11.3 Sep 2025. Source: https://hpss-collaboration.org/product-releases/ . All summaries below are paraphrases of those pages; where a roadmap slide and the shipped feature list disagree, both are noted.

---

## 1. What changed between HPSS 9.3 and 11.x

### 9.3.0 — baseline (June 2021)
Source: https://hpss-collaboration.org/releases/release-9-3-0/
- Tape/library: grouped Spectra Logic TeraPack moves for faster mount/dismount; deferred tape labelling on import (label on first write instead of at import).
- Performance: new optional fast-positioning mover mode that skips tape section-header verification (off by default); disk-mover / disk-VV I/O metrics, previously internal to the Core Server, exposed via state dump and the `showdiskmaps` tool.
- Operations: a command-line tool to abort I/O jobs, and PFTP clients gained the ability to cancel in-progress parallel transfers.
- Security/auth: the proprietary GAS library was replaced with industry-standard GSS; FTP and HPSS user sets were unified, and `hpssuser` lost its separate `-unix/-krb/-ldap` account options.
- Packaging: RPM RPATH behaviour changed so an installed tree must not be renamed (linking to `/opt/hpss` remains allowed).

### 10.1.0 (January 2022)
Source: https://hpss-collaboration.org/releases/release-10-1-0/
- Monitoring (the big theme): Kibana dashboard templates for server status, Core Server statistics, file/byte counts by class/storage class, tape mounts, transfers by device/mover, and trashcan/migration/purge trends; two new JSON-capable tools, `hpss_server_metrics` and `hpss_db_metrics`; `lscos`/`lsvol` gained JSON output.
- Recall: `lori`, a low-overhead read tool that reads via PIO directly to an output directory instead of staging to the top of the hierarchy, was introduced (the 10.2 page lists it again — see note under 10.2).
- Security/auth: Restricted Access replaced the on/off Restricted User switch, allowing per-operation restrictions (e.g. copy, create, write, stage); users may now belong to 65,535 alternate groups, up from 64.
- Tape: per-device toggle for RAO (Recommended Access Order, default on); repack began emitting media-access INFO logs; file extended attributes began reporting the media type per tape level.
- Misc: `dump_acct_sum -b` bandwidth table; `dumpv_pvl` shows tape label format; `hpssmsg` rewritten in Python (its `-u` argument removed).
- Platform context for this release (RHEL 7/8/9, x86-64 and PPC-64 LE for core/mover/client roles) is tabulated at https://hpss-collaboration.org/hardware-interfaces/rhel-platforms/

### 10.2.0 (January 2023)
Source: https://hpss-collaboration.org/releases/release-10-2-0/
- Migration/purge: a purge-on-migrate bitfile flag — files so marked are purged from disk immediately after migration to tape; settable via the C API, the Python client and `scrub`.
- Tape/library: the SCSI PVR can now discover new library control paths at runtime on a server re-init (vanished in-use paths are marked DOWN rather than removed).
- Diagnostics: optional ASAN-enabled server RPMs for memory-error detection, stated to run roughly 20–30% slower than standard binaries.
- Performance: administrators may disable the mover's Direct I/O to disk; a script was added to create HPSS-compatible volumes in AWS tape storage gateways.
- Note on source quality: this page repeats the `lori` description already listed for 10.1, so vendor summaries should not be treated as strict deltas.

### 10.3.0 (September 2023; 10.3.0 released 30 Sep 2023 per https://hpss-collaboration.org/news/ )
Source: https://hpss-collaboration.org/releases/release-10-3-0/
- **S3 (new):** first HPSS S3 interface, described as providing AWS-S3-like client functionality (documented in the Install Guide). Later site talks call the production form the S3 Proxy — see §2.
- Recall at scale: new Read Queue APIs for submitting very large file-recall lists, implemented by `lori`; read queues are **persisted in Db2**, so the Core Server can resume them after downtime, with a new `rq_cleanup` tool to discard them.
- Operations: most configuration changes (migration/purge policies, storage classes, hierarchies, classes of service) now apply via an "Apply Config" action without restarting the Core Server/MPS; on MPS start, migration/purge now pause first (default 300 s, tunable via an environment variable) and MPS state is preserved across restarts.
- Purge: purge candidates can be filtered/exempted by file size and last-access age in the purge policy; `dumpv_pvl -r` can show the PVR name per volume.

### 11.1.0 (August 2024; released 9 Aug 2024 per https://hpss-collaboration.org/news/ )
Source: https://hpss-collaboration.org/releases/release-11-1-0/
- **Cloud tiering / S3:** a new S3 object-store storage class can be a tier in an HPSS hierarchy, holding low-cost copies in AWS or in a remote HPSS reached via the HPSS S3 Proxy. A BNL roadmap summary describes this as native cloud tiering replacing the AWS tape gateway: https://indico.bnl.gov/event/30275/contributions/115422/attachments/66800/114767/HpssSDCC2025.pdf
- S3 Proxy gained AWS Glacier behaviour including the `restore` API (i.e. tape staging exposed as a Glacier restore).
- Tape selection: tape choice, previously by creation order, can now be script/policy driven with weighting criteria — the feature BNL later illustrated as per-PVR weighted selection (same BNL PDF above).
- Operations/performance: new `hpsslimits` monitoring tool; purge by largest file first; new multi-threaded directory-crawl tool `hpss_recurse`; HPSSFS-FUSE moved into the baseline install.

### 11.2.0 (February 2025; released 13 Feb 2025 per https://hpss-collaboration.org/news/ )
Source: https://hpss-collaboration.org/releases/release-11-2-0/
- Security/auth: the S3 Proxy gained Kerberos authentication; cryptographic strength for UNIX GAS communication was increased.
- Performance: improved per-stream disk write performance in the disk mover and in the mover–client protocol (the BNL roadmap summarises this release as faster per-file performance and stronger authentication — same BNL PDF above).
- Deprecation/format change: HTAR moved from USTAR to PAX format, removing USTAR limits on filename length, file size and UID/GID range.
- Documentation: the Management Guide and Installation Guide were merged into a single HPSS Admin Guide.

### 11.3.0 (September 2025; released 30 Sep 2025, nine features, per https://hpss-collaboration.org/news/ )
Source (verified live 2026-10-11): https://hpss-collaboration.org/releases/release-11-3-0/
- Management: a REST API to SSM (SSM API) for programmatic monitoring/management and automation; a read-only, initially limited web-based SSM dashboard; visibility of pending configuration changes plus a configuration-history tool.
- Performance/scale: stage callback requests are now persisted in metadata and handled like read queuing, allowing far more parallel stage requests and survival across Core Server restarts; the class-of-service change-stream count can be configured up to 256.
- Clients: ARM-architecture client nodes supported, with HSI/HTAR explicitly not yet supported on ARM; the s3proxy client can specify a client stripe width.
- Tape/library maintenance: a PVR can be marked Disabled in SSM for library maintenance — its volumes are treated as DOWN and check-in/import/eject are disabled for it.
- Security/auth: for UNIX authentication, keytabs and passwords were separated in function and implementation (a UNIX keytab shadow file).
- **Roadmap vs shipped discrepancy:** the Dec 2025 BNL roadmap slide (BNL PDF above) summarised 11.3 as also including native in-flight data encryption and containerisation. Neither appears in the official 11.3 feature list above; optional end-to-end/in-flight encryption instead appears in the 12.1 feature list on https://hpss-collaboration.org/product-releases/ . Treat the roadmap items as planned, not shipped in 11.3, on public evidence.

### Cross-cutting answers for 9.3→11.3
- **Tape/drive/library support:** the public summaries contain **no** per-version additions of LTO or TS11xx drive generations. Concrete tape items are only: TeraPack grouping (9.3), RAO toggle (10.1), SCSI-PVR control-path rediscovery (10.2) and PVR Disabled (11.3). Drive-generation activity is visible only in site talks, e.g. NERSC testing TS1160/JE media and deploying TS1170/JF, and adding a fourth TS4500, in 2024 (see §2, HUF 2024), and BNL running LTO-7/8/9 in TS4500 and Oracle SL8500 libraries in 2025 (BNL PDF above).
- **DB2/metadata:** no Db2 version bump is stated in any 9.3–11.3 public summary. Metadata changes that are stated: read queues persisted in Db2 (10.3) and stage callbacks persisted in metadata (11.3). Db2 version support (11.5 and 12.1, with RHEL 9/10) is first stated publicly in the 12.1 list at https://hpss-collaboration.org/product-releases/ .
- **Deprecations / end of support:** no public HPSS end-of-support dates for 9.3–11.x were found (HPSS is sold as an IBM Consulting services offering, not a standard catalogue product — https://hpss-collaboration.org/offerings/ ). Functional replacements that act as deprecations: Restricted User → Restricted Access (10.1), AWS tape gateway → native S3 object-store tiering (11.1, per BNL roadmap), HTAR USTAR → PAX (11.2).

---

## 2. Public talks / papers from HPC centres — operations lessons

All items below were found publicly; takeaways are paraphrases of the linked abstract/article/case study. HUF 2024 items share the proceedings links: contribution list https://indico.kit.edu/event/742/contributions/ and book of abstracts https://indico.kit.edu/event/742/book-of-abstracts.pdf (KIT, 9–12 Sep 2024).

| # | Title / venue | Centre, authors, year | Takeaway |
|---|---|---|---|
| 1 | HPSS Status and Future (SDCC talk) — https://indico.bnl.gov/event/30275/contributions/115422/attachments/66800/114767/HpssSDCC2025.pdf | BNL, Tim Chou / Ognian Novakov / Iris Wu, 2025 | Repack as the migration engine: ~3,900 LTO-6 (ATLAS), ~6,700 LTO-5/6 (PHENIX) and ~8,850 LTO-5 (STAR) tapes repacked to LTO-8 in 2025, explicitly to retire Oracle libraries and save annual service fees. Site still on HPSS 8.3 (567 PB, 16 libraries, 308 drives) and preparing an 8.3→11.x upgrade. |
| 2 | NERSC Site Report, HUF 2024 (abstracts PDF above) | NERSC/LBNL, Owen James, 2024 | A worked upgrade recipe: HPSS 7.4.3→9.3 with new RHEL8 Core Servers, new FS7300 metadata arrays, movers moved to RHEL8 and a PAM auth update. Also candid hardware lesson: difficulty deploying TS1170 drives in an air-cooled room, alongside a 4th TS4500 and REST-over-Ethernet library testing. |
| 3 | Transitioning HPSS Monitoring from Nagios to VictoriaMetrics, HUF 2024 (abstracts PDF above) | NERSC/LBNL, Basil Lalli, 2024 | The closest public HPSS monitoring talk to a Prometheus/Grafana story — but the stack chosen was VictoriaMetrics + Loki + Alertmanager, with third-party and custom exporters, dashboards and alerts. Lesson framed by the author: Nagios-style check monitoring did not scale to their HPSS observability needs. |
| 4 | HPSS S3 Scalability with Rubin LFA S3 Store Use Case, HUF 2024 (abstracts PDF above) | SLAC, Guangwei Che, 2024 | Earliest S3 field report: testing began on the pre-GA interface in July 2023 and was hardened with the developers. Hard problems were scalability, I/O performance and very small files in large, deeply nested structures from the Rubin LFA Ceph S3 store. |
| 5 | Testing HPSS S3 Interface at MPCDF, HUF 2024 (abstracts PDF above) | MPCDF, Elena Summer, 2024 | Test-system evaluation of the 10.3 S3 interface with Ceph Cloud Sync, rclone, presigned URLs and several S3 clients, including retrieving objects from tape. Useful as a checklist of S3 operations to test before production. |
| 6 | Staging ~2 Million Files from Tape for a User, HUF 2024 (abstracts PDF above) | LLNL, Geoff Cleary, 2024 | Mass-recall playbook: a retrieval estimated at ~6 months at the normal rate was attacked with `quaid`, SQLite, RabbitMQ and custom Python across tens of tape volumes. Lesson: bulk staging is a queueing/orchestration problem, not a per-file `hsi` problem. |
| 7 | HPSS Core Servers on Commodity Hardware, or: How We Learned to Love Databases on ZFS, HUF 2024 (abstracts PDF above) | LLNL, Herb Wartens, 2024 | The only public Db2-adjacent operations talk found: putting HPSS Core Servers (and hence their database) on commodity hardware with ZFS underneath for reliability, and testing whether a traditional database performs acceptably on ZFS. No standalone public "Db2 tuning" talk was found (see Gaps). |
| 8 | Have I Right-Sized My Disk Cache?, HUF 2024 (abstracts PDF above) | NERSC/LBL, Francis Dequenne, 2024 | Disk-cache sizing is measurable, not folklore: NERSC built tools to assess an existing cache's effectiveness and model the effect of growing/shrinking it. Pairs with the older NERSC cache-log studies in §3. |
| 9 | Implementing a Virtualized HPSS Deployment for Testing and Development — https://indico.kit.edu/event/742/contributions/17307/ | Indiana University, Forrest Greenwood, 2024 | A disposable HPSS for upgrade testing (built for IU's move to 10.3): VM + mhVTL virtual tape library + Db2 + HPSS, modelled on IBM's training environment. Lesson: rehearse upgrades without consuming scarce bare-metal/tape hardware. |
| 10 | Exploring Storage Technologies for HPSS Disk Caches, HUF 2024 (contribution list above) | KIT (GridKa / BW Data Archive), Andreas Petzold, 2024 | Disk-cache performance limits pushed KIT to benchmark classic SSD storage systems against servers with local NVMe for the HPSS cache tier. (Public record is abstract-level; no slides found.) |
| 11 | Case study: OLCF tape consolidation to Spectra TFinity — https://spectralogic.com/wp-content/uploads/spectralogic-case-study-oak-ridge-leadership-computing-facility.pdf | ORNL/OLCF (admin Gregg Gawinski quoted), undated vendor case study (library installed 2019 per item 12) | The SL8500-era replacement in practice: a 17-frame TFinity ExaScale with 85 IBM TS1155 drives under HPSS consolidated all OLCF data, cut footprint by 85% while holding >150 PB (expandable to 1.52 EB), and migrating data from the old libraries took six months before decommissioning them. |
| 12 | At Oak Ridge, 'End of Life' Sometimes Isn't — https://www.hpcwire.com/2020/10/31/at-oak-ridge-end-of-life-sometimes-isnt/ | ORNL, reported 2020 | The other half of the migration story: OLCF's six retired Oracle StorageTek SL8500 cabinets were not scrapped — they were transferred for reuse, with NOAA contractors dismantling/packing cabinets. Lesson: plan disposition of the old library as part of the migration. |
| 13 | Case study: LANL archive on Spectra TFinity — https://spectralogic.com/wp-content/uploads/spectralogic-case-study-los-alamos-national-laboratory.pdf | LANL, undated vendor case study | Four TFinity libraries across three data centres under HPSS (with IBM Spectrum Protect), relocating an 86 PB archive, mixing LTO-7/LTO-8 and Oracle T10000 drives and repurposing existing Oracle tape media instead of discarding it. |
| 14 | NERSC: Delivering Cost-Effective and Reliable Storage for Primary Data on Tape (ESG case study) — http://www.oracle.com/us/dm/h2fy11/esg-nersc-case-study-202702-362593.pdf?evite=EMEAFM10041984MPP017 | NERSC (Jason Hick), 2010 | The classic repack/reliability evidence: migrating to T9840D/T10000B in 2009–10 meant reading back nearly 24,000 cartridges up to 12 years old; only 13 tapes had any unreadable data (~14 files, <100 GB). NERSC used this to justify keeping a single tape copy for most data, and reported HPSS tape $/GB almost 20× lower than its GPFS disk. |
| 15 | NERSC Tape Archives Make the Move to Berkeley Lab — https://cs-newsarchive.lbl.gov/news/2019/nersc-tape-archives-make-the-move-to-berkeley-lab/ | NERSC/LBNL, 2019 | Library migration driven by the building, not the software: Shyh Wang Hall's variable temperature/humidity ruled out moving the old libraries, so NERSC deployed environmentally self-contained IBM libraries and streamed ~120 PB of archive data over a 400 Gb link, a copy expected to take about two years while balancing user access. |
| 16 | The Living Archive: Inside ECMWF's Exabyte-Scale Meteorological Data Repository — https://WWW.ECMWF.INT/en/about/media-centre/focus/2026/mars-exabyte-scale-meteorological-data | ECMWF, 2026 | MARS and ECFS sit on the same HPSS-managed tape hierarchy. The 2022 Reading→Bologna relocation moved >450 PB of primary data (~700 PB with backups) by dismantling, shipping and reassembling libraries/disks/servers while operational forecasting continued uninterrupted. Scale context: ECMWF passed 1 EB in a single HPSS namespace in March 2024 (https://hpss-collaboration.org/news/ ). |
| 17 | New Data Transfer Tool Developed at ORNL (hsi_xfer) — https://www.olcf.ornl.gov/2024/12/04/new-data-transfer-tool-developed-at-ornl-to-be-made-available-for-public-use/ | ORNL/OLCF, Jake Wynne & Gregg Gawinski, 2024 | Exit-from-HPSS lesson that generalises to any mass recall: with limited tape drives and hundreds of users, ORNL disabled Globus for this flow and built `hsi_xfer` on `hsi` to coordinate the exodus to the 134 PB Kronos nearline system ahead of HPSS decommissioning on 31 Jan 2025, specifically to avoid overloading ageing tape hardware. |
| 18 | Storage Architecture of IU's Media Digitization and Preservation Initiative — http://www.digitalpreservation.gov/meetings/DSA2016/Day1/Wheeler_bdwheele-loc-dsa-20160914.pdf | Indiana University, Brian Wheeler, 2016 | HPSS-based Scholarly Data Archive as preservation storage: tape with large disk caches, data mirrored between Bloomington and Indianapolis, on an IBM TS3500 with TS1150 drives and 3592 JD cartridges, ingesting ~7 PB of digitised audio/video (9 TB/day peak). |
| 19 | Sandia HPSS Site Update, HUF 2022 (OSTI SAND2022-14569C) — https://www.osti.gov/servlets/purl/2005675 | Sandia (SNL), Mike Martinez, 2022 | Listed for completeness as a genuine HUF site update; the PDF could not be retrieved in this session (fetch timed out), so no content takeaway is claimed beyond its title/author/venue as indexed by OSTI. |
| 20 | LLNL hosts HPSS User Forum for 1st time in 33 years — https://www.hpcwire.com/bigdatawire/this-just-in/llnl-hosts-hpss-user-forum-for-1st-time-in-33-years/ | LLNL / HPSS Collaboration, 2025 (HUF 2025) | Context, not a technical talk: HUF 2025 drew 58 participants at LLNL, back-to-back with the IBM Future of Tape Summit and SC25; LLNL participants emphasise that the candid improvement/bug discussions, not the success reports, are the forum's main output. No public HUF 2025 proceedings were found. |

**Topics searched with no credible public item found:** HPSS monitoring specifically with **Prometheus/Grafana** (vendor material only says HPSS tools emit JSON ingestible by tools such as Grafana, and that Kibana templates are shipped — https://hpss-collaboration.org/wp-content/uploads/2023/09/HPSS-Overview-Feb-2026.pdf ); a standalone **Db2/metadata tuning** talk (closest: item 7 above); an **ANL-operated** HPSS talk (Argonne appears only as a *user* of ORNL's HPSS); a **NOAA** HPSS operations talk (NOAA appears only as recipient of ORNL's retired SL8500s, item 12); a public **repack-strategy** paper as such (repack practice is documented in site reports, item 1, and in the release notes in §1, not in a dedicated paper).

---

## 3. Reading list — 10 most useful public resources for deep HPSS engineering knowledge (ranked)

1. **HPSS Product Documentation index** — https://hpss-collaboration.org/product-documentation/ — The entry point to the current Admin Guide (installation, configuration, COS/hierarchies, movers, Db2, troubleshooting), Error Manual, Users Guide, Programmer's Reference and HPSSFS-FUSE Admin Guide. Note it now lists the 12.1 manuals; older-version manuals are customer-only on the AdminWiki.
2. **HPSS 11.3 Programmer's Reference** — https://hpss-collaboration.org/wp-content/uploads/2023/09/hpss_programmers_reference_11_3.pdf — Client API, PIO and related interfaces in full; the document that explains bitfiles, I/O descriptors and how clients actually talk to Core Server/movers.
3. **Watson, "High Performance Storage System Scalability: Architecture, Implementation and Experience," MSST 2005 (UCRL-PROC-208872)** — https://www.osti.gov/servlets/purl/15015911 — The canonical internals paper: network-centred architecture, out-of-band metadata service, Core Server / PVL / PVR / Migration-Purge Server / movers, third-party transfers, and why the metadata engine was rebuilt on a commercial RDBMS (Db2).
4. **HPSS 11.3 User's Guide** — https://hpss-collaboration.org/wp-content/uploads/2023/09/hpss_users_guide_11_3.pdf — Storage concepts an admin must internalise (class of service, storage class, hierarchy, file family) plus every user interface (FTP/PFTP, VFS, utilities).
5. **HUF 2024 Book of Abstracts** — https://indico.kit.edu/event/742/book-of-abstracts.pdf — The most current public operations corpus in one file: S3 field reports, mass staging, Db2-on-ZFS core servers, disk-cache sizing, monitoring migration, virtualised test HPSS.
6. **HPSS RAIT page** — https://hpss-collaboration.org/rait/ — Tape aggregation/redundancy internals: striping with single/double parity (RAID-5/6-like, Reed-Solomon), stripe widths up to 16, when RAIT beats dual-copy on cost (~45% saving at 2+P) and why small files stay on dual-copy.
7. **HPSS Error Manual (10.2 edition)** — https://hpss-collaboration.org/wp-content/uploads/2023/09/hpss_10.2_error_manual.pdf — Troubleshooting by log message, with server source-file references; also the public place where Db2 operational failure modes (agent/connection limits, buffer-pool/memory and paging pathologies) are discussed concretely.
8. **"Extreme Scale HPSS" distributed-metadata poster (PDSW)** — https://pdsw.org/pdsw10/resources/posters/HPSS8.pdf — How metadata scales beyond one server: Db2 Data Partitioning Feature, split namespace/storage-space metadata servers, with prototype create/transaction rates vs the single-metadata-server design. Essential background for any metadata-schema or Db2-partitioning discussion.
9. **Holmes, "Exploration of Cache Behavior Using HPSS Per-File Transfer Logs," LBNL/OSTI, 2001** — https://www.osti.gov/biblio/793764 — Workload-analysis method from 18 months of NERSC production logs: file-size/access-age distributions, write-dominated cache, cache lifetime scaling with cache size and data flow. The companion bandwidth study is at https://escholarship.org/uc/item/1gg3x0pt .
10. **HPSS Tech Topics (LLNL: ZFS ZVOL Settings for HPSS Disk Movers, Sep 2023)** — https://hpss-collaboration.org/tech-topics/ — Short, site-contributed engineering notes; the LLNL piece shows how default ZFS ZVOL settings hurt disk-mover performance and which blocksize/readahead/layout changes fixed it. The Collaboration's channel for exactly this kind of tuning knowledge.

*Runner-up (not counted):* HPSS Overview, Feb 2026 — https://hpss-collaboration.org/wp-content/uploads/2023/09/HPSS-Overview-Feb-2026.pdf — best one-deck orientation to current interfaces (S3 Proxy, Storage Broker, GHI, HPSSFS) and the JSON/Kibana monitoring direction.

---

## Gaps / not publicly documented

- **Full release notes:** only the Collaboration's short public feature summaries (§1) are public. Full release-note documents, defect lists and upgrade procedures were not found publicly; the documentation page states older documentation lives on the customer HPSS Administrator Wiki: https://hpss-collaboration.org/product-documentation/
- **Per-version hardware support:** no public 9.3–11.3 statement of newly supported LTO generations (e.g. LTO-10), TS1170/TS1160 qualification, or Spectra/Oracle library firmware matrices was found; the "Big Picture" supported-hardware page referenced from https://hpss-collaboration.org/offerings/ was not retrievable as a public page in this session.
- **Db2 versions / metadata schema changes per version:** not stated in any public 9.3–11.3 summary (first public Db2 version statement found is for 12.1). No public HPSS metadata schema documentation was found at all.
- **End-of-support dates:** none published publicly for any HPSS version, as far as could be verified; IBM lifecycle searches returned no HPSS entries.
- **11.3 encryption/containerisation:** listed on a Dec 2025 roadmap slide but absent from the official 11.3 feature list — shipped status cannot be verified publicly (see §1).
- **Prometheus/Grafana, Db2 tuning, ANL, NOAA:** searched, no credible public talks found (details at end of §2).
- **HUF proceedings generally:** HUF is a customers-only forum (https://hpss-collaboration.org/services/hpss-user-forum/ ); HUF 2024 (KIT Indico) is the exception with public abstracts. HUF 2025 (LLNL) and HUF 2022 slides other than Sandia's OSTI copy were not found publicly. Most HUF 2024 entries have abstracts only, no slides.
- **Sandia HUF 2022 PDF:** bibliographic record verified via OSTI indexing; full text not retrieved (fetch timed out), so it is listed without a content takeaway.

## Sources
Primary sources are cited inline at every claim above. Key indices: Product Releases https://hpss-collaboration.org/product-releases/ ; News https://hpss-collaboration.org/news/ ; Documentation https://hpss-collaboration.org/product-documentation/ ; HUF 2024 https://indico.kit.edu/event/742/contributions/ . Access mode: web index for most pages; the 11.3 release page and Product Releases index were also verified in a live browser session on 2026-10-11.
