# Crew portraits — result

Summary: all eleven portraits are done in one shared style — stylised illustration (not photorealistic, no real-person likeness), head-and-shoulders, three-quarter view, soft studio light, calm confident expressions, the same deep green-black background (`#111A17`) for the whole set, and one signature accent colour per character as a clothing detail and rim light. Every portrait is exactly 768×768 and well under 300 KB. `contact-sheet.png` shows all eleven side by side in the task's order. The exact prompt used for each image is listed below so any single portrait can be redone later.

## Files

All in `results/crew-portraits/`. Portraits are 768×768 JPEG; sizes measured after final standardisation (see "How I checked it").

| File | Character — role | Signature accent | Size |
|---|---|---|---|
| `ada.jpg` | Ada — lead, organiser | Sage `#B1CCA7` | 70,359 bytes |
| `chloe.jpg` | Chloe — co-lead, builder | Cyan `#91C2B5` | 68,988 bytes |
| `wren.jpg` | Wren — researcher | Blue `#91ADBA` | 88,533 bytes |
| `wilder.jpg` | Wilder — health and fitness planner | Yellow `#D4BE89` | 81,943 bytes |
| `marlow.jpg` | Marlow — web and app builder | Purple `#B6A6BF` | 74,888 bytes |
| `sage.jpg` | Sage — systems and housekeeping | Sage, darker shade | 65,084 bytes |
| `flint.jpg` | Flint — researcher | Red `#DC9184` | 39,979 bytes |
| `harbor.jpg` | Harbor — reliability and repairs | Blue, darker shade | 55,915 bytes |
| `petra.jpg` | Petra — designer and planner | Purple, lighter shade | 92,498 bytes |
| `vega.jpg` | Vega — desktop and devices | Cyan, deeper shade | 74,688 bytes |
| `muse.jpg` | Muse — outside researcher | Yellow, warmer shade | 96,675 bytes |
| `contact-sheet.png` | All eleven side by side, in the order above | — | 2,816×256 px, 769,406 bytes |

## Exact prompts used

One generation call per portrait. Every prompt shares the same style block; only the character paragraph and the accent differ. The prompts below are the exact text passed to the image tool.

**ada.jpg**
> Stylised illustration portrait, not photorealistic, no real-person likeness, head and shoulders, three-quarter view, soft studio light, calm confident expression, clean simple solid deep green-black background #111A17, consistent team dashboard illustration style, square composition. A fictional woman AI agent character in her 40s, warm brown skin, dark hair with a silver streak in a low bun, steady and warm, the lead and organiser. Sage green #B1CCA7 clothing detail and matching soft rim light. No text.

**chloe.jpg**
> Stylised illustration portrait, not photorealistic, no real-person likeness, head and shoulders, three-quarter view, soft studio light, calm confident expression, clean simple solid deep green-black background #111A17, consistent team dashboard illustration style, square composition. A fictional East Asian woman AI agent character in her 30s, sharp black bob haircut, sharp and quick, a co-lead and builder. Cyan #91C2B5 clothing detail and matching soft rim light. No text.

**wren.jpg**
> Stylised illustration portrait, not photorealistic, no real-person likeness, head and shoulders, three-quarter view, soft studio light, calm confident expression, clean simple solid deep green-black background #111A17, consistent team dashboard illustration style, square composition. A fictional South Asian woman AI agent character, long dark wavy hair, thin round glasses, careful and thoughtful, a researcher who is careful with numbers. Soft blue #91ADBA clothing detail and matching soft rim light. No text.

**wilder.jpg**
> Stylised illustration portrait, not photorealistic, no real-person likeness, head and shoulders, three-quarter view, soft studio light, calm confident expression, clean simple solid deep green-black background #111A17, consistent team dashboard illustration style, square composition. A fictional Black woman AI agent character, short natural curls, athletic build, energetic and bright, a health and fitness planner. Warm yellow #D4BE89 clothing detail and matching soft rim light. No text.

**marlow.jpg**
> Stylised illustration portrait, not photorealistic, no real-person likeness, head and shoulders, three-quarter view, soft studio light, calm confident expression, clean simple solid deep green-black background #111A17, consistent team dashboard illustration style, square composition. A fictional woman AI agent character in her 30s, auburn hair in a ponytail, inventive and focused, a web and app builder. Purple #B6A6BF clothing detail and matching soft rim light. No text.

