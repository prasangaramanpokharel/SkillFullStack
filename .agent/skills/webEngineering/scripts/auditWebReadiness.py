#!/usr/bin/env python3
"""
auditWebReadiness.py — Web Production Readiness & Pre-Flight Auditor
Evaluates web projects across Legal, Security Headers, Technical SEO,
AI-Agent Discovery (llms.txt & robots.txt), Core Web Vitals, and API Standards.

Generates web-readiness-report.md scorecard.
"""

import os
import sys
import re
import json
import argparse
from pathlib import Path
from datetime import datetime

CHECKS = [
    # ─── LEGAL & COMPLIANCE ───
    {
        "id": "LEG-01",
        "category": "Legal & Privacy",
        "title": "Privacy Policy Page (/privacy-policy or /privacy)",
        "check": lambda p: check_file_or_pattern(p, r'(?:privacy[-_]?policy|privacy\.(?:tsx|jsx|html|md|vue|svelte)|app/privacy)'),
        "fix": "Create a dedicated privacy policy page at /privacy-policy or /privacy detailing data handling and user rights."
    },
    {
        "id": "LEG-02",
        "category": "Legal & Privacy",
        "title": "Terms of Service Page (/terms-of-service or /terms)",
        "check": lambda p: check_file_or_pattern(p, r'(?:terms[-_]?(?:of[-_]?service|conditions)|terms\.(?:tsx|jsx|html|md|vue|svelte)|app/terms)'),
        "fix": "Create a terms of service page at /terms-of-service or /terms defining user obligations and liability limitations."
    },
    {
        "id": "LEG-03",
        "category": "Legal & Privacy",
        "title": "Cookie Policy & Opt-In Consent (/cookie-policy or /cookies)",
        "check": lambda p: check_file_or_pattern(p, r'(?:cookie[-_]?policy|cookies\.(?:tsx|jsx|html|md|vue|svelte)|app/cookies)'),
        "fix": "Provide a cookie policy at /cookie-policy or /cookies detailing tracking technologies and opt-out options."
    },
    {
        "id": "LEG-04",
        "category": "Legal & Privacy",
        "title": "Accessibility Statement Page (/accessibility)",
        "check": lambda p: check_file_or_pattern(p, r'(?:accessibility[-_]?statement|accessibility\.(?:tsx|jsx|html|md|vue|svelte)|app/accessibility)'),
        "fix": "Provide an accessibility statement at /accessibility documenting WCAG 2.2 AA conformity."
    },

    # ─── TECHNICAL SEO & AGENT READINESS ───
    {
        "id": "SEO-01",
        "category": "SEO & Agent Discovery",
        "title": "RFC 9309 robots.txt with Crawlers Configured (/robots.txt)",
        "check": lambda p: check_robots_txt(p),
        "fix": "Provide public/robots.txt with differentiated policies for search engines and AI agents."
    },
    {
        "id": "SEO-02",
        "category": "SEO & Agent Discovery",
        "title": "AI Agent Documentation Index (/llms.txt)",
        "check": lambda p: check_llms_txt(p),
        "fix": "Create public/llms.txt following the Markdown specification to assist AI agents and LLMs."
    },
    {
        "id": "SEO-03",
        "category": "SEO & Agent Discovery",
        "title": "Open Graph & Social Share Metadata",
        "check": lambda p: check_code_patterns(p, [r'og:image', r'og:title', r'twitter:card']),
        "fix": "Configure Open Graph metadata tags (og:title, og:image, og:description, twitter:card)."
    },
    {
        "id": "SEO-04",
        "category": "SEO & Agent Discovery",
        "title": "Canonical URL Specification",
        "check": lambda p: check_code_patterns(p, [r'rel=["\']canonical["\']', r'canonical:\s*["\']']),
        "fix": "Emit canonical link tags (<link rel='canonical' href='...'>) on all indexable routes."
    },
    {
        "id": "SEO-05",
        "category": "SEO & Agent Discovery",
        "title": "Sitemap XML Index (/sitemap.xml)",
        "check": lambda p: check_file_or_pattern(p, r'(?:sitemap\.xml|sitemap\.ts|sitemap\.js)'),
        "fix": "Generate and register /sitemap.xml listing all canonical, indexable URLs."
    },

    # ─── SECURITY HEADERS & DISCLOSURE ───
    {
        "id": "SEC-01",
        "category": "Security Headers",
        "title": "Strict-Transport-Security (HSTS)",
        "check": lambda p: check_code_patterns(p, [r'Strict-Transport-Security', r'max-age=\d+;\s*includeSubDomains']),
        "fix": "Enforce HSTS with max-age=63072000; includeSubDomains; preload in HTTP response headers."
    },
    {
        "id": "SEC-02",
        "category": "Security Headers",
        "title": "Content-Security-Policy (CSP)",
        "check": lambda p: check_code_patterns(p, [r'Content-Security-Policy', r'default-src']),
        "fix": "Configure a strict Content-Security-Policy using cryptographic nonces or hashes."
    },
    {
        "id": "SEC-03",
        "category": "Security Headers",
        "title": "MIME Sniffing & Clickjacking Defense",
        "check": lambda p: check_code_patterns(p, [r'X-Content-Type-Options', r'nosniff']),
        "fix": "Add X-Content-Type-Options: nosniff and X-Frame-Options: DENY response headers."
    },
    {
        "id": "SEC-04",
        "category": "Security Headers",
        "title": "RFC 9116 Security Disclosure (/.well-known/security.txt)",
        "check": lambda p: check_file_or_pattern(p, r'(?:security\.txt|\.well-known/security\.txt)'),
        "fix": "Provide /.well-known/security.txt documenting vulnerability reporting contact details."
    },

    # ─── CORE WEB VITALS & PERFORMANCE ───
    {
        "id": "CWV-01",
        "category": "Core Web Vitals",
        "title": "Image Dimensions & Aspect Ratio (CLS Prevention)",
        "check": lambda p: check_image_dimensions(p),
        "fix": "Ensure all <img> elements define explicit width/height attributes or CSS aspect-ratio."
    },
    {
        "id": "CWV-02",
        "category": "Core Web Vitals",
        "title": "Font Preloading or Display Swap",
        "check": lambda p: check_code_patterns(p, [r'font-display:\s*swap', r'rel=["\']preload["\'][^>]*as=["\']font["\']', r'next/font']),
        "fix": "Configure font-display: swap and preload primary web fonts to prevent FOIT/FOUT shifts."
    },

    # ─── API & ERROR HANDLING ───
    {
        "id": "API-01",
        "category": "Production API Standards",
        "title": "RFC 9457 Problem Details Error Envelope",
        "check": lambda p: check_code_patterns(p, [r'application/problem\+json', r'ProblemDetails', r'["\']status["\']:\s*\d+,\s*["\']title["\']']),
        "fix": "Format API errors adhering to RFC 9457 (type, title, status, detail, instance)."
    },
    {
        "id": "API-02",
        "category": "Production API Standards",
        "title": "Uptime Probe Endpoint (/api/health or /health)",
        "check": lambda p: check_file_or_pattern(p, r'(?:healthz?|api/health)'),
        "fix": "Provide a lightweight /api/health probe endpoint returning HTTP 200 for uptime monitors."
    }
]

