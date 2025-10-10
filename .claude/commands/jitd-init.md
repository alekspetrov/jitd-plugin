---
description: Initialize JITD documentation structure in your project
---

# Initialize JITD - Just-In-Time Documentation

You are setting up the JITD (Just-In-Time Documentation) system for the first time in this project.

## What JITD Does

**Problem**: AI coding assistants load entire codebase documentation upfront, wasting 150k+ tokens

**Solution**: JITD loads documentation on-demand (92% reduction to ~12k tokens)

**Result**: 86%+ context remaining for actual work, zero session restarts

## Initialization Steps

### Step 1: Create .agent/ Structure

Create the following folder structure:

```
.agent/
├── DEVELOPMENT-README.md      # Navigator (always load first)
├── tasks/                     # Implementation plans from tickets
│   └── .gitkeep
├── system/                    # Living architecture documentation
│   ├── project-architecture.md
│   └── tech-stack-patterns.md
└── sops/                      # Standard Operating Procedures
    ├── integrations/          # Third-party service guides
    │   └── .gitkeep
    ├── debugging/             # Common issues and solutions
    │   └── .gitkeep
    ├── development/           # Development workflows
    │   └── .gitkeep
    └── deployment/            # Deployment procedures
        └── .gitkeep
```

### Step 2: Copy Templates and Customize

#### A. CLAUDE.md (Project-Level Configuration)

Copy `CLAUDE.md` template to project root and customize:

**Location**: `CLAUDE.md` (project root, not in `.agent/`)

**Replace placeholders**:
- `[Project Name]` → Actual project name
- `[Brief project description]` → 1-2 sentence description
- `[Your tech stack]` → e.g., "Next.js 15 + React 19 + TypeScript"
- `[Key architectural principle]` → e.g., "SSR-first", "Microservices", "Event-driven"
- `[Date]` → Today's date

**Customize sections**:
- Code Standards → Add framework-specific rules
- Forbidden Actions → Add project-specific violations
- Project-Specific Guidelines → Add framework patterns (Next.js, Django, Go, etc.)

**Purpose**:
- Defines JITD workflow for Claude Code
- Sets project-wide coding standards
- Configures integrations and tools
- ~15k tokens (optimized size)

#### B. DEVELOPMENT-README.md (Documentation Navigator)

Copy `DEVELOPMENT-README.md` template to `.agent/` and customize:

**Location**: `.agent/DEVELOPMENT-README.md`

**Replace placeholders**:
- `[Project Name]` → Actual project name
- `[Brief project description]` → 1-2 sentence description
- `[Your tech stack]` → e.g., "Next.js 15 + React 19 + TypeScript"
- `[Date]` → Today's date

**Customize sections**:
- Quick Start → Add project-specific setup steps
- Documentation Structure → Keep standard or adapt
- Integration Reference → Add if using Linear/Jira/etc

**Purpose**:
- Navigator for `.agent/` documentation system
- Always loaded first (~2k tokens)
- "When to read what" decision tree
- Documentation index

### Step 3: Generate Initial System Docs

#### project-architecture.md

**Scan for**:
- `package.json` → Tech stack, dependencies
- Project folder structure → Organization
- Config files → Build setup, linting, testing

**Generate**:
```markdown
# Project Architecture

**Tech Stack**: [Detected stack]
**Updated**: [Today's date]

## Technology Stack
[List from package.json]

## Project Structure
[Folder tree from codebase]

## Key Components
[Main directories/modules]

## Development Workflow
[Build, test, deploy commands]
```

#### tech-stack-patterns.md

**Scan for**:
- Framework-specific patterns (React hooks, Django views, etc.)
- Common code patterns in src/
- Testing patterns in tests/

**Generate**:
```markdown
# Tech Stack Patterns

**Framework**: [Primary framework]
**Updated**: [Today's date]

## [Framework] Best Practices
[Detected patterns from codebase]

## Common Patterns
[Recurring code structures]

## Testing Strategy
[Test setup from codebase]
```

### Step 4: Configure JITD Settings

Prompt user for optional configuration:

```
JITD Configuration
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Project Management Tool:
  1. Linear (MCP integration)
  2. GitHub Issues
  3. Jira
  4. GitLab
  5. None (manual docs)

Choice [1-5]:

Task Prefix (e.g., TASK, GH, JIRA): [input]

Team Chat (optional):
  1. Slack
  2. Discord
  3. Teams
  4. None

Choice [1-4]:
```

