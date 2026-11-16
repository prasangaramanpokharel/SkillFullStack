# GitHub Actions Production Workflow Patterns

## 1. Automated Release & Tagging Workflow (`release.yml`)

```yaml
name: Release & Tagging

on:
  push:
    branches: [main]

permissions:
  contents: write
  pull-requests: write

jobs:
  release:
    runs-on: ubuntu-latest
    timeout-minutes: 15
    steps:
      - name: Checkout
        uses: actions/checkout@11bd71901bbe5b1630ceea73d27597364c9af683
        with:
          fetch-depth: 0

      - name: Setup Node.js
        uses: actions/setup-node@39370e3970a6d050c480ffad4ff0ed4d3fdee5af
        with:
          node-version: 22

      - name: Run Semantic Release
        env:
          GITHUB_TOKEN: ${{ secrets.GITHUB_TOKEN }}
        run: npx semantic-release
```

---

## 2. Docker Build & Push with Multi-Platform & Cache (`docker.yml`)

```yaml
name: Docker Build & Push

on:
  push:
    tags: ['v*']

permissions:
  contents: read
  packages: write

jobs:
  docker:
    runs-on: ubuntu-latest
    timeout-minutes: 20
    steps:
      - name: Checkout
        uses: actions/checkout@11bd71901bbe5b1630ceea73d27597364c9af683

      - name: Set up QEMU
        uses: docker/setup-qemu-action@49b3bc8e6bdd4480e8226f5bfdd1b22f29821c29

      - name: Set up Docker Buildx
        uses: docker/setup-buildx-action@c47758b77c9736f4b2ef4073d4d51994fabfe349

      - name: Login to GitHub Container Registry
        uses: docker/login-action@9780b0c442fbb1117ed29e0efdff1e18412f7567
        with:
          registry: ghcr.io
          username: ${{ github.actor }}
          password: ${{ secrets.GITHUB_TOKEN }}

      - name: Build & Push
        uses: docker/build-push-action@4f58ea79222b3b150c8844d69901d7071a2322e4
        with:
          context: .
          push: true
          tags: ghcr.io/${{ github.repository }}:${{ github.ref_name }}
          cache-from: type=gha
          cache-to: type=gha,mode=max
```
