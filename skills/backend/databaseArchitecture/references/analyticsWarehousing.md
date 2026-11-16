# Analytical Data Architecture & Dimensional Modeling Reference

---

## 1. OLTP vs. OLAP Paradigms

```
OLTP (Online Transaction Processing)
├── Normalized schemas (3NF / BCNF)
├── High-frequency small transactions (Row-based storage)
└── Goal: Low latency point writes and reads (< 10ms)

OLAP (Online Analytical Processing)
├── Dimensional schemas (Star / Snowflake)
├── Batch or stream ingestion (Columnar storage: ClickHouse, DuckDB, BigQuery)
└── Goal: High-throughput aggregate scans over millions/billions of records
```

---

## 2. Dimensional Modeling: Star Schema

- **Fact Tables**: Contain quantitative measurements, metrics, and foreign keys to dimensions (e.g. `fact_sales`: `order_id`, `customer_key`, `date_key`, `amount_sold`, `discount_amount`).
- **Dimension Tables**: Contain contextual, descriptive attributes (e.g. `dim_customer`: `customer_key`, `name`, `tier`, `country`, `segment`).

---

## 3. Slowly Changing Dimensions (SCD)

- **SCD Type 1 (Overwrite)**: Overwrite historical value with new value. History is lost.
- **SCD Type 2 (Add New Row - Recommended)**: Add new record with validity date ranges (`valid_from`, `valid_to`, `is_current`). Full historical tracking.
- **SCD Type 3 (Add Previous Value Column)**: Store `current_tier` and `previous_tier` in the same row. Limited history.
