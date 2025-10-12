---
description: Smart context compact - preserve essential JITD markers and documentation context
---

# JITD Smart Compact

You are performing a context-optimized compact operation that preserves essential JITD documentation markers.

## What This Does

**Regular `/compact`**: Clears all conversation history, loses context

**JITD `/jitd:compact`**:
- Generates a **context marker** (snapshot of where you are)
- Saves marker to `.agent/.context-markers/`
- Shows you exactly how to resume
- Clears conversation history
- You restore context in your next session by reading the marker

**The Magic**: Context markers compress your entire session (50+ messages, 130k tokens) into a focused summary (3k tokens) that captures only what matters: current task, decisions made, next steps.

## How Context Markers Work

Think of it like save points in a video game:

```
Before Compact:
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
You: "Help me implement auth"
Claude: [50 messages of implementation]
You: "Now add OAuth"
Claude: [20 messages of OAuth work]
Total: 130k tokens, approaching limit

After /jitd:compact:
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
✅ Marker saved: .agent/.context-markers/2025-10-12.md

Contains:
- Task: TASK-45 (auth + OAuth)
- Status: OAuth integrated, needs testing
- Decisions: Using passport.js, JWT tokens
- Next: Write tests for OAuth flow
- 3k tokens

Next session:
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
You: Read @.agent/.context-markers/2025-10-12.md
Claude: *knows exactly where you left off*
You: "Write the OAuth tests"
Claude: *continues seamlessly*
```

**You never lose progress. The knowledge is preserved, just compressed.**

## When to Use

### ✅ Good Times to Compact

**After isolated sub-tasks**:
- Just finished documentation update
- Created SOP for solved issue
- Archived feature implementation plan
- Completed debugging session

**Before context switches**:
- Switching from feature A to feature B
- Moving from debugging to new feature
- Starting new sprint/milestone
- After research phase, before implementation

**Token optimization**:
- Approaching 70% token usage
- Long conversation with repeated info
- After multiple /jitd:update-doc operations

### ❌ Bad Times to Compact

**In middle of work**:
- Feature half-implemented
- Debugging complex issue
- Multiple related sub-tasks pending

**Context still needed**:
- Next sub-task depends on current conversation
- Need to reference recent decisions
- Team discussion ongoing

## Compact Process

### Step 1: Identify Essential Context

Scan conversation for:

**Must preserve**:
- Current task ID (TASK-XX)
- Active feature/epic name
- Key technical decisions made
- Unresolved blockers/questions
- Next steps planned

**Can clear**:
- Completed sub-tasks details
- Resolved debugging sessions
- Documentation already written
- Exploratory research (if documented)

### Step 2: Generate Context Marker

Create compact marker to preserve essentials:

```markdown
# JITD Context Marker (Post-Compact)

**Session**: [Date/Time]
**Navigator**: .agent/DEVELOPMENT-README.md

## Active Work
- **Task**: TASK-XX - [Feature Name]
- **Status**: [Phase/Progress]
- **Location**: [File/component being worked on]

## Recent Decisions
- [Decision 1]
- [Decision 2]

## Documentation State
- **Task docs**: [List updated docs]
- **System docs**: [List updated docs]
- **SOPs**: [List created SOPs]

## Next Steps
1. [Next action]
2. [Following action]

## Blockers
- [Blocker 1 if any]

## Don't Load Again (Already Documented)
- [Doc 1] - Already in .agent/
- [Doc 2] - Already in .agent/

---
Load this context marker after compacting to resume efficiently.
```

### Step 3: Save Context Marker

**IMPORTANT**: You MUST save the marker where the user can access it after compact.

**Recommended**: Save to `.agent/.context-markers/` directory

```bash
# Create directory if doesn't exist
mkdir -p .agent/.context-markers

# Save with timestamp
Write(
  file_path: ".agent/.context-markers/2025-10-12-143022-compact.md"
  content: [context marker from Step 2]
)
```

**Show user the saved location**:
```
✅ Context marker saved to:
   .agent/.context-markers/2025-10-12-143022-compact.md

After compact, start your new session with:
   Read @.agent/.context-markers/2025-10-12-143022-compact.md

This will restore your context in ~3k tokens.
```

**Alternative locations**:

**Option 2**: Append to current task doc (if task exists)
```
Append to: .agent/tasks/TASK-XX-feature.md

## Session Notes
### Compact Point - [Date]
[Context marker content]

After compact: Read @.agent/tasks/TASK-XX-feature.md
```

**Option 3**: User clipboard (if no task doc yet)
```
⚠️  No task doc exists yet.

Copy this marker and paste it in your next session:

[Show marker content]

Or save it manually before compacting.
```

### Step 4: Show Resume Instructions

**CRITICAL**: Tell the user exactly how to resume.

```
╔══════════════════════════════════════════════════════╗
║                                                      ║
║  🔄 Ready to Compact                                 ║
║                                                      ║
╚══════════════════════════════════════════════════════╝

Context marker saved to:
→ .agent/.context-markers/2025-10-12-143022-compact.md

TO RESUME AFTER COMPACT:
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

In your next conversation, start with:

1. Read @.agent/.context-markers/2025-10-12-143022-compact.md

That's it! Your context will be restored.

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Proceed with compact? Type 'yes' to continue.
```

