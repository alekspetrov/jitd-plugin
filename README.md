# JITD Plugin - Just-In-Time Documentation for Claude Code

> Context-efficient documentation system that loads what you need, when you need it.

**Status**: 🚧 Experimental (Extracted from real production usage)

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

**Real Results** (from production usage):
- **18% token usage** → 10 commits (5 features + docs)
- **10x productivity improvement** per token
- **Zero session restarts** in 2-week sprint

---

## Installation (Coming Soon)

```bash
# Via Claude Code marketplace
/plugin marketplace add jitd/official
/plugin install jitd

# Initialize in your project
/jitd-init
```

---

## Project Roadmap

### Phase 1: Core Extraction ✅
- [x] Analyze JITD components from quant-flow-landing
- [x] Identify universal patterns vs project-specific
- [x] Design generalized architecture
- [ ] Extract sanitized templates
- [ ] Remove sensitive data (company names, business model)

### Phase 2: Plugin System 🚧
- [ ] Create `.claude-plugin/` structure
- [ ] Build marketplace.json manifest
- [ ] Implement `/update-doc` slash command
- [ ] Implement `/jitd-init` setup command
- [ ] Implement `/jitd-compact` smart compact
- [ ] Create configuration system

### Phase 3: Templates & Docs 📝
- [ ] DEVELOPMENT-README.md (navigator template)
- [ ] Task documentation template
- [ ] SOP template
- [ ] System architecture template
- [ ] Quick start guide (5min setup)
- [ ] Configuration guide
- [ ] Integration guide

### Phase 4: Examples 💡
- [ ] Generic Next.js example
- [ ] Generic Python/Django example
- [ ] Generic Go example
- [ ] Optional Linear integration example
- [ ] Optional Slack integration example

### Phase 5: Launch 🚀
- [ ] Publish to GitHub (MIT license)
- [ ] Submit to Claude Code marketplace
- [ ] Create announcement blog post
- [ ] Share on Twitter/LinkedIn
- [ ] Set up Discord community

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

## Data Source: quant-flow-landing

This plugin extracts learnings from real production usage:

**Project**: H-1B alternative landing page
**Tech**: Next.js 15, React 19, TypeScript, TailwindCSS v4
**Timeline**: 2-week experiment

**Before JITD**:
- 12+ session restarts per feature
- 32% token usage → 1 commit
- Documentation rarely consulted

**After JITD**:
- Zero session restarts in 2 weeks
- 18% token usage → 10 commits
- Documentation referenced 50+ times

**Key Insight**: Context management > raw token count

---

## What Gets Extracted (Sanitized)

### ✅ Included (Universal Patterns)
- Documentation structure
- Navigator pattern
- Template formats
- Token optimization techniques
- Workflow patterns
- `/update-doc` command logic

### ❌ Excluded (Project-Specific)
- Company name (Quant Flow)
- Business model (H-1B alternative positioning)
- Client contracts/templates
- Internal Slack channels
- Linear ticket IDs
- Team member names

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

## Timeline

**Week 1** (Current): Extract & sanitize core templates
**Week 2**: Build plugin system + slash commands
**Week 3**: Create examples + documentation
**Week 4**: Launch on GitHub + Claude Code marketplace

---

## License

MIT - Use freely, contribute back if it helps you.

---

## Resources

- **Documentation**: [docs/](./docs/)
- **Templates**: [templates/](./templates/)
- **Examples**: [examples/](./examples/)
- **Changelog**: [CHANGELOG.md](./CHANGELOG.md)
- **Issues**: [GitHub Issues](https://github.com/jitd/plugin/issues)

---

## Contact

- **Twitter**: [@alekspetrov](https://twitter.com/alekspetrov) (experiment updates)
- **Discord**: Coming soon (community discussions)
- **Email**: Coming soon (for partnerships)

---

**Status**: 🧪 Experimental - Built in public, learning as we go.

**Last Updated**: 2025-10-09
