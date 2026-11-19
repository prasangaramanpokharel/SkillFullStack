#!/usr/bin/env python3
"""
runComplianceAudit.py — Universal Skill Compliance Auditor & Report Generator
Audits any codebase against any SkillFullStack skill specification,
verifying rules and anti-patterns file-by-file and generating compliance-report.md.
"""

import os
import sys
import re
import json
import argparse
from pathlib import Path
from datetime import datetime

def find_skill_file(skill_name: str, repo_root: Path) -> Path:
    catalog_path = repo_root / ".skillsRegistry" / "catalog.json"
    if catalog_path.exists():
        try:
            with open(catalog_path, "r", encoding="utf-8") as f:
                catalog = json.load(f)
            for s in catalog.get("skills", []):
                if s["name"].lower() == skill_name.lower():
                    skill_file = repo_root / s["path"] / "SKILL.md"
                    if skill_file.exists():
                        return skill_file
        except Exception:
            pass

    # Fallback recursive search
    for skill_file in repo_root.glob("skills/**/SKILL.md"):
        if skill_file.parent.name.lower() == skill_name.lower():
            return skill_file
    return None

def extract_rules_from_skill(skill_file: Path):
    rules = []
    with open(skill_file, "r", encoding="utf-8") as f:
        content = f.read()

    # 1. Parse anti-patterns table if present
    # Look for markdown tables with Anti-Pattern | Why ... | Correct Modern Standard
    table_pattern = re.compile(
        r'\|\s*\*\*?([^*|\n]+)\*\*?\s*\|\s*([^|\n]+)\s*\|\s*([^|\n]+)\s*\|'
    )
    matches = table_pattern.findall(content)
    rule_idx = 1
    for m in matches:
        anti_pat = m[0].strip()
        why = m[1].strip()
        standard = m[2].strip()
        if "Anti-Pattern" in anti_pat or "---" in anti_pat:
            continue
        rules.append({
            "id": f"R-{rule_idx:02d}",
            "title": anti_pat,
            "category": "Anti-Pattern",
            "forbidden": anti_pat,
            "why": why,
            "required": standard
        })
        rule_idx += 1

    # 2. If no table, extract headers as general rules
    if not rules:
        headers = re.findall(r'^##\s+(.+)$', content, re.MULTILINE)
        for h in headers:
            if h.startswith("⚡") or "Notice" in h:
                continue
            rules.append({
                "id": f"R-{rule_idx:02d}",
                "title": h.strip(),
                "category": "Architectural Principle",
                "forbidden": f"Non-compliance with {h.strip()}",
                "why": "Violates core architectural directive in skill",
                "required": f"Adhere to {h.strip()} specifications"
            })
            rule_idx += 1

    return rules

def audit_codebase(target_path: Path, rules: list):
    findings = []
    scanned_files = 0

    # Collect source files
    source_files = []
    if target_path.is_file():
        source_files = [target_path]
    else:
        for root, dirs, files in os.walk(target_path):
            dirs[:] = [d for d in dirs if not d.startswith('.') and d not in ('node_modules', 'dist', 'build', 'temp', '.git')]
            for f in files:
                ext = Path(f).suffix.lower()
                if ext in ('.js', '.jsx', '.ts', '.tsx', '.py', '.go', '.rs', '.c', '.cpp', '.h', '.java', '.did', '.mo', '.json', '.yaml'):
                    source_files.append(Path(root) / f)

    scanned_files = len(source_files)

    for sf in source_files:
        try:
            with open(sf, "r", encoding="utf-8", errors="ignore") as f:
                lines = f.readlines()
        except Exception:
            continue

        for line_no, line in enumerate(lines, 1):
            line_str = line.strip()
            for r in rules:
                # Basic heuristic matching on forbidden terms
                # Clean forbidden string for matching
                terms = [t for t in re.split(r'[\s`(),]+', r["forbidden"]) if len(t) > 3 and not t.lower() in ("using", "without", "entire", "with", "from")]
                for term in terms:
                    if term.lower() in line_str.lower():
                        findings.append({
                            "rule": r,
                            "file": str(sf),
                            "line_number": line_no,
                            "snippet": line_str
                        })
                        break
    return source_files, findings

