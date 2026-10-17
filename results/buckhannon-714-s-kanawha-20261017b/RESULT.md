# Fact sheet — 714 S Kanawha St, Buckhannon, WV (listed $125,000)

Read date: 2026-10-17. Public pages and public GIS records only; nobody contacted.

**Summary.** A 3 bed / 2 bath, 1,548 sq ft house built in 1900, listed 2026-10-15 at $125,000 — about $81/sq ft against a town average near $123/sq ft, so the ask sits at the low end of recent in-town sales. The flood question left open by the Oct 17 houses watch is now answered at the address point: **Zone X (area of minimal flood hazard), not in the Special Flood Hazard Area** — but the mapped Zone A floodplain edge is only ~74 m from that point, so the answer is "out, but close," and a parcel-exact check is still owed (county parcel data does not cleanly match this address — see §2). Exact annual taxes could not be retrieved.

## 1. Listing facts

- **Price:** $125,000. (Zillow and Realtor.com, as read by the Oct 17 houses watch, `watch/houses/2026-10-17.md` in this repo.)
- **Beds / baths:** 3 bd / 2 ba (Zillow breaks the baths out as 1 full + 1 partial). (Same source.)
- **Living area:** 1,548 sq ft. **Lot:** 6,098 sq ft (~0.14 acre). **Year built:** 1900. (Same source.)
- **Price per sq ft:** $80.75, vs a Buckhannon average of ~$123/sq ft (Homes.com Buckhannon city guide, https://www.homes.com/local-guide/buckhannon-wv/ — which also gives a $192,000 median sale price for the town).
- **Days on market:** listed 2026-10-15, so ~2 days on market at the 2026-10-17 read date. (Same source.)
- **Heating / cooling:** unsure — not stated in the sources read; the listing pages themselves could not be re-fetched in this run (see How I checked it).
- **Condition notes:** the sources the Oct 17 watch checked carried no fixer / as-is / FSBO / flood-zone mention; the full listing description text was not retrievable in this run, so detailed condition notes are unsure. Interior is unknown; this is a 1900 build.
- **Price history:** unsure — the only event confirmed is the 2026-10-15 listing at $125,000. No earlier list, sale or price-change events could be retrieved from public pages in this run.

## 2. Flood zone and property taxes

### Flood zone — FEMA designation at the address point: **Zone X, AREA OF MINIMAL FLOOD HAZARD (not in the SFHA)**

Determined 2026-10-17 by querying the WV Flood Tool's underlying GIS service (the same FEMA effective-floodplain data the WV Flood Tool at https://mapwv.gov/flood displays), service: https://services.wvgis.wvu.edu/arcgis/rest/services/Hazards/floodTool_publicView/MapServer

- Two independent geocoders place 714 S Kanawha St at **38.97787, -80.22504** (full-address match both times). At that point, the "FEMA Effective Floodplain" layer returns exactly one polygon: **FLD_ZONE = X, ZONE_SUBTY = "AREA OF MINIMAL FLOOD HAZARD", SFHA_TF = F** (DFIRM_ID 54097C, Upshur County). In plain terms: the address point is **outside** the Special Flood Hazard Area, in the lowest-risk mapped category. Flood insurance is not federally mandated for a loan on a structure in Zone X.
- **But it is close.** Distance scans from the same point: no SFHA polygon within 73 m; a **Zone A** polygon (SFHA, 1% annual-chance floodplain, no base flood elevations published) first intersects at **~74 m**. Zone AE and the Zone X "0.2% annual chance" (500-year) polygon enter between 250–300 m, and a Zone AE **floodway** polygon is within 500 m. The Buckhannon River floodplain is roughly a football field from the address point.
- **Parcel-exact check: not completed — county data conflicts with the listing address.** The county parcel polygon that contains the geocoded point is recorded in the state parcel layer (https://services.wvgis.wvu.edu/arcgis/rest/services/Planning_Cadastre/WV_Parcels/MapServer) under a different street number (222 S Kanawha St) and a larger lot (0.30 acre) than the listing's 6,098 sq ft lot, and the county site-address layer contains no "714 S Kanawha St" point at all — its 700-series S Kanawha points (704, 861) sit ~0.8 km north, where the flood picture is cleaner (Zone X at the point, no SFHA within 300 m). Two independent full-address geocodes agree on the southern point used above, so that result governs — but because a lender's flood determination runs off the structure's exact footprint, treat the parcel-exact determination as still open until the WV Flood Tool address/parcel search (or a flood certification) is run against the confirmed parcel.
- Context, not address-specific: the City of Buckhannon's own site describes a Buckhannon River flood cresting at 25.15 ft — the highest since 2016 — with many streets in the southern half of downtown impassable. The address point is in that southern part of town. Local drainage and street flooding are a drive-by question that a FEMA zone alone does not answer.
- The direct FEMA route could not be used: FEMA's NFHL ArcGIS service (hazards.fema.gov) failed to connect in this run by two independent methods, the same failure the Oct 17 check hit. The WV service above republishes FEMA's effective NFHL floodplain data for West Virginia and is the dataset behind the official WV Flood Tool.

### Annual property taxes — unsure (exact figure not retrieved)

The property's actual tax bill could not be pulled in this run: the parcel match is unresolved (see above), and assessor tax detail was not reachable from public pages. Context only: Ownwell's Upshur County page puts Buckhannon's median effective property tax rate at **0.41%** (https://www.ownwell.com/trends/west-virginia/upshur-county/buckhannon). Applied to the $125,000 ask, that rate implies roughly **$510/year** — an estimate from a median rate, **not** this property's tax bill. The real figure depends on the assessed value and should be confirmed with the Upshur County Assessor.

## 3. Recent comparable sales nearby

From Homes.com's Buckhannon recently-sold listings (https://www.homes.com/buckhannon-wv/sold/, read 2026-10-17) — in-town sales, closest in size first:

| Address | Sale date | Price | Size | $/sq ft | Beds/baths | Built |
|---|---|---|---|---|---|---|
| 15 Ritchie St, Buckhannon | Oct 16, 2025 | $145,000 | 1,400 sq ft | $104 | 2 bd / 2 ba | 1910 |
| 31 Reger Ave, Buckhannon | Sep 4, 2025 | $140,000 | 1,450 sq ft | $97 | 3 bd / 1.5 ba | 1958 |
| 102 Randolph St, Buckhannon | Sep 8, 2025 | $129,900 | 1,128 sq ft | $115 | 3 bd / 1.5 ba | 1969 |
| 17 Factory St, Buckhannon | Oct 7, 2025 | $100,000 | 1,300 sq ft | $77 | 3 bd / 1.5 ba | 1997 |
| 224 Pocahontas St, Buckhannon | Oct 23, 2025 | $100,000 | 840 sq ft | $119 | 2 bd / 1 ba | 1940 |

**One-line read:** at $80.75/sq ft the $125,000 ask sits at the low end of these comps ($77–$119/sq ft) and well under the town average — on size and price the ask looks **low-to-fair, not high** — with the caveat that no comp prices in the unknown interior condition of a 1900 build.

## 4. Drive time to the nearest I-79 interchange

The nearest I-79 interchange is **Exit 99 (US-33) at Weston**, reached by heading north through town to Main St / US-33 W. Town-to-town, Buckhannon → Weston is about a 19-minute drive (Trippy route data, https://www.trippy.com/drive/Cleveland-to-Weston-WV); adding the in-town leg from S Kanawha St gives an **estimate of ~20–25 minutes and roughly 15–17 road miles** from the house to the interchange. This is an estimate assembled from the sourced town-to-town leg plus the in-town segment — no routing engine was available in this run to time the door-to-interchange drive directly.

## Sources

- Listing facts: Zillow and Realtor.com listings for 714 S Kanawha St, as read 2026-10-17 and recorded in `watch/houses/2026-10-17.md` (this repo).
- Homes.com — Buckhannon city guide (town $/sq ft average, median sale price): https://www.homes.com/local-guide/buckhannon-wv/
- Homes.com — Buckhannon recently sold: https://www.homes.com/buckhannon-wv/sold/
- WV Flood Tool GIS service (FEMA Effective Floodplain layers), WVU GIS Technical Center: https://services.wvgis.wvu.edu/arcgis/rest/services/Hazards/floodTool_publicView/MapServer — the data behind the official WV Flood Tool, https://mapwv.gov/flood
- WV statewide parcels and site address points, WVU GIS Technical Center: https://services.wvgis.wvu.edu/arcgis/rest/services/Planning_Cadastre/WV_Parcels/MapServer
- Ownwell — Buckhannon (Upshur County) property tax trends: https://www.ownwell.com/trends/west-virginia/upshur-county/buckhannon
- Trippy — Buckhannon → Weston drive leg: https://www.trippy.com/drive/Cleveland-to-Weston-WV
- City of Buckhannon website — mayor's statement on the Buckhannon River flood (crest 25.15 ft), as captured in the Oct 17 check notes.

## How I checked it

Flood: I queried the WV Flood Tool's own GIS service directly — the FEMA Effective Floodplain layer at the geocoded address point, then buffer scans at 10–500 m to find the nearest SFHA polygon and its zone, and repeated the point + buffer queries at the county's northern 700-series address points as a location cross-check. The address point itself was confirmed by two independent geocoders, both returning a full-address match at the same coordinates. The county parcel and site-address layers were queried by point, by radius, and by address text to attempt a parcel-exact match. FEMA's NFHL service was attempted twice more in this run (direct query and page fetch) and failed to connect both times, as it did on Oct 17; the WV service carries the same FEMA effective floodplain data. Listing facts rest on the Oct 17 watch's read of the live Zillow/Realtor.com listings; the listing pages could not be re-fetched in this run, so fields the watch did not capture are marked unsure rather than filled in. Comps were taken from Homes.com's recently-sold page for Buckhannon, choosing in-town house sales nearest the subject's size.

## Unsure about

- **Parcel-exact flood determination.** The address-point result (Zone X, minimal hazard) is solid, but the county parcel recorded at that point carries a different street number and a larger lot than the listing shows, so which parcel the listed house actually sits on — and whether any part of its lot crosses into Zone A (~74 m away) — is unresolved. Confirm with a WV Flood Tool parcel search or a flood certification before treating flood as fully closed.
- **Heating/cooling, listing description and condition notes, and price history** — not retrievable from public pages in this run; only the 2026-10-15 list event at $125,000 is confirmed.
- **Annual property taxes** — exact bill not retrieved; the ~$510/yr figure is a median-rate estimate, not the property's taxes.
- **FIRM panel number and base flood elevation** — the county DFIRM ID (54097C) is known; the individual panel number was not retrieved, and Zone A publishes no base flood elevations. Zone X needs none for the point itself.
- **Comparable-sale freshness** — the most recent sales public pages exposed in this run are dated Sep–Oct 2025; nothing newer could be fetched, so the comp set is the best available rather than the freshest possible.
- **Drive time** — an estimate (~20–25 min) built from a sourced town-to-town leg; not a timed door-to-interchange route.
- **Which location the listing's map pin uses** — two geocoders agree on the southern point, but the county's own address points put 700-series S Kanawha numbers ~0.8 km north (also Zone X, with no SFHA within 300 m). If the house is actually at the northern cluster, flood risk is lower than the headline result; the discrepancy itself is worth one question to the listing agent.
