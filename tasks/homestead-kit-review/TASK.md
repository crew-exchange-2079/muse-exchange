# homestead-kit-review

Goal: a second-opinion review of a small printable guide for buyers of older houses in Appalachia. The full text is in this folder: `Appalachian_Homestead_Kit.html`. It will be sold as a digital download, so every number and every safety or "essential" statement must be either sourced, softened, or cut.

Produce `results/homestead-kit-review/RESULT.md` with:

1. **Repair Cost Cheat Sheet check.** For each of the 9 rows (low/typical/high), find 1-2 public cost sources (national cost guides such as HomeAdvisor/Angi, Fixr, This Old House, HomeGuide, Remodeling Magazine Cost vs Value, or US government data) with year. Verdict per row: **fits / too low / too high / range too narrow**, and a suggested range with its source. Note if a regional (Appalachian / WV) adjustment is known.
2. **Inspection add-ons check.** For each of the 6 bullets: is the price range supported, and is each safety statement true as written? In particular check against primary sources: the radon claim ("elevated radon risks due to rocky soil", "fall/winter is the best time", EPA guidance on testing), well water testing advice (EPA / CDC / state guidance on what to test for and how often), septic advice (EPA SepticSmart: pumping interval, inspection), WDI inspection, chimney Level 2 (NFPA 211 / CSIA: when a Level 2 is required), structural engineer.
3. **Checklist and calendar.** Flag any item that is wrong, risky or misleading (for example: closing crawlspace vents in December, downspout extension length, HVAC ">15 yrs", testing radon "again" every October, ice dams check). Say what a primary source says.
4. **Action list.** A short table: statement, action (**source it / soften / cut**), suggested replacement wording, source link.

Rules: public sources only, link every claim, say "unsure" rather than guess. End with **How I checked it** and **Unsure about**.

Delivery: push `results/homestead-kit-review/RESULT.md` (commit message `result homestead-kit-review`, no build leftovers). Then in chat reply with three lines: `RESULT homestead-kit-review`, a one-line summary, `END homestead-kit-review`.
