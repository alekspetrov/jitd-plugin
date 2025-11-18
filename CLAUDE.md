# Navigator: Context-Efficient AI Development

## Why This Exists

**The problem**: AI coding sessions hit context limits in 5-7 exchanges.

**Why**: Loading all docs upfront wastes 70-90% of context window on irrelevant data.

**Navigator's solution**: Load what you need, when you need it. 150k → 12k tokens (92% reduction).

**Proven**: OpenTelemetry-verified, not estimates. Session efficiency scores 94/100.

---

## How You'll Use It

**Every session starts with**:
```
"Start my Navigator session"
```

This loads:
- Navigator index (2k tokens) - what exists
- Current task context (3k tokens) - what you're working on
- Nothing else (yet)

**As you work**:
- Need system architecture? Loads on-demand (5k)
- Need SOP? Loads when relevant (2k)
- Need integration details? Loads if required

**Result**: Context window stays efficient. Sessions last 20+ exchanges without restart.

---

## Understanding Context Efficiency

**New to this approach?** Read the philosophy:
- `.agent/philosophy/CONTEXT-EFFICIENCY.md` - Why Navigator exists
- `.agent/philosophy/ANTI-PATTERNS.md` - Common mistakes (upfront loading, etc.)
- `.agent/philosophy/PATTERNS.md` - What works and why

