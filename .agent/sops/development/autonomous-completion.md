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
