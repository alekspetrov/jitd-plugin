#!/bin/bash
# Navigator Multi-Claude Workflow Installer
# Installs scripts and verifies dependencies

set -euo pipefail

# Colors
GREEN='\033[0;32m'
BLUE='\033[0;34m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m'

echo -e "${BLUE}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
echo -e "${BLUE}Navigator Multi-Claude Workflow Installer${NC}"
echo -e "${BLUE}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
echo ""

# Check if we're in a git repository
if [ ! -d ".git" ]; then
  echo -e "${RED}❌ Error: Not in a git repository${NC}"
  echo "Please run this script from the root of your project"
  exit 1
fi

echo -e "${BLUE}📋 Checking prerequisites...${NC}"
echo ""

# Check for claude CLI
if ! command -v claude &> /dev/null; then
  echo -e "${RED}❌ claude CLI not found${NC}"
  echo "Install Claude Code from: https://claude.com/code"
  exit 1
else
  echo -e "${GREEN}✅ claude CLI found${NC}"
fi

# Check for git
if ! command -v git &> /dev/null; then
  echo -e "${RED}❌ git not found${NC}"
  exit 1
else
  echo -e "${GREEN}✅ git found${NC}"
fi

# Check for jq
if ! command -v jq &> /dev/null; then
  echo -e "${YELLOW}⚠️  jq not found (optional)${NC}"
  echo "   Install with: brew install jq (macOS) or apt-get install jq (Linux)"
else
  echo -e "${GREEN}✅ jq found${NC}"
fi

# Check for gh CLI (optional)
if ! command -v gh &> /dev/null; then
  echo -e "${YELLOW}⚠️  gh CLI not found (optional)${NC}"
  echo "   PR creation will be skipped without gh CLI"
  echo "   Install from: https://cli.github.com/"
else
  echo -e "${GREEN}✅ gh CLI found${NC}"

  # Check gh auth status
  if gh auth status &> /dev/null; then
    echo -e "${GREEN}✅ gh CLI authenticated${NC}"
  else
    echo -e "${YELLOW}⚠️  gh CLI not authenticated${NC}"
    echo "   Run: gh auth login"
  fi
fi

echo ""
echo -e "${BLUE}📦 Installing Multi-Claude Workflow...${NC}"
echo ""

# Create scripts directory if it doesn't exist
mkdir -p scripts

# Check if script already exists locally
if [ -f "scripts/navigator-multi-claude.sh" ]; then
  echo -e "${GREEN}✅ Multi-Claude script already present${NC}"
else
  # Try to download from GitHub
  SCRIPT_URL="https://raw.githubusercontent.com/alekspetrov/navigator/main/scripts/navigator-multi-claude.sh"

  if command -v curl &> /dev/null; then
    echo "Downloading navigator-multi-claude.sh..."
    if curl -fsSL "$SCRIPT_URL" -o scripts/navigator-multi-claude.sh 2>/dev/null; then
      echo -e "${GREEN}✅ Script downloaded${NC}"
    else
      echo -e "${YELLOW}⚠️  Could not download from GitHub${NC}"
      echo "Please manually copy scripts/navigator-multi-claude.sh to this directory"
      exit 1
    fi
  elif command -v wget &> /dev/null; then
    echo "Downloading navigator-multi-claude.sh..."
    if wget -q "$SCRIPT_URL" -O scripts/navigator-multi-claude.sh 2>/dev/null; then
      echo -e "${GREEN}✅ Script downloaded${NC}"
    else
      echo -e "${YELLOW}⚠️  Could not download from GitHub${NC}"
      echo "Please manually copy scripts/navigator-multi-claude.sh to this directory"
      exit 1
    fi
  else
    echo -e "${RED}❌ Neither curl nor wget found${NC}"
    echo "Please install curl or wget and try again"
    exit 1
  fi
fi

# Make script executable
chmod +x scripts/navigator-multi-claude.sh

# Create .agent directory structure if it doesn't exist
echo ""
echo -e "${BLUE}📁 Setting up Navigator directory structure...${NC}"
mkdir -p .agent/tasks
mkdir -p .agent/system
mkdir -p .agent/sops

echo -e "${GREEN}✅ Directory structure created${NC}"

# Create example task file
if [ ! -f ".agent/tasks/TASK-example.md" ]; then
  cat > .agent/tasks/TASK-example.md << 'EOF'
# TASK-1: Example Task

**Status**: 📋 Todo
**Priority**: Low
**Assignee**: Claude

## Context

This is an example task file. Replace with your actual task.

## Requirements

1. Requirement one
2. Requirement two
3. Requirement three

## Acceptance Criteria

- [ ] Criterion one met
- [ ] Criterion two met
- [ ] Tests passing
EOF

  echo -e "${GREEN}✅ Example task created: .agent/tasks/TASK-example.md${NC}"
fi

echo ""
echo -e "${GREEN}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
echo -e "${GREEN}✅ Installation Complete!${NC}"
echo -e "${GREEN}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
echo ""
echo "Next steps:"
echo ""
echo "1. Create a task file:"
echo -e "   ${BLUE}cat > .agent/tasks/TASK-1-my-feature.md${NC}"
echo ""
echo "2. Run the workflow:"
echo -e "   ${BLUE}./scripts/navigator-multi-claude.sh TASK-1-my-feature${NC}"
echo ""
echo "3. Monitor progress:"
echo -e "   ${BLUE}tail -f .agent/tasks/task-1-my-feature-*-plan.md${NC}"
echo ""
echo "Documentation: https://github.com/alekspetrov/navigator#multi-claude-workflow"
echo ""
