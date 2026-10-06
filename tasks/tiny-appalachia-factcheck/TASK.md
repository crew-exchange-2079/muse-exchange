# tiny-appalachia-factcheck

Goal: fact-check five short on-screen captions for a public video series of AI-made miniature (tilt-shift) scenes of West Virginia landmarks. Each caption makes a factual claim. Check each against primary or official sources (National Park Service, WV State Parks / wvstateparks.com, WV Department of Tourism, the railroad operator, US Forest Service, the original publisher of any award), not blogs.

| # | Place | Caption |
|---|---|---|
| 1 | Glade Creek Grist Mill, Babcock State Park | "West Virginia's most photographed place — but make it miniature." |
| 2 | Harpers Ferry | "Two rivers, one tiny town, 200 years of history in 6 seconds." |
| 3 | Cass Scenic Railroad | "A 1905 steam locomotive, shrunk. The whistle is real-sized." |
| 4 | Lewisburg | "America's coolest small town, pocket-sized." |
| 5 | Seneca Rocks | "900 feet of stone, now fits in your hand." |

For each caption produce: the factual claim(s) in it, verdict (**correct / roughly right / wrong / unverifiable**), what the official source actually says (short quote), the link, and, if not correct, a corrected caption of similar length and tone. Note things like: is "most photographed" an official claim or a "one of the most" claim; how old Harpers Ferry really is and which two rivers; whether a 1905-built locomotive actually runs at Cass today (which one, built when); who named Lewisburg "coolest small town" and in what year; the official height of Seneca Rocks.

Rules: public sources only, link every claim, say "unsure" rather than guess. End with **How I checked it** and **Unsure about**.

Delivery: push `results/tiny-appalachia-factcheck/RESULT.md` (commit message `result tiny-appalachia-factcheck`, no build leftovers). Then in chat reply with three lines: `RESULT tiny-appalachia-factcheck`, a one-line summary, `END tiny-appalachia-factcheck`.
