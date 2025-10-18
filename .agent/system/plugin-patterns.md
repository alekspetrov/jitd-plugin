# Claude Code Plugin Development Patterns

**Framework**: Claude Code Plugin System
**Updated**: 2025-10-10

---

## Claude Code Plugin Best Practices

### 1. Slash Command Design

**Pattern**: Imperative instructions for Claude

```markdown
---
description: Short description (appears in /help)
---

# Command Title

Clear instructions for what Claude should do:

1. Step 1: Action
2. Step 2: Action
3. Step 3: Verification

Use code blocks for examples:
\`\`\`bash
example command
\`\`\`
```

**Good Example** (`/nav:init`):
- Clear steps (Create X, Copy Y, Generate Z)
- Examples of expected output
- Error handling instructions
- Success criteria

**Bad Example**:
- Vague instructions ("Set up the project")
- No examples
- No error handling
- Unclear success state

### 2. Template Design Patterns

**Universal Templates Pattern**:
```markdown
# [Project Name] - Configuration

**Context**: [Brief description]
**Tech Stack**: [Your stack]

[Universal workflow - same for all projects]

---

## Project-Specific Section

[Customizable content with examples]

**Example (Next.js)**:
- Pattern 1
- Pattern 2

**Example (Django)**:
- Pattern 1
- Pattern 2
```

**Key Principles**:
- Placeholders in `[brackets]`
- Universal sections (Navigator workflow, token optimization)
- Customizable sections (code standards, integrations)
- Multiple framework examples

### 3. Marketplace Manifest Pattern

**Location**: `.claude-plugin/marketplace.json`

```json
{
  "name": "plugin-marketplace-name",
  "metadata": {
    "version": "1.1.0"  // Sync with plugin version
  },
  "plugins": [
    {
      "name": "plugin-name",
      "version": "1.1.0",  // Must match metadata.version
      "repository": "https://github.com/user/repo",
      "strict": false  // Allow flexible loading
    }
  ]
}
```

**Versioning**:
- Update both `metadata.version` AND `plugins[].version`
- Use semantic versioning
- Tag releases in Git

---

## Common Patterns

### Pattern: Multi-File Creation Command

**Use Case**: `/nav:init` creates entire structure

**Implementation**:
1. Create folder structure (mkdir -p)
2. Copy templates with customization
3. Generate dynamic content (scan codebase)
4. Create config file
5. Verify setup
6. Show usage instructions

**Template** (from `/nav:init`):
```markdown
### Step 1: Create Structure
Create folders...

### Step 2: Copy Templates
Copy X to Y and customize...

### Step 3: Generate Docs
Scan codebase for...

### Step 4: Configure
Create config file...

### Step 5: Verify
Check that...

### Step 6: Show Usage
Display next steps...
```

### Pattern: Conditional Logic in Commands

**Use Case**: Different instructions based on project type

**Implementation**:
```markdown
## Detect Project Type

**Scan for**:
- `package.json` → Node.js project
- `requirements.txt` → Python project
- `go.mod` → Go project

**If Node.js**:
Do X...

**If Python**:
Do Y...

**If Go**:
Do Z...
```

### Pattern: Template Placeholder System

**Standard Placeholders**:
- `[Project Name]` → Project title
- `[Brief project description]` → 1-2 sentences
- `[Your tech stack]` → Technology list
- `[Date]` → Current date
- `[Key architectural principle]` → Main pattern

**Customizable Sections**:
```markdown
## Code Standards

[Customize for your project]

**Example (Next.js)**:
- Server Components by default
- 'use client' only for interactivity

**Example (Django)**:
- Class-Based Views preferred
- Type hints on all functions
```

### Pattern: Documentation Navigator

**Purpose**: Index that loads first (~2k tokens)

**Structure**:
```markdown
# Project - Documentation Navigator

## Quick Start
- New developer? Read X, Y, Z
- Starting feature? Do A, B, C
- Debugging? Check 1, 2, 3

## Documentation Index
[List all docs with "When to read"]

## When to Read What
[Scenario-based loading guide]
```

**Token Optimization**:
- Navigator always loads first
- Other docs loaded on-demand
- Never load all docs at once

---

## Testing Patterns

### Manual Testing Checklist

```markdown
**For new slash command**:
- [ ] Command runs without errors
- [ ] Creates expected files/folders
- [ ] Placeholders replaced correctly
- [ ] Success message displays
- [ ] Works in clean test project

**For new template**:
- [ ] Template copies correctly
- [ ] Placeholders clear and documented
- [ ] Examples provided for common stacks
- [ ] Token size reasonable (<5k lines)

**For version update**:
- [ ] Both version numbers updated
- [ ] Committed to Git
- [ ] Tagged with version
- [ ] Pushed to GitHub
```

