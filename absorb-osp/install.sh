#!/usr/bin/env bash
#
# absorb-osp — Open Source Project Absorption Workflow
# Installer for Unix/macOS
#
# Usage:
#   git clone https://github.com/SATPROTOCOL/micos.git && cd micos/absorb-osp && ./install.sh
#   ./install.sh [--prefix=~/.claude] [--hermes]
#
set -euo pipefail

# ── Configuration ──────────────────────────────────────────────────

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
REPO_URL="https://github.com/SATPROTOCOL/micos"

# Detect target directory
if [ -n "${CLAUDE_CONFIG_DIR:-}" ]; then
  TARGET_DIR="$CLAUDE_CONFIG_DIR"
elif [ -d "$HOME/.claude/skills" ]; then
  TARGET_DIR="$HOME/.claude"
else
  TARGET_DIR="$HOME/.claude"
fi

INSTALL_HERMES=false
for arg in "$@"; do
  case "$arg" in
    --prefix=*) TARGET_DIR="${arg#*=}" ;;
    --hermes) INSTALL_HERMES=true ;;
    --help)
      echo "Usage: $0 [--prefix=DIR] [--hermes]"
      echo "  --prefix=DIR   Install to DIR (default: ~/.claude)"
      echo "  --hermes       Also install Hermes Agent config"
      exit 0
      ;;
  esac
done

# ── Colors ─────────────────────────────────────────────────────────

RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

info()  { echo -e "${BLUE}[INFO]${NC} $*"; }
ok()    { echo -e "${GREEN}[OK]${NC}   $*"; }
warn()  { echo -e "${YELLOW}[WARN]${NC} $*"; }
error() { echo -e "${RED}[ERROR]${NC} $*"; }

# ── Install Functions ──────────────────────────────────────────────

install_claude() {
  local src="$SCRIPT_DIR/claude"
  local dst="$TARGET_DIR"

  info "Installing absorb-osp for Claude Code..."
  info "  Source: $src"
  info "  Target: $dst"

  # Create directories
  mkdir -p "$dst/skills/absorb-osp"
  mkdir -p "$dst/rules"

  # Copy skill
  if [ -f "$src/SKILL.md" ]; then
    cp "$src/SKILL.md" "$dst/skills/absorb-osp/SKILL.md"
    ok "Installed skill → $dst/skills/absorb-osp/SKILL.md"
  fi

  # Copy workflow spec
  if [ -f "$src/WORKFLOW_SPEC.md" ]; then
    cp "$src/WORKFLOW_SPEC.md" "$dst/skills/absorb-osp/WORKFLOW_SPEC.md"
    ok "Installed spec → $dst/skills/absorb-osp/WORKFLOW_SPEC.md"
  fi

  # Copy rules
  if [ -f "$src/rules/absorb-workflow.md" ]; then
    cp "$src/rules/absorb-workflow.md" "$dst/rules/absorb-workflow.md"
    ok "Installed rules → $dst/rules/absorb-workflow.md"
  fi

  # Copy templates
  mkdir -p "$dst/absorbed"
  local template_src="$SCRIPT_DIR/templates"
  if [ -d "$template_src" ]; then
    for tmpl in "$template_src"/*.md; do
      cp "$tmpl" "$dst/absorbed/TEMPLATE_$(basename "$tmpl")"
      ok "Installed template → $dst/absorbed/TEMPLATE_$(basename "$tmpl")"
    done
  fi

  # Copy shared indexes
  local shared_src="$SCRIPT_DIR/shared"
  if [ -d "$shared_src" ]; then
    for f in "$shared_src"/*.md; do
      if [ ! -f "$dst/absorbed/$(basename "$f")" ]; then
        cp "$f" "$dst/absorbed/$(basename "$f")"
        ok "Created index → $dst/absorbed/$(basename "$f")"
      else
        warn "Skipping existing: $dst/absorbed/$(basename "$f")"
      fi
    done
  fi
}

install_hermes() {
  local src="$SCRIPT_DIR/hermes"
  local hermes_config="${HERMES_CONFIG_DIR:-$HOME/.hermes/config}"

  if [ ! -d "$hermes_config" ]; then
    warn "Hermes config directory not found at $hermes_config"
    warn "Creating directory..."
    mkdir -p "$hermes_config"
  fi

  if [ -f "$src/absorb-osp.yaml" ]; then
    cp "$src/absorb-osp.yaml" "$hermes_config/absorb-osp.yaml"
    ok "Installed Hermes config → $hermes_config/absorb-osp.yaml"
  fi

  if [ -f "$src/README.md" ]; then
    cp "$src/README.md" "$hermes_config/absorb-osp-hermes.md"
    ok "Installed Hermes readme → $hermes_config/absorb-osp-hermes.md"
  fi
}

# ── Main ───────────────────────────────────────────────────────────

echo ""
echo "╔══════════════════════════════════════════╗"
echo "║     absorb-osp  Installation             ║"
echo "║     v2.0.0                               ║"
echo "╚══════════════════════════════════════════╝"
echo ""

install_claude

if [ "$INSTALL_HERMES" = true ]; then
  install_hermes
fi

echo ""
echo "╔══════════════════════════════════════════╗"
echo "║  Installation Complete!                   ║"
echo "║                                           ║"
echo "║  Next steps:                              ║"
echo "║  1. Restart your agent session            ║"
echo "║  2. Send a GitHub URL to test:            ║"
echo '║     "Absorb https://github.com/..."       ║'
echo "║                                           ║"
echo "║  Docs: $REPO_URL           ║"
echo "╚══════════════════════════════════════════╝"
echo ""