Save configuration to `.agent/.jitd-config.json`:

```json
{
  "version": "1.0.0",
  "project_management": "linear",
  "task_prefix": "TASK",
  "team_chat": "none",
  "auto_load_navigator": true,
  "compact_strategy": "conservative"
}
```

### Step 5: Create .gitignore (if not exists)

Add JITD-specific ignores:

```gitignore
# JITD local config (optional - commit if sharing with team)
# .agent/.jitd-config.json

# Keep documentation in git
# .agent/ is for the team
```

Recommend **committing** `.agent/` to git so team shares knowledge.

### Step 6: Verify Setup

Run verification checks:

```bash
✓ Created .agent/ folder structure
✓ Copied CLAUDE.md template to project root
✓ Copied DEVELOPMENT-README.md template to .agent/
✓ Generated project-architecture.md
✓ Generated tech-stack-patterns.md
✓ Created .jitd-config.json
✓ Updated .gitignore

JITD initialized successfully! 🎉
```

### Step 7: Usage Instructions

Show user how to start:

```
Next Steps
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

1. Customize your configuration:
   Edit CLAUDE.md (project root)
   - Add framework-specific rules
   - Configure integrations
   - Set coding standards

2. Customize your navigator:
   Edit .agent/DEVELOPMENT-README.md
   - Add project-specific setup
   - Customize documentation structure

3. Start documentation workflow:
   - Complete a feature → /update-doc feature TASK-XX
   - Solve an issue → /update-doc sop debugging [issue-name]
   - Change architecture → /update-doc system architecture

4. Every session starts with:
   Read .agent/DEVELOPMENT-README.md (~2k tokens)

Token Savings
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Before JITD: 150k+ tokens (all docs upfront)
With JITD:   12k tokens (on-demand loading)
Reduction:   92%

Context available for work: 86%+
```

## Integration Setup (Optional)

### If Linear Selected

**Guide user**:
```
Linear MCP Setup
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

1. Install Linear MCP (if not already):
   claude mcp add linear-server

2. Configure API key:
   Follow prompts to add Linear API token

3. Test connection:
   /linear list-issues

Now you can use:
- /update-doc feature <linear-id>
- Auto-link docs to Linear tickets
```

### If GitHub Selected

**Guide user**:
```
GitHub CLI Setup
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

1. Install GitHub CLI:
   brew install gh (or https://cli.github.com)

2. Authenticate:
   gh auth login

3. Test:
   gh issue list

Now you can use:
- /update-doc feature GH-123
- Link docs to GitHub issues
```

## Customization Prompts

After basic setup, ask user:

```
Would you like to:
1. Add custom system docs? (e.g., database-schema.md, api-endpoints.md)
2. Create example task doc? (see how it works)
3. Create example SOP? (see how it works)
4. Configure advanced options? (compact strategy, etc.)

[1-4, or Enter to skip]
```

## Common Issues

### Issue: Folder already exists
**Solution**: Ask if user wants to:
1. Merge (keep existing + add missing)
2. Overwrite (replace with fresh templates)
3. Cancel

### Issue: No package.json found
**Solution**:
- Detect project type from files (.py, .go, etc.)
- Use generic templates
- Prompt user for tech stack manually

### Issue: Git not initialized
**Solution**:
- Initialize git: `git init`
- Or continue without git (docs won't be versioned)

## Success Message

```
╔══════════════════════════════════════════════════════╗
║                                                      ║
║  JITD Initialized Successfully! 🎉                   ║
║                                                      ║
║  Your project now has:                               ║
║  ✓ CLAUDE.md - Project configuration & workflow      ║
║  ✓ .agent/DEVELOPMENT-README.md - Navigator (~2k)    ║
║  ✓ Context-efficient documentation system            ║
║  ✓ Living docs that update as code evolves           ║
║  ✓ 86%+ context available for actual work            ║
║                                                      ║
║  Start every session with:                           ║
║  → Read .agent/DEVELOPMENT-README.md                 ║
║                                                      ║
║  Document features with:                             ║
║  → /update-doc feature TASK-XX                       ║
║                                                      ║
║  Build your knowledge base! 📚                       ║
║                                                      ║
╚══════════════════════════════════════════════════════╝
```

---

**Remember**: JITD saves 92% of documentation loading overhead by loading on-demand, not upfront. Your context is now optimized for productivity.
