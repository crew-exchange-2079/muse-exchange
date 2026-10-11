# Prometheus exporter for LTO tape drives and libraries — public-interface research

Date read: 2026-10-11. Public sources only, no logins. All summaries are in my own words; URLs are given inline for every factual claim. `index` = found via web index / text fetch; the GitHub repos in §4 marked verified were opened directly in the research browser.

## Summary

- No single existing open-source project is a native, vendor-neutral, SCSI LOG SENSE Prometheus exporter for standalone LTO drives. The closest are: a shell/textfile script for IBM libraries (mcmilk), a REST exporter for IBM TS4500 only (SckyzO), smartmontools/`smartctl_exporter` (disk-centric; `smartctl` itself can poll TapeAlert, the exporter README does not document tape), SNMP exporters (library, not drive, data), and Bacula/Bareos TapeAlert scripts (alert text, not metrics).
- Design core: start from LOG SENSE page 0x00 (supported pages) and discover per-drive, because IBM, HPE and Quantum expose different page sets and different vendor pages in 0x30–0x3E. Export TapeAlert 0x2E, error counters 0x02/0x03/0x06, Sequential-Access 0x0C, Temperature 0x0D, Device Statistics 0x14, Volume Statistics 0x17, Informational Exceptions 0x2F, plus vendor Tape Usage 0x30 / Tape Capacity 0x31, and MAM via READ ATTRIBUTE. Never assume a page exists.
- Critical operational fact: reading TapeAlert can clear it for that initiator–target nexus. An exporter polling 0x2E can steal alerts from backup software unless the drive's mode-page control for that behaviour is understood.
- Testing: mhvtl gives real `/dev/st*`, `/dev/sg*` and a changer for integration tests and is what Bareos documents for tape/autochanger work, but its vtltape daemon does not implement the full SSC-3 set, and recent mhvtl work shows capacity/volume pages were placeholders until fixed — so it cannot validate real error counters, wear, temperature or vendor pages. Pair it with recorded `sg_logs --inhex` / JSON fixtures and parser unit tests.

---

## Findings

### 1. SCSI log pages most useful for a tape drive exporter

#### 1.0 Transport and discovery

