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

### Step 1: Check Navigator Initialization

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

### Step 2: Load Documentation Navigator

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

### Step 3: Check for Active Context Marker

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

### Step 4: Load Navigator Configuration

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

### Step 5: Check PM Tool for Assigned Tasks

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

### Step 6: Calculate Real Token Usage

Run the session statistics script:

```bash
python3 scripts/session_stats.py
```

This outputs:
- Navigator file size → token count
- CLAUDE.md file size → token count
- Total documentation loaded
- Available context for work

**If script doesn't exist or fails**, fallback to file size calculation:

```bash
nav_bytes=$(wc -c < .agent/DEVELOPMENT-README.md 2>/dev/null || echo "0")
nav_tokens=$((nav_bytes / 4))

claude_bytes=$(wc -c < CLAUDE.md 2>/dev/null || echo "0")
claude_tokens=$((claude_bytes / 4))

total_tokens=$((nav_tokens + claude_tokens))
available=$((200000 - 50000 - total_tokens))
percent=$((available * 100 / 200000))

echo "Navigator: $nav_bytes bytes = $nav_tokens tokens"
echo "CLAUDE.md: $claude_bytes bytes = $claude_tokens tokens"
echo "Total: $total_tokens tokens"
echo "Available: $available tokens ($percent%)"
```

### Step 7: Display Session Summary

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

## Reference Files

This skill uses:
- **session_stats.py**: Calculate token usage from file sizes
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