### Test Project Setup

```bash
# Create clean test environment
mkdir -p ~/Projects/tmp/plugin-test
cd ~/Projects/tmp/plugin-test

# Point to local plugin
/plugin marketplace add file:///path/to/plugin

# Test command
/command-name

# Verify results
ls -la
cat generated-file.md
```

---

## Error Handling Patterns

### Pattern: Graceful Degradation

**Example**: Project type detection

```markdown
### Detect Project Type

**Try to find**:
- package.json → Use Node.js patterns
- requirements.txt → Use Python patterns

**If not found**:
- Use generic templates
- Prompt user for tech stack
- Continue with manual configuration
```

### Pattern: User Choice on Conflicts

**Example**: Folder already exists

```markdown
### Issue: .agent/ folder already exists

**Ask user**:
1. Merge (keep existing + add missing)
2. Overwrite (replace with fresh)
3. Cancel

**Handle each choice**:
- Merge: Only create missing files
- Overwrite: Backup existing → Replace
- Cancel: Exit safely
```

---

## Distribution Patterns

### Pattern: GitHub-Based Distribution

**Setup**:
1. Public GitHub repository
2. Marketplace manifest in repo
3. Version tags for releases
4. MIT license for open source

**User Installation**:
```bash
/plugin marketplace add user/repo
/plugin install plugin-name
```

**Updates**:
- Users reinstall to get latest
- GitHub CDN caches for 1-2 hours
- Local file:// bypasses cache

### Pattern: Local Development

**For Testing**:
```bash
/plugin marketplace add file:///absolute/path/to/plugin
/plugin install plugin-name
```

**Benefits**:
- Instant updates (no cache)
- Test before publishing
- Rapid iteration

---

## Token Efficiency Patterns

### Pattern: Navigator-First Loading

**Always load first**: Navigator (~2k tokens)

**Then load on-demand**:
- Task doc (~3k) if working on feature
- System doc (~5k) if need architecture
- SOP (~2k) if need process guide

**Total**: 7-12k tokens vs 150k (loading all docs)

### Pattern: Compact Strategy

**Run `/nav:compact` after**:
- Isolated sub-task completed
- Documentation updated
- SOP created
- Switching between unrelated tasks

**Don't compact when**:
- In middle of implementation
- Context needed for next step
- Debugging complex issue

---

## Common Mistakes to Avoid

### ❌ Loading All Templates at Once

**Bad**:
```markdown
Read all files in templates/
```

**Good**:
```markdown
Copy templates/CLAUDE.md to project root
Only read what's needed for current task
```

### ❌ Project-Specific Content in Templates

**Bad**:
```markdown
Use Next.js 15 with React 19
```

**Good**:
```markdown
[Your tech stack]

**Example (Next.js)**: Next.js 15 + React 19
**Example (Django)**: Django 5.0 + PostgreSQL
```

### ❌ Hardcoded Paths

**Bad**:
```markdown
Copy to /Users/user/project/
```

**Good**:
```markdown
Copy to current working directory
Detect project root via .git/ or package.json
```

### ❌ Version Mismatch

**Bad**:
```json
{
  "metadata": {"version": "1.1.0"},
  "plugins": [{"version": "1.0.0"}]
}
```

**Good**:
```json
{
  "metadata": {"version": "1.1.0"},
  "plugins": [{"version": "1.1.0"}]
}
```

---

## Performance Optimization

### Template Size Optimization

- **Target**: <400 lines per template
- **Technique**: Use examples instead of exhaustive content
- **Token goal**: <5k tokens when filled out

### Command Execution Speed

- **Goal**: <5 seconds for `/nav:init`
- **Technique**: Minimize file operations
- **User experience**: Show progress messages

### Distribution Size

- **Plugin size**: <50KB
- **Install time**: <5 seconds
- **No external dependencies**: Pure markdown/JSON

---

## Future Patterns

### Modular Plugin Architecture

```
nav-core/         # Base Navigator functionality
nav-linear/       # Linear integration
nav-slack/        # Slack notifications
nav-nextjs/       # Next.js-specific templates
```

**Benefits**:
- Users install only what they need
- Smaller plugin sizes
- Community extensions

### Community Template System

```
templates/
├── core/          # Universal (from plugin)
├── nextjs/        # Next.js-specific (community)
├── django/        # Django-specific (community)
└── go/            # Go-specific (community)
```

**Distribution**: Separate GitHub repos, installable via plugin

---

**Last Updated**: 2025-10-10
**Pattern Version**: 1.0
