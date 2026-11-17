#!/usr/bin/env python3
"""
Astro Production Architecture & Best Practices Auditor
Validates Astro 5.x projects for:
- Island hydration directives optimization
- Server island fallback implementations
- Image optimization via astro:assets
- Content collection definitions
"""

import sys
import os
import re
from pathlib import Path

def audit_file(filepath: Path):
    issues = []
    content = filepath.read_text(encoding="utf-8", errors="ignore")
    rel_path = filepath.name

    # 1. Check for unoptimized <img> tags
    if filepath.suffix in [".astro", ".mdx", ".tsx", ".jsx", ".vue", ".svelte"]:
        raw_img_matches = re.findall(r'<img\s+[^>]*src=[^>]*>', content)
        for match in raw_img_matches:
            if "astro:assets" not in content and "alt=" in match:
                issues.append(f"[{rel_path}] Found raw <img> tag. Prefer `<Image />` from 'astro:assets' for automated AVIF/WebP conversion and CLS prevention.")

    # 2. Check for over-eager hydration (client:load on carousels or comments)
    if filepath.suffix == ".astro":
        eager_hydration = re.findall(r'<([A-Z][a-zA-Z0-9]+)[^>]*client:load[^>]*>', content)
        for comp in eager_hydration:
            comp_lower = comp.lower()
            if any(term in comp_lower for term in ["carousel", "comment", "review", "footer", "modal", "drawer"]):
                issues.append(f"[{rel_path}] Eager hydration `client:load` detected on `<{comp}>`. Consider `client:visible` or `client:idle` to eliminate TTI lockup.")

        # 3. Check for server:defer missing fallback
        if "server:defer" in content and "slot=\"fallback\"" not in content:
            issues.append(f"[{rel_path}] Server Island `server:defer` detected without a designated `slot=\"fallback\"` component.")

    return issues

def audit_directory(root_dir: str):
    root = Path(root_dir)
    print(f"🚀 Scanning Astro project at: {root.resolve()}")
    all_issues = []

    src_dir = root / "src"
    if not src_dir.exists():
        print(f"⚠️  No 'src' directory found at {root}. Running in standalone mode.")
        src_dir = root

    for ext in ["*.astro", "*.tsx", "*.jsx", "*.svelte", "*.vue", "*.mdx"]:
        for file in src_dir.rglob(ext):
            issues = audit_file(file)
            all_issues.extend(issues)

    # Check for content configuration
    has_astro5_content = (root / "src" / "content.config.ts").exists()
    has_astro4_content = (root / "src" / "content" / "config.ts").exists()
    if not has_astro5_content and not has_astro4_content and (root / "src" / "content").exists():
        all_issues.append("No Content Collections schema file found (`src/content.config.ts` or `src/content/config.ts`).")

    print("\n" + "=" * 60)
    print("📋 ASTRO PRODUCTION AUDIT REPORT")
    print("=" * 60)
    if not all_issues:
        print("✅ No Astro architectural anti-patterns detected! Production ready.")
        return 0
    else:
        print(f"⚠️  Found {len(all_issues)} architectural suggestion(s):")
        for idx, issue in enumerate(all_issues, 1):
            print(f"  {idx}. {issue}")
        print("=" * 60)
        return 1

if __name__ == "__main__":
    target = sys.argv[1] if len(sys.argv) > 1 else "."
    sys.exit(audit_directory(target))
