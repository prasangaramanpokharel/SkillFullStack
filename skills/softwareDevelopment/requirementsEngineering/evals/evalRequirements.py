#!/usr/bin/env python3
"""
evalRequirements.py
Validates the validateUserStories script against sample requirements.
"""

import subprocess
import json
import os
import sys

def test_validate_stories():
    script_path = os.path.join(os.path.dirname(__file__), "..", "scripts", "validateUserStories.py")
    sample_input = """
    As a verified user
    I want to reset my password
    So that I can regain access if locked out.

    Given I enter my registered email
    When I click send reset link
    Then a signed token email is dispatched within 5 seconds.
    """
    res = subprocess.run([sys.executable, script_path], input=sample_input, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
    assert res.returncode == 0, f"Script failed: {res.stderr}"
    data = json.loads(res.stdout)
    assert data["hasStandardFormat"] is True
    assert data["hasGherkinAcceptanceCriteria"] is True
    assert data["isInvestReady"] is True
    print(" test_validate_stories passed")

if __name__ == "__main__":
    test_validate_stories()
    print("All requirementsEngineering evals passed.")
