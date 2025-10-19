# Navigator Plugin - Navigator for Claude Code

> Context-efficient documentation system with on-demand loading and conversation checkpoints.

**Status**: ✅ Published v2.2.0 - Self-Improving Capability

[![MIT License](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)
[![Version](https://img.shields.io/badge/version-2.2.0-blue.svg)](https://github.com/alekspetrov/navigator-plugin/releases)

---

## 🎯 What is Navigator?

Navigator (Navigator) is a Claude Code plugin that **optimizes context usage through on-demand documentation loading**. Instead of loading 150k+ tokens of docs upfront, Navigator loads only what you need (12k tokens), freeing 92% of your context for actual work.

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

### The Navigator Solution

```
✅ Navigator Approach:
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

# 2. Add the Navigator plugin marketplace
/plugin marketplace add alekspetrov/nav-plugin

# 3. Install the plugin
/plugin install jitd

# 4. Restart Claude Code to load the plugin

# 5. Initialize Navigator in your project
/nav:init
```

**Requirements**:
- Claude Code with plugin support (October 2025+)
- Update if needed: `pnpm upgrade -g @anthropic-ai/claude-code@latest`
- `.claude/` directory in project (run `/init` first)

### First Session

```bash
# Start every new conversation with:
/nav:start

# This loads the navigator and sets up Navigator workflow
```

---

## 🎨 Features

### 1. Self-Improving Capability (v2.2+) 🔄

**The plugin that generates its own tools.**

Navigator can now analyze your codebase patterns and generate project-specific skills automatically:

```bash
# Tell Navigator what pattern to automate
"Create a skill for adding API endpoints"

# nav-skill-creator auto-invokes and:
# 1. Analyzes existing endpoints in your codebase
# 2. Identifies patterns and conventions
# 3. Generates complete skill with functions
# 4. Creates templates and examples
# 5. Validates output quality

# Result: New skill ready to use!
```

**What gets generated**:
- Complete SKILL.md with instructions
- Predefined Python functions (generators, validators)
- Templates with placeholders
- Real examples from your codebase

**Token efficiency**:
- Before: Read 3-5 examples manually (~15k tokens)
- After: Skill auto-invokes (~3k tokens)
- **Savings**: 80% reduction

**Example skills**:
- `plugin-slash-command` - Generate Navigator commands (built-in)
- `frontend-component` - Generate React/Vue components (you create)
- `backend-endpoint` - Generate API endpoints (you create)
- `database-migration` - Generate schema changes (you create)

The self-improving loop: Navigator generates tools that generate more tools.

### 2. Navigator-First Pattern

**Always load lightweight navigator first** (2k tokens):
- Documentation index
- "When to read what" decision tree
- Project setup guides
- Current sprint focus

```bash
/nav:start  # Loads .agent/DEVELOPMENT-README.md
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
/nav:marker lunch-break

# Before risky refactor
/nav:marker before-routing-refactor

# End of day
/nav:marker eod-2025-10-12 "Finished OAuth, need tests tomorrow"

# Manage markers (interactive)
/nav:markers

# Or list all markers
/nav:markers list

# Clean old markers
/nav:markers clean
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
/nav:update-doc feature TASK-123

# After solving novel issue
/nav:update-doc sop debugging cors-issue

# After architecture change
/nav:update-doc system architecture
```

### 5. Smart Context Compacting

**Clear conversation while preserving knowledge**:

```bash
/nav:compact
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
| `/nav:init` | One-time setup: creates .agent/ structure |
| `/nav:start` | Start session: loads navigator, sets Navigator context |
| `/nav:update-doc feature TASK-XX` | Archive implementation plan after feature |
| `/nav:update-doc sop <category> <name>` | Create Standard Operating Procedure |
| `/nav:update-doc system <doc>` | Update architecture documentation |
| `/nav:marker [name]` | Create context save point anytime |
| `/nav:markers` | Manage markers: list, load, clean |
| `/nav:compact` | Smart compact: preserves markers, clears history |

---

## 🏗️ How It Works

### Token Optimization Strategy

Navigator uses a **navigator-first pattern** with lazy-loading:

**Step 1: Session Start**
```bash
/nav:start
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
/nav:update-doc feature TASK-123

# Then compact context
/nav:compact
# Creates marker automatically
# Frees up tokens for next task
```

### Context Markers Explained

**Problem**: Conversations grow to 130k+ tokens, then you compact and lose everything.

**Navigator Solution**: Create markers (3k token snapshots) before compacting:

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

After running `/nav:init`:

```
your-project/
├── CLAUDE.md                    # Project configuration
├── .agent/
│   ├── DEVELOPMENT-README.md    # Navigator (2k tokens)
│   ├── .nav-config.json        # Plugin configuration
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

Navigator configuration in `.agent/.nav-config.json`:

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
- **Before Navigator**: 150k tokens loaded, 50k available (25%)
- **With Navigator**: 12k tokens loaded, 188k available (94%)
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
/nav:start
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
/nav:marker lunch-break "Stripe integration 70% complete, need to add webhooks"

# Resume after lunch
/nav:markers
# [Interactive list appears]
# [Select "lunch-break" from list]
# Context restored in 30 seconds!
```

### Afternoon: Complete Feature

```bash
# Finish implementation and tests

# Document what you built
/nav:update-doc feature TASK-456

# Clear context for next task
/nav:compact
# Automatically creates marker
# Shows restore instructions
```

### Evening: Risky Refactor

```bash
# Before trying new approach
/nav:marker before-api-refactor

# Try refactoring API structure
# ...doesn't work well...

# Restore from marker
Read @.agent/.context-markers/before-api-refactor.md

# Try different approach with full context
```

---

## 🗺️ Roadmap

### ✅ Phase 1: Core Plugin (Complete)
- Slash commands (/nav:init, /nav:start, /nav:update-doc, /nav:compact, /nav:marker, /nav:markers)
- Documentation templates
- Configuration system
- Context markers with interactive management
- Auto-resume system
- Autonomous task completion
- v1.5.1 published

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

## ❓ FAQ

### General Questions

**Q: What makes Navigator different from just organizing docs well?**

A: Organization helps discoverability for humans. Navigator adds **token efficiency** for AI. Traditional well-organized docs still load 150k tokens upfront. Navigator's navigator pattern loads 2k tokens initially, then lazy-loads specific docs (3-5k each) only when needed. Result: 92% fewer tokens wasted on unused documentation.

**Q: Do I need project management tools (Linear/GitHub) to use Navigator?**

A: No. Navigator works standalone. PM integrations are optional enhancements. Set `"project_management": "none"` in `.agent/.nav-config.json` and document tasks manually from conversation context.

**Q: What's the minimum project size where Navigator makes sense?**

A: Any project with 3+ documentation files benefits. Even small projects (5-10 files) see 60-70% token reduction. Larger codebases (50+ files) achieve 90%+ savings.

**Q: Can I use Navigator with existing documentation?**

A: Yes. Run `/nav:init` to create `.agent/` structure, then migrate existing docs:
- README → `.agent/DEVELOPMENT-README.md` (navigator)
- Architecture docs → `.agent/system/`
- Setup guides → `.agent/sops/integrations/`
- Issue resolutions → `.agent/sops/debugging/`

### Token Optimization

**Q: How does Navigator calculate token usage?**

A: When you run `/nav:start`, it measures actual file sizes using `wc -c` (bytes) and calculates tokens as `bytes / 4` (standard estimation). This shows real documentation overhead, not educational guesses.

Example output:
```
Navigator: 12,282 bytes = 3,070 tokens (measured)
CLAUDE.md: 10,085 bytes = 2,521 tokens (measured)
Total documentation: 5,591 tokens
Available for work: 144,409 tokens (72%)
```

**Q: Why load navigator every session if it costs 2k tokens?**

A: Navigator is your **documentation index**. Without it, you either:
1. Load all docs (150k tokens) to find what you need, or
2. Blindly guess which docs exist (inefficient, error-prone)

2k tokens for complete documentation awareness is a 98.7% savings vs loading everything.

**Q: Does `/nav:compact` delete my work?**

A: No. It creates a **context marker** (save point) automatically, then clears conversation history. Your code, documentation, and markers remain intact. You can restore context anytime with `/nav:markers`.

**Q: How much space do context markers save?**

A: Context markers compress conversations by 85-97%:
- 30-message conversation: ~130k tokens → 3k marker (97.7% reduction)
- 10-message sub-task: ~40k tokens → 2k marker (95% reduction)

Markers extract key decisions, progress, and next steps—discarding redundant conversational back-and-forth.

### Context Markers

**Q: When should I create a marker?**

A: Create markers before:
- **Breaks** (lunch, end of day): Resume faster than re-explaining
- **Experiments** (refactors, new approaches): Safety net if it fails
- **Compacting** (automatic): Preserve context before clearing
- **Handoffs** (switching tasks): Clear boundary between work streams

**Q: How are markers different from git commits?**

A: Git commits save **code state**. Markers save **conversation state**:
- What you were working on
- Technical decisions and reasoning
- What's done vs what's pending
- Files modified and why
- Next steps

Think: Git commits are for code history, markers are for context history.

**Q: Can I load markers from old projects?**

A: Technically yes, but not recommended. Markers are **session-specific**: they reference code state, task context, and decisions from that project. Loading cross-project markers creates context mismatch. Create new markers for each project.

**Q: Do markers work across different Claude Code sessions?**

A: Yes! That's the point. Create marker in session A → start session B → run `/nav:markers` → select marker → full context restored. No need to re-explain 20 messages of context.

### Workflow

**Q: Do I have to run `/nav:start` every session?**

A: Yes. It's **mandatory** for Navigator workflow. Without it:
- Navigator not loaded (documentation index missing)
- Token optimization not active
- PM tool not checked (if configured)
- Navigator context not set

Think of it like `git status` at start of day—essential for knowing where you are.

**Q: What's "autonomous task completion"?**

A: When you finish a task, Claude **automatically**:
1. Commits changes with proper message
2. Archives implementation plan (`/nav:update-doc feature TASK-XX`)
3. Creates completion marker (`TASK-XX-complete`)
4. Suggests compact to clear context

No need to prompt "please commit now" or "update docs"—it's done autonomously once work is verified complete.

**Q: Can I skip documentation updates?**

A: You *can*, but you **shouldn't**. Documentation updates are the compounding benefit:
- Week 1: 3 features documented → 9k tokens of reusable knowledge
- Month 1: 15 features + 10 SOPs → 45k tokens (but you load 3-5k at a time)
- Year 1: Complete project knowledge base, onboard new devs in 48h

Skipping documentation is like skipping git commits—you lose the trail of why decisions were made.

**Q: How do I share Navigator docs with my team?**

A: Commit `.agent/` to git (except `.agent/.context-markers/`—those are personal session save points). Team members:
1. Pull repo
2. Install Navigator plugin
3. Run `/nav:start`
4. Instant access to all documentation, SOPs, architecture

### Technical

**Q: What's the `.agent/.context-markers/.active` file?**

A: When you run `/nav:compact`, it creates a marker and writes the filename to `.active`. Next time you run `/nav:start`, it detects the active marker and asks if you want to load it (auto-resume feature). After loading, `.active` is deleted.

**Q: Why are context markers git-ignored?**

A: Markers are **personal session save points**, not project documentation:
- Contain incomplete thoughts, experiments, failed attempts
- Specific to your work stream, not useful to team
- Would create merge conflicts (everyone has different markers)

Task docs and SOPs (in `.agent/tasks/` and `.agent/sops/`) ARE committed—they're polished documentation.

**Q: Can I customize the Navigator templates?**

A: Yes. After `/nav:init`, edit templates in `.agent/`:
- `DEVELOPMENT-README.md`: Customize navigator sections
- `.nav-config.json`: Change PM tool, task prefix, compact strategy
- Template files: Modify structures for your workflow

Changes persist across sessions. Share customizations by committing `.agent/` structure.

**Q: Does Navigator work with other AI assistants (Cursor, Copilot, etc.)?**

A: Navigator is a **Claude Code plugin**—it won't run in other tools. However, the **documentation pattern** (navigator + lazy loading + markers) works anywhere:
- Manually follow Navigator workflow
- Manually create/load `.agent/` docs
- Use bash scripts to mimic `/nav:compact` functionality

But you lose slash commands, autonomous completion, and PM integrations.

**Q: What if `/nav:start` shows "navigator not found"?**

A: Navigator isn't initialized. Run:
```bash
/nav:init
```

This creates `.agent/` structure with DEVELOPMENT-README.md. Then `/nav:start` will work.

**Q: Can I use Navigator for non-code projects (writing, research, etc.)?**

A: Yes! Navigator is a **documentation workflow**, not code-specific:
- Writing project: Task docs = chapter plans, SOPs = style guides
- Research project: Task docs = experiment logs, SOPs = methodologies
- Creative project: Task docs = scene outlines, SOPs = character bibles

Any project with evolving documentation benefits from on-demand loading and context markers.

### Troubleshooting

**Q: I ran `/nav:compact` but lost all my context—how do I recover?**

A: `/nav:compact` creates a marker automatically. Run:
```bash
/nav:markers
```

Select the most recent marker to restore context. If you want to restore immediately after compact, copy the marker filename shown in compact output and:
```bash
Read @.agent/.context-markers/[marker-name].md
```

**Q: My tokens are still high after `/nav:start`—why?**

A: Tokens accumulate from:
1. **Documentation** (shown in `/nav:start` output)
2. **Message history** (grows with conversation)
3. **Code files read** (not shown in Navigator tracking)

Navigator optimizes documentation (1). To reduce message history (2), run `/nav:compact`. To reduce code reads (3), use agents for multi-file searches instead of reading files directly.

**Q: `/nav:update-doc` created a doc I don't like—can I regenerate?**

A: Yes. Documentation is versioned with git, so you can:
1. Review the generated doc
2. Edit manually if needed
3. Or delete and run `/nav:update-doc` again with better context
4. Commit when satisfied

SOPs and task docs are living documents—iterate until they're useful.

**Q: Can I have multiple projects with different Navigator configs?**

A: Yes! Each project has its own `.agent/.nav-config.json`. Configure per project:
- Project A: Linear + Slack + aggressive compact
- Project B: GitHub + Discord + conservative compact
- Project C: No PM tool + manual workflow

Navigator detects config when you run `/nav:start` in each project directory.

---

## 🤝 Contributing

Navigator is open source (MIT) and community-driven.

**How to Help**:
1. Try Navigator in your project
2. Share your results (token usage, productivity improvements)
3. Contribute templates for your tech stack
4. Report issues or suggest improvements
5. Build integration plugins

**Want to contribute?**
- [Report bugs](https://github.com/alekspetrov/nav-plugin/issues)
- [Request features](https://github.com/alekspetrov/nav-plugin/issues)
- [Submit PRs](https://github.com/alekspetrov/nav-plugin/pulls)

---

## 📄 License

MIT - Use freely, contribute back if it helps you.

---

## 📚 Resources

- **Documentation**: [docs/](./docs/)
- **Templates**: [templates/](./templates/)
- **Commands**: [commands/](./commands/)
- **Quick Start**: [docs/QUICK-START.md](./docs/QUICK-START.md)
- **GitHub**: [alekspetrov/nav-plugin](https://github.com/alekspetrov/nav-plugin)
- **Issues**: [Report bugs or request features](https://github.com/alekspetrov/nav-plugin/issues)

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

**Built in public** 🚀 Share your Navigator success stories!

**Version**: 1.6.0
**Last Updated**: 2025-10-16
**Author**: [Aleks Petrov](https://github.com/alekspetrov)
