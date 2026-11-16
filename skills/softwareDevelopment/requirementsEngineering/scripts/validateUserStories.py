#!/usr/bin/env python3
"""
validateUserStories.py
Lints user stories against the INVEST criteria and checks for Gherkin acceptance criteria (Given/When/Then).
"""

import sys
import re
import json

AMBIGUOUS_WORDS = ["fast", "quick", "intuitive", "easy", "user-friendly", "robust", "scalable", "seamless"]

def validate_story_text(text):
    has_as_a = bool(re.search(r"as an?\s+", text, re.IGNORECASE))
    has_i_want = bool(re.search(r"i want\s+", text, re.IGNORECASE))
    has_so_that = bool(re.search(r"so that\s+", text, re.IGNORECASE))
    
    has_given = bool(re.search(r"\bgiven\b", text, re.IGNORECASE))
    has_when = bool(re.search(r"\bwhen\b", text, re.IGNORECASE))
    has_then = bool(re.search(r"\bthen\b", text, re.IGNORECASE))
    
    found_ambiguous = [w for w in AMBIGUOUS_WORDS if re.search(rf"\b{w}\b", text, re.IGNORECASE)]

    valid_format = has_as_a and has_i_want and has_so_that
    valid_acceptance = has_given and has_when and has_then

    score = 0
    if valid_format: score += 40
    if valid_acceptance: score += 40
    if not found_ambiguous: score += 20

    return {
        "hasStandardFormat": valid_format,
        "hasGherkinAcceptanceCriteria": valid_acceptance,
        "ambiguousTermsDetected": found_ambiguous,
        "qualityScore": score,
        "isInvestReady": score >= 80
    }

def main():
    sample_text = sys.stdin.read() if not sys.stdin.isatty() else """
    As a shopper I want to checkout So that I buy items.
    Given my cart has items When I pay Then order is placed.
    """
    result = validate_story_text(sample_text)
    print(json.dumps(result, indent=2))

if __name__ == "__main__":
    main()
