-- NOIZY Consent Gateway D1 Schema
-- Database: agent-memory
-- Version: 1.0.0

-- ============================================================================
-- consent_records
-- The source of truth for creator consent state.
-- ============================================================================
CREATE TABLE IF NOT EXISTS consent_records (
    id              TEXT PRIMARY KEY,
    creator_id      TEXT NOT NULL,
    consent_id      TEXT NOT NULL UNIQUE,
    status          TEXT NOT NULL CHECK (status IN ('active', 'revoked')),
    scope_json      TEXT DEFAULT '{}',
    usage_types     TEXT DEFAULT '*',
    exclusions      TEXT DEFAULT '[]',
    granted_at      TEXT NOT NULL,
    revoked_at      TEXT,
    created_at      TEXT NOT NULL DEFAULT (datetime('now'))
);

CREATE INDEX IF NOT EXISTS idx_consent_records_creator
    ON consent_records (creator_id, status);

CREATE INDEX IF NOT EXISTS idx_consent_records_consent_id
    ON consent_records (consent_id);

-- ============================================================================
-- consent_events
-- Immutable audit log of every consent operation.
-- ============================================================================
CREATE TABLE IF NOT EXISTS consent_events (
    id              TEXT PRIMARY KEY,
    creator_id      TEXT NOT NULL,
    consent_id      TEXT,
    event_type      TEXT NOT NULL CHECK (event_type IN ('verify', 'grant', 'revoke', 'block')),
    usage_type      TEXT,
    asset_ref       TEXT,
    requestor_id    TEXT,
    result          TEXT NOT NULL CHECK (result IN ('cleared', 'blocked')),
    reason          TEXT,
    clearance_token TEXT,
    created_at      TEXT NOT NULL DEFAULT (datetime('now'))
);

CREATE INDEX IF NOT EXISTS idx_consent_events_creator
    ON consent_events (creator_id, created_at);

CREATE INDEX IF NOT EXISTS idx_consent_events_token
    ON consent_events (clearance_token);

-- ============================================================================
-- voice_estate
-- Creator identity and royalty configuration.
-- ============================================================================
CREATE TABLE IF NOT EXISTS voice_estate (
    id              TEXT PRIMARY KEY,
    creator_id      TEXT NOT NULL UNIQUE,
    display_name    TEXT NOT NULL,
    hvs_hash        TEXT NOT NULL,
    estate_status   TEXT NOT NULL CHECK (estate_status IN ('active', 'frozen', 'legacy')),
    royalty_rule     TEXT NOT NULL DEFAULT '75_25',
    created_at      TEXT NOT NULL DEFAULT (datetime('now')),
    updated_at      TEXT NOT NULL DEFAULT (datetime('now'))
);

CREATE INDEX IF NOT EXISTS idx_voice_estate_creator
    ON voice_estate (creator_id);

-- ============================================================================
-- Seed: RSP_001 — founding creator
-- ============================================================================
INSERT OR IGNORE INTO voice_estate (id, creator_id, display_name, hvs_hash, estate_status, royalty_rule, created_at, updated_at)
VALUES (
    'vest_00000001',
    'RSP_001',
    'RSP — Founding Creator',
    'hvs_sha256_placeholder_rsp001',
    'active',
    '75_25',
    datetime('now'),
    datetime('now')
);

INSERT OR IGNORE INTO consent_records (id, creator_id, consent_id, status, scope_json, usage_types, exclusions, granted_at, created_at)
VALUES (
    'crec_00000001',
    'RSP_001',
    'consent_rsp001_founding',
    'active',
    '{"scope": "full", "tier": "founding"}',
    '*',
    '[]',
    datetime('now'),
    datetime('now')
);
