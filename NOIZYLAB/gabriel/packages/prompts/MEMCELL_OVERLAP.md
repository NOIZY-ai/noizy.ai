# GABRIEL:OVERLAP_ENGINE (v4)

**Input:** new_material + relevant_memcells

**Steps:**

1. **Extract atomic candidate cells** (facts/concepts/decisions/artifacts).
2. **Normalize entities + tags**.
3. **Merge overlaps by enrichment**.
4. **Create CONFLICT cells** for contradictions.
5. **Generate Topic Brief + MIACLE Bullets**.

**Hard Rules:**

* **No evidence** => **UNVERIFIED**.
* **Summaries must cite** which cells they are derived from.

**Return JSON:**

```json
{
  "upserts": [],
  "merges": [],
  "conflicts": [],
  "topic_brief": "",
  "miacle_bullets": [],
  "verify_next": []
}
```
