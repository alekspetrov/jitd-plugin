---
name: nav-marker
description: Create context save points to preserve conversation state before breaks, risky changes, or compaction. Use when user says "save my progress", "create checkpoint", "mark this point", or before clearing context.
allowed-tools: Read, Write, Bash
version: 1.0.0
---

# Navigator Marker Skill

Create context markers - save points that preserve conversation state so you can resume work later without re-explaining everything.

## When to Invoke

Invoke this skill when the user:
- Says "save my progress", "create checkpoint", "mark this"
- Says "before I take a break", "save before lunch"
- Mentions "risky refactor ahead", "experiment with new approach"
- Says "end of day", "stopping for today"
- Before compacting context

**DO NOT invoke** if:
- User is asking about existing markers (use listing, not creation)
- Context is fresh (< 5 messages exchanged)

## Execution Steps

### Step 1: Check Navigator Structure

Verify `.agent/.context-markers/` directory exists:

```bash
mkdir -p .agent/.context-markers
```

### Step 2: Determine Marker Name

**If user provided name**:
- Use their name (sanitize: lowercase, hyphens for spaces)
- Example: "Before Big Refactor" → "before-big-refactor"

**If no name provided**:
- Auto-generate with timestamp: `marker-{YYYY-MM-DD}-{HHmm}`
- Example: `marker-2025-10-16-1430`

**Ask user for optional note**:
```
Creating marker: [name]

Add a note? (optional - helps remember context later)
Example: "OAuth working, need to add tests"

Note:
```

### Step 3: Generate Marker Content

Create marker document with this structure:

```markdown
# Context Marker: [name]

**Created**: [YYYY-MM-DD HH:MM]
**Note**: [user's note or "No note provided"]

---

## Conversation Summary

[Summarize last 10-15 messages:
- What user was working on
- Key decisions made
- Problems solved
- Current progress state
]

## Documentation Loaded

[List docs that were Read during session:
- Navigator: ✅ .agent/DEVELOPMENT-README.md
- Task: TASK-XX-feature.md
- System: project-architecture.md
- SOPs: [if any]
]

## Files Modified

[List files with Write/Edit calls:
- src/auth/login.ts (implemented OAuth)
- src/routes/auth.ts (added endpoints)
- tests/auth.test.ts (created tests)
]

## Current Focus

[What user is working on right now:
- Feature: Authentication with OAuth
- Phase: Integration complete, testing pending
- Blockers: [if any]
]

## Technical Decisions

[Key architectural choices:
- Using passport.js over next-auth (better control)
- JWT tokens in httpOnly cookies (XSS protection)
- Redis for session storage (scalability)
]

## Next Steps

[What to do after restore:
1. Finish writing tests for OAuth flow
2. Add error handling for failed logins
3. Document setup in README
]

## Restore Instructions

To restore this marker:
\```bash
Read .agent/.context-markers/[filename]
\```

Or use: `/nav:markers` and select this marker
```

### Step 4: Save Marker File

Write marker to file:

```
Write(
  file_path: ".agent/.context-markers/[timestamp]_[name].md",
  content: [generated marker content]
)
```

Filename format: `{YYYY-MM-DD-HHmm}_{name}.md`
Example: `2025-10-16-1430_before-big-refactor.md`

### Step 5: Confirm Creation

Show success message:

```
✅ Context marker created!

Marker: [name]
File: .agent/.context-markers/[filename]
Size: [X] KB (~[Y] tokens)

This marker captures:
- Last [N] messages of conversation
- Files you were working on
- Technical decisions made
- Next steps to continue

To restore later:
- Start new session
- Say "load marker [name]"
- Or use /nav:markers to list all markers
```

## Scripts

**create_marker.py**: Generates marker content from conversation analysis
- Input: Conversation history (from Claude)
- Output: Formatted markdown marker

## Common Use Cases

### Before Lunch Break
```
User: "Save my progress, taking lunch"
→ Creates marker: "lunch-break-2025-10-16"
→ Captures current state
→ User resumes after lunch: "Load my lunch marker"
```

### Before Risky Refactor
```
User: "Mark this before I refactor routing"
→ Creates marker: "before-routing-refactor"
→ If refactor fails, restore marker
→ If refactor succeeds, delete marker
```

### End of Day
```
User: "End of day checkpoint"
→ Creates marker: "eod-2025-10-16"
→ Note: "OAuth done, tests tomorrow"
→ Next morning: "Load yesterday's marker"
```

### Before Context Compact
```
Automatic (via nav-compact skill):
→ Creates marker: "before-compact-2025-10-16-1500"
→ Compact clears conversation
→ Marker preserves knowledge
→ Next session: Auto-offers to restore
```

## Marker Best Practices

**Good marker names**:
- `lunch-break` (clear when/why)
- `before-api-refactor` (indicates purpose)
- `feature-complete` (marks milestone)
- `eod-friday` (specific timing)

**Bad marker names**:
- `temp` (not descriptive)
- `marker1` (meaningless)
- `test` (confusing)

**When to create markers**:
- ✅ Before breaks (lunch, EOD)
- ✅ Before risky changes
- ✅ Before context compact
- ✅ At milestones (feature complete)
- ❌ After every single message (noise)
- ❌ When context is fresh (< 5 messages)

## Error Handling

**Marker directory missing**:
```
Creating .agent/.context-markers/ directory...
✅ Ready to save markers
```

**Duplicate marker name**:
```
⚠️  Marker "[name]" already exists

Options:
1. Overwrite (replace existing)
2. Append timestamp (create "[name]-v2")
3. Choose different name

Your choice [1-3]:
```

**Insufficient context**:
```
⚠️  Very little context to save (< 5 messages)

Markers work best when there's significant progress to preserve.
Continue anyway? [y/N]:
```

## Success Criteria

Marker creation is successful when:
- [ ] Marker file created in `.agent/.context-markers/`
- [ ] Filename is unique and descriptive
- [ ] Content includes: summary, loaded docs, files modified, next steps
- [ ] User knows how to restore marker later
- [ ] Marker is 2-5k tokens (comprehensive but efficient)

## Notes

- Markers are **git-ignored** (personal session save points)
- Team members don't see each other's markers
- Markers can be deleted anytime with `/nav:markers clean`
- Typical marker size: 2-5k tokens (97.7% compression from 130k conversation)

This skill provides same functionality as `/nav:marker` command but with natural language invocation.
