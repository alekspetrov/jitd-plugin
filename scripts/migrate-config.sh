#!/bin/bash
# Navigator Config Migration Script
# Migrates .jitd-config.json → .nav-config.json
# Usage: ./migrate-config.sh /path/to/project

set -e

PROJECT_ROOT="${1:-.}"
AGENT_DIR="$PROJECT_ROOT/.agent"

# Colors
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

echo -e "${BLUE}🔄 Navigator Config Migration${NC}"
echo ""

# Check if .agent directory exists
if [ ! -d "$AGENT_DIR" ]; then
    echo -e "${YELLOW}⏭️  No .agent directory found in $PROJECT_ROOT${NC}"
    echo "This doesn't appear to be a Navigator project."
    exit 0
fi

# Check for old config
OLD_CONFIG="$AGENT_DIR/.jitd-config.json"
NEW_CONFIG="$AGENT_DIR/.nav-config.json"

if [ ! -f "$OLD_CONFIG" ]; then
    if [ -f "$NEW_CONFIG" ]; then
        echo -e "${GREEN}✅ Already migrated${NC}"
        echo "Using: .nav-config.json"
    else
        echo -e "${YELLOW}⏭️  No config file found${NC}"
        echo "Run /nav:init to create config"
    fi
    exit 0
fi

# Handle both configs present
if [ -f "$OLD_CONFIG" ] && [ -f "$NEW_CONFIG" ]; then
    echo -e "${YELLOW}⚠️  Both .jitd-config.json and .nav-config.json found${NC}"
    echo ""
    echo "Comparing files..."

    if diff -q "$OLD_CONFIG" "$NEW_CONFIG" > /dev/null 2>&1; then
        echo -e "${GREEN}Files are identical${NC}"
        echo ""
        echo "Safe to remove old config? [Y/n]"
        read -r response

        if [[ "$response" =~ ^([yY][eE][sS]|[yY]|)$ ]]; then
            rm "$OLD_CONFIG"
            echo -e "${GREEN}✅ Removed .jitd-config.json${NC}"
        else
            echo -e "${YELLOW}⏭️  Keeping both files (you can remove .jitd-config.json manually)${NC}"
        fi
    else
        echo -e "${RED}Files are different${NC}"
        echo ""
        echo "Please manually resolve:"
        echo "  1. Compare: diff $OLD_CONFIG $NEW_CONFIG"
        echo "  2. Keep one, remove the other"
        echo "  3. Or merge changes manually"
    fi
    exit 0
fi

# Migrate old config to new config
echo -e "${BLUE}Found old config:${NC} .jitd-config.json"
echo -e "${BLUE}Migrating to:${NC}     .nav-config.json"
echo ""

# Show current config
echo -e "${YELLOW}Current config:${NC}"
cat "$OLD_CONFIG"
echo ""

# Confirm migration
echo "Proceed with migration? [Y/n]"
read -r response

if [[ ! "$response" =~ ^([yY][eE][sS]|[yY]|)$ ]]; then
    echo -e "${YELLOW}⏭️  Migration cancelled${NC}"
    exit 0
fi

# Perform migration
echo ""
echo -e "${BLUE}Migrating...${NC}"

# Copy old config to new location
cp "$OLD_CONFIG" "$NEW_CONFIG"

# Update version to 2.0.0 if it's 1.0.0
if grep -q '"version": "1.0.0"' "$NEW_CONFIG"; then
    # macOS compatible sed
    sed -i '' 's/"version": "1\.0\.0"/"version": "2.0.0"/' "$NEW_CONFIG"
    echo -e "${GREEN}  ✓${NC} Updated version: 1.0.0 → 2.0.0"
fi

# Remove old config
rm "$OLD_CONFIG"
echo -e "${GREEN}  ✓${NC} Renamed: .jitd-config.json → .nav-config.json"

echo ""
echo -e "${GREEN}✅ Migration complete!${NC}"
echo ""
echo -e "${YELLOW}New config:${NC}"
cat "$NEW_CONFIG"
echo ""

echo -e "${BLUE}📝 Next steps:${NC}"
echo "  1. Review changes: git diff"
echo "  2. Update documentation: /nav:migrate (in Claude Code)"
echo "  3. Commit: git add .agent && git commit -m 'chore: migrate to Navigator v2.0'"
echo ""
echo -e "${YELLOW}💡 Note:${NC} Old commands (/jitd:*) still work but are deprecated"
echo "         Update to new commands: /jitd:start → /nav:start"
