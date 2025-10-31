# Multi-Claude POC Learnings

**Date**: 2025-10-31
**Test**: Proof of concept for automated multi-Claude orchestration

---

## What Was Tested

Created `navigator-multi-claude-poc.sh` to test basic 2-phase workflow:
1. Orchestrator: Create plan + marker
2. Implementation: Load marker + implement

**Approach**:
- Bash orchestration with headless Claude (`-p` flag)
- JSON output parsing (`--output-format json`)
- Session management (`--resume session_id`)
- Marker-based coordination (wait for `.context-markers/*.md`)

---

## Results

### ✅ What Worked

1. **Bash Orchestration**
   - Script structure sound
   - Process management works
   - Background execution functional
   - Exit code handling correct

2. **Logging & Progress**
   - Colored output clear
   - Phase transitions visible
   - Timestamps helpful
   - Error reporting good

3. **Marker Waiting**
   - File system watching works
   - Timeout logic correct
   - Polling pattern efficient

### ❌ What Didn't Work

1. **JSON Output Parsing**
   - `claude -p ... --output-format json` command hangs or produces unparseable output
   - `jq` unable to extract `session_id` from output
   - May be Claude Code version issue or configuration problem

2. **Marker Creation**
   - Natural language "create marker X" doesn't auto-invoke nav-marker skill in headless mode
   - Claude completes successfully but no marker file created
   - May need explicit skill invocation syntax

3. **Session Timeout**
   - First Claude call took 3+ minutes (loading Navigator session)
   - Script timed out waiting for marker after 5 minutes
   - No visible progress during Claude processing

---

## Technical Blockers

### Blocker 1: Headless JSON Output
**Issue**: `--output-format json` doesn't produce parseable JSON
**Impact**: Can't extract session IDs for resume
**Potential causes**:
- Claude Code version incompatibility
- Missing configuration
- Stdout/stderr mixing
- Need different output format flag

**Investigation needed**:
```bash
# Test minimal JSON output
claude -p "Hello" --output-format json

# Test with stderr redirect
claude -p "Hello" --output-format json 2>/dev/null

# Test streaming JSON
claude -p "Hello" --output-format stream-json
```

### Blocker 2: Marker Creation in Headless
**Issue**: "Create marker X" natural language doesn't invoke skill
**Impact**: Can't coordinate between phases
**Potential causes**:
- Skills don't auto-invoke in headless mode
- Need explicit skill syntax
- Marker skill requires interactive context

**Investigation needed**:
- Test marker creation in interactive mode
- Check if skills available in headless
- Try explicit skill invocation
- Alternative: have Claude write marker files directly

### Blocker 3: No Progress Visibility
**Issue**: Can't see what Claude is doing during 3+ minute processing
**Impact**: Appears hung, no feedback
**Potential solutions**:
- Add `--verbose` flag to Claude calls
- Tail Claude's logs in real-time
- Show "thinking..." animation
- Estimate completion time

---

## Architecture Validation

**What we proved**:
✅ Bash can orchestrate multiple Claude instances
✅ Marker-based coordination is viable approach
✅ Session management concept correct
✅ Script structure scales to 5+ phases

**What we need to solve**:
❌ Reliable JSON output from headless Claude
❌ Programmatic marker creation
❌ Progress visibility during processing

---

## Next Steps

### Immediate (Before continuing implementation)

1. **Test JSON output in isolation**
   ```bash
   claude -p "Echo: test" --output-format json > test.json
   cat test.json | jq .
   ```

2. **Test marker creation interactively**
   ```bash
   claude
   > "Create marker test-poc"
   # Verify .context-markers/test-poc.md created
   ```

3. **Check Claude Code version**
   ```bash
   claude --version
   # Verify >= 1.0.90 for streaming JSON support
   ```

### Alternative Approaches (If blockers persist)

**Option A: Direct Marker File Creation**
- Have Claude write marker content to stdout
- Bash script creates .md file from output
- Bypass skill system entirely

**Option B: Interactive Mode with Automation**
- Use `expect` to drive interactive Claude
- Send prompts via stdin
- Parse output without JSON

**Option C: MCP Integration**
- Create MCP server for orchestration
- Claude calls MCP tools for coordination
- Cleaner than bash parsing

**Option D: Navigator Skill Enhancement**
- Add `nav-multi-claude-run` skill
- Skill handles orchestration internally
- Returns when all phases complete

---

## Files Created

- `scripts/navigator-multi-claude-poc.sh` - POC orchestrator (4.1KB)
- `scripts/POC-LEARNINGS.md` - This document

---

## Recommendations

**For TASK-19 Phase 1**:

1. **Solve blockers first** before building full system
2. **Test each automation primitive** in isolation
3. **Document workarounds** if official API doesn't work
4. **Consider alternative architectures** if headless mode too limited

**Don't proceed with**:
- Building 5-phase orchestrator until 2-phase works
- Creating role-specific templates until coordination proven
- CI/CD integration until local automation reliable

**Timeline impact**:
- Original: 2 weeks (assuming automation works)
- Revised: 3-4 weeks (1 week solving blockers, 2-3 weeks implementation)

---

## Context for Next Session

**Quick summary**: POC script created but hit technical blockers with headless Claude JSON output and marker creation. Need to investigate Claude Code CLI behavior before continuing implementation.

**Resume from**: Test JSON output in isolation, verify marker creation works interactively, check Claude Code version compatibility.

**Priority**: Solve Blocker 1 (JSON output) first - it's critical for session management.
