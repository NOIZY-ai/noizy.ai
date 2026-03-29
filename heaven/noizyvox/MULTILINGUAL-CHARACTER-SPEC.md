# NOIZYVOX — Multilingual Character Adaptation Layer

> Canonical Character → Language Variants. Characters that survive translation.

---

## Core Concept

### Canonical Character (language-agnostic soul)
- Character brief (identity, motivations, vibe)
- Emotional palette (calm / menace / tenderness / mania)
- Boundaries (allowed/restricted/disallowed categories)
- Pricing tier + licensing categories

### Language Variant (language-specific skin)
- Language + locale: `fr-CA`, `es-ES`, `ja-JP`
- Accent/dialect target
- Pronunciation lexicon (names, invented terms)
- Cultural adaptation notes (idioms, formality level)
- Performance mode mapping (emotion equivalence)

---

## Three Adaptation Methods

### Method 1 — Native Performance (Best Quality)
Actor performs the character in the target language.
- Capture: 3-5 minutes per emotional mode per language
- Result: strongest authenticity
- Use when: premium clients, hero characters, cultural sensitivity required

### Method 2 — Multilingual Clone Transfer (Fastest Scale)
Actor provides base language reference; system generates target language.
- Works with: Qwen3-TTS (10 languages), Chatterbox Multilingual (23 languages)
- Risk: accent transfer and prosody mismatch
- Mitigation: match reference clip language to target language tag

### Method 3 — Character Franchise (Premium)
Different voice actors in different languages perform the same canonical character.
- Licensing the character identity system, not just the voice
- How Disney-level dubbing works — one character, many languages
- The Voice Identity System endgame

---

## Emotional Mapping (per language variant)

| Canonical Mode | French-CA Mode | Notes |
|---------------|----------------|-------|
| calm authority | calm authority | pace slightly slower |
| restrained menace | polite menace | menace via warmth + subtext |
| intimate vulnerability | intimate vulnerability | reduce intensity, soften consonants |

Emotion is not 1:1 across cultures. Every language variant needs explicit emotional mapping.

---

## Pronunciation & Glossary (mandatory)

Per language variant:
- **Proper nouns**: names, cities, drug names, fantasy terms
- **IPA / phoneme hints**
- **Forbidden substitutions** (e.g., never anglicize "Benoit")

---

## Client Experience — Multilingual Casting

Artist Profile Layout:
- Actor hero reel
- Characters (4-6 cards)
- Each card shows language flags: EN ✅ FR-CA ✅ ES ✅ JA ⏳
- Clicking a language plays that variant demo
- Boundaries display per character + per language

Search filters:
- Language + locale (fr-CA matters in Canada)
- Accent/dialect
- Use-case tags (games, docs, training)
- Emotional profile tags

**Category wedge:** ElevenLabs has 10k voices. NOIZYVOX has "Find the character in the language you ship in."

---

## Economics — Range × Languages = Compounding Asset

### Per Character
More characters = more surface area.

### Per Language Variant
Each language variant = its own licensable SKU:
- EN character = baseline
- FR-CA variant = +20%
- ES variant = +15%

### Franchise Licensing
Studio wants character across 8 languages:
- Buy the character identity bundle
- Route to native actors or multilingual models
- Engine splits royalties per language contributor

---

## Governance — Language-Aware Boundaries

### Boundaries can be language-specific
- "Allowed: crime drama" (global)
- "Restricted: political persuasion" (global)
- "Extra restriction for locale X" (language-specific)

### Disclosure / Provenance
- EU AI Act Article 50: synthetic content must be detectable/marked
- Attach "synthetic audio" metadata + audit logs from day one
- NOIZY PROOF handles this — every use stamped with provenance

---

## Technology Support Matrix

| Engine | Languages | Emotion Control | Notes |
|--------|-----------|----------------|-------|
| Qwen3-TTS | 10 major | Via description | Multilingual by design |
| Chatterbox Multilingual | 23 | Expressiveness settings | Match ref language to target |
| Kokoro TTS | Multi | Pronunciation hints | High quality, popular |
| IndexTTS 2 | Multi | Emotion methods | Expressive synthesis |
| Dia 1.6B | **English only** | Dialogue generation | Not for multilingual |
| MegaTTS 3 | Multi | Voice cloning | Micro-inflection capture |
| Voice Clone | Multi | Minimal samples | Industry standard |

---

## Schema (YAML reference)

```yaml
Character:
  id: char_123
  canonical:
    name: "Detective Morrison"
    brief: "Burnt-out cop, sardonic humor, trauma carried quietly"
    boundaries:
      allowed_categories: ["crime_drama", "thriller", "noir"]
      restricted_categories: ["copaganda"]
      disallowed_categories: ["impersonation", "deception"]
    modes:
      - id: calm_authority
      - id: restrained_menace
      - id: intimate_vulnerability
    base_pricing:
      unit: "characters"
      rate: 0.15
  language_variants:
    - lang: "en-US"
      method: "native_performance"
      demos:
        calm_authority: demo_en_calm.wav
        restrained_menace: demo_en_menace.wav
      glossary:
        proper_nouns: [...]
      notes: "Baseline"
    - lang: "fr-CA"
      method: "native_performance"
      emotional_mapping:
        restrained_menace: "polite_menace"
      glossary:
        proper_nouns: [...]
      pricing_multiplier: 1.2
    - lang: "es-ES"
      method: "multilingual_clone_transfer"
      constraints:
        require_language_matched_reference: true
      pricing_multiplier: 1.15
```

---

*NOIZYVOX Multilingual Character Spec v1.0*
*GORUNFREE*
