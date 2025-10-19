# Navigator Plugin - Claude Code Configuration

## Context
Navigator (Navigator) plugin for context-efficient AI development. Load documentation on-demand, not upfront.

**Core Principle**: Navigator-first pattern → 92% reduction in doc loading overhead (12k vs 150k tokens)

---

## Navigator Workflow (CRITICAL - ENFORCE STRICTLY)

### SESSION START PROTOCOL (MANDATORY)

**🚨 EVERY new conversation/session MUST begin with**:

```bash
/nav:start
```

**What `/nav:start` does**:
1. Loads `.agent/DEVELOPMENT-README.md` (navigator)
2. Checks for assigned tasks from PM tool (if configured)
3. Sets Navigator workflow context
4. Activates token optimization strategy
5. Reminds about agent usage for complex tasks

**If user doesn't explicitly run `/nav:start`**:
- You MUST proactively run it or ask to run it
- Never proceed with work without loading navigator
- This is NOT optional - it's the foundation of Navigator

**Alternative (if `/nav:start` unavailable)**:
```
Read .agent/DEVELOPMENT-README.md
```

---

### 1. Read Documentation Navigator First (Always)

**AFTER running `/nav:start`, the navigator is loaded**:

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
/nav:update-doc feature TASK-XX
```

**After solving novel issue**:
```bash
/nav:update-doc sop debugging issue-name
```

**After architecture change**:
```bash
/nav:update-doc system architecture
```

### 4. Autonomous Task Completion (CRITICAL)

**When task implementation is complete, execute finish protocol AUTOMATICALLY**:

✅ **DO automatically** (no human prompt needed):
1. **Commit changes** with proper conventional commit message
2. **Archive implementation plan** via `/nav:update-doc feature TASK-XX`
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

Next: Run /nav:compact to clear context
```

**Key principle**: Navigator projects expect full autonomy. When work is done, execute the complete finish protocol without coordination prompts.

### 5. Agents vs Skills - Hybrid Architecture (CRITICAL FOR TOKEN OPTIMIZATION)

Navigator uses **both Agents and Skills strategically**:
- **Agents** = Research & exploration (separate context, 60-80% token savings)
- **Skills** = Execution & consistency (main context, predefined functions/templates)

```
┌─────────────────────────────────────────┐
│ User: "Add authentication to frontend" │
└─────────────────────────────────────────┘
                  ↓
      ┌───────────┴────────────┐
      ↓                        ↓
  [AGENT]                  [SKILL]
  Research                 Execute
      ↓                        ↓
"JWT in api/auth.ts"     Uses functions:
"Context in App.tsx"     - auth_generator.py
                         - test_generator.py
8k tokens (agent)        Output: Consistent
200 tokens (summary)     5k tokens (skill)
```

#### When to Use Agents (Research & Exploration)

**Agents = Separate Context (No Pollution)**

✅ **Multi-file codebase searches**:
```
BAD:  Grep for pattern, Read 10 files manually
GOOD: Use Task agent to search and analyze pattern across codebase
Savings: 60-80% tokens (agent optimizes file reading)
```

✅ **Research tasks** (understanding unfamiliar code):
```
BAD:  Read main.ts, utils.ts, config.ts, types.ts manually
GOOD: Use Task agent "Research authentication flow in codebase"
Savings: 70% tokens (agent reads only relevant sections)
```

✅ **Multi-step investigations**:
```
BAD:  Manually grep → read → grep again → read more
GOOD: Use Task agent "Find all API endpoints and their authentication"
Savings: 65% tokens (agent optimizes search strategy)
```

✅ **Code pattern discovery**:
```
BAD:  Read every component file to understand patterns
GOOD: Use Task agent "Analyze React component patterns in /components"
Savings: 75% tokens (agent samples representative files)
```

❌ **DON'T use agents when**:
- Reading specific known file (use Read directly)
- Working with 1-2 files you already loaded
- Making small edits to current context
- User explicitly wants to see the process

