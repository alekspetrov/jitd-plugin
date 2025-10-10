# JITD Plugin Deployment Guide

How to deploy JITD to Claude Code marketplace and make it available to users.

---

## Understanding Claude Code Marketplaces

### What is a Marketplace?

A **marketplace** is a Git repository (usually GitHub) that hosts Claude Code plugins. It contains:
- Plugin files (`.claude/` folder)
- Plugin manifest (`.claude-plugin/marketplace.json`)
- Documentation (README, guides)

### How Marketplaces Work

```
GitHub Repo (jitd-plugin)
    ↓
Contains .claude-plugin/marketplace.json
    ↓
Users add marketplace: /plugin marketplace add user/repo
    ↓
Users install plugin: /plugin install jitd
    ↓
Plugin files copied to user's project
```

**Key insight**: The marketplace IS just a GitHub repository. No special hosting needed!

---

## Deployment Options

### Option 1: Official JITD Marketplace (Recommended)

**Setup**: Host as standalone marketplace

**Repository structure**:
```
github.com/alekspetrov/jitd-plugin
├── .claude-plugin/
│   ├── marketplace.json
│   └── README.md
├── .claude/commands/
├── templates/
├── docs/
└── README.md
```

**How users install**:
```bash
# Add marketplace
/plugin marketplace add alekspetrov/jitd-plugin

# Install plugin
/plugin install jitd

# Use plugin
/jitd-init
```

**Benefits**:
- Direct control over plugin
- Simple user experience
- Can update independently

### Option 2: Submit to Anthropic's Official Marketplace

**Repository**: `anthropics/claude-code`

**Process**:
1. Fork anthropics/claude-code
2. Add JITD to their plugins/
3. Submit PR
4. Wait for review/approval

**How users install**:
```bash
# Marketplace pre-added (official)
/plugin install jitd
```

**Benefits**:
- Appears in official marketplace
- Higher visibility
- Anthropic endorsement

**Trade-offs**:
- Requires approval
- Slower updates (PR review)
- Must meet Anthropic's standards

### Option 3: Multi-Plugin Marketplace

**Setup**: Create marketplace with multiple plugins

**Repository structure**:
```
github.com/alekspetrov/claude-plugins
├── .claude-plugin/
│   └── marketplace.json  # Lists all plugins
├── jitd/
│   ├── .claude/
│   └── templates/
├── other-plugin/
│   └── ...
└── README.md
```

**Benefits**:
- Host multiple plugins
- Users add marketplace once
- Can bundle related plugins

---

## Step-by-Step Deployment

### Step 1: Create GitHub Repository

**Option A: Via GitHub Website**
1. Go to github.com/new
2. Repository name: `jitd-plugin`
3. Description: "Just-In-Time Documentation plugin for Claude Code"
4. Public (recommended for community)
5. Don't initialize (we have existing code)
6. Create repository

**Option B: Via GitHub CLI**
```bash
cd /Users/aleks.petrov/Projects/startups/jitd-plugin

# Create repo
gh repo create alekspetrov/jitd-plugin \
  --public \
  --description "Just-In-Time Documentation plugin for Claude Code - 92% token reduction" \
  --source=. \
  --push
```

### Step 2: Push Code to GitHub

```bash
cd /Users/aleks.petrov/Projects/startups/jitd-plugin

# Add remote
git remote add origin https://github.com/alekspetrov/jitd-plugin.git

# Push
git push -u origin main
```

### Step 3: Verify Marketplace File

Ensure `.claude-plugin/marketplace.json` is correct:

```json
{
  "name": "jitd",
  "displayName": "JITD - Just-In-Time Documentation",
  "version": "1.0.0",
  "description": "Context-efficient documentation system...",
  "repository": {
    "type": "git",
    "url": "https://github.com/alekspetrov/jitd-plugin"  // Update this!
  }
}
```

**Update repository URL** to your actual GitHub repo.

### Step 4: Create GitHub Release (Optional but Recommended)

```bash
# Tag version
git tag -a v1.0.0 -m "Initial release: JITD plugin"
git push origin v1.0.0

# Create release via GitHub CLI
gh release create v1.0.0 \
  --title "JITD v1.0.0 - Initial Release" \
  --notes "$(cat <<'EOF'
# JITD v1.0.0 - Just-In-Time Documentation

First public release of JITD plugin for Claude Code.

## Features
- 92% reduction in documentation loading overhead
- Navigator-first pattern for context efficiency
- Slash commands: /jitd-init, /update-doc, /jitd-compact
- Universal templates for any tech stack
- Optional integrations: Linear, Jira, GitHub, Slack, Discord

## Installation
\`\`\`bash
/plugin marketplace add alekspetrov/jitd-plugin
/plugin install jitd
/jitd-init
\`\`\`

## Metrics from Production Testing
- 10x productivity improvement (commits per token)
- Zero session restarts over 2-week test period
- 86%+ context available for actual work

See README.md for complete documentation.
EOF
)"
```