- LOG SENSE is opcode 0x4D, LOG SELECT 0x4C; `sg_logs` sends LOG SENSE, decodes known pages, and with `--reset/--select` issues LOG SELECT. SPC-4 added log subpages; subpage 0xFF is a wildcard. Source: sg_logs man page (index) https://manpages.debian.org/unstable/sg3-utils/sg_logs.8.en.html
- Always fetch page 0x00 first: it lists supported pages (and, as `0x00,0xff`, supported pages+subpages). The same man page lists pages sg_logs can decode, including 0x02, 0x03, 0x06, 0x0C, 0x0D, 0x0E, 0x2F. Source: https://manpages.debian.org/wheezy/sg3-utils/sg_logs.8.en.html
- `sg_logs` normally does a two-step fetch — a short fetch to learn the length, then a full fetch — and offers `--maxlen`, `--json`, `--inhex=FN` (decode a captured hex file, no device needed), `--page=`, `--paramp=`, `--temperature`, `--vendor=`. Source: https://manpages.opensuse.org/Tumbleweed/sg3_utils/sg_logs.8.en.html
- Linux access paths: drives appear as `/dev/st*`/`/dev/nst*` (st driver) and `/dev/sg*` (sg driver); Quantum's LTO guide summarises that the first drive is `/dev/st0` or `/dev/nst0` (index) http://qsupport.quantum.com/freedownloads/lto4hh/20020140-001.pdf — and `smartctl`'s man page says to use `/dev/nst*` and `/dev/sg*` for SCSI tape drives/changers with TapeAlert (index) https://manpages.opensuse.org/Tumbleweed/smartmontools/smartctl.8.en.html
- MODE SENSE relevant pages: Informational Exceptions Control 0x1C (controls TapeAlert/failure-prediction reporting: DExcpt, Test, LogErr, MRIE, interval timer, report count — IBM's summary is that MRIE=3 reports via Check Condition) http://docs.oracle.com/cd/E21407_01/en/CRCM2529/CRCM2529.pdf ; changer pages in Quantum's Scalar reference — Element Address Assignment 0x1D, Transport Geometry 0x1E, Device Capabilities 0x1F, Disconnect-Reconnect 0x02, plus 0x1C (index) https://qsupport.quantum.com/kb/flare/content/Scalar_i3/downloads/SupDocs/6-00423-17_RevA_SCSI Reference Guide.pdf . Device Configuration / Data Compression pages (SSC 0x10 / 0x0F) are named in the mission; I could not verify their field layouts from a public source I opened — see Could not verify.

#### 1.1 Page-by-page table

Classification key: **Std** = SPC/SSC-defined; **Vendor** = in the vendor range 0x30–0x3E or vendor-defined parameters inside a standard page.

| Page | Name / class | What to export | Notes / sources |
|---|---|---|---|
| 0x00 | Supported log pages — Std | Discovery only; drive the per-drive capability map (labels or `_info`) | sg_logs list, above |
| 0x02 | Write Error Counters — Std (SPC) | Counters: errors corrected without / with delay, total rewrites-or-rereads, total errors corrected, times correction algorithm processed, total bytes processed, total uncorrected errors | Bareos issue reproduces an HP Ultrium-6 `sg_logs -a` dump listing exactly these fields for 0x02 (index) https://github.com/bareos/bareos/issues/2534 ; IBM LTO ref: parameters 0–2 unsupported/zero, most lengths 4 bytes, parameter 0x8000 is 8 bytes, and parameters must be parsed dynamically because presence/order changes (index, summarised) http://docs.oracle.com/cd/E21407_01/en/CRCM2529/CRCM2529.pdf |
| 0x03 | Read Error Counters — Std | Same parameter family as 0x02, read side | Same sources; Microsoft HLK summary lists for 0x03 parameters Total (0x0002), Total Errors Corrected (0x0003), Total Uncorrected (0x0006), likewise for 0x02 (index) https://learn.microsoft.com/en-us/windows-hardware/test/hlk/testref/f4fe41e4-62b2-4c58-b131-8f2e51b0bbe3 |
| 0x06 | Non-Medium Errors — Std | Single non-medium error count (IBM docs) | IBM supported-pages lists include 0x06 for Ultrium (index) http://docs.oracle.com/cd/E21407_01/en/CRCM2529/CRCM2529.pdf |
| 0x0C | Sequential-Access Device — Std (SSC) | Per-mount byte counters: param 0x0000 total channel write bytes, 0x0001 total device write bytes, 0x0002 total device read bytes, 0x0003 total channel read bytes; 0x0100 Cleaning Required (non-zero = cleaning required); IBM adds e.g. 0x8000 MB processed since last cleaning, 0x8001 lifetime load cycles, 0x8002 lifetime cleaning cycles, 0x8003 lifetime power-on seconds | Older IBM SSC summary (index) https://public.dhe.ibm.com/systems/support/system_x_pdf/3570cref.pdf and IBM LTO ref for the 0x8000-series (index) http://docs.oracle.com/cd/E21407_01/en/CRCM2529/CRCM2529.pdf . Reset scope matters: these are *this-mount* counters, so they are not lifetime Prometheus counters — export as gauges per mount or accumulate carefully (see §2) |
| 0x0D | Temperature — Std | Current temperature (param 0x0000), reference temperature (0x0001) → gauge in celsius | HLK summary (index) https://learn.microsoft.com/en-us/windows-hardware/test/hlk/testref/f4fe41e4-62b2-4c58-b131-8f2e51b0bbe3 ; HP and Bareos dumps list 0x0D on LTO drives (below) |
| 0x0E | Start-Stop Cycle Counter — Std | Manufacture date, specified / accumulated start-stop and load-unload cycles → largely drive-lifetime context | HLK summary, same URL |
| 0x14 | Device Statistics — Std (SSC-3/ADC, per sg_logs) | Lifetime media loads, cleaning operations, power-on hours, media-motion (head) hours, metres of tape processed, hours since last cleaning, plus drive serial parameters (0x40/0x41, strings) | sg3_utils issue discussing `sg_logs --page=0x14` output and a fix to print serial parameters as strings (index) https://github.com/doug-gilbert/sg3_utils/issues/45 ; a field summary in an Unraid tape plugin doc (index) https://github.com/und3f1ned/unraid-tape-library/blob/HEAD/CLAUDE.md . Note: 0x14 with subpages is reused for other device types (e.g. zoned block in Seagate's manual) — key decoding on peripheral device type |
| 0x17 | Volume Statistics — Std (SSC, replaces legacy 0x30) | Per-volume/per-partition: volume identifier/barcode, mounts, recovered/unrecovered read & write errors, datasets written/read, MB written/read lifetime and previous load, total native capacity, total used native capacity, beginning/middle tape-pass wear counts | mhvtl issue quotes IBM LTO-7 text saying Tape Usage 0x30 is replaced by the standard Volume Statistics 0x17 (index) https://github.com/markh794/mhvtl/issues/52 ; Unraid plugin field summary (index) https://github.com/und3f1ned/unraid-tape-library/blob/HEAD/CLAUDE.md ; mhvtl PR confirms 0x17 carries total native / total used native capacity fields (index) https://github.com/markh794/mhvtl/pull/186 . Vendor divergence inside the standard page: the same mhvtl issue notes HP and IBM generate different (both legal) partition records for 0x17 — parsers must walk parameter lengths, never assume fixed layout |
| 0x2E | TapeAlert — Std (SSC for drives, SMC for changers) | 64 one-byte flags, parameters 1–64 (0x01–0x40); see §1.2 | IBM: page length/format and parameter codes 1–64 (index) https://www.ibm.com/docs/en/dtl/2.9.4?topic=x4d-log-page-x2e-tapealert |
| 0x2F | Informational Exceptions — Std | Failure-prediction / exception status; sg_logs decodes it | sg_logs decoded-page list https://manpages.debian.org/wheezy/sg3-utils/sg_logs.8.en.html . Pair with MODE SENSE 0x1C above. I did not find a tape-specific parameter breakdown in a public source opened — see Could not verify |
| 0x30 | Tape Usage — Vendor (IBM/HP LTO) | Non-volatile volume usage (legacy; superseded by 0x17 on newer IBM generations) | IBM supported lists + mhvtl issue quote, above |
| 0x31 | Tape Capacity — Vendor (IBM/HP LTO) | Per-partition remaining capacity and maximum capacity (MiB) | HP LTO-4 supported list (index, summarised in §1.3) and mhvtl PR #186 https://github.com/markh794/mhvtl/pull/186 |
| 0x32 / 0x1B | Data Compression — Vendor 0x32 on IBM/HP LTO-5-era lists; standardised Data Compression is 0x1B in newer sg_logs naming | Compression counters/ratio inputs | Bareos HP dump lists both 0x1B Data compression and 0x32 Data compression (lto-5) on one drive (index) https://github.com/bareos/bareos/issues/2534 — expect aliasing/duplication across generations |
| 0x33, 0x34, 0x38, 0x39, 0x3B, 0x3C, 0x3D | HP/IBM vendor: Device Wellness (HP 0x33), Performance (HP 0x34), Write Errors / Read Forward Errors (IBM 0x33/0x34 — note the collision with HP meanings), Blocks/Bytes Transferred 0x38, Host Port interface errors 0x39/0x3B, vendor-specific 0x3C (IBM drive-usage counters incl. time since last cleaning in minutes, cumulative power-on minutes, cumulative cleaning count), Subsystem Errors 0x3D | Optional, behind vendor+product detection | IBM and HP supported-page lists (index) http://docs.oracle.com/cd/E21407_01/en/CRCM2529/CRCM2529.pdf and HP LTO-4 manual below; IBM GA32-0928-02 drive-usage 0x3C parameters (index) https://dn721800.ca.archive.org/0/items/SCSISpecificationDocumentsSCSIDocuments/Vendor%20SCSI%20documents/IBM/IBM%20TotalStorage%20LTO%20Ultrium%20Tape%20Drive%20SCSI%20Reference%20%28GA32-0928-02%29.pdf . **Key lesson: page numbers in 0x30–0x3E do not mean the same thing across vendors — decode only after INQUIRY vendor/product match** |
| 0x11, 0x12, 0x13, 0x15, 0x16, 0x18, 0x3E | HP LTO extras: DTD Status 0x11, TapeAlert Response 0x12, Requested Recovery 0x13, Service Buffers 0x15, Tape Diagnostic Data 0x16, Protocol-Specific Port 0x18, Device Status 0x3E | Mostly diagnostic; 0x12/0x13 are TapeAlert-adjacent | HP LTO-4 supported list, below |

#### 1.2 TapeAlert 0x2E — all 64 flags, severity, and the clearing trap

Facts that frame the table:

- IBM describes TapeAlert as up to 64 flags read via LOG SENSE page 0x2E, some mandatory and some optional, presented in decimal, and cleared at power-on reset (index, summarised) https://www.ibm.com/docs/en/3592-rackmount?topic=STPRH6/com.ibm.storage.drives.doc/tapealert.html
- IBM's library doc gives the on-wire format: page length 0x0140, parameter code = flag number 1–64, one-byte value, 0 = not set, 1 = set (index) https://www.ibm.com/docs/en/dtl/2.9.4?topic=x4d-log-page-x2e-tapealert
- IBM's LTO reference adds: unsupported parameters are always 0, parameters are 1 byte, and — critically — all log parameters are set to 0 when the log is read, and also at power-on/reset/LOG SELECT; the PC field is ignored and current values are always returned (index, summarised) http://docs.oracle.com/cd/E21407_01/en/CRCM2529/CRCM2529.pdf
- smartmontools' man page makes the same point operationally and per I_T nexus, notes it can be controlled by a bit in the SSC Device Configuration Extension mode page, and says modern smartctl only fetches TapeAlert on `--health` given twice or `--log=tapealert` precisely because clearing broke other tools (index) https://manpages.opensuse.org/Tumbleweed/smartmontools/smartctl.8.en.html
- Severity vocabulary: a T10 SMC-3 proposal summarises three severities — Information (log/inform operator), Warning (continued operation may cause failure), Critical (failure has occurred or is imminent, corrective action required) — plus response classes such as intervention-required and call-service in that proposal's table (index) https://www.t10.org/ftp/t10/document.06/06-420r2.pdf
- Drive flags and changer flags are different namespaces: that same SMC proposal defines 64 TapeAlert flags for a media changer device and notes other standards (e.g. SSC-3) may define other flags (index) https://www.t10.org/ftp/t10/document.06/06-420r2.pdf . Do not reuse the drive table for a changer LUN, or vice versa. Quantum's Scalar library reference likewise lists only Supported Log Page 0x00 and TapeAlert 0x2E for the changer (index) https://qsupport.quantum.com/kb/flare/content/Scalar_i3/downloads/SupDocs/6-00423-17_RevA_SCSI Reference Guide.pdf

Drive flag table below is my condensation (flag name + severity letter only) of the T10 SSC-3 TapeAlert proposal T10/05-154r4 (index) https://www.t10.org/ftp/t10/document.05/05-154r4.pdf , cross-checked against IBM's supported-flags page (index) https://www.ibm.com/docs/en/ts4300-tape-library?topic=flags-tapealert-supported-by-drive . C = Critical, W = Warning, I = Information/Informational. Where IBM/T10 revisions disagree on a severity (observed for e.g. flags 0x0F, 0x10, 0x11), the exporter should ship the severity as data with a source/revision note, not hard-code one true table.

| # (hex) | Flag | Sev | # (hex) | Flag | Sev |
|---|---|---|---|---|---|
| 1 (01) | Read warning | W | 33 (21) | Eject media | C |
| 2 (02) | Write warning | W | 34 (22) | Download fail | W |
| 3 (03) | Hard error | W | 35 (23) | Drive humidity | W |
| 4 (04) | Media | C | 36 (24) | Drive temperature | W |
| 5 (05) | Read failure | C | 37 (25) | Drive voltage | W |
| 6 (06) | Write failure | C | 38 (26) | Predictive failure | C |
| 7 (07) | Media life | W | 39 (27) | Diagnostics required | W |
| 8 (08) | Not data grade | W | 40–46 (28–2E) | Obsolete | — |
| 9 (09) | Write protect | C | 47–49 (2F–31) | Reserved | — |
| 10 (0A) | No removal | I | 50 (32) | Lost statistics | W |
| 11 (0B) | Cleaning media | I | 51 (33) | Tape directory invalid at unload | W |
| 12 (0C) | Unsupported format | I | 52 (34) | Tape system area write failure | C |
| 13 (0D) | Recoverable mechanical cartridge failure | C | 53 (35) | Tape system area read failure | C |
| 14 (0E) | Unrecoverable mechanical cartridge failure | C | 54 (36) | No start of data | C |
| 15 (0F) | Memory chip in cartridge failure | W* | 55 (37) | Loading failure | C |
| 16 (10) | Forced eject | C* | 56 (38) | Unrecoverable unload failure | C |
| 17 (11) | Read-only format | W* | 57 (39) | Automation interface failure | C |
| 18 (12) | Tape directory corrupted on load | W | 58 (3A) | Firmware failure | W |
| 19 (13) | Nearing media life | I | 59 (3B) | WORM medium — integrity check failed | W |
| 20 (14) | Clean now | C | 60 (3C) | WORM medium — overwrite attempted | W |
| 21 (15) | Clean periodic | W | 61–64 (3D–40) | Reserved | — |
| 22 (16) | Expired cleaning media | C | | | |
| 23 (17) | Invalid cleaning tape | C | | | |
| 24 (18) | Retension requested | W | | | |
| 25 (19) | Dual-port interface error | W | | | |
| 26 (1A) | Cooling fan failure | W | | | |
| 27 (1B) | Power supply failure | W | | | |
| 28 (1C) | Power consumption | W | | | |
| 29 (1D) | Drive maintenance | W | | | |
| 30 (1E) | Hardware A | C | | | |
| 31 (1F) | Hardware B | C | | | |
| 32 (20) | Interface | W | | | |

\* Severity differs in some delineation/vendor tables I saw in the index; treat as revision-dependent. Cleaning cluster is flags 20–23 (0x14–0x17) plus 0x0B; cleaning state is also available non-destructively from 0x0C param 0x0100 and from 0x14/0x3C hours/counts since cleaning — prefer those for gauges and reserve 0x2E for alerting.

Exporter implication of clearing: either (a) be the *only* TapeAlert consumer on that nexus and document it, (b) read 0x2E on a slower cadence and immediately surface/clear deliberately, or (c) check/set the mode-page control smartmontools mentions. Backup software (Bacula/Bareos, NetBackup) also polls TapeAlert — co-existence must be a documented design decision, not an accident.

#### 1.3 Vendor differences — supported-page lists are the ground truth

- **IBM Ultrium (LTO-2/3 and LTO-4 lists in the IBM SCSI Reference):** 0x00, 0x02, 0x03, 0x06, 0x0C, 0x18, 0x2E, 0x30 Tape Usage, 0x31 Tape Capacity, 0x32 Data Compression, 0x33 Write Errors, 0x34 Read Forward Errors, 0x38 Blocks/Bytes Transferred, 0x39/0x3B Host Port Interface Errors, 0x3C vendor-specific, 0x3D Subsystem Errors; LTO-4 adds 0x37 Performance Characteristics (index, summarised) http://docs.oracle.com/cd/E21407_01/en/CRCM2529/CRCM2529.pdf . Full text: GA32-0450-07 (index) https://dn721800.ca.archive.org/0/items/SCSISpecificationDocumentsSCSIDocuments/Vendor%20SCSI%20documents/IBM/IBM%20TotalStorage%20LTO%20Ultrium%20Tape%20Drive%20SCSI%20Reference%20%28GA32-0450-07%29.pdf and the newer GA32-0928-02 (index) https://dn721800.ca.archive.org/0/items/SCSISpecificationDocumentsSCSIDocuments/Vendor%20SCSI%20documents/IBM/IBM%20TotalStorage%20LTO%20Ultrium%20Tape%20Drive%20SCSI%20Reference%20%28GA32-0928-02%29.pdf
- **HPE (HP LTO-4 host interface guide):** 0x00, 0x02, 0x03, 0x0C, 0x0D Temperature, 0x11 DTD Status, 0x12 TapeAlert Response, 0x13 Requested Recovery, 0x18 (FC/SAS only), 0x2E, 0x30 Tape Usage, 0x31 Tape Capacity, 0x32 Data Compression, 0x33 Device Wellness, 0x34 Performance, 0x3E Device Status (may be absent in some firmware) (index, summarised) https://dn721800.ca.archive.org/0/items/SCSISpecificationDocumentsSCSIDocuments/Vendor%20SCSI%20documents/HP/HP%20LTO%204%20Ultrium%20tape%20drives%20technical%20reference%20manual%20host%20interface%20guide.pdf . HP LTO-5 guide documents Device Statistics-style lifetime parameters including lifetime media loads (0x0000), lifetime cleaning operations (0x0001), lifetime power-on hours (0x0002), lifetime head hours (0x0003), lifetime metres processed (0x0004), and head hours since last / 2nd-last / 3rd-last successful cleaning (0x0008–0x000A) (index, summarised) https://dn721800.ca.archive.org/0/items/SCSISpecificationDocumentsSCSIDocuments/Vendor%20SCSI%20documents/HP/HP%20LTO%205%20Ultrium%20tape%20drives%20technical%20refererence%20host%20interface%20guide.pdf
- **Real HP Ultrium-6 dump (via Bareos issue):** 0x00, 0x02, 0x03, 0x0C, 0x0D, 0x11, 0x12, 0x13, 0x14 Device Statistics, 0x15, 0x16, 0x17 Volume Statistics, 0x18, 0x1B Data Compression, 0x2E, and legacy-suffixed 0x30/0x31/0x32/0x34/0x35/0x3E — i.e. a modern HP drive exposes the *standard* 0x14 and 0x17 that the older HP list above does not name (index) https://github.com/bareos/bareos/issues/2534
- **Quantum:** I found a public Quantum *library* (Scalar) SCSI reference (changer pages above) and Quantum LTO user guides, but **no public Quantum standalone-drive SCSI reference with a log-page table** — see Could not verify. LTFS's supported-drive table lists Quantum LTO-5–LTO-9 half-height drives as supported targets, which at least confirms Quantum drives are in scope for open tools (index) https://github.com/LinearTapeFileSystem/ltfs

#### 1.4 MAM / READ ATTRIBUTE (`sg_read_attr`)

- READ ATTRIBUTE is mostly defined in SPC, only tape systems seem to implement it, and much of its data overlaps LOG SENSE and INQUIRY VPD — so treat MAM as a complement, not a replacement (index, summarised) https://www.mywebuniversity.com/man2pdf/Ubuntu2604/sg_read_attr.8.pdf
- Attribute-value service action returns, in the man page's worked example: remaining capacity in partition [MiB], maximum capacity in partition [MiB], TapeAlert flags, load count, MAM space remaining [B], assigning organization, format density code, etc. Other service actions list attribute lists and partition lists; output can be captured to hex and decoded later with `--inhex`-style input (index, summarised) https://www.mywebuniversity.com/man2pdf/Ubuntu2604/sg_read_attr.8.pdf
- Units trap (confirmed in mhvtl code history): MAM attributes 0x0000/0x0001 are specified by SSC in megabytes, not bytes (index) https://github.com/markh794/mhvtl/pull/186 — an exporter must convert MiB→bytes for Prometheus base units and must not copy a buggy implementation's units.
- Useful MAM exports: `remaining_capacity_bytes` and `maximum_capacity_bytes` per partition (gauge), `load_count_total` (counter), barcode/volume serial and medium type via the standard MAM attribute set (as `_info` labels — exact attribute IDs beyond 0x0000/0x0001 and the volume-lock example 0x1623 seen in LTFS/mhvtl discussions were not verified from a primary SPC text I opened; see Could not verify).

#### 1.5 Cleaning and drive statistics — synthesis

Export as first-class metrics, not only as TapeAlert bits: lifetime loads, lifetime cleanings, power-on time, head/motion hours, metres processed, time/minutes since last cleaning, cumulative cleaning count. Sources: 0x14 summary https://github.com/und3f1ned/unraid-tape-library/blob/HEAD/CLAUDE.md , HP LTO-5 lifetime parameters https://dn721800.ca.archive.org/0/items/SCSISpecificationDocumentsSCSIDocuments/Vendor%20SCSI%20documents/HP/HP%20LTO%205%20Ultrium%20tape%20drives%20technical%20refererence%20host%20interface%20guide.pdf , IBM 0x3C counters https://dn721800.ca.archive.org/0/items/SCSISpecificationDocumentsSCSIDocuments/Vendor%20SCSI%20documents/IBM/IBM%20TotalStorage%20LTO%20Ultrium%20Tape%20Drive%20SCSI%20Reference%20%28GA32-0928-02%29.pdf , IBM 0x0C vendor params http://docs.oracle.com/cd/E21407_01/en/CRCM2529/CRCM2529.pdf . Convert hours/minutes to seconds for Prometheus (§2).

---

### 2. Prometheus metric naming and exposition best practices

#### 2.1 Official rules (Prometheus docs, opened directly)

Source: https://prometheus.io/docs/practices/naming/

- Metric names should carry a single-word application prefix / namespace (e.g. the exporter's or domain's name).
- A metric must refer to a single unit and a single quantity; do not mix units.
- Use base units — seconds, bytes, metres, celsius — not milliseconds, megabytes or kilometres.
- Suffix with the unit in plural form; an accumulating count takes `_total` in addition to the unit if any. The docs' own examples include a unit-less accumulating count ending in `_total`, an accumulating count with unit ending in `_seconds_total`, and a `_build_info` pseudo-metric for metadata about the running binary.
- A metric should represent the same logical thing across all label dimensions, so that `sum()`/`avg()` across dimensions is meaningful; otherwise split it.
- Labels differentiate characteristics of the thing measured; do not put label names in the metric name; every unique label combination is a new series, so avoid high-cardinality / unbounded label values.
- Base-unit table: time = seconds, temperature = celsius, bytes = bytes (use bytes even where bits are customary), percent = ratio 0–1 with `ratio` suffix or the `A_per_B` pattern.

#### 2.2 Writing-exporters guidance (Prometheus docs repo)

Source: https://github.com/prometheus/docs/blob/HEAD/docs/instrumenting/writing_exporters.md

- Failed scrapes: two accepted patterns — return HTTP 5xx, or expose a `<exporter>_up` gauge (0/1) — the latter is better when partial metrics are still useful, the former is simpler and makes Prometheus's own `up` behave normally, at the cost of not distinguishing exporter-down from target-down (summarised from the docs text returned in search).
- Also in that guidance (same source): prefer raw counters over pre-computed deltas/rates and let PromQL `rate()` do the work; for push-style sources consider expiry of stale series. Design consequence for tape: export the drive's cumulative counters raw; do **not** export drive-computed rates or ratios except as clearly-labelled gauges where no raw pair exists.

#### 2.3 Analogues and their naming

- **smartctl_exporter** (prometheus-community, verified live on GitHub): it exports smartctl statistics to Prometheus, requires smartmontools ≥ 7.0 because JSON output arrived in 7.0, polls on `--smartctl.interval` (default 60s) with periodic rescan, serves on :9633, and explicitly does not fix up data — if smartctl's JSON is wrong/missing, that is an upstream issue (verified) https://github.com/prometheus-community/smartctl_exporter . Its metric family is `smartctl_device_*` with a `device` label — e.g. from a downstream summary: `smartctl_device_temperature{temperature_type="current"}`, `smartctl_device_smart_status`, `smartctl_device_bytes_read`/`_bytes_written`, `smartctl_device_power_on_seconds`, and an info-style `smartctl_device` carrying model/serial/firmware (index) https://github.com/bleenq-technology/ai-homelab/blob/HEAD/docker/monitoring/smartctl-exporter/README.md . Note two deviations to *not* copy: several of those names lack `_total` on counters and use 0–100 percent instead of ratio.
  - **Tape support:** `smartctl` itself polls TapeAlert from SCSI tape drives/changers and has tape log options such as `--log=tapedevstat` https://manpages.opensuse.org/Tumbleweed/smartmontools/smartctl.8.en.html , but I found **no tape mention in smartctl_exporter's README/EXAMPLE material I opened** — treat tape support in the exporter as *not verified / likely incidental via smartctl JSON*, not a feature. Its `--smartctl.fake-data` mode (run the exporter from saved JSON files in a `debug/` directory) is, however, an excellent testing pattern to copy — see §3.
- **node_exporter:** the pattern mcmilk's exporter (below) piggy-backs on — a textfile collector directory whose `.prom` files are included in the scrape; the general textfile pattern requires atomic write-then-rename so a scrape never sees a partial file (index, general pattern) https://github.com/eugene-eeo/nano-exporter2 . node_exporter metric names use the `node_` prefix with base units, e.g. `node_network_mtu_bytes`, `node_boot_time_seconds`, `node_context_switches_total` (index, same source). A native exporter is preferable to textfile for a long-lived SCSI poller (error handling, `up`, scrape duration), but textfile is a legitimate v0.
- **snmp_exporter:** maps SNMP index instances to Prometheus labels and combines related OIDs into one labelled series; it is a multi-target *proxy* exporter driven by a generated `snmp.yml` from MIBs via its generator (verified live) https://github.com/prometheus/snmp_exporter . Lesson for tape libraries: index→label mapping (slot, drive, element address) is exactly the changer model too; and generated config from a machine-readable definition (MIB ↔ log-page definition table) beats hand-written per-model code.

#### 2.4 Proposed naming scheme for the new exporter (design recommendation, not a sourced fact)

Prefix `tape_` (or `lto_` — pick one single-word namespace and keep it). Labels: `device` (`/dev/sgN` or stable by-id/by-path), `serial`, `vendor`, `model`, `library` / `changer`, `slot`, `barcode` (bounded: cartridges in one library; still the highest-cardinality label — consider putting barcode only on volume metrics), `partition`.

| Metric | Type | Source |
|---|---|---|
| `tape_drive_info{vendor,model,serial,firmware,device,...}` = 1 | info gauge | INQUIRY / VPD 0x80/0x83 |
| `tape_library_info{...}` / `tape_changer_element_info{type,address,barcode,drive}` | info gauge | SMC READ ELEMENT STATUS / mtx-equivalent |
| `tape_exporter_up{device}` , `tape_scrape_duration_seconds`, `tape_scrape_errors_total` | gauge / gauge / counter | exporter itself (§2.2 pattern) |
| `tape_alert{flag="20",name="clean_now",severity="critical",device}` = 0/1, emit all known flags every scrape | gauge | 0x2E (see clearing warning §1.2) |
| `tape_write_errors_corrected_total`, `tape_write_errors_uncorrected_total`, `tape_write_bytes_processed_total` (and `read_` twins) | counters | 0x02 / 0x03 |
| `tape_mount_bytes_written_total`… — **do not** name per-mount 0x0C values `_total` across mounts; either export `tape_loaded_bytes_written` gauge scoped by a `mount`/`barcode` label set that resets on load, or accumulate in-exporter into a true counter and document reset behaviour | gauge/counter | 0x0C |
| `tape_temperature_celsius` | gauge | 0x0D param 0 (and `..._reference_celsius`) |
| `tape_drive_loads_total`, `tape_drive_cleanings_total`, `tape_drive_power_on_seconds_total`, `tape_drive_head_seconds_total`, `tape_drive_tape_meters_total` (metres is the base unit; name it `_meters_total` — Prometheus spelling is American `meters` in the base-unit table) | counters | 0x14 / HP lifetime page / IBM 0x3C (convert h/min→s) |
| `tape_drive_seconds_since_cleaning` (gauge), `tape_cleaning_required` (0/1 gauge) | gauge | 0x0C 0x0100, 0x14/0x3C |
| `tape_volume_info{barcode,serial,manufacturer,medium_type,worm,write_protected}` | info gauge | 0x17 / MAM |
| `tape_volume_mounts_total`, `tape_volume_read_errors_recovered_total`, `tape_volume_write_errors_uncorrected_total`, etc. | counters (per barcode) | 0x17 |
| `tape_volume_capacity_bytes`, `tape_volume_remaining_capacity_bytes` per partition | gauges | 0x17 totals / 0x31 / MAM (convert MiB→bytes, §1.4) |
| `tape_volume_load_total` (MAM load count) | counter | READ ATTRIBUTE |
| `tape_informational_exception{...}` / failure-prediction gauge | gauge | 0x2F + MODE SENSE 0x1C state |

Rules applied: counters only for truly monotonic lifetime values; ratios 0–1 (`tape_volume_used_ratio`, not percent); no rate/ratio pre-computation where raw counters exist; HELP/TYPE on every family; omit unsupported pages entirely rather than exporting 0 (a 0 error counter from a drive that has the page is data; absence of the page is not).

---

### 3. Testing without real hardware using mhvtl

#### 3.1 What mhvtl is and how it installs

- mhvtl is a Linux Virtual Tape Library: a kernel module (mhvtl, described in its README as a pseudo-HBA derived in spirit from scsi_debug, with a char-device back end) passing SCSI commands to user-space daemons that emulate the library and drives (verified live) https://github.com/markh794/mhvtl
- Daemons: `vtltape` emulates a tape drive for a queue ID taken from `device.conf`, media files are created with `mktape`, and the man page itself warns it does not implement the complete SCSI SSC-3 command set (index) https://manpages.opensuse.org/Tumbleweed/mhvtl/vtltape.1.en.html ; `vtllibrary` is the changer daemon configured by `library_contents`.
- `library_contents.<id>`: one section per element — Drive, Picker, MAP (import/export), Slot — slots carry an optional barcode (1–12 ASCII chars); an undefined barcode means an empty slot; drive serial numbers are set in `device.conf`, not here; vtllibrary must be restarted to pick up changes (index) https://manpages.opensuse.org/Tumbleweed/mhvtl/library_contents.5.en.html
- Install flow (Bareos developer FAQ, index): clone https://github.com/markh794/mhvtl.git , build/install the kernel module first (`cd kernel && make && sudo make install`), then build/install the user tools (`make && sudo make install`), then enable/start the mhvtl services; some distributions (e.g. openSUSE) package it https://github.com/end-9214/bareos/blob/HEAD/docs/manuals/source/DeveloperGuide/developerFAQ.rst . That file is in a fork mirror in the index; the same steps match mhvtl's own INSTALL/docker material.
- mhvtl's own Docker README shows the modern flow: install the kernel module on the host (`make kernel`), bring the container up, generate config with `etc/generate_device_conf` and `etc/generate_library_contents`, `systemctl start mhvtl.target`, and verify with `lsscsi -g` — devices defined in `device.conf` should appear, and should disappear after stopping the target (index) https://github.com/markh794/mhvtl/blob/HEAD/docker/README.md
- `device.conf` content: generated stanzas define a library (e.g. IBM 3584) and drives by personality — the generator/issues show forms like `add_ibm_ultrium_5_drive` / `_6_` / `_7_` / `_8_` with index, channel, target, LUN, serial, library and slot (index) https://github.com/markh794/mhvtl/issues/99 ; HP personalities also exist — an issue configures an HP MSL8096 with Ultrium 8-SCSI drives (index) https://github.com/markh794/mhvtl/issues/146

#### 3.2 What it presents

From a Bareos workshop deck reproducing `lsscsi -g` and `mtx status` against mhvtl (index) https://www.slideshare.net/NETWAYS/open-source-backup-conference-2014-workshop-bareos-introduction-by-philipp-storz :

- A changer appears as `mediumx STK L700` on `/dev/sch0` with an sg node (`/dev/sg2` in that example), and a drive as `tape IBM ULT3580-TD5` on `/dev/st0` with its own sg node (`/dev/sg1`).
- `mtx -f <changer> status` works against it and reports Data Transfer Elements and Storage Elements with `VolumeTag=E01001L5`-style barcodes, plus import/export slots — i.e. the full SMC surface an exporter needs for changer inventory.
- The same mhvtl shape appears in a Bacula tooling issue: STK L700 and L80 changers with IBM ULT3580-TD5/TD4 and STK T10000B drives, each with `/dev/st*` + `/dev/sg*` pairs (index) https://github.com/waa/bacula-resource-auto-creator/issues/1

So: yes — `sg_inq`, `sg_logs`, `mtx`, `mt`, tar and backup suites all see ordinary devices. That is the point of the kernel-module design.

#### 3.3 Does LOG SENSE / TapeAlert work against mhvtl? Limitations

Supported, with sharp edges — this is the most important section for test design:

1. **Incomplete SSC-3.** vtltape's own man page says so (above). Expect missing/partial commands and pages versus any real drive.
2. **Capacity and volume pages were placeholders until recently.** An mhvtl PR (2026, index) describes the Tape Capacity page 0x31 and Volume Statistics 0x17 returning a constant sentinel for every capacity field, the 0x31 updater never being called from LOG SENSE, placeholder byte-order bugs, and MAM capacity attributes holding bytes where SSC specifies megabytes — all fixed in that PR https://github.com/markh794/mhvtl/pull/186 . Pin a known mhvtl version in CI and assert exact values; older versions will silently give plausible-looking garbage.
3. **0x17 is genuinely hard.** An older mhvtl issue discussion notes Volume Statistics has subpages/history records, partition records whose size depends on partition count, and different-but-legal HP vs IBM partition records; the same thread quotes IBM LTO-7 documentation that 0x30 was replaced by 0x17 (index) https://github.com/markh794/mhvtl/issues/52 . A parser that passes mhvtl may still fail on real HP or IBM layouts, and vice versa.
4. **No real wear/errors.** By construction a VTL has no medium errors, head wear, temperature or cleaning physics. I found no public source documenting mhvtl injecting TapeAlert flags or non-zero error counters; a *different* (Rust) VTL project's issue explicitly describes its 0x02/0x03/0x06/0x0C/0x14/0x17/0x1B/0x30–0x32 pages as all-zero stubs and calls zero error counters truthful for a VTL (index) https://github.com/metebalci/thur/issues/61 — do not cite that as mhvtl behaviour, but the principle applies: mhvtl cannot validate alert/error paths. Treat any mhvtl TapeAlert claim as *not verified* (see Could not verify).
5. **Emulated-device quirks leak into tools.** A sg3_utils issue shows `sg_logs --page=0x14` against an emulated device returning malformed serial-number strings, with the reporter owning the emulator bug (index) https://github.com/doug-gilbert/sg3_utils/issues/45 — parsers must be defensive about non-printable/short vendor strings.
6. **Personalities matter.** Default libraries have changed over time (e.g. mhvtl's ChangeLog notes default library drives moving from LTO-4/5 to LTO-6/LTO-8, initial LTO-9 emulation, and a VHF log page implementation) (index) https://raw.githubusercontent.com/markh794/mhvtl/master/ChangeLog — record the exact personality (IBM 3584/ULT3580-TDn, HP MSL/Ultrium, STK L700) in every fixture.

#### 3.4 How backup suites use it

- Bareos's developer FAQ section on testing tape/autochanger changes says, in summary, that they use mhvtl to simulate tape and autochanger devices, and gives the install flow in §3.1 (index) https://github.com/end-9214/bareos/blob/HEAD/docs/manuals/source/DeveloperGuide/developerFAQ.rst
- Bareos conference material credits mhvtl with making tape and changer regression tests possible in its nightly/CDash-style regression runs on VMs (index) https://github.com/bareos/OpenSourceBackupConference/raw/refs/heads/main/2013/osbconf2013-en-PhilippStorz-Bareos_Features.pdf
- I did **not** find a public GitHub Actions workflow in Bacula or Bareos that boots mhvtl in hosted CI (a kernel module generally cannot load in hosted runners) — the documented pattern is self-hosted VMs/appliances. Flagged in Could not verify.

#### 3.5 Alternatives and supplements

| Technique | What it gives you | Source / note |
|---|---|---|
| Record/replay `sg_logs` fixtures | `sg_logs --inhex=FN` decodes a captured hex response with no device; `sg_logs --json` gives machine-readable output to snapshot. Record once per real drive model, replay in unit tests forever | sg_logs synopsis (index) https://manpages.opensuse.org/Tumbleweed/sg3_utils/sg_logs.8.en.html |
| Record/replay the *tool's* JSON (smartctl_exporter pattern) | Its `--smartctl.fake-data` mode runs the whole exporter from saved JSON files named per device — copy this pattern: an exporter flag/env that reads a directory of captured `sg_logs --json` / raw hex per device | smartctl_exporter README (verified) https://github.com/prometheus-community/smartctl_exporter |
| `sg_raw` crafted commands/responses | `sg_raw` sends an arbitrary CDB to a device (man page examples include INQUIRY) — useful to probe a real or virtual drive for a specific page/subpage and capture the response that becomes a fixture; it does not by itself mock a device | sg_raw man page (index) https://manpages.debian.org/experimental/sg3-utils/sg_raw.8.en.html |
| Parser-level unit tests + golden files (Go) | Feed raw LOG SENSE byte strings (valid, truncated, unknown parameter codes, HP-vs-IBM 0x17 layouts, non-printable serials) directly to the decoder; assert metrics with the Prometheus test utilities. This is where most exporter bugs live | Design recommendation; motivated by the variable-layout evidence in §1.1/§3.3 |
| LD_PRELOAD / ioctl mocking | Interpose `open`/`ioctl(SG_IO)` in the exporter process and serve fixture responses. **No public tape-exporter example found** — flagged as unverified; prefer an internal `Transport` interface in Go (device layer behind an interface, fake in tests) over LD_PRELOAD, which is fragile and C-oriented | Could not verify — see below |
| tcmu-runner / LIO TCMU | A userspace SCSI target framework: tcmu-runner handles the TCMU backstore's UIO/netlink/D-Bus plumbing and exposes a C handler API for SCSI commands — a possible base for a *programmable* fake drive that can inject TapeAlert flags and error counters, which mhvtl cannot | tcmu-runner README mirror (index) https://github.com/seanpm2001/markh794_tcmu-runner — note this is a mirror/fork in the index; the upstream project is open-iscsi/tcmu-runner, which I did not open directly |
| Other VTLs | QUADStor VTL (open-source edition on GitHub) is an alternative library emulator (index) https://github.com/allfs/quadstorvtl ; the Rust thur/QuantumVTL-style projects surfaced in search are immature and their log pages are stubs (above) | Use only as a second changer-personality test, not for log-page truth |
| Dummy coverage in Go | Build the exporter with a fake collector that emits every metric family with representative label sets, so dashboards/alerts and `promtool`-style linting can be CI-tested with zero SCSI layer involved | Design recommendation (no source claimed) |

Recommended test pyramid: (1) golden-fixture parser tests for every page × vendor, (2) fake-data full-exporter tests, (3) mhvtl integration job on a self-hosted runner asserting discovery, changer inventory, load/unload and *known-version* 0x14/0x17/0x31 values, (4) one real drive of each vendor in a hardware lab for TapeAlert/error/cleaning paths.

---

### 4. Existing open-source projects — verified on GitHub

| Project | What it does | What it does NOT do (gap vs a native SCSI Prometheus exporter) |
|---|---|---|
| **mcmilk/prometheus-tapedrv-exporter** https://github.com/mcmilk/prometheus-tapedrv-exporter (verified live: 1 commit, created 2025-09-18, shell script + systemd unit) | Small shell script gathering metrics from tape drives inside libraries such as IBM TS4500; supports Ultrium 3–9 / ULT3580-TD3–TD9; exports basic health/status; designed to integrate with node_exporter's textfile mechanism; preview via `tapedrv-exporter-daemon getinfo` | Not a native exporter daemon (no own HTTP server/scrape semantics of its own), basic health/status only per its README — no documented full log-page decoding (error counters, volume statistics, MAM, temperature), IBM-library-centric, single initial commit |
| **SckyzO/tapelibrary_exporter** https://github.com/SckyzO/tapelibrary_exporter (verified live: Go, GPL-3.0, 42 commits, created 2026-08-04 per GitHub metadata) | Prometheus exporter for IBM TS4500 only, over the library's RoE REST API (`https://<library>/web/api/v1` → `/metrics` on :9170); 18 collectors (library, frames, accessors, drives, power, node cards, I/O stations, FC ports, logical libraries, cleaning/data/diagnostic cartridges, slots, events, lifetime reports); per-collector `tapelibrary_exporter_collector_success` / `_duration_seconds`; multi-instance and multi-target (`/probe`) builds; alerting rules + Grafana dashboard in `monitoring/` | No SCSI at all: no LOG SENSE, no TapeAlert page decoding, no standalone drives, no non-IBM libraries, nothing for drives behind a generic HBA. Drive data is only what the TS4500 REST API exposes. (Note the very recent creation date in the metadata — evaluate maturity accordingly.) |
| **benmcclelland/tapealert** https://github.com/benmcclelland/tapealert (verified live: Go, MIT, 2 commits, created 2018-01-06) | Go library to decode TapeAlert flags; code-generated tables (`tapealert.csv.go`, `standalone.csv.go`), a `tadecode` helper and a test file | Library only — no SCSI transport, no exporter, no metrics. Useful as a flag-table reference/import candidate; unmaintained appearance (2 commits) means vendor the table with attribution and re-verify severities (§1.2) |
| **waa/bacula-tapealert** https://github.com/waa/bacula-tapealert/blob/HEAD/README.md (index) | Drop-in Python replacement for Bacula's `tapealert` script: its raison d'être is that Bacula SD's `ControlDevice` can point at the wrong sg node, so it auto-determines the current correct sg node for the drive (from the `ArchiveDevice` by-id path) on the fly, with logging/test options | Bacula-specific alert plumbing, not metrics; no Prometheus exposition, no log pages beyond TapeAlert via tapeinfo. Its sg-node-drift problem is a real design lesson: an exporter must resolve drives by stable identity (by-id / serial), never by `/dev/sgN` numbering |
| **Bacula built-in `tapealert`** (scripts/) | Bacula ships a `tapealert` script installed by its scripts Makefile alongside `mtx-changer` (index) https://gitlab.bacula.org/bacula-community-edition/bacula-community/-/blob/Branch-15.0/bacula/scripts/Makefile.in?ref_type=heads ; typical SD configuration is `AlertCommand = "sh -c 'tapeinfo -f %c \| grep TapeAlert'"` with a `ControlDevice` (index) https://github.com/waa/bacula-tapealert/blob/HEAD/README.md | Event/alert text at job end only; no continuous metrics, no counters/gauges, grep-level parsing |
| **Bareos TapeAlert** | Bareos added initial TapeAlert support in its storage daemon (per its changelog summary in the index) and its docs/issues show `sg_logs -a` as the diagnostic workflow for drive/media data (index) https://github.com/bareos/bareos/issues/2534 | Same shape as Bacula: job-time alerting/diagnostics, not a Prometheus exporter; no published metric schema |
| **Zabbix templates** | Community template collections include SNMP tape-library templates (e.g. Dell PowerVault TL2000, Oracle/Sun SL150/SL3000 in the community repo listing) (index) https://github.com/zz-forks/zabbix__community-templates ; for IBM TS4300 a forum thread reports no predefined template, with a user generating one from the MIB with mib2zabbix and polling via SNMP (index) https://www.zabbix.com/forum/zabbix-help/452575-ibm-ts4300-tape-library | Zabbix, not Prometheus; SNMP/library-level only; I found **no dedicated LTO-drive/TapeAlert Zabbix template** in a public source — see Could not verify |
| **Prometheus snmp_exporter + library MIBs** https://github.com/prometheus/snmp_exporter (verified live) | Recommended way to expose SNMP data to Prometheus; generator builds `snmp.yml` from MIBs; vendor/community MIBs live in the prometheus-community/snmp collection it points to; multi-target proxy model on :9116 | Library management-plane data only (whatever the library's SNMP agent/MIB exposes — typically status, slots, sometimes drive presence), no per-drive SCSI log pages, no TapeAlert flag fidelity, no standalone drives. Complementary to, not a substitute for, a SCSI exporter |
| **smartctl_exporter** https://github.com/prometheus-community/smartctl_exporter (verified live) | See §2.3: polls smartctl JSON for ATA/SATA/SCSI disks and NVMe, `smartctl_device_*` metrics, fake-data test mode | Disk/NVMe-centric; tape not documented in its README (despite smartctl itself supporting TapeAlert polling, §2.3). No changer, no MAM, no volume statistics. Best used as the architectural analogue, not as the tape solution |
| **sg3_utils itself** (`sg_logs`, `sg_read_attr`, `sg_inq`, `sg_raw`, `sg_modes`) | Complete, maintained low-level access + decoding for LOG SENSE, MAM, INQUIRY, MODE SENSE, with JSON and inhex modes (man pages cited throughout §1/§3) | CLI tools, not an exporter: no HTTP exposition, no label model, no scrape semantics. An exporter can either link the knowledge (re-implement decoding) or shell out to `sg_logs --json` (simpler, inherits sg3_utils' vendor quirks coverage — the smartctl_exporter pattern) |
| **mtx** | Controls single/multi-drive SCSI media changers (tape changers, autoloaders, libraries) over the sg device, per the SMC spec; `status` gives drives/slots/barcodes, plus load/unload etc. (index) https://manpages.ubuntu.com/manpages/focal/en/man1/mtx.1.html ; upstream is SourceForge (http://mtx.sourceforge.net per its man page) | A control tool, not monitoring: no metrics, and its primary use (moving media) is a side effect an exporter must never trigger — an exporter should implement READ ELEMENT STATUS read-only itself or parse `mtx status` only. Its status output format is, however, the de-facto changer inventory shape to mirror |
| **stenc** https://github.com/scsitape/stenc/blob/HEAD/README.md (index) | SCSI tape encryption manager: hardware encryption on/off, AES, key descriptors, key-change audit logging; Linux/FreeBSD; SSP-compliant drives such as LTO-4+ | Encryption administration only; no health metrics. Relevant only if the exporter later surfaces encryption status (stenc shows what status fields drives expose) |
| **LTFS** (reference implementation) https://github.com/LinearTapeFileSystem/ltfs (index) | Reference implementation of the SNIA LTFS format spec: mounts an LTFS tape as a filesystem; supported-drives table covers IBM LTO-5–9/TS11xx, HP LTO-5–9, Quantum LTO-5–9 (half-height) | A filesystem, not monitoring. Its drive-backend code is a useful public reference for per-vendor SCSI quirks (mode pages, MAM attributes, partitioning) when writing an exporter |
| **smartmontools (`smartctl`/`smartd`)** | Polls TapeAlert from tape drives/changers, tape device-statistics log, etc. (§2.3) https://manpages.opensuse.org/Tumbleweed/smartmontools/smartctl.8.en.html | Not Prometheus-native (that is smartctl_exporter's job, which is disk-focused); TapeAlert clearing interaction (§1.2) originated here |

**Net gap:** changer inventory (SMC READ ELEMENT STATUS), drive log pages (SSC/SPC), MAM, TapeAlert with correct clearing semantics, and Prometheus-native exposition in one vendor-neutral daemon — that combination does not exist in the projects above.

---

## Could not verify

- **Quantum standalone LTO drive SCSI Reference with log-page tables:** only Quantum library (Scalar) SCSI reference and LTO user guides were found publicly; no drive-level Quantum log-page list could be verified. Do not assume Quantum follows the IBM or HP 0x30–0x3E assignments.
- **Tape Capacity page code numbering in the mission (0x17 vs 0x31):** the mission calls 0x17 "Tape Log / Volume Statistics" — public sources consistently call 0x17 *Volume Statistics* (standard, SSC) and *Tape Capacity* is 0x31 on IBM/HP lists. No public source found for a "Tape Log" page at 0x17 under that name.
- **Informational Exceptions log page 0x2F parameter breakdown for tape:** sg_logs decodes 0x2F and MODE SENSE 0x1C is documented, but no tape-specific 0x2F parameter table was found in a public source opened.
- **MODE SENSE Device Configuration (0x10) / Data Compression (0x0F) field layouts for LTO:** not verified from a public source opened in this session (the IBM/HPE PDFs contain them, but I did not extract those sections via the index).
- **Full MAM attribute ID list** (barcode, medium serial, etc. beyond capacity 0x0000/0x0001, load count, and TapeAlert in the sg_read_attr example): the sg_read_attr man page example names the attributes but the complete SPC attribute-ID table was not opened from a primary public source.
- **mhvtl TapeAlert behaviour:** no public source found stating whether mhvtl's vtltape sets/returns meaningful 0x2E flags, or nonzero 0x02/0x03 counters. Assume it does not for test-planning purposes, but this is an absence of evidence, not a verified negative.
- **Bacula/Bareos hosted-CI mhvtl workflows:** documented mhvtl use is developer/self-hosted VM regression testing; no public GitHub Actions workflow booting mhvtl was found.
- **LD_PRELOAD / SG_IO ioctl mocking for tape exporters, and Go "dummy coverage" exporters:** no public worked example found; both are presented in §3.5 as design options, not sourced practice.
- **smartctl_exporter tape support:** not documented in its README as opened; whether smartctl's tape JSON flows through usefully is untested/unverified here.
- **A dedicated Zabbix LTO/TapeAlert template:** only generic SNMP library templates and a user-generated TS4300 MIB template were found.
- **T10 SSC/SPC texts themselves:** T10 draft/proposal PDFs on t10.org were used for TapeAlert; the final published SSC/SPC standards are paywalled/not public, so parameter-level claims rely on IBM/HPE implementations and sg3_utils/smartmontools man pages, which occasionally disagree (flagged where seen, §1.2).
- SckyzO/tapelibrary_exporter GitHub metadata shows a 2026-08-04 creation date and 0 stars as read on 2026-10-11 — treat adoption claims accordingly; mcmilk's exporter shows a single commit.

## Sources

Primary / official:
- Prometheus metric & label naming — https://prometheus.io/docs/practices/naming/
- Prometheus writing-exporters docs — https://github.com/prometheus/docs/blob/HEAD/docs/instrumenting/writing_exporters.md
- IBM TapeAlert log page 0x2E format — https://www.ibm.com/docs/en/dtl/2.9.4?topic=x4d-log-page-x2e-tapealert
- IBM TapeAlert error reporting — https://www.ibm.com/docs/en/3592-rackmount?topic=STPRH6/com.ibm.storage.drives.doc/tapealert.html
- IBM TapeAlert flags supported by the drive — https://www.ibm.com/docs/en/ts4300-tape-library?topic=flags-tapealert-supported-by-drive
- IBM LTO Ultrium SCSI Reference GA32-0450-07 — https://dn721800.ca.archive.org/0/items/SCSISpecificationDocumentsSCSIDocuments/Vendor%20SCSI%20documents/IBM/IBM%20TotalStorage%20LTO%20Ultrium%20Tape%20Drive%20SCSI%20Reference%20%28GA32-0450-07%29.pdf
- IBM LTO SCSI Reference GA32-0928-02 — https://dn721800.ca.archive.org/0/items/SCSISpecificationDocumentsSCSIDocuments/Vendor%20SCSI%20documents/IBM/IBM%20TotalStorage%20LTO%20Ultrium%20Tape%20Drive%20SCSI%20Reference%20%28GA32-0928-02%29.pdf
- IBM LTO SCSI Reference (Oracle-hosted copy) — http://docs.oracle.com/cd/E21407_01/en/CRCM2529/CRCM2529.pdf
- HP LTO-4 host interface guide — https://dn721800.ca.archive.org/0/items/SCSISpecificationDocumentsSCSIDocuments/Vendor%20SCSI%20documents/HP/HP%20LTO%204%20Ultrium%20tape%20drives%20technical%20reference%20manual%20host%20interface%20guide.pdf
- HP LTO-5 host interface guide — https://dn721800.ca.archive.org/0/items/SCSISpecificationDocumentsSCSIDocuments/Vendor%20SCSI%20documents/HP/HP%20LTO%205%20Ultrium%20tape%20drives%20technical%20refererence%20host%20interface%20guide.pdf
- Quantum Scalar SCSI Reference Guide — https://qsupport.quantum.com/kb/flare/content/Scalar_i3/downloads/SupDocs/6-00423-17_RevA_SCSI Reference Guide.pdf
- T10 SSC-3 TapeAlert proposal 05-154r4 — https://www.t10.org/ftp/t10/document.05/05-154r4.pdf
- T10 SMC-3 TapeAlert proposal 06-420r2 — https://www.t10.org/ftp/t10/document.06/06-420r2.pdf

Tools / man pages:
- sg_logs (Debian unstable) — https://manpages.debian.org/unstable/sg3-utils/sg_logs.8.en.html ; (openSUSE) https://manpages.opensuse.org/Tumbleweed/sg3_utils/sg_logs.8.en.html ; (wheezy, decoded-page list) https://manpages.debian.org/wheezy/sg3-utils/sg_logs.8.en.html
- sg_read_attr — https://www.mywebuniversity.com/man2pdf/Ubuntu2604/sg_read_attr.8.pdf
- sg_raw — https://manpages.debian.org/experimental/sg3-utils/sg_raw.8.en.html
- smartctl (openSUSE) — https://manpages.opensuse.org/Tumbleweed/smartmontools/smartctl.8.en.html
- mtx (Ubuntu) — https://manpages.ubuntu.com/manpages/focal/en/man1/mtx.1.html
- vtltape / library_contents (openSUSE mhvtl) — https://manpages.opensuse.org/Tumbleweed/mhvtl/vtltape.1.en.html ; https://manpages.opensuse.org/Tumbleweed/mhvtl/library_contents.5.en.html

Projects and issues (all read 2026-10-11):
- https://github.com/markh794/mhvtl ; https://github.com/markh794/mhvtl/blob/HEAD/docker/README.md ; https://github.com/markh794/mhvtl/pull/186 ; https://github.com/markh794/mhvtl/issues/52 ; https://github.com/markh794/mhvtl/issues/99 ; https://github.com/markh794/mhvtl/issues/146 ; https://raw.githubusercontent.com/markh794/mhvtl/master/ChangeLog
- https://github.com/mcmilk/prometheus-tapedrv-exporter ; https://github.com/SckyzO/tapelibrary_exporter ; https://github.com/benmcclelland/tapealert ; https://github.com/prometheus-community/smartctl_exporter ; https://github.com/prometheus/snmp_exporter
- https://github.com/waa/bacula-tapealert/blob/HEAD/README.md ; https://gitlab.bacula.org/bacula-community-edition/bacula-community/-/blob/Branch-15.0/bacula/scripts/Makefile.in?ref_type=heads ; https://github.com/bareos/bareos/issues/2534 ; https://github.com/end-9214/bareos/blob/HEAD/docs/manuals/source/DeveloperGuide/developerFAQ.rst
- https://github.com/doug-gilbert/sg3_utils/issues/45 ; https://github.com/scsitape/stenc/blob/HEAD/README.md ; https://github.com/LinearTapeFileSystem/ltfs ; https://github.com/und3f1ned/unraid-tape-library/blob/HEAD/CLAUDE.md ; https://github.com/metebalci/thur/issues/61

---

## Appendix A — Verified GitHub metadata (GitHub API, checked 2026-10-11)

Language, licence (as reported by the GitHub API SPDX field) and last-commit date for the GitHub projects cited above. "NOASSERTION / None" means the API could not detect a licence file — it does not mean the project is unlicensed in its own terms.

| Repo | Language | Licence (API) | Last commit |
|---|---|---|---|
| [mcmilk/prometheus-tapedrv-exporter](https://github.com/mcmilk/prometheus-tapedrv-exporter) | Shell | NOASSERTION | 2025-09-19 |
| [SckyzO/tapelibrary_exporter](https://github.com/SckyzO/tapelibrary_exporter) | Go | GPL-3.0 | 2026-08-06 (repo pushed 2026-09-14) |
| [benmcclelland/tapealert](https://github.com/benmcclelland/tapealert) | Go | MIT | 2018-01-06 |
| [waa/bacula-tapealert](https://github.com/waa/bacula-tapealert) | Python | BSD-2-Clause | 2024-08-09 |
| [FunctionSir/ltouwrap](https://github.com/FunctionSir/ltouwrap) | Go | MPL-2.0 | 2025-08-24 |
| [SeeleVolleri/tapelogs](https://github.com/SeeleVolleri/tapelogs) | C | GPL-3.0 | 2026-03-03 |
| [prometheus-community/smartctl_exporter](https://github.com/prometheus-community/smartctl_exporter) | Go | Apache-2.0 | 2026-10-10 |
| [prometheus/snmp_exporter](https://github.com/prometheus/snmp_exporter) | Go | Apache-2.0 | 2026-10-10 |
| [prometheus/node_exporter](https://github.com/prometheus/node_exporter) | Go | Apache-2.0 | 2026-10-10 |
| [LinearTapeFileSystem/ltfs](https://github.com/LinearTapeFileSystem/ltfs) | C | BSD-3-Clause | 2026-09-23 |
| [scsitape/stenc](https://github.com/scsitape/stenc) | C++ | GPL-2.0 | 2025-07-23 |
| [doug-gilbert/sg3_utils](https://github.com/doug-gilbert/sg3_utils) | C | NOASSERTION | 2026-09-22 |
| [bareos/bareos](https://github.com/bareos/bareos) | C++ | NOASSERTION | 2026-10-09 |
| [markh794/mhvtl](https://github.com/markh794/mhvtl) | C | NOASSERTION | 2026-09-30 |
| [yottatsa/tapeutils](https://github.com/yottatsa/tapeutils) | Python | None | 2022-04-09 |

## How I checked it

- Existing projects were found and verified two ways: GitHub API repository search and per-repo metadata/commit lookups (2026-10-11, dates in Appendix A), and direct reading of the key repos' pages/READMEs during the research pass.
- SCSI log-page, TapeAlert, MAM and vendor claims are cited inline to T10 documents, IBM/HPE SCSI references, and sg3_utils/smartmontools man pages in Sections 1–2; Prometheus naming claims are cited to prometheus.io and the prometheus/docs repo in Section 2; mhvtl claims are cited to the mhvtl repo, its man pages and Bareos developer docs in Section 3.
- Anything that could not be verified from a public source is listed explicitly under "Could not verify" above — notably Quantum standalone-drive log pages, mhvtl TapeAlert behaviour, and hosted-CI mhvtl workflows.

## Unsure about

- See "Could not verify" at the end of the main report. In addition: GitHub API licence detection returns NOASSERTION for several mature projects (sg3_utils, Bareos, mhvtl, mcmilk exporter) — check each repo's COPYING/LICENCE file before reusing code.
- SckyzO/tapelibrary_exporter is very new (created 2026-08-04 per GitHub metadata) and its last-commit and last-push dates differ; treat its maturity accordingly.
