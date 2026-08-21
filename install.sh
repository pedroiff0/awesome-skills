#!/usr/bin/env bash
# ==============================================================================
# awesome-skills — Universal Multi-Agent Installer
# Write once in SKILL.md — Run on all AI Agents (AGY, Claude, Hermes, Cursor, Windsurf, Roo, OpenCode)
# ==============================================================================

set -e

# Detect if Python 3 is available
if ! command -v python3 >/dev/null 2>&1; then
    echo "Error: python3 is required to run the awesome-skills installer." >&2
    exit 1
fi

# Detect repository location
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" 2>/dev/null && pwd)"

# If running directly from git clone
if [ -d "$SCRIPT_DIR/skills" ] && [ -f "$SCRIPT_DIR/tools/installer.py" ]; then
    REPO_DIR="$SCRIPT_DIR"
else
    # Running via curl / piped bash: clone or update temporary/cache directory
    CACHE_DIR="${HOME}/.cache/awesome-skills"
    if [ ! -d "$CACHE_DIR/.git" ]; then
        echo "Cloning awesome-skills repository to $CACHE_DIR..."
        mkdir -p "$CACHE_DIR"
        git clone --depth 1 https://github.com/pedroiff0/awesome-skills.git "$CACHE_DIR"
    else
        echo "Updating awesome-skills cache in $CACHE_DIR..."
        git -C "$CACHE_DIR" pull --ff-only || true
    fi
    REPO_DIR="$CACHE_DIR"
fi

# Execute installer python engine
exec python3 "$REPO_DIR/tools/installer.py" "$@"
