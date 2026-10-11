# Venu 3 custom fonts missing / falling back in the Connect IQ simulator — full report

Task id: `venu3-fonts-20261011`
Date researched: 2026-10-11
Scope: public Garmin Connect IQ developer documentation and public Garmin forum threads only. No private data is included in this report.

## Summary

A custom watch face for a Venu 3 (45 mm, 454x454 AMOLED) that compiles and runs, but shows missing or fallen-back custom fonts in the full-face simulator, is usually failing for one of a small set of separable reasons. The symptom pattern tells you which:

| Symptom | Most likely layer | First check |
|---|---|---|
| Whole font replaced by a system font, everywhere | Resource not included in the `venu3` build, loaded font not actually used, stale simulator build, or a vector-font call returning null and running a fallback | Clean build; invalid-id test on the fonts file (Section 2.4); null guard on `getVectorFont()` |
| Individual glyphs show as boxes / blank, rest of font fine | Glyph never baked into the BMFont character set, or trimmed at compile time by the `filter` attribute, or a texture page is missing/misnamed | Compare drawn characters against (a) BMFont selected characters and (b) `filter` string |
| Font present but wrong size, weight, or spacing in the simulator only | Known simulator divergence for custom and vector fonts on this device family | Restart the simulator fresh on `venu3`; verify on a real device before changing code |
| Font present in one size, missing in another | Each size is a separate BMFont export; charset, filter, and export options can differ per size | Diff the `.fnt` files and the two `<font>` elements |
| Works after a fresh build, breaks after editing the font | Simulator / build cache still serving the old font | Delete `bin/`, use Clean Project, restart the simulator |
| Face crashes to the IQ logo, or a font load fails, when several/large fonts are loaded | Watch-face heap exhausted (128 KB total on Venu 3 — Section 3) | Simulator footer peak memory; reduce glyph count, sizes, and anti-aliasing |

Key conclusions:

1. BMFont exports must be text-format `.fnt` with **PNG** textures, the needed characters actually selected, and the texture filename inside the `.fnt` matching the shipped `.png` file(s).
2. `filter` and `antialias` in the font XML are compile-time decisions, not cosmetic ones. A digits-only filter deletes every other glyph; anti-aliasing inflates font memory.
3. A folder named `resources-venu3` is not, by itself, a default resource qualifier. Either keep fonts in base `resources/` (recommended for a single-device project) or wire the folder into `monkey.jungle` explicitly.
4. Resolution-qualified folders for other sizes (for example `resources-round-416x416` or `resources-round-390x390`) are not used for the 454x454 Venu 3.
5. Vector fonts via `Graphics.getVectorFont()` are firmware-provided faces that vary by device; a name that works on another model may return `null` on Venu 3, and reported simulator sizing for vector fonts on Venu 3 / Venu 3S is known to diverge from devices.
6. The Venu 3 watch-face heap limit reported in its device `compiler.json` is 131,072 bytes (128 KB) total — code objects, data, and all loaded fonts together. Large anti-aliased fonts with full alphabets are the usual way to exhaust it.

---

## 1) Common causes

### 1.1 BMFont export problems

Garmin's Resources documentation describes converting a font with the BMFont tool, setting the Unicode character set in BMFont's Font Settings before export, and notes that the font converter defaults to non-anti-aliased 1-bit fonts to save memory. Sources: [S1], [S2].

| BMFont setting / artefact | Wrong value | Result |
|---|---|---|
| Texture file format | TGA (the BMFont default in older versions) | Font does not render in Connect IQ, which supports PNG custom fonts only [S5] |
| Bit depth | 8-bit | Glyphs can render whited-out or blacked-out; a forum report fixed this by exporting at 32-bit [S4] |
| Selected characters (Font Settings charset) | Character not selected | Glyph does not exist in the font at all; shows as box/blank everywhere, sim and device |
| Texture page files | `.fnt` references `time_0.png` but the file was renamed, or a second page (`_1.png`) was not copied | Font fails or partially renders; renaming after export is the usual cause |
| Font size "match char height" / padding differences between sizes | Inconsistent between exports | Same design renders at different effective heights per size; looks like a fallback |
| Channel settings for icon fonts | Alpha channel not set to the glyph channel | Icons render as solid blocks (procedure summarised in the custom-font-icon thread [S7]) |