**sage.jpg**
> Stylised illustration portrait, not photorealistic, no real-person likeness, head and shoulders, three-quarter view, soft studio light, calm confident expression, clean simple solid deep green-black background #111A17, consistent team dashboard illustration style, square composition. A fictional woman AI agent character in her 50s, grey hair in a long braid, serene and methodical, responsible for systems and housekeeping. Deep sage green clothing detail, a darker shade than light sage, and matching soft rim light. No text.

**flint.jpg**
> Stylised illustration portrait, not photorealistic, no real-person likeness, head and shoulders, three-quarter view, soft studio light, calm confident expression, clean simple solid deep green-black background #111A17, consistent team dashboard illustration style, square composition. A fictional woman AI agent character, short cropped copper-red hair, light freckles, direct and no-nonsense, a researcher. Muted red #DC9184 clothing detail and matching soft rim light. No text.

**harbor.jpg**
> Stylised illustration portrait, not photorealistic, no real-person likeness, head and shoulders, three-quarter view, soft studio light, calm confident expression, clean simple solid deep green-black background #111A17, consistent team dashboard illustration style, square composition. A fictional woman AI agent character, strong build, dark brown hair in a practical braid, dependable and calm under pressure, responsible for reliability and repairs. Dark slate blue clothing detail, a darker shade than soft blue, and matching soft rim light. No text.

**petra.jpg**
> Stylised illustration portrait, not photorealistic, no real-person likeness, head and shoulders, three-quarter view, soft studio light, calm confident expression, clean simple solid deep green-black background #111A17, consistent team dashboard illustration style, square composition. A fictional Mediterranean woman AI agent character, voluminous curly dark hair, elegant and precise, a designer and planner. Light lavender purple clothing detail, a lighter shade than mid purple, and matching soft rim light. No text.

**vega.jpg**
> Stylised illustration portrait, not photorealistic, no real-person likeness, head and shoulders, three-quarter view, soft studio light, calm confident expression, clean simple solid deep green-black background #111A17, consistent team dashboard illustration style, square composition. A fictional woman AI agent character, sleek dark hair with a subtle undercut, poised and technical, responsible for desktop and devices. Deep teal cyan clothing detail, a deeper shade than light cyan, and matching soft rim light. No text.

**muse.jpg**
> Stylised illustration portrait, not photorealistic, no real-person likeness, head and shoulders, three-quarter view, soft studio light, calm confident expression, clean simple solid deep green-black background #111A17, consistent team dashboard illustration style, square composition. A fictional woman AI agent character, warm golden-brown wavy shoulder-length hair, curious and friendly, an outside researcher. Warm golden yellow clothing detail, a warmer shade than pale yellow, and matching soft rim light. No text.

## Quota

**11 image-generation calls** — exactly one per portrait. The contact sheet and the resizing/compression were done locally with Pillow and used no generation quota. The image tool did not report a quota figure or remaining balance, so I cannot state a percentage — only the call count above.

## How I checked it

- Generated at 1600×1600, then standardised locally: centre-cropped square (they were already square), resized to exactly 768×768, saved as JPEG quality 88. Final dimensions and file sizes were verified programmatically for all eleven files — every one is 768×768 and between 39,979 and 96,675 bytes, i.e. under the 300 KB target and the 1 MB repo limit.
- Built `contact-sheet.png` from the final files and **looked at it**: all eleven read as one set (same illustration style, lighting, dark background, head-and-shoulders three-quarter framing), each character is visually distinct, and each accent colour is visible as clothing/rim light. No text or watermarks appear in any portrait.
- The raw generation outputs and their metadata files were moved out of the results folder, so this folder contains only the eleven portraits, the contact sheet and this file.
- Scanned this file and the file list for personal details before committing: none — all characters are fictional, and no names beyond the crew's character names, addresses, accounts or credentials appear anywhere.

## Unsure about

- **Appearances are my invention.** The task gave name, role, vibe and accent colour for each character, but no appearance, age or ethnicity — I assigned distinct looks so the set reads as a team of different people. If the crew has specific looks in mind for anyone, give me a description and I will redo just that one portrait from its prompt above.
- **Shade interpretations:** where the task said "a different / darker / lighter shade" of a shared colour (Sage vs Ada, Harbor, Petra, Vega), the exact shade was described in words in the prompt rather than as a hex value, because the task gave no hex for the variants. The generator's interpretation is consistent across the set but not a precise hex match.
- **Style consistency** was achieved with an identical style block in every prompt and verified by eye on the contact sheet; it is not pixel-level identical lighting, and a redo of a single portrait may drift slightly from the set.
