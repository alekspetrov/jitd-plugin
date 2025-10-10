# [Project Name] - Claude Code Configuration

## Context
[Brief project description]

**Tech Stack**: [Your tech stack]

**Core Principle**: [Key architectural principle for your project]

---

## JITD Workflow (CRITICAL)

### 1. Read Documentation Navigator First (Always)

**Every session starts with**:
```
Read .agent/DEVELOPMENT-README.md (~2k tokens)
```

This navigator provides:
- Documentation index
- "When to read what" decision tree
- Current task context
- Quick start guides

**Never load all docs at once** - This defeats JITD's purpose

### 2. Lazy-Load Documentation Based on Task

**Implementing feature?**
```
1. Read .agent/DEVELOPMENT-README.md (2k)
2. Read relevant .agent/tasks/TASK-XX-feature.md (3k)
3. Read relevant .agent/system/ doc (5k)
Total: 10k tokens vs 150k
```

**Debugging issue?**
```
1. Read .agent/DEVELOPMENT-README.md (2k)
2. Check .agent/sops/debugging/ for relevant SOP (2k)
3. Read relevant system doc if needed (5k)
Total: 9k tokens vs 150k
```

**Adding integration?**
```
1. Read .agent/DEVELOPMENT-README.md (2k)
2. Check .agent/sops/integrations/ for similar pattern (2k)
3. Read .agent/system/project-architecture.md (5k)
Total: 9k tokens vs 150k
```

### 3. Update Documentation As You Go

**After completing feature**:
```bash
/update-doc feature TASK-XX
```

**After solving novel issue**:
```bash
/update-doc sop debugging issue-name
```

**After architecture change**:
```bash
/update-doc system architecture
```

### 4. Smart Compact Strategy

**Run `/jitd-compact` after**:
- Completing isolated sub-task
- Finishing documentation update
- Creating SOP
- Switching between unrelated tasks

**Don't compact when**:
- In middle of feature implementation
- Context needed for next sub-task
- Debugging complex issue

---

## Code Standards

[Customize for your project]

- **Architecture**: KISS, DRY, SOLID principles
- **Components**: [Framework-specific patterns]
- **TypeScript**: Strict mode (if applicable), no `any` without justification
- **Line Length**: Max 100 characters
- **Testing**: High coverage (backend 90%+, frontend 85%+)

**Example (Next.js/React)**:
- Server Components by default (no 'use client' unless interactive)
- Functional components only, no classes
- TailwindCSS v4 for styling (no inline styles)

**Example (Python/Django)**:
- Type hints on all functions
- Black formatter (88 char line length)
- Django best practices (CBVs, managers, querysets)

**Example (Go)**:
- Standard library first, minimize dependencies
- Go idioms (errors as values, interfaces)
- gofmt + golangci-lint

---

## Forbidden Actions

### JITD Violations (HIGHEST PRIORITY)
- ❌ NEVER load all `.agent/` docs at once (defeats context optimization)
- ❌ NEVER skip reading DEVELOPMENT-README.md (navigator is essential)
- ❌ NEVER create docs outside `.agent/` structure (breaks discovery)
- ❌ NEVER skip documentation after completing features (knowledge loss)

### General Violations
- ❌ No Claude Code mentions in commits/code
- ❌ No package.json modifications without approval
- ❌ Never commit secrets/API keys/.env files
- ❌ Don't delete tests without replacement

[Add project-specific violations]

---

## Development Workflow

1. **Read Navigator First** → `.agent/DEVELOPMENT-README.md`
2. **Check Task Context** → Load only current task doc
3. **Load Relevant Docs** → Only what's needed for current work
4. **Plan** → Use TodoWrite for complex tasks
5. **Implement** → Follow project patterns
6. **Test** → Run tests, verify functionality
7. **Document** → `/update-doc feature TASK-XX` when complete
8. **Compact** → Run `/jitd-compact` after isolated tasks

---

## Documentation System

### Structure
```
.agent/
├── DEVELOPMENT-README.md      # Navigator (always load first)
├── tasks/                     # Implementation plans
├── system/                    # Living architecture docs
└── sops/                      # Standard Operating Procedures
    ├── integrations/
    ├── debugging/
    ├── development/
    └── deployment/
```

### Load Strategy (Token Optimization)
**Always load**: `.agent/DEVELOPMENT-README.md` (~2k tokens)
**Load for current work**: Specific task doc (~3k tokens)
**Load as needed**: Relevant system doc (~5k tokens)
**Load if required**: Specific SOP (~2k tokens)
**Total**: ~12k tokens vs ~150k if loading all docs

