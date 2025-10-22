---
name: nav-start
description: Load Navigator documentation navigator when starting development session, resuming work, or beginning new feature. Use when user mentions starting work, beginning session, resuming after break, or checking project status.
allowed-tools: Read, Bash
version: 1.0.0
---

# Navigator Navigator Skill

Load the Navigator documentation navigator to start your development session with optimized context.

## When to Invoke

Invoke this skill when the user:
- Says "start my session", "begin work", "start working"
- Says "load the navigator", "show me the docs"
- Asks "what should I work on?"
- Mentions "resume work", "continue from where I left off"
- Asks about project structure or current tasks

**DO NOT invoke** if:
- User already ran `/nav:start` command this conversation
- Navigator already loaded (check conversation history)
- User is in middle of implementation (only invoke at session start)

## Execution Steps

### Step 1: Check Navigator Version

Check if user is running latest Navigator version:

```bash
# Run version checker (optional - doesn't block session start)
if [ -f "scripts/check-version.sh" ]; then
  bash scripts/check-version.sh

  # Note: Exit code 1 means update available, but don't block session
  # Exit code 0 means up to date
  # Exit code 2 means cannot check (network issue)
fi
```

**Version check behavior**:
- If update available: Show notification, continue session
- If up to date: Show ✅, continue session
- If cannot check: Skip silently, continue session

**Never block session start** due to version check.

### Step 2: Check Navigator Initialization

Check if `.agent/DEVELOPMENT-README.md` exists:

```bash
if [ ! -f ".agent/DEVELOPMENT-README.md" ]; then
  echo "❌ Navigator not initialized in this project"
  echo ""
  echo "Run /nav:init to set up Navigator structure first."
  exit 1
fi
```

If not found, inform user to run `/nav:init` first.

### Step 3: Load Documentation Navigator

Read the navigator file:

```
Read(
  file_path: ".agent/DEVELOPMENT-README.md"
)
```

This is the lightweight index (~2k tokens) that tells you:
- What documentation exists
- When to load specific docs
- Current task focus
- Project structure overview

### Step 4: Check for Active Context Marker

Check if there's an active marker from previous `/nav:compact`:

```bash
if [ -f ".agent/.context-markers/.active" ]; then
  marker_file=$(cat .agent/.context-markers/.active)
  echo "🔄 Active context marker detected!"
  echo ""
  echo "Marker: $marker_file"
  echo ""
  echo "This marker was saved during your last /nav:compact."
  echo "Load it to continue where you left off?"
  echo ""
  echo "[Y/n]:"
fi
```

If user confirms (Y or Enter):
- Read the marker file: `Read(file_path: ".agent/.context-markers/{marker_file}")`
- Delete `.active` file: `rm .agent/.context-markers/.active`
- Show confirmation: "✅ Context restored from marker!"

If user declines (n):
- Delete `.active` file
- Show: "Skipping marker load. You can load it later with /nav:markers"

### Step 5: Load Navigator Configuration

Read configuration:

```
Read(
  file_path: ".agent/.nav-config.json"
)
```

Parse:
- `project_management`: Which PM tool (linear, github, jira, none)
- `task_prefix`: Task ID format (TASK, GH, LIN, etc.)
- `team_chat`: Team notifications (slack, discord, none)

### Step 6: Check PM Tool for Assigned Tasks

**If PM tool is Linear**:
```bash
# Check if Linear MCP available
# Try to list assigned issues
```

**If PM tool is GitHub**:
```bash
gh issue list --assignee @me --limit 10 2>/dev/null
```

**If PM tool is none**:
Skip task checking.

### Step 7: Display Session Statistics (OpenTelemetry)

Run the OpenTelemetry session statistics script:

```bash
# Get the skill's base directory (passed via SKILL_BASE_DIR)
SKILL_DIR="${SKILL_BASE_DIR:-$HOME/.claude/plugins/marketplaces/jitd-marketplace/skills/nav-start}"
python3 "$SKILL_DIR/scripts/otel_session_stats.py"
```

This script:
- **If OTel enabled**: Shows real-time metrics from Claude Code
  - Real token usage (input/output/cache)
  - Cache hit rate (CLAUDE.md caching performance)
  - Session cost (actual USD spent)
  - Active time (seconds of work)
  - Context availability