def generate_compliance_report(skill_name: str, skill_file: Path, target_path: Path, rules: list, findings: list, output_file: Path):
    now_str = datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S UTC")
    total_rules = len(rules) if rules else 1
    violated_rule_ids = set(f["rule"]["id"] for f in findings)
    passed_rules = total_rules - len(violated_rule_ids)
    score = int((passed_rules / total_rules) * 100) if total_rules > 0 else 100
    status = "FULLY_COMPLIANT" if score == 100 else "REMEDIATION_REQUIRED"

    report_lines = [
        f"# Compliance Audit Report: {skill_name}",
        "",
        f"- **Audit Date**: {now_str}",
        f"- **Target Skill**: `{skill_name}` ({skill_file.relative_to(skill_file.parents[2]) if skill_file else 'N/A'})",
        f"- **Evaluated Codebase**: `{target_path.resolve()}`",
        f"- **Overall Compliance Score**: {score}% ({passed_rules}/{total_rules} Rules Passed)",
        f"- **Compliance Status**: {status}",
        f"- **Agent Execution Mode**: STANDALONE_CLI / COMPLIANCE_ENGINEER",
        "",
        "---",
        "",
        "## 1. Compliance Executive Summary",
        f"This audit evaluated codebase adherence against the **{skill_name}** engineering standard.",
        f"Overall adherence stands at **{score}%**. {f'{len(findings)} non-compliant code occurrences were detected across {len(violated_rule_ids)} rules.' if findings else 'The codebase satisfies all audited architectural constraints and anti-pattern invariants.'}",
        "",
        "---",
        "",
        "## 2. Rule-by-Rule Compliance Verification Matrix",
        "",
        "| Rule ID | Category | Requirement / Constraint | Status | Violations Found |",
        "| :--- | :--- | :--- | :---: | :---: |"
    ]

    for r in rules:
        r_id = r["id"]
        v_count = sum(1 for f in findings if f["rule"]["id"] == r_id)
        r_status = "✅ PASS" if v_count == 0 else "❌ FAIL"
        report_lines.append(f"| `{r_id}` | {r['category']} | {r['title']} | {r_status} | {v_count} |")

    report_lines.extend([
        "",
        "---",
        "",
        "## 3. Detailed Line-by-Line Non-Compliance Diffs",
        ""
    ])

    if not findings:
        report_lines.append("✅ No non-compliant code blocks detected. Full adherence achieved.")
    else:
        for idx, f in enumerate(findings, 1):
            r = f["rule"]
            report_lines.extend([
                f"### Violation {idx}: {r['title']}",
                f"- **File**: `{f['file']}:{f['line_number']}`",
                f"- **Violated Constraint**: {r['why']}",
                f"- **Required Modern Standard**: {r['required']}",
                "",
                "```diff",
                f"--- a/{f['file']}",
                f"+++ b/{f['file']}",
                f"@@ -{f['line_number']},1 +{f['line_number']},1 @@",
                f"- {f['snippet']}",
                f"+ // COMPLIANT FIX: {r['required']}",
                "```",
                ""
            ])

    report_lines.extend([
        "---",
        "",
        "## 4. Remediation Action Plan & Loop Progression",
        f"- **Total Violations Detected**: {len(findings)}",
        f"- **Remaining Deviations**: {len(violated_rule_ids)} rule(s)",
        f"- **Continuous Loop State**: {'TERMINATED (100% Compliant)' if score == 100 else 'LOOPING (Remediations in progress)'}",
        ""
    ])

    with open(output_file, "w", encoding="utf-8") as f:
        f.write("\n".join(report_lines))

    return score, status

def main():
    parser = argparse.ArgumentParser(description="SkillFullStack Universal Compliance Auditor")
    parser.add_argument("--skill", required=True, help="Target skill name to compliance-audit (e.g. nextjs, apiEngineering, cloudflare)")
    parser.add_argument("--path", default=".", help="Root directory of codebase to audit (default: current directory)")
    parser.add_argument("--output", default="compliance-report.md", help="Output path for compliance report")
    parser.add_argument("--repo-root", default=".", help="SkillFullStack repository root")
    parser.add_argument("--format", choices=["terminal", "json"], default="terminal", help="Console output format")

    args = parser.parse_args()
    repo_root = Path(args.repo_root).resolve()
    target_path = Path(args.path).resolve()
    output_file = Path(args.output).resolve()

    skill_file = find_skill_file(args.skill, repo_root)
    if not skill_file:
        print(f"❌ Error: Target skill '{args.skill}' not found in skills catalog at {repo_root}")
        sys.exit(1)

    rules = extract_rules_from_skill(skill_file)
    source_files, findings = audit_codebase(target_path, rules)
    score, status = generate_compliance_report(args.skill, skill_file, target_path, rules, findings, output_file)

    if args.format == "json":
        print(json.dumps({
            "skill": args.skill,
            "score": score,
            "status": status,
            "total_rules": len(rules),
            "findings_count": len(findings),
            "report_path": str(output_file)
        }, indent=2))
        sys.exit(0 if score == 100 else 1)

    print("══════════════════════════════════════════════════════════════════════════")
    print(" ⚖️   SKILLFULLSTACK UNIVERSAL COMPLIANCE AUDITOR")
    print("══════════════════════════════════════════════════════════════════════════")
    print(f" Target Skill:      {args.skill}")
    print(f" Skill Spec:        {skill_file}")
    print(f" Evaluated Path:    {target_path}")
    print(f" Files Inspected:   {len(source_files)}")
    print(f" Rules Evaluated:   {len(rules)}")
    print(f" Compliance Score:  {score}% ({status})")
    print(f" Report Output:     {output_file}")
    print("──────────────────────────────────────────────────────────────────────────")

    if score == 100:
        print(" ✅ FULL COMPLIANCE ACHIEVED: Zero policy or anti-pattern deviations found.")
    else:
        print(f" ⚠️  REMEDIATION REQUIRED: {len(findings)} violation(s) flagged.")
        print(f" Consult {output_file} for line-level diffs and remediation steps.")

    print("══════════════════════════════════════════════════════════════════════════")
    sys.exit(0 if score == 100 else 1)

if __name__ == "__main__":
    main()
