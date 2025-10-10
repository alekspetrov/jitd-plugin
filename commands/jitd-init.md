---
description: Initialize JITD documentation structure in your project
---

# Initialize JITD - Just-In-Time Documentation

You are setting up the JITD (Just-In-Time Documentation) system in this project.

**What JITD Does**:
- Problem: AI loads 150k+ tokens of docs upfront
- Solution: Load on-demand (92% reduction to ~12k tokens)
- Result: 86%+ context free for work, zero session restarts

---

## EXECUTION PLAN

You will execute these steps in order. Each step has explicit tool calls.

---

## Step 1: Pre-Flight Checks

### Check for existing CLAUDE.md

```bash
ls CLAUDE.md 2>/dev/null && echo "EXISTS" || echo "NOT_FOUND"
```

**If EXISTS**:
- Ask user:
  1. Backup and create new (recommended)
  2. Skip CLAUDE.md creation
  3. Cancel
- If choice 1: Run `mv CLAUDE.md CLAUDE.md.backup.$(date +%Y%m%d-%H%M%S)`
- If choice 2: Set flag `SKIP_CLAUDE_MD=true`
- If choice 3: Exit now

### Check for existing .agent/

```bash
ls -la .agent/ 2>/dev/null && echo "EXISTS" || echo "NOT_FOUND"
```

**If EXISTS**:
- Ask user:
  1. Merge (keep existing, add missing)
  2. Backup and recreate
  3. Cancel
- If choice 1: Set flag `MERGE_MODE=true`
- If choice 2: Run `mv .agent .agent.backup.$(date +%Y%m%d-%H%M%S)`
- If choice 3: Exit now

---

## Step 2: Create Folder Structure

**Execute these Bash commands**:

```bash
# Create directory structure
mkdir -p .agent/tasks
mkdir -p .agent/system
mkdir -p .agent/sops/integrations
mkdir -p .agent/sops/debugging
mkdir -p .agent/sops/development
mkdir -p .agent/sops/deployment

# Create .gitkeep files
touch .agent/tasks/.gitkeep
touch .agent/sops/integrations/.gitkeep
touch .agent/sops/debugging/.gitkeep
touch .agent/sops/development/.gitkeep
touch .agent/sops/deployment/.gitkeep
```

**Verify**: Run `tree .agent/ -L 2` to confirm structure created

---

## Step 3: Create CLAUDE.md

**Skip if**: `SKIP_CLAUDE_MD=true` from pre-flight checks

### 3A: Fetch Template

Use the `WebFetch` tool:

```
WebFetch(
  url: "https://raw.githubusercontent.com/alekspetrov/jitd-plugin/main/templates/CLAUDE.md"
  prompt: "Return the complete file content exactly as-is"
)
```

### 3B: Detect Project Info

