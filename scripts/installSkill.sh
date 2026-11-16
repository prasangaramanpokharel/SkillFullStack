#!/usr/bin/env bash
# installSkill.sh
# Universal installer to fetch any skill from SkillFullStack into your AI environment.
#
# Usage:
#   curl -fsSL https://raw.githubusercontent.com/prasangaramanpokharel/SkillFullStack/main/scripts/installSkill.sh | bash -s <skill-name> [agent|target-dir]
#
# Supported Agents:
#   antigravity -> .gemini/antigravity/skills/<skill-name>/
#   claude      -> .claude/commands/<skill-name>.md and .claude/skills/<skill-name>/
#   cursor      -> .cursor/rules/<skill-name>.mdc
#   windsurf    -> .windsurf/skills/<skill-name>/
#   agent       -> .agent/skills/<skill-name>/ (default)
#
# Examples:
#   bash installSkill.sh databaseArchitecture antigravity
#   bash installSkill.sh apiEngineering claude
#   bash installSkill.sh testDrivenDevelopment cursor

set -euo pipefail

SKILL_NAME="${1:-}"
TARGET_ARG="${2:-agent}"
REPO_RAW="https://raw.githubusercontent.com/prasangaramanpokharel/SkillFullStack/main"

if [ -z "$SKILL_NAME" ]; then
  echo "Error: Skill name required."
  echo "Usage: $0 <skill-name> [antigravity|claude|cursor|windsurf|agent|custom-dir]"
  echo "Example: $0 databaseArchitecture antigravity"
  exit 1
fi

echo "==> Fetching catalog from SkillFullStack..."
CATALOG_JSON=$(curl -fsSL "${REPO_RAW}/.skillsRegistry/catalog.json")

# Extract relative path from catalog.json
SKILL_PATH=$(echo "$CATALOG_JSON" | grep -B 2 -A 5 "\"name\": \"$SKILL_NAME\"" | grep "\"path\":" | head -n 1 | sed -E 's/.*"path": "([^"]+)".*/\1/')

if [ -z "$SKILL_PATH" ]; then
  # Fallback search across taxonomies
  echo "==> Searching taxonomy for skill '$SKILL_NAME'..."
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

# Determine target directory and file based on agent target
case "$TARGET_ARG" in
  antigravity)
    TARGET_DIR=".gemini/antigravity/skills/${SKILL_NAME}"
    TARGET_FILE="${TARGET_DIR}/SKILL.md"
    ;;
  claude)
    TARGET_DIR=".claude/skills/${SKILL_NAME}"
    TARGET_FILE="${TARGET_DIR}/SKILL.md"
    CMD_DIR=".claude/commands"
    CMD_FILE="${CMD_DIR}/${SKILL_NAME}.md"
    mkdir -p "$CMD_DIR"
    ;;
  cursor)
    TARGET_DIR=".cursor/rules"
    TARGET_FILE="${TARGET_DIR}/${SKILL_NAME}.mdc"
    ;;
  windsurf)
    TARGET_DIR=".windsurf/skills/${SKILL_NAME}"
    TARGET_FILE="${TARGET_DIR}/SKILL.md"
    ;;
  agent|"")
    TARGET_DIR=".agent/skills/${SKILL_NAME}"
    TARGET_FILE="${TARGET_DIR}/SKILL.md"
    ;;
  *)
    TARGET_DIR="${TARGET_ARG}/${SKILL_NAME}"
    TARGET_FILE="${TARGET_DIR}/SKILL.md"
    ;;
esac

mkdir -p "$TARGET_DIR"

echo "==> Installing '$SKILL_NAME' for target '$TARGET_ARG'..."
curl -fsSL "${REPO_RAW}/${SKILL_PATH}/SKILL.md" -o "$TARGET_FILE"

# If Claude Code, also configure the command file
if [ "$TARGET_ARG" = "claude" ]; then
  cp "$TARGET_FILE" "$CMD_FILE"
  echo "   Slash Command registered at: $CMD_FILE (Invoke via /${SKILL_NAME})"
fi

echo " Successfully installed $SKILL_NAME!"
echo "   File: $TARGET_FILE"
echo "   Source: ${REPO_RAW}/${SKILL_PATH}/SKILL.md"
