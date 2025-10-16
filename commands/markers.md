---
description: Manage context markers - list, load, and clean conversation save points
---

# JITD Markers Management

Manage your context markers: list, load, and clean conversation save points.

**Related**: Use `/jitd:marker` to CREATE new markers.

---

## What This Does

Interactive management of context markers:
- List all markers with details
- Load markers to restore context
- Clean up old markers

---

## Usage

### Interactive Mode (Default)

```bash
/jitd:markers
```

**What happens**:
1. Lists all markers sorted by date (newest first)
2. Shows marker details (name, date, size, task)
3. Prompts you to select one to load
4. Automatically reads selected marker file

**Perfect for**: "What was I working on yesterday?"

### List Mode

```bash
/jitd:markers list
```

**What happens**:
- Shows all markers with details
- No selection prompt
- Just displays information

**Perfect for**: Quick overview of available save points

### Clean Mode

```bash
/jitd:markers clean
```

**What happens**:
1. Shows markers older than 7 days
2. Asks which to keep/delete
3. Removes selected markers

**Perfect for**: Periodic cleanup to avoid clutter

---

## Execution Plan

### Step 1: Check Markers Directory

```bash
ls -la .agent/.context-markers/ 2>/dev/null
```

**If directory doesn't exist**:
```
⚠️  No markers directory found

Context markers aren't set up yet.

To enable markers:
1. Run /jitd:init (if JITD not initialized)
   OR
2. mkdir -p .agent/.context-markers

After setup, create markers with:
   /jitd:marker [name]
```

**Exit command**.

**If directory exists but empty**:
```
📍 No markers found

You haven't created any context markers yet.

To create a marker:
   /jitd:marker lunch-break
   /jitd:marker before-refactor
   /jitd:marker eod-2025-10-12 "Description here"

Markers let you save conversation state and restore later.
```

**Exit command**.

### Step 2: Scan and Parse Markers

**Scan directory**:
```bash
ls -lt .agent/.context-markers/*.md 2>/dev/null | grep -v ".gitkeep"
```

**For each marker file**, extract metadata:
1. **Filename**: Extract name and timestamp from filename format `[name]-YYYY-MM-DD-HHMMSS.md`
2. **File size**: Get size in bytes, convert to tokens (~4 chars/token estimate)
3. **Creation time**: From filename timestamp
4. **Task/content**: Read first 50 lines, extract task ID if present

**Build marker list**:
```javascript
markers = [
  {
    filename: "lunch-break-2025-10-12-120000.md",
    name: "lunch-break",
    timestamp: "2025-10-12 12:00:00",
    age: "2 hours ago",
    size: "3.2k tokens",
    task: "TASK-456", // if found in content
    preview: "First 100 chars of marker content..."
  },
  // ... more markers
]
```

**Sort**: Newest first (by timestamp)

### Step 3: Determine Mode

**Check command arguments**:
- No args or `interactive` → Interactive mode
- `list` → List mode
- `clean` → Clean mode

### Step 4A: Interactive Mode

**Display markers**:
```
📍 Available Context Markers

Recent markers:
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

1. lunch-break (2 hours ago)
   Created: 2025-10-12 12:00
   Task: TASK-456 - Payment integration
   Size: 3.2k tokens
   Preview: "Stripe integration 70% complete, need webhooks..."

2. before-refactor (7 hours ago)
   Created: 2025-10-12 09:15
   Task: TASK-455 - API refactor
   Size: 2.8k tokens
   Preview: "Current routing works, about to refactor..."

3. eod-2025-10-11 (yesterday)
   Created: 2025-10-11 17:00
   Task: TASK-454 - User dashboard
   Size: 3.5k tokens
   Preview: "Dashboard complete, tests passing..."

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Total: 3 markers | Combined size: 9.5k tokens

Which marker would you like to load?
[Enter number, or 'q' to quit]:
```

**Wait for user input**.

