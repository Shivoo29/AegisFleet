CREATE TABLE IF NOT EXISTS events (
  id TEXT PRIMARY KEY, paypal_event_id TEXT UNIQUE, type TEXT NOT NULL, source TEXT NOT NULL,
  subject_id TEXT NOT NULL, data JSONB NOT NULL, verified BOOLEAN NOT NULL DEFAULT false,
  rejected BOOLEAN NOT NULL DEFAULT false, received_at TIMESTAMPTZ NOT NULL DEFAULT now());
CREATE TABLE IF NOT EXISTS ledger (
  id BIGSERIAL PRIMARY KEY, kind TEXT NOT NULL, subject_id TEXT NOT NULL, summary TEXT NOT NULL,
  payload JSONB NOT NULL, prev_hash TEXT NOT NULL, hash TEXT NOT NULL,
  created_at TIMESTAMPTZ NOT NULL DEFAULT now());
CREATE TABLE IF NOT EXISTS approvals (
  id TEXT PRIMARY KEY, agent TEXT, tool TEXT, args JSONB, reason TEXT, summary TEXT,
  amount_cents BIGINT, currency TEXT, status TEXT NOT NULL DEFAULT 'pending',
  decided_by TEXT, decided_at TIMESTAMPTZ, created_at TIMESTAMPTZ NOT NULL DEFAULT now());
CREATE TABLE IF NOT EXISTS budgets (
  agent TEXT, tool TEXT, subject_id TEXT, window_start DATE, count INT NOT NULL DEFAULT 0,
  amount_cents BIGINT NOT NULL DEFAULT 0, PRIMARY KEY (agent, tool, subject_id, window_start));
CREATE TABLE IF NOT EXISTS agent_runs (
  id TEXT PRIMARY KEY, agent TEXT, event_id TEXT, event_type TEXT, status TEXT,
  steps JSONB NOT NULL DEFAULT '[]', output JSONB, started_at TIMESTAMPTZ DEFAULT now(), finished_at TIMESTAMPTZ);
CREATE TABLE IF NOT EXISTS invoices (id TEXT PRIMARY KEY, data JSONB NOT NULL, updated_at TIMESTAMPTZ DEFAULT now());
CREATE TABLE IF NOT EXISTS shipments (id TEXT PRIMARY KEY, data JSONB NOT NULL, updated_at TIMESTAMPTZ DEFAULT now());
CREATE TABLE IF NOT EXISTS settings (key TEXT PRIMARY KEY, value TEXT NOT NULL);