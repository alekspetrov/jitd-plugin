---
description: Start Navigator session - load navigator, set context, check tasks
---

# Start Navigator Session

Initialize your development session with Navigator workflow and context optimization.

---

## What This Command Does

1. Loads documentation navigator
2. Sets Navigator workflow context
3. Checks for assigned tasks (if PM tool configured)
4. Reminds about token optimization strategy

---

## EXECUTION PLAN

### Step 1: Load Documentation Navigator

**ALWAYS start with this**:

```
Read(
  file_path: ".agent/DEVELOPMENT-README.md"
)
```

**If file not found**:
- Ask user if Navigator is initialized
- Suggest running `/nav:init` first
- Exit command

---

### Step 1.5: Check for Active Context Marker (NEW)

**Check if resuming from compact**:

```bash
cat .agent/.context-markers/.active 2>/dev/null
```

**If .active file exists**:

1. Read the filename from .active file
2. Show detection message:
   ```
   🔄 Active context marker detected!

   Marker: [marker-name]
   Created: [timestamp from filename]

   This marker was saved during your last /nav:compact.
   Load it to continue where you left off?

   [Y/n]:
   ```

3. **If user confirms (Y or Enter)**:
   - Use Read tool to load the marker:
     ```
     Read(
       file_path: ".agent/.context-markers/[filename-from-active]"
     )
     ```
   - Show confirmation:
     ```
     ✅ Context restored from marker!

     Your previous session state has been loaded.
     Continue with your work.
     ```
   - Delete .active file (marker consumed):
     ```bash
     rm .agent/.context-markers/.active
     ```

4. **If user declines (n)**:
   - Show message:
     ```
     Skipping marker load. You can load it later with:
     /nav:markers
     ```
   - Delete .active file (user chose not to load)

5. **Continue to Step 2**

**If .active file doesn't exist**:
- No active marker (normal session start)
- Continue to Step 2

---

### Step 2: Set Session Context

**Load Navigator configuration**:

```
Read(
  file_path: ".agent/.nav-config.json"
)
```

**Parse configuration**:
- `project_management`: Which PM tool is configured
- `task_prefix`: Task numbering system (TASK, GH, LIN, etc.)
- `team_chat`: Team communication tool
- `auto_load_navigator`: Whether to auto-load on startup

---

### Step 3: Check for Assigned Tasks

**If PM tool is Linear**:

```bash
# Check if Linear MCP is available
# Try to list assigned issues
```

If Linear MCP is configured and working:
- List issues assigned to user
- Show recent activity
- Ask which task to work on

**If PM tool is GitHub**:

```bash
gh issue list --assignee @me --limit 10
```

**If PM tool is Jira/GitLab**:
- Show manual workflow (API integration not auto-configured)
- Remind to check dashboard

**If PM tool is none**:
- Skip task checking
- Remind to manually track work

---

### Step 4: Calculate Actual Token Usage

**Measure files loaded in this session**:

```bash
# Get navigator size
nav_bytes=$(wc -c < .agent/DEVELOPMENT-README.md 2>/dev/null || echo "0")
nav_tokens=$((nav_bytes / 4))

# Get CLAUDE.md size (auto-loaded by Claude Code)
claude_bytes=$(wc -c < CLAUDE.md 2>/dev/null || echo "0")
claude_tokens=$((claude_bytes / 4))

# Calculate total
total_tokens=$((nav_tokens + claude_tokens))

# Calculate available (200k total context window)
# System overhead: ~50k tokens
available=$((200000 - 50000 - total_tokens))
percent=$((available * 100 / 200000))
```

**Store these values for display**.

---

### Step 4.5: Extract Real Session Statistics (NEW)

**Get actual token usage from Claude Code internals**:

```bash
# Run session stats script
if [ -f "./scripts/session-stats.sh" ]; then
  session_stats=$(./scripts/session-stats.sh 2>/dev/null)

  # If successful, parse the output
  if [ $? -eq 0 ]; then
    # Extract values (format: KEY=VALUE)
    eval "$session_stats"

    # Now have variables:
    # - MESSAGES (number of messages in session)
    # - INPUT_TOKENS (fresh input tokens)
    # - OUTPUT_TOKENS (assistant responses)
    # - CACHE_CREATION (tokens loaded into cache)
    # - CACHE_READ (tokens read from cache)
    # - TOTAL_FRESH (input + cache_creation)
    # - TOTAL_CACHED (input + cache_read)
    # - CACHE_EFFICIENCY (percentage cached)

    has_session_stats=true
  else
    has_session_stats=false
  fi
else
  has_session_stats=false
fi
```

**If session stats available**:
- Display in summary (Step 5)
- Show cache efficiency
- Prove on-demand loading works

**If not available**:
- Just show file-size measurements
- Session stats optional (nice-to-have)

---

### Step 5: Session Context Summary

**Show this summary with REAL token counts**:

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

   Total with all docs:        ~[total_tokens + 15]k tokens

   vs Traditional (all upfront): ~150k tokens
   Savings: ~[150 - total_tokens - 15]k tokens

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
```

**If session stats available (has_session_stats=true), add this section**:

```
📈 REAL SESSION STATISTICS (from Claude Code internals)
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Messages in session:     [MESSAGES]
Input tokens:            [INPUT_TOKENS]
Output tokens:           [OUTPUT_TOKENS]

Cache Performance:
  Cache creation:        [CACHE_CREATION] tokens
  Cache read:            [CACHE_READ] tokens
  Cache efficiency:      [CACHE_EFFICIENCY]%

Total session usage:
  Fresh input:           [TOTAL_FRESH] tokens
  Cached read:           [TOTAL_CACHED] tokens

💡 What this means:
   Documentation loaded once ([CACHE_CREATION] tokens)
   Then reused from cache ([CACHE_READ] tokens)
   Result: Zero fresh tokens for repeated doc access

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
```

**Continue with workflow reminder**:

```
🔹 Navigator WORKFLOW REMINDER

1. Navigator-first loading
   - ✅ Loaded: .agent/DEVELOPMENT-README.md
   - Next: Load ONLY relevant task/system docs

2. Task documentation
   - After features: /nav:update-doc feature [TASK-XX]
   - After bugs: /nav:update-doc sop debugging [issue]

3. Context management
   - Run /nav:compact after isolated sub-tasks
   - Context markers save your progress

4. Agent usage for complex tasks
   - Use agents for multi-step research
   - Use agents for code search across files
   - Reduces token usage by 60-80%

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

[If tasks found from PM tool, list them here]

[If no tasks found, show:]
No active tasks found. What would you like to work on?

```

---

### Step 6: PM Tool Setup Check

**If PM tool configured but not working**:

For **Linear**:
```
⚠️  Linear configured but MCP not detected

Setup Linear MCP:
1. Install: claude mcp add linear-server
2. Configure API key when prompted
3. Test: /nav:start (run this command again)

Need help? Check .agent/sops/integrations/linear-mcp.md
```

For **GitHub**:
```
⚠️  GitHub configured but gh CLI not working

Setup GitHub CLI:
1. Install: brew install gh
2. Authenticate: gh auth login
3. Test: gh issue list

Need help? Check .agent/sops/integrations/github-cli.md
```

---

## Token Optimization Strategy

**This session**:
- Navigator loaded: ~2k tokens
- CLAUDE.md (auto-loaded): ~15k tokens
- Available for work: ~180k tokens (90%+)

**As you work**:
- Load task doc: +3k tokens
- Load system doc: +5k tokens
- Total used: ~25k tokens
- Still available: ~175k tokens (87%+)

**Traditional approach** (without Navigator):
- All docs loaded: 150k tokens
- Available for work: ~50k tokens (25%)
- Session restarts: 3-4 per day

**Navigator advantage**: 3.5x more context available

---

## Next Steps

**If working on existing task**:
```
Read .agent/tasks/[TASK-XX]-feature.md
```

**If starting new feature**:
```
1. Create task doc: .agent/tasks/TASK-XX-feature.md
2. Plan implementation
3. Execute with TodoWrite tracking
4. Document: /nav:update-doc feature TASK-XX
```

**If debugging issue**:
```
1. Check .agent/sops/debugging/ for similar issues
2. Load relevant system doc for context
3. Fix issue
4. Document: /nav:update-doc sop debugging [issue-name]
```

---

## Troubleshooting

### Navigator not found

**Error**: `.agent/DEVELOPMENT-README.md` doesn't exist

**Solution**:
```
Run /nav:init to initialize Navigator structure
```

### PM tool not responding

**Error**: Linear/GitHub commands fail

**Solution**:
1. Check `.agent/.nav-config.json`
2. Verify PM tool is installed
3. Check authentication
4. Update config if needed

### Config file malformed

**Error**: Cannot parse `.agent/.nav-config.json`

**Solution**:
```bash
# Validate JSON
cat .agent/.nav-config.json | jq .

# Fix any syntax errors
# Re-run /nav:init if corrupted
```

---

## Success Criteria

**This command succeeds when**:
- [ ] Navigator loaded successfully
- [ ] Navigator workflow context set
- [ ] Token optimization active
- [ ] PM tool status checked (if configured)
- [ ] User knows what to work on next

---

**This command sets you up for maximum productivity with minimal token waste** 🚀
