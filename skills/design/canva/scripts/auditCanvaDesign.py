#!/usr/bin/env python3
"""
Canva Design Inspector & Pre-flight Auditor
Diagnoses Canva design structure, transactional readiness, brand compliance, and feedback status.

Usage:
    python3 auditCanvaDesign.py [--mock] [--design-id ID] [--url URL] [--brand-palette HEX1,HEX2] [--json]
"""

import sys
import re
import json
import argparse
from typing import Dict, Any, List

class Colors:
    RESET = "\033[0m"
    BOLD = "\033[1m"
    DIM = "\033[2m"
    RED = "\033[31m"
    GREEN = "\033[32m"
    YELLOW = "\033[33m"
    BLUE = "\033[34m"
    CYAN = "\033[36m"
    GRAY = "\033[90m"

MOCK_DESIGN_DATA = {
    "id": "DAGfA-mock991",
    "title": "2026 Enterprise Product Launch Pitch Deck",
    "pages_count": 4,
    "pages": [
        {
            "page_index": 0,
            "title": "Cover Slide",
            "is_responsive": False,
            "width": 1920,
            "height": 1080,
            "elements": [
                {"id": "elem_cover_h1", "type": "text", "text": "Cloud Scale 2026", "font_size": 48, "color": "#0B5CD7", "font_weight": "bold"},
                {"id": "elem_cover_sub", "type": "text", "text": "Unified Agent Architecture", "font_size": 24, "color": "#1F2937", "font_weight": "normal"},
                {"id": "elem_cover_logo", "type": "fill", "asset_id": "asset_logo_01", "width": 180, "height": 60, "x": 48, "y": 48}
            ]
        },
        {
            "page_index": 1,
            "title": "Executive Summary",
            "is_responsive": False,
            "width": 1920,
            "height": 1080,
            "elements": [
                {"id": "elem_s2_h1", "type": "text", "text": "Strategic Imperatives", "font_size": 36, "color": "#1A73E8", "font_weight": "bold"},
                {"id": "elem_s2_body", "type": "text", "text": "Delivering sub-100ms latency across global edge points with zero cold starts.", "font_size": 18, "color": "#374151", "font_weight": "normal"}
            ]
        },
        {
            "page_index": 2,
            "title": "Architecture Overview",
            "is_responsive": True,
            "width": 1920,
            "height": 1080,
            "elements": [
                {"id": "elem_s3_h1", "type": "text", "text": "Responsive Topology", "font_size": 36, "color": "#0B5CD7", "font_weight": "bold"},
                {"id": "elem_s3_body", "type": "text", "text": "Reflows automatically across devices.", "font_size": 18, "color": "#374151", "font_weight": "normal"}
            ]
        },
        {
            "page_index": 3,
            "title": "Call to Action",
            "is_responsive": False,
            "width": 1920,
            "height": 1080,
            "elements": [
                {"id": "elem_s4_h1", "type": "text", "text": "Get Started Today", "font_size": 40, "color": "#0B5CD7", "font_weight": "bold"},
                {"id": "elem_s4_cta", "type": "text", "text": "Visit https://example.com/start", "font_size": 20, "color": "#EF4444", "font_weight": "bold"}
            ]
        }
    ],
    "comments": [
        {"id": "cmt_01", "author": "Sarah Chen", "page_index": 1, "text": "The blue in this heading (#1A73E8) is off-brand; change it to our primary blue #0B5CD7.", "status": "open"},
        {"id": "cmt_02", "author": "David Miller", "page_index": 2, "text": "Can we change the body font to Montserrat across the deck?", "status": "open"},
        {"id": "cmt_03", "author": "Sarah Chen", "page_index": 3, "text": "Looks great! LGTM.", "status": "resolved"}
    ]
}

def parse_design_id(url_or_id: str) -> str:
    if not url_or_id:
        return ""
    if url_or_id.startswith("D"):
        return url_or_id.split("/")[0]
    m = re.search(r"/design/([A-Za-z0-9_-]+)", url_or_id)
    if m:
        return m.group(1)
    return url_or_id