**If user selects number**:
1. Validate selection (1-N)
2. Get corresponding marker file
3. Use `Read` tool to load the marker:
   ```
   Read(
     file_path: ".agent/.context-markers/[filename]"
   )
   ```
4. Confirm to user:
   ```
   ✅ Loaded marker: lunch-break

   Context restored from 2 hours ago.
   You can now continue where you left off.
   ```

**If user quits**: Exit gracefully

### Step 4B: List Mode

**Display all markers** (same format as interactive, but no prompt):

```
📍 Available Context Markers

Recent markers (last 30 days):
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

1. lunch-break-2025-10-12-120000.md
   Created: 2025-10-12 12:00 (2 hours ago)
   Task: TASK-456 - Payment integration
   Size: 3.2k tokens

2. before-refactor-2025-10-12-091500.md
   Created: 2025-10-12 09:15 (7 hours ago)
   Task: TASK-455 - API refactor
   Size: 2.8k tokens

3. eod-2025-10-11-170000.md
   Created: 2025-10-11 17:00 (yesterday)
   Task: TASK-454 - User dashboard
   Size: 3.5k tokens

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Total: 3 markers | Combined: 9.5k tokens

To load a marker:
   /jitd:markers

   OR

   Read @.agent/.context-markers/[filename]
```

### Step 4C: Clean Mode

**Filter markers older than 7 days**:
```bash
# Get markers older than 7 days
find .agent/.context-markers/ -name "*.md" -mtime +7 -type f
```

**If none found**:
```
✨ All markers are recent (< 7 days old)

No cleanup needed.

Current markers: 3
Total size: 9.5k tokens
```

**If old markers found**:
```
🧹 Marker Cleanup

Found 8 markers older than 7 days:
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

1. eod-2025-10-01.md (11 days old) - 3.2k tokens
2. lunch-break-2025-09-28.md (14 days old) - 2.8k tokens
3. before-deploy-2025-09-25.md (17 days old) - 3.1k tokens
...
8. marker-2025-09-15.md (27 days old) - 2.5k tokens

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Total old markers: 8 (22.4k tokens)

Cleanup options:
1. Archive markers older than 30 days (recommended)
   → Moves to .agent/.context-markers/archive/
   → Safe, can restore if needed

2. Delete markers older than 30 days
   → Permanent deletion
   → Frees up space

3. Keep all, just show me
4. Cancel

Choice [1-4]:
```

**Wait for user input**.

**If option 1 selected** (Archive 30 days):
```bash
# Create archive directory if it doesn't exist
mkdir -p .agent/.context-markers/archive

# Archive markers older than 30 days
find .agent/.context-markers/ -maxdepth 1 -name "*.md" -mtime +30 -type f -exec mv {} .agent/.context-markers/archive/ \;
```

**Confirm archival**:
```
✅ Cleanup complete

Archived: 3 markers to .agent/.context-markers/archive/
Kept active: 5 markers (14.3k tokens)

To restore archived markers:
  mv .agent/.context-markers/archive/[filename] .agent/.context-markers/

To delete archived markers:
  rm -rf .agent/.context-markers/archive/
```

**If option 2 selected** (Delete 30 days):
```bash
# Delete markers older than 30 days
find .agent/.context-markers/ -maxdepth 1 -name "*.md" -mtime +30 -type f -delete
```

**Confirm deletion**:
```
✅ Cleanup complete

Deleted: 3 markers (8.2k tokens freed)
Kept: 5 recent markers (14.3k tokens)

Permanent deletion - cannot be restored.
```

**If option 3 or 4**: Exit without changes

---

## Implementation Notes

### Performance Optimizations

1. **Fast scanning**: Use `ls -lt` for sorted list (no full file reads)
2. **Lazy loading**: Only read full marker content when selected
3. **Token estimation**: Size in bytes / 4 ≈ tokens (no need for exact count)
4. **Preview extraction**: Read first 50 lines only for preview

