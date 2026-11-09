-- GABRIEL MemCell D1 Schema
-- ═══════════════════════════════════════════════════════════════
-- Persistent memory for GABRIEL Workers AI Controller
-- ═══════════════════════════════════════════════════════════════

-- Memories table - Stores knowledge, patterns, facts
CREATE TABLE IF NOT EXISTS memories (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    content TEXT NOT NULL,
    category TEXT NOT NULL CHECK(category IN ('pattern', 'fact', 'preference', 'instruction', 'episodic')),
    tags TEXT,
    embedding BLOB,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    accessed_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    access_count INTEGER DEFAULT 0
);

-- Batches table - Tracks batch inference jobs
CREATE TABLE IF NOT EXISTS batches (
    id TEXT PRIMARY KEY,
    task_count INTEGER NOT NULL,
    status TEXT NOT NULL CHECK(status IN ('queued', 'running', 'completed', 'failed')),
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    completed_at DATETIME
);

-- Batch Results table - Stores individual task results
CREATE TABLE IF NOT EXISTS batch_results (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    batch_id TEXT NOT NULL REFERENCES batches(id),
    task_id TEXT NOT NULL,
    result TEXT,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    UNIQUE(batch_id, task_id)
);

-- Conversations table - Episodic memory for chat history
CREATE TABLE IF NOT EXISTS conversations (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    session_id TEXT NOT NULL,
    role TEXT NOT NULL CHECK(role IN ('system', 'user', 'assistant', 'tool')),
    content TEXT NOT NULL,
    tool_calls TEXT,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP
);

-- Tool Executions table - Track tool usage patterns
CREATE TABLE IF NOT EXISTS tool_executions (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    tool_name TEXT NOT NULL,
    arguments TEXT,
    result TEXT,
    success INTEGER DEFAULT 1,
    execution_time_ms INTEGER,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP
);

-- Patterns table - Store learned patterns from ekkOS
CREATE TABLE IF NOT EXISTS patterns (
    id TEXT PRIMARY KEY,
    title TEXT NOT NULL,
    description TEXT,
    solution TEXT,
    confidence REAL DEFAULT 0.5,
    usage_count INTEGER DEFAULT 0,
    success_count INTEGER DEFAULT 0,
    tags TEXT,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    updated_at DATETIME DEFAULT CURRENT_TIMESTAMP
);

-- Directives table - User preferences and rules
CREATE TABLE IF NOT EXISTS directives (
    id TEXT PRIMARY KEY,
    type TEXT NOT NULL CHECK(type IN ('MUST', 'NEVER', 'PREFER', 'AVOID')),
    content TEXT NOT NULL,
    context TEXT,
    priority INTEGER DEFAULT 5,
    active INTEGER DEFAULT 1,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP
);

-- HP-OMEN Bridge Status - Track remote machine state
CREATE TABLE IF NOT EXISTS hp_omen_status (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    hostname TEXT,
    ip_address TEXT,
    vpn_ip TEXT,
    status TEXT CHECK(status IN ('online', 'offline', 'unknown')),
    last_ping_ms INTEGER,
    last_seen DATETIME,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP
);

-- Indexes for performance
CREATE INDEX IF NOT EXISTS idx_memories_category ON memories(category);
CREATE INDEX IF NOT EXISTS idx_memories_tags ON memories(tags);
CREATE INDEX IF NOT EXISTS idx_memories_created ON memories(created_at);
CREATE INDEX IF NOT EXISTS idx_batch_results_batch ON batch_results(batch_id);
CREATE INDEX IF NOT EXISTS idx_conversations_session ON conversations(session_id);
CREATE INDEX IF NOT EXISTS idx_conversations_created ON conversations(created_at);
CREATE INDEX IF NOT EXISTS idx_tool_executions_name ON tool_executions(tool_name);
CREATE INDEX IF NOT EXISTS idx_patterns_tags ON patterns(tags);
CREATE INDEX IF NOT EXISTS idx_directives_type ON directives(type);

-- Full-text search for memories
CREATE VIRTUAL TABLE IF NOT EXISTS memories_fts USING fts5(
    content,
    tags,
    content='memories',
    content_rowid='id'
);

-- Triggers to keep FTS in sync
CREATE TRIGGER IF NOT EXISTS memories_ai AFTER INSERT ON memories BEGIN
    INSERT INTO memories_fts(rowid, content, tags) VALUES (NEW.id, NEW.content, NEW.tags);
END;

CREATE TRIGGER IF NOT EXISTS memories_ad AFTER DELETE ON memories BEGIN
    INSERT INTO memories_fts(memories_fts, rowid, content, tags) VALUES('delete', OLD.id, OLD.content, OLD.tags);
END;

CREATE TRIGGER IF NOT EXISTS memories_au AFTER UPDATE ON memories BEGIN
    INSERT INTO memories_fts(memories_fts, rowid, content, tags) VALUES('delete', OLD.id, OLD.content, OLD.tags);
    INSERT INTO memories_fts(rowid, content, tags) VALUES (NEW.id, NEW.content, NEW.tags);
END;
