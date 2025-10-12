# [Project Name] - Development Documentation Navigator

**Project**: [Brief project description]
**Tech Stack**: [Your tech stack]
**Updated**: [Date]

---

## 🚀 Quick Start for Development

### New to This Project?
**Read in this order:**
1. [Project Architecture](./system/project-architecture.md) - Tech stack, structure, patterns
2. [Tech Stack Patterns](./system/tech-stack-patterns.md) - Framework-specific patterns
3. [Workflow Guide](./system/workflow.md) - Development workflow

### Starting a New Feature?
1. Check if similar task exists in [`tasks/`](#implementation-plans-tasks)
2. Read relevant system docs from [`system/`](#system-architecture-system)
3. Check for integration SOPs in [`sops/`](#standard-operating-procedures-sops)
4. Create ticket in your project management tool
5. Generate implementation plan with `/jitd:update-doc feature TASK-XX`

### Fixing a Bug?
1. Check [`sops/debugging/`](#debugging) for known issues
2. Review relevant system docs for context
3. After fixing, create SOP: `/jitd:update-doc sop debugging [issue-name]`

---

## 📂 Documentation Structure

```
.agent/
├── DEVELOPMENT-README.md     ← You are here (navigator)
│
├── tasks/                    ← Implementation plans from tickets
│   └── TASK-XX-feature.md
│
├── system/                   ← Living architecture documentation
│   ├── project-architecture.md
│   └── tech-stack-patterns.md
│
└── sops/                     ← Standard Operating Procedures
    ├── integrations/         # Third-party service integration guides
    ├── debugging/            # Common issues and solutions
    ├── development/          # Development workflows
    └── deployment/           # Deployment procedures
```

---

## 📖 Documentation Index

### System Architecture (`system/`)

#### [Project Architecture](./system/project-architecture.md)
**When to read**: Starting work on project, understanding overall structure

**Contains**:
- Technology stack
- Project folder structure
- Component architecture patterns
- Routing setup
- Performance targets
- Development workflow
- Code quality standards

**Updated**: Every major architecture change

#### [Tech Stack Patterns](./system/tech-stack-patterns.md)
**When to read**: Implementing new components/features

**Contains**:
- Framework-specific best practices
- Design patterns for your stack
- Common mistakes to avoid
- Performance optimization techniques

**Updated**: When adding new patterns or major components

---

### Implementation Plans (`tasks/`)

**Format**: `TASK-XX-feature-slug.md`

**When created**:
- Via `/jitd:update-doc feature TASK-XX` after completing feature
- OR manually when starting major feature (planning phase)

**Template structure**:
```markdown
# TASK-XX: [Feature Name]

## Ticket
- Ticket: [URL]
- Status: In Progress / Completed
- Sprint/Milestone: [Name]

## Context
[Why building this]

## Implementation Plan
### Phase 1: [Name]
- [ ] Sub-task 1
- [ ] Sub-task 2

## Technical Decisions
[Framework choices, patterns used]

## Dependencies
[What's required, what this blocks]

## Completion Checklist
- [ ] All sub-tasks completed
- [ ] System docs updated
- [ ] Tests written
- [ ] Deployed
```

---

### Standard Operating Procedures (`sops/`)

**Purpose**: Process knowledge, integration guides, debugging solutions

#### Integrations (`sops/integrations/`)
**When to create**: After integrating third-party service or new pattern

**Example SOPs**:
- Third-party API integrations
- Authentication service setup
- Payment processing integration
- Analytics tool setup

#### Debugging (`sops/debugging/`)
**When to create**: After solving non-obvious bug or recurring issue

**Example SOPs**:
- Framework-specific errors
- Build/deployment failures
- Common runtime issues

#### Development (`sops/development/`)
**When to create**: Establishing development patterns and workflows

**Example SOPs**:
- Local development setup
- Testing standards
- Git workflow
- Code review checklist

#### Deployment (`sops/deployment/`)
**When to create**: After setting up deployment processes

**Example SOPs**:
- Production deploy checklist
- Rollback procedure
- Environment variable management

**SOP Template**:
```markdown
# SOP: [Process Name]

## Context
[When/why you need this]

## Problem
[What went wrong or needs to be done]

## Solution
### Step-by-step
1. [Action 1]
2. [Action 2]

### Code Example
\`\`\`
// Example implementation
\`\`\`

## Prevention
- [ ] Checklist item to avoid future issues
- [ ] Validation step to add

## Related Documents
- See also: system/[doc].md
- Ticket: TASK-XX
```

---

## 🔄 When to Read What

### Scenario: Starting New Feature

**Read order**:
1. Ticket via project management → Get requirements
2. Check `tasks/` for similar previous work
3. Review `system/project-architecture.md` → Understand where this fits
4. Review `system/tech-stack-patterns.md` → Patterns needed
5. Check `sops/integrations/` → Any relevant integration guides
6. Generate implementation plan → `/jitd:update-doc feature TASK-XX`

**Load into context**: Only relevant docs, not entire .agent/

### Scenario: Adding Third-Party Integration

**Read order**:
1. Check `sops/integrations/` → Similar integration exists?
2. `system/project-architecture.md` → Where integration fits
3. Implement integration
4. Create new SOP → `/jitd:update-doc sop integrations [service-name]`
5. Update `system/project-architecture.md` if architecture changed

### Scenario: Debugging Issue

**Read order**:
1. Check `sops/debugging/` → Known issue?
2. Review relevant system doc for context
3. Check project management for related tickets
4. Solve issue
5. If novel pattern → Create SOP: `/jitd:update-doc sop debugging [issue-name]`

### Scenario: Context Optimization (Running Low on Tokens)

**Do this**:
1. Read ONLY `DEVELOPMENT-README.md` (this file) → ~2,000 tokens
2. Load ONLY current feature's task doc → ~3,000 tokens
3. Load ONLY needed system doc → ~5,000 tokens
4. Reference SOPs on-demand → ~2,000 each

**Total**: ~12,000 tokens vs ~150,000 if loading everything

**After isolated tasks**: Run `/compact` to clear conversation history

---

## 🛠️ Slash Commands Reference

### `/jitd:update-doc` Command

**Purpose**: Maintain documentation system

**Modes**:

#### 1. Initialize Structure
```bash
/jitd:update-doc init
```
Creates folders, generates initial system docs, sets up README

#### 2. Archive Feature Implementation
```bash
/jitd:update-doc feature TASK-XX
```
After completing feature, archives implementation plan and updates system docs

#### 3. Create SOP
```bash
/jitd:update-doc sop <category> <name>

# Examples:
/jitd:update-doc sop integrations stripe
/jitd:update-doc sop debugging build-errors
/jitd:update-doc sop development local-setup
```

#### 4. Update System Doc
```bash
/jitd:update-doc system <doc-name>

# Examples:
/jitd:update-doc system architecture
/jitd:update-doc system patterns
```

---

## 📊 Token Optimization Strategy

### On-Demand Documentation Loading

**Instead of loading everything** (~150,000 tokens):

1. **Always load**: `DEVELOPMENT-README.md` (~2,000 tokens)
2. **Load for current work**: Specific task doc (~3,000 tokens)
3. **Load as needed**: Relevant system doc (~5,000 tokens)
4. **Load if required**: Specific SOP (~2,000 tokens)

**Total**: ~12,000 tokens vs ~150,000 (92% savings)

### When to Run `/compact`

**Run after**:
- Completing isolated sub-task
- Finishing documentation update
- Creating SOP
- Research phase before implementation
- Resolving blocker (separate from main work)

**Don't run when**:
- In middle of feature implementation
- Context needed for next sub-task
- Debugging complex issue

---

## ✅ Documentation Quality Checklist

### When Creating Task Doc
- [ ] Ticket linked with URL
- [ ] Context explains WHY building this
- [ ] Implementation broken into phases
- [ ] Technical decisions documented
- [ ] Dependencies mapped (requires, blocks)
- [ ] Completion checklist comprehensive

### When Creating SOP
- [ ] Clear context (when/why needed)
- [ ] Problem statement specific
- [ ] Step-by-step solution provided
- [ ] Code examples included
- [ ] Prevention checklist added
- [ ] Related documents linked
- [ ] Ticket referenced if applicable

### When Updating System Doc
- [ ] Reflects current codebase state
- [ ] Code examples are accurate
- [ ] Timestamp updated
- [ ] README.md index updated
- [ ] Breaking changes noted
- [ ] Related SOPs created if needed

---

## 🚦 Success Metrics

### Documentation Coverage
- [ ] 100% of completed features have task docs
- [ ] 90%+ of integrations have SOPs
- [ ] System docs updated within 24h of changes
- [ ] Zero repeated mistakes (SOPs working)

### Context Efficiency
- [ ] <70% token usage for typical tasks
- [ ] <12,000 tokens loaded per session (documentation)
- [ ] Context optimization rules followed
- [ ] /compact used appropriately

---

**This documentation system transforms your tickets into living knowledge while keeping AI context efficient.**

**Last Updated**: [Date]
**Powered By**: JITD (Just-In-Time Documentation)