### Metadata Extraction

**From filename** (primary source):
```
Format: [name]-YYYY-MM-DD-HHMMSS.md
Example: lunch-break-2025-10-12-120000.md

Extract:
- name: "lunch-break"
- date: "2025-10-12"
- time: "12:00:00"
```

**From content** (optional, for preview):
```markdown
Read first 50 lines, look for:
- "Task: TASK-XXX" → Extract task ID
- First paragraph → Preview text
```

### Edge Cases

**No markers directory**:
- Show setup instructions
- Suggest `/jitd:init` or manual mkdir

**Empty directory**:
- Show "no markers yet"
- Explain how to create markers

**Invalid filename format**:
- Skip files that don't match `*-YYYY-MM-DD-HHMMSS.md`
- Warn about unexpected files in directory

**User interrupts selection**:
- Accept 'q', 'quit', 'exit'
- Exit gracefully without error

---

## Examples

### Example 1: Interactive Load

```bash
User: /jitd:markers

System:
📍 Available Context Markers

1. lunch-break (2 hours ago)
   Task: TASK-456
   Size: 3.2k tokens

2. eod-yesterday (1 day ago)
   Task: TASK-455
   Size: 2.8k tokens

Which marker would you like to load? [1-2, or 'q']:

User: 1

System:
✅ Loaded marker: lunch-break

[Marker content displayed via Read tool]

Context restored! Continue where you left off.
```

### Example 2: Quick List

```bash
User: /jitd:markers list

System:
📍 Available Context Markers

1. lunch-break-2025-10-12-120000.md
   Created: 2 hours ago
   Size: 3.2k tokens

2. eod-2025-10-11-170000.md
   Created: yesterday
   Size: 2.8k tokens

Total: 2 markers (6.0k tokens)
```

### Example 3: Cleanup

```bash
User: /jitd:markers clean

System:
🧹 Found 5 markers older than 7 days (15.2k tokens)

Cleanup options:
1. Delete markers older than 30 days (recommended)
2. Delete markers older than 7 days
3. Keep all
4. Cancel

Choice [1-4]:

User: 1

System:
✅ Cleanup complete

Deleted: 2 markers (5.4k tokens freed)
Kept: 3 markers (9.8k tokens)
```

---

## User Experience Guidelines

### When to run `/jitd:markers`

**Daily workflow**:
- Morning: `/jitd:markers` → Load yesterday's eod marker
- After break: `/jitd:markers` → Load pre-break marker
- Context switch: `/jitd:markers` → Load previous task marker

**Periodic maintenance**:
- Weekly: `/jitd:markers clean` → Remove old markers
- Monthly: `/jitd:markers list` → Review what's saved

### Best Practices

**DO**:
- Use interactive mode for quick restoration
- Clean markers monthly (avoid clutter)
- Review list periodically

**DON'T**:
- Keep markers forever (they're session-specific)
- Load markers from different projects (context mismatch)
- Delete recent markers (< 7 days)

---

## Integration with `/jitd:marker`

**Clear separation**:
- `/jitd:marker` → CREATE markers (during work)
- `/jitd:markers` → MANAGE markers (load, list, clean)

**Typical workflow**:
```bash
# During work
/jitd:marker lunch-break

# After break
/jitd:markers
# [Select lunch-break from list]
# [Context restored]

# Continue working...

# End of day
/jitd:marker eod-2025-10-12

# Next morning
/jitd:markers
# [Select eod marker]
# [Yesterday's context restored]
```

---

## Success Criteria

**This command succeeds when**:
- [ ] Lists all markers with accurate metadata
- [ ] Interactive mode loads selected marker
- [ ] List mode shows all details
- [ ] Clean mode removes old markers safely
- [ ] Performance: <1 second for 50+ markers
- [ ] User knows which marker to load

---

**Remember**: Markers are your conversation save points. Create with `/jitd:marker`, manage with `/jitd:markers`. 🎯
