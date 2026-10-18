# threejs-indie-showcase-20261018

Task: real examples of small teams or solo devs shipping impressive Three.js / React Three Fiber browser games in 2025–2026, ideally with AI help — with creator, team size, stack, AI use quoted, and any public revenue/player numbers — plus five patterns the best-looking browser games share.

Read date for all pages: 2026-10-18. Public pages only. Items marked "search-captured" come from search-result text of the creator's post (X posts could not be opened directly); everything else was read on the page linked.

## The examples

### 1. fly.pieter.com — the one that made real money
- **Play:** https://fly.pieter.com · **Creator:** Pieter Levels (@levelsio), **solo**
- **What it is:** A real-time **multiplayer** 3D flight sim / dogfight game in a browser tab — Three.js (WebGL), WebSockets, Web Audio, custom physics; in-world ad billboards and paid plane upgrades (an F16 at $29.99).
- **AI use:** The flagship "vibe coding" ship — built February 2025 with **Cursor and Claude**, the first version in ~3 hours (reported figures of "30 minutes" in one newsletter vs "~3 hours" in others likely split prototype vs fuller demo).
- **Numbers (creator-shared, as reported):** Levels posted on Mar 12, 2025 that **in 17 days, 320,000 people played and ad profits reached $87,000**; a contemporary newsletter put projected revenue at ~$52,000/month. https://dev.ua/en/news/kalichna-shi-hra-zarobyla-vzhe-87k-baksiv-na-reklami-1741866359 · https://www.beyondthebuzz.ai/p/vibe-coding-a-flying-game

### 2. Claude of Duty — one person, a fleet of agents, zero art assets
- **Play/source:** https://github.com/mshumer/Claude-of-Duty (open source, run locally; **3,471 stars, 527 forks** as read) · **Creator:** Matt Shumer (@mshumer), **solo orchestrator** — the code was written by AI sub-agents
- **What it is:** A browser FPS aiming at Call of Duty quality: **Three.js r180 + WebGL2**, ~55,000 lines across 11 subsystems, custom physics from scratch (BVH raycasts, ragdolls, bullet penetration), HDR pipeline with cascaded shadows, GTAO, TAA, bloom. README, verbatim: *"There are no art assets. Every texture, mesh, animation and sound is generated procedurally at load time from code."*
- **AI use — the creator's published prompt:** *"I want you to build a first-person shooter at the level of the most recent Call of Duty games… Fan out sub-agents and have sub-agents tackle each one individually… Do this in ThreeJS. /loop until it's utterly perfect."* (prompt.md in the repo)
- **Numbers:** After an optimisation pass, **28–30 fps p50** at Retina resolution (from 12–17); 11 adversarial AI critics scored it vs real CoD frames, climbing 3.59 → **5.05/10** — the creator is candid it doesn't match the real thing.

### 3. Tree Appreciator — a complete game from one sentence
- **Play:** via https://tools.simonwillison.net/by-month (Oct 2026) · **Creator:** Simon Willison (@simonw), **solo**, published Oct 14, 2026
- **What it is:** A cozy 3D spot-the-difference game: two trees grown from the same seed in Three.js; find 3–7 differences (31 kinds — missing boughs, an owl, a kite, "a very small door"), with music, animation and achievements.
- **AI use — the creator's entire prompt, published by him:** *"Build a three js game called 'Tree appreciator' - it shows you two algorithmically generated trees and the game mechanics is about appreciating the differences between them. Think hard about how to make sure it is both fun and beautiful."* Run in the Claude phone app (not Claude Code); the model worked **3 hours 7 minutes** on that single prompt and produced the complete game. His shared transcript: https://claude.ai/share/ee7de555-f85c-4ff0-96cb-d51ed5e479e9

### 4. Singularity Rush — a deterministic 3D RTS with no build step
- **Play:** https://webgamerush.com (free, no signup) · **Creator:** "webgamerush" (dev.to), **solo**
- **What it is:** A complete 3D RTS (four AI labs racing to train a Gen-5 model: economy, rival AI, red-team attacks) in ~6,700 lines of plain JavaScript — **no framework, no build step**, Three.js r186 vendored. The sim is decoupled from the renderer (fixed 10 Hz ticks, seeded PRNG, deterministic), so full AI-vs-AI matches run headlessly in Node CI to catch balance regressions. StarCraft II-style stencil silhouettes show units through buildings.
- **AI use — creator's words:** *"I built the whole thing solo, with plenty of help from AI coding tools."* Also: *"AI is very good at producing a change that looks convincing and runs just long enough to fool you, and making those changes survive full matches was a much better filter than staring at the diff."* (Assets are Kenney CC0, not AI-generated.)
- **Numbers:** None shared (free). Postmortem: https://dev.to/webgamerush/what-i-learned-building-a-3d-browser-rts-with-threejs-and-no-build-step-1a31

