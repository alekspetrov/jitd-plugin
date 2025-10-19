# Navigator Plugin - Development Documentation Navigator

**Project**: Claude Code plugin for Navigator
**Tech Stack**: Markdown templates, JSON configuration, Bash slash commands, Python functions
**Updated**: 2025-10-19

---

## 🚀 Quick Start for Development

### New to This Project?
**Read in this order:**
1. [Project Architecture](./system/project-architecture.md) - Plugin structure, templates
2. [Plugin Development Patterns](./system/plugin-patterns.md) - Claude Code plugin best practices

### Working on Plugin Features?
1. Check if similar task exists in [`tasks/`](#implementation-plans-tasks)
2. Read relevant system docs from [`system/`](#system-architecture-system)
3. Check for integration SOPs in [`sops/`](#standard-operating-procedures-sops)
4. Test changes in `/Users/aleks.petrov/Projects/tmp/nav-test`

### Fixing a Bug?
1. Check [`sops/debugging/`](#debugging) for known issues
2. Review relevant system docs for context
3. After fixing, create SOP: `/nav:update-doc sop debugging [issue-name]`

---

## 🤖 Task Completion Protocol (CRITICAL)

### Autonomous Completion Expected

Navigator projects run in **full autonomy mode**. When task implementation is complete:

✅ **Execute automatically** (no human prompt needed):
1. **Commit changes** with conventional commit message
2. **Archive implementation plan** (`/nav:update-doc feature TASK-XX`)
3. **Close ticket** in PM tool (if configured)
4. **Create completion marker** (`TASK-XX-complete`)
5. **Suggest compact** for next task

❌ **Don't wait for**:
- "Please commit now"
- "Close the ticket"
- "Update documentation"
- "Create a marker"

### Exception Cases (Ask First)

Only interrupt autonomous flow if:
- Uncommitted files contain secrets (.env, credentials, API keys)
- Multiple unrelated tasks modified (unclear which to close)
- No task context loaded (ambiguous TASK-XX)
- Tests failing or implementation incomplete

### Completion Summary Template

```
✅ TASK-XX Complete

Automated actions:
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
✅ Committed: [hash] [message]
✅ Documentation: Implementation plan archived
✅ Ticket: Closed in [PM tool]
✅ Marker: TASK-XX-complete created
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Next: Run /nav:compact to clear context
```

**For detailed protocol**: See [`sops/development/autonomous-completion.md`](#autonomous-completion)

---

## 📂 Documentation Structure

```
.agent/
├── DEVELOPMENT-README.md     ← You are here (navigator)
│
├── tasks/                    ← Implementation plans
│   └── TASK-01-session-start-pm-integration.md
│
├── system/                   ← Living architecture documentation
│   ├── project-architecture.md
│   └── plugin-patterns.md
│
└── sops/                     ← Standard Operating Procedures
    ├── integrations/         # (Not applicable for this project)
    ├── debugging/            # Plugin issues and solutions (none yet)
    ├── development/          # Development workflows
    │   └── plugin-release-workflow.md
    └── deployment/           # Publishing to GitHub (none yet)
```

---

## 📖 Documentation Index

### Implementation Plans (`tasks/`)

#### [TASK-01: Session Start Command and PM Integration](./tasks/TASK-01-session-start-pm-integration.md)
**Status**: ✅ Completed (v1.3.0)
**Completed**: 2025-10-12

**What was built**:
- New `/nav:start` command for session initialization
- Enhanced `/nav:init` with PM tool auto-configuration (Step 6.5)
- Linear MCP and GitHub CLI detection with setup guidance
- Auto-generated integration SOPs
- Stronger CLAUDE.md enforcement of Navigator workflow

**Impact**: Dramatically improved onboarding UX and consistent Navigator adoption

#### [TASK-02: README Overhaul & Context Markers](./tasks/TASK-02-readme-markers-v1.4.0.md)
**Status**: ✅ Completed (v1.4.0)
**Completed**: 2025-10-12

**What was built**:
- New `/nav:marker` command for on-demand conversation save points
- Updated `/nav:init` with `.context-markers/` setup and .gitignore
- Comprehensive README.md rewrite with clear feature explanations
- Token optimization strategy documented step-by-step
- Context markers explained with examples (97.7% compression)

**Impact**: Crystal-clear plugin value proposition, users understand Navigator in 30 seconds

#### [TASK-03: Interactive Marker Management + Auto-Resume](./tasks/TASK-03-markers-management-auto-resume.md)
**Status**: ✅ Completed (v1.5.0)
**Completed**: 2025-10-12

**What was built**:
- New `/nav:markers` command for interactive marker management (list, load, clean)
- Active marker auto-resume system (.active file + /nav:start detection)
- Performance optimizations (<1s for 50+ markers)
- Updated `/nav:compact` to create active markers
- Updated `/nav:start` to auto-detect and load active markers

**Impact**: One-command resume after compact (vs 3 manual steps), visual marker selection

#### [TASK-04: Version Sync Fix & Release Process](./tasks/TASK-04-version-sync-release-process.md)
**Status**: ✅ Completed (v1.5.0 docs)
**Completed**: 2025-10-13

**What was built**:
- Fixed README.md version references (1.4.0 → 1.5.0)
- Created Version Management SOP with audit script
- Enhanced Plugin Release Workflow with mandatory version sync step
- Created missing GitHub releases (v1.3.0, v1.4.0, v1.5.0)
- Systematic checklist to prevent future version drift

**Impact**: Zero version drift prevention, professional release quality, clear process for contributors

#### [TASK-05: Autonomous Task Completion](./tasks/TASK-05-autonomous-completion.md)
**Status**: ✅ Completed (v1.5.1)
**Completed**: 2025-10-13

**What was built**:
- Updated CLAUDE.md with autonomous completion protocol
- Updated DEVELOPMENT-README.md with Task Completion Protocol
- Created Autonomous Completion SOP (sops/development/)
- Modified Development Workflow to show [AUTONOMOUS] completion
- Enforced "no wait for prompts" behavior via Forbidden Actions

**Impact**: Fully autonomous task completion - no more "please commit" or "close ticket" prompts needed

#### [TASK-06: Real Session Statistics from Claude Code Internals](./tasks/TASK-06-session-statistics.md)
**Status**: ✅ Completed (v1.6.0)
**Completed**: 2025-10-16

**What was built**:
- session_stats.py script to extract real token usage from Claude Code internals
- Proof of Navigator efficiency with actual measurements (not estimates)
- Integration with /nav:start command to show cache performance
- Real-world validation of 92% token reduction claim

**Impact**: Concrete proof of Navigator's token efficiency, verified cache performance metrics

#### [TASK-07: Skills Migration Strategy](./tasks/TASK-07-skills-migration.md)
**Status**: ✅ Completed (v2.0.0)
**Completed**: 2025-10-19

**What was built**:
- 5 core Navigator skills (nav-start, nav-marker, nav-compact, nav-task, nav-sop)
- Skills registered in plugin.json with auto-invocation capability
- Hybrid architecture: Both commands and skills work simultaneously
- Foundation for progressive disclosure (250 token overhead)

**Impact**: Natural language invocation, auto-detection, zero breaking changes for v1.x users

#### [TASK-08: Skills Enhancements & Hybrid Architecture](./tasks/TASK-08-skills-enhancements-v2.1.md)
**Status**: ✅ Completed (v2.1.0)
**Completed**: 2025-10-19

**What was built**:
- Predefined functions for nav-task (task_id_generator.py, task_formatter.py, index_updater.py)
- Predefined functions for nav-sop (sop_formatter.py)
- Predefined functions for nav-marker (marker_compressor.py)
- nav-skill-creator skill (self-improving capability)
- Functions execute with 0 tokens (no context pollution)

**Impact**: Consistent output via templates, self-improving system, foundation for v2.2 project-specific skills

#### [TASK-09: Plugin Update Migration System](./tasks/TASK-09-migration-system.md)
**Status**: ✅ Completed (v2.0.0)
**Completed**: 2025-10-19

**What was built**:
- Backward compatibility commands (_jitd_*.md) for smooth v1→v2 transition
- Post-install script for automatic project migration discovery
- Config migration (.jitd-config.json → .nav-config.json)
- Zero breaking changes for existing users

**Impact**: Smooth migration path, old commands work with warnings, automatic upgrade detection

#### [TASK-10: Project-Specific Skills Generation](./tasks/TASK-10-project-skills-v2.2.md)
**Status**: ✅ Completed (v2.2.0)
**Completed**: 2025-10-19

**What was built**:
- Completed nav-skill-creator implementation (531 lines with comprehensive instructions)
- Generated plugin-slash-command skill (first project-specific skill)
- Predefined functions: command_generator.py, command_validator.py
- Templates and examples for slash command generation
- Self-improving capability validated on Navigator codebase

**Impact**: Self-improving plugin that generates its own tools, 80% token reduction for command creation, repeatable pattern for any project

#### [TASK-11: Project-Specific Skills Generation v2.3](./tasks/TASK-11-project-skills-generation-v2.3.md)
**Status**: ✅ Completed (v2.3.0)
**Completed**: 2025-10-19

**What was built**:
- Generated 5 project-specific skills for common development patterns
- frontend-component skill (React/Vue components with tests and styles)
- backend-endpoint skill (REST/GraphQL APIs with validation)
- database-migration skill (Schema changes with rollbacks)
- backend-test skill (Unit/integration tests with mocks)
- frontend-test skill (Component tests with RTL)
- Total: 12 skills (7 core + 5 project-specific)

**Impact**: 80% token reduction for common dev patterns (15k → 3k tokens), validates self-improving capability at scale, proven repeatable skill generation process

#### [TASK-12: v3.0 Skills-Only Migration](./tasks/TASK-12-v3.0-skills-only.md)
**Status**: 🚧 In Progress (v3.0.0)
**Started**: 2025-10-19

**What's being built**:
- Remove all slash commands (/nav:* deleted)
- Skills-only architecture (natural language interface)
- Breaking change migration (v3.0 major version)
- 11k token reduction (commands overhead eliminated)
- Cleaner architecture (no hybrid complexity)

**Impact**: Natural language only, simpler UX, 11k additional token savings, future-proof architecture

---

### System Architecture (`system/`)

#### [Project Architecture](./system/project-architecture.md)
**When to read**: Starting work on plugin, understanding structure

**Contains**:
- Plugin file structure
- Template system organization
- Slash command implementations
- Configuration schema
- Development workflow

**Updated**: Every major architecture change

#### [Plugin Development Patterns](./system/plugin-patterns.md)
**When to read**: Adding new features or commands

**Contains**:
- Claude Code plugin best practices
- Template design patterns
- Slash command patterns
- Testing strategies

**Updated**: When adding new patterns

---

### Standard Operating Procedures (`sops/`)

#### Development

##### [Version Management](./sops/development/version-management.md)
**When to use**: Before every release, auditing version consistency

**Contains**:
- Single source of truth (marketplace.json)
- Version reference map (9 locations)
- Pre-release checklist with audit script
- Semantic versioning guide
- Troubleshooting version mismatches

**Last Updated**: 2025-10-13

##### [Plugin Release Workflow](./sops/development/plugin-release-workflow.md)
**When to use**: Releasing new plugin version

**Contains**:
- **Step 0: Pre-Release Version Sync (MANDATORY)**
- Semantic versioning guide
- Step-by-step release process
- Git tag and GitHub release creation
- Troubleshooting common issues
- Complete release checklist

**Last Used**: v1.5.0 (2025-10-13)

##### [Autonomous Completion](./sops/development/autonomous-completion.md)
**When to use**: Understanding how to complete tasks autonomously

**Contains**:
- Autonomous completion protocol (7 steps)
- Exception handling (secrets, multiple tasks, no context, test failures)
- Completion summary template
- Integration with PM tools and markers
- Best practices for fully autonomous workflow

**Last Updated**: 2025-10-13

#### Integrations
*No SOPs yet - this project doesn't integrate with external services*

#### Debugging
*No SOPs yet - document issues as they're discovered*

#### Deployment
*No SOPs yet - currently using manual GitHub releases*

---

## 🔄 When to Read What

### Scenario: Adding New Slash Command

**Read order**:
1. This navigator (DEVELOPMENT-README.md)
2. `system/plugin-patterns.md` → Command structure
3. Check existing commands in `.claude/commands/`
4. Implement new command
5. Test in nav-test project
6. Document: `/nav:update-doc feature TASK-XX`

### Scenario: Adding New Template

**Read order**:
1. This navigator
2. `system/project-architecture.md` → Template location
3. Check existing templates in `templates/`
4. Create new template
5. Update `/nav:init` command to copy it
6. Test in nav-test project
7. Document: `/nav:update-doc feature TASK-XX`

### Scenario: Fixing Plugin Installation Issues

**Read order**:
1. Check `sops/debugging/` → Known installation issues?
2. `system/project-architecture.md` → Plugin manifest
3. Debug issue
4. Create SOP: `/nav:update-doc sop debugging [issue-name]`

### Scenario: Releasing New Plugin Version

**Read order**:
1. This navigator (DEVELOPMENT-README.md)
2. `sops/development/plugin-release-workflow.md` → Complete process
3. Follow checklist step-by-step
4. Document: `/nav:update-doc feature TASK-XX`
5. Update SOP with lessons learned

---

## 🛠️ Development Workflow

### Local Development Setup

```bash
# 1. Clone repo
git clone https://github.com/alekspetrov/nav-plugin.git
cd nav-plugin

# 2. Create test project
mkdir -p ~/Projects/tmp/nav-test
cd ~/Projects/tmp/nav-test

# 3. Point to local plugin (for testing)
# In Claude Code:
/plugin marketplace add file:///Users/aleks.petrov/Projects/startups/nav-plugin
/plugin install jitd
```

### Making Changes

```bash
# 1. Read navigator first
Read .agent/DEVELOPMENT-README.md

# 2. Make changes to plugin files
# - Templates: templates/
# - Commands: .claude/commands/
# - Config: .claude-plugin/marketplace.json

# 3. Test in nav-test project
cd ~/Projects/tmp/nav-test
/nav:init  # or other command you're testing

# 4. Verify changes work
ls .agent/  # Check structure created
cat CLAUDE.md  # Check file generated

# 5. Document changes
/nav:update-doc feature TASK-XX
```

### Release Process

```bash
# 1. Update version in marketplace.json
# - Patch: 1.0.1 (bug fix)
# - Minor: 1.1.0 (new feature)
# - Major: 2.0.0 (breaking change)

# 2. Commit changes
git add -A
git commit -m "feat: description"

# 3. Push to GitHub
git push origin main

# 4. Tag release
git tag -a v1.1.0 -m "Version 1.1.0: Feature X"
git push origin v1.1.0

# 5. Create GitHub release (optional)
gh release create v1.1.0 --title "Navigator v1.1.0" --notes "..."
```

---

## 📊 Token Optimization Strategy

**This repo follows Navigator principles**:

1. **Always load**: `DEVELOPMENT-README.md` (~2k tokens)
2. **Load for current work**: Specific system doc (~3k tokens)
3. **Load if needed**: Specific SOP (~2k tokens)
4. **Never load**: All templates at once (~20k tokens)

**Total**: ~7k tokens vs ~35k (80% savings)

---

## 🎯 Success Metrics

### Plugin Quality
- [ ] All templates follow universal pattern
- [ ] Slash commands work in test project
- [ ] Documentation is accurate
- [ ] Examples provided for common use cases

### Token Efficiency
- [ ] <30k tokens per development session
- [ ] Navigator-first loading practiced
- [ ] `/nav:compact` used between tasks

### User Experience
- [ ] `/nav:init` creates complete structure
- [ ] Templates easy to customize
- [ ] Documentation clear and helpful

---

## 🚀 Quick Natural Language Reference

Navigator v3.0 uses natural language - no commands needed!

**Initialize Navigator**:
```
"Initialize Navigator in this project"
```

**Update documentation**:
```
"Archive TASK-XX documentation"
"Create an SOP for debugging [issue]"
"Update system architecture documentation"
```

**Smart compact**:
```
"Clear context and preserve markers"
```

---

**This documentation system keeps plugin development context-efficient while maintaining comprehensive knowledge.**

**Last Updated**: 2025-10-19 (v3.0.0)
**Powered By**: Navigator (Skills-Only Architecture)
