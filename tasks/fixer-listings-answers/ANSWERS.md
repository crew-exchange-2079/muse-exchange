# Answers to the fixer-listings-scan questions

Checked 2026-10-05, public web only. Realtor, Redfin, Zillow and Homes.com refused direct fetches (HTTP 403), so listing facts come from search-index snippets. Nobody was contacted.

## 1. 424 Spring Ave, Clarksburg: price and what is included

**Finding:** $98,500 is most likely the current price. Different portals and snippets show $139,900, $119,900, $104,900 and $98,500. That is a price-cut ladder, not a conflict. $104,900 minus the $6.4K cut Muse saw equals exactly $98,500. The $139,900 figure is probably the original or MLS-feed price.
- Zillow's snippet shows off market (stale or incomplete).
- Parcels and garage apartment: a search summary of Redfin's Clarksburg fixer-upper page describes 424 Spring Ave as including "a 2 bedroom apartment above garage". I could not read the full remarks or see which parcels convey.
- The county-record aggregator shows the house parcel itself at 0.11 acre (taxes about $893/yr, last sale $98,000, parcel 17-03-28-0061.0000). Muse's 0.61 acre is therefore the house plus separate parcels. Their inclusion rests on listing text only.

**Confidence:** price, medium (inference from the cut arithmetic, no single dated page). Parcels/apartment included, low-medium. Zoning/legality of the apartment, could not verify.
Sources: [Redfin](https://www.redfin.com/WV/Clarksburg/424-Spring-Ave-26301/home/117769288), [Zillow](https://www.zillow.com/homedetails/424-Spring-Ave-Clarksburg-WV-26301/22524554_zpid/), [Redfin fixer-upper index](https://www.redfin.com/city/4048/WV/Clarksburg/fixer-upper), [Ownerly parcel data](https://www.ownerly.com/wv/clarksburg/spring-ave-home-details). All read 2026-10-05.

## 2. 515 Center Ave, Weston: July 2026 flood damage

**Finding:** the street was in the flood. The city's recovery notice lists Center Ave among the streets served by National Guard debris pickup. The listing remarks say the house "sustained flood damage from the late July 2026 Weston flooding event," is sold strictly as-is, and some photos predate the flood.
- Town-wide: water marks up to 7 ft on some buildings, higher than 1985. As of 2026-09-02, 30 homes need demolition or are already demolished.
- No source gives water depth for this house or street. I found no inspection, FEMA damage assessment or listing remark saying gut or cleanout.
- Federal flood maps put the point in Zone AE (see 3). Price it as a possible gut job until a contractor says otherwise; ask the Weston floodplain administrator about substantial-damage rules.

**Confidence:** street flooded, high. Depth, gut vs cleanout, could not verify.
Sources: [MetroNews 2026-07-22](https://wvmetronews.com/2026/07/22/flooding-in-weston-its-a-mess/), [MetroNews 2026-09-02](https://wvmetronews.com/2026/09/02/lewis-county-flood-recovery-making-progress-residents-urged-to-meet-with-fema/), [City of Weston recovery page](https://www.cityofwestonwv.gov/2026/07/29/31978/lewis-county-flood-recovery-resource-lists/), [Homes.com listing](https://www.homes.com/property/515-center-ave-weston-wv/b5gc5e9k5tk8g/) (via search summary).

## 3. Flood history and FEMA zones

Method: I geocoded each address with the Census geocoder and queried FEMA's National Flood Hazard Layer (public ArcGIS service) at that point. Geocodes are interpolated along the street, so a lot can be off by tens of meters. A parcel-exact check on the [WV Flood Tool](https://mapwv.gov/flood/) is still required. The tool is an interactive map and could not be read here.

| Address | NFHL at point | Nearby (within 25-75 m) |
|---|---|---|
| 920 E Park Ave, Fairmont | X, minimal hazard | Zone AE within 75 m |
| 38 Kitson St, Weston | X, minimal hazard | AE floodway within 25 m |
| 515 Center Ave, Weston | **AE** | AE floodway within 75 m |
| 424 Spring Ave, Clarksburg | X | all X within 75 m |
| 106 E Main St, Buckhannon | **AE** | 0.2% zone nearby |
| 103 Washington St, Mannington | **AE** | AE floodway within 25 m |
| 194 Anglin Run Rd, Philippi | X | all X within 75 m |

- **920 E Park Ave:** the state's building risk report for 938 E Park Ave (same street) shows Zone AE, floodway, 1.2 ft modeled depth. A Fairmont news summary places East Park Avenue in the Hickman Run watershed, which the June 15, 2025 storm hit. I found no source naming 920 itself as flooded, so footprint membership is unconfirmed. The flood hit hardest on Locust Ave, Hickman Run and Park Drive.
- **38 Kitson St:** the listing says West Fork River frontage with no flood disclosure, and it has a river-side AE floodway within 25 m. Weston flooded in July 2026 (see 2). Treat it as likely affected, not confirmed.

**Confidence:** zone results medium (point geocode). Flood history for 920 E Park, low-medium. Kitson flooding, low.
Sources: [FEMA NFHL service](https://hazards.fema.gov/arcgis/rest/services/public/NFHL/MapServer/28), [WV Risk Explorer, 938 E Park Ave](https://wvfrf.org/wvre/blra/?sortfield=Flood_Depth_Value&sorttype=desc&statement=GIS_Parcel_ID+IN+%2824-05-0003-0129-0001%29), [WBOY search summary](https://www.wboy.com/emergencies/fathers-day-flood-west-virginia-2025/meteorologist-explains-record-rainfall-that-caused-fairmont-flood/), [Kepner Realty, 38 Kitson](https://www.kepnerrealty.com/p/38-Kitson-Street-Weston-WV-26452/dmgid_185587991). Read 2026-10-05.

## 4. 751 Snider St, Morgantown: lease

**Finding:** confirmed as listing text. $180,000, 5 bd / 2.5 ba, 1,910 sq ft, "leased through July 2027" at $1,600/month plus all utilities, as a 4-bedroom (a fifth bedroom could be leased for more). New roof 2024. Listing agent is at Bel-Cross Properties. The listing says it sells as-is after city code-enforcement repair items are completed "over the next 60 days". That is a new flag: ask what the citations were. I did not read the Bel-Cross page or any lease.

**Confidence:** high that the listing says this; medium that the lease is real.
Sources: [Homes.com Morgantown under $200K](https://www.homes.com/morgantown-wv/houses-for-sale/under-200k/), [Redfin investment-property index](https://www.redfin.com/city/14431/WV/Morgantown/amenity/investment+property) (search summaries). Read 2026-10-05.

## 5. Top pick, repair budgets, missed candidates

- **Top pick:** 424 Spring Ave stays first if $98,500 holds. The federal map shows minimal flood hazard, which is a real advantage over four of her top five. At $98,500 all-in is about $146K. Add title/survey checks on the extra parcels.
- **Budgets:** plausible for cosmetic work. Treat Spring Ave's $48K as a floor until a boiler/electrical inspection. Budget 515 Center and 103 Washington at the high end plus flood insurance.
- **Ranking:** 106 E Main, 103 Washington and 515 Center are in AE; 920 E Park is near AE. 194 Anglin Run moves up on risk.
- **Missed candidates:** I found nothing better that I could verify. Portal pages are blocked to my tools. Search snippets showed 1133 Speedway Ave, Fairmont ($149,999, but 1,344 sq ft, under the size floor) and 419 Stealey Ave, Clarksburg ($29,900, 1,792 sq ft, under the price floor and a likely teardown). Neither fits. **Could not verify** a better in-brief listing.

**Confidence:** medium.
Source: [Redfin Fairmont, 1133 Speedway](https://www.redfin.com/WV/Fairmont/1133-Speedway-Ave-26554/home/120536862).
