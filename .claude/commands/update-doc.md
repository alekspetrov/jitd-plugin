---
description: Maintain .agent/ documentation system - initialize structure, archive task docs, generate SOPs, update system docs
---

# JITD Documentation System Maintenance

You are maintaining the Just-In-Time Documentation (JITD) system that transforms tickets into living knowledge while optimizing context efficiency.

## Command Modes

### Mode 1: Initialize (`/update-doc init`)

**Purpose**: Set up .agent/ documentation structure for first time

**Tasks**:
1. **Create folder structure**:
   ```
   .agent/
   ├── DEVELOPMENT-README.md  # Navigator (start here)
   ├── tasks/                 # Implementation plans
   ├── system/                # Living architecture docs
   │   ├── project-architecture.md
   │   └── tech-stack-patterns.md
   └── sops/                  # Standard operating procedures
       ├── integrations/
       ├── debugging/
       ├── development/
       └── deployment/
   ```

2. **Copy templates**:
   - Use templates from jitd-plugin/templates/
   - Customize DEVELOPMENT-README.md with project specifics
   - Replace placeholders: [Project Name], [Tech Stack], etc.

3. **Generate initial system docs**:
   - Scan current codebase structure
   - Create project-architecture.md with tech stack overview
   - Create tech-stack-patterns.md from existing code patterns

4. **Confirm completion**:
   - Show created structure
   - Prompt user to customize DEVELOPMENT-README.md

### Mode 2: Feature Complete (`/update-doc feature TASK-XX`)

**Purpose**: Archive implementation plan and update system docs after completing feature

**Tasks**:
1. **Get ticket details** (if project management configured):
   - Linear: Use `get_issue` with ticket ID
   - GitHub: Use gh CLI or GitHub API
   - Jira: Manual entry or API
   - None: Use conversation context

2. **Create/update implementation plan**:
   - Save to `.agent/tasks/TASK-XX-[slug].md`
   - Use task-template.md structure
   - Include: Context, implementation phases, technical decisions, completion checklist

3. **Update system documentation**:
   - Review what was actually built
   - Update `system/project-architecture.md` if new components added
   - Update relevant tech-stack pattern docs

4. **Check for new patterns**:
   - If new integration added → Prompt to create SOP
   - If new development pattern → Suggest SOP creation

5. **Update DEVELOPMENT-README.md**:
   - Add task to index
   - Update timestamps

6. **Notify team** (if chat configured):
   - Slack: Post to engineering channel
   - Discord: Post to dev channel
   - Teams: Post to project channel
   - None: Skip notification

### Mode 3: Create SOP (`/update-doc sop <category> <name>`)

**Purpose**: Document processes, integrations, or debugging solutions

**Categories**:
- `integrations` - Third-party service setups
- `debugging` - Common issues and solutions
- `development` - Development workflows and patterns
- `deployment` - Deployment and infrastructure procedures

**Tasks**:
1. **Analyze recent work**:
   - Review conversation history for what was just solved/built
   - Extract: problem, solution, prevention steps

2. **Generate SOP document**:
   - Save to `.agent/sops/<category>/<name>.md`
   - Use sop-template.md structure
   - Include: Context, problem, step-by-step solution, code examples, prevention

3. **Update DEVELOPMENT-README.md**:
   - Add SOP to appropriate category index
   - Link from related system docs

4. **Link to ticket** (if applicable):
   - Add comment to relevant ticket with SOP link
   - Use configured project management tool

5. **Share with team** (if configured):
   - Post announcement with SOP summary

### Mode 4: Update System Doc (`/update-doc system <doc-name>`)

**Purpose**: Refresh specific system documentation from current codebase state

**Supported docs**:
- `architecture` - Regenerate project-architecture.md
- `patterns` - Regenerate tech-stack-patterns.md
- Custom docs based on project

**Tasks**:
1. **Scan codebase**:
   - Read relevant files for selected doc type
   - Extract current state

2. **Update document**:
   - Preserve manual annotations/notes
   - Update technical details from code
   - Add timestamp

3. **Update DEVELOPMENT-README.md**:
   - Update doc timestamp in index

## Documentation Standards

### Task Documents (Implementation Plans)
**Location**: `.agent/tasks/TASK-XX-feature-slug.md`

**Required sections**:
- Ticket (link, status, sprint/milestone)
- Context (why building this)
- Implementation Plan (phased breakdown)
- Technical Decisions (framework, patterns used)
- Dependencies (requires, blocks)
- Completion Checklist

