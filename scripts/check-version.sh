#!/bin/bash
#
# Navigator Version Checker
#
# Checks if user is running latest version and prompts to update if outdated.
#
# Usage:
#   ./scripts/check-version.sh
#
# Returns:
#   0 - Up to date
#   1 - Update available
#   2 - Error (cannot check)

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PLUGIN_DIR="$(dirname "$SCRIPT_DIR")"

# Colors for output
RED='\033[0;31m'
YELLOW='\033[1;33m'
GREEN='\033[0;32m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Get current version from plugin.json
get_current_version() {
    if [ -f "$PLUGIN_DIR/.claude-plugin/plugin.json" ]; then
        grep -o '"version"[[:space:]]*:[[:space:]]*"[^"]*"' "$PLUGIN_DIR/.claude-plugin/plugin.json" | \
            cut -d'"' -f4
    else
        echo "unknown"
    fi
}

# Get latest version from GitHub
get_latest_version() {
    # Try GitHub API first
    local latest_version=$(curl -s https://api.github.com/repos/alekspetrov/navigator/releases/latest | \
        grep '"tag_name":' | \
        sed -E 's/.*"v([^"]+)".*/\1/')

    if [ -n "$latest_version" ]; then
        echo "$latest_version"
        return 0
    fi

    # Fallback: check plugin.json in main branch
    local fallback_version=$(curl -s https://raw.githubusercontent.com/alekspetrov/navigator/main/.claude-plugin/plugin.json | \
        grep -o '"version"[[:space:]]*:[[:space:]]*"[^"]*"' | \
        cut -d'"' -f4)

    if [ -n "$fallback_version" ]; then
        echo "$fallback_version"
        return 0
    fi

    # Cannot determine latest version
    return 1
}

# Compare versions (returns 0 if v1 < v2, 1 otherwise)
version_lt() {
    local v1=$1
    local v2=$2

    # Remove 'v' prefix if present
    v1=${v1#v}
    v2=${v2#v}

    # Use sort -V for version comparison
    printf '%s\n%s\n' "$v1" "$v2" | sort -V -C || return 0
    return 1
}

# Main execution
main() {
    local current_version=$(get_current_version)

    if [ "$current_version" = "unknown" ]; then
        echo -e "${RED}⚠️  Cannot determine current Navigator version${NC}"
        echo "   Expected: .claude-plugin/plugin.json"
        return 2
    fi

    echo -e "${BLUE}🔍 Checking Navigator version...${NC}"
    echo -e "   Current: ${GREEN}v$current_version${NC}"

    local latest_version=$(get_latest_version)

    if [ $? -ne 0 ] || [ -z "$latest_version" ]; then
        echo -e "${YELLOW}⚠️  Cannot check for updates (network issue or GitHub API limit)${NC}"
        echo "   You can manually check: https://github.com/alekspetrov/navigator/releases"
        return 2
    fi

    echo -e "   Latest:  ${GREEN}v$latest_version${NC}"
    echo

    if version_lt "$current_version" "$latest_version"; then
        # Update available
        echo -e "${YELLOW}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
        echo -e "${YELLOW}📦 Update Available: v$current_version → v$latest_version${NC}"
        echo -e "${YELLOW}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
        echo
        echo -e "${BLUE}What's new in v$latest_version:${NC}"
        echo "   See: https://github.com/alekspetrov/navigator/releases/tag/v$latest_version"
        echo
        echo -e "${GREEN}To update Navigator:${NC}"
        echo '   Say: "Update Navigator"'
        echo "   Or run: cd $PLUGIN_DIR && git pull origin main"
        echo
        echo -e "${YELLOW}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
        return 1
    else
        # Up to date
        echo -e "${GREEN}✅ Navigator is up to date!${NC}"
        return 0
    fi
}

# Execute
main "$@"
