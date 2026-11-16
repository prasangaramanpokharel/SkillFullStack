-- Safe Zero Downtime Expand Migration
ALTER TABLE orders ADD COLUMN fulfillment_status VARCHAR(50) NULL;
CREATE INDEX CONCURRENTLY idx_orders_fulfillment ON orders (fulfillment_status);
