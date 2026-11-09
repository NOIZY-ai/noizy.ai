# MEMCELL++ (v3)

## JSON SCHEMA

```json
{
  "id": "mc_<timestamp>_<slug>",
  "type": "fact | concept | decision | artifact | source | conflict | preference | task",
  "claim": "single sentence claim OR single concept label",
  "summary": "1-2 lines max",
  "entities": ["people", "products", "projects", "files", "tracks"],
  "tags": ["mc96", "gabriel", "audio", "video"],
  "provenance": {
    "source_ids": ["src_<...>"],
    "captured_at": "ISO-8601",
    "author": "GABRIEL | Rob"
  },
  "evidence": [
    { "source_id": "src_...", "quote": "<=25 words", "locator": "page/line/timecode" }
  ],
  "confidence": 0.0,
  "integrity": {
    "input_hash": "sha256:...",
    "cell_hash": "sha256:..."
  },
  "links": {
    "supports": ["mc_..."],
    "contradicts": ["mc_..."],
    "depends_on": ["mc_..."],
    "related": ["mc_..."]
  },
  "checks": [
    { "method": "cross_source", "result": "pass|fail|pending", "notes": "" },
    { "method": "tool_test", "result": "pass|fail|pending", "notes": "" }
  ]
}
```
