# NOIZY Presentation Decks

> All deck assets for investor, board, creator, and press presentations.

## Deck Variants

| Deck | Style | Audience | Source |
|------|-------|----------|--------|
| **Cathedral Deck** | Cinematic, immersive | Investors, press, creator recruitment | `heaven/design/CATHEDRAL-DECK-SPEC.md` |
| **Agency Section — Cinematic** | Bold, category-defining | Board, investors | `NOIZY_Agency_Section_Cinematic.pptx` |
| **Agency Section — Technical** | Clean, diligence-friendly | Due diligence, technical partners | `NOIZY_Agency_Section_Technical.pptx` |
| **Agency Section — Hybrid** | Boardroom + NOIZY energy | Default board presentation | `NOIZY_Agency_Section_Hybrid.pptx` |
| **Performer Revenue Split** | One-page doc | Artists, unions, legal | `NOIZY_Performer_Revenue_Split_Model.docx` |

## How to Add .pptx Files

From GOD:
```bash
cd ~/noizy.ai
mkdir -p heaven/decks
# Copy files from iCloud/Downloads
cp ~/Downloads/NOIZY_Agency_Section_*.pptx heaven/decks/
cp ~/Downloads/NOIZY_Performer_Revenue_Split_Model.docx heaven/decks/
git add heaven/decks/
git commit -m "Agency deck variants + performer revenue model"
git push origin claude/code-review-hf5hD
```

## Content Already in Repo (text versions)

All deck content exists as deployable markdown:

| Content | File |
|---------|------|
| Category definition | `heaven/noizyvox/AGENCY-POSITIONING.md` |
| Why libraries fail premium buyers | Same file, comparison table |
| Agency operating loop | Same file, 5-stage model |
| Talent profile + rights schema | Same file, JSON examples |
| Revenue model + tiers | Same file + D1 `hvs_rate_table` |
| Moat (8 layers) | Same file, moat section |
| Design system + slide specs | `heaven/design/CATHEDRAL-DECK-SPEC.md` |
| Gospel content | `heaven/gospel/CATHEDRAL.md` |
| Multilingual characters | `heaven/noizyvox/MULTILINGUAL-CHARACTER-SPEC.md` |
| Artist-centric discovery | `heaven/noizyvox/ARTIST-CENTRIC-DISCOVERY.md` |

## The Combined Master Deck (when ready)

Merge sequence:
1. Cathedral Deck (12 slides) — the vision
2. Agency Section (6 slides) — the business
3. = 18-slide master deck covering everything from "Together, We Rise" to "Revenue Model + Moat"

---

*GORUNFREE*
