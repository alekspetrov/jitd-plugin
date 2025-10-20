# [Project Name] - Claude Code Configuration

## Context
[Brief project description]

**Tech Stack**: [Your tech stack]

**Core Principle**: [Key architectural principle for your project]

---

## Navigator Workflow (CRITICAL - ENFORCE STRICTLY)

### SESSION START PROTOCOL (MANDATORY)

**🚨 EVERY new conversation/session MUST begin with**:

```
"Start my Navigator session"
```

**What this does**:
1. nav-start skill auto-invokes
2. Loads `.agent/DEVELOPMENT-README.md` (navigator)
3. Checks for assigned tasks from PM tool
4. Sets Navigator workflow context
5. Activates token optimization strategy
6. Reminds about agent usage for complex tasks

**Alternative phrases**:
- "Load the navigator"
- "Initialize my session"
- "Begin working on this project"

**If nav-start doesn't activate**:
- You MUST proactively invoke it or ask user
- Never proceed with work without loading navigator
- This is NOT optional - it's the foundation of Navigator

**Manual fallback** (if skill doesn't work):
```
Read .agent/DEVELOPMENT-README.md
```

---

### 1. Read Documentation Navigator First (Always)

**AFTER starting session, the navigator is loaded**:

This navigator provides:
- Documentation index
- "When to read what" decision tree
- Current task context
- Quick start guides
- Integration setup status

**Never load all docs at once** - This defeats Navigator's purpose

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
```
"Archive TASK-XX documentation"
```
(nav-task skill auto-invokes)

**After solving novel issue**:
```
"Create an SOP for debugging [issue-name]"
```
(nav-sop skill auto-invokes)

**After architecture change**:
```
"Update system architecture documentation"
```
(nav-task skill auto-invokes)

### 4. Smart Compact Strategy

**Clear context after**:
- Completing isolated sub-task
- Finishing documentation update
- Creating SOP
- Switching between unrelated tasks

Say: "Clear context and preserve markers" (nav-compact skill auto-invokes)

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

### Navigator Violations (HIGHEST PRIORITY)
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

1. **Start Session** → "Start my Navigator session"
2. **Check Task Context** → Load only current task doc
3. **Load Relevant Docs** → Only what's needed for current work
4. **Plan** → Use TodoWrite for complex tasks
5. **Implement** → Follow project patterns
6. **Test** → Run tests, verify functionality
7. **Document** → "Archive TASK-XX documentation" when complete
8. **Compact** → "Clear context and preserve markers" after isolated tasks

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

### Natural Language Commands (v3.0)

Navigator uses **skills** that auto-invoke based on your intent:

**Initialize Navigator**:
- "Initialize Navigator in this project"
- "Set up Navigator documentation structure"
→ nav-init skill activates

**Start Session**:
- "Start my Navigator session"
- "Load the navigator"
- "Begin working"
→ nav-start skill activates

**Archive Task Documentation**:
- "Archive TASK-XX documentation"
- "Document this completed feature"
→ nav-task skill activates

**Create SOP**:
- "Create an SOP for debugging [issue]"
- "Document this solution as a procedure"
→ nav-sop skill activates

**Create Marker**:
- "Create a checkpoint marker called [name]"
- "Save my progress as [name]"
→ nav-marker skill activates

**Manage Markers**:
- "Show my markers"
- "Load a previous marker"
- "Clean up old markers"
→ nav-markers skill activates

**Compact Context**:
- "Clear context and preserve markers"
- "Smart compact"
→ nav-compact skill activates

**No slash commands needed** - just describe what you want!

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
5. Complete → "Archive TASK-XX documentation"
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
- Message history: ~60k (managed via compacting)
- **Documentation**: ~66k (on-demand loading)

### Smart Compact Strategy
**Clear context after**:
- Completing isolated sub-task
- Finishing documentation update
- Creating SOP
- Research phase before implementation
- Resolving blocker

**Don't clear when**:
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
1. "Start my Navigator session" (loads navigator, checks PM tool)
2. Select task to work on
3. Load only that task's docs
```

### During Work
```
1. Follow Navigator lazy-loading (don't load everything)
2. Use TodoWrite for complex tasks
3. Create SOPs for new patterns discovered
4. Update system docs if architecture changes
```

### After Completion
```
1. "Archive TASK-XX documentation"
2. Update ticket status (if PM configured)
3. "Clear context and preserve markers"
```

---

## Configuration

Navigator configuration stored in `.agent/.nav-config.json`:

```json
{
  "version": "3.1.0",
  "project_management": "none",
  "task_prefix": "TASK",
  "team_chat": "none",
  "auto_load_navigator": true,
  "compact_strategy": "conservative"
}
```

**Customize after initializing Navigator**

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
- [ ] 10x more work per token spent (vs no Navigator)
- [ ] Team finds docs within 30 seconds
- [ ] New developers productive in 48 hours

---

## Navigator Benefits Reminder

**Token Savings**: 97% reduction (6k vs 200k tokens)
**Context Available**: 97%+ free for actual work
**Session Restarts**: Zero (vs 3-4 per day without Navigator)
**Productivity**: 10x more commits per token spent
**Interface**: Natural language (no commands to remember)

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

**For complete Navigator documentation**: See `.agent/DEVELOPMENT-README.md`

**Last Updated**: [Date]
**Navigator Version**: 3.0.0
