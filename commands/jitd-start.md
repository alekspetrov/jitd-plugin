---
description: Start JITD session - load navigator, set context, check tasks
---

# Start JITD Session

Initialize your development session with JITD workflow and context optimization.

---

## What This Command Does

1. Loads documentation navigator
2. Sets JITD workflow context
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
- Ask user if JITD is initialized
- Suggest running `/jitd-init` first
- Exit command

---

### Step 2: Set Session Context

**Load JITD configuration**:

```
Read(
  file_path: ".agent/.jitd-config.json"
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

### Step 4: Session Context Summary

**Show this summary**:

```
╔══════════════════════════════════════════════════════╗
║                                                      ║
║  🚀 JITD Session Started                             ║
║                                                      ║
╚══════════════════════════════════════════════════════╝

📖 Documentation Navigator: Loaded
🎯 Project Management: [PM tool or "Manual"]
✅ Token Optimization: Active

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

🔹 JITD WORKFLOW REMINDER

1. Navigator-first loading
   - Loaded: .agent/DEVELOPMENT-README.md
   - Next: Load ONLY relevant task/system docs

2. Task documentation
   - After features: /update-doc feature [TASK-XX]
   - After bugs: /update-doc sop debugging [issue]

3. Context management
   - Current: [X]k tokens used
   - Run /jitd-compact after isolated sub-tasks

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

### Step 5: PM Tool Setup Check

**If PM tool configured but not working**:

For **Linear**:
```
⚠️  Linear configured but MCP not detected

Setup Linear MCP:
1. Install: claude mcp add linear-server
2. Configure API key when prompted
3. Test: /jitd-start (run this command again)

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

**Traditional approach** (without JITD):
- All docs loaded: 150k tokens
- Available for work: ~50k tokens (25%)
- Session restarts: 3-4 per day

**JITD advantage**: 3.5x more context available

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
4. Document: /update-doc feature TASK-XX
```

**If debugging issue**:
```
1. Check .agent/sops/debugging/ for similar issues
2. Load relevant system doc for context
3. Fix issue
4. Document: /update-doc sop debugging [issue-name]
```

---

## Troubleshooting

### Navigator not found

**Error**: `.agent/DEVELOPMENT-README.md` doesn't exist

**Solution**:
```
Run /jitd-init to initialize JITD structure
```

### PM tool not responding

**Error**: Linear/GitHub commands fail

**Solution**:
1. Check `.agent/.jitd-config.json`
2. Verify PM tool is installed
3. Check authentication
4. Update config if needed

### Config file malformed

**Error**: Cannot parse `.agent/.jitd-config.json`

**Solution**:
```bash
# Validate JSON
cat .agent/.jitd-config.json | jq .

# Fix any syntax errors
# Re-run /jitd-init if corrupted
```

---

## Success Criteria

**This command succeeds when**:
- [ ] Navigator loaded successfully
- [ ] JITD workflow context set
- [ ] Token optimization active
- [ ] PM tool status checked (if configured)
- [ ] User knows what to work on next

---

**This command sets you up for maximum productivity with minimal token waste** 🚀