### Step 5: Test Installation

In a **different project**, test the installation:

```bash
# Add your marketplace
/plugin marketplace add alekspetrov/jitd-plugin

# Install plugin
/plugin install jitd

# Verify files copied
ls .claude/commands/
# Should show: jitd-init.md, update-doc.md, jitd-compact.md

# Test initialization
/jitd-init
```

### Step 6: Update Main README

Ensure main README has installation instructions:

```markdown
## Installation

\`\`\`bash
# Add JITD marketplace
/plugin marketplace add alekspetrov/jitd-plugin

# Install plugin
/plugin install jitd

# Initialize in your project
/jitd-init
\`\`\`
```

---

## Marketplace Configuration

### marketplace.json Anatomy

```json
{
  "name": "jitd",                    // Plugin identifier (lowercase, no spaces)
  "displayName": "JITD - Just-In-Time Documentation",  // Shown to users
  "version": "1.0.0",                // Semantic versioning
  "description": "...",              // Short description

  "author": {
    "name": "Aleks Petrov",
    "url": "https://github.com/alekspetrov"
  },

  "repository": {
    "type": "git",
    "url": "https://github.com/alekspetrov/jitd-plugin"  // Must match actual repo!
  },

  "license": "MIT",

  "keywords": [                      // For search/discovery
    "documentation",
    "context-management",
    "token-optimization"
  ],

  "capabilities": {                  // What plugin provides
    "slash_commands": [...],
    "hooks": {...}
  },

  "configuration": {...},            // User-configurable options

  "requirements": {
    "claude_code": ">=1.0.0"         // Minimum version
  },

  "examples": [...],                 // Example projects

  "support": {                       // Help resources
    "docs": "https://github.com/alekspetrov/jitd-plugin/blob/main/docs/README.md",
    "issues": "https://github.com/alekspetrov/jitd-plugin/issues"
  }
}
```

### Required Fields

Must have:
- `name` - Plugin ID
- `version` - Semantic version
- `description` - What it does
- `repository.url` - Where it's hosted

### Optional but Recommended

- `author` - Credits
- `license` - Legal clarity
- `keywords` - Discoverability
- `support` - Help users
- `examples` - Show usage

---

## User Installation Flow

### What Happens When User Installs

```bash
# User runs:
/plugin marketplace add alekspetrov/jitd-plugin
```

Claude Code:
1. Fetches `https://github.com/alekspetrov/jitd-plugin`
2. Reads `.claude-plugin/marketplace.json`
3. Registers marketplace as "alekspetrov/jitd-plugin"

```bash
# User runs:
/plugin install jitd
```

Claude Code:
1. Looks up `jitd` in registered marketplaces
2. Finds it in `alekspetrov/jitd-plugin`
3. Copies these files to user's project:
   - `.claude/commands/` → User's `.claude/commands/`
   - `templates/` → Available for reference
   - `CLAUDE.md` → User's project (optional)

```bash
# User runs:
/jitd-init
```

Plugin:
1. Runs `.claude/commands/jitd-init.md`
2. Creates `.agent/` structure
3. Copies templates from plugin
4. User's project now has JITD

---

## Updating the Plugin

### Publish New Version

```bash
# Update version in marketplace.json
vim .claude-plugin/marketplace.json
# Change: "version": "1.1.0"

# Commit changes
git add .
git commit -m "feat: add feature X (v1.1.0)"
git push

# Tag new version
git tag -a v1.1.0 -m "Version 1.1.0: Add feature X"
git push origin v1.1.0

# Create GitHub release
gh release create v1.1.0 --title "JITD v1.1.0" --notes "..."
```

### User Updates

**Option 1: Manual**
```bash
/plugin update jitd
```

**Option 2: Reinstall**
```bash
/plugin uninstall jitd
/plugin install jitd
```

---

## Multi-Plugin Marketplace Setup

If you want to host multiple plugins:

### Structure

```
github.com/alekspetrov/claude-plugins/
├── .claude-plugin/
│   └── marketplace.json          # Lists all plugins
├── jitd/
│   ├── .claude-plugin/
│   │   └── plugin.json           # JITD plugin manifest
│   ├── .claude/commands/
│   └── templates/
├── another-plugin/
│   └── ...
└── README.md
```

### Marketplace manifest

`.claude-plugin/marketplace.json`:
```json
{
  "name": "alekspetrov-plugins",
  "displayName": "Aleks Petrov's Claude Plugins",
  "version": "1.0.0",
  "plugins": [
    {
      "name": "jitd",
      "path": "jitd/",
      "version": "1.0.0"
    },
    {
      "name": "another-plugin",
      "path": "another-plugin/",
      "version": "1.0.0"
    }
  ]
}
```

### User installs

```bash
/plugin marketplace add alekspetrov/claude-plugins
/plugin install jitd
/plugin install another-plugin
```

