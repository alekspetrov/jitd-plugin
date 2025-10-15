# TASK-05: Autonomous Task Completion

**Status**: In Progress
**Priority**: High
**Version**: 1.5.1 (Patch)
**Created**: 2025-10-13

---

## Problem Statement

Claude completes feature implementation but waits for explicit human prompts to:
- Commit changes
- Close tickets in PM tools
- Update documentation
- Create completion markers

This creates friction and breaks the autonomous workflow JITD is designed to enable.

**User feedback**: "Most of the time they don't... finish the job, don't close the ticket, or more often don't commit changes on finish, maybe expecting human input."

---

## Root Cause

**Conflict between safety protocols and autonomy**:
1. Claude Code's commit protocol: "NEVER commit changes unless the user explicitly asks"
2. No explicit "task complete" signal in JITD workflow
3. Documentation doesn't override default conservative behavior
4. Claude assumes coordination over autonomy

---

## Solution Design

### Core Principle
**JITD projects expect full autonomy** - When task is complete, execute the entire finish protocol automatically without waiting for human prompts.

### Autonomous Completion Protocol

**When task implementation is complete, automatically**:
1. ✅ Commit changes with proper conventional commit message
2. ✅ Run `/jitd:update-doc feature TASK-XX` to archive implementation plan
3. ✅ Close ticket in PM tool (if configured)
4. ✅ Create completion marker `TASK-XX-complete`
5. ✅ Suggest `/jitd:compact` to clear context

**Only ask for human confirmation if**:
- Uncommitted changes contain secrets (.env, credentials, API keys)
- Multiple unrelated tasks modified (unclear which to close)
- No task context loaded (ambiguous which task to complete)
- PM tool integration not configured and ticket closure requested

---

## Implementation Plan

### 1. Create Implementation Plan (This File)
**File**: `.agent/tasks/TASK-05-autonomous-completion.md`
**Purpose**: Document the problem, solution, and implementation steps

### 2. Version Bump
**File**: `marketplace.json`
**Change**: `"version": "1.5.0"` → `"version": "1.5.1"`
**Rationale**: Patch version - enhances existing behavior without breaking changes

### 3. Update Project CLAUDE.md
**File**: `CLAUDE.md`
**Section to modify**: "Development Workflow" + "Forbidden Actions"

**Add new section**:
```markdown
## Autonomous Task Completion (JITD Override)

### Standard Projects vs JITD Projects

**Standard Projects**: Conservative approach
- Ask before committing
- Wait for explicit "close ticket" request
- Wait for "update documentation" prompt

**JITD Projects**: Autonomous completion (when task is done)
- ✅ Commit automatically with proper message
- ✅ Archive implementation plan automatically
- ✅ Close ticket automatically (if PM configured)
- ✅ Create completion marker automatically
- ✅ Inform user of actions taken

### Completion Trigger

When you finish implementing a task/feature:
1. Verify work is complete (tests pass, functionality works)
2. Execute autonomous completion protocol
3. Show user summary of automated actions

### Exception Cases (Ask First)

Only interrupt autonomous flow if:
- Uncommitted files look suspicious (.env, secrets, credentials)
- Multiple unrelated tasks modified (unclear scope)
- No task context available (can't determine TASK-XX)
- Critical changes that need explicit approval

### Autonomous Protocol Steps

**Step 1: Commit Changes**
```bash
git status  # Check what's changed
git add .   # Stage relevant files
git commit -m "feat(feature): implement X (TASK-XX)

