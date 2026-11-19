# Autoscaling & Read Replica Topology

Neon decouples Postgres compute (stateless CPU/RAM nodes) from durable storage (Page Servers and cloud object storage).

---

## 1. Autoscaling Mechanics

- **Fractional Compute Units (CUs)**: Scale dynamically between a minimum and maximum CU (e.g. 0.25 CU to 8 CU, where 1 CU = 1 vCPU and 4 GB RAM).
- **Scale to Zero**: Set compute to suspend after an inactivity window (e.g. 5 minutes). When an incoming connection request arrives, Neon wakes the endpoint in ~500ms.
- **Cost Optimization**: Development branches scale to zero when developers are offline, slashing cloud database bills by up to 90%.

---

## 2. Read Replicas & Analytical Queries

Add read replicas to a branch to separate production transactional writes (OLTP) from heavy analytical queries or reporting dashboards:
- Read replicas query the identical storage Page Servers with zero replication delay and zero storage duplication cost.
- Configure dedicated connection strings for read replicas in your ORM or connection pool.
