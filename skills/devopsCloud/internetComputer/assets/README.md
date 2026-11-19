# Internet Computer (ICP) Official Documentation Catalog

This directory contains offline, un-truncated official documentation mirrored from DFINITY's official developer documentation (`github.com/dfinity/developer-docs`) and `skills.internetcomputer.org` for zero-hallucination agent execution.

## Catalog Sitemap

### Getting Started
- [Quickstart Guide](getting-started/quickstart.md): Install `icp-cli` and `ic-wasm`, create a project, and deploy your first canister.
- [Project Structure](getting-started/project-structure.mdx): Understanding `dfx.json`, `icp.yaml`, recipes, and directory conventions.
- [Application Architecture](getting-started/app-architecture.md): Canisters, WebAssembly bytecode, consensus, and frontends.
- [Choose Your Path](getting-started/choose-your-path.md): Selecting languages (Motoko vs Rust), frameworks, and canister roles.

### Languages: Motoko
- [Motoko Overview](languages/motoko/index.md)
- [Base Core Migration](languages/motoko/base-core-migration.md)
- [Motoko Language Manual](languages/motoko/reference/language-manual.md)
- [Style Guide](languages/motoko/reference/style-guide.md)
- [Compiler Reference](languages/motoko/reference/compiler-ref.md)
- [Actors & Orthogonal Persistence](languages/motoko/fundamentals/actors/orthogonal-persistence/overview.md)
- [Candid Serialization](languages/motoko/icp-features/candid-serialization.md)
- [Caller Identification](languages/motoko/icp-features/caller-identification.md)
- [Stable Memory in Motoko](languages/motoko/icp-features/stable-memory.md)

### Languages: Rust
- [Rust Canister Development Guide](languages/rust/index.md): Building canisters with `ic-cdk` and `candid`.
- [Stable Structures](languages/rust/stable-structures.md): High-capacity persistence using `ic-stable-structures` without serialization overhead.
- [Testing Rust Canisters](languages/rust/testing.md): Unit tests and integration workflows with PocketIC.

### Canister Calls & Candid
- [Candid Interface](guides/canister-calls/candid.mdx): Type-safe interface definition language (`.did`) for canisters.
- [Inter-Canister Calls](guides/canister-calls/inter-canister-calls.mdx): Calling other canisters across subnets.
- [Safe Retries & Idempotency](guides/canister-calls/idempotency.md): Preventing double-spend with deduplication keys.

### Backends & Persistence
- [Data Persistence](guides/backends/data-persistence.mdx): Orthogonal persistence vs stable memory.
- [HTTPS Outcalls](guides/backends/https-outcalls.mdx): Direct HTTP requests from canisters to Web2 APIs with consensus.

### Security
- [Canister Security Guidelines](guides/security/overview.md): Reentrancy defense (CallerGuard), anonymous principal rejection, and cycle drain prevention.

### Chain Fusion
- [Bitcoin Integration](guides/chain-fusion/bitcoin.mdx): Direct interaction with Bitcoin (`ckBTC`) without third-party bridges.
- [Ethereum Integration](guides/chain-fusion/ethereum.mdx): Threshold ECDSA and EVM contracts.