**Wait for confirmation before compacting**.

### Step 5: Perform Compact

**Only after user confirms**, execute Claude Code's `/compact` command.

### Step 6: Post-Compact Resume (For User's Next Session)

**Immediately after compact**:

1. **Load navigator** (always):
   ```
   Read .agent/DEVELOPMENT-README.md (~2k tokens)
   ```

2. **Load context marker**:
   ```
   Read context marker from Step 2
   ```

3. **Load active task doc** (if exists):
   ```
   Read .agent/tasks/TASK-XX-feature.md (~3k tokens)
   ```

4. **Resume work**: Continue where left off

**Total tokens loaded**: ~7k (vs 60k+ if keeping full conversation)

## Compact Strategies

### Aggressive (Compact Often)

**When**: Token-constrained, switching tasks frequently

**Trigger**:
- After every sub-task
- Before every new task
- Every 50% token usage

**Trade-off**: More compacts, less context continuity

**Best for**: Multiple short tasks, exploratory work

### Conservative (Compact Rarely)

**When**: Deep work on single feature, need context continuity

**Trigger**:
- After major milestones only
- When reaching 70%+ tokens
- Between unrelated epics

**Trade-off**: Fewer compacts, more token usage

**Best for**: Complex features, long debugging sessions

### Manual (User Decides)

**When**: User knows when to compact

**Trigger**: User runs `/jitd:compact` explicitly

**Trade-off**: Full control, requires judgment

**Best for**: Experienced users, custom workflows

## Configuration

Set in `.agent/.jitd-config.json`:

```json
{
  "compact_strategy": "conservative",
  "compact_trigger_percent": 70,
  "save_context_markers": true,
  "context_marker_location": ".agent/.context-markers/"
}
```

## Example Compact Scenarios

### Scenario 1: Feature Complete

```
Before Compact:
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Tokens: 65% (130k used)
Conversation: 50+ messages
Feature TASK-123 complete
Docs updated
Tests passing

Action: /jitd:compact
Reason: Feature done, docs archived, ready for next task

After Compact:
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Tokens: 5% (10k used)
- Navigator loaded (2k)
- Context marker (3k)
- Ready for TASK-124

Savings: 120k tokens freed (60% of budget)
```

### Scenario 2: Research → Implementation

```
Before Compact:
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Tokens: 45% (90k used)
Research: Explored 5 different approaches
Decision: Chose approach #3
Key findings: Documented in SOP

Action: /jitd:compact
Reason: Research done, documented, time to implement

After Compact:
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Tokens: 7% (14k used)
- Navigator (2k)
- Task doc with decision (3k)
- Relevant SOP (2k)
- Implementation ready

Savings: 76k tokens freed
```

### Scenario 3: Multi-Task Day

```
Morning:
- TASK-101: Bug fix (15k tokens)
- /jitd:compact
- TASK-102: New feature (25k tokens)
- /jitd:compact

Afternoon:
- TASK-103: Integration (20k tokens)
- /jitd:compact
- TASK-104: Documentation (10k tokens)

Total work: 4 tasks
Peak usage: 25k tokens (12.5%)
Without compact: Would hit 70k+ (35%), slower responses

Benefit: Maintained fast responses all day
```

## Compact Checklist

Before running `/jitd:compact`:

- [ ] Current task completed or at good stopping point
- [ ] Important decisions documented (task doc or SOP)
- [ ] No unresolved blockers requiring conversation context
- [ ] Ready to switch tasks or take break
- [ ] Context marker generated (if needed)

After running `/jitd:compact`:

- [ ] Load navigator (.agent/DEVELOPMENT-README.md)
- [ ] Load context marker (if saved)
- [ ] Load active task doc (if continuing work)
- [ ] Verify ready to continue

## Advanced: Auto-Compact

**Future enhancement**: Automatically compact based on triggers

```json
{
  "auto_compact": {
    "enabled": false,
    "triggers": {
      "token_percent": 70,
      "after_update_doc": true,
      "between_tasks": true
    },
    "require_confirmation": true
  }
}
```

When trigger hit:
```
⚠️  JITD Auto-Compact Suggested

Reason: Token usage at 71%
Action: Run /jitd:compact to free 60k+ tokens

Compact now? [Y/n]:
```

## Metrics

Track compact efficiency:

**Before Compact**:
- Tokens used: 130k (65%)
- Message count: 50+
- Time: 2 hours

**After Compact**:
- Tokens used: 10k (5%)
- Context preserved: Task doc + decision markers
- Ready for: Next task immediately

**Savings**:
- 120k tokens freed
- 60% of budget reclaimed
- Fast responses restored

---

**Remember**: JITD compact preserves what matters (documented knowledge) and clears what doesn't (conversation history). This keeps your context lean and your sessions productive.
