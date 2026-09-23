#!/usr/bin/env bash
# ==============================================================================
# Production Agent Skills Universal Installer
# Compatible with Google Antigravity, Claude Code, Cursor, Codex, and OpenCode
# ==============================================================================

set -e

REPO_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
TARGET_ENV="antigravity"
DRY_RUN=false
ALL_SKILLS=true
SPECIFIC_SKILL=""

# Colors
GREEN='\033[0;32m'
BLUE='\033[0;34m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
BOLD='\033[1m'
NC='\033[0m'

usage() {
  echo -e "${BOLD}Production Agent Skills Universal Installer${NC}"
  echo ""
  echo "Usage: ./install.sh [options]"
  echo ""
  echo "Options:"
  echo "  -t, --target <env>     Target environment: antigravity (default), claude, cursor, local"
  echo "  -s, --skill <name>     Install only a specific skill (e.g. ai-website-polish)"
  echo "  -d, --dry-run          Simulate installation without copying files"
  echo "  -h, --help             Show this help message"
  echo ""
  echo "Target Directories:"
  echo "  • antigravity: ~/.gemini/config/skills/"
  echo "  • claude:      ~/.claude/skills/"
  echo "  • cursor:      ~/.cursor/skills/"
  echo "  • local:       ./.agents/skills/ (in current project)"
  echo ""
  exit 0
}

while [[ "$#" -gt 0 ]]; do
  case $1 in
    -t|--target) TARGET_ENV="$2"; shift ;;
    -s|--skill) SPECIFIC_SKILL="$2"; ALL_SKILLS=false; shift ;;
    -d|--dry-run) DRY_RUN=true ;;
    -h|--help) usage ;;
    *) echo -e "${RED}Unknown option: $1${NC}"; usage ;;
  esac
  shift
done

# Resolve destination directory
case $TARGET_ENV in
  antigravity)
    DEST_DIR="$HOME/.gemini/config/skills"
    ;;
  claude)
    DEST_DIR="$HOME/.claude/skills"
    ;;
  cursor)
    DEST_DIR="$HOME/.cursor/skills"
    ;;
  local)
    DEST_DIR="$(pwd)/.agents/skills"
    ;;
  *)
    echo -e "${RED}Invalid target environment: $TARGET_ENV${NC}"
    exit 1
    ;;
esac

SKILLS=(
  "ai-website-polish"
  "frontend-math-precision"
  "quantitative-ux-engine"
  "ux-laws-for-ai-design"
  "website-data-protection"
)

if [[ -n "$SPECIFIC_SKILL" ]]; then
  FOUND=false
  for s in "${SKILLS[@]}"; do
    if [[ "$s" == "$SPECIFIC_SKILL" ]]; then
      FOUND=true
      SKILLS=("$SPECIFIC_SKILL")
      break
    fi
  done
  if [[ "$FOUND" == false ]]; then
    echo -e "${RED}Skill '$SPECIFIC_SKILL' not found in repository.${NC}"
    exit 1
  fi
fi

echo -e "${BOLD}=== Installing Production Agent Skills ===${NC}"
echo -e "Target Environment : ${BLUE}$TARGET_ENV${NC}"
echo -e "Destination Path   : ${BLUE}$DEST_DIR${NC}"
if [[ "$DRY_RUN" == true ]]; then
  echo -e "Execution Mode     : ${YELLOW}DRY RUN (no files modified)${NC}"
fi
echo ""

if [[ "$DRY_RUN" == false ]]; then
  mkdir -p "$DEST_DIR"
fi

for skill in "${SKILLS[@]}"; do
  SRC_PATH="$REPO_DIR/$skill"
  TARGET_PATH="$DEST_DIR/$skill"

  if [[ ! -d "$SRC_PATH" ]]; then
    echo -e "${RED}Skipping missing skill: $skill${NC}"
    continue
  fi

  if [[ "$DRY_RUN" == true ]]; then
    echo -e "  [${YELLOW}PLAN${NC}] Would install: ${BOLD}$skill${NC} -> $TARGET_PATH"
  else
    rm -rf "$TARGET_PATH"
    cp -r "$SRC_PATH" "$TARGET_PATH"
    echo -e "  [${GREEN}INSTALLED${NC}] ${BOLD}$skill${NC}"
  fi
done

echo ""
if [[ "$DRY_RUN" == true ]]; then
  echo -e "${YELLOW}Dry run completed successfully.${NC}"
else
  echo -e "${GREEN}${BOLD}✔ All selected skills successfully installed to $DEST_DIR!${NC}"
  echo -e "Your AI coding agent will discover them automatically."
fi