### Slash Commands
```bash
/jitd-init                     # Initialize JITD in project
/update-doc feature TASK-XX    # Archive implementation plan
/update-doc sop <category> <name>  # Create SOP
/update-doc system <doc-name>  # Update architecture doc
/jitd-compact                  # Smart context compact
```

---

## Project Management Integration (Optional)

[Configure based on your setup]

### Supported Tools
- **Linear**: Full MCP integration
- **GitHub Issues**: Via gh CLI
- **Jira**: Via API
- **GitLab**: Via glab CLI
- **None**: Manual documentation from conversation

### Workflow (if configured)
```
1. Read ticket via PM tool
2. Generate implementation plan → .agent/tasks/
3. Implement features
4. Update system docs as architecture evolves
5. Complete → /update-doc feature TASK-XX
6. Notify team (if chat configured)
```

### Linear MCP Usage (Example)
```typescript
// Morning workflow
list_issues({ assignee: "me" })      // Check assignments
get_issue({ id: "TASK-XX" })         // Read requirements
update_issue({ id: "TASK-XX", state })  // Update progress
create_comment({ issueId, body })    // Share updates
```

[Configure for GitHub, Jira, etc. as needed]

---

## Context Optimization

### Token Budget Strategy
- System + tools: ~50k (fixed)
- CLAUDE.md: ~15k (this file, optimized)
- Message history: ~60k (managed via /jitd-compact)
- **Documentation**: ~66k (on-demand loading)

### /jitd-compact Strategy
**Run after**:
- Completing isolated sub-task
- Finishing documentation update
- Creating SOP
- Research phase before implementation
- Resolving blocker

**Don't run when**:
- In middle of feature
- Context needed for next sub-task
- Debugging complex issue

---

## Commit Guidelines

- Format: `type(scope): description`
- Reference ticket: `feat(feature): implement X TASK-XX`
- No Claude Code mentions
- Concise and descriptive

---

## Quick Reference

### Start Session
```
1. Read .agent/DEVELOPMENT-README.md
2. Check PM tool for assigned tasks (if configured)
3. Load only current task's docs
```

### During Work
```
1. Follow JITD lazy-loading (don't load everything)
2. Use TodoWrite for complex tasks
3. Create SOPs for new patterns discovered
4. Update system docs if architecture changes
```

### After Completion
```
1. /update-doc feature TASK-XX
2. Update ticket status (if PM configured)
3. /jitd-compact to clear context
```

---

## Configuration

JITD configuration stored in `.agent/.jitd-config.json`:

```json
{
  "version": "1.0.0",
  "project_management": "none",
  "task_prefix": "TASK",
  "team_chat": "none",
  "auto_load_navigator": true,
  "compact_strategy": "conservative"
}
```

**Customize after `/jitd-init`**

---

## Success Metrics

### Context Efficiency
- [ ] <70% token usage for typical tasks
- [ ] <12,000 tokens loaded per session (documentation)
- [ ] 10+ exchanges per session without compact
- [ ] Zero session restarts during features

### Documentation Coverage
- [ ] 100% completed features have task docs
- [ ] 90%+ integrations have SOPs
- [ ] System docs updated within 24h of changes
- [ ] Zero repeated mistakes (SOPs working)

### Productivity
- [ ] 10x more work per token spent (vs no JITD)
- [ ] Team finds docs within 30 seconds
- [ ] New developers productive in 48 hours

---

## JITD Benefits Reminder

**Token Savings**: 92% reduction (12k vs 150k tokens)
**Context Available**: 86%+ free for actual work
**Session Restarts**: Zero (vs 3-4 per day without JITD)
**Productivity**: 10x more commits per token spent

---

## Project-Specific Guidelines

[Add framework-specific rules here]

### Example: Next.js + React

**SSR-First Principles**:
- Default to Server Components
- 'use client' ONLY for interactivity
- Data fetching on server (async/await)
- SEO through SSR

### Example: Python + Django

**Django Patterns**:
- Class-Based Views preferred
- Custom managers for complex queries
- Signals for decoupled logic
- Django ORM (avoid raw SQL)

### Example: Go

**Go Idioms**:
- Errors as values (no exceptions)
- Interfaces for abstraction
- Goroutines for concurrency
- Minimize external dependencies

---

**For complete JITD documentation**: See `.agent/DEVELOPMENT-README.md`

**Last Updated**: [Date]
**JITD Version**: 1.0.0
