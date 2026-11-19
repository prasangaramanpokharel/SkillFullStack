# Git Directed Acyclic Graph (DAG) & Object Model Internals

Git is fundamentally a content-addressable storage filesystem structured as a **Directed Acyclic Graph (DAG)** of immutable objects.

---

## 1. The Four Core Git Object Types

Every object in Git is identified by the SHA-1 or SHA-256 hash of its header and compressed payload:

| Object Type | Role | Content |
| :--- | :--- | :--- |
| **Blob** | Raw file contents | File payload (no metadata, no filename, no permissions) |
| **Tree** | Directory structure | Array of SHA hashes, file modes, and filenames pointing to blobs or subtrees |
| **Commit** | Point-in-time snapshot | Tree SHA, parent commit SHA(s), author/committer timestamps, commit message |
| **Annotated Tag** | Immutable release marker | Object SHA, tagger, date, GPG signature, tag message |

```
Commit Object (SHA: 8f3a1...)
├── tree: 4c2b9... (Root Directory)
│   ├── 100644 blob e69de... README.md
│   └── 040000 tree 9a1d3... src/
│       └── 100644 blob 3b184... index.ts
├── parent: 1e5f8... (Previous Commit)
├── author: Dev <dev@example.com> 1731750000 +0000
└── message: "feat: add user authentication"
```

---

## 2. DAG Mechanics & Branch Pointers

1. **Branches are just mutable pointers**: A branch in Git (e.g., `main`, `feature/auth`) is simply a 41-byte text file located in `.git/refs/heads/<branch>` containing the 40-character commit hash it currently points to.
2. **HEAD**: A reference pointer (`.git/HEAD`) pointing to the currently active branch or a detached commit.
3. **Immutability of History**: When you rebase or amend, Git **does not mutate** existing commit objects; it creates new commit objects with different parent pointers. The old commits remain in the DAG until garbage collected (`git gc`).
4. **Reflog (`git reflog`)**: A local audit ledger of every update to `HEAD` and branch tips over the past 30-90 days, enabling recovery of orphaned commits after destructive operations (`git reset --hard`).

---

## 3. Fast-Forward vs Three-Way Merge DAGs

### Fast-Forward (`git merge --ff`)
Moves the branch pointer forward along the direct linear ancestor chain. Zero new commit objects created.
```
main: A ─── B
             \
feature:      C ─── D

Result: A ─── B ─── C ─── D (main, feature)
```

### Three-Way Merge (`git merge --no-ff`)
Creates a new merge commit object with **two parent pointers** (`parent1` = main tip, `parent2` = feature tip).
```
main: A ─── B ───────── M (Merge Commit: parents B, D)
             \         /
feature:      C ─── D /
```

---

## 4. Rebase Internals (`git rebase`)

Rebase unplugs a branch's commits from their original fork point and replays each commit as a brand new patch onto the target upstream tip:
```
Original:
A ─── B ─── C (main)
       \
        D ─── E (feature)

After `git rebase main`:
A ─── B ─── C (main)
             \
              D' ─── E' (feature: new commit hashes!)
```
