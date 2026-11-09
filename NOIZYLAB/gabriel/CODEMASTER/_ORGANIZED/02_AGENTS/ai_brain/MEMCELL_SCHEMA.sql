-- MEMCELL_SCHEMA.sql
-- Description: D1 schema. Tables, indexes, views, seed data.

DROP TABLE IF EXISTS users;
DROP TABLE IF EXISTS memories;
DROP TABLE IF EXISTS patterns;
DROP TABLE IF EXISTS logs;
DROP TABLE IF EXISTS graph_nodes;
DROP TABLE IF EXISTS graph_edges;

-- Users
CREATE TABLE users (
    id TEXT PRIMARY KEY,
    name TEXT,
    role TEXT,
    created_at INTEGER
);

-- Memories (The Core)
CREATE TABLE memories (
    id TEXT PRIMARY KEY,
    user_id TEXT,
    content TEXT,
    embedding BLOB, -- Vector data
    tags TEXT,
    importance INTEGER,
    created_at INTEGER,
    FOREIGN KEY(user_id) REFERENCES users(id)
);

-- Patterns (Learned Behaviors)
CREATE TABLE patterns (
    id TEXT PRIMARY KEY,
    signature TEXT,
    confidence REAL,
    frequency INTEGER,
    last_detected INTEGER
);

-- Logs (Audit)
CREATE TABLE logs (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    timestamp INTEGER,
    input TEXT,
    output TEXT
);

-- Graph Nodes (Knowledge Graph)
CREATE TABLE graph_nodes (
    id TEXT PRIMARY KEY,
    type TEXT NOT NULL,
    created INTEGER,
    frequency INTEGER DEFAULT 0,
    properties TEXT, -- JSON
    temporal_start INTEGER,
    temporal_end INTEGER
);

-- Graph Edges (Relationships)
CREATE TABLE graph_edges (
    source TEXT NOT NULL,
    target TEXT NOT NULL,
    relationship TEXT NOT NULL,
    weight REAL DEFAULT 0,
    FOREIGN KEY(source) REFERENCES graph_nodes(id),
    FOREIGN KEY(target) REFERENCES graph_nodes(id),
    PRIMARY KEY(source, target, relationship)
);

-- Indexes for Speed
CREATE INDEX idx_memories_user ON memories(user_id);
CREATE INDEX idx_memories_tags ON memories(tags);
CREATE INDEX idx_patterns_sig ON patterns(signature);

-- Seed Data
INSERT INTO users (id, name, role, created_at) VALUES ('m2ultra', 'MasterUser', 'ADMIN', 1700000000);
INSERT INTO patterns (id, signature, confidence, frequency, last_detected) VALUES ('p_init', 'system_boot', 1.0, 1, 1700000000);
