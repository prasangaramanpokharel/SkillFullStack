#!/usr/bin/env python3
"""
SkillFullStack / Skills Repository — Professional Quality & Consistency Validator
Validates every skill in the repository against strict Agent Skills and AGENTS.md standards.

Usage:
    python3 scripts/validateSkills.py [--strict] [--skill NAME] [--taxonomy TAX] [--json]

Exit codes:
    0 = All skills passed validation
    1 = Validation errors detected
"""

import os
import sys
import re
import json
import argparse
from datetime import datetime
from pathlib import Path

# ANSI colors for beautiful terminal output
class Colors:
    RESET = "\033[0m"
    BOLD = "\033[1m"
    DIM = "\033[2m"
    RED = "\033[31m"
    GREEN = "\033[32m"
    YELLOW = "\033[33m"
    BLUE = "\033[34m"
    MAGENTA = "\033[35m"
    CYAN = "\033[36m"
    WHITE = "\033[37m"
    GRAY = "\033[90m"

VALID_TAXONOMIES = [
    "foundation",
    "frontend",
    "design",
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
    "teamProject",
]

class SkillValidator:
    def __init__(self, repo_root: Path, strict: bool = False):
        self.repo_root = repo_root
        self.strict = strict
        self.catalog = self._load_catalog()
        self.results = {}
        self.total_errors = 0
        self.total_warnings = 0

    def _load_catalog(self):
        catalog_file = self.repo_root / ".skillsRegistry" / "catalog.json"
        if not catalog_file.exists():
            return {"skills": []}
        try:
            with open(catalog_file, "r", encoding="utf-8") as f:
                return json.load(f)
        except Exception as e:
            print(f"{Colors.RED}Failed to load catalog.json: {e}{Colors.RESET}")
            return {"skills": []}

    def validate_all(self, target_skill: str = None, target_taxonomy: str = None):
        skills_dir = self.repo_root / "skills"
        if not skills_dir.exists():
            print(f"{Colors.RED}Error: 'skills' directory not found in {self.repo_root}{Colors.RESET}")
            return False

        skill_dirs = []
        for tax_dir in sorted(skills_dir.iterdir()):
            if tax_dir.is_dir() and not tax_dir.name.startswith("."):
                if target_taxonomy and tax_dir.name != target_taxonomy:
                    continue
                for sdir in sorted(tax_dir.iterdir()):
                    if sdir.is_dir() and (sdir / "SKILL.md").exists():
                        if target_skill and sdir.name != target_skill:
                            continue
                        skill_dirs.append(sdir)

        print(f"\n{Colors.BOLD}{Colors.CYAN}══════════════════════════════════════════════════════════════════════════{Colors.RESET}")
        print(f"{Colors.BOLD}{Colors.CYAN} 🛡️   AGENT SKILLS PRODUCTION CONSISTENCY VALIDATOR{Colors.RESET}")
        print(f"{Colors.BOLD}{Colors.CYAN}══════════════════════════════════════════════════════════════════════════{Colors.RESET}")
        print(f"{Colors.GRAY}Scanning {len(skill_dirs)} skill(s) across taxonomy directories...{Colors.RESET}\n")

        for sdir in skill_dirs:
            self._validate_skill(sdir)

        self._validate_catalog_completeness(skill_dirs)
        return self._render_summary()

    def _validate_skill(self, sdir: Path):
        skill_name = sdir.name
        taxonomy = sdir.parent.name
        skill_file = sdir / "SKILL.md"

        errors = []
        warnings = []
        metrics = {
            "name": skill_name,
            "taxonomy": taxonomy,
            "path": str(sdir.relative_to(self.repo_root)),
            "char_count": 0,
            "slash_commands": [],
            "assets_count": 0,
            "references_count": 0,
            "has_evals": False,
        }

        # 1. Directory & Taxonomy Check
        if taxonomy not in VALID_TAXONOMIES:
            errors.append(f"Invalid taxonomy '{taxonomy}'. Must be one of: {', '.join(VALID_TAXONOMIES)}")

        # 2. SKILL.md Content & Frontmatter Checks
        try:
            content = skill_file.read_text(encoding="utf-8")
        except Exception as e:
            errors.append(f"Cannot read SKILL.md: {e}")
            self.results[skill_name] = {"errors": errors, "warnings": warnings, "metrics": metrics}
            return

        metrics["char_count"] = len(content)
        if len(content) < 1200:
            warnings.append(f"SKILL.md is short ({len(content)} chars). Expected comprehensive documentation.")

        # Check frontmatter
        fm_match = re.match(r"^---\n(.*?)\n---\n", content, re.DOTALL)
        if not fm_match:
            errors.append("Missing valid YAML frontmatter delimiters (`---`).")
        else:
            fm_text = fm_match.group(1)

            # Name check
            name_m = re.search(r"^name:\s*(.+)$", fm_text, re.MULTILINE)
            if not name_m:
                errors.append("Missing 'name' field in frontmatter.")
            else:
                parsed_name = name_m.group(1).strip()
                if parsed_name != skill_name:
                    errors.append(f"Frontmatter name '{parsed_name}' does not match directory name '{skill_name}'.")

            # Description check
            desc_m = re.search(r"^description:\s*(.+)$", fm_text, re.MULTILINE)
            if not desc_m:
                errors.append("Missing 'description' in frontmatter.")
            elif len(desc_m.group(1).strip()) < 25:
                warnings.append("Description is brief. Provide high-density 'use when' criteria.")

            # Version check
            ver_m = re.search(r"^version:\s*(.+)$", fm_text, re.MULTILINE)
            if not ver_m:
                warnings.append("Missing 'version' in frontmatter.")

            # Last verified check
            lv_m = re.search(r"^last-verified:\s*(.+)$", fm_text, re.MULTILINE)
            if not lv_m:
                warnings.append("Missing 'last-verified' date in frontmatter.")
            else:
                date_str = lv_m.group(1).strip()
                try:
                    datetime.strptime(date_str, "%Y-%m-%d")
                except ValueError:
                    warnings.append(f"Invalid date format in 'last-verified' ('{date_str}'). Expected YYYY-MM-DD.")

            # Slash commands check
            if "slash-commands:" not in fm_text:
                warnings.append("No slash-commands defined in frontmatter.")
            else:
                cmds = re.findall(r"command:\s*(/[a-zA-Z0-9_-]+)", fm_text)
                metrics["slash_commands"] = cmds
                if not cmds:
                    warnings.append("'slash-commands' block exists but no valid commands parsed.")

        # 3. Heading & Section Structure
        if not re.search(r"^#\s+.+", content, re.MULTILINE):
            errors.append("Missing main `# Title` H1 heading in SKILL.md.")

        h2_headings = re.findall(r"^##\s+(.+)$", content, re.MULTILINE)
        if len(h2_headings) < 3:
            warnings.append(f"Only {len(h2_headings)} H2 section(s) found. Expected structured sections.")

        # Anti-patterns section check
        has_anti_patterns = any(
            re.search(term, content, re.IGNORECASE) for term in ["anti-pattern", "traps", "common mistake", "gotchas", "pitfalls"]
        )
        if not has_anti_patterns:
            warnings.append("Missing explicit 'Anti-Patterns / Common Mistakes' section in SKILL.md.")

        # Placeholder checks
        if "<!-- Content after this section is automatically generated -->" in content:
            errors.append("Detected OpenAPI build stub placeholder. Replace with full content.")
        if "TODO" in content:
            warnings.append("Detected 'TODO' marker in SKILL.md.")

        # 4. Link & Asset Resolution Checks
        links = re.findall(r'\[([^\]]+)\]\(([^)]+)\)', content)
        for text, link in links:
            if link.startswith("http://") or link.startswith("https://") or link.startswith("#") or link.startswith("mailto:"):
                continue
            if link.startswith("file:///"):
                errors.append(f"Hardcoded local absolute path detected in link [{text}]({link}). Use relative paths.")
                continue

            target_clean = link.split("#")[0]
            if target_clean:
                target_path = sdir / target_clean
                if not target_path.exists():
                    errors.append(f"Broken relative link: [{text}]({link}) -> File not found.")

        # 5. Offline Assets & References
        assets_dir = sdir / "assets"
        if assets_dir.exists() and assets_dir.is_dir():
            asset_files = list(assets_dir.rglob("*.md"))
            metrics["assets_count"] = len(asset_files)
            if not (assets_dir / "README.md").exists():
                warnings.append("`assets/` directory exists but is missing `assets/README.md` navigation sitemap.")

        refs_dir = sdir / "references"
        if refs_dir.exists() and refs_dir.is_dir():
            ref_files = list(refs_dir.rglob("*.md"))
            metrics["references_count"] = len(ref_files)
            if not ref_files:
                warnings.append("`references/` directory exists but contains no markdown files.")

        evals_dir = sdir / "evals"
        if evals_dir.exists() and evals_dir.is_dir():
            eval_files = list(evals_dir.glob("*.json")) + list(evals_dir.glob("*.py"))
            metrics["has_evals"] = len(eval_files) > 0

        # 6. Catalog Parity Check
        catalog_entry = next((s for s in self.catalog.get("skills", []) if s.get("name") == skill_name), None)
        if not catalog_entry:
            errors.append(f"Skill '{skill_name}' is not registered in `.skillsRegistry/catalog.json`.")
        else:
            if catalog_entry.get("taxonomy") != taxonomy:
                errors.append(f"Taxonomy mismatch in catalog.json: '{catalog_entry.get('taxonomy')}' vs disk '{taxonomy}'.")
            expected_path = f"skills/{taxonomy}/{skill_name}"
            if catalog_entry.get("path") != expected_path:
                warnings.append(f"Path mismatch in catalog.json: '{catalog_entry.get('path')}' vs '{expected_path}'.")

        self.total_errors += len(errors)
        self.total_warnings += len(warnings)
        self.results[skill_name] = {"errors": errors, "warnings": warnings, "metrics": metrics}

    def _validate_catalog_completeness(self, scanned_dirs):
        scanned_names = {d.name for d in scanned_dirs}
        for entry in self.catalog.get("skills", []):
            name = entry.get("name")
            if name not in scanned_names:
                self.total_errors += 1
                if name not in self.results:
                    self.results[name] = {"errors": [], "warnings": [], "metrics": {}}
                self.results[name]["errors"].append(f"Registered in catalog.json but directory '{entry.get('path')}' does not exist on disk.")

    def _render_summary(self):
        total_skills = len(self.results)
        passed_clean = 0
        passed_with_warnings = 0
        failed = 0

        for name, res in sorted(self.results.items()):
            errs = res["errors"]
            warns = res["warnings"]
            m = res.get("metrics", {})

            if errs:
                failed += 1
                status_icon = f"{Colors.RED}❌ FAIL{Colors.RESET}"
            elif warns:
                passed_with_warnings += 1
                status_icon = f"{Colors.YELLOW}⚠️  WARN{Colors.RESET}"
            else:
                passed_clean += 1
                status_icon = f"{Colors.GREEN}✅ PASS{Colors.RESET}"

            cmds_info = f"{len(m.get('slash_commands', []))} cmds" if m.get("slash_commands") else "no cmds"
            assets_info = f"{m.get('assets_count', 0)} assets" if m.get("assets_count") else "0 assets"
            refs_info = f"{m.get('references_count', 0)} refs"

            print(f" {status_icon}  {Colors.BOLD}{name.ljust(26)}{Colors.RESET} {Colors.GRAY}[{m.get('taxonomy', 'unknown')}] ({cmds_info}, {refs_info}, {assets_info}){Colors.RESET}")

            for err in errs:
                print(f"      {Colors.RED}✗ ERROR:{Colors.RESET} {err}")
            for warn in warns:
                print(f"      {Colors.YELLOW}▲ WARN:{Colors.RESET}  {warn}")

        print(f"\n{Colors.BOLD}{Colors.CYAN}══════════════════════════════════════════════════════════════════════════{Colors.RESET}")
        print(f"{Colors.BOLD} AUDIT REPORT SUMMARY{Colors.RESET}")
        print(f"{Colors.BOLD}{Colors.CYAN}══════════════════════════════════════════════════════════════════════════{Colors.RESET}")
        print(f"  Total Skills Audited:  {Colors.BOLD}{total_skills}{Colors.RESET}")
        print(f"  Passed Cleanly:        {Colors.GREEN}{Colors.BOLD}{passed_clean}{Colors.RESET}")
        print(f"  Passed with Warnings:  {Colors.YELLOW}{Colors.BOLD}{passed_with_warnings}{Colors.RESET}")
        print(f"  Failed:                {Colors.RED}{Colors.BOLD}{failed}{Colors.RESET}")
        print(f"  Total Errors:          {Colors.RED if self.total_errors else Colors.GREEN}{self.total_errors}{Colors.RESET}")
        print(f"  Total Warnings:        {Colors.YELLOW if self.total_warnings else Colors.GREEN}{self.total_warnings}{Colors.RESET}")

        score = max(0, 100 - (self.total_errors * 5) - (self.total_warnings * 1))
        score_color = Colors.GREEN if score >= 90 else (Colors.YELLOW if score >= 75 else Colors.RED)
        print(f"  Overall Repository Quality Score: {score_color}{Colors.BOLD}{score}/100{Colors.RESET}\n")

        if self.total_errors > 0 or (self.strict and self.total_warnings > 0):
            print(f"{Colors.RED}{Colors.BOLD}Validation failed! Address the issues above before publishing.{Colors.RESET}\n")
            return False
        else:
            print(f"{Colors.GREEN}{Colors.BOLD}All validation checks passed! Repository meets professional Agent Skills standards.{Colors.RESET}\n")
            return True

def main():
    parser = argparse.ArgumentParser(description="Professional Agent Skills Consistency & Quality Validator")
    parser.add_argument("--strict", action="store_true", help="Fail if any warnings are detected")
    parser.add_argument("--skill", type=str, help="Validate a specific skill by name")
    parser.add_argument("--taxonomy", type=str, help="Validate a specific taxonomy domain")
    parser.add_argument("--json", action="store_true", help="Output audit results as JSON")
    args = parser.parse_args()

    repo_root = Path(__file__).resolve().parent.parent
    validator = SkillValidator(repo_root, strict=args.strict)
    success = validator.validate_all(target_skill=args.skill, target_taxonomy=args.taxonomy)

    if args.json:
        print(json.dumps(validator.results, indent=2))

    sys.exit(0 if success else 1)

if __name__ == "__main__":
    main()
