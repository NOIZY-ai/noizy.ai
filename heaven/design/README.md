# NOIZY Design System — The Cathedral Visual Language

> Black + Amber + Cyan. Cormorant + Inter. 12-column grid. 8px baseline.

## Quick Reference

### Colors
| Token | Hex | Use |
|-------|-----|-----|
| `--noizy-black` | `#0B0B0B` | Background primary |
| `--noizy-amber` | `#FFB300` | Accent, CTAs, headlines |
| `--noizy-cyan` | `#00D1FF` | Secondary accent, highlights |
| `--noizy-neutral` | `#F6F6F6` | Cards, text backgrounds |
| `--noizy-muted` | `#6B7280` | Secondary text |

### Typography
| Level | Font | Size | Use |
|-------|------|------|-----|
| Hero | Cormorant Bold | 72px | Cathedral titles |
| H1 | Cormorant Bold | 56px | Page titles |
| H2 | Cormorant SemiBold | 36px | Section titles |
| H3 | Cormorant SemiBold | 24px | Card titles |
| Body | Inter Regular | 16px | Body copy |
| Caption | Inter Regular | 12px | Labels |

### Grid
- 12 columns, 40px gutters, 80px outer margins
- 48px safe area for logos/footers
- 8px modular scale for vertical rhythm

### Animation
- Entrance: `cubic-bezier(0.22, 1, 0.36, 1)`, 400-700ms
- Stagger: 60-120ms between elements
- Max 2 animated elements per view
- CTA pulse: scale 1→1.03, 1.2s loop

## Files
| File | Purpose |
|------|---------|
| `design-system.css` | CSS variables + base styles + utility classes |
| `slide-specs.md` | Presentation slide templates with exact specs |

## Presentation Slide Templates

### 1. Title Slide
Full-bleed black. Left third: logo + tagline. Right two-thirds: Cormorant Bold 64px amber title. Inter 20px cyan subtitle. Fade-in + slide-up.

### 2. Section Break
Large numeral in cyan at 30% opacity behind. Section title centered. Subtle scale loop.

### 3. Problem Slide
Left column: H2 + amber bullet list. Right column: full-bleed image with 12px cyan border. Staggered bullet fade.

### 4. Solution / Product
Centered mockup carousel (iPhone + iPad + Mac Studio). Feature chips below. Crossfade + scale entrance.

### 5. DreamChamber UI
Left: large app screenshot with parallax entrance. Right: three stacked feature callouts with icons. H3 Cormorant + Inter body.

### 6. Market / Traction
Top KPI strip (3 metrics). Bottom chart area — amber line, cyan highlights, muted gridlines. Line draw animation.

### 7. Financials
Left summary bullets. Right 3-column table (Revenue, Costs, EBITDA). Amber header on black. Sequential row fade.

### 8. Team
Circular portraits with name + role + one-line credential. Cyan vignette background. Pop with 0.12s stagger.

### 9. Ask / Closing
Large ask number in amber. Supporting bullets below. Cyan CTA button with pulse animation.

## The Five Epochs Visual
```
I    Sheet Music    (1400s)  → Publishers profited
II   Recording      (1920s)  → Labels profited
III  Digital        (2000s)  → Platforms profited
IV   Streaming      (2010s)  → Extractors profited
V    NOIZY          (2026)   → CREATORS profit. Finally. Forever.
```