**Why agents save tokens**:
1. Agents run in separate context (don't pollute main conversation)
2. Agents read/search efficiently without loading everything into your context
3. Agents return only relevant findings (summary, not full files)
4. Your main context stays free for implementation work

**Example workflow**:
```
User: "Add rate limiting to all API endpoints"

WRONG approach:
1. Grep for "endpoint" → 50 files found
2. Read api/users.ts (5k tokens)
3. Read api/posts.ts (5k tokens)
4. Read api/comments.ts (5k tokens)
5. ... (15 more files)
= 100k+ tokens consumed, context full

CORRECT approach:
1. Use Task agent: "Find all API endpoint patterns and list files"
2. Agent returns: "Found 18 endpoints across 3 files: api/routes.ts, api/middleware.ts, api/handlers.ts"
3. Read only api/middleware.ts (where rate limiting should go)
= 8k tokens total (92% savings)
```

**Real impact**:
- Multi-file search: 60-80% token reduction
- Research task: 70% token reduction
- Pattern discovery: 75% token reduction
- **Average**: 65-70% token savings vs manual file reading

#### When to Use Skills (Execution & Consistency)

**Skills = Main Context (Predefined Functions & Templates)**

✅ **Implementing features following patterns**:
```
User: "Create a new React component for user profile"
→ Skill auto-invokes: frontend-component
→ Uses: component_generator.py, test_generator.py
→ Uses: component-template.tsx, test-template.spec.tsx
→ Output: Consistent, follows project conventions
```

✅ **Generating boilerplate code**:
```
User: "Add API endpoint for posts"
→ Skill auto-invokes: backend-endpoint
→ Uses: endpoint_generator.py, route_validator.py
→ Uses: endpoint-template.ts, test-template.spec.ts
→ Output: Follows project API patterns
```

✅ **Enforcing project conventions**:
```
User: "Create migration to add users table"
→ Skill auto-invokes: database-migration
→ Uses: migration_generator.py, schema_validator.py
→ Uses: migration-template.sql
→ Output: Follows migration standards
```

**Why skills ensure consistency**:
1. Predefined functions handle boilerplate automatically
2. Templates ensure format consistency
3. Examples guide implementation style
4. Auto-invocation (no manual commands needed)

**❌ Don't create broad "engineer" skills**:
- Too broad: "backend-engineer", "frontend-engineer"
- ✅ Better: Specific task skills (backend-endpoint, frontend-component, database-migration)

#### Hybrid Workflow Example

```
User: "Add user profile page with avatar upload"

Step 1: Agent explores (if needed)
→ Task agent: "Find existing upload patterns"
→ Returns: "File upload in utils/upload.ts, S3 in api/storage.ts"
→ Token cost: 200 tokens (summary)

Step 2: Skill executes
→ Skill auto-invokes: frontend-component
→ Uses findings from agent
→ Uses functions: page_generator.py, upload_component_generator.py
→ Uses templates: page-template.tsx, upload-form-template.tsx
→ Output: Consistent implementation
→ Token cost: 5k tokens (skill instructions)

Total: 5.2k tokens vs 100k+ if reading all files manually
```

#### Skills vs Agents Decision Matrix

| Scenario | Use | Why |
|----------|-----|-----|
| "How does auth work?" | **Agent** | Research, no pollution (200 tokens) |
| "Find all endpoints" | **Agent** | Multi-file search (60-80% savings) |
| "Create component" | **Skill** | Auto-invoke, templates, consistency |
| "Add endpoint" | **Skill** | Predefined functions, patterns |
| "Understand codebase" | **Agent** | Exploration (separate context) |
| "Generate boilerplate" | **Skill** | Templates ensure consistency |
| "Debug issue" | **Agent** | Investigation across files |
| "Follow conventions" | **Skill** | Enforce project patterns |

**Key principle**: Agents for exploration, Skills for execution. Both auto-invoke, both save tokens.

---

### 6. Smart Compact Strategy

**Run `/nav:compact` after**:
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

### Navigator Violations (HIGHEST PRIORITY)
- ❌ NEVER wait for explicit commit prompts after task completion (autonomous mode)
- ❌ NEVER leave tickets open after implementation complete (close automatically)
- ❌ NEVER skip documentation after completing features (knowledge loss)
- ❌ NEVER load all `.agent/` docs at once (defeats context optimization)
- ❌ NEVER skip reading DEVELOPMENT-README.md (navigator is essential)
- ❌ NEVER create docs outside `.agent/` structure (breaks discovery)
- ❌ NEVER manually Read multiple files when Task agent should be used (wastes 60-80% tokens)

### General Violations
- ❌ No Claude Code mentions in commits/code
- ❌ No package.json modifications without approval
- ❌ Never commit secrets/API keys/.env files
- ❌ Don't delete tests without replacement

---

## Development Workflow

1. **Start Session** → `/nav:start` (loads navigator, checks PM tool)
2. **Select Task** → Load task doc (`.agent/tasks/TASK-XX.md`)
3. **Research** → Use Task agent for multi-file searches (NOT manual Read)
4. **Plan** → Use TodoWrite for complex tasks
5. **Implement** → Follow project patterns, write tests
6. **Verify** → Run tests, confirm functionality works
7. **Complete** → [AUTONOMOUS] Commit, document, close ticket, create marker
8. **Compact** → Run `/nav:compact` to clear context for next task

**Critical**: Step 3 (Research) with agents saves 60-80% tokens vs manual file reading

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
/nav:init                     # Initialize Navigator in project (one-time setup)
/nav:start                    # Start Navigator session (EVERY new conversation)
/nav:update-doc feature TASK-XX    # Archive implementation plan
/nav:update-doc sop <category> <name>  # Create SOP
/nav:update-doc system <doc-name>  # Update architecture doc
/nav:marker [name]            # Create context save point (anytime)
/nav:markers                  # Manage markers: list, load, clean
/nav:compact                  # Smart context compact
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
5. Complete → /nav:update-doc feature TASK-XX
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
- Message history: ~60k (managed via /nav:compact)
- **Documentation**: ~66k (on-demand loading)

### /nav:compact Strategy
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
1. Run /nav:start (loads navigator, checks PM tool, sets context)
2. Select task to work on
3. Load only that task's docs
```

### During Work
```
1. Follow Navigator lazy-loading (don't load everything)
2. Use Task agent for multi-file searches (saves 60-80% tokens)
3. Use TodoWrite for complex tasks
4. Create SOPs for new patterns discovered
5. Update system docs if architecture changes
```

**Token Optimization Checklist**:
- [ ] Used Task agent instead of manual file reading? (60-80% savings)
- [ ] Loaded only relevant docs? (not everything)
- [ ] Using navigator to find docs? (not guessing paths)
- [ ] Planning to compact after this sub-task? (free up context)

### After Completion (AUTONOMOUS)
```
When task is complete, automatically:
1. Commit changes with proper message
2. /nav:update-doc feature TASK-XX
3. Close ticket in PM tool (if configured)
4. Create marker TASK-XX-complete
5. Suggest /nav:compact to clear context

NO human prompts needed - execute autonomously.
```

---

## Configuration

Navigator configuration stored in `.agent/.nav-config.json`:

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

**Customize after `/nav:init`**

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

**Token Savings**: 92% reduction (12k vs 150k tokens)
**Context Available**: 86%+ free for actual work
**Session Restarts**: Zero (vs 3-4 per day without Navigator)
**Productivity**: 10x more commits per token spent

---

**For complete Navigator documentation**: See `.agent/DEVELOPMENT-README.md`

**Last Updated**: 2025-10-13
**Navigator Version**: 1.5.1