**Quick start?** Continue to [Navigator Workflow](#navigator-workflow-critical---enforce-strictly)

---

## Core Principle

**Context engineering beats bulk loading.**

Not "load everything just in case."
Not "better safe than sorry."

Strategic loading saves 92% of context for actual work.

---

## Navigator Workflow (CRITICAL - ENFORCE STRICTLY)

### SESSION START PROTOCOL (MANDATORY)

**🚨 EVERY new conversation/session MUST begin with**:

```
"Start my Navigator session"
```
OR (legacy): `/nav:start`

**What this does**:
1. Loads `.agent/DEVELOPMENT-README.md` (navigator)
2. Checks for assigned tasks from PM tool (if configured)
3. Sets Navigator workflow context
4. Activates token optimization strategy

**If user doesn't start session**:
- You MUST proactively suggest it
- Never proceed without loading navigator
- This is NOT optional - it's the foundation of Navigator

---

### Documentation Loading Strategy

**1. Read Navigator First** (Always)

After starting session, `.agent/DEVELOPMENT-README.md` provides:
- Documentation index
- "When to read what" decision tree
- Current task context
- Integration setup status

**2. Lazy-Load Based on Task**

**Never load all docs at once** - defeats Navigator's purpose.

Examples:
- **Implementing feature**: DEVELOPMENT-README (2k) + task doc (3k) + system doc (5k) = 10k tokens
- **Debugging**: DEVELOPMENT-README (2k) + SOP (2k) + system doc if needed (5k) = 9k tokens
- **Integration**: DEVELOPMENT-README (2k) + integration SOP (2k) + architecture (5k) = 9k tokens

**vs 150k tokens loading everything**

**3. Update Documentation As You Go**

- After feature: "Archive TASK-XX documentation"
- After solving issue: "Create an SOP for debugging [issue]"
- After architecture change: "Update system architecture documentation"

---

### Autonomous Task Completion (CRITICAL)

**When task implementation is complete, execute finish protocol AUTOMATICALLY**:

✅ **DO automatically** (no human prompt needed):
1. Commit changes with conventional commit message
2. Archive implementation plan
3. Close ticket in PM tool (if configured)
4. Create completion marker
5. Suggest compact to clear context

❌ **DON'T wait for**: "Please commit", "Close ticket", "Update docs"

**Exception cases** (ask first):
- Secrets in uncommitted files
- Multiple unrelated tasks modified
- Tests failing or implementation incomplete

**Key principle**: Navigator expects full autonomy. Execute finish protocol without prompts.

---

### Agents vs Skills - Token Optimization Strategy

Navigator uses **both strategically**:
- **Agents** = Research & exploration (separate context, 60-80% token savings)
- **Skills** = Execution & consistency (predefined functions/templates)

#### When to Use Agents

✅ **Multi-file codebase searches**
- Agent optimizes file reading (60-80% savings)
- Returns summary, not full files

✅ **Research tasks**
- Understanding unfamiliar code (70% savings)
- Reads only relevant sections

✅ **Multi-step investigations**
- Optimizes search strategy (65% savings)

✅ **Code pattern discovery**
- Samples representative files (75% savings)

❌ **Don't use agents for**:
- Reading specific known file
- Working with 1-2 already loaded files
- Small edits to current context

**Example**:
```
User: "Add rate limiting to all API endpoints"

WRONG: Grep → Read 20 files manually = 100k+ tokens
CORRECT: Task agent → Returns 3 relevant files = 8k tokens (92% savings)
```

#### When to Use Skills

✅ **Implementing features** following patterns
- Auto-invokes on natural language
- Uses predefined functions + templates
- Ensures consistency

✅ **Generating boilerplate** code
- Templates enforce format
- Functions handle validation

✅ **Enforcing project** conventions
- Examples guide implementation
- Zero manual command memorization

**Decision Matrix**:

| Scenario | Use |
|----------|-----|
| "How does auth work?" | **Agent** |
| "Find all endpoints" | **Agent** |
| "Create component" | **Skill** |
| "Add endpoint" | **Skill** |
| "Understand codebase" | **Agent** |
| "Generate boilerplate" | **Skill** |

**Key principle**: Agents for exploration, Skills for execution.

---

### Smart Compact Strategy

**Run compact after**:
- Completing isolated sub-task
- Finishing documentation update
- Switching between unrelated tasks

**Don't compact when**:
- In middle of feature
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

### Navigator Violations (HIGHEST PRIORITY)
- ❌ NEVER wait for explicit commit prompts (autonomous mode)
  → See: `.agent/philosophy/PATTERNS.md` (Autonomous Completion pattern)
- ❌ NEVER leave tickets open after completion
- ❌ NEVER skip documentation after features
- ❌ NEVER load all `.agent/` docs at once
  → See: `.agent/philosophy/ANTI-PATTERNS.md` (Upfront Loading anti-pattern)
- ❌ NEVER skip reading DEVELOPMENT-README.md
  → See: `.agent/philosophy/PATTERNS.md` (Lazy Loading pattern)
- ❌ NEVER manually Read multiple files when Task agent should be used
  → See: `.agent/philosophy/PATTERNS.md` (Direct MCP pattern)

### General Violations
- ❌ No Claude Code mentions in commits/code
- ❌ No package.json modifications without approval
- ❌ Never commit secrets/API keys/.env files
- ❌ Don't delete tests without replacement

---

## Development Workflow

1. **Start Session** → "Start my Navigator session"
2. **Select Task** → Load task doc (`.agent/tasks/TASK-XX.md`)
3. **Research** → Use Task agent for multi-file searches (NOT manual Read)
4. **Plan** → Use TodoWrite for complex tasks
5. **Implement** → Follow patterns, write tests
6. **Verify** → Run tests, confirm functionality
7. **Complete** → [AUTONOMOUS] Commit, document, close ticket, create marker
8. **Compact** → Clear context for next task

---

## Documentation System

### Structure
```
.agent/
├── DEVELOPMENT-README.md      # Navigator (always load first)
├── tasks/                     # Implementation plans
├── system/                    # Architecture docs
└── sops/                      # Standard Operating Procedures
    ├── integrations/
    ├── debugging/
    ├── development/
    └── deployment/
```

### Load Strategy
- **Always**: `.agent/DEVELOPMENT-README.md` (~2k tokens)
- **Current work**: Task doc (~3k tokens)
- **As needed**: System doc (~5k tokens)
- **If required**: SOP (~2k tokens)
- **Total**: ~12k vs ~150k loading everything

### Natural Language Commands

```
"Initialize Navigator in this project"     # First-time setup
"Start my Navigator session"               # Every session
"Archive TASK-XX documentation"             # After feature
"Create an SOP for debugging [issue]"       # After solving issue
"Update system architecture documentation"  # After changes
"Create context marker [name]"              # Save point
"Clear context and preserve markers"        # Compact
```

**Slash commands** (legacy, still work):
- `/nav:init`, `/nav:start`, `/nav:update-doc`, `/nav:marker`, `/nav:compact`

---

## Project Management Integration (Optional)

### Supported Tools
- **Linear**: Full MCP integration
- **GitHub Issues**: Via gh CLI
- **Jira**: Via API
- **GitLab**: Via glab CLI
- **None**: Manual documentation

### Workflow (if configured)
1. Read ticket via PM tool
2. Generate implementation plan → `.agent/tasks/`
3. Implement features
4. Update system docs
5. Complete → archive, close ticket
6. Notify team (if chat configured)

---

## Context Optimization

### Token Budget
- System + tools: ~50k (fixed)
- CLAUDE.md: ~15k (this file)
- Message history: ~60k (managed via compact)
- **Documentation**: ~66k (on-demand loading)

### Compact Strategy
**Run after**: Sub-task, doc update, SOP creation, task switch
**Don't run**: Mid-feature, context needed, debugging

---

## Commit Guidelines

- Format: `type(scope): description`
- Reference ticket: `feat(feature): implement X TASK-XX`
- No Claude Code mentions
- Concise and descriptive

---

## Quick Reference

### Token Optimization Checklist
- [ ] Used Task agent vs manual file reading? (60-80% savings)
- [ ] Loaded only relevant docs?
- [ ] Using navigator for doc discovery?
- [ ] Planning to compact after sub-task?

### After Task Completion (AUTONOMOUS)
1. Commit with proper message
2. Archive documentation
3. Close ticket (if configured)
4. Create marker
5. Suggest compact

**NO human prompts needed**

---

## Configuration

Navigator config in `.agent/.nav-config.json`:

```json
{
  "version": "4.5.0",
  "project_management": "none",
  "task_prefix": "TASK",
  "team_chat": "none",
  "auto_load_navigator": true,
  "compact_strategy": "conservative"
}
```

---

## Success Metrics

### Context Efficiency
- <70% token usage for typical tasks
- <12k tokens loaded per session
- 10+ exchanges without compact
- Zero session restarts during features

### Documentation Coverage
- 100% features have task docs
- 90%+ integrations have SOPs
- System docs updated within 24h
- Zero repeated mistakes

### Productivity
- 10x more work per token vs no Navigator
- Team finds docs within 30 seconds
- New developers productive in 48 hours

---

**For complete Navigator documentation**: See `.agent/DEVELOPMENT-README.md`

**Last Updated**: 2025-01-20
**Navigator Version**: 4.5.0