### 5. Kart Chaos — a full Mario Kart package, in a tab
- **Play:** https://kartchaos.com (no account, works on phones) · **Creator:** "kartchaos" (dev.to), presented as one developer's side project
- **What it is:** 5-track Grand Prix cup, Versus, Time Trial, a daily challenge, and **online multiplayer with rooms, text chat and voice**, plus touch controls — with heavy iteration on arcade drift handling and low-end-phone performance. *"Multiplayer changes everything… Adding rooms, chat and voice on top made it feel like a real game night rather than a tech demo."*
- **Stack:** Three.js + WebGL (multiplayer backend not specified). **AI use:** not mentioned. **Numbers:** none shared.
- https://dev.to/kartchaos/i-built-a-multiplayer-kart-racer-that-runs-in-the-browser-with-threejs-652

### 6. ECHO — your voice is the controller (React Three Fiber)
- **Source:** https://github.com/kishore1035/echo · **Creator:** Team Alt F4, **small team** (hackathon submission, Hacker House Goa 2026)
- **What it is:** A cel-shaded dark-fantasy RPG where spoken commands change the world: say "Destroy the bridge" and it physically collapses; "Call the rain" douses torches and routs enemies. Voice is parsed by a zero-latency local keyword fallback, with Gemini Flash returning structured JSON for natural language. Timeline rewind uses deep immutable world snapshots; NPC fates derive from simulation state, not scripts. All audio is procedurally synthesised (Web Audio) — zero audio files.
- **Stack:** React 19 + TypeScript + Vite, **React Three Fiber + Drei**, Zustand, Web Speech API + Gemini Flash. **AI use:** AI is integral to the *game*; AI *coding* tools not stated.
- https://dev.to/kishore1035/we-built-a-3d-game-where-your-voice-breaks-reality-as-our-hacker-house-submission-4gec

### 7. NEON SIEGE — a complete wave FPS, zero build step
- **Play:** https://fps.gzeven.cc.cd · **Source:** https://github.com/guangzhoueven/fps · **Creators:** guangzhoueven + StarlightFootprint (**2 people**)
- **What it is:** Endless scaling waves with boss fights, 8 weapons, 7 enemy types with distinct AI, a **custom B\* pathfinding algorithm** (A\* fallback), combo/headshot scoring, shop and power-ups, full save/export/import, dynamic day-night sky, bilingual UI — Three.js r160 vendored, vanilla JS, no bundler; also packaged as a Windows Electron app (18 releases since Sep 25, 2026).
- **AI use:** not stated. **Numbers:** none shared (free, open source).

### 8. GoPuzzleGo — 3D jigsaw pieces with car-paint metal
- **Play:** https://gopuzzlego.com (free, no signup) · **Creator:** solo developer (three.js forum showcase post, Oct 8, 2026)
- **What it is:** A jigsaw game where every piece is a real 3D object — extruded with a *modelled* chamfer bevel (not a shader trick) on a tilt-able 3D table. The "Metal puzzles" mode has no image at all: solid-metal pieces in `MeshPhysicalMaterial` with clearcoat, a procedural flake normal map for car-paint finishes and iridescence, lit by image-based lighting. "Planets" mode turns heightmaps into relief terrain per piece. All pieces render as one `BatchedMesh`, so hundreds of metal pieces stay smooth.
- **Stack:** Three.js (BatchedMesh, MeshPhysicalMaterial, IBL). **AI use:** not mentioned. **Numbers:** none shared.
- https://discourse.threejs.org/t/free-game-gopuzzlego-jigsaw-puzzles-in-three-js-car-paint-metals-beveled-pieces-and-planets-you-can-assemble/95131

