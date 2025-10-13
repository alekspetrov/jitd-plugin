# JITD Plugin - Claude Code Configuration

## Context
JITD (Just-In-Time Documentation) plugin for context-efficient AI development. Load documentation on-demand, not upfront.

**Core Principle**: Navigator-first pattern → 92% reduction in doc loading overhead (12k vs 150k tokens)

---

## JITD Workflow (CRITICAL - ENFORCE STRICTLY)

### SESSION START PROTOCOL (MANDATORY)

**🚨 EVERY new conversation/session MUST begin with**:

```bash
/jitd:start
```

**What `/jitd:start` does**:
1. Loads `.agent/DEVELOPMENT-README.md` (navigator)
2. Checks for assigned tasks from PM tool (if configured)
3. Sets JITD workflow context
4. Activates token optimization strategy
5. Reminds about agent usage for complex tasks

**If user doesn't explicitly run `/jitd:start`**:
- You MUST proactively run it or ask to run it
- Never proceed with work without loading navigator
- This is NOT optional - it's the foundation of JITD

**Alternative (if `/jitd:start` unavailable)**:
```
Read .agent/DEVELOPMENT-README.md
```

---

### 1. Read Documentation Navigator First (Always)

**AFTER running `/jitd:start`, the navigator is loaded**:

This navigator provides:
- Documentation index
- "When to read what" decision tree
- Current task context
- Quick start guides
- Integration setup status

**Never load all docs at once** - This defeats JITD's purpose

### 2. Lazy-Load Documentation Based on Task

**Implementing feature?**
```
1. Read .agent/DEVELOPMENT-README.md (2k)
2. Read .agent/tasks/TASK-XX-feature.md (3k)
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
/jitd:update-doc feature TASK-XX
```

**After solving novel issue**:
```bash
/jitd:update-doc sop debugging issue-name
```

**After architecture change**:
```bash
/jitd:update-doc system architecture
```

### 4. Autonomous Task Completion (CRITICAL)

**When task implementation is complete, execute finish protocol AUTOMATICALLY**:

✅ **DO automatically** (no human prompt needed):
1. **Commit changes** with proper conventional commit message
2. **Archive implementation plan** via `/jitd:update-doc feature TASK-XX`
3. **Close ticket** in PM tool (if configured)
4. **Create completion marker** `TASK-XX-complete`
5. **Suggest compact** to clear context for next task

❌ **DON'T wait for**:
- "Please commit now"
- "Close the ticket"
- "Update documentation"
- "Create a marker"

**Exception cases** (ask first):
- Uncommitted files contain secrets (.env, credentials, API keys)
- Multiple unrelated tasks modified (unclear which to close)
- No task context loaded (ambiguous which TASK-XX)
- Tests failing or implementation incomplete

**Completion summary template**:
```
✅ TASK-XX Complete

Automated actions:
- Committed: [hash] [message]
- Documentation: Implementation plan archived
- Ticket: Closed in [PM tool]
- Marker: TASK-XX-complete created

Next: Run /jitd:compact to clear context
```

**Key principle**: JITD projects expect full autonomy. When work is done, execute the complete finish protocol without coordination prompts.

### 5. Smart Compact Strategy

**Run `/jitd:compact` after**:
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

- **Architecture**: KISS, DRY, SOLID principles
- **Components**: Framework best practices
- **TypeScript**: Strict mode (if applicable), no `any` without justification
- **Line Length**: Max 100 characters
- **Testing**: High coverage (backend 90%+, frontend 85%+)

---

## Forbidden Actions

### JITD Violations (HIGHEST PRIORITY)
- ❌ NEVER wait for explicit commit prompts after task completion (autonomous mode)
- ❌ NEVER leave tickets open after implementation complete (close automatically)
- ❌ NEVER skip documentation after completing features (knowledge loss)
- ❌ NEVER load all `.agent/` docs at once (defeats context optimization)
- ❌ NEVER skip reading DEVELOPMENT-README.md (navigator is essential)
- ❌ NEVER create docs outside `.agent/` structure (breaks discovery)

### General Violations
- ❌ No Claude Code mentions in commits/code
- ❌ No package.json modifications without approval
- ❌ Never commit secrets/API keys/.env files
- ❌ Don't delete tests without replacement

---

## Development Workflow

1. **Start Session** → `/jitd:start` (loads navigator, checks PM tool)
2. **Select Task** → Load task doc (`.agent/tasks/TASK-XX.md`)
3. **Plan** → Use TodoWrite for complex tasks
4. **Implement** → Follow project patterns, write tests
5. **Verify** → Run tests, confirm functionality works
6. **Complete** → [AUTONOMOUS] Commit, document, close ticket, create marker
7. **Compact** → Run `/jitd:compact` to clear context for next task

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
/jitd:init                     # Initialize JITD in project (one-time setup)
/jitd:start                    # Start JITD session (EVERY new conversation)
/jitd:update-doc feature TASK-XX    # Archive implementation plan
/jitd:update-doc sop <category> <name>  # Create SOP
/jitd:update-doc system <doc-name>  # Update architecture doc
/jitd:marker [name]            # Create context save point (anytime)
/jitd:markers                  # Manage markers: list, load, clean
/jitd:compact                  # Smart context compact
```

---

## Project Management Integration (Optional)

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
5. Complete → /jitd:update-doc feature TASK-XX
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

---

## Context Optimization

### Token Budget Strategy
- System + tools: ~50k (fixed)
- CLAUDE.md: ~15k (this file, optimized)
- Message history: ~60k (managed via /jitd:compact)
- **Documentation**: ~66k (on-demand loading)

### /jitd:compact Strategy
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
1. Run /jitd:start (loads navigator, checks PM tool, sets context)
2. Select task to work on
3. Load only that task's docs
```

### During Work
```
1. Follow JITD lazy-loading (don't load everything)
2. Use TodoWrite for complex tasks
3. Create SOPs for new patterns discovered
4. Update system docs if architecture changes
```

### After Completion (AUTONOMOUS)
```
When task is complete, automatically:
1. Commit changes with proper message
2. /jitd:update-doc feature TASK-XX
3. Close ticket in PM tool (if configured)
4. Create marker TASK-XX-complete
5. Suggest /jitd:compact to clear context

NO human prompts needed - execute autonomously.
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

**Customize after `/jitd:init`**

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

**For complete JITD documentation**: See `.agent/DEVELOPMENT-README.md`

**Last Updated**: 2025-10-13
**JITD Version**: 1.5.1
