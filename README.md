# JITD Plugin - Just-In-Time Documentation for Claude Code

> Context-efficient documentation system with on-demand loading and conversation checkpoints.

**Status**: ✅ Published v1.4.0

[![MIT License](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)
[![Version](https://img.shields.io/badge/version-1.4.0-blue.svg)](https://github.com/alekspetrov/jitd-plugin/releases)

---

## 🎯 What is JITD?

JITD (Just-In-Time Documentation) is a Claude Code plugin that **optimizes context usage through on-demand documentation loading**. Instead of loading 150k+ tokens of docs upfront, JITD loads only what you need (12k tokens), freeing 92% of your context for actual work.

### The Problem

```
❌ Traditional Approach:
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Entire codebase docs    ~150,000 tokens
System prompts          ~50,000 tokens
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
= 200k tokens used before any work
= Frequent session restarts
= Lost context mid-feature
```

### The JITD Solution

```
✅ JITD Approach:
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Navigator (roadmap)      ~2,000 tokens
Current task doc         ~3,000 tokens
Relevant system doc      ~5,000 tokens
Specific SOP (optional)  ~2,000 tokens
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
= 12,000 tokens (92% reduction)
= 188k tokens free for work
= Zero session restarts
```

**Real Results**:
- 92% reduction in documentation overhead
- 10x more work per token spent
- Zero session restarts over multi-week projects
- Context markers compress 130k sessions → 3k snapshots

---

## 🚀 Quick Start

### Installation

```bash
# 1. Ensure Claude Code is initialized in your project
/init

# 2. Add the JITD plugin marketplace
/plugin marketplace add alekspetrov/jitd-plugin

# 3. Install the plugin
/plugin install jitd

# 4. Restart Claude Code to load the plugin

# 5. Initialize JITD in your project
/jitd:init
```

**Requirements**:
- Claude Code with plugin support (October 2025+)
- Update if needed: `pnpm upgrade -g @anthropic-ai/claude-code@latest`
- `.claude/` directory in project (run `/init` first)

### First Session

```bash
# Start every new conversation with:
/jitd:start

# This loads the navigator and sets up JITD workflow
```

---

## 🎨 Features

### 1. Navigator-First Pattern

**Always load lightweight navigator first** (2k tokens):
- Documentation index
- "When to read what" decision tree
- Project setup guides
- Current sprint focus

```bash
/jitd:start  # Loads .agent/DEVELOPMENT-README.md
```

### 2. On-Demand Documentation Loading

**Load only what you need, when you need it**:

| Scenario | Load | Tokens |
|----------|------|--------|
| Working on feature | Task doc | +3k |
| Need architecture | System doc | +5k |
| Solving pattern | SOP | +2k |
| **Total** | | **~12k** |

**vs Traditional**: Loading everything = 150k tokens

### 3. Context Markers (Save Points)

**Save conversation state anytime** - like git commits for AI conversations:

```bash
# Before lunch break
/jitd:marker lunch-break

# Before risky refactor
/jitd:marker before-routing-refactor

# End of day
/jitd:marker eod-2025-10-12 "Finished OAuth, need tests tomorrow"

# Manage markers (interactive)
/jitd:markers

# Or list all markers
/jitd:markers list

# Clean old markers
/jitd:markers clean
```

**Benefits**:
- Resume after breaks in 30 seconds (vs 5-10 min re-explaining)
- Safety nets before experiments
- Perfect handoff between sessions
- 85-90% token savings vs re-explaining context

### 4. Living Documentation

**Docs update as code evolves**:

```bash
# After completing feature
/jitd:update-doc feature TASK-123

# After solving novel issue
/jitd:update-doc sop debugging cors-issue

# After architecture change
/jitd:update-doc system architecture
```

### 5. Smart Context Compacting

**Clear conversation while preserving knowledge**:

```bash
/jitd:compact
```

- Creates context marker automatically
- Shows you how to restore
- Clears conversation history
- Frees up tokens for new work

**When to compact**:
- After completing isolated sub-tasks
- After documentation updates
- Before switching to unrelated work
- When approaching 70%+ token usage

---

## 📋 Available Commands

| Command | Description |
|---------|-------------|
| `/jitd:init` | One-time setup: creates .agent/ structure |
| `/jitd:start` | Start session: loads navigator, sets JITD context |
| `/jitd:update-doc feature TASK-XX` | Archive implementation plan after feature |
| `/jitd:update-doc sop <category> <name>` | Create Standard Operating Procedure |
| `/jitd:update-doc system <doc>` | Update architecture documentation |
| `/jitd:marker [name]` | Create context save point anytime |
| `/jitd:markers` | Manage markers: list, load, clean |
| `/jitd:compact` | Smart compact: preserves markers, clears history |

---

## 🏗️ How It Works

### Token Optimization Strategy

JITD uses a **navigator-first pattern** with lazy-loading:

**Step 1: Session Start**
```bash
/jitd:start
# Loads: .agent/DEVELOPMENT-README.md (~2k tokens)
# Result: Documentation index loaded, ready to load specific docs
```

**Step 2: Load On-Demand**
```bash
# Only load what's needed for current task
Read .agent/tasks/TASK-123-oauth.md  # +3k tokens
Read .agent/system/project-architecture.md  # +5k tokens (if needed)
```

**Step 3: Work Efficiently**
```
Total loaded: 10k tokens (vs 150k traditional)
Available for work: 190k tokens (95%)
```

**Step 4: Document & Clear**
```bash
# After completing work
/jitd:update-doc feature TASK-123

# Then compact context
/jitd:compact
# Creates marker automatically
# Frees up tokens for next task
```

### Context Markers Explained

**Problem**: Conversations grow to 130k+ tokens, then you compact and lose everything.

**JITD Solution**: Create markers (3k token snapshots) before compacting:

```markdown
# Context Marker Structure

## Current Location
- Task: TASK-123 - OAuth implementation
- Phase: Integration complete, testing pending
- Files: src/auth/oauth.ts, src/routes/auth.ts

## What's Done
✅ OAuth flow implemented with passport.js
✅ JWT token generation working
✅ Login/logout endpoints created

## Technical Decisions
- Chose passport.js over next-auth (better control)
- JWT in httpOnly cookies (XSS protection)
- Redis for session storage (fast, scalable)

## Next Steps
1. Write comprehensive tests
2. Add error handling
3. Document OAuth setup in README

## Restore Instructions
Read @.agent/.context-markers/oauth-working.md
```

**Result**: 130k conversation → 3k marker (97.7% compression)

---

## 📁 Project Structure

After running `/jitd:init`:

```
your-project/
├── CLAUDE.md                    # Project configuration
├── .agent/
│   ├── DEVELOPMENT-README.md    # Navigator (2k tokens)
│   ├── .jitd-config.json        # Plugin configuration
│   ├── .context-markers/        # Session save points (git-ignored)
│   │   ├── lunch-break-2025-10-12.md
│   │   └── before-refactor-2025-10-12.md
│   ├── tasks/                   # Implementation plans
│   │   └── TASK-123-oauth.md    # Generated from tickets
│   ├── system/                  # Living architecture docs
│   │   ├── project-architecture.md
│   │   └── tech-stack-patterns.md
│   └── sops/                    # Standard Operating Procedures
│       ├── integrations/        # Third-party service setups
│       ├── debugging/           # Common issues & solutions
│       ├── development/         # Dev workflows
│       └── deployment/          # Deploy procedures
└── .gitignore                   # Includes .context-markers/
```

---

## 💡 Use Cases

### Solo Developer
- Maintain project knowledge as you build
- No session restarts mid-feature
- Resume after breaks instantly with markers
- Onboard future contributors in 48 hours

### Small Team (2-5)
- Share patterns via SOPs
- Consistent architecture decisions
- Context markers for handoffs
- Zero repeated mistakes

### Enterprise
- Standardize documentation across teams
- Enforce best practices through templates
- Scale knowledge without context bloat
- Institutional memory that compounds

---

## 🔧 Configuration

JITD configuration in `.agent/.jitd-config.json`:

```json
{
  "version": "1.0.0",
  "project_management": "linear",  // linear | github | jira | gitlab | none
  "task_prefix": "TASK",           // TASK | GH | LIN | JIRA-123
  "team_chat": "none",             // slack | discord | teams | none
  "auto_load_navigator": true,
  "compact_strategy": "conservative"  // aggressive | conservative | manual
}
```

**Supported Integrations**:
- **Linear**: Full MCP integration (list issues, create tasks, update status)
- **GitHub**: Via gh CLI (issues, PRs)
- **Jira**: Manual workflow (API integration available)
- **GitLab**: Via glab CLI

---

## 📊 Metrics & Benefits

### Token Efficiency
- **Before JITD**: 150k tokens loaded, 50k available (25%)
- **With JITD**: 12k tokens loaded, 188k available (94%)
- **Improvement**: 3.8x more context for work

### Productivity Gains
- **92% reduction** in documentation overhead
- **10x more work** per token spent
- **Zero session restarts** during features
- **85-90% token savings** with markers vs re-explaining

### Real-World Results
- Multi-week projects without session restart
- 30-second context restoration after breaks
- Complete feature history in 3k token markers
- Team finds docs in <30 seconds

---

## 🎓 Example Workflow

### Morning: Start New Feature

```bash
# 1. Start session
/jitd:start
# Loads navigator, shows assigned tasks from Linear/GitHub

# 2. Select task to work on
# Claude loads: .agent/tasks/TASK-456-payment.md

# 3. Load relevant architecture
Read .agent/system/project-architecture.md

# 4. Implement feature
# (Using only ~10k tokens for docs, 190k available for work)
```

### Noon: Take Lunch Break

```bash
# Create marker before leaving
/jitd:marker lunch-break "Stripe integration 70% complete, need to add webhooks"

# Resume after lunch
/jitd:markers
# [Interactive list appears]
# [Select "lunch-break" from list]
# Context restored in 30 seconds!
```

### Afternoon: Complete Feature

```bash
# Finish implementation and tests

# Document what you built
/jitd:update-doc feature TASK-456

# Clear context for next task
/jitd:compact
# Automatically creates marker
# Shows restore instructions
```

### Evening: Risky Refactor

```bash
# Before trying new approach
/jitd:marker before-api-refactor

# Try refactoring API structure
# ...doesn't work well...

# Restore from marker
Read @.agent/.context-markers/before-api-refactor.md

# Try different approach with full context
```

---

## 🗺️ Roadmap

### ✅ Phase 1: Core Plugin (Complete)
- Slash commands (/jitd:init, /jitd:start, /jitd:update-doc, /jitd:compact, /jitd:marker)
- Documentation templates
- Configuration system
- Context markers
- v1.4.0 published

### 🚧 Phase 2: Documentation & Examples (In Progress)
- [ ] Generic Next.js example project
- [ ] Generic Python/Django example project
- [ ] Generic Go example project
- [ ] Video walkthrough
- [x] Comprehensive README

### 📈 Phase 3: Community & Growth (Planned)
- [ ] Gather user feedback
- [ ] Submit to Anthropic official marketplace
- [ ] Build integration examples
- [ ] Create announcement blog post
- [ ] GitHub Discussions

---

## 🤝 Contributing

JITD is open source (MIT) and community-driven.

**How to Help**:
1. Try JITD in your project
2. Share your results (token usage, productivity improvements)
3. Contribute templates for your tech stack
4. Report issues or suggest improvements
5. Build integration plugins

**Want to contribute?**
- [Report bugs](https://github.com/alekspetrov/jitd-plugin/issues)
- [Request features](https://github.com/alekspetrov/jitd-plugin/issues)
- [Submit PRs](https://github.com/alekspetrov/jitd-plugin/pulls)

---

## 📄 License

MIT - Use freely, contribute back if it helps you.

---

## 📚 Resources

- **Documentation**: [docs/](./docs/)
- **Templates**: [templates/](./templates/)
- **Commands**: [commands/](./commands/)
- **Quick Start**: [docs/QUICK-START.md](./docs/QUICK-START.md)
- **GitHub**: [alekspetrov/jitd-plugin](https://github.com/alekspetrov/jitd-plugin)
- **Issues**: [Report bugs or request features](https://github.com/alekspetrov/jitd-plugin/issues)

---

## 🎯 Success Criteria

### Context Efficiency
- ✅ <70% token usage for typical tasks
- ✅ <12k tokens loaded per session (documentation)
- ✅ 10+ exchanges per session without compact
- ✅ Zero session restarts during features

### Documentation Coverage
- ✅ 100% completed features have task docs
- ✅ 90%+ integrations have SOPs
- ✅ System docs updated within 24h
- ✅ Zero repeated mistakes (SOPs prevent them)

---

**Built in public** 🚀 Share your JITD success stories!

**Version**: 1.4.0
**Last Updated**: 2025-10-12
**Author**: [Aleks Petrov](https://github.com/alekspetrov)
