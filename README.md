# JITD Plugin - Just-In-Time Documentation for Claude Code

> Context-efficient documentation system that loads what you need, when you need it.

**Status**: ✅ Published v1.0.0

---

## The Problem

AI coding assistants have finite context windows. Loading all documentation upfront wastes tokens:

```
❌ Traditional Approach:
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Entire codebase docs    ~150,000 tokens
All agent definitions   ~42,000 tokens
System prompts          ~50,000 tokens
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
= Context overflow before work begins
```

**Result**: Agent restarts mid-task, loses context, inconsistent decisions.

---

## The Solution: JITD

**Core Principle**: Load documentation on-demand, not upfront.

```
✅ JITD Approach:
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Navigator (roadmap)     ~2,000 tokens
Current task doc        ~3,000 tokens
Relevant system doc     ~5,000 tokens
Specific SOP (if needed) ~2,000 tokens
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
= 12,000 tokens (92% reduction)
```

**Real Results** (from production testing):
- **92% token reduction** (12k vs 150k documentation loading)
- **10x productivity improvement** per token spent
- **Zero session restarts** over 2-week period

---

## Installation

```bash
# Via Claude Code marketplace
/plugin marketplace add alekspetrov/jitd-plugin
/plugin install jitd

# Initialize in your project
/jitd-init
```

---

## Project Roadmap

### Phase 1: Core Plugin ✅
- [x] Extract universal documentation patterns
- [x] Create `.claude-plugin/` structure
- [x] Build marketplace.json manifest
- [x] Implement `/update-doc` slash command
- [x] Implement `/jitd-init` setup command
- [x] Implement `/jitd-compact` smart compact
- [x] Create configuration system
- [x] Publish to GitHub (MIT license)
- [x] Release v1.0.0

### Phase 2: Documentation & Examples 🚧
- [x] DEVELOPMENT-README.md (navigator template)
- [x] Task documentation template
- [x] SOP template
- [x] System architecture template
- [x] Quick start guide
- [x] Configuration guide
- [ ] Generic Next.js example project
- [ ] Generic Python/Django example project
- [ ] Generic Go example project
- [ ] Video walkthrough

### Phase 3: Community & Growth 📈
- [ ] Gather user feedback
- [ ] Create announcement blog post
- [ ] Set up GitHub Discussions
- [ ] Submit to Anthropic official marketplace
- [ ] Build integration examples (Linear, Jira, etc)

---

## Architecture

### Core JITD (Universal - No Dependencies)

```
.agent/
├── DEVELOPMENT-README.md      # Navigator (always load first)
├── tasks/                     # Implementation plans from tickets
│   └── TASK-XX-feature.md
├── system/                    # Living architecture docs
│   ├── project-architecture.md
│   └── tech-stack-patterns.md
└── sops/                      # Standard Operating Procedures
    ├── integrations/
    ├── debugging/
    ├── development/
    └── deployment/
```

### Plugin Structure

```
jitd-plugin/
├── .claude-plugin/
│   ├── marketplace.json       # Plugin manifest
│   └── README.md              # Marketplace description
├── .claude/
│   └── commands/
│       ├── update-doc.md      # Core documentation command
│       ├── jitd-init.md       # Initialize structure
│       └── jitd-compact.md    # Smart context compact
├── templates/
│   ├── DEVELOPMENT-README.md  # Navigator template
│   ├── task-template.md
│   ├── sop-template.md
│   └── system-template.md
├── docs/
│   ├── QUICK-START.md
│   ├── CONFIGURATION.md
│   └── INTEGRATIONS.md
└── examples/
    ├── nextjs-project/
    ├── python-project/
    └── go-project/
```

### Optional Extensions (User Choice)

```bash
# Users install only what they need
/plugin install jitd-linear    # Linear ticket integration
/plugin install jitd-slack     # Slack notifications
/plugin install jitd-github    # GitHub PR integration
/plugin install jitd-jira      # Jira ticket management
```

---

## Key Features

### 1. Navigator-First Pattern
Always load `DEVELOPMENT-README.md` first (2k tokens):
- Documentation index
- "When to read what" decision tree
- Current sprint focus
- Quick start guides

