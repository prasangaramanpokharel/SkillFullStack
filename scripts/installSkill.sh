#!/usr/bin/env bash
# installSkill.sh
# One-liner installer to fetch any skill from SkillFullStack into your local project or global agent directory.
#
# Usage:
#   curl -fsSL https://raw.githubusercontent.com/prasangaramanpokharel/SkillFullStack/main/scripts/installSkill.sh | bash -s <skill-name> [dest-dir]
#
# Examples:
#   bash installSkill.sh databaseArchitecture
#   bash installSkill.sh apiEngineering .agent/skills

set -euo pipefail

SKILL_NAME="${1:-}"
DEST_ROOT="${2:-.agent/skills}"
REPO_RAW="https://raw.githubusercontent.com/prasangaramanpokharel/SkillFullStack/main"

if [ -z "$SKILL_NAME" ]; then
  echo "Error: Skill name required."
  echo "Usage: $0 <skill-name> [target-directory]"
  echo "Example: $0 databaseArchitecture"
  exit 1
fi

echo "==> Fetching catalog from SkillFullStack..."
CATALOG_JSON=$(curl -fsSL "${REPO_RAW}/.skillsRegistry/catalog.json")

# Extract relative path from catalog.json
SKILL_PATH=$(echo "$CATALOG_JSON" | grep -B 2 -A 5 "\"name\": \"$SKILL_NAME\"" | grep "\"path\":" | head -n 1 | sed -E 's/.*"path": "([^"]+)".*/\1/')

if [ -z "$SKILL_PATH" ]; then
  # Fallback search across taxonomy
  echo "==> Searching taxonomy for skill '$SKILL_NAME'..."
  # Try common taxonomies
  FOUND=""
  for TAX in backend frontend cicdDevops gitVersionControl softwareDevelopment testing github dataAi securityQa foundation; do
    CHECK_CODE=$(curl -o /dev/null -s -w "%{http_code}\n" "${REPO_RAW}/skills/${TAX}/${SKILL_NAME}/SKILL.md")
    if [ "$CHECK_CODE" = "200" ]; then
      SKILL_PATH="skills/${TAX}/${SKILL_NAME}"
      FOUND="true"
      break
    fi
  done
  if [ -z "$FOUND" ]; then
    echo "Error: Skill '$SKILL_NAME' not found in catalog."
    exit 1
  fi
fi

TARGET_DIR="${DEST_ROOT}/${SKILL_NAME}"
mkdir -p "$TARGET_DIR"

echo "==> Installing '$SKILL_NAME' into '$TARGET_DIR'..."
curl -fsSL "${REPO_RAW}/${SKILL_PATH}/SKILL.md" -o "${TARGET_DIR}/SKILL.md"

echo " Successfully installed $SKILL_NAME!"
echo "    Specification: ${TARGET_DIR}/SKILL.md"
echo "    Source: ${REPO_RAW}/${SKILL_PATH}/SKILL.md"
