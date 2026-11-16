-- Dangerous Breaking Migration (Exclusive Locks & Immediate Downtime)
ALTER TABLE orders DROP COLUMN old_notes;
ALTER TABLE orders RENAME COLUMN status TO order_state;
CREATE INDEX idx_blocking ON orders (created_at);
