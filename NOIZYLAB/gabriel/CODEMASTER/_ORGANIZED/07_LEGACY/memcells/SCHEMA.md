# MemCell Schema for Forensic Reconstruction

## Purpose

MemCells store timestamped code artifacts with metadata for forensic analysis and version tracking.

## Schema

```json
{
  "memcell_id": "uuid",
  "timestamp": "ISO8601",
  "source_path": "/original/path/to/file",
  "category": "code|config|prompt|doc",
  "content_hash": "sha256",
  "relevance_score": 0.0-1.0,
  "tags": ["gabriel", "turbo", "mission_control"],
  "dependencies": ["other_memcell_ids"],
  "content": "actual file content or reference"
}
```

## Categories

- `code` - Python, TypeScript, JavaScript, Shell
- `config` - JSON, YAML, TOML configurations
- `prompt` - AI prompt modules
- `doc` - Documentation, markdown

## Reconstruction Process

1. Scan all volumes for code files
2. Extract modification timestamps
3. Hash content for deduplication
4. Score relevance based on keywords
5. Build dependency graph
6. Create memcell entries
7. Commit to repository