- **If OTel disabled**: Shows setup instructions
- **If no metrics yet**: Shows "waiting for export" message

**Benefits of OTel integration**:
- Real data (not file-size estimates)
- Cache performance validation
- Cost tracking for ROI measurement
- Official API (won't break on updates)

### Step 8: Display Session Summary

Show this formatted summary:

```
╔══════════════════════════════════════════════════════╗
║                                                      ║
║  🚀 Navigator Session Started                             ║
║                                                      ║
╚══════════════════════════════════════════════════════╝

📖 Documentation Navigator: Loaded
🎯 Project Management: [PM tool or "Manual"]
✅ Token Optimization: Active

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

📊 DOCUMENTATION LOADED (MEASURED)
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Navigator (.agent/DEVELOPMENT-README.md):
  Size: [nav_bytes] bytes = [nav_tokens] tokens

CLAUDE.md (auto-loaded):
  Size: [claude_bytes] bytes = [claude_tokens] tokens

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Total documentation:     [total_tokens] tokens
Available for work:      [available] tokens ([percent]%)
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

💡 On-demand loading strategy:
   Load task doc when needed:  +3-5k tokens
   Load system doc if needed:  +4-6k tokens
   Load SOP if helpful:        +2-3k tokens

   Total with all docs:        ~[total + 15]k tokens

   vs Traditional (all upfront): ~150k tokens
   Savings: ~[150 - total - 15]k tokens

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

🔹 Navigator WORKFLOW REMINDER

1. Navigator-first loading
   - ✅ Loaded: .agent/DEVELOPMENT-README.md
   - Next: Load ONLY relevant task/system docs

2. Use agents for research
   - Multi-file searches: Use Task agent (saves 60-80% tokens)
   - Code exploration: Use Explore agent
   - NOT manual Read of many files

3. Task documentation
   - After features: Use nav-task-manager skill
   - After bugs: Use nav-sop-creator skill

4. Context management
   - Run nav-compact skill after isolated sub-tasks
   - Context markers save your progress

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

[If tasks found from PM tool, list them here]

[If no tasks found:]
No active tasks found. What would you like to work on?
```

## Predefined Functions

### scripts/otel_session_stats.py

**Purpose**: Display real-time session statistics via OpenTelemetry

**When to call**: After loading navigator, before presenting session summary

**Requirements**:
- CLAUDE_CODE_ENABLE_TELEMETRY=1 (optional - shows setup if disabled)
- Metrics available from current session (shows waiting message if not)

**Execution**:
```bash
SKILL_DIR="${SKILL_BASE_DIR:-$HOME/.claude/plugins/marketplaces/jitd-marketplace/skills/nav-start}"
python3 "$SKILL_DIR/scripts/otel_session_stats.py"
```

**Output**: Formatted statistics with:
- Token usage breakdown (input/output/cache)
- Cache hit rate percentage
- Session cost in USD
- Active time
- Context availability

**Error Handling**:
- If OTel not enabled: Shows setup instructions
- If no metrics yet: Shows "waiting for export" message
- Never crashes - always displays helpful guidance

## Reference Files

This skill uses:
- **otel_session_stats.py**: Real-time session stats via OpenTelemetry
- **.agent/DEVELOPMENT-README.md**: Navigator content
- **.agent/.nav-config.json**: Configuration
- **.agent/.context-markers/.active**: Active marker check

## Error Handling

**Navigator not found**:
```
❌ Navigator not initialized

Run /nav:init to create .agent/ structure first.
```

**PM tool configured but not working**:
```
⚠️  [PM Tool] configured but not accessible

Check authentication or run setup guide.
```

**Config file malformed**:
```
⚠️  .agent/.nav-config.json is invalid JSON

Fix syntax or run /nav:init to regenerate.
```

## Success Criteria

Session start is successful when:
- [ ] Navigator loaded successfully
- [ ] Token usage calculated and displayed
- [ ] PM tool status checked (if configured)
- [ ] User knows what to work on next
- [ ] Navigator workflow context set

## Notes

This skill provides the same functionality as `/nav:start` command but with:
- Natural language invocation (no need to remember `/` syntax)
- Auto-detection based on user intent
- Composable with other Navigator skills

If user prefers manual invocation, they can still use `/nav:start` command (both work in hybrid mode).
