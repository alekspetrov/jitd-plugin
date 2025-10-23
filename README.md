# Navigator - Context Engineering for Your Codebase

**92% token savings. Verified, not estimated.**

[![MIT License](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)
[![Version](https://img.shields.io/badge/version-3.4.0-blue.svg)](https://github.com/alekspetrov/navigator/releases)

---

## The Problem

I kept hitting context limits in Claude Code.

Session 5: Claude forgot a function I just wrote.
Session 7: It hallucinated a class that didn't exist.
Session 8: "Context limit reached."

I checked the stats: **150,000 tokens loaded**. I'd used **8,000**.

**I was wasting 94% of my context window on documentation I never needed.**

---

## The Realization

This wasn't a bug. This was my workflow.

**Every AI session, same pattern**:
1. Load all project docs at start ("better to have everything")
2. Context fills with 150k tokens
3. AI gets overwhelmed (signal lost in noise)
4. Forgets recent changes
5. Session crashes
6. Start over

**The default approach—bulk loading—was the problem.**

Then I read Anthropic's context engineering docs. Two insights changed everything:

**Context engineering ≠ Prompt engineering**

```
Prompt engineering: Single query → optimize prompt
Context engineering: Multi-turn agent → curate context
```

**From Anthropic's docs** (literally):
```
Available context:          Curated context:
├── Doc 1                  ├── Doc 1 ✓
├── Doc 2                  ├── Doc 2 ✓
├── Doc 3                  └── Tool 1 ✓
├── Doc 4
└── Tool 1

Load strategically, not everything.
```

**Navigator implements this for your codebase.**

---

## The Solution

**Context engineering: Strategic curation over bulk loading**

### How It Works

**Traditional approach** (bulk loading):
```
Session start → Load all docs (150k) → Context 75% full → Work cramped
Result: Sessions die in 5-7 exchanges
```

**Navigator** (context engineering):
```
Session start:
├── Navigator/index (2k) ✓ Map of what exists
└── Current task (3k) ✓ What you're working on

As you work:
├── Need architecture? Load it (5k)
├── Hit a bug? Load SOP (2k)
└── On-demand, strategic

Result: Sessions last 20+ exchanges
```

**Your project**: 150k tokens available
**Navigator loads**: 12k tokens
**You save**: 138k tokens (92%)

**For actual work. Not documentation overhead.**

---

## The Proof

**Not estimates. Verified via OpenTelemetry.**

```
╔══════════════════════════════════════════════════════╗
║          NAVIGATOR EFFICIENCY REPORT                 ║
╚══════════════════════════════════════════════════════╝

📊 TOKEN USAGE
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Your project documentation:     150,000 tokens
Loaded this session:             12,000 tokens
Tokens saved:                   138,000 tokens (92% ↓)

📈 SESSION METRICS
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Context usage:                        35% (excellent)
Efficiency score:                  94/100 (excellent)

⏱️  TIME SAVED
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Estimated time saved:             ~42 minutes
```

**Check your own: Run `/nav:stats` after installing.**

---

## What Navigator Does

### Context Engineering Implementation

**1. Lazy Loading** - Load what you need, when you need it
```
Always: Navigator (2k) + Current task (3k)
On-demand: System docs (5k), SOPs (2k), Integration guides (3k)
Result: 90%+ context available for work
```

**2. Agent-Optimized Search** - Curated exploration, not bulk reading
```
Traditional: Read 20 files manually (80k tokens)
Navigator: Agent searches → Returns summary (8k tokens)
Savings: 90%
```

**3. Progressive Refinement** - Metadata first, details on-demand
```
Step 1: Load overview (2k)
Step 2: Identify needs
Step 3: Load relevant details (5k)
vs Loading everything: 15k
Savings: 53%
```

**4. Context Markers** - Compress decisions, not raw data
```
Full session: 200k tokens
Context marker: 5k tokens (decisions preserved)
Compression: 97.5%
```

**5. Autonomous Completion** - No manual prompts for predictable workflows
```
Feature complete → Auto-commits, updates docs, closes ticket
Zero "please commit" prompts
```

**These are patterns from Anthropic's context engineering docs, implemented.**

📖 **[Read the Philosophy](.agent/philosophy/CONTEXT-EFFICIENCY.md)** - Why this works
📖 **[See the Patterns](.agent/philosophy/PATTERNS.md)** - How to apply
📖 **[Avoid Anti-Patterns](.agent/philosophy/ANTI-PATTERNS.md)** - Common mistakes

---

## Quick Start

### Installation

```bash
# Claude Code plugin marketplace
/plugin marketplace add alekspetrov/navigator
/plugin install navigator

# Restart Claude Code
```

### Initialize Your Project

```bash
# In your project directory
"Initialize Navigator in this project"
```

Creates documentation structure:
```
your-project/
└── .agent/
    ├── DEVELOPMENT-README.md    # Navigator (your index)
    ├── philosophy/               # Context engineering principles
    ├── tasks/                    # Implementation plans
    ├── system/                   # Architecture docs
    ├── sops/                     # Standard procedures
    └── .nav-config.json         # Configuration
```

**Works with any codebase**: Rust, Python, JavaScript, Go, etc.

### Start Your Session

**Every session begins**:
```
"Start my Navigator session"
```

This loads:
- Navigator/index (2k tokens) - Map of your docs
- Current task (if configured with PM tools) - 3k tokens
- **Nothing else yet** - 195k tokens available for work

### Use Context Engineering

```
# Agent-optimized search (vs reading 15 files)
"Find all authentication implementation files"
→ Agent returns curated summary (8k vs 80k tokens)

# Progressive refinement (vs loading full docs)
"How does the payment system work?"
→ Loads overview → Drills down only if needed

# Lazy loading (vs bulk loading)
"Implement user profile feature"
→ Loads task doc → Adds architecture only when relevant
```

**You'll see the difference in `/nav:stats`**

---

## What's New in v3.4.0

**Direct Figma MCP Integration** - Proves the preprocessing pattern

**Before v3.4.0**:
```
Claude orchestrates → Call MCP → Save temp files →
Call MCP again → Process files → 15-20 steps, 150k tokens
```

**After v3.4.0**:
```
Python connects to Figma MCP directly →
Preprocesses → Returns clean data → 1 step, 12k tokens
```

**Results**:
- 95% orchestration reduction (20 steps → 1)
- 92% token reduction (150k → 12k)
- 75% faster (15 min → 5 min)
- Deterministic output (no hallucinations)

**This proves**: Python for deterministic, LLM for semantic.

📖 **[v3.4.0 Release Notes](RELEASE-NOTES-v3.4.0.md)** | **[Setup Guide](UPGRADE-v3.4.0.md)**

---

## Built-in Skills (18)

Navigator includes 18 skills that auto-invoke on natural language:

### Navigation & Session Management
```
"Start my Navigator session"              → nav-start
"Initialize Navigator in this project"    → nav-init
"Create context marker: feature-v1"       → nav-marker
```

### Development Workflow
```
"Create a React component for profile"    → frontend-component
"Add an API endpoint for posts"           → backend-endpoint
"Create a database migration for users"   → database-migration
```

### Design & Documentation
```
"Review this Figma design: [URL]"         → product-design
"Archive TASK-05 documentation"           → nav-task
"Create an SOP for debugging auth"        → nav-sop
```

**No commands to memorize** - Skills auto-invoke from natural language.

📖 **[All 18 Skills](.agent/DEVELOPMENT-README.md#available-skills)**

---

## Context Efficiency Score

Navigator tracks how well you're using context engineering:

```bash
/nav:stats
```

**Score calculation** (0-100):
- **Token savings** (40 points): 85%+ = 40 points
- **Cache efficiency** (30 points): 100% = 30 points
- **Context usage** (30 points): <40% = 30 points

**Interpretation**:
- **90-100**: Excellent - Optimal context engineering
- **80-89**: Good - Minor improvements possible
- **70-79**: Fair - Review lazy-loading strategy
- **<70**: Check anti-patterns (wasting context)

**Your metrics. Your project. Your savings.**

---

## Real Workflows

### Feature Implementation
```
Load:
├── Navigator (2k)
├── Task doc (3k)
└── System architecture (5k)

Total: 10k tokens
Session: 15 exchanges to completion
Context at end: 45% (comfortable)
```

### Bug Fix
```
Load:
├── Navigator (2k)
├── Debugging SOP (2k)
└── Agent search results (5k)

Total: 9k tokens
Session: 8 exchanges to fix
Context at end: 30% (plenty of room)
```

### Design Review
```
Load:
├── Navigator (2k)
├── Figma data (12k, preprocessed)
└── Design system docs (5k)

Total: 19k tokens
Session: Complete review in 5 minutes
vs Without preprocessing: 150k tokens, 15 minutes
```

**Efficiency is measurable. Check yours: `/nav:stats`**

---

## Why This Works

### Context Engineering Principles

From Anthropic's docs on context engineering:

**1. Curate, don't bulk load**
```
Available context (left) → Curated context (right)
Select what matters, not everything
```
**Navigator implements**: Lazy loading, agent search, progressive refinement

**2. Right tool for the job**
```
Deterministic tasks → Traditional code (Python, bash)
Semantic tasks → LLM (understanding, generation)
```
**Navigator implements**: Preprocessing (v3.4.0 Figma), autonomous completion

**3. Compress decisions, not data**
```
200k session → Extract decisions → 5k marker
Preserve what matters, not transcripts
```
**Navigator implements**: Context markers (97.5% compression)

📖 **[Context Engineering Philosophy](.agent/philosophy/CONTEXT-EFFICIENCY.md)**

---

## Project Management Integration

**Optional**: Connect Navigator to your PM tool

### Supported
- **Linear** (MCP) - Full integration
- **GitHub Issues** (gh CLI) - Via gh command
- **Jira** (API) - Via API calls
- **Manual** - Documentation-only mode (default)

### With PM Integration
```
"Start my Navigator session"

→ Checks Linear for assigned tasks
→ Loads current task implementation plan
→ Shows task context (3k tokens)
```

When done:
```
→ Auto-closes ticket
→ Archives documentation
→ Creates completion marker
```

**Zero-config works without PM tools.** Integration is enhancement, not requirement.

📖 **[PM Integration Guide](.agent/sops/integrations/linear-setup.md)**

---

## Configuration

Minimal configuration required. Works with defaults.

**Optional** `.agent/.nav-config.json`:
```json
{
  "version": "3.4.0",
  "project_management": "none",
  "task_prefix": "TASK",
  "auto_load_navigator": true,
  "compact_strategy": "conservative"
}
```

**Auto-detected**:
- Project type (JS, Python, Rust, etc.)
- Available integrations
- Documentation structure

**No setup required to start.**

---

## Documentation Structure

Navigator creates organized, discoverable documentation:

```
.agent/
├── DEVELOPMENT-README.md           # Navigator (always load first)
│
├── philosophy/                     # Context engineering principles
│   ├── CONTEXT-EFFICIENCY.md      # Why Navigator exists
│   ├── ANTI-PATTERNS.md            # Common mistakes
│   └── PATTERNS.md                 # Success patterns
│
├── tasks/                          # Implementation plans
│   ├── TASK-01-feature.md
│   └── archive/                    # Completed tasks
│
├── system/                         # Architecture docs
│   ├── architecture.md
│   ├── database.md
│   └── api-design.md
│
└── sops/                           # Standard procedures
    ├── debugging/
    ├── deployment/
    └── integrations/
```

**Strategy**:
- Always load: `DEVELOPMENT-README.md` (2k tokens)
- On-demand: Everything else (as needed)
- Result: 90%+ savings

---

## Examples

### Before Navigator

```bash
# Load all docs
cat .agent/**/*.md  # 150k tokens

# Session
User: "Add auth to API"
AI: "Here's the implementation..."
[5 exchanges]
AI: "What was that function you just wrote?"
[7 exchanges]
Error: Context limit reached

# Restart, start over
```

### With Navigator

```bash
# Strategic loading
"Start my Navigator session"  # 2k tokens

# Work
User: "Add auth to API"
Navigator: Loads task doc (3k) + architecture on-demand (5k)
AI: "Here's the implementation following your patterns..."
[20 exchanges, feature complete]

Context usage: 35%
Efficiency: 94/100
Time saved: 42 minutes
```

**Try it: Install Navigator, check `/nav:stats` after your first session.**

---

## Advanced Features

### Context Markers
```
"Create context marker: auth-implementation-v1"

Saves:
├── Decisions made (what & why)
├── Code written (summary)
├── Next steps

Compression: 200k → 5k (97.5%)

Resume later:
"Resume from marker: auth-implementation-v1"
→ Full context restored in seconds
```

### Agent-Optimized Search
```
"Find all API endpoints and explain routing"

Agent:
├── Searches codebase (50 files found)
├── Reads relevant files
├── Extracts patterns
└── Returns summary (200 tokens)

vs Manual: Read 50 files = 80k tokens
Savings: 99.8%
```

### Skill Generation
```
"Create a skill for adding database indexes"

Navigator:
├── Analyzes your project patterns
├── Generates custom skill
├── Adds functions and templates
└── Auto-invokes on: "Add index for users table"

Result: Automation of repetitive workflows
```

### Real-Time Metrics
```
Session statistics (live):
├── Tokens loaded: 12k / 200k (6%)
├── Cache efficiency: 100%
├── Efficiency score: 94/100
└── Time saved: ~38 minutes
```

---

## Performance

**Token Efficiency**:
- Documentation loading: 150k → 12k (92% ↓)
- Agent searches: 80k → 8k (90% ↓)
- Context markers: 200k → 5k (97.5% ↓)

**Time Savings**:
- Design review: 15 min → 5 min (67% ↓)
- Codebase search: 10 min → 30 sec (95% ↓)
- Context restore: Hours → Seconds (99%+ ↓)

**Session Longevity**:
- Without Navigator: 5-7 exchanges
- With Navigator: 20+ exchanges
- Improvement: 3-4x longer sessions

**Verified via OpenTelemetry** (not file size estimates)

📖 **[Performance Details](PERFORMANCE.md)** | **[Architecture](ARCHITECTURE.md)**

---

## Contributing

Navigator is open source and community-driven.

**Ways to contribute**:
- Share your efficiency scores (`/nav:stats` screenshots)
- Submit patterns you discovered
- Create project-specific skills
- Report issues or request features

📖 **[Contributing Guide](CONTRIBUTING.md)** | **[Skill Creation Guide](.agent/sops/development/creating-skills.md)**

---

## Philosophy

**Navigator isn't about features. It's about principles.**

From Anthropic's context engineering:
- Curate context, don't bulk load
- Right tool for the job (Python + LLM)
- Compress decisions, not data

Navigator implements these patterns for your codebase.

**Result**: 92% token savings. 94/100 efficiency scores. Verified, not claimed.

📖 **[Read the Manifesto](.agent/philosophy/CONTEXT-EFFICIENCY.md)**

---

## License

MIT License - See [LICENSE](LICENSE)

---

## Links

**Documentation**:
- 📖 [Philosophy](.agent/philosophy/CONTEXT-EFFICIENCY.md) - Why Navigator exists
- 📖 [Patterns](.agent/philosophy/PATTERNS.md) - Success patterns
- 📖 [Anti-Patterns](.agent/philosophy/ANTI-PATTERNS.md) - What to avoid
- 📖 [Development Guide](.agent/DEVELOPMENT-README.md) - Complete reference

**Releases**:
- 🚀 [v3.4.0 Release Notes](RELEASE-NOTES-v3.4.0.md) - Direct Figma MCP
- 📋 [All Releases](https://github.com/alekspetrov/navigator/releases)
- 🔄 [Migration Guide](MIGRATION.md) - Upgrade to v3.0+

**Community**:
- 💬 [GitHub Discussions](https://github.com/alekspetrov/navigator/discussions)
- 🐛 [Issues](https://github.com/alekspetrov/navigator/issues)
- ⭐ [Star on GitHub](https://github.com/alekspetrov/navigator)

---

## Quick Commands

```bash
# Start session
"Start my Navigator session"

# Check efficiency
/nav:stats

# Create marker
"Create context marker: checkpoint-name"

# Initialize project
"Initialize Navigator in this project"

# Get help
"How do I use Navigator?"
```

---

**Transform your AI coding workflow from wasteful to efficient.**

**Install Navigator. Start your first session. Check `/nav:stats`.**

**See the difference: 92% token savings, verified.**
