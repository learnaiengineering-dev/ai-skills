#!/usr/bin/env bash
# Copy skills into the folder a given tool reads.
#
# Usage: scripts/install.sh <tool> [--project] [--dry-run] [skill ...]
#   tool:      claude | agents | copilot | cursor
#              (agents = the shared .agents/skills folder read by Codex, Cursor and Copilot)
#   --project  install into the current repo instead of your home folder
#   skill      names to install; default is every skill in this repo
set -euo pipefail

ROOT="$(cd "$(dirname "$0")/.." && pwd)"
TOOL="${1:-}"
[ -n "$TOOL" ] || { sed -n '2,9p' "$0"; exit 2; }
shift

SCOPE=user
DRY=0
NAMES=()
for arg in "$@"; do
  case "$arg" in
    --project) SCOPE=project ;;
    --dry-run) DRY=1 ;;
    -*) echo "unknown option: $arg" >&2; exit 2 ;;
    *) NAMES+=("$arg") ;;
  esac
done

case "$TOOL:$SCOPE" in
  claude:user)    DEST="$HOME/.claude/skills" ;;
  claude:project) DEST=".claude/skills" ;;
  agents:user)    DEST="$HOME/.agents/skills" ;;
  agents:project) DEST=".agents/skills" ;;
  copilot:user)   DEST="$HOME/.copilot/skills" ;;
  copilot:project) DEST=".github/skills" ;;
  cursor:user)    DEST="$HOME/.cursor/skills" ;;
  cursor:project) DEST=".cursor/skills" ;;
  *) echo "unknown tool: $TOOL (use claude, agents, copilot or cursor)" >&2; exit 2 ;;
esac

if [ ${#NAMES[@]} -eq 0 ]; then
  for d in "$ROOT"/skills/*/; do NAMES+=("$(basename "$d")"); done
fi

for name in "${NAMES[@]}"; do
  src="$ROOT/skills/$name"
  [ -f "$src/SKILL.md" ] || { echo "no such skill: $name" >&2; exit 1; }
  echo "$name -> $DEST/$name"
  if [ "$DRY" -eq 0 ]; then
    mkdir -p "$DEST"
    rm -rf "${DEST:?}/$name"
    cp -R "$src" "$DEST/$name"
  fi
done
[ "$DRY" -eq 0 ] || echo "(dry run, nothing copied)"