**Use template**: task-template.md

### System Documents (Living Architecture)
**Location**: `.agent/system/`

**Update triggers**:
- New major component → project-architecture.md
- New development pattern → tech-stack-patterns.md
- Major refactor → relevant system doc

**Format**: Technical, concise, code examples, timestamp

**Use template**: system-template.md

### SOPs (Standard Operating Procedures)
**Location**: `.agent/sops/<category>/`

**Template**: Context → Problem → Solution → Prevention → Related docs

**Good SOP examples**:
- `integrations/stripe-payment-setup.md`
- `development/testing-patterns.md`
- `debugging/build-errors.md`
- `deployment/production-checklist.md`

**Use template**: sop-template.md

### DEVELOPMENT-README.md (Navigator)
**Purpose**: Single source of truth for documentation discovery

**Required sections**:
- Quick Start (onboarding guide)
- Documentation Structure (visual map)
- Documentation Index (all docs organized)
- When to Read What (context-specific guidance)
- Token Optimization Strategy

## Integration with Project Management

### Supported Tools
- **Linear**: Full MCP integration (get_issue, create_comment, etc.)
- **GitHub Issues**: Via gh CLI
- **Jira**: Via API (requires setup)
- **GitLab**: Via glab CLI
- **None**: Manual documentation from conversation

### Configuration
Set in plugin config:
```
project_management: linear | github | jira | gitlab | none
task_prefix: TASK | GH | JIRA-123 | etc
```

### Ticket → Documentation Flow
1. Ticket created (human or via PM tool)
2. Claude reads ticket → Generates implementation plan
3. Implementation plan saved to .agent/tasks/
4. Feature implemented → System docs updated
5. Feature completed → Full documentation archived

## Integration with Team Chat (Optional)

### Supported Tools
- **Slack**: Via MCP
- **Discord**: Via webhook/bot
- **Teams**: Via webhook
- **None**: No notifications

### Configuration
Set in plugin config:
```
team_chat: slack | discord | teams | none
```

### Notification Triggers
- **Feature completed** → Post milestone announcement
- **Daily documentation updates** → Post to dev channel
- **New SOP created** → Share with team

### Message Format
```
📚 Documentation Update

✅ Completed:
- [What was documented]

📝 Updated Docs:
- .agent/tasks/TASK-XX-feature.md
- .agent/system/architecture.md

🔗 Ticket: TASK-XX
```

## Context Optimization Rules

### Load Only What's Needed
1. **Always start with**: `.agent/DEVELOPMENT-README.md` (navigator)
2. **For current task**: Load only that task's doc
3. **For implementation**: Load relevant system doc + SOP
4. **Never load all**: Don't read all docs at once

### Token Budget Management
- DEVELOPMENT-README.md: ~2,000 tokens
- Single task doc: ~3,000 tokens
- Single system doc: ~5,000 tokens
- Single SOP: ~2,000 tokens
- **Target**: <12,000 tokens for docs per session (vs ~150,000 if loading all)

**Benefit**: 92% reduction in documentation loading overhead

### When to Run /jitd-compact
After completing these isolated tasks:
- Finishing documentation update
- Creating SOP
- Generating implementation plan
- Switching between unrelated tasks

## Error Handling

### If project management tool fails
- Log error details
- Create documentation manually from conversation context
- Note in README that ticket TASK-XX needs manual sync

### If team chat fails
- Log message for retry
- Continue with documentation creation
- Alert user to post update manually

### If documentation exists
- Read existing doc first
- Merge new information with existing
- Preserve manual annotations
- Update timestamp

## Success Metrics

Track these in DEVELOPMENT-README.md:

**Coverage**:
- [ ] 100% of completed features have task docs
- [ ] 90%+ of integrations have SOPs
- [ ] All system docs updated within 24h of changes

**Quality**:
- [ ] All docs follow template standards
- [ ] All tickets linked to documentation
- [ ] Zero repeated mistakes (SOPs working)

**Performance**:
- [ ] <12,000 tokens loaded per typical session
- [ ] Context efficiency >70% (vs loading everything)
- [ ] Team finds docs within 30 seconds

## Command Examples

```bash
# First time setup
/update-doc init

# After completing task
/update-doc feature TASK-123

# After integrating new service
/update-doc sop integrations stripe-payment

# After major code changes
/update-doc system architecture
```

---

**Remember**: JITD optimizes context by loading documentation on-demand, not upfront. This keeps 86%+ of your context available for actual work while maintaining complete project knowledge.
