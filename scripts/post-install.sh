#!/bin/bash
# Navigator Plugin Post-Install Hook
# Called automatically by Claude Code after plugin install/update
# Scans for old JITD projects and offers migration

set -e

PLUGIN_DIR="$(cd "$(dirname "$0")/.." && pwd)"
PLUGIN_VERSION=$(grep -o '"version": "[^"]*"' "$PLUGIN_DIR/.claude-plugin/marketplace.json" | cut -d'"' -f4)

# Colors
BLUE='\033[0;34m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

echo -e "${BLUE}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
echo -e "${BLUE}🔧 Navigator Plugin Post-Install (v$PLUGIN_VERSION)${NC}"
echo -e "${BLUE}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
echo ""

# Function to migrate a single project
migrate_project() {
    local project_dir="$1"
    local agent_dir="$project_dir/.agent"

    # Skip if no .agent directory
    [ ! -d "$agent_dir" ] && return

    # Check for old config
    if [ -f "$agent_dir/.jitd-config.json" ] && [ ! -f "$agent_dir/.nav-config.json" ]; then
        echo ""
        echo -e "${YELLOW}📦 Navigator project found:${NC} $(basename "$project_dir")"
        echo -e "${YELLOW}🔄 Migration needed:${NC} .jitd-config.json detected"
        echo ""
        echo "   Path: $project_dir"
        echo ""
        echo "Migrate automatically? [Y/n]"
        read -r response

        if [[ "$response" =~ ^([yY][eE][sS]|[yY]|)$ ]]; then
            # Run migration
            bash "$PLUGIN_DIR/scripts/migrate-config.sh" "$project_dir"

            echo ""
            echo -e "${GREEN}💡 Tip:${NC} Run '/nav:migrate' in Claude Code to update documentation"
            echo ""
        else
            echo -e "${YELLOW}⏭️  Skipped migration for $(basename "$project_dir")${NC}"
            echo -e "${BLUE}💡 Run '/nav:migrate' in Claude Code when ready${NC}"
            echo ""
        fi
    fi
}

# Find all Navigator projects in common locations
echo -e "${BLUE}🔍 Scanning for Navigator projects...${NC}"
echo ""

FOUND_COUNT=0

# Scan ~/Projects (customize based on user's workspace)
if [ -d "$HOME/Projects" ]; then
    while IFS= read -r -d '' config_file; do
        project_dir="$(dirname "$(dirname "$config_file")")"
        migrate_project "$project_dir"
        ((FOUND_COUNT++))
    done < <(find "$HOME/Projects" -maxdepth 5 -name ".jitd-config.json" -print0 2>/dev/null)
fi

# Also check current directory if in a project
if [ -f "./.agent/.jitd-config.json" ]; then
    migrate_project "."
    ((FOUND_COUNT++))
fi

if [ $FOUND_COUNT -eq 0 ]; then
    echo -e "${GREEN}✅ No migration needed${NC}"
    echo "   All Navigator projects are up to date"
    echo ""
fi

echo -e "${BLUE}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
echo -e "${GREEN}✅ Post-install complete${NC}"
echo -e "${BLUE}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
echo ""
echo -e "${BLUE}📚 Documentation:${NC} https://github.com/alekspetrov/navigator-plugin"
echo -e "${BLUE}💬 Issues:${NC} https://github.com/alekspetrov/navigator-plugin/issues"
echo ""