**Auto-detect** (don't ask user):
- Project name: Extract from `package.json` name field, or use current directory name
- Tech stack: Extract from `package.json` dependencies, or scan for `.py`, `.go`, `Cargo.toml`
- Date: Use today's date from system

### 3C: Customize Template

Replace placeholders in fetched content:
- `[Project Name]` → Detected project name
- `[Brief project description]` → "Project description" (user can customize later)
- `[Your tech stack]` → Detected stack
- `[Key architectural principle]` → "To be defined" (user customizes)
- `[Date]` → Today's date (YYYY-MM-DD format)

### 3D: Write File

Use the `Write` tool:

```
Write(
  file_path: "CLAUDE.md"
  content: [customized template content]
)
```

**Verify**: Run `ls -lh CLAUDE.md` to confirm file exists and size > 8KB

---

## Step 4: Create DEVELOPMENT-README.md

**Skip if**: `MERGE_MODE=true` AND file exists

### 4A: Fetch Template

Use the `WebFetch` tool:

```
WebFetch(
  url: "https://raw.githubusercontent.com/alekspetrov/jitd-plugin/main/templates/DEVELOPMENT-README.md"
  prompt: "Return the complete file content exactly as-is"
)
```

### 4B: Customize Template

Replace placeholders:
- `[Project Name]` → Same as detected earlier
- `[Brief project description]` → Same
- `[Your tech stack]` → Same
- `[Date]` → Today's date

### 4C: Write File

Use the `Write` tool:

```
Write(
  file_path: ".agent/DEVELOPMENT-README.md"
  content: [customized template content]
)
```

**Verify**: Run `ls -lh .agent/DEVELOPMENT-README.md` to confirm file exists

---

## Step 5: Generate System Documentation

### 5A: project-architecture.md

**Scan the project**:
- Look for `package.json`, `requirements.txt`, `go.mod`, `Cargo.toml`
- Scan top-level folder structure

**Generate content**:

```markdown
# Project Architecture

**Tech Stack**: [Detected from package.json or file types]
**Updated**: [Today's date]

## Technology Stack

[List dependencies from package.json or detected files]

## Project Structure

[Output of: ls -la at project root, excluding node_modules, .git]

## Key Components

[List main directories: src/, app/, lib/, etc.]

## Development Workflow

[Extract from package.json scripts if available]
```

**Write**:

```
Write(
  file_path: ".agent/system/project-architecture.md"
  content: [generated content]
)
```

### 5B: tech-stack-patterns.md

**Detect framework**:
- React/Next.js: Check for `react` in dependencies
- Django/Flask: Check for `.py` files + `requirements.txt`
- Go: Check for `go.mod`

**Generate content**:

```markdown
# Tech Stack Patterns

**Framework**: [Detected framework]
**Updated**: [Today's date]

## [Framework] Best Practices

[Framework-specific patterns - use generic template initially]

## Common Patterns

[To be documented as code is written]

## Testing Strategy

[Extract from package.json test scripts or detected test framework]
```

**Write**:

```
Write(
  file_path: ".agent/system/tech-stack-patterns.md"
  content: [generated content]
)
```

---

## Step 6: Create Configuration

### Prompt User for Settings

Ask these questions (don't assume):

```
JITD Configuration
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Project Management Tool:
  1. Linear (MCP integration)
  2. GitHub Issues
  3. Jira
  4. GitLab
  5. None (manual docs)

Choice [1-5]: [wait for input]

Task Prefix (e.g., TASK, GH, JIRA): [wait for input or default to "TASK"]

Team Chat (optional):
  1. Slack
  2. Discord
  3. Teams
  4. None

Choice [1-4]: [wait for input or default to 4]
```

### Write Config File

Use the `Write` tool:

```json
{
  "version": "1.0.0",
  "project_management": "[user choice: linear|github|jira|gitlab|none]",
  "task_prefix": "[user input or 'TASK']",
  "team_chat": "[user choice: slack|discord|teams|none]",
  "auto_load_navigator": true,
  "compact_strategy": "conservative"
}
```

**Write**:

```
Write(
  file_path: ".agent/.jitd-config.json"
  content: [config JSON]
)
```

---

## Step 7: VERIFICATION (CRITICAL)

**Run these checks and SHOW results to user**:

### File Existence Checks

```bash
echo "=== JITD Installation Verification ==="
echo ""
echo "1. CLAUDE.md (project root):"
ls -lh CLAUDE.md 2>/dev/null && echo "✓ EXISTS" || echo "✗ MISSING"

echo ""
echo "2. .agent/DEVELOPMENT-README.md:"
ls -lh .agent/DEVELOPMENT-README.md 2>/dev/null && echo "✓ EXISTS" || echo "✗ MISSING"

echo ""
echo "3. .agent/system/project-architecture.md:"
ls -lh .agent/system/project-architecture.md 2>/dev/null && echo "✓ EXISTS" || echo "✗ MISSING"

echo ""
echo "4. .agent/system/tech-stack-patterns.md:"
ls -lh .agent/system/tech-stack-patterns.md 2>/dev/null && echo "✓ EXISTS" || echo "✗ MISSING"

echo ""
echo "5. .agent/.jitd-config.json:"
ls -lh .agent/.jitd-config.json 2>/dev/null && echo "✓ EXISTS" || echo "✗ MISSING"

echo ""
echo "6. Directory structure:"
tree .agent/ -L 2 2>/dev/null || ls -R .agent/
```

### Content Verification

```bash
echo ""
echo "=== Content Verification ==="
echo ""
echo "CLAUDE.md has placeholders replaced?"
grep -q "\[Project Name\]" CLAUDE.md && echo "✗ FAIL: Placeholders still present" || echo "✓ PASS: Customized"

echo ""
echo "DEVELOPMENT-README.md has placeholders replaced?"
grep -q "\[Project Name\]" .agent/DEVELOPMENT-README.md && echo "✗ FAIL: Placeholders still present" || echo "✓ PASS: Customized"
```

### Success Criteria

**ALL of these must be TRUE**:
- [ ] CLAUDE.md exists and > 8KB
- [ ] .agent/DEVELOPMENT-README.md exists
- [ ] .agent/system/project-architecture.md exists
- [ ] .agent/system/tech-stack-patterns.md exists
- [ ] .agent/.jitd-config.json exists and is valid JSON
- [ ] No `[Project Name]` placeholders remain in CLAUDE.md
- [ ] No `[Project Name]` placeholders remain in DEVELOPMENT-README.md
- [ ] Directory structure complete (tasks/, system/, sops/)

**If ANY check fails**:
- Stop and report error
- Do NOT show success message
- Tell user what's missing

**If ALL checks pass**:
- Proceed to Step 8 (Success Message)

---

## Step 8: Success Message

**Only show this if Step 7 verification passed**:

```
╔══════════════════════════════════════════════════════╗
║                                                      ║
║  ✅ JITD Initialized Successfully!                   ║
║                                                      ║
║  Your project now has:                               ║
║  ✓ CLAUDE.md - Project configuration (~15k tokens)  ║
║  ✓ .agent/DEVELOPMENT-README.md - Navigator (~2k)   ║
║  ✓ .agent/system/ - Architecture docs               ║
║  ✓ .agent/.jitd-config.json - Settings              ║
║  ✓ Complete documentation structure                 ║
║                                                      ║
╚══════════════════════════════════════════════════════╝
```

**If backups were created**:

```
📦 Backups:
- [list any backup files created with timestamps]

Restore with: mv backup-file original-name
Delete after verifying: rm backup-file
```

---

## Step 9: How to Use JITD

**Show this guide**:

```
╔══════════════════════════════════════════════════════╗
║                                                      ║
║  📖 HOW TO USE JITD                                  ║
║                                                      ║
╚══════════════════════════════════════════════════════╝

🔹 EVERY SESSION STARTS WITH:

   Read .agent/DEVELOPMENT-README.md

   This loads your documentation navigator (~2k tokens)
   instead of all docs (~150k tokens).


🔹 WORKING ON A FEATURE:

   1. Read navigator first (see above)
   2. Load ONLY relevant task doc:
      Read .agent/tasks/TASK-XX-feature.md
   3. Load ONLY needed system doc:
      Read .agent/system/project-architecture.md

   Total: ~10k tokens vs 150k (93% savings)


🔹 AFTER COMPLETING FEATURE:

   /update-doc feature TASK-XX

   This creates documentation from your work so:
   - You never solve same problem twice
   - Team knows what you built
   - Future you remembers why


🔹 AFTER SOLVING A BUG:

   /update-doc sop debugging issue-name

   Creates a Standard Operating Procedure so you
   never waste time on this issue again.


🔹 WHEN CONTEXT GETS FULL:

   /jitd-compact

   Clears conversation while preserving JITD markers.
   Run after completing isolated sub-tasks.


🔹 CUSTOMIZING YOUR SETUP:

   1. Edit CLAUDE.md:
      - Add framework-specific rules
      - Set coding standards
      - Configure integrations

   2. Edit .agent/DEVELOPMENT-README.md:
      - Add project-specific setup steps
      - Customize documentation structure


🔹 TOKEN OPTIMIZATION:

   Before JITD: 150k+ tokens loaded upfront
   With JITD:   12k tokens (on-demand loading)
   Reduction:   92%

   Context available for work: 86%+
   Session restarts: Zero


🔹 NEXT ACTIONS:

   [ ] Customize CLAUDE.md with your code standards
   [ ] Customize .agent/DEVELOPMENT-README.md
   [ ] Commit .agent/ to git (share with team)
   [ ] Start using /update-doc after features
   [ ] Read navigator at start of every session


Need help? Check .agent/DEVELOPMENT-README.md for:
- Documentation index
- "When to read what" guide
- Token optimization strategy
```

---

## Post-Installation Integration Setup

**If user selected Linear (Step 6)**:

Show Linear MCP setup:

```
Linear MCP Setup
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

1. Install Linear MCP:
   claude mcp add linear-server

2. Configure API key:
   [Follow prompts]

3. Test:
   /linear list-issues

4. Use with JITD:
   /update-doc feature LIN-123
```

**If user selected GitHub Issues (Step 6)**:

Show GitHub CLI setup:

```
GitHub CLI Setup
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

1. Install gh:
   brew install gh

2. Authenticate:
   gh auth login

3. Test:
   gh issue list

4. Use with JITD:
   /update-doc feature GH-123
```

---

## Troubleshooting

### WebFetch fails

**Error**: "Cannot fetch template"

**Solution**:
- Check internet connection
- Try again (GitHub may be temporarily down)
- Fallback: Manually create CLAUDE.md from https://github.com/alekspetrov/jitd-plugin/blob/main/templates/CLAUDE.md

### Verification fails

**Error**: File exists but placeholders remain

**Fix**:
- Manually edit the file
- Replace `[Project Name]` with your project name
- Replace `[Your tech stack]` with your stack
- Replace `[Date]` with today's date

### Permission denied

**Error**: Cannot create .agent/

**Fix**:
```bash
# Check current directory
pwd

# Ensure you're in project root
cd /path/to/your/project

# Run /jitd-init again
```

---

**Remember**: JITD saves 92% documentation loading overhead through on-demand loading, not upfront loading.

**Your context is now optimized for productivity** 🚀
