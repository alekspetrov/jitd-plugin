# JITD Plugin - Project Architecture

**Tech Stack**: Markdown templates, JSON configuration, Bash
**Updated**: 2025-10-10

---

## Technology Stack

### Core Technologies
- **Markdown**: Documentation templates
- **JSON**: Plugin manifest and configuration
- **Bash**: Slash command scripts (implicit in .md commands)
- **Git**: Version control and distribution

### Claude Code Plugin System
- **Marketplace**: `.claude-plugin/marketplace.json`
- **Commands**: `.claude/commands/*.md`
- **Templates**: `templates/*.md`

---

## Project Structure

```
jitd-plugin/
├── .claude-plugin/              # Plugin manifest for marketplace
│   ├── marketplace.json         # Plugin config (version, metadata)
│   └── README.md                # Marketplace description
│
├── commands/                    # Slash commands (note: commands/ not .claude/commands/)
│   ├── jitd-init.md            # Initialize JITD in project (one-time)
│   ├── jitd-start.md           # Start JITD session (every conversation)
│   ├── update-doc.md           # Maintain documentation
│   └── jitd-compact.md         # Smart context compact
│
├── templates/                   # Universal templates
│   ├── CLAUDE.md                # Project configuration template
│   ├── DEVELOPMENT-README.md    # Navigator template
│   ├── task-template.md         # Feature planning
│   ├── sop-template.md          # Process documentation
│   └── system-template.md       # Architecture docs
│
├── docs/                        # User guides
│   ├── QUICK-START.md           # 5-minute setup
│   ├── CONFIGURATION.md         # All options
│   └── DEPLOYMENT.md            # Publishing guide
│
├── .agent/                      # JITD for this repo (meta!)
│   ├── DEVELOPMENT-README.md    # Development navigator
│   ├── tasks/                   # Feature implementation plans
│   ├── system/                  # Architecture docs
│   └── sops/                    # Development SOPs
│
├── CLAUDE.md                    # JITD configuration for this repo
├── README.md                    # Master roadmap
└── .gitignore                   # Proper excludes
```

---

## Key Components

### 1. Plugin Manifest (`.claude-plugin/marketplace.json`)

```json
{
  "name": "jitd-marketplace",
  "metadata": {
    "version": "1.3.0"  // Update on release
  },
  "plugins": [
    {
      "name": "jitd",
      "version": "1.3.0",  // Keep in sync with metadata.version
      "repository": "https://github.com/alekspetrov/jitd-plugin"
    }
  ]
}
```

**Purpose**: Defines plugin for Claude Code marketplace

**Update when**: Releasing new version

### 2. Slash Commands (`.claude/commands/*.md`)

**Format**:
```markdown
---
description: Short description
---

# Command Title

Instructions for Claude to execute...
```

**Location**: `.claude/commands/command-name.md`

**Invocation**: `/command-name` in Claude Code

**Current Commands**:
- `/jitd-init` → Initialize JITD structure in user project (one-time setup)
- `/jitd-start` → Start JITD session (EVERY new conversation) **NEW in v1.3.0**
- `/update-doc` → Maintain documentation (feature|sop|system)
- `/jitd-compact` → Smart context compact

### 3. Templates (`templates/*.md`)

**Purpose**: Copied to user projects during `/jitd-init`

**Design Principles**:
- Universal (no project-specific content)
- Placeholder-based (`[Project Name]`, `[Tech Stack]`)
- Customizable sections marked clearly
- Examples for common stacks (Next.js, Django, Go)

**Templates**:
- `CLAUDE.md` → Project configuration (~15k tokens when filled)
- `DEVELOPMENT-README.md` → Navigator (~2k tokens)
- `task-template.md` → Feature planning
- `sop-template.md` → Process documentation
- `system-template.md` → Architecture documentation

### 4. Documentation (`docs/*.md`)

**Purpose**: User-facing guides

**Files**:
- `QUICK-START.md` → 5-minute installation and usage
- `CONFIGURATION.md` → All configuration options
- `DEPLOYMENT.md` → How to publish plugin

**Target Audience**: Plugin users, not developers

---

## Development Workflow

### Local Testing