### 9. The Great Taxi Assignment: Vibe City — won the 2025 Vibe Coding Game Jam
- **Play:** https://great-taxi-assignment.netlify.app · **Creator/team:** not stated in the non-social sources consulted
- **What it is:** **First place** in the 2025 Vibe Coding Game Jam (organised by Pieter Levels; judges included three.js creator Ricardo Cabello/mrdoob and Andrej Karpathy; 1,000+ entries per utsubo's three.js blog). A retro 3D taxi sim: pick up/drop off passengers in a bustling city, manage time and fuel, spend earnings on taxi upgrades.
- **AI use:** By the jam's rules — every entry had to be **at least 80% AI-written** ("at least 80% of the game's code must be generated by AI tools, such as Claude, Gemini, or OpenAI"); the jam recommended three.js. **Numbers:** none shared (prize amount not stated in sources consulted).
- https://www.utsubo.com/blog/threejs-2026-what-changed · https://bizrescuepro.com/exploring-winners-2025-vibe-coding-game-jam/

### 10. Astropilot VR — one weekend, one 5,000-line HTML file
- **Play:** https://astropilot.mikekasberg.com · **Creator:** Mike Kasberg (@mike_kasberg), **solo**, built over **one weekend** for Vibe Jam 2026
- **What it is:** A 3D "Flappy Bird in space" for phones: steer by physically tilting the phone (Device Orientation APIs) through rings on procedurally assembled courses. The entire game is **one ~5,000-line HTML file, 180 kB** — no build, no downloaded assets, programmatic audio.
- **AI use — the creator's launch post:** *"Vibe coded in a single 5,000 line file with plain HTML and JS, mostly in a single weekend. With @threejs, of course!"* Devlog detail: built "primarily with Kimi K2.5 in OpenCode"; the AI also built him a level-editor tool when course generation failed, and a refactor that "probably would have taken me 8 hours or more" took "about ten minutes to write a detailed prompt."
- https://www.mikekasberg.com/blog/2026/06/04/vibe-jam-2026-astropilot.html

### 11. HUSTLE CAB: NEW YORK — a GTA-style city from one prompt (search-captured)
- **Play:** https://taxi-theta-kohl.vercel.app (desktop) · **Creator:** single poster (handle not shown in capture)
- **What it is:** A GTA/Roblox-hybrid taxi game: a whole procedurally generated city with vehicles, pedestrians, carjacking (press F to steal any car), fares that pay more in fancier cars, a "Hustle Combo" for reckless driving, and destructible cars that dent, smoke, burn and explode.
- **AI use — creator's words:** *"Fable 5.1 built this GTA-style taxi game in 2 hours… made entirely from one prompt. Claude generated the whole city, every vehicle, pedestrian, texture, and sound on the fly, no download, no build, no assets. Just Three.js from a CDN and a few JS libraries."*
- Source: Reddit post mirrored in the Claude Project Showcase hub (updated Sep 5, 2026) — search-captured. **Numbers:** none shared.

### 12. @Rubzem's "No Man's Sky" — one prompt, 7,000 players (search-captured)
- **Creator:** @Rubzem, **solo** (X post, Sep 30, 2026, via the Made with Three.js feed)
- **What it is:** A No-Man's-Sky-style space exploration game in the browser — seamless surface-to-space flight with **no loading screens**, later expanded (two more prompts) with ground battles against giant "Behemoth" walkers and capital-ship space battles.
- **AI use / numbers — creator's words:** *"My 'No Man's Sky' game built with 1 prompt went viral: 700k+ views and 7,000+ unique players. So I kept going and added a full galactic war. With 2 more prompts… No loading screens. All in the browser. Built with Opus 5.5 & @threejs on @TesanaAI"*
- https://madewiththreejs.com/

### 13. @maxt3chno's survival world — no coding background, 12 hours (search-captured)
- **Creator:** @maxt3chno, **solo, explicitly no coding background** (X post, Sep 30, 2026, via Made with Three.js)
- **What it is:** A first-person 3D survival world: terrain, water, grass, dynamic weather, full day/night cycle, a drivable car and campfire — running natively in the browser.
- **AI use — creator's words:** *"literally one dude (me) built this entire 3D world: - with no coding background; - coming home after a regular 9-to-5 job; - using 93% of a basic $20 weekly sub quota - in just 12 hours total… all game mechanics, water, grass, terrain, sky, dynamic weather + day/night cycle: built by opus 5.5 - car and campfire: written 100% in code by sonnet 5.5 - AK-47, boat, bed, knife, hands: generated on meshy free tier… and it runs in JUST three.js natively in the browser"*
- https://madewiththreejs.com/

**Also noted:** Pumpkin Collector (trendinggames.tech) — an open-world action game as a single 3,094-line JS class, six biomes in one draw call, three NPC AI archetypes, and multiplayer over a **111-line Node WebSocket relay** (https://www.trendinggames.tech/pumpkin-collector-article.html). ODD & OUT — a ToeJam & Earl-style co-op adventure on **three.js WebGPU + TSL shaders** with a WebGL2 fallback, online co-op via invite link (https://odd-and-out-game.vercel.app; only substantive source found was its trailer/site, so it sits below the main list). A dev.to write-up describes a solo dev shipping **4 complete 3D games in 7 days for ~$20** with "Claude Code (primary) + Codex CLI… Meshy for AI-generated 3D models… Playwright for automated testing… Zero lines of code written by hand" — secondhand, no playable links, cited as colour only (https://dev.to/jasonguo/a-developer-built-4-complete-3d-games-in-7-days-41i6).

## Five patterns the best-looking browser games share

1. **Stylised art direction beats attempted realism.** Low-poly flat-shaded worlds (fly.pieter.com), cel shading (ECHO), procedural trees (Tree Appreciator), retro taxi cities — the winners pick a look that procedural assets can actually sustain. The one deliberate exception, Claude of Duty, shows the cost of chasing realism: an 11-critic adversarial loop to reach 5.05/10 against the real thing.
2. **Lighting and post-processing do the "graphics".** HDR pipelines, cascaded shadows, GTAO, TAA and bloom (Claude of Duty); image-based lighting and clearcoat materials (GoPuzzleGo); dynamic day-night skies (NEON SIEGE, the survival world). Almost nobody wins on raw geometry — they win on light, colour grading and materials.
3. **Procedural everything replaces the asset pipeline.** Worlds, vehicles, textures, sounds and even music are generated in code (Claude of Duty: literally zero asset files; HUSTLE CAB: city, vehicles, pedestrians, textures and sound "on the fly"). Where 3D props are needed, AI generation (Meshy) fills the gap. CC0 libraries (Kenney, Quaternius) are the other standard crutch.
4. **Performance discipline is a design feature, not an afterthought.** Seeded/deterministic sims decoupled from rendering (Singularity Rush runs whole matches headlessly in CI), one-draw-call terrain (Pumpkin Collector), `BatchedMesh` for hundreds of pieces (GoPuzzleGo), stencil tricks from StarCraft II, and a recurring badge of honour: **no build step** — single-file or vendored-library games that load instantly (Astropilot VR: 180 kB total).
5. **A playable link and multiplayer are the distribution strategy.** Every breakout here is click-and-play with no install, and the ones with audiences added cheap multiplayer early — WebSocket relays measured in hundreds of lines, rooms and invite links rather than netcode sophistication (Kart Chaos added rooms + chat + voice; fly.pieter.com's multiplayer + in-world ads are the whole business). The jam circuit (Vibe Jam) and a single shareable URL do the marketing.

## Sources

Linked per example above. Principal sources: the games' own sites/repos (github.com/mshumer/Claude-of-Duty, github.com/kishore1035/echo, github.com/guangzhoueven/fps), creator devlogs and postmortems (mikekasberg.com, dev.to — webgamerush, kartchaos, kishore1035), Simon Willison's tools index and shared Claude transcript (tools.simonwillison.net, claude.ai/share), the three.js forum showcase (discourse.threejs.org), the Made with Three.js feed (madewiththreejs.com), and reporting on fly.pieter.com (dev.ua, beyondthebuzz.ai, codingbeautydev.beehiiv.com).

## How I checked it

- Examples were gathered from two independent sweeps — non-social sources (itch.io/GitHub/dev.to/three.js forum/game sites) and social/community sources (X via search and the Made with Three.js feed, Reddit, devlogs) — then merged and de-duplicated (fly.pieter.com surfaced in both).
- AI-use claims are quoted from the creator's own words wherever the task asked for them; where AI use is only inferable (a jam's ≥80%-AI rule), that basis is stated instead of a quote. Numbers are creator-shared figures as reported, with the reporting source named.
- X posts that couldn't be opened directly are labelled "search-captured" and quoted from the captured text; secondhand items (the dev.to 4-games write-up) are quarantined as colour, not examples.
- Deliberately excluded: a Godot game with a great solo-dev story (wrong engine), an in-development itch.io title with a messy multi-year history (not a clean 2025–26 ship), and platform-roundup play counts for games without identified creators.

## Unsure about

- **fly.pieter.com's build time** — reports differ ("30 minutes" vs "~3 hours"); likely prototype vs fuller demo, but no creator-owned page settled it in the sources consulted.
- **Its revenue figures** come from newsletters/dev.ua reporting the creator's posts, not from a creator-owned page read directly.
- **HUSTLE CAB's creator handle and team size** — not shown in the captured post.
- **The Great Taxi Assignment's creator, team size and stack** — not stated in the non-social sources consulted; its three.js use is inferred from the jam's rules/recommendation, not confirmed for this title.
- **ODD & OUT's** creator/team/AI use — only its trailer description and own site could be found.
- Several creators (Kart Chaos, NEON SIEGE, GoPuzzleGo, Pumpkin Collector) never mention AI either way — "not mentioned" is reported as such, not read as "no AI."
- Search-captured X quotes (@Rubzem, @maxt3chno) are exact as captured in search results but the original posts could not be opened for a full read.