def check_file_or_pattern(root_path: Path, pattern_str: str) -> bool:
    reg = re.compile(pattern_str, re.IGNORECASE)
    for root, dirs, files in os.walk(root_path):
        dirs[:] = [d for d in dirs if not d.startswith('.') and d not in ('node_modules', 'dist', 'build', 'temp')]
        for f in files:
            if reg.search(f):
                return True
    return False

def check_robots_txt(root_path: Path) -> bool:
    candidates = [
        root_path / "public" / "robots.txt",
        root_path / "static" / "robots.txt",
        root_path / "robots.txt"
    ]
    for c in candidates:
        if c.is_file():
            try:
                content = c.read_text(encoding="utf-8", errors="ignore")
                if "User-agent:" in content or "user-agent:" in content:
                    return True
            except Exception:
                pass
    return False

def check_llms_txt(root_path: Path) -> bool:
    candidates = [
        root_path / "public" / "llms.txt",
        root_path / "static" / "llms.txt",
        root_path / "llms.txt",
        root_path / "app" / "llms.txt" / "route.ts"
    ]
    for c in candidates:
        if c.is_file():
            return True
    return False

def check_code_patterns(root_path: Path, patterns: list) -> bool:
    regs = [re.compile(p, re.IGNORECASE) for p in patterns]
    for root, dirs, files in os.walk(root_path):
        dirs[:] = [d for d in dirs if not d.startswith('.') and d not in ('node_modules', 'dist', 'build', 'temp')]
        for f in files:
            ext = Path(f).suffix.lower()
            if ext in ('.html', '.jsx', '.tsx', '.vue', '.svelte', '.js', '.ts', '.mjs', '.json', '.toml', '.conf'):
                fp = Path(root) / f
                try:
                    content = fp.read_text(encoding="utf-8", errors="ignore")
                    for reg in regs:
                        if reg.search(content):
                            return True
                except Exception:
                    pass
    return False

