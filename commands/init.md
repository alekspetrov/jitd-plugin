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
mkdir -p .agent/.context-markers

# Create .gitkeep files
touch .agent/tasks/.gitkeep
touch .agent/sops/integrations/.gitkeep
touch .agent/sops/debugging/.gitkeep
touch .agent/sops/development/.gitkeep
touch .agent/sops/deployment/.gitkeep
touch .agent/.context-markers/.gitkeep
```

**Verify**: Run `tree .agent/ -L 2` to confirm structure created

---

## Step 3: Create CLAUDE.md

**Skip if**: `SKIP_CLAUDE_MD=true` from pre-flight checks

### 3A: Fetch Template

Use the `Bash` tool with curl:

```bash
curl -fsSL https://raw.githubusercontent.com/alekspetrov/jitd-plugin/main/templates/CLAUDE.md -o /tmp/jitd-template-CLAUDE.md
```

**Verify**: Run `ls -lh /tmp/jitd-template-CLAUDE.md` to confirm download

### 3B: Detect Project Info

**Auto-detect** (don't ask user):
- Project name: Extract from `package.json` name field, or use current directory name
- Tech stack: Extract from `package.json` dependencies, or scan for `.py`, `.go`, `Cargo.toml`
- Date: Use today's date from system

### 3C: Read Template

Use the `Read` tool to read the downloaded template:

```
Read(
  file_path: "/tmp/jitd-template-CLAUDE.md"
)
```

### 3D: Customize Template

Replace placeholders in the template content you just read:
- `[Project Name]` → Detected project name
- `[Brief project description]` → "Project description" (user can customize later)
- `[Your tech stack]` → Detected stack
- `[Key architectural principle]` → "To be defined" (user customizes)
- `[Date]` → Today's date (YYYY-MM-DD format)

### 3E: Write File

Use the `Write` tool with the customized content:

```
Write(
  file_path: "CLAUDE.md"
  content: [customized template content from previous step]
)
```

**Verify**: Run `ls -lh CLAUDE.md` to confirm file exists and size > 8KB

---

## Step 4: Create DEVELOPMENT-README.md

**Skip if**: `MERGE_MODE=true` AND file exists

### 4A: Fetch Template

Use the `Bash` tool with curl:

```bash
curl -fsSL https://raw.githubusercontent.com/alekspetrov/jitd-plugin/main/templates/DEVELOPMENT-README.md -o /tmp/jitd-template-DEV-README.md
```

**Verify**: Run `ls -lh /tmp/jitd-template-DEV-README.md` to confirm download

### 4B: Read Template

Use the `Read` tool:

```
Read(
  file_path: "/tmp/jitd-template-DEV-README.md"
)
```

### 4C: Customize Template

Replace placeholders in the template content:
- `[Project Name]` → Same as detected earlier
- `[Brief project description]` → Same
- `[Your tech stack]` → Same
- `[Date]` → Today's date

### 4D: Write File

Use the `Write` tool with customized content:

```
Write(
  file_path: ".agent/DEVELOPMENT-README.md"
  content: [customized template content from previous step]
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

## Step 6.3: Setup .gitignore for JITD

**Create .gitignore entry for context markers**:

Context markers are session-specific and shouldn't be committed to git.

### 6.3A: Fetch .gitignore template

```bash
curl -fsSL https://raw.githubusercontent.com/alekspetrov/jitd-plugin/main/templates/.gitignore -o /tmp/jitd-template-gitignore
```

### 6.3B: Append to existing .gitignore or create new

**If .gitignore exists**:
```bash
# Append JITD entries
cat /tmp/jitd-template-gitignore >> .gitignore
```

**If .gitignore doesn't exist**:
```bash
# Create new .gitignore
cp /tmp/jitd-template-gitignore .gitignore
```

**Result**: Context markers are git-ignored but directory structure is preserved

---

## Step 6.5: PM Tool Integration Setup

**Run this step AFTER config file is created**

### Check PM Tool Selection

Read `.agent/.jitd-config.json` to get `project_management` value.

### If Linear Selected

**Check if Linear MCP is available**:

```bash
# Check if MCP tools starting with mcp__linear are available
# This will be visible if Linear MCP is installed and configured
echo "Checking for Linear MCP..."
```

**If Linear MCP is NOT detected**:

Show setup instructions:

```
╔══════════════════════════════════════════════════════╗
║                                                      ║
║  🔧 Linear MCP Setup Required                        ║
║                                                      ║
╚══════════════════════════════════════════════════════╝

You selected Linear for project management, but Linear MCP
is not configured yet.

SETUP STEPS:

1. Install Linear MCP server:

   In your terminal (not here), run:
   $ claude mcp add linear-server

2. When prompted, provide your Linear API key:
   - Get it from: https://linear.app/settings/api
   - Create Personal API Key
   - Copy and paste when prompted

3. Restart Claude Code after installation

4. Test Linear integration:
   /jitd:start

   This will verify Linear is working and show your tasks.

ALTERNATIVE: Manual Workflow

If you prefer not to use Linear MCP:
- Update .agent/.jitd-config.json
- Change "project_management": "none"
- Track tasks manually

Would you like me to:
1. Continue setup (you'll configure Linear manually later)
2. Change config to "none" now
3. Wait while you set up Linear MCP

[Wait for user choice]
```

**If choice is 1 or 3**: Continue to next step

**If choice is 2**: Update `.agent/.jitd-config.json` to set `"project_management": "none"`

**If Linear MCP IS detected**:

Create Linear integration SOP:

```markdown
# Linear MCP Integration

**Status**: ✅ Configured
**Updated**: [Today's date]

## Setup

Linear MCP is installed and ready to use.

## Common Commands

### List Your Assigned Issues

Use Claude Code's Linear MCP tools:
- List issues assigned to you
- Filter by status (backlog, todo, in progress, done)
- Search by team or project

### Create Issue from Chat

Describe the issue and ask to create it in Linear.

### Update Issue Status

Reference issue ID (e.g., "LIN-123") and request status update.

### Add Comments

Mention issue ID and provide comment text.

## JITD Workflow Integration

### Starting Work on Issue

```
1. /jitd:start
   - Lists your assigned issues
2. Select issue to work on
3. Claude loads issue details from Linear
4. Creates .agent/tasks/LIN-XXX-feature.md
5. Begin implementation
```

### Completing Issue

```
1. Finish implementation
2. /jitd:update-doc feature LIN-XXX
   - Archives task doc
   - Updates system docs if needed
3. Update Linear issue status (done/completed)
4. Add completion comment to Linear
```

### Best Practices

- Use Linear issue ID in commit messages
- Reference LIN-XXX in task documentation
- Update Linear status as you progress
- Add technical notes as Linear comments

## Troubleshooting

### MCP Not Responding

**Symptoms**: Linear commands fail or timeout

**Solutions**:
1. Check API key is valid
2. Restart Claude Code
3. Verify Linear workspace access
4. Check internet connection

### Rate Limiting

**Symptoms**: "Too many requests" errors

**Solution**:
- Wait a few minutes
- Linear API has rate limits
- Batch operations when possible

---

**Linear MCP makes JITD even more powerful by connecting docs to real tasks** 🚀
```

Write this to: `.agent/sops/integrations/linear-mcp.md`

### If GitHub Selected

**Check if gh CLI is available**:

```bash
which gh && gh --version || echo "GH_NOT_FOUND"
```

**If gh CLI is NOT installed**:

Show setup instructions:

```
╔══════════════════════════════════════════════════════╗
║                                                      ║
║  🔧 GitHub CLI Setup Required                        ║
║                                                      ║
╚══════════════════════════════════════════════════════╝

You selected GitHub Issues for project management.
This requires GitHub CLI (gh).

SETUP STEPS:

1. Install GitHub CLI:

   macOS:    $ brew install gh
   Linux:    $ sudo apt install gh
   Windows:  Download from https://cli.github.com

2. Authenticate:

   $ gh auth login

   Follow prompts to authenticate with your GitHub account.

3. Test:

   $ gh issue list

   Should show issues from current repository.

4. Use with JITD:

   /jitd:start will now show your GitHub issues

ALTERNATIVE: Manual Workflow

If you prefer not to use GitHub CLI:
- Update .agent/.jitd-config.json
- Change "project_management": "none"
- Track tasks manually

Would you like me to:
1. Continue setup (you'll configure gh CLI later)
2. Change config to "none" now

[Wait for user choice]
```

**If gh CLI IS installed**:

Check authentication:

```bash
gh auth status
```

If authenticated, create GitHub integration SOP:

```markdown
# GitHub CLI Integration

**Status**: ✅ Configured
**Updated**: [Today's date]

## Setup

GitHub CLI is installed and authenticated.

## Common Commands

### List Your Issues

```bash
gh issue list --assignee @me
```

### View Issue Details

```bash
gh issue view [issue-number]
```

### Create Issue

```bash
gh issue create --title "Title" --body "Description"
```

### Update Issue

```bash
gh issue edit [issue-number] --add-label "in-progress"
gh issue close [issue-number]
```

## JITD Workflow Integration

### Starting Work on Issue

```
1. /jitd:start
   - Lists your assigned GitHub issues via gh CLI
2. Select issue to work on
3. Claude loads issue details
4. Creates .agent/tasks/GH-XXX-feature.md
5. Begin implementation
```

### Completing Issue

```
1. Finish implementation
2. /jitd:update-doc feature GH-XXX
   - Archives task doc
   - Updates system docs if needed
3. Close issue: gh issue close XXX
4. Add completion comment if needed
```

### Best Practices

- Use "Fixes #XXX" in commit messages
- Reference GH-XXX in task documentation
- Add labels as status changes
- Keep issue updated with progress

## Troubleshooting

### Auth Expired

**Symptoms**: gh commands fail with auth error

**Solution**:
```bash
gh auth refresh
# or
gh auth login
```

### Wrong Repository

**Symptoms**: Issues from wrong project

**Solution**:
- Ensure you're in correct directory
- Check remote: git remote -v
- Use -R flag: gh issue list -R owner/repo

---

**GitHub CLI + JITD = Seamless issue tracking** 🚀
```

Write this to: `.agent/sops/integrations/github-cli.md`

### If Jira or GitLab Selected

Show manual setup instructions:

```
╔══════════════════════════════════════════════════════╗
║                                                      ║
║  📋 Manual Integration Setup                         ║
║                                                      ║
╚══════════════════════════════════════════════════════╝

You selected [Jira/GitLab] for project management.

Currently, JITD doesn't have automated integration for this tool.

MANUAL WORKFLOW:

1. Check your [Jira/GitLab] dashboard for assigned tasks
2. When starting work, create task doc manually:

   Write(
     file_path: ".agent/tasks/[PREFIX]-XXX-feature.md"
     content: [task details from ticket]
   )

3. Work on implementation with JITD workflow
4. When complete: /jitd:update-doc feature [PREFIX]-XXX
5. Update [Jira/GitLab] status manually

FUTURE: API integration may be added in future versions

Would you like to:
1. Continue with manual workflow
2. Change to Linear/GitHub for automation
3. Change to "none"

[Wait for user choice]
```

### If None Selected

Skip PM tool setup entirely. No SOP needed.

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

   /jitd:update-doc feature TASK-XX

   This creates documentation from your work so:
   - You never solve same problem twice
   - Team knows what you built
   - Future you remembers why


🔹 AFTER SOLVING A BUG:

   /jitd:update-doc sop debugging issue-name

   Creates a Standard Operating Procedure so you
   never waste time on this issue again.


🔹 SAVE YOUR PROGRESS ANYTIME:

   /jitd:marker lunch-break

   Creates a save point you can restore later.
   Perfect for:
   - Before taking breaks
   - Before risky changes
   - End of day
   - After important decisions

   Resume: Read @.agent/.context-markers/[marker-name].md


🔹 WHEN CONTEXT GETS FULL:

   /jitd:compact

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
   [ ] Start using /jitd:update-doc after features
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
   /jitd:update-doc feature LIN-123
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
   /jitd:update-doc feature GH-123
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

# Run /jitd:init again
```

---

**Remember**: JITD saves 92% documentation loading overhead through on-demand loading, not upfront loading.

**Your context is now optimized for productivity** 🚀