---

## Distribution Channels

### 1. Direct GitHub (Primary)

**URL**: `https://github.com/alekspetrov/jitd-plugin`

**Installation**:
```bash
/plugin marketplace add alekspetrov/jitd-plugin
```

**Best for**: Full control, fast updates

### 2. Anthropic Official Marketplace

**URL**: `https://github.com/anthropics/claude-code`

**Installation**:
```bash
# Marketplace pre-added
/plugin install jitd
```

**Best for**: Maximum visibility, official endorsement

### 3. Community Marketplaces

**Example**: Seth Hobson's marketplace (mentioned in article)

**Installation**:
```bash
/plugin marketplace add seth-hobson/claude-code
/plugin install jitd  # If he includes it
```

**Best for**: Reaching specific communities

---

## Marketing & Promotion

### GitHub Repository

**README.md badges**:
```markdown
![Version](https://img.shields.io/badge/version-1.0.0-blue)
![License](https://img.shields.io/badge/license-MIT-green)
![Claude Code](https://img.shields.io/badge/claude--code-plugin-orange)
```

**Topics**: Add GitHub topics for discovery
- claude-code
- documentation
- context-management
- productivity
- ai-tools

### Twitter/LinkedIn

Use tweet from `JITD-TWEET.md` (Option 0 - Experiment):

```
Experimenting with Just-In-Time Documentation (JITD) for @AnthropicAI Claude Code.

Goal: Cut token usage, improve performance by loading docs on-demand
instead of everything upfront.

Early results: 92% less loading overhead (12k vs 150k tokens)

Following this experiment in real-time 🧪

Install: /plugin marketplace add alekspetrov/jitd-plugin
```

### Blog Post

Write blog post covering:
- The problem (context overflow)
- The experiment (2-week test)
- The results (10x productivity)
- How to use (installation + workflow)
- Open source invitation

---

## Monetization (Optional)

### Free Core + Paid Extensions

**Free** (Open Source):
- Core JITD plugin
- Basic templates
- Documentation

**Paid** (Separate marketplace):
- Enterprise templates
- Custom integrations
- Priority support
- Team training

### Sponsorship

Add GitHub Sponsors:
- `.github/FUNDING.yml`
- Link in README
- "Buy me a coffee" button

---

## Support & Maintenance

### Issue Template

Create `.github/ISSUE_TEMPLATE/bug_report.md`:

```markdown
**Describe the bug**
A clear description of what the bug is.

**To Reproduce**
Steps to reproduce:
1. Run `/plugin install jitd`
2. Run `/jitd-init`
3. See error...

**Expected behavior**
What you expected to happen.

**Environment**
- Claude Code version: [e.g., 1.0.0]
- OS: [e.g., macOS 14.0]
- JITD version: [e.g., 1.0.0]
```

### Contributing Guide

Create `CONTRIBUTING.md`:
- How to submit PRs
- Code style guide
- Testing requirements
- Documentation standards

---

## Metrics to Track

### GitHub Analytics

- Stars (measure interest)
- Forks (measure adoption)
- Issues (measure engagement)
- Traffic (measure reach)

### Plugin Usage (if trackable)

- Installations
- Active users
- Command usage (/jitd-init, /update-doc, etc.)

### Community Feedback

- GitHub Discussions
- Twitter mentions
- Blog comments
- Direct messages

---

## Deployment Checklist

**Before Publishing**:
- [ ] Update `.claude-plugin/marketplace.json` with correct repo URL
- [ ] Test installation in clean project
- [ ] Verify all slash commands work
- [ ] Complete documentation (README, guides)
- [ ] Create GitHub release
- [ ] Add installation instructions to README

**After Publishing**:
- [ ] Announce on Twitter
- [ ] Post in relevant communities (HN, Reddit, etc.)
- [ ] Write blog post
- [ ] Submit to Anthropic (if desired)
- [ ] Monitor issues/feedback

**Ongoing**:
- [ ] Respond to issues within 24h
- [ ] Merge PRs after review
- [ ] Release updates regularly
- [ ] Share success stories
- [ ] Grow community

---

## Quick Commands Reference

```bash
# Create GitHub repo
gh repo create alekspetrov/jitd-plugin --public --source=. --push

# Tag version
git tag -a v1.0.0 -m "Initial release"
git push origin v1.0.0

# Create release
gh release create v1.0.0 --title "JITD v1.0.0" --notes "..."

# Test installation
/plugin marketplace add alekspetrov/jitd-plugin
/plugin install jitd
/jitd-init

# Update plugin
git commit -m "feat: new feature (v1.1.0)"
git tag -a v1.1.0 -m "Version 1.1.0"
git push origin v1.1.0
```

---

**Ready to deploy**: Follow steps above to publish JITD to GitHub and make it available to the world! 🚀

**Support**: Issues at https://github.com/alekspetrov/jitd-plugin/issues
