#!/usr/bin/env bash
# ==============================================================================
# awesome-skills — Universal Multi-Agent Installer (Cosmic Purple Dev Edition)
# ☕ Fresh Cosmic Brew • Write once in SKILL.md • Run across all AI Agents 🪐 🌌
# ==============================================================================

set -e

PURPLE="\033[38;5;141m"
NEBULA="\033[38;5;183m"
COSMIC_GREEN="\033[38;5;120m"
GOLD="\033[38;5;220m"
CYAN="\033[38;5;87m"
RESET="\033[0m"
BOLD="\033[1m"
DIM="\033[2m"

# ------------------------------------------------------------------------------
# 1. OS Detection & Compatibility Dispatcher
# ------------------------------------------------------------------------------
OS_TYPE="$(uname -s 2>/dev/null || echo "Unknown")"
case "${OS_TYPE}" in
    Linux*)
        DETECTED_OS="🐧 Linux (Tier 1 Primary Platform)"
        ;;
    Darwin*)
        DETECTED_OS="🍎 macOS (Darwin - Paths & Defaults Adapted)"
        ;;
    CYGWIN*|MINGW*|MSYS*)
        DETECTED_OS="🪟 Windows (POSIX Emulation - Paths Adapted)"
        ;;
    *)
        DETECTED_OS="🌐 Other/Unix (${OS_TYPE})"
        ;;
esac

# Detect if Python 3 is available
if ! command -v python3 >/dev/null 2>&1; then
    echo -e "${GOLD}⚠️  Error:${RESET} python3 is required to run the awesome-skills installer." >&2
    echo -e "${DIM}Please install Python 3.8+ on your system and try again.${RESET}" >&2
    exit 1
fi

# Detect repository location
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" 2>/dev/null && pwd)"

if [ -d "$SCRIPT_DIR/skills" ] && [ -f "$SCRIPT_DIR/tools/installer.py" ]; then
    REPO_DIR="$SCRIPT_DIR"
else
    CACHE_DIR="${HOME}/.cache/awesome-skills"
    if [ ! -d "$CACHE_DIR/.git" ]; then
        echo -e "${PURPLE}🪐 Brewing cosmic environment... Cloning awesome-skills to ${CACHE_DIR}...${RESET}"
        mkdir -p "$CACHE_DIR"
        git clone --depth 1 https://github.com/pedroiff0/awesome-skills.git "$CACHE_DIR"
    else
        echo -e "${PURPLE}✨ Checking constellation updates...${RESET}"
        git -C "$CACHE_DIR" pull --ff-only 2>/dev/null || true
    fi
    REPO_DIR="$CACHE_DIR"
fi

# Print OS Detection Telemetry
echo -e "${DIM}🛰️  OS Detection:${RESET} ${CYAN}${DETECTED_OS}${RESET} ${DIM}• Primary Verified: Linux${RESET}"

# If stdin is not a terminal (e.g. piped via curl | bash), re-attach to /dev/tty if available
if [ -t 0 ]; then
    exec python3 "$REPO_DIR/tools/installer.py" "$@"
elif [ -r /dev/tty ]; then
    exec python3 "$REPO_DIR/tools/installer.py" "$@" </dev/tty
else
    exec python3 "$REPO_DIR/tools/installer.py" "$@"
fi
