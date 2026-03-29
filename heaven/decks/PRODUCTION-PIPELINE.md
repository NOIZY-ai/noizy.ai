# Cathedral Deck — Production Pipeline

> Figma layers, PowerPoint animations, asset manifest.
> Exact filenames. Exact timings. Exact export settings.

---

## Figma Setup

- **File:** `NOIZY_CATHEDRAL_Deck.fig`
- **Frame size:** 1920 × 1080 (16:9)
- **Grid:** 12 columns, 40px gutters, 80px margins, 8px baseline
- **Color styles:** `--noizy-black`, `--noizy-amber`, `--noizy-cyan`, `--noizy-gold`, `--noizy-neutral`, `--noizy-muted`
- **Text styles:** `H1/Cormorant/72/Amber`, `H2/Cormorant/44/Amber`, `H3/Cormorant/28/White`, `Body/Inter/16/Neutral`, `Caption/Inter/12/Muted`
- **Components:** `Title_Master`, `Gospel_Master`, `TwoColumn_Master`, `FullBleed_Master`, `DeviceMockup_Component`, `Callout_Component`, `KPI_Strip_Component`

---

## Slide 01 — Title

**Frame:** `01_Title / 1920x1080`

| Layer | Style | Export |
|-------|-------|--------|
| `Title_Text` | H1/Cormorant/72/Amber | no export |
| `Subtitle_Text` | Body/Inter/20/Cyan | no export |
| `Logo_SVG` | — | SVG 1x → `01_logo_noizy.svg` |
| `Hero_Image_Faint` | masked right 2/3 | PNG @2x → `01_hero_faint@2x.png` |
| `BG_RimLight_Right` | gradient overlay | PNG @2x → `01_rimlight@2x.png` |
| `BG_Vignette` | black + grain | PNG @2x → `01_bg_vignette@2x.png` |

**Animation:** Title fade 0.6s → Subtitle float-in 0.5s (0.12s delay) → Hero appear 0.4s

---

## Slide 02 — Gospel Covenant

**Frame:** `02_Gospel / 1920x1080`

| Layer | Style | Export |
|-------|-------|--------|
| `BG_Solid` | --noizy-black | no export |
| `Covenant_Line` | Cormorant Bold 64/gold | PNG @2x → `02_covenant_line@2x.png` |

**Animation:** Grow/Shrink 98%→100% in 0.42s. Nothing else. Let it hit.

---

## Slide 03 — Problem

**Frame:** `03_Problem / 1920x1080`
**Layout:** left 6 cols text, right 6 cols image

| Layer | Style | Export |
|-------|-------|--------|
| `Problem_Heading` | H2/Cormorant/36/Amber | no export |
| `Problem_Bullet_1-3` | Body/Inter/18/White | no export |
| `Right_Image` | masked | PNG @2x → `03_problem_image@2x.png` |
| `Right_Image_Stroke` | 12px cyan | no export (shape in PPT) |

**Animation:** Heading fade 0.5s → Bullets stagger (0.36s each, 0.08s delay) → Image fade 0.5s

---

## Slide 04 — Solution

**Frame:** `04_Solution / 1920x1080`

| Layer | Style | Export |
|-------|-------|--------|
| `BG_DreamChamber_Mood` | particles + soundwave | PNG @2x → `04_bg_mood@2x.png` |
| `Overlay_Card` | semi-transparent 1100×420 | no export |
| `Feature_Chip_1-3` | Callout_Component | SVG icons → `04_chip1-3_icon.svg` |

**Animation:** Background parallax (Morph 6s) → Card fade 0.5s → Chips float-in stagger 0.08s

---

## Slide 05 — DreamChamber Immersive

**Frame:** `05_DreamChamber / 1920x1080`

| Layer | Style | Export |
|-------|-------|--------|
| `BG_Particles` | particle field | PNG @2x → `05_particles@2x.png` |
| `BG_Volumetric` | volumetric light | PNG @2x → `05_volumetric@2x.png` |
| `Mid_SoundWaves` | animated | Lottie → `05_soundwave.json` + `.aep` |
| `FG_Silhouette` | human figure transparent | PNG @2x → `05_silhouette@2x.png` |
| `Dream_Tagline` | Cormorant/36/gold | PNG @2x → `05_tagline@2x.png` |

**Animation:** Volumetric fade 0.6s → Silhouette wipe L→R 1.2s (soft edge 20px) → Tagline fade 0.42s. Lottie loops.

---

## Slide 06 — Product UI

**Frame:** `06_ProductUI / 1920x1080`
**Layout:** left 7 cols mockup, right 5 cols callouts

| Layer | Style | Export |
|-------|-------|--------|
| `MacStudio_Mockup` | device | PNG @2x → `06_macstudio@2x.png` |
| `iPad_Mockup` | device | PNG @2x → `06_ipad@2x.png` |
| `iPhone_Mockup` | device | PNG @2x → `06_iphone@2x.png` |
| `UI_Screen_Replace` | placeholder | PNG @2x → `06_ui_screen@2x.png` |
| `Callout_1-3` | Callout_Component | SVG icons → `06_callout1-3_icon.svg` |

**Animation:** Devices fade+grow stagger 0.12s → Callouts float-in from right stagger 0.08s

---

## Asset Manifest

| Filename | Type | Size | Format | License |
|----------|------|------|--------|---------|
| `logo_noizy.svg` | vector | vector | SVG | internal brand |
| `01_hero_faint@2x.png` | image | 3840×2160 | PNG | commercial required |
| `02_covenant_line@2x.png` | image | 3840×2160 | PNG | generated |
| `03_problem_image@2x.png` | image | 1920×1080 | PNG | commercial required |
| `04_bg_mood@2x.png` | image | 3840×2160 | PNG | generated |
| `05_particles@2x.png` | image | 3840×2160 | PNG | generated |
| `05_volumetric@2x.png` | image | 3840×2160 | PNG | generated |
| `05_soundwave.json` | motion | vector | Lottie | include .aep |
| `05_silhouette@2x.png` | image | 1920×1080 | PNG | model release |
| `06_macstudio@2x.png` | mockup | 1920×1080 | PNG | mockup license |
| `06_ipad@2x.png` | mockup | 1200×1600 | PNG | mockup license |
| `06_iphone@2x.png` | mockup | 800×1600 | PNG | mockup license |
| `portrait_rob@2x.png` | portrait | 1200×1600 | PNG | model release |
| `grain_overlay@2x.png` | texture | 3840×2160 | PNG | commercial |

## PowerPoint Global Settings

- Slide size: 1920×1080 (16:9)
- Transition easing: Morph where available, Fade fallback
- Animation easing: Ease Out (Smooth End)
- Export: 30fps, Full HD or 4K

## Licensing Checklist

- [ ] Stock images: commercial license + receipts
- [ ] Portraits: signed model releases in `/legal/releases/`
- [ ] Fonts: Cormorant + Inter desktop/web licenses confirmed
- [ ] Lottie/AE: plugin license receipts
- [ ] Mockups: commercial use verified

---

*Cathedral Deck Production Pipeline v1.0*
*Slides 01–06 of 18. Remaining slides follow same conventions.*
*GORUNFREE*
