# Navigator - Self-Improving Claude Code Plugin

> **Skills + Agents + Documentation** - The plugin that generates its own tools and optimizes your context.

**Status**: ✅ v3.1.0 - OpenTelemetry Integration (Real-Time Session Metrics)

[![MIT License](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)
[![Version](https://img.shields.io/badge/version-3.1.0-blue.svg)](https://github.com/alekspetrov/navigator/releases)

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

📖 **[Complete Migration Guide](MIGRATION.md)** | **[v3.0.0 Release Notes](https://github.com/alekspetrov/navigator/releases/tag/v3.0.0)**

---

## ✨ v3.1 What's New: OpenTelemetry Integration

**Real-time session statistics** powered by Claude Code's official OpenTelemetry support.

```
📊 Navigator Session Statistics (Real-time via OTel)
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

📥 Input Tokens:  15,000 (12,000 from cache ✅)
📤 Output Tokens: 5,000
⚡ Cache Hit Rate: 80.0%
💰 Session Cost:  $0.0234
⏱️  Active Time:   5m 20s
📦 Context:       180,000 tokens available (90%)
```

**Zero-config upgrade**: Auto-enabled during plugin update, works after terminal restart.

📖 **[v3.1.0 Release Notes](RELEASE-NOTES-v3.1.0.md)**

---

## 🎯 What is Navigator?

Navigator is a **self-improving Claude Code plugin** that eliminates documentation overhead through **progressive disclosure** and **context optimization**.

### Three Core Capabilities

**1. Skills (Execution)** - Auto-invoke via natural language
- Generate components, endpoints, migrations following your patterns
- Use predefined functions (0-token execution)
- Apply templates for consistency
- Progressive disclosure: 50-token descriptions, 3k instructions only when invoked

**2. Agents (Research)** - Explore in separate context (60-80% token savings)
- "Find all API endpoints" → Agent reads 50 files → Returns 200-token summary
- 99.8% token savings vs manual file reading
- No pollution of main conversation
- Perfect for "How does X work?" questions

**3. Documentation (Knowledge)** - Navigator-first pattern (92% reduction)
- Load 2k-token navigator instead of 150k-token docs
- Navigator guides to only what you need
- Living docs that update with code
- Context markers compress 130k → 3k

**Result**: 97% context available for actual work (vs 0% without Navigator)

📖 **[Architecture Deep-Dive](ARCHITECTURE.md)** | **[Performance Metrics](PERFORMANCE.md)**

---

## ⚡ Quick Example

```bash
# Traditional approach: Load everything upfront
Load all docs → 150k tokens → No space left → Session restart

# Navigator approach: Progressive disclosure
"Start my Navigator session"           # 2k tokens (navigator loads)
"Find all authentication patterns"     # 200 tokens (agent summary)
"Create a React component for profile" # 3k tokens (skill invokes)
# Result: 5,200 tokens used, 194k available (97% free)
```

**Token savings**: 92% | **Productivity**: 10-30x more work per session

---

## 🚀 Quick Start

### Installation

```bash
# Add Navigator from marketplace
/plugin marketplace add alekspetrov/navigator
/plugin install navigator

# Restart Claude Code
```

### Initialize Your Project

```bash
# Start Claude Code in your project
cd your-project/

# Initialize Navigator
"Initialize Navigator in this project"
```

This creates:
```
.agent/
├── DEVELOPMENT-README.md  # Your project navigator
├── tasks/                 # Implementation plans
├── system/                # Architecture docs
├── sops/                  # Standard procedures
└── .nav-config.json       # Navigator configuration
```

### Start Your Session

**Every session begins with**:
```
"Start my Navigator session"
```

This:
1. Loads your project navigator (2k tokens)
2. Checks PM tool for assigned tasks (if configured)
3. Activates token optimization
4. Shows real-time session stats (v3.1)

### Your First Skill

Navigator includes 14 built-in skills that auto-invoke on natural language:

```
"Create a React component for user profile"
```
→ `frontend-component` skill auto-invokes
→ Generates component with TypeScript, tests, and styles
→ Follows your project conventions

```
"Add an API endpoint for posts"
```
→ `backend-endpoint` skill auto-invokes
→ Creates route with validation and error handling
→ Includes tests

**No commands to memorize** - just describe what you want!

---

## 🎨 Core Capabilities

### Built-in Skills (14)

**Core Skills** (7):
- **nav-start**: Session initialization, navigator loading
- **nav-skill-creator**: Generate project-specific skills (self-improving)
- **nav-marker**: Save conversation state (130k → 3k compression)
- **nav-compact**: Smart context clearing with preservation
- **nav-task**: Implementation plan generation
- **nav-sop**: Document solutions as procedures
- **plugin-slash-command**: Create Navigator slash commands

**Development Skills** (7, generated):
- **frontend-component**: React/Vue components with tests
- **backend-endpoint**: REST/GraphQL API routes
- **database-migration**: Schema changes with rollback
- **backend-test**: API test generation
- **frontend-test**: Component test generation

📖 **[Complete Skills Reference](ARCHITECTURE.md#skills-system)**

### Agents Integration

Agents explore your codebase in **separate context** - 99.8% token savings:

```bash
# Without agents: Read 50 files manually = 100k+ tokens
# With agents: "Find all endpoints" = 200 tokens (summary)
```

**When to use**:
- ✅ Multi-file searches: "Find all API endpoints"
- ✅ Pattern discovery: "How does authentication work?"
- ✅ Code exploration: "What's the structure of components/"

**When not to use**:
- ❌ Reading specific known file (use Read tool)
- ❌ Working with 1-2 files already loaded

📖 **[Agents Architecture](ARCHITECTURE.md#agents-integration)**

### Documentation System

Navigator-first pattern eliminates upfront loading:

```
.agent/
├── DEVELOPMENT-README.md  # Navigator (ALWAYS load first, 2k tokens)
├── tasks/                 # Load current task only (3k tokens)
├── system/                # Load as needed (5k tokens)
└── sops/                  # Load when relevant (2k tokens)

Total: ~12k tokens vs ~150k (92% reduction)
```

**Living documentation** - updates automatically:
- "Archive TASK-XX documentation" (after features)
- "Create an SOP for debugging [issue]" (after solutions)
- "Update system architecture documentation" (after changes)

📖 **[Documentation Strategy](ARCHITECTURE.md#documentation-strategy)**

---

## 📊 Performance

### Token Efficiency

| Metric | Without Navigator | With Navigator | Improvement |
|--------|-------------------|----------------|-------------|
| Upfront loading | 150k tokens | 2k tokens | **98.7% ↓** |
| Research cost | 100k tokens | 200 tokens | **99.8% ↓** |
| Context available | 0% (restart) | 97% free | **∞** |
| Work per session | 100 lines | 3,000 lines | **30x ↑** |

### Real-Time Metrics (v3.1)

OpenTelemetry integration provides:
- **Token tracking**: Input, output, cache hits
- **Cost monitoring**: Per session and cumulative
- **Cache performance**: Validate prompt caching
- **ROI measurement**: Compare with/without Navigator

📖 **[Complete Performance Analysis](PERFORMANCE.md)**

---

## 🎓 Best Practices

### Session Workflow

1. **Start**: "Start my Navigator session" (loads navigator)
2. **Research**: Use agents for multi-file exploration
3. **Implement**: Skills auto-invoke for repetitive patterns
4. **Document**: "Archive TASK-XX" after completion
5. **Compact**: "Clear context and preserve markers" after sub-tasks

### Token Optimization

- ✅ **Use agents** for multi-file searches (60-80% savings)
- ✅ **Load navigator first** before any docs (guides discovery)
- ✅ **Let skills auto-invoke** (progressive disclosure)
- ❌ **Never load all docs** at once (defeats purpose)
- ❌ **Don't read manually** when agent can explore

### Self-Improving

Generate project-specific skills:

```bash
"Create a skill for adding API endpoints"
→ Analyzes your codebase patterns
→ Generates backend-endpoint skill with functions, templates
→ Auto-invokes on "Add endpoint", "Create API"
```

---

## 🔮 What's Next

### v3.2 - Enhanced Session Analytics (Planned Q1 2025)
- Session history tracking across days/weeks
- Productivity trends and insights
- Team-level aggregation
- Grafana dashboard improvements

### v4.0 - Multi-Project Context Sharing (Planned Q2 2025)
- Share SOPs across projects
- Cross-project skill library
- Team knowledge base
- Organization-level patterns

📖 **[Full Roadmap](.agent/DEVELOPMENT-README.md)**

---

## 🤝 Contributing

Contributions welcome! Focus areas:

- **Skills**: Generate new project-specific skills
- **Documentation**: Improve examples and guides
- **Performance**: Optimize token usage further
- **Integrations**: PM tools, chat platforms

📖 **[Contributing Guide](CONTRIBUTING.md)** (coming soon)

---

## 📚 Documentation

### User Documentation
- **[README.md](README.md)** - This file, getting started
- **[QUICK-START.md](docs/QUICK-START.md)** - Step-by-step quick start guide
- **[MIGRATION.md](MIGRATION.md)** - v2.x → v3.0 migration guide
- **[RELEASE-NOTES-v3.1.0.md](RELEASE-NOTES-v3.1.0.md)** - v3.1 features
- **[CLAUDE.md](CLAUDE.md)** - Workflow reference for AI

### Technical Documentation
- **[ARCHITECTURE.md](ARCHITECTURE.md)** - How Navigator works (skills, agents, docs)
- **[PERFORMANCE.md](PERFORMANCE.md)** - Metrics, benchmarks, ROI analysis
- **[CONFIGURATION.md](docs/CONFIGURATION.md)** - Configuration options and PM integrations
- **[DEPLOYMENT.md](docs/DEPLOYMENT.md)** - Team deployment and best practices

### Monitoring & Metrics
- **[GRAFANA-DASHBOARD.md](docs/GRAFANA-DASHBOARD.md)** - Grafana dashboard setup guide
- **[.agent/grafana/README.md](.agent/grafana/README.md)** - Dashboard quick reference

### Project Documentation
- **[.agent/DEVELOPMENT-README.md](.agent/DEVELOPMENT-README.md)** - Navigator's own navigator

---

## 🙏 Acknowledgments

Built on:
- **Claude Code** by Anthropic - Official CLI and plugin system
- **OpenTelemetry** - Real-time session metrics (v3.1)
- **Navigator community** - Feedback, testing, contributions

---

## 📄 License

MIT License - See [LICENSE](LICENSE) file

---

## 🚀 Get Started

```bash
# Install Navigator
/plugin marketplace add alekspetrov/navigator
/plugin install navigator

# Restart Claude Code

# Initialize in your project
"Initialize Navigator in this project"

# Start working
"Start my Navigator session"
```

**Questions?** Open an issue on [GitHub](https://github.com/alekspetrov/navigator/issues)

**Want to contribute?** See [Contributing Guide](CONTRIBUTING.md)
