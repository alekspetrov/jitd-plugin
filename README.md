# Navigator - Self-Improving Claude Code Plugin

> **Skills + Agents + Documentation** - The plugin that generates its own tools and optimizes your context.

**Status**: ✅ v3.4.0 - Direct Figma MCP Integration (Automated Design Handoff)

[![MIT License](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)
[![Version](https://img.shields.io/badge/version-3.4.0-blue.svg)](https://github.com/alekspetrov/navigator/releases)

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

## ✨ What's New in v3.4.0

**Direct Figma MCP Integration** - Python connects directly to Figma Desktop, eliminating orchestration overhead.

```
"Review this Figma design: [URL]"

→ Python connects to Figma MCP automatically
→ Progressive refinement (smart token usage)
→ 95% orchestration reduction (15-20 steps → 1)
→ 92% token reduction (150k → 12k)
→ 75% faster (15 min → 5 min)
→ One-command setup: ./setup.sh
```

**Performance**: 95% orchestration reduction | **Setup**: 30 seconds | **Requires**: Figma Desktop with MCP

📖 **[v3.4.0 Release Notes](RELEASE-NOTES-v3.4.0.md)** | **[Upgrade Guide](UPGRADE-v3.4.0.md)**

---

## 📋 Release History

See **[All Releases](https://github.com/alekspetrov/navigator/releases)** for complete version history.

**Recent releases**:
- **v3.4.0** (2025-10-22) - Direct Figma MCP integration
- **v3.3.1** (2025-10-21) - Navigator upgrade automation
- **v3.3.0** (2025-10-20) - Visual regression integration
- **v3.2.0** (2025-10-19) - Product design skill
- **v3.1.0** (2025-10-18) - OpenTelemetry integration
```

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

📖 **[Architecture Deep-Dive](ARCHITECTURE.md)** | **[Performance Metrics](PERFORMANCE.md)** | **[Visual Diagrams](ARCHITECTURE-DIAGRAMS.md)**

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

Navigator includes 18 built-in skills that auto-invoke on natural language:

```
"Review this design from Figma"
```
→ `product-design` skill auto-invokes
→ Extracts tokens, maps components, detects drift
→ Generates implementation plan (6-10 hours → 15 minutes)

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

### Built-in Skills (18)

**Core Navigator Skills** (11):
- **nav-init**: Initialize Navigator in new project
- **nav-start**: Session initialization, navigator loading
- **nav-update-claude**: Update CLAUDE.md to latest Navigator version
- **nav-upgrade**: Automate Navigator plugin updates (NEW in v3.3.1)
- **nav-marker**: Save conversation state (130k → 3k compression)
- **nav-markers**: Manage and load context markers
- **nav-compact**: Smart context clearing with preservation
- **nav-task**: Implementation plan generation
- **nav-sop**: Document solutions as procedures
- **nav-skill-creator**: Generate project-specific skills (self-improving)
- **plugin-slash-command**: Create Navigator slash commands

**Development Skills** (7, generated):
- **product-design**: Design handoff automation with Figma MCP integration
- **visual-regression**: Storybook + Chromatic/Percy/BackstopJS setup
- **frontend-component**: React/Vue components with tests
- **backend-endpoint**: REST/GraphQL API routes
- **database-migration**: Schema changes with rollback
- **backend-test**: API test generation
- **frontend-test**: Component test generation

📖 **[Complete Skills Reference](ARCHITECTURE.md#skills-system)** | **[Visual Workflow Diagrams](ARCHITECTURE-DIAGRAMS.md#skills-system-architecture)**

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

📖 **[Agents Architecture](ARCHITECTURE.md#agents-integration)** | **[Visual Flow Diagrams](ARCHITECTURE-DIAGRAMS.md#agents-system-architecture)**

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

📖 **[Documentation Strategy](ARCHITECTURE.md#documentation-strategy)** | **[Visual Loading Patterns](ARCHITECTURE-DIAGRAMS.md#documentation-system-navigator-first-pattern)**

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

### v3.4 - Design System Enhancements (Planned Q1 2026)
- **Figma → Storybook Integration**: Enhanced component story generation from Figma
- **Design System Dashboard**: Real-time drift metrics and health monitoring
- **Visual Regression Dashboard**: Aggregate visual diff metrics
- **Team Collaboration**: Multi-designer support with shared baselines

### v4.0 - Multi-Project Context Sharing (Planned Q2 2026)
- **Share Patterns Across Projects**: SOPs, skills, design systems
- **Cross-Project Skill Library**: Reusable automation
- **Team Knowledge Base**: Organization-level documentation
- **AI Design Suggestions**: Component optimization recommendations

📖 **[Full Roadmap](.agent/DEVELOPMENT-README.md)**

---

## 📐 Architecture Documentation

### Visual Diagrams (ASCII Art)

Comprehensive visual representations of Navigator's architecture:

**[ARCHITECTURE-DIAGRAMS.md](ARCHITECTURE-DIAGRAMS.md)** - 9 detailed diagrams:

1. **[Core Architecture](ARCHITECTURE-DIAGRAMS.md#1-navigator-core-architecture)** - Skills + Agents + Docs integration
2. **[Skills System](ARCHITECTURE-DIAGRAMS.md#2-skills-system-architecture)** - Progressive disclosure, auto-invocation
3. **[Agents System](ARCHITECTURE-DIAGRAMS.md#3-agents-system-architecture)** - Separate context, 99.8% token savings
4. **[Documentation System](ARCHITECTURE-DIAGRAMS.md#4-documentation-system-navigator-first-pattern)** - Navigator-first pattern
5. **[Product Design Workflow](ARCHITECTURE-DIAGRAMS.md#5-product-design-skill-workflow)** - 5-step design handoff automation
6. **[Token Optimization](ARCHITECTURE-DIAGRAMS.md#6-token-optimization-flow)** - Without vs With Navigator
7. **[Self-Improving System](ARCHITECTURE-DIAGRAMS.md#7-self-improving-system-nav-skill-creator)** - Skill generation workflow
8. **[Complete Integration](ARCHITECTURE-DIAGRAMS.md#8-complete-system-integration)** - Full session lifecycle
9. **[Progressive Disclosure](ARCHITECTURE-DIAGRAMS.md#9-progressive-disclosure-visual)** - Layer-by-layer loading

Perfect for understanding Navigator's token efficiency strategy and workflow automation.

### Technical Documentation

**[ARCHITECTURE.md](ARCHITECTURE.md)** - Deep technical dive into Navigator's design
**[PERFORMANCE.md](PERFORMANCE.md)** - Metrics, benchmarks, and optimization strategies

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