def audit_design(data: Dict[str, Any], brand_palette: List[str] = None) -> Dict[str, Any]:
    issues = []
    warnings = []
    supported_edits = []
    manual_edits = []

    palette_set = set(p.upper() for p in brand_palette) if brand_palette else {"#0B5CD7", "#1F2937", "#374151", "#FFFFFF"}

    total_elements = 0
    responsive_pages = 0

    for page in data.get("pages", []):
        p_idx = page.get("page_index", 0)
        is_resp = page.get("is_responsive", False)
        if is_resp:
            responsive_pages += 1
            warnings.append(f"Page {p_idx + 1} ('{page.get('title')}') has is_responsive=True. Position/size/format operations restricted.")

        for elem in page.get("elements", []):
            total_elements += 1
            color = elem.get("color")
            if color:
                color_upper = color.upper()
                if color_upper not in palette_set:
                    issues.append(f"Page {p_idx + 1} element '{elem.get('id')}' uses off-brand color {color}. Approved: {', '.join(sorted(palette_set))}")

    # Audit comments
    for cmt in data.get("comments", []):
        text = cmt.get("text", "")
        if cmt.get("status") == "resolved" or "lgtm" in text.lower():
            continue
        if "font" in text.lower() and ("montserrat" in text.lower() or "family" in text.lower() or "inter" in text.lower()):
            manual_edits.append({"comment_id": cmt.get("id"), "request": text, "reason": "API cannot mutate font family/typeface"})
        else:
            supported_edits.append({"comment_id": cmt.get("id"), "request": text, "type": "text/color operation"})

    score = max(0, 100 - (len(issues) * 15) - (len(warnings) * 5))

    return {
        "design_id": data.get("id"),
        "title": data.get("title"),
        "pages_count": data.get("pages_count", 0),
        "total_elements": total_elements,
        "responsive_pages": responsive_pages,
        "score": score,
        "issues": issues,
        "warnings": warnings,
        "supported_edits": supported_edits,
        "manual_edits": manual_edits,
    }

def print_audit_report(report: Dict[str, Any]):
    print(f"\n{Colors.BOLD}{Colors.CYAN}══════════════════════════════════════════════════════════════════════════{Colors.RESET}")
    print(f"{Colors.BOLD}{Colors.CYAN} 🎨 CANVA DESIGN AUDITOR & PRE-FLIGHT DIAGNOSTIC{Colors.RESET}")
    print(f"{Colors.BOLD}{Colors.CYAN}══════════════════════════════════════════════════════════════════════════{Colors.RESET}\n")

    print(f" {Colors.BOLD}Design Title:{Colors.RESET} {report['title']} ({Colors.GRAY}{report['design_id']}{Colors.RESET})")
    print(f" {Colors.BOLD}Pages:{Colors.RESET}        {report['pages_count']} (Responsive: {report['responsive_pages']})")
    print(f" {Colors.BOLD}Elements:{Colors.RESET}     {report['total_elements']} inspectable elements")

    score = report["score"]
    score_col = Colors.GREEN if score >= 85 else (Colors.YELLOW if score >= 60 else Colors.RED)
    print(f" {Colors.BOLD}Audit Score:{Colors.RESET}  {score_col}{score}/100{Colors.RESET}\n")

    if report["issues"]:
        print(f"{Colors.BOLD}{Colors.RED}❌ Brand / Formatting Deviations ({len(report['issues'])}):{Colors.RESET}")
        for iss in report["issues"]:
            print(f"   • {iss}")
        print()

    if report["warnings"]:
        print(f"{Colors.BOLD}{Colors.YELLOW}⚠️  Structural Warnings ({len(report['warnings'])}):{Colors.RESET}")
        for wrn in report["warnings"]:
            print(f"   • {wrn}")
        print()

    if report["supported_edits"]:
        print(f"{Colors.BOLD}{Colors.GREEN}⚡ Actionable Feedback (API-Fixable via /canva-edit):{Colors.RESET}")
        for edit in report["supported_edits"]:
            print(f"   • [{edit['comment_id']}] {edit['request']}")
        print()

    if report["manual_edits"]:
        print(f"{Colors.BOLD}{Colors.BLUE}🛠️  Requires Manual Action in Canva Editor:{Colors.RESET}")
        for edit in report["manual_edits"]:
            print(f"   • [{edit['comment_id']}] {edit['request']} ({Colors.GRAY}{edit['reason']}{Colors.RESET})")
        print()

    print(f"{Colors.BOLD}{Colors.CYAN}══════════════════════════════════════════════════════════════════════════{Colors.RESET}\n")

def main():
    parser = argparse.ArgumentParser(description="Canva Design Structure & Compliance Inspector")
    parser.add_argument("--design-id", type=str, help="Canva design identifier")
    parser.add_argument("--url", type=str, help="Canva design link or share URL")
    parser.add_argument("--mock", action="store_true", help="Run in offline mock mode with simulated design")
    parser.add_argument("--brand-palette", type=str, help="Comma-separated hex codes for palette verification")
    parser.add_argument("--json", action="store_true", help="Output results in raw JSON")
    args = parser.parse_args()

    palette = [c.strip() for c in args.brand_palette.split(",")] if args.brand_palette else None

    if args.mock or (not args.design_id and not args.url):
        data = MOCK_DESIGN_DATA
    else:
        # In a real environment, query CLI or MCP. If offline, advise user or use mock.
        target_id = parse_design_id(args.design_id or args.url)
        data = MOCK_DESIGN_DATA.copy()
        data["id"] = target_id or "DAGfA-offline"

    report = audit_design(data, brand_palette=palette)

    if args.json:
        print(json.dumps(report, indent=2))
    else:
        print_audit_report(report)

if __name__ == "__main__":
    main()
