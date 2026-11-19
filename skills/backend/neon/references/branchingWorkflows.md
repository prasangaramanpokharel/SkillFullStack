# Database Branching Workflows

Neon's copy-on-write storage engine decouples compute from storage, allowing you to create instantaneous database branches with both schema and data in under 1 second.

---

## 1. How Branching Works

- **Copy-on-Write (CoW)**: Creating a branch does NOT duplicate data blocks on disk. Instead, the child branch points to the parent branch's Page Server blocks at a specific Log Sequence Number (LSN).
- **Zero Storage Overhead**: Storage is only allocated for delta blocks written after the branch is created.
- **Independent Compute**: Each branch has its own isolated compute endpoint with independent connection strings.

---

## 2. CI/CD Preview Environments (GitHub Actions Pattern)

```yaml
name: Ephemeral Database Branch for PR
on:
  pull_request:
    types: [opened, synchronize, closed]

jobs:
  neon-branch:
    runs-on: ubuntu-latest
    steps:
      - name: Create or Reuse Branch
        if: github.event.action != 'closed'
        uses: neondatabase/create-branch-action@v5
        with:
          project_id: ${{ secrets.NEON_PROJECT_ID }}
          branch_name: pr-${{ github.event.number }}
          api_key: ${{ secrets.NEON_API_KEY }}
        id: create-branch

      - name: Run Migrations and Tests
        if: github.event.action != 'closed'
        run: |
          npx prisma migrate deploy
          npm test
        env:
          DATABASE_URL: ${{ steps.create-branch.outputs.db_url }}

      - name: Delete Branch on PR Merge/Close
        if: github.event.action == 'closed'
        run: |
          npx neon branches delete pr-${{ github.event.number }} --project-id ${{ secrets.NEON_PROJECT_ID }}
        env:
          NEON_API_KEY: ${{ secrets.NEON_API_KEY }}
```

---

## 3. Resetting a Branch to Parent LSN
When troubleshooting migrations or re-syncing staging data:
```bash
# Reset dev branch to production's latest state instantaneously
neon branches reset dev --parent main
```
