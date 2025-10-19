---
description: "[DEPRECATED] Use /nav:start instead - Start Navigator session"
---

⚠️ **DEPRECATION WARNING**

The `/jitd:start` command is deprecated and will be removed in Navigator v3.0.

**Plugin Renamed**: JITD → Navigator (v2.0)

**Update your workflow**:
- ~~`/jitd:start`~~ → **`/nav:start`**
- ~~`/jitd:marker`~~ → **`/nav:marker`**
- ~~`/jitd:compact`~~ → **`/nav:compact`**
- ~~`/jitd:update-doc`~~ → **`/nav:doc`**

**Backward compatibility will be removed in v3.0** (6-12 months)

Run `/nav:migrate` to update your documentation.

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

**Executing /nav:start for you...**

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

### Step 1.5: Check for Active Context Marker

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
   - Use Read tool to load the marker
   - Show confirmation message
   - Delete .active file (marker consumed)

4. **If user declines (n)**:
   - Skip marker load
   - Delete .active file

5. **Continue to Step 2**

---

### Step 2: Set Session Context

**Load Navigator configuration**:

```
Read(
  file_path: ".agent/.nav-config.json"
)
```

If file doesn't exist, try legacy location:
```
Read(
  file_path: ".agent/.jitd-config.json"
)
```

**If found old config**: Show migration warning and suggest `/nav:migrate`

**Parse configuration**:
- `project_management`: Which PM tool is configured
- `task_prefix`: Task numbering system
- `team_chat`: Team communication tool

---

### Step 3: Check for Assigned Tasks

**Based on PM tool configured**, check for assigned work.

Skip this step in backward compat mode (legacy behavior).

---

### Step 4: Calculate Token Usage

**Measure files loaded**:

```bash
nav_bytes=$(wc -c < .agent/DEVELOPMENT-README.md 2>/dev/null || echo "0")
nav_tokens=$((nav_bytes / 4))

claude_bytes=$(wc -c < CLAUDE.md 2>/dev/null || echo "0")
claude_tokens=$((claude_bytes / 4))

total_tokens=$((nav_tokens + claude_tokens))
available=$((200000 - 50000 - total_tokens))
percent=$((available * 100 / 200000))
```

---

### Step 5: Session Summary

Show session started message with token measurements and Navigator workflow reminders.

---

**📝 Remember**: This command is deprecated. Please update to `/nav:start`
