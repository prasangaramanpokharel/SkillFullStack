-- Problematic Schema Missing Primary Key, Incomplete RLS, Cross-Tenant FK, and Foreign Key Indexes
CREATE TABLE bad_orders (
    customer_id BIGINT,
    extra_data TEXT,
    FOREIGN KEY (customer_id) REFERENCES customers(id)
);

CREATE TABLE tbl_items (
    id BIGINT PRIMARY KEY,
    name VARCHAR(255)
);

CREATE TABLE appointments (
    id BIGINT PRIMARY KEY,
    tenant_id UUID NOT NULL,
    doctor_id UUID NOT NULL,
    scheduled_start TIMESTAMPTZ NOT NULL,
    scheduled_end TIMESTAMPTZ NOT NULL,
    FOREIGN KEY (doctor_id) REFERENCES doctors(id)
);

-- RLS enabled but lacking any CREATE POLICY definition
ALTER TABLE bad_orders ENABLE ROW LEVEL SECURITY;
