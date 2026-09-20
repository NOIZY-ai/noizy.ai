-- NOIZY Imperial Registry — Universe manifest table
-- Deploy: wrangler d1 execute agent-memory --file=imperial-registry.sql

CREATE TABLE IF NOT EXISTS imperial_registry (
  canonical_id TEXT PRIMARY KEY,
  name TEXT NOT NULL,
  type TEXT NOT NULL,
  status TEXT NOT NULL,
  owner TEXT NOT NULL,
  domain TEXT,
  repo TEXT,
  next_milestone TEXT,
  clock TEXT DEFAULT 'now',
  created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
  updated_at DATETIME DEFAULT CURRENT_TIMESTAMP
);

-- Seed the 10 pillars from the Imperial Charter
INSERT OR REPLACE INTO imperial_registry VALUES
  ('n001', 'NOIZY.AI', 'command_center', 'ACTIVE', 'RSP_001', 'noizy.ai', 'NOIZY-ai/noizy.ai', 'Email routing', 'now', datetime('now'), datetime('now')),
  ('n002', 'DreamChamber', 'creation_interface', 'DESIGNED', 'RSP_001', 'noizy.ai', 'NOIZY-ai/noizy.ai/apps/cathedral-web', 'Pilot launch', 'next', datetime('now'), datetime('now')),
  ('n003', 'GABRIEL', 'guardian_strategist', 'LIVE_D1', 'RSP_001', NULL, 'NOIZY-ai/noizy.ai/heaven/agents', 'Deploy to Ollama', 'now', datetime('now'), datetime('now')),
  ('n004', 'HEAVEN', 'routing_orchestration', 'DESIGNED', 'CB01', NULL, 'NOIZY-ai/noizy.ai/heaven/routing', 'Deploy Worker', 'next', datetime('now'), datetime('now')),
  ('n005', 'NOIZY_PROOF', 'truth_engine', 'BUILT', 'GABRIEL', NULL, 'NOIZY-ai/noizy.ai/schemas', 'Pilot validation', 'next', datetime('now'), datetime('now')),
  ('n006', 'Consent_Gateway', 'legal_boundary', 'CODE_READY', 'ENGR_KEITH', NULL, 'NOIZY-ai/noizy.ai/cloudflare/workers', 'Deploy Worker', 'now', datetime('now'), datetime('now')),
  ('n007', 'NOIZYFISH', 'music_engine', 'CONSTITUTION_WRITTEN', 'RSP_001', NULL, 'NOIZY-ai/noizy.ai/docs/noizyempire', 'Pilot 0-30 days', 'next', datetime('now'), datetime('now')),
  ('n008', 'NOIZYVOX', 'voice_sovereignty', 'POSITIONED', 'GABRIEL', NULL, 'NOIZY-ai/noizy.ai/heaven/noizyvox', 'First talent intake', 'next', datetime('now'), datetime('now')),
  ('n009', 'NOIZYLAB', 'revenue_engine', 'ACTIVE', 'SHIRLEY', 'noizylab.ca', NULL, 'Device repair ops', 'now', datetime('now'), datetime('now')),
  ('n010', 'NOIZYKIDZ', 'future_culture', 'PLANNED', 'POPS', NULL, NULL, 'Design phase Q3', 'forever', datetime('now'), datetime('now'));