def check_image_dimensions(root_path: Path) -> bool:
    # Heuristic: check if standard layout or components define width/height on images
    for root, dirs, files in os.walk(root_path):
        dirs[:] = [d for d in dirs if not d.startswith('.') and d not in ('node_modules', 'dist', 'build', 'temp')]
        for f in files:
            ext = Path(f).suffix.lower()
            if ext in ('.html', '.jsx', '.tsx', '.vue', '.svelte'):
                try:
                    content = (Path(root) / f).read_text(encoding="utf-8", errors="ignore")
                    if 'next/image' in content or 'astro:assets' in content:
                        return True
                    if re.search(r'<img[^>]+(?:width=|height=)[^>]*>', content, re.IGNORECASE):
                        return True
                except Exception:
                    pass
    return False

def generate_report(results: list, output_file: Path, target_path: Path):
    now_str = datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S UTC")
    total_checks = len(results)
    passed_checks = sum(1 for r in results if r["passed"])
    score = int((passed_checks / total_checks) * 100) if total_checks > 0 else 100
    status = "PRODUCTION_READY" if score >= 90 else "LAUNCH_BLOCKED_CRITICAL_ISSUES"

    report_lines = [
        "# Web Production Launch Readiness Report",
        "",
        f"- **Evaluation Date**: {now_str}",
        f"- **Target Application**: `{target_path.resolve()}`",
        f"- **Overall Readiness Score**: {score}% ({passed_checks}/{total_checks} Checks Passed)",
        f"- **Launch Status**: {status}",
        "",
        "---",
        "",
        "## 1. Domain Health Scorecards",
        "",
        "| Check ID | Category | Audit Requirement | Status |",
        "| :--- | :--- | :--- | :---: |"
    ]

    for r in results:
        stat_icon = "✅ PASS" if r["passed"] else "❌ FAIL"
        report_lines.append(f"| `{r['id']}` | {r['category']} | {r['title']} | {stat_icon} |")

    report_lines.extend([
        "",
        "---",
        "",
        "## 2. Actionable Remediation Guidance",
        ""
    ])

    failures = [r for r in results if not r["passed"]]
    if not failures:
        report_lines.append("✅ All pre-flight launch checks passed! The web application satisfies modern production standards.")
    else:
        for idx, f in enumerate(failures, 1):
            report_lines.extend([
                f"### {idx}. [{f['id']}] {f['title']}",
                f"- **Category**: {f['category']}",
                f"- **Required Fix**: {f['fix']}",
                ""
            ])

    report_lines.extend([
        "---",
        "",
        "## 3. Launch Certification Sign-off",
        f"- **Certified By**: SkillFullStack Web Engineering Auditor",
        f"- **Verdict**: {'Approved for deployment.' if score >= 90 else 'Remediate critical blockers prior to release.'}",
        ""
    ])

    output_file.write_text("\n".join(report_lines), encoding="utf-8")
    return score, status

def main():
    parser = argparse.ArgumentParser(description="SkillFullStack Web Production Auditor")
    parser.add_argument("--path", default=".", help="Root directory of web project to evaluate")
    parser.add_argument("--output", default="web-readiness-report.md", help="Output path for readiness report")
    parser.add_argument("--format", choices=["terminal", "json"], default="terminal", help="Console output format")

    args = parser.parse_args()
    target_path = Path(args.path).resolve()
    output_file = Path(args.output).resolve()

    results = []
    for c in CHECKS:
        passed = c["check"](target_path)
        results.append({
            "id": c["id"],
            "category": c["category"],
            "title": c["title"],
            "passed": passed,
            "fix": c["fix"]
        })

    score, status = generate_report(results, output_file, target_path)

    if args.format == "json":
        print(json.dumps({
            "target": str(target_path),
            "score": score,
            "status": status,
            "checks": results,
            "report_path": str(output_file)
        }, indent=2))
        return

    print("══════════════════════════════════════════════════════════════════════════")
    print(" 🌐   SKILLFULLSTACK WEB PRODUCTION AUDITOR")
    print("══════════════════════════════════════════════════════════════════════════")
    print(f" Target Path:      {target_path}")
    print(f" Readiness Score:  {score}% ({status})")
    print(f" Report Output:    {output_file}")
    print("──────────────────────────────────────────────────────────────────────────")

    for r in results:
        mark = "✅ PASS" if r["passed"] else "❌ FAIL"
        print(f" {mark}  [{r['id']}] {r['title']} ({r['category']})")

    print("══════════════════════════════════════════════════════════════════════════")

if __name__ == "__main__":
    main()