Practical rule: rename files **before** export, or edit the `file="..."` line inside the `.fnt` after renaming, and ship every texture page the `.fnt` references.

### 1.2 Font XML (`resources.xml` / `fonts.xml`) problems

The resource compiler merges XML files under the resource path; a dedicated `resources/fonts/fonts.xml` is the conventional location, with the `.fnt` and `.png` files placed in `resources/fonts/` and the font loaded in code as `Rez.Fonts.<id>` [S6].

Font element attributes (per Garmin's Resources documentation [S1]):

| Attribute | Required | Default | Effect |
|---|---|---|---|
| `id` | Yes | — | Identifier used as `Rez.Fonts.<id>` in code and `@Fonts.<id>` in layouts |
| `filename` | Yes | — | The BMFont-generated `.fnt` file |
| `filter` | No | None (all glyphs) | Only the listed characters are imported; every other glyph is dropped at compile time |
| `antialias` | No | `false` | Imports anti-aliasing information; nicer edges, noticeably more memory |
| `scope` | No | `foreground` | Resource scope (see Garmin's resource scopes documentation) |

Failure modes:

| Mistake | Symptom |
|---|---|
| `filter="0123456789:"` on a font also used for labels | Digits render; `%`, `-`, letters, degree sign, etc. are missing — Garmin's own documented example uses exactly this digits-only filter for a large watch-face number font [S1] |
| `antialias="true"` on a 1-bit (non-AA) export | No improvement in edges; the AA data was never exported |
| `antialias` left `false` on an AA export | Pixelated edges, especially visible in the simulator, where pixels are magnified relative to the watch [S3] |
| `id` in XML does not match code/layout reference | Compile error if the reference is in code; silent system-font fallback is possible where a layout or a code path substitutes a `Graphics.FONT_*` constant |
| Same `id` defined twice (base folder and a device folder) with different filters/sizes | Which definition wins becomes build-dependent; a classic "works for one product, falls back for another" cause |

### 1.3 Per-device and per-resolution resource folders

| Folder pattern | Picked up automatically for Venu 3? | Notes |
|---|---|---|
| `resources/` | Yes | Base path from the jungle file; always included |
| `resources-round/` | Yes (shape qualifier) | Venu 3 is round |
| `resources-round-454x454/` | Yes (shape + size qualifier) | Correct size qualifier for Venu 3 (45 mm) |
| `resources-round-416x416/` | **No** | That is the Venu 2 / Venu 3S size class; a 454x454 build ignores it |
| `resources-round-390x390/` | **No** | vivoactive 5 / Venu Sq 2 class size; ignored for Venu 3 |
| `resources-venu3/` | **No, not by name alone** | Product folders must be wired in through the jungle file (Section 2.3); an unreferenced folder is simply not in the resource path |
| `resources-<language>/` (e.g. for strings) | Language-dependent | Relevant to strings, not a fix for fonts |

Forum discussion of resource folders describes using an intentionally invalid resource id, or temporarily moving non-target folders away and rebuilding for the target, to prove whether a given folder is actually being picked up for a given screen size [S13]. That test is reused in Section 2.4.

A related trap: building and running for product `venu3s` (416x416) and viewing it scaled is not a Venu 3 test. The product id for the 45 mm watch is `venu3` [S19].

### 1.4 Simulator-specific causes (sim wrong, device right)

| Cause | Evidence |
|---|---|
| Stale font in the simulator / build output | A forum thread reports the simulator showing a deleted, replaced font until the project's `bin` folder was deleted / the project was cleaned and rebuilt [S11] |
| Individual glyphs missing in the sim only | A reporter found `%` missing and `7` incomplete at a small size in the simulator, while both rendered on the real device [S10] |
| Different `drawText` behaviour between simulated devices | A Garmin reply in the bug thread attributes the difference to a simulator bug with custom TrueType fonts and says a real device should not behave that way [S12] |
| Vector-font definition carried over from a previously simulated device | A bug report describes the simulator reusing part of a previous device's vector-font definition when the current device's definition is numbers-only, changing what the same code renders [S15] |
| Simulator magnification | Pixelation that is obvious in the sim is much less visible on the real watch, because sim pixels are far larger on screen [S3] |

Working rule: clean, restart the simulator fresh on `venu3`, and treat the real device as ground truth for glyph rendering. Do not ship simulator-compensation hacks for these cases.

### 1.5 Vector fonts — `Graphics.getVectorFont()`

Vector (scalable) fonts are **not** user-supplied fonts. They are faces defined in a specific device's firmware, they vary by device, they are only available on some newer devices, and developers cannot add their own [S8]. Custom bitmap fonts, by contrast, are fixed-height and work on every Connect IQ device, but cannot be used with `drawRadialText` / `drawAngledText` [S8].

| Vector-font mistake | Result |
|---|---|
| Face name copied from another model (for example a Fenix-only face) | `getVectorFont()` returns `null` on Venu 3 |
| Passing the `null` result to `drawText`, or substituting a system font without logging it | Looks exactly like "custom font fell back" |
| Assuming `:font => Graphics.FONT_*` with `:scale` is scalable on every device | Returns `null` where that system font is not scalable on the target; this behaviour is the subject of a documentation-improvement bug report [S14] |
| Trusting sim sizes for Venu 3 / Venu 3S / FR265 / FR965 | A long-running bug thread reports vector fonts rendering at roughly twice the requested size for this device group in the simulator, and a face listed/rendered in the sim that the Venu 3 device definition does not list [S9] |
| Hard-coding a size correction factor from the sim | Face breaks if/when the simulator/device definitions are fixed, and may already be wrong on hardware |

Correct pattern (original example code, not copied from a source):

```monkeyc
var f = null;
if (Graphics has :getVectorFont) {
    f = Graphics.getVectorFont({
        :face => ["RobotoCondensedBold", "RobotoRegular"],
        :size => 80
    });
}
if (f == null) {
    f = Graphics.FONT_NUMBER_HOT; // deliberate, visible fallback
}
```

The array form of `:face` tries faces in priority order, and guarding with `Graphics has :getVectorFont` keeps the code safe on devices/SDKs without the call; this pattern appears in working Venu-sized example projects [S20]. The authoritative face list for this watch is the Venu 3 page of Garmin's Device Reference [S18] and the device files installed with the SDK — not a list copied from another model. A separate bug report for a newer Venu model shows the reference page, the simulator, and the real device disagreeing about which Roboto faces exist, which is why the null check and the array fallback both matter [S16].

### 1.6 Code-path causes

| Cause | Symptom |
|---|---|
| Font loaded in `onLayout()` but the view never uses layouts / `onLayout` path differs in the sim's full-face mode | Font variable stays null; a defensive code path draws with a system font |
| `onEnterSleep()` (low-power / always-on path) replaces the font with a system font, and the simulator is left in the sleep state | Full face appears to have "lost" its font; check which power state the sim is simulating |
| Font loaded every `onUpdate()` | Memory spikes and possible out-of-memory failure (Section 3); also slow |
| Layout XML in a resolution folder for a different size contains the custom-font labels, base layout does not | Venu 3 silently uses the base layout with system fonts |

---

## 2) Correct resource layout and jungle / manifest settings for Venu 3

### 2.1 Recommended layout (single-device project)

```
MyFace/
├── manifest.xml
├── monkey.jungle
├── source/
│   ├── MyFaceApp.mc
│   └── MyFaceView.mc
└── resources/
    ├── drawables/
    │   ├── drawables.xml
    │   └── launcher_icon.png
    ├── fonts/
    │   ├── fonts.xml
    │   ├── time.fnt            <- BMFont export, text format
    │   └── time_0.png          <- BMFont PNG texture; name must match the .fnt
    ├── layouts/
    │   └── layout.xml          <- optional, only if setLayout() is used
    └── strings/
        └── strings.xml         <- must contain AppName
```

This follows the documented pattern: font files in `resources/fonts/`, declared in a fonts XML file, loaded with `loadResource(Rez.Fonts.<id>)` [S6].

### 2.2 Font XML

```xml
<fonts>
  <font id="TimeFont"  filename="time.fnt"  antialias="true" filter="0123456789:" />
  <font id="LabelFont" filename="label.fnt" antialias="true" />
</fonts>
```

Notes:

- One BMFont export per size. Bitmap fonts are fixed-height; a different height is a different font file and a different `<font>` element.
- Keep the time font's filter digits-only; keep the label font's filter wide enough for every string it will draw (day/month abbreviations, AM/PM, units, `%`, `-`, degree sign if used).
- Set `antialias="true"` only for fonts actually exported with anti-aliasing, and only where the memory budget allows (Section 3).

### 2.3 Jungle file

Minimal (recommended when only Venu 3 is targeted):

```
project.manifest = manifest.xml
base.sourcePath = source
base.resourcePath = resources
```

Optional Venu 3-only override folder — only if it is wired in like this:

```
project.manifest = manifest.xml
base.sourcePath = source
base.resourcePath = resources

venu3.resourcePath = $(base.resourcePath);resources-venu3
venu3.sourcePath = $(base.sourcePath)
```

Rules:

- Do not rely on the folder name `resources-venu3` alone; without the jungle line it is not in the build.
- Do not define the same font `id` in both `resources/` and `resources-venu3/` with different contents unless the override behaviour has been verified with the test in Section 2.4.
- The build command form for this product is `monkeyc -d venu3 -f monkey.jungle -o bin/MyFace.prg -y <developer_key>` [S19].

### 2.4 Manifest

```xml
<iq:manifest xmlns:iq="http://www.garmin.com/xml/connectiq" version="3">
  <iq:application id="REPLACE-WITH-A-UUID" type="watchface" entry="MyFaceApp"
                  name="@Strings.AppName" minApiLevel="4.2.0">
    <iq:products>
      <iq:product id="venu3" />
    </iq:products>
    <iq:permissions />
    <iq:languages>
      <iq:language>eng</iq:language>
    </iq:languages>
  </iq:application>
</iq:manifest>
```

Notes:

- `type="watchface"` and the `venu3` product id are the load-bearing parts for this question.
- Keep the `minApiLevel` generated by your SDK template unless you have a reason to raise it; guard newer calls such as `getVectorFont` with `has` checks instead of raising the floor for one call.

### 2.5 Minimal working view (original example code)

```monkeyc
import Toybox.Graphics;
import Toybox.WatchUi;

class MyFaceView extends WatchUi.WatchFace {
    hidden var _timeFont as WatchUi.FontResource?;

    function initialize() {
        WatchFace.initialize();
    }

    function onLayout(dc as Graphics.Dc) as Void {
        // Load once. Do not load resources in onUpdate().
        _timeFont = WatchUi.loadResource(Rez.Fonts.TimeFont) as WatchUi.FontResource;
    }

    function onUpdate(dc as Graphics.Dc) as Void {
        dc.setColor(Graphics.COLOR_WHITE, Graphics.COLOR_BLACK);
        dc.clear();
        var t = System.getClockTime();
        var s = t.hour.format("%02d") + ":" + t.min.format("%02d");
        dc.drawText(dc.getWidth() / 2, dc.getHeight() / 2, _timeFont, s,
                    Graphics.TEXT_JUSTIFY_CENTER | Graphics.TEXT_JUSTIFY_VCENTER);
    }
}
```

### 2.6 Verification test for the resource path

1. Temporarily change the `id` in `fonts.xml` to an invalid identifier.
2. Build for `venu3`. The build **must** fail.
3. If it does not fail, that fonts file is not in the Venu 3 resource path — fix the jungle file / folder before touching any drawing code. (Technique adapted from the resource-folder forum discussion [S13].)
4. Restore the id, delete `bin/`, clean the project, restart the simulator, and run on `venu3` again.

---

## 3) Memory and size limits on Venu 3 that can drop fonts

### 3.1 The limits

| Limit | Venu 3 value | What counts against it | Source / how to verify |
|---|---|---|---|
| Watch-face heap (`watchFace` app type) | **131,072 bytes (128 KB)** | All heap: code objects, strings, data, and every loaded font/bitmap resource | Reported for `venu3` in its device `compiler.json`, the same value as several other current AMOLED models [S17]; per-device limits live in each device's `compiler.json` in the installed SDK [S21] |
| Graphics resource pool (separate from heap) | **4 MB** reported for Venu 3 | `BufferedBitmap`s created through the graphics pool (CIQ 4 enhanced graphics) — not ordinary loaded fonts | Reported from Venu 3's `simulator.json` (`graphicsResourcePoolSize`) [S17] |
| Extended code space (System 8, `:extendedCode`) | 16 MB of paged **code** space on supported devices | Annotated functions/classes/modules only; data created by that code still lives in regular app memory | System 8 summary [S22]; data-in-regular-memory finding [S23]; Venu 3 listed among devices where `:extendedCode` works [S24] |
| Background process heap | Much smaller than the watch-face heap (see `background` in `compiler.json`) | Anything a background service delegate loads | Check `Devices/venu3/compiler.json` in your SDK install [S21] |
| Simulator footer | Shows current / total / **peak** memory for the selected device | Use peak, not idle, when judging headroom | Forum explanation of the simulator memory footer [S25] |

Important distinctions:

- Fonts do not get dropped because a `.prg` file is "too big" in the abstract. They fail when **loading** them would exceed the heap — which surfaces as an out-of-memory error, a crash, or (in defensive code) a fallback font.
- A separate app type on the same hardware gets far more memory (a watch app is reported at 768 KB on the same class of hardware [S17]). That does not help a watch face; the 128 KB figure is an app-type policy, not a hardware limit.

### 3.2 Why fonts are usually the thing that pushes a face over

| Factor | Effect |
|---|---|
| Glyph count | Cost scales with the number of characters baked in. A forum report describes one added 96-character custom font growing an app from about 22K to about 33K, and notes that character count and height are the two drivers, with anti-aliasing adding a noticeable increase on top [S4] |
| Glyph height | Cost grows roughly with the square of height for large number fonts; a full alphabet at time-display size is the worst case |
| Anti-aliasing | The converter defaults to 1-bit non-AA fonts precisely because bitmap fonts can take a lot of runtime memory; AA is opt-in via the `antialias` attribute [S1] |
| Multiple sizes loaded at once | Each size is a separate font resource; holding all of them loaded holds all of their memory at once |
| Loading in `onUpdate()` | An out-of-memory forum case was traced to `loadResource()` inside `onUpdate()`; the recommended fix was to load once in `initialize()` / on settings change [S26] |

### 3.3 Budget practices for a 454x454 face

1. Time font: digits + colon only (`filter="0123456789:"`) — the standard saving, also recommended in forum memory discussions for time-display fonts [S25].
2. Bake each size separately; never include a full alphabet in the largest size.
3. Use anti-aliasing on the fonts where it is visible (large time digits) and consider 1-bit for tiny label fonts.
4. Load fonts once (layout/initialize), not per update; release unneeded sizes (`font = null`) on low-memory code paths.
5. Watch the simulator's **peak** memory during `onUpdate()`, complication updates, and settings changes — not the idle figure.
6. If code size (not data) is the pressure, `:extendedCode` can move code to the 16 MB extended space on Venu 3, but it will not move font data out of the heap [S22] [S23].
7. Do not cache a full-screen 454x454 bitmap in the heap; a full-frame buffer at 16 bpp is roughly 412 KB, far over the heap — use the graphics pool for buffered bitmaps instead [S17].

### 3.4 Ordered diagnostic checklist

| Step | Action | Pass condition |
|---|---|---|
| 1 | Delete `bin/`, Clean Project, restart simulator, run on `venu3` (not `venu3s`) | Symptom reproduced on a clean build |
| 2 | Invalid-id test on the fonts XML (Section 2.6) | `venu3` build fails with the bad id, passes when restored |
| 3 | List every character the face draws; compare against BMFont selected characters **and** the `filter` string | No drawn character is missing from either list |
| 4 | Open the `.fnt`; check every `file="..."` texture page exists, with that exact name and case | All pages present |
| 5 | Check texture format (PNG), bit depth (32), AA export vs. `antialias` attribute | Export and XML agree |
| 6 | Add null/array handling around `getVectorFont()` and log which branch ran | No silent fallback |
| 7 | Read peak memory in the simulator; compare against 131,072 bytes | Peak leaves headroom during updates and settings changes |
| 8 | Sideload to a real Venu 3 | Device rendering is the ground truth where the sim is known to diverge |

---

## Sources

All links are to public Garmin documentation or public forum threads, retrieved 2026-10-11.

- [S1] Garmin Connect IQ — Core Topics: Resources (fonts, BMFont, `filter`, `antialias`, font element attributes). https://developer.garmin.com/connect-iq/core-topics/resources/
- [S2] Garmin Connect IQ FAQ — How Do I Use Custom Fonts? https://developer.garmin.com/connect-iq/connect-iq-faq/how-do-i-use-custom-fonts/
- [S3] Garmin Forums — How to export properly fonts with Bitmap Font Generator? (simulator magnification; `antialias=true` in the font XML). https://forums.garmin.com/developer/connect-iq/f/discussion/6003/how-to-export-properly-fonts-with-bitmap-font-generator
- [S4] Garmin Forums — BMFont program (32-bit depth fix; custom-font memory cost by character count, height, and anti-aliasing). https://forums.garmin.com/developer/connect-iq/f/discussion/167723/bmfont-program
- [S5] Garmin Forums — Using Custom Fonts (Connect IQ supports PNG custom fonts; BMFont default texture format is TGA). https://forums.garmin.com/developer/connect-iq/f/discussion/2193/using-custom-fonts/1138351
- [S6] Garmin Forums — How do I create a custom font? (files in `resources/fonts`, fonts XML, `loadResource(Rez.Fonts.<id>)`). https://forums.garmin.com/developer/connect-iq/f/discussion/430939/how-do-i-create-a-custom-font
- [S7] Garmin Forums — Custom font icon (BMFont/FontForge procedure; PNG textures; channel settings). https://forums.garmin.com/developer/connect-iq/f/discussion/165912/custom-font-icon
- [S8] Garmin Forums — Vector Font faces list? (scalable fonts are firmware-defined per device, cannot be added by developers; custom fonts are fixed-height and universal). https://forums.garmin.com/thread/1775345?ContentTypeID=1
- [S9] Garmin Forums — BUG: Scalable fonts incorrect size on F265/F265s/F965/Venu3/Venu3s. https://forums.garmin.com/developer/connect-iq/f/discussion/348831/bug---scalable-fonts-incorrect-size-on-f265-f265s-f965-venu3-venu3s
- [S10] Garmin Forums — Custom Font with some ascii char missing into simulator (glyphs missing in sim, visible on the real device). https://forums.garmin.com/developer/connect-iq/f/discussion/326573/custom-font-with-some-ascii-char-missing-into-simulator/1585809
- [S11] Garmin Forums — Simulator Showing Old Font (delete `bin` / clean project fix). https://forums.garmin.com/developer/connect-iq/f/discussion/332676/simulator-showing-old-font
- [S12] Garmin Forums (bug reports) — Different behaviour of dc.drawText between devices on simulator (Garmin reply attributing it to a simulator bug with custom TrueType fonts). https://forums.garmin.com/developer/connect-iq/i/bug-reports/different-behaviour-of-dc-drawtext-between-devices-on-simulator?CommentId=34ae2f78-cd49-48a0-9863-48ec45fc1c90
- [S13] Garmin Forums — Help with Resource Folder (proving whether a resource folder is picked up for a given screen size). https://forums.garmin.com/developer/connect-iq/f/discussion/252666/help-with-resource-folder
- [S14] Garmin Forums (bug reports) — Documentation Improvement: getVectorFont() and Scalable Fonts (returns null when the font definition is not scalable on the target). https://forums.garmin.com/developer/connect-iq/i/bug-reports/documentation-improvement-getvectorfont-and-scalable-fonts
- [S15] Garmin Forums (bug reports) — Simulator bug for older systems (simulator reusing a previous device's vector-font definition). https://forums.garmin.com/developer/connect-iq/i/bug-reports/bug-simulator-bug-for-older-systems?CommentId=75d9a67d-a4c6-44a1-8c8a-06cc10543186
- [S16] Garmin Forums (bug reports) — Venu X1 Simulator vector font does not match actual device (reference page / simulator / device disagreement on available faces; cited as a pattern, not as Venu 3 evidence). https://forums.garmin.com/developer/connect-iq/i/bug-reports/venu-x1-simulator-vector-font-does-not-match-actual-device
- [S17] Third-party performance analysis checking installed SDK device files — Venu 3 `watchFace = 131072` in `compiler.json`, graphics pool 4 MB on Venu 3 in `simulator.json`, full-frame buffer estimate. https://github.com/wistrand/moonkey/blob/HEAD/agent_docs/perf-analysis.md
- [S18] Garmin Connect IQ — Device Reference: Venu 3. https://developer.garmin.com/connect-iq/device-reference/venu3/
- [S19] Public Garmin project documentation — `monkeyc -f monkey.jungle -d venu3` build form and `monkeydo <prg> venu3` simulator deployment. https://github.com/alexandruc/custom_reminders
- [S20] Public Venu-sized watch-face project — `getVectorFont` priority-array face list, `Graphics has :getVectorFont` guard, system-font fallback. https://github.com/trip1elift/garmin-watchface-custom
- [S21] Garmin Forums — What is best practice to offer same App for low memory and high memory devices? (per-device memory limits are in each device's `compiler.json` installed by the SDK Manager). https://forums.garmin.com/developer/connect-iq/f/discussion/387411/what-is-best-practice-to-offer-same-app-for-low-memory-and-high-memory-devices
- [S22] Garminology — Garmin Connect IQ System 8 Beta details (16 MB extended code space via `:extendedCode`). https://www.garminology.com/2025/01/10/garmin-connect-iq-system-8-beta-details/
- [S23] Garmin Forums — Rez vs extendedCode (data created by extended-code functions remains in regular app memory). https://forums.garmin.com/developer/connect-iq/f/discussion/409103/rez-vs-extendedcode
- [S24] Garmin Forums — :extendedCode — Inconsistent Implementation in SDK / Devices (works on Venu 3; out-of-memory crashes on some other System 8 devices). https://forums.garmin.com/developer/connect-iq/f/discussion/415479/extendedcode---inconsistent-implementation-in-sdk-devices
- [S25] Garmin Forums — out of memory (simulator memory footer meaning; cutting a time font back to digits and colon to save memory). https://forums.garmin.com/developer/connect-iq/f/discussion/4629/out-of-memory
- [S26] Garmin Forums — getting Error: Out Of Memory Error (crash traced to `loadResource()` in `onUpdate()`; load once instead). https://forums.garmin.com/developer/connect-iq/f/discussion/274289/getting-error-out-of-memory-error-details-failed-invoking

## How I checked it

- Every factual claim above is tied to a Garmin documentation page or a public Garmin forum thread found in web search on 2026-10-11; the Garmin Resources page and the custom-fonts FAQ were opened directly, and forum claims were read in the threads themselves, not only in snippets.
- Cross-checked the memory figure two ways: a forum explanation that per-device limits live in each device's SDK `compiler.json` [S21], and a third-party analysis that read the installed device files and reported `watchFace = 131072` for `venu3` specifically [S17]. Both agree the limit is an app-type value in the device files.
- Cross-checked the vector-font claims across three independent threads: firmware-defined faces [S8], the Venu 3-family sizing bug [S9], and the null-return documentation report [S14].
- The code in Sections 1.5 and 2.5 is original example code written for this report, following the documented loading pattern in [S2] and [S6]; it was not copied from any source.
- This file was scanned before committing for personal-data patterns (names, emails, phone numbers, credential/token strings) per the repository rules; none are present. All content is original paraphrase and synthesis with source links, with no substantial copied text.

## Unsure about

- The exact list of scalable (vector) face names available on Venu 3 firmware: Garmin's device-reference web page did not render its data table in a text-readable form during this research, and forum evidence shows the reference page, the simulator definitions, and real devices can disagree [S9] [S16]. Verify against the `simulator.json` / device files in your installed SDK and, ideally, on hardware.
- The 131,072-byte watch-face figure and the 4 MB graphics-pool figure are reported from installed SDK device files by a third-party analysis [S17], consistent with Garmin's forum guidance on where the limits live [S21], but they were not re-read from a local SDK install during this research (no Connect IQ SDK is installed in this workspace). Treat them as "verify in your own `Devices/venu3/compiler.json`".
- Whether a product-qualified jungle line (`venu3.resourcePath = ...`) overrides or supplements the base path for a duplicate font `id` in a given SDK version: behaviour is described indirectly in forum discussion [S13], not in a single unambiguous Garmin statement found in this research. The invalid-id test in Section 2.6 is the reliable way to confirm it for your SDK version.
- Simulator bug reports cited here span several SDK versions; some may be fixed in the current SDK. The clean-build / fresh-simulator / real-device checks in Section 3.4 remain valid regardless.
