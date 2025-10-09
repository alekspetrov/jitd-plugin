# JITD - Just-In-Time Documentation

**Context-efficient documentation that loads what you need, when you need it.**

---

## The Problem

AI coding assistants have finite context windows. Traditional approaches load entire codebase documentation upfront, wasting 150k+ tokens before work begins. This leads to:

- Context overflow mid-feature
- Agent restarts and lost conversation history
- Inconsistent architecture decisions
- Documentation too "expensive" to reference

---

## The Solution

**JITD loads documentation on-demand, not upfront.**

Instead of loading everything:
```
Navigator (2k tokens)
  ↓
Current task (3k tokens)
  ↓
Relevant system doc (5k tokens)
  ↓
Specific SOP if needed (2k tokens)
━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Total: 12k tokens (92% reduction)
```

---

## Real Results

From production usage (2-week experiment):

| Metric | Before JITD | After JITD | Improvement |
|--------|-------------|------------|-------------|
| **Commits per session** | 1 commit @ 32% | 10 commits @ 18% | **10x productivity** |
| **Session restarts** | 12+ per feature | 0 | **100% completion rate** |
| **Doc loading** | 150k tokens | 12k tokens | **92% reduction** |
| **Context remaining** | ~13% | ~86% | **6.6x more available** |

---

## Features

### 📂 Structured Documentation
- `.agent/` folder with tasks, system docs, SOPs
- Navigator-first pattern (always load roadmap first)
- Living docs that update as code evolves

### ⚡ Token Optimization
- On-demand loading (not upfront)
- Smart `/compact` strategy
- Context budget tracking

### 🔄 Workflow Integration
- `/update-doc` command for maintenance
- Optional Linear/Jira integration
- Optional Slack/Discord notifications

### 📝 Rich Templates
- Task documentation (feature planning)
- SOP templates (process knowledge)
- System architecture docs
- Framework-specific examples

---

## Quick Start

### Install Plugin

```bash
# Via Claude Code marketplace
/plugin marketplace add jitd/official
/plugin install jitd
```

### Initialize in Your Project

```bash
/jitd-init
```

This creates:
```
your-project/
└── .agent/
    ├── DEVELOPMENT-README.md  (Navigator)
    ├── tasks/                 (Feature plans)
    ├── system/                (Architecture)
    └── sops/                  (Procedures)
```

### Start Using

1. **Read navigator first** (always):
   ```
   Load .agent/DEVELOPMENT-README.md
   ```

2. **Create task docs** (after features):
   ```
   /update-doc feature TASK-123
   ```

3. **Create SOPs** (after solving issues):
   ```
   /update-doc sop debugging auth-errors
   ```

4. **Update system docs** (after arch changes):
   ```
   /update-doc system architecture
   ```

---

## Configuration

JITD works standalone, but integrates with your tools:

```bash
# Set your project management tool (optional)
project_management: linear | jira | github | none

# Set your team chat (optional)
team_chat: slack | discord | teams | none

# Customize task prefix
task_prefix: TASK | JIRA | GH | etc

# Auto-load navigator on session start
auto_load_navigator: true | false
```

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

## Examples

See [examples/](../examples/) for complete project setups:

- **Next.js** - SSR patterns, component architecture
- **Python/Django** - Backend patterns, API docs
- **Go** - Microservices, testing patterns

---

## Token Savings Explained

### Traditional Approach (150k tokens)
```
✗ All task docs loaded upfront
✗ All system docs loaded upfront
✗ All SOPs loaded upfront
✗ Business docs included
━━━━━━━━━━━━━━━━━━━━━━━━━━━━
= 150,000+ tokens before work begins
```

### JITD Approach (12k tokens)
```
✓ Navigator only (2k)
✓ Current task only (3k)
✓ Relevant system doc (5k)
✓ Specific SOP if needed (2k)
━━━━━━━━━━━━━━━━━━━━━━━━━━━━
= 12,000 tokens (92% reduction)
```

**Context remaining**: 86% available for actual work

---

## How It Works

### 1. Navigator-First Pattern
Every session starts with `DEVELOPMENT-README.md`:
- Documentation index
- "When to read what" decision tree
- Current sprint focus
- Quick start guides

**Token cost**: 2,000 (vs 150,000 loading everything)

### 2. Lazy-Loading Strategy
Load docs based on current task:
- Implementing feature? Load task doc + system doc
- Debugging issue? Load relevant SOP + system doc
- New integration? Load integration SOP

**Token cost**: 5,000-10,000 per session (vs 150,000)

### 3. Living Documentation
Docs update as code evolves:
- Complete feature → `/update-doc feature TASK-XX`
- Solve novel issue → `/update-doc sop debugging issue-x`
- Refactor architecture → `/update-doc system architecture`

**Benefit**: Always current, never outdated

### 4. Smart Compact
Clear context strategically:
- After isolated sub-task
- After documentation update
- Before switching epics

**Benefit**: 10+ exchanges per session without restart

---

## FAQ

### Does JITD work with my project management tool?
Yes. JITD works standalone or integrates with Linear, Jira, GitHub Issues, etc. Integration is optional.

### Does JITD work with my tech stack?
Yes. JITD is framework-agnostic. We provide examples for Next.js, Python, and Go, but it works with any stack.

### How much setup time required?
5 minutes. Run `/jitd-init`, customize navigator template, start documenting.

### Will my team adopt this?
JITD shows immediate benefits (zero restarts, faster sessions). Teams naturally adopt tools that save time.

### Is JITD only for Claude Code?
JITD principles work with any context-limited AI (Cursor, GitHub Copilot, etc). Plugin is Claude Code-specific, but approach is universal.

---

## Metrics & Success Criteria

### Context Efficiency
- ✅ <70% token usage for typical tasks
- ✅ <12k tokens loaded per session
- ✅ 10+ exchanges without compact

### Documentation Coverage
- ✅ 100% completed features have task docs
- ✅ 90%+ integrations have SOPs
- ✅ System docs updated within 24h

### Productivity
- ✅ Zero session restarts during features
- ✅ 10x more commits per token
- ✅ 48-hour onboarding for new team members

---

## Support

- **Documentation**: [Full Docs](https://github.com/jitd/plugin/blob/main/docs/README.md)
- **Issues**: [GitHub Issues](https://github.com/jitd/plugin/issues)
- **Discussions**: [Community](https://github.com/jitd/plugin/discussions)
- **Twitter**: [@alekspetrov](https://twitter.com/alekspetrov)

---

## License

MIT - Use freely, contribute back if it helps you.

---

**Built by developers fighting context limits. Open sourced for the community.**

**Status**: 🧪 Experimental - Built in public, learning as we go.
