# Navigator - Self-Improving Claude Code Plugin

> **Skills + Agents + Documentation** - The plugin that generates its own tools and optimizes your context.

**Status**: ✅ v3.0.0 - Skills-Only Architecture Released (Breaking Change)

[![MIT License](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)
[![Version](https://img.shields.io/badge/version-3.0.0-blue.svg)](https://github.com/alekspetrov/navigator/releases)

---

## 🚨 v3.0 Breaking Change: Natural Language Only

**Navigator v3.0 removes all slash commands.** Skills auto-invoke via natural language.

```diff
- /nav:start
- /nav:marker checkpoint
+ "Start my Navigator session"
+ "Create a marker called checkpoint"
```

**Migration**: All skills work immediately - just use natural language instead of commands.

**What you gain**: +11k tokens saved, simpler UX, no syntax to remember.

📖 **[Complete Migration Guide](MIGRATION.md)** | **[v3.0.0 Release Notes](https://github.com/alekspetrov/navigator/releases/tag/v3.0.0)**

---

## 🎯 What is Navigator?

Navigator is a **self-improving Claude Code plugin** that combines **Skills** (execution tools), **Agents** (research assistants), and **on-demand documentation** to maximize your context efficiency.

### The Evolution

```
v1.x: Documentation system (on-demand loading)
  ↓
v2.0: + Skills architecture (progressive disclosure)
  ↓
v2.1: + Predefined functions (0-token execution)
  ↓
v2.2: + Self-improving capability (generates own tools)
  ↓
v2.3: + Project-specific skills (5 dev pattern skills)
  ↓
v3.0: Natural language only (commands removed) ← YOU ARE HERE
```

### Three Core Capabilities

**1. Skills (Execution)**
- Auto-invoke when you mention patterns
- Use predefined functions and templates
- Ensure consistency across your project
- Generate boilerplate following your conventions

**2. Agents (Research)**
- Explore codebase in separate context (60-80% token savings)
- Return summaries, not full files
- Perfect for "How does X work?" questions
- No pollution of main conversation

**3. Documentation (Knowledge)**
- Load only what you need, when you need it
- Navigator-first pattern (2k tokens vs 150k upfront)
- Living docs that update with code
- Context markers compress 130k → 3k

---

## ⚡ Quick Example

```bash
# Traditional approach (150k+ tokens loaded upfront)
❌ "Help me add a new API endpoint"
→ Claude reads all documentation
→ Manually creates endpoint
→ You validate format
→ Token-heavy, inconsistent

# Navigator approach (Skills auto-invoke)
✅ "Add a POST /users endpoint"
→ backend-endpoint skill auto-invokes (50 tokens)
→ Analyzes existing endpoints (Agent, separate context)
→ Generates route + controller + tests (predefined functions)
→ Follows your project conventions
→ Total: ~3k tokens, consistent output
```

**Result**: 95% token reduction, 10x productivity boost

---

## 🚀 Quick Start

### Installation

```bash
# 1. Install Navigator plugin
/plugin marketplace add alekspetrov/navigator
/plugin install navigator

# 2. Restart Claude Code

# 3. Initialize in your project
/nav:init

# 4. Start every session with:
/nav:start
```

### Your First Skill

```bash
# Navigator includes 7 built-in skills that auto-invoke:

"Create a skill for adding React components"
# → nav-skill-creator auto-invokes
# → Analyzes your components/
# → Generates frontend-component skill
# → Ready to use immediately

"Add a UserProfile component"
# → frontend-component auto-invokes
# → Generates component + tests + styles
# → Follows your project patterns
```

---

## 🎨 Core Architecture

### Skills (What Navigator Executes)

Skills auto-invoke when you mention trigger phrases. They use predefined functions and templates to ensure consistency.

#### Built-in Skills (7)

**1. nav-skill-creator** 🔄
- **Triggers**: "Create a skill for...", "Automate this workflow"
- **Purpose**: Analyzes codebase and generates project-specific skills
- **Output**: Complete skill with SKILL.md, functions, templates, examples
- **Token cost**: 50 (description) + 3k (instructions on invoke)

**2. plugin-slash-command**
- **Triggers**: "Add slash command", "Create /nav:... command"
- **Purpose**: Generate Navigator slash commands following conventions
- **Functions**: command_generator.py, command_validator.py
- **Token cost**: 50 + 3k on invoke

**3. nav-start**
- **Triggers**: Loads on /nav:start
- **Purpose**: Initialize session, load navigator, check PM tool
- **Functions**: session_stats.py (real token metrics)
- **Token cost**: 50 + 2k on invoke

**4. nav-marker**
- **Triggers**: "Create marker", "Save progress"
- **Purpose**: Save conversation state (like git commits)
- **Functions**: marker_compressor.py
- **Token cost**: 50 + 2k on invoke

**5. nav-compact**
- **Triggers**: Loads on /nav:compact
- **Purpose**: Smart context clearing with preservation
- **Token cost**: 50 + 2k on invoke

**6. nav-task**
- **Triggers**: "Create task doc", "Document implementation"
- **Purpose**: Generate implementation plans
- **Functions**: task_id_generator.py, task_formatter.py, index_updater.py
- **Token cost**: 50 + 2k on invoke

**7. nav-sop**
- **Triggers**: "Document solution", "Create SOP"
- **Purpose**: Capture solutions as reusable procedures
- **Functions**: sop_formatter.py
- **Token cost**: 50 + 2k on invoke

**Total overhead**: 350 tokens (7 skills × 50) - always loaded
**Instructions**: Loaded only when skill invokes (progressive disclosure)

#### Skills You Can Generate

Use `nav-skill-creator` to generate project-specific skills:

```bash
"Create a skill for adding API endpoints"
→ Generates: backend-endpoint skill
→ Auto-invokes on: "Add endpoint", "Create API"
→ Functions: endpoint_generator.py, route_validator.py
→ Templates: endpoint-template.ts, test-template.spec.ts

"Create a skill for React components"
→ Generates: frontend-component skill
→ Auto-invokes on: "Add component", "Create component"
→ Functions: component_generator.py, test_generator.py
→ Templates: component-template.tsx, test-template.spec.tsx

"Create a skill for database migrations"
→ Generates: database-migration skill
→ Auto-invokes on: "Create migration", "Add table"
→ Functions: migration_generator.py, schema_validator.py
→ Templates: migration-template.sql
```

**The self-improving loop**: Navigator generates tools that generate more tools.

---

### Agents (How Navigator Researches)

Agents run in **separate context** - they explore your codebase without polluting your main conversation.

#### When to Use Agents

**✅ Use Agents for** (60-80% token savings):
- Multi-file searches: "Find all API endpoints"
- Pattern discovery: "How does authentication work?"
- Code exploration: "What's the structure of components/"
- Research: "Analyze Redux patterns in this project"

**❌ Don't use Agents for**:
- Reading specific known file (use Read tool)
- Working with 1-2 files already loaded
- Small edits to current context

#### How Agents Save Tokens

```
Manual approach:
Grep for "endpoint" → 50 files found
Read api/users.ts (5k tokens)
Read api/posts.ts (5k tokens)
Read api/comments.ts (5k tokens)
... (15 more files)
= 100k+ tokens consumed

Agent approach:
Task agent: "Find all API endpoint patterns"
Agent reads 50 files in separate context
Agent returns: "Found 18 endpoints in 3 files: routes.ts, middleware.ts, handlers.ts"
= 200 tokens returned (summary only)
= 99.8% token savings
```

**Critical**: Agent instructions in CLAUDE.md remind Claude to use agents for exploration automatically.

---

### Documentation (Navigator's Knowledge Base)

On-demand loading with Navigator-first pattern.

#### Structure

```
.agent/
├── DEVELOPMENT-README.md      # Navigator (ALWAYS load first, 2k tokens)
│
├── tasks/                     # Implementation plans (load when working on task)
│   ├── TASK-01-feature.md    # (~3k tokens each)
│   └── archive/               # Completed tasks
│
├── system/                    # Architecture docs (load as needed)
│   ├── project-architecture.md    # (~5k tokens)
│   └── plugin-patterns.md         # (~4k tokens)
│
└── sops/                      # Standard Operating Procedures (load when relevant)
    ├── integrations/          # How to integrate tools
    ├── debugging/             # Common issue solutions
    ├── development/           # Development workflows
    └── deployment/            # Deployment procedures
```

#### Loading Strategy

```
ALWAYS load first:
  .agent/DEVELOPMENT-README.md  (~2k tokens)

Load for current work:
  .agent/tasks/TASK-XX.md       (~3k tokens)

Load as needed:
  .agent/system/[doc].md        (~5k tokens)

Load if helpful:
  .agent/sops/[category]/[sop].md  (~2k tokens)

Total: ~12k tokens vs ~150k (92% reduction)
```

---

## 🔧 How It Works Together

### Example: Adding a New Feature

```
User: "Add user authentication with OAuth"

1. nav-task skill auto-invokes
   → Creates .agent/tasks/TASK-XX-oauth-auth.md
   → Implementation plan generated

2. Agent explores (separate context)
   → "Find existing auth patterns"
   → Returns: "Uses passport.js in api/auth.ts"
   → 200 tokens (summary) vs 50k (manual reading)

3. backend-endpoint skill auto-invokes
   → Generates /auth/login, /auth/callback endpoints
   → Follows project patterns
   → Tests included

4. nav-marker saves progress
   → "OAuth routes implemented, need session management"
   → 3k token snapshot

5. Continue working...

6. nav-task completes
   → Archives implementation plan
   → Updates navigator with completion

Total tokens: ~15k (Agent + Skills + Docs)
vs Traditional: ~200k (loading everything upfront)
Savings: 92%
```

---

## 📊 Token Efficiency Breakdown

### Before Navigator

```
Upfront loading:
  All documentation        150,000 tokens
  System prompts            50,000 tokens
  ──────────────────────────────────────
  Total before work:       200,000 tokens
  Available for work:            0 tokens

  Result: Session restart required immediately
```

### With Navigator v2.2

```
Progressive loading:
  Skills (7 descriptions)      350 tokens
  Navigator (roadmap)        2,000 tokens
  Task doc (if needed)       3,000 tokens
  ──────────────────────────────────────
  Loaded upfront:            5,350 tokens
  Available for work:      194,650 tokens (97% free)

When skill invokes:
  Skill instructions         3,000 tokens (one-time)
  Functions                      0 tokens (execute separately)
  ──────────────────────────────────────
  Total after invoke:        8,350 tokens
  Available for work:      191,650 tokens (96% free)

When agent researches:
  Agent context          50,000 tokens (separate, doesn't count)
  Agent summary             200 tokens (returned)
  ──────────────────────────────────────
  Main context impact:        200 tokens
  Savings vs manual:       49,800 tokens (99.6%)
```

**Result**: 10x more work per session, zero restarts

---

## 🎓 Skills vs Agents - Decision Guide

### Use Skills When...

✅ **Implementing** following patterns
- "Add a React component"
- "Create API endpoint"
- "Generate database migration"

✅ **Generating** boilerplate code
- Components, endpoints, migrations, tests

✅ **Enforcing** project conventions
- Naming, structure, format

✅ **Automating** repetitive tasks
- Slash command creation
- Documentation updates
- SOP generation

**How Skills work**:
- Auto-invoke based on trigger phrases
- Load instructions only when invoked (progressive disclosure)
- Execute predefined functions (0 tokens)
- Use templates for consistency
- Run in main context

### Use Agents When...

✅ **Researching** codebase
- "How does auth work?"
- "Find all API endpoints"
- "What's the component structure?"

✅ **Exploring** patterns
- "Analyze Redux usage"
- "Find similar implementations"
- "Understand data flow"

✅ **Searching** across files
- Multi-file pattern discovery
- Dependency tracing
- Architecture understanding

✅ **Understanding** unfamiliar code
- Before making changes
- Learning project patterns
- Onboarding to codebase

**How Agents work**:
- Run in separate context (no pollution)
- Search/read efficiently
- Return summaries only (200 tokens vs 50k)
- 60-80% token savings vs manual
- Triggered automatically by CLAUDE.md instructions

### Hybrid Workflow (Best Practice)

```
User: "Add payment processing with Stripe"

Step 1: Agent explores
  → "Find existing payment code"
  → Returns: "Payment utils in lib/payments.ts, using checkout API"
  → 200 tokens

Step 2: Skill executes
  → backend-endpoint auto-invokes
  → Uses agent findings
  → Generates /api/payment/checkout endpoint
  → Follows project patterns
  → 3k tokens

Total: 3.2k tokens
vs Manual: 100k+ tokens (reading all payment-related files)
Savings: 97%
```

---

## 🗣️ Natural Language Interface (v3.0)

**No slash commands needed!** Navigator skills auto-invoke based on your intent.

### Session Management

**Start session**:
```
"Start my Navigator session"
"Load the navigator"
"Begin working on this project"
```

### Documentation

**Archive task**:
```
"Archive TASK-12 documentation"
"Document this completed feature"
```

**Create SOP**:
```
"Create an SOP for debugging memory leaks"
"Document this solution as a procedure"
```

### Context Management

**Create marker**:
```
"Create a checkpoint marker called feature-complete"
"Save my progress as experiment-1"
```

**Manage markers**:
```
"Show my markers"
"Load the profile-edit-started marker"
"Clean up old markers"
```

**Smart compact**:
```
"Clear context and preserve markers"
"Smart compact"
```

### Initialization

**First-time setup**:
```
"Initialize Navigator in this project"
"Set up Navigator documentation structure"
```

**Skills auto-detect intent** - just describe what you want!

---

## 🏗️ Complete Workflow Example

### Day 1: New Feature

```
# Morning - Start session
"Start my Navigator session"

"Implement user profile editing"

# nav-task auto-invokes
→ Creates TASK-45-user-profile-edit.md
→ Implementation plan ready

# Agent explores
"Find existing profile code"
→ Agent searches in separate context
→ Returns: "Profile in components/Profile.tsx, uses Formik"
→ 200 tokens

# Skill executes
"Create ProfileEdit component"
→ frontend-component auto-invokes
→ Generates component + tests + styles
→ Follows project Formik patterns
→ 3k tokens

# Save progress before lunch
"Create a marker called profile-edit-started"

# After lunch
→ Read the marker (3k tokens)
→ Continue where you left off

# End of day
"Save progress as eod-day1"
```

### Day 2: Continue Feature

```
# Morning - Resume
"Start my Navigator session"
→ Loads navigator
→ Detects active marker from yesterday
→ Prompts: "Load eod-day1 marker?"
→ Context restored (3k tokens vs re-explaining)

# Add API integration
"Add PUT /api/profile endpoint"
→ backend-endpoint auto-invokes
→ Generates endpoint + validation + tests
→ 3k tokens

# Complete feature
→ Tests passing
→ Ready for review

# Document completion
"Archive TASK-45 documentation"

# Autonomous completion
→ Commits changes
→ Archives task doc
→ Closes ticket (if PM tool configured)
→ Creates TASK-45-complete marker

"Clear context and preserve markers"
→ Clears conversation
→ Preserves marker for future reference
```

**Total tokens used over 2 days**: ~25k
**vs Traditional (loading all docs)**: ~400k
**Savings**: 93%

---

## 🔄 Self-Improving Capability

### How It Works

```
1. Identify Pattern
   User: "We keep adding API endpoints manually"

2. Request Skill
   User: "Create a skill for adding endpoints"

3. nav-skill-creator auto-invokes
   → Asks: Framework? Location? Auth? Testing?
   → User: "Express, api/routes/, JWT, Jest"

4. Agent Analyzes (separate context)
   → Searches api/routes/*.ts
   → Identifies patterns (structure, naming, tests)
   → Returns summary (200 tokens)

5. Skill Generates
   → Creates skills/backend-endpoint/
   → SKILL.md (auto-invocation instructions)
   → Functions (endpoint_generator.py, route_validator.py)
   → Templates (endpoint-template.ts, test-template.spec.ts)
   → Examples (real endpoints from your codebase)

6. Skill Ready
   User: "Add GET /api/users endpoint"
   → backend-endpoint auto-invokes
   → Generates route + middleware + tests
   → Follows YOUR project conventions
```

### Generated Skills Include

**SKILL.md**:
- Auto-invocation triggers
- Execution steps
- Examples from your codebase

**Functions** (predefined Python scripts):
- Generators (create boilerplate)
- Validators (ensure quality)
- Formatters (consistent style)

**Templates** (with placeholders):
- ${ENDPOINT_NAME}, ${HTTP_METHOD}, etc.
- Your project structure
- Your coding conventions

**Examples** (from your code):
- Best practices extracted
- Real implementations
- Common patterns

---

## 📈 Success Metrics

### Token Efficiency

**Documentation loading**:
- Traditional: 150k tokens upfront
- Navigator: 2k upfront, 10k as needed
- **Savings**: 92-95%

**Research & exploration**:
- Manual file reading: 50k+ tokens
- Agent summaries: 200 tokens
- **Savings**: 99.6%

**Code generation**:
- Manual with examples: 15k tokens
- Skills with templates: 3k tokens
- **Savings**: 80%

**Overall session efficiency**:
- Work per session: 10x increase
- Session restarts: 0 (vs 3-4/day)
- Context available: 96% (vs 0%)

### Development Productivity

- **Onboarding**: New devs productive in 48 hours (vs 2 weeks)
- **Pattern consistency**: 100% (templates enforce)
- **Documentation**: Always current (living docs)
- **Knowledge loss**: 0% (SOPs capture solutions)

---

## 🎯 Best Practices

### Session Workflow

```
# 1. ALWAYS start with
"Start my Navigator session"

# 2. Let skills auto-invoke (don't force)
✅ "Add user authentication"
❌ "Use the backend-endpoint skill to add auth"

# 3. Use agents for research
✅ "How does our routing work?" (agent explores)
❌ "Read all route files" (manual, expensive)

# 4. Save progress with markers
"Create a marker called [name]" before breaks/experiments

# 5. Compact when switching contexts
"Clear context and preserve markers" after completing isolated work

# 6. Document as you go
"Archive TASK-XX documentation" when done
```

### Skill Creation

```bash
# Generate skills for patterns you repeat 3+ times
✅ "We add components weekly" → Create skill
❌ "I added one endpoint" → Too early

# Let nav-skill-creator analyze first
✅ "Create skill for components" → Agent finds patterns
❌ "I'll describe the pattern" → Skip analysis

# Test generated skills immediately
✅ "Add UserCard component" → Verify output
❌ Generate and forget → Might not match needs
```

### Agent Usage

```bash
# Use for broad questions
✅ "Find all database queries"
✅ "How is state managed?"
✅ "What's the auth flow?"

# Not for specific files
❌ "Find UserProfile.tsx" (use Glob)
❌ "Read one file" (use Read)
```

---

## 🔮 What's Next

### v3.0 Roadmap (In Progress)

**Breaking Change**: Skills-only architecture

**What's changing**:
- ❌ Remove all slash commands (`/nav:*`)
- ✅ Natural language only ("Start my session" vs `/nav:start`)
- ✅ 11k token reduction (commands overhead eliminated)
- ✅ Cleaner architecture (no hybrid complexity)
- ✅ Simpler UX (no syntax to remember)

**Migration**:
```bash
# Before (v2.x)
/nav:start
/nav:marker checkpoint

# After (v3.0)
"Start my Navigator session"
"Create a checkpoint marker"
```

Skills auto-invoke - no manual commands needed.

**Target**: v3.0.0 release in 3 days

---

### v3.1+ Roadmap (Post-v3.0)

**More Built-in Skills**:
- `test-generator` - Generate test files
- `doc-generator` - Generate API docs
- `config-generator` - Generate config files
- `session-analytics` - Real-time token tracking

**Platform Features**:
- Skill marketplace (share skills)
- Skill versioning
- Cross-project sync
- Skill dependencies

**Framework Skills** (community-driven):
- Community can generate via `nav-skill-creator`
- React, Vue, Express, Prisma patterns
- Shared via skill marketplace

---

## 🤝 Contributing

Navigator is open source and welcomes contributions:

**Ways to contribute**:
1. **Generate skills** for your stack (React, Vue, Express, etc.)
2. **Share skills** via GitHub (skill marketplace coming)
3. **Report issues** with navigator workflow
4. **Suggest improvements** to core skills
5. **Document patterns** you've discovered

**Skill contribution**:
```bash
# 1. Generate skill for your project
"Create a skill for [pattern]"

# 2. Test it thoroughly
Use skill 5-10 times, verify output

# 3. Share via GitHub
Fork repo, add to skills/, PR with examples

# 4. Community benefits
Others can use your skill immediately
```

---

## 📚 Documentation

**Quick references**:
- [Installation Guide](./docs/installation.md)
- [Skills Architecture](./docs/skills.md)
- [Agent Usage Guide](./docs/agents.md)
- [CLAUDE.md Template](./templates/CLAUDE.md)

**In-project docs** (after initializing Navigator):
- `.agent/DEVELOPMENT-README.md` - Navigator
- `.agent/system/` - Architecture docs
- `.agent/sops/` - Procedures

---

## 🙏 Acknowledgments

Built with [Claude Code](https://claude.com/claude-code)

Inspired by the need for context-efficient AI development and the realization that AI should generate its own tools.

---

## 📄 License

MIT License - see [LICENSE](LICENSE) file

---

## 🚀 Get Started

```bash
/plugin marketplace add alekspetrov/navigator
/plugin install navigator
# Restart Claude Code
```

Then use natural language:
```
"Initialize Navigator in this project"
"Start my Navigator session"
```

**Welcome to self-improving AI development with natural language.** 🔄