🤖 Generated with [Claude Code](https://claude.com/claude-code)

Co-Authored-By: Claude <noreply@anthropic.com>"
```

**Step 2: Archive Implementation Plan**
```bash
/jitd:update-doc feature TASK-XX
```

**Step 3: Close Ticket (if PM configured)**
```typescript
// Linear example
update_issue({ id: "TASK-XX", state: "Done" })

// GitHub Issues example
gh issue close TASK-XX
```

**Step 4: Create Completion Marker**
```bash
/jitd:marker TASK-XX-complete
```

**Step 5: Suggest Compact**
```
Inform user: "Run /jitd:compact to clear context and start next task."
```

**Step 6: Show Summary**
```
✅ TASK-XX Complete

Automated actions:
- Committed changes (abc123)
- Archived implementation plan
- Closed ticket in Linear
- Created marker: TASK-XX-complete

Ready for next task. Run /jitd:compact to clear context.
```
```

**Update "Forbidden Actions" section**:
```markdown
### JITD Violations (HIGHEST PRIORITY)
- ❌ NEVER wait for explicit commit prompts after task completion (autonomous mode)
- ❌ NEVER leave tickets open after implementation complete (close automatically)
- ❌ NEVER skip documentation after completing features (knowledge loss)
- ❌ NEVER load all `.agent/` docs at once (defeats context optimization)
```

### 4. Update DEVELOPMENT-README.md
**File**: `.agent/DEVELOPMENT-README.md`
**Section to add**: "Task Completion Protocol"

**Add after "Current Tasks" section**:
```markdown
## Task Completion Protocol

### Autonomous Completion (CRITICAL)

JITD projects expect **full autonomy** when tasks complete. No human prompts needed.

**When task implementation is done**:

✅ **Automatically execute** (no confirmation needed):
1. Commit changes with conventional commit message
2. Archive implementation plan (`/jitd:update-doc feature TASK-XX`)
3. Close ticket in PM tool (if configured)
4. Create completion marker (`TASK-XX-complete`)
5. Suggest `/jitd:compact`

❌ **Don't wait for**:
- "Please commit now"
- "Close the ticket"
- "Update documentation"
- "Create a marker"

**Exception**: Only ask if ambiguous state or security concerns (.env files, secrets)

### Completion Checklist

Before executing autonomous completion, verify:
- [ ] Tests passing (if applicable)
- [ ] Feature works as intended
- [ ] No secrets in uncommitted files
- [ ] Task context is clear (know which TASK-XX)

### Completion Summary Template

After autonomous completion, show:
```
✅ TASK-XX Complete

Automated actions:
- Committed: [commit hash] [commit message]
- Documentation: Implementation plan archived
- Ticket: Closed in [PM tool]
- Marker: TASK-XX-complete created

Next: Run /jitd:compact to clear context
```
```

**Update "Development Workflow" section**:
```markdown
## Development Workflow

1. **Start Session** → `/jitd:start` (loads navigator, checks PM tool)
2. **Select Task** → Load task doc (`.agent/tasks/TASK-XX.md`)
3. **Implement** → Follow patterns, write tests, verify functionality
4. **Complete** → [AUTONOMOUS] Commit, document, close ticket, create marker
5. **Compact** → Run `/jitd:compact` to clear context for next task
```

### 5. Create Autonomous Completion SOP
**File**: `.agent/sops/development/autonomous-completion.md`

**Purpose**: Detailed SOP for executing autonomous task completion

**Content**:
```markdown
# Autonomous Task Completion

**SOP ID**: DEV-003
**Category**: Development
**Last Updated**: 2025-10-13
**Version**: 1.0.0

---

## When to Use This SOP

Execute this protocol automatically when:
- Task implementation is complete
- Tests are passing (if applicable)
- Feature functionality verified
- Working in a JITD-enabled project

**Do NOT wait for explicit human prompt** - Autonomy is expected.

---

## Prerequisites

Before executing autonomous completion:

### Required
- [ ] Task context known (TASK-XX identified)
- [ ] Implementation complete and verified
- [ ] No secrets in uncommitted files

### Optional
- [ ] PM tool configured (Linear/GitHub/Jira/etc)
- [ ] Tests passing
- [ ] Documentation updated

---

## Execution Steps

### Step 1: Verify Completion

**Check implementation**:
```bash
# Run tests if available
npm test || pytest || cargo test

# Verify functionality manually if needed
# Check that requirements are met
```

**Verify safety**:
```bash
git status
# Look for suspicious files:
# - .env, .env.local
# - credentials.json, secrets.yaml
# - *_key.pem, *.p12
# - Any file with "secret", "password", "token" in name
```

**If suspicious files found**: Ask user before committing

---

### Step 2: Commit Changes

**Stage and commit**:
```bash
git add .

git commit -m "$(cat <<'EOF'
feat(scope): implement feature description (TASK-XX)

[Brief description of what was implemented and why]

🤖 Generated with [Claude Code](https://claude.com/claude-code)

Co-Authored-By: Claude <noreply@anthropic.com>
EOF
)"
```

**Commit message format**:
- Type: `feat`, `fix`, `refactor`, `docs`, `test`, `chore`
- Scope: Feature area or component name
- Description: Clear, concise, present tense
- Reference: `(TASK-XX)` at end of subject

**Push to remote**:
```bash
git push origin HEAD
```

---

### Step 3: Archive Implementation Plan

**Run update-doc command**:
```bash
/jitd:update-doc feature TASK-XX
```

**What this does**:
1. Moves `.agent/tasks/TASK-XX-*.md` → `.agent/tasks/archive/`
2. Updates `.agent/DEVELOPMENT-README.md` to mark task complete
3. Preserves task history for future reference

---

### Step 4: Close Ticket in PM Tool

**If Linear configured**:
```typescript
// Get issue to verify it exists
const issue = await get_issue({ id: "TASK-XX" })

// Update to Done state
await update_issue({
  id: "TASK-XX",
  state: "Done"
})

// Optional: Add completion comment
await create_comment({
  issueId: "TASK-XX",
  body: "Implementation complete. [Commit hash]"
})
```

**If GitHub Issues**:
```bash
gh issue close TASK-XX --comment "Implementation complete. See commit [hash]"
```

**If Jira configured**:
```bash
# Via Jira API or CLI
jira issue move TASK-XX "Done"
```

**If no PM tool**: Skip this step (no error)

---

### Step 5: Create Completion Marker

**Create marker automatically**:
```bash
/jitd:marker TASK-XX-complete
```

**Marker contents should include**:
- Task ID and description
- What was implemented
- Commits made
- Files modified
- Next steps (if any)

---

### Step 6: Suggest Compact

**Inform user**:
```
Ready for next task. Run /jitd:compact to clear context.
```

**Don't auto-compact** - Let user decide when to clear context

---

### Step 7: Show Completion Summary

**Display summary**:
```
✅ TASK-XX Complete

Automated actions:
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
✅ Committed: abc1234 "feat(auth): implement user login"
✅ Documentation: Implementation plan archived
✅ Ticket: Closed in Linear
✅ Marker: TASK-XX-complete created
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Next: Run /jitd:compact to clear context and start next task
```

---

## Exception Handling

### Exception 1: Secrets Detected

**If .env or credentials found**:
```
⚠️  Detected potential secrets in uncommitted files:
- .env
- credentials.json

Should I:
1. Commit without these files (add to .gitignore)
2. Include these files (not recommended)
3. Cancel commit (you review manually)

Choice [1-3]:
```

**Recommended**: Option 1 (exclude secrets)

---

### Exception 2: Multiple Tasks Modified

**If changes span multiple task contexts**:
```
⚠️  Changes affect multiple areas:
- Task A files: src/auth/*
- Task B files: src/payments/*

Which task should I complete?
1. TASK-A (auth)
2. TASK-B (payments)
3. Both (create 2 commits)
4. Cancel (you decide)

Choice [1-4]:
```

---

### Exception 3: No Task Context

**If TASK-XX unknown**:
```
⚠️  No task context loaded

I can't determine which task to complete.

Options:
1. Load task manually: Read .agent/tasks/TASK-XX.md
2. Complete without task reference (generic commit)
3. Cancel completion

Choice [1-3]:
```

---

### Exception 4: PM Tool Not Configured

**If trying to close ticket but no PM tool**:
- Skip ticket closure step silently
- Don't error or interrupt flow
- Continue with other steps

---

### Exception 5: Tests Failing

**If tests fail during verification**:
```
⚠️  Tests are failing

Should I:
1. Fix tests first (recommended)
2. Commit anyway (not recommended)
3. Cancel completion

Choice [1-3]:
```

**Recommended**: Option 1 (fix tests)

---

## Success Criteria

Autonomous completion succeeds when:
- [ ] Changes committed with proper message
- [ ] Implementation plan archived
- [ ] Ticket closed (if PM configured)
- [ ] Completion marker created
- [ ] User informed of actions taken
- [ ] No manual prompts required (fully autonomous)

---

## Related Documentation

- **Task Completion Protocol**: `.agent/DEVELOPMENT-README.md`
- **Commit Guidelines**: `CLAUDE.md` → "Committing Changes"
- **Update Doc Command**: `.claude/commands/jitd-update-doc.md`
- **Markers Command**: `.claude/commands/jitd-marker.md`

---

## Version History

| Version | Date | Changes |
|---------|------|---------|
| 1.0.0 | 2025-10-13 | Initial SOP for autonomous completion |

---

**Remember**: Autonomy is expected in JITD projects. Execute the full protocol without waiting for human prompts. Only interrupt for security concerns or ambiguous state.
```

### 6. Update README.md Version References
**File**: `README.md`
**Changes**: Update all version references from `1.5.0` → `1.5.1`

**Locations** (from version-management.md SOP):
1. Line 5: Status badge
2. Line 8: Version badge
3. Line 435: Roadmap section
4. Line 506: Footer

### 7. Update .agent/DEVELOPMENT-README.md Index
**File**: `.agent/DEVELOPMENT-README.md`
**Change**: Add TASK-05 to task index

---

## Testing Plan

### Manual Testing
1. Use plugin in test project
2. Implement a feature without mentioning "commit" or "close ticket"
3. Verify Claude autonomously:
   - Commits changes
   - Archives implementation plan
   - Closes ticket (if PM configured)
   - Creates completion marker
   - Shows summary

### Expected Behavior
```
USER: "Implement user authentication"
CLAUDE: [implements feature]
CLAUDE: "Implementation complete. Executing finish protocol..."
CLAUDE: [commits, documents, closes ticket, creates marker]
CLAUDE: "✅ TASK-XX Complete. Ready for next task."
```

### User Feedback
- Deploy v1.5.1 to production
- Test on real project (this conversation)
- Verify no manual prompts needed
- Confirm workflow feels autonomous

---

## Success Metrics

- [ ] No "please commit now" prompts needed
- [ ] No "close the ticket" prompts needed
- [ ] Tasks complete end-to-end autonomously
- [ ] User only needs to say "implement X" and "start next task"
- [ ] Completion time reduced by ~30 seconds per task
- [ ] User satisfaction: "Feels truly autonomous"

---

## Rollout Plan

1. **v1.5.1 Release**: Autonomous completion behavior
2. **User Testing**: Deploy and test immediately (this project)
3. **Documentation Update**: Ensure clarity in navigator
4. **Feedback Loop**: Adjust based on real-world usage
5. **Future Enhancement**: Add config flag `"autonomous_completion": true/false`

---

## Future Considerations

### Phase 1 (v1.5.1)
- ✅ Documentation updates (CLAUDE.md, DEVELOPMENT-README.md)
- ✅ Autonomous completion SOP
- ✅ Rely on Claude's training to follow instructions

### Phase 2 (v1.6.0+)
- [ ] Add `.jitd-config.json` flag: `"autonomous_completion": true`
- [ ] Create `/jitd:config` command to toggle settings
- [ ] Add telemetry to track autonomous completion success rate
- [ ] Smart detection: "This looks complete, should I finish?"

---

## Notes

**Why patch version (1.5.1)?**
- No breaking changes
- No new features (just behavior enhancement)
- Backward compatible (doesn't affect projects without JITD)
- Semantic versioning: PATCH for behavior fixes

**Why not a new command?**
- Commands add complexity
- The workflow already exists (just needs autonomy)
- Training via documentation is more elegant
- Reduces user cognitive load

**Key insight from user**:
> "Why can't it be fully autonomous as on the schema you showed?"

This is the answer: **It can be, and it should be.** Just update the rules.

---

**Status**: Ready for implementation
**Next Step**: Execute implementation plan (update files, bump version, test, release)
