#!/usr/bin/env python3
"""
Skill Scaffolding Utility
Creates a spec-compliant, high-density Agent Skill adhering to the Agent Skills standard.
"""

import os
import sys
import json
import argparse
from datetime import datetime

VALID_TAXONOMIES = [
    "foundation",
    "frontend",
    "backend",
    "dataAi",
    "devopsCloud",
    "securityQa",
    "github",
    "softwareDevelopment",
    "architectureDesign",
    "gitVersionControl",
    "testing",
    "staticChecking",
    "softwareSecurity",
    "qualityMetrics",
    "cicdDevops",
    "maintenanceEvolution",
    "teamProject"
]

def scaffold_skill(taxonomy: str, name: str, description: str, version: str = "latest", docs_url: str = ""):
    if taxonomy not in VALID_TAXONOMIES:
        print(f"Error: Invalid taxonomy '{taxonomy}'. Choose from: {', '.join(VALID_TAXONOMIES)}")
        sys.exit(1)

    skill_dir = os.path.join("skills", taxonomy, name)
    if os.path.exists(skill_dir):
        print(f"Error: Skill '{name}' already exists at {skill_dir}")
        sys.exit(1)

    # Create directory structure
    for subdir in ["scripts", "references", "assets", "evals"]:
        os.makedirs(os.path.join(skill_dir, subdir), exist_ok=True)

    today = datetime.now().strftime("%Y-%m-%d")
    title = name.replace("-", " ").title()

    skill_md = f"""---
name: {name}
description: {description}
version: {version}
last-verified: {today}
---

# {title}

## Overview & Scope
High-leverage, battle-tested patterns for {title}. Verified against current official releases.

## Core Rules & Modern Patterns
1. Apply current idiomatic patterns (avoiding legacy/deprecated methods).
2. Keep prompt context ultra-compact; offload verbose specs to `references/`.
3. Use deterministic CLI commands and automation scripts where applicable.

## Anti-Patterns & Common Traps
- ❌ **Outdated APIs**: Do not use deprecated packages or obsolete syntax.
- ❌ **Context Bloat**: Do not dump entire manuals into prompt responses.
- ✅ **Canonical Solution**: Focus directly on high-yield, maintainable code.

## References
- Official Documentation: {docs_url or "Verified via latest web documentation."}
- See [references/api-reference.md](references/api-reference.md) for detailed signatures.
"""

    with open(os.path.join(skill_dir, "SKILL.md"), "w", encoding="utf-8") as f:
        f.write(skill_md)

    with open(os.path.join(skill_dir, "references", "apiReference.md"), "w", encoding="utf-8") as f:
        f.write(f"# {title} Reference\n\nOfficial docs: {docs_url or 'N/A'}\n")

    # Update catalog
    catalog_path = os.path.join(".skillsRegistry", "catalog.json")
    catalog = {"skills": []}
    if os.path.exists(catalog_path):
        try:
            with open(catalog_path, "r", encoding="utf-8") as f:
                catalog = json.load(f)
        except Exception:
            catalog = {"skills": []}

    catalog["skills"].append({
        "name": name,
        "taxonomy": taxonomy,
        "path": skill_dir,
        "description": description,
        "version": version,
        "docs": docs_url,
        "verified_date": today,
        "commands": [f"/{name}-action"]
    })

    with open(catalog_path, "w", encoding="utf-8") as f:
        json.dump(catalog, f, indent=2)

    print(f" Successfully scaffolded {name} in {skill_dir}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Scaffold an agent skill")
    parser.add_argument("--taxonomy", required=True, choices=VALID_TAXONOMIES, help="Skill domain")
    parser.add_argument("--name", required=True, help="Skill identifier (kebab-case)")
    parser.add_argument("--description", required=True, help="Use-when criteria and summary")
    parser.add_argument("--version", default="latest", help="Package/tool version")
    parser.add_argument("--docs", default="", help="Official documentation URL")

    args = parser.parse_args()
    scaffold_skill(args.taxonomy, args.name, args.description, args.version, args.docs)