### 2. Lazy-Loading Documentation
Load docs on-demand based on current task:
- Task doc when working on feature
- System doc when needing architecture
- SOP when encountering pattern

### 3. Living Documentation
Docs update as code evolves:
- `/update-doc feature TASK-XX` after completion
- `/update-doc sop <category> <name>` after solving novel issue
- `/update-doc system <doc>` after architecture change

### 4. Smart Compact Strategy
Clear context strategically:
- After isolated sub-task
- After documentation update
- Before switching epics
- After resolving blocker

### 5. Token Optimization
Built-in efficiency rules:
- Slim system prompts (<15k tokens)
- Lazy agent activation (core only)
- Structured templates (prevent duplication)
- Context budget tracking

---

## Use Cases

### Solo Developer
- Maintain project knowledge as you build
- No session restarts mid-feature
- Onboard future contributors instantly

### Small Team (2-5)
- Share patterns via SOPs
- Consistent architecture decisions
- 48-hour onboarding for new members

### Enterprise
- Standardize documentation across teams
- Enforce best practices
- Scale knowledge without context bloat

---

## How It Works

JITD implements a **navigator-first pattern** with lazy-loading documentation:

1. **Always load navigator first** (`.agent/DEVELOPMENT-README.md` - 2k tokens)
   - Documentation index
   - "When to read what" decision tree
   - Current project context

2. **Load docs on-demand** based on current task:
   - Working on feature? Load task doc (3k tokens)
   - Need architecture? Load system doc (5k tokens)
   - Solving pattern? Load SOP (2k tokens)

3. **Keep docs current** with slash commands:
   - `/update-doc feature TASK-XX` after implementation
   - `/update-doc sop <category> <name>` after solving novel issue
   - `/update-doc system <doc>` after architecture changes

4. **Clear context strategically**:
   - `/jitd-compact` after isolated sub-tasks
   - Preserves essential JITD markers
   - Maintains documentation references

**Key Insight**: Context management > raw token count

---

## Contributing

JITD is open source (MIT) and community-driven.

**How to Help**:
1. Try JITD in your project
2. Share your results (token usage, productivity)
3. Contribute templates for your tech stack
4. Build integration plugins (Jira, Discord, etc)
5. Report issues / suggest improvements

---

## Metrics & Success Criteria

### Context Efficiency
- [ ] <70% token usage for typical dev tasks
- [ ] <12k tokens loaded per session (docs)
- [ ] 10+ exchanges per session without compact
- [ ] Zero session restarts during features

### Documentation Coverage
- [ ] 100% completed features have task docs
- [ ] 90%+ integrations have SOPs
- [ ] 24-hour update lag for system docs
- [ ] Zero repeated architecture mistakes

### Adoption
- [ ] 100+ GitHub stars (week 1)
- [ ] 10+ projects using JITD (month 1)
- [ ] 5+ community-contributed templates (month 2)
- [ ] Featured in Claude Code marketplace (month 3)

---

## What's Next

- Gather user feedback and iterate
- Create example projects (Next.js, Python, Go)
- Build integration examples (Linear, Jira, etc)
- Submit to Anthropic official marketplace
- Grow community and share success stories

---

## License

MIT - Use freely, contribute back if it helps you.

---

## Resources

- **Documentation**: [docs/](./docs/)
- **Templates**: [templates/](./templates/)
- **Quick Start**: [docs/QUICK-START.md](./docs/QUICK-START.md)
- **Configuration**: [docs/CONFIGURATION.md](./docs/CONFIGURATION.md)
- **Issues**: [GitHub Issues](https://github.com/alekspetrov/jitd-plugin/issues)

---

## Contact

- **GitHub**: [alekspetrov/jitd-plugin](https://github.com/alekspetrov/jitd-plugin)
- **Issues**: [Report bugs or request features](https://github.com/alekspetrov/jitd-plugin/issues)
- **Twitter**: [@alekspetrov](https://twitter.com/alekspetrov)

---

**Built in public** - Share your JITD success stories!

**Last Updated**: 2025-10-10
