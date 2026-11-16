-- Production Grade Valid Schema
CREATE TABLE customers (
    id BIGINT PRIMARY KEY,
    tenant_id UUID NOT NULL,
    email VARCHAR(255) NOT NULL,
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    CONSTRAINT uq_customers_tenant_email UNIQUE (tenant_id, email),
    CONSTRAINT uq_customers_tenant_id UNIQUE (tenant_id, id)
);

CREATE TABLE orders (
    id BIGINT PRIMARY KEY,
    tenant_id UUID NOT NULL,
    customer_id BIGINT NOT NULL,
    status VARCHAR(50) NOT NULL CHECK (status IN ('pending', 'paid', 'shipped', 'cancelled')),
    total_amount NUMERIC(12, 2) NOT NULL CHECK (total_amount >= 0),
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    CONSTRAINT fk_orders_customer FOREIGN KEY (tenant_id, customer_id) REFERENCES customers(tenant_id, id) ON DELETE RESTRICT,
    CONSTRAINT uq_orders_tenant_id UNIQUE (tenant_id, id)
);

-- Supporting composite index for Foreign Key
CREATE INDEX idx_orders_customer_composite ON orders (tenant_id, customer_id);
-- Composite index for tenant filtering and sorting
CREATE INDEX idx_orders_tenant_status ON orders (tenant_id, status, created_at);

ALTER TABLE customers ENABLE ROW LEVEL SECURITY;
ALTER TABLE customers FORCE ROW LEVEL SECURITY;
CREATE POLICY rls_customers ON customers FOR ALL
    USING (tenant_id = NULLIF(current_setting('app.current_tenant_id', true), '')::UUID)
    WITH CHECK (tenant_id = NULLIF(current_setting('app.current_tenant_id', true), '')::UUID);

ALTER TABLE orders ENABLE ROW LEVEL SECURITY;
ALTER TABLE orders FORCE ROW LEVEL SECURITY;
CREATE POLICY rls_orders ON orders FOR ALL
    USING (tenant_id = NULLIF(current_setting('app.current_tenant_id', true), '')::UUID)
    WITH CHECK (tenant_id = NULLIF(current_setting('app.current_tenant_id', true), '')::UUID);