```bash
# 1. Make changes to plugin repo
cd ~/Projects/startups/jitd-plugin
vim templates/CLAUDE.md  # or other file

# 2. Test in jitd-test project
cd ~/Projects/tmp/jitd-test

# 3. Point to local plugin
/plugin marketplace add file:///Users/aleks.petrov/Projects/startups/jitd-plugin

# 4. Reinstall and test
/plugin install jitd
/jitd-init  # or other command

# 5. Verify results
ls -la .agent/
cat CLAUDE.md
```

### Release Process

**Semantic Versioning**:
- Patch (1.0.1): Bug fixes, docs updates
- Minor (1.1.0): New features, new templates
- Major (2.0.0): Breaking changes

**Steps**:
1. Update `marketplace.json` version (both locations)
2. Commit changes
3. Push to GitHub
4. Tag release: `git tag -a v1.1.0 -m "..."`
5. Push tag: `git push origin v1.1.0`
6. Create GitHub release (optional)

---

## Plugin Distribution

### GitHub Repository
- **URL**: https://github.com/alekspetrov/jitd-plugin
- **License**: MIT
- **Public**: Yes

### Installation by Users

```bash
# Add marketplace
/plugin marketplace add alekspetrov/jitd-plugin

# Install plugin
/plugin install jitd

# Use commands
/jitd-init
```

### Caching Issues

**Problem**: GitHub CDN caches for hours

**Solutions**:
- Specific commit: `alekspetrov/jitd-plugin#789bd4e`
- Local file: `file:///path/to/jitd-plugin`
- Wait 1-2 hours for CDN refresh

---

## Configuration System

### Plugin Config (`.agent/.jitd-config.json`)

Created during `/jitd-init` in user projects:

```json
{
  "version": "1.0.0",
  "project_management": "none",  // linear|github|jira|gitlab|none
  "task_prefix": "TASK",
  "team_chat": "none",  // slack|discord|teams|none
  "auto_load_navigator": true,
  "compact_strategy": "conservative"
}
```

**Purpose**: User project configuration

**Not committed to plugin repo**: Generated per-project

---

## Code Quality Standards

- **Templates**: Max 400 lines, universal content only
- **Commands**: Clear step-by-step instructions
- **Documentation**: Examples for common use cases
- **No project-specific content**: Keep templates generic

---

## Testing Strategy

### Manual Testing Checklist

- [ ] `/jitd-init` creates complete structure
- [ ] CLAUDE.md generated in project root
- [ ] DEVELOPMENT-README.md in .agent/
- [ ] System docs generated
- [ ] Config file created
- [ ] All placeholders customizable
- [ ] Templates work for different stacks

### Test Projects

- `/Users/aleks.petrov/Projects/tmp/jitd-test` → Clean test environment

---

## Token Optimization

### Plugin Repo (This Codebase)
- CLAUDE.md: ~15k tokens
- .agent/DEVELOPMENT-README.md: ~2k tokens
- System docs: ~3k tokens each
- **Total**: ~23k tokens (on-demand loading)

### User Projects (After `/jitd-init`)
- CLAUDE.md: ~15k tokens (auto-loaded by Claude Code)
- .agent/DEVELOPMENT-README.md: ~2k tokens (read first)
- System docs: ~5k tokens each (lazy-loaded)
- **Total**: ~17-27k tokens depending on task

---

## Performance Metrics

### Plugin Efficiency
- Template count: 5
- Slash commands: 4 (added /jitd-start in v1.3.0)
- Plugin size: <60KB
- Install time: <5 seconds

### User Impact
- Setup time: 2 minutes (`/jitd-init`)
- Token reduction: 92% (12k vs 150k)
- Context available: 86%+
- Session restarts: 0

---

## Future Enhancements

### Potential Features
- [ ] Integration-specific plugins (jitd-linear, jitd-slack)
- [ ] Example projects (Next.js, Python, Go)
- [ ] Video walkthrough
- [ ] Blog post and announcement
- [ ] Submit to Anthropic official marketplace

### Extensibility
- Modular integration plugins
- Community-contributed templates
- Framework-specific extensions

---

**Last Updated**: 2025-10-12
**Version**: 1.3.0
