# Modern Git Branching Models & DAG Strategy Reference

## 1. Trunk-Based Development vs GitFlow

### Trunk-Based Development (Recommended for Modern CI/CD)
- Developers work in short-lived feature branches (< 1-2 days) branched from `main`.
- Continuous integration requires daily integration into `main`.
- High test coverage and fast automated CI prevent trunk breakage.
- Feature flags decouple deployment from release.

### GitFlow (Legacy / Heavy Release Cycles)
- Branches: `main`, `develop`, `feature/*`, `release/*`, `hotfix/*`.
- High merge overhead and long-lived branches risk painful "merge hell".
- Best reserved for scheduled binary packaging (e.g. embedded firmware, mobile app stores).

---

## 2. The Directed Acyclic Graph (DAG) Internals

- **Blobs**: Store file contents (compressed zlib, identified by SHA-1/SHA-256).
- **Trees**: Directories mapping filenames and permissions to Blobs and sub-Trees.
- **Commits**: Pointer to a Tree, parent commit SHAs, author, committer, and message.
- **Fast-Forward**: Occurs when target branch commit is an ancestor of the branch being merged. No merge commit created.

---

## 3. Conflict Resolution Protocol

1. Run `git checkout --conflict=diff3 <file>` to view the 3-way diff (Ancestor, Ours, Theirs).
2. Prefer structural resolution: Keep both non-conflicting imports/routes, isolate the real functional divergence.
3. Validate with unit tests before staging: `pytest` or `npm test`.
4. Stage: `git add <file>` and run `git rebase --continue`.
