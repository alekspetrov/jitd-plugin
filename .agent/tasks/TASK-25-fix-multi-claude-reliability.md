# TASK-25: Fix Multi-Claude Workflow Reliability (30% → 90%)

**Created**: 2025-11-01
**Assignee**: Multi-Claude Workflow (dogfooding)
**Priority**: High
**Status**: Planning
**Target**: v4.5.0

---

## Problem Statement

**Current state**: Multi-Claude workflows succeed 30% of the time (3/10 test workflows)

**Main failure mode**: Marker timeout in Phase 3 (Testing)
```
[15:24:49] Waiting for file: .agent/tasks/poc-1762006598-tests-done
[15:26:51] ❌ Timeout waiting for file
[15:26:51] ❌ Testing phase timeout - no completion marker
```

**Root causes**:
1. Sub-Claude instances don't always invoke marker skill
2. No retry logic when marker creation fails
3. No self-monitoring in sub-Claude (doesn't detect own timeout)
4. Orchestrator can't distinguish "working" from "stuck"
5. No recovery mechanism to resume from last successful phase

**Impact**: Users can't rely on multi-Claude workflows for production use

---

## Success Criteria

**Target**: 90% success rate (9/10 workflows complete successfully)

**Metrics**:
- Marker creation reliability: 95%+ (was ~60%)
- Phase transition success: 95%+ (was ~70%)
- Automatic recovery from timeouts: 80%+
- User intervention needed: <10% (was ~70%)

**Test plan**:
- 10 simple POC workflows (1-2 file changes)
- 10 medium workflows (3-5 file changes)
- 5 complex workflows (6+ files, integration tests)
- All run without manual intervention

---

## Solution Design

### 1. Automatic Retry Logic

**Problem**: Marker skill invoked but creation fails silently

**Solution**: Orchestrator detects missing marker and retries phase

**Implementation** (`navigator-multi-claude.sh`):
```bash
wait_for_marker_with_retry() {
  local marker_file=$1
  local max_retries=${2:-1}  # Default: retry once
  local timeout=${3:-120}    # Default: 2 minutes

  for attempt in $(seq 1 $((max_retries + 1))); do
    echo "[$(date +%H:%M:%S)] Attempt $attempt: Waiting for $marker_file"

    if wait_for_file "$marker_file" "$timeout"; then
      echo "[$(date +%H:%M:%S)] ✅ Marker found: $marker_file"
      return 0
    fi

    if [ $attempt -le $max_retries ]; then
      echo "[$(date +%H:%M:%S)] ⚠️  Retry: Marker not found, restarting phase..."
      restart_current_phase
    else
      echo "[$(date +%H:%M:%S)] ❌ Failed after $attempt attempts"
      return 1
    fi
  done
}
```

**Files modified**:
- `scripts/navigator-multi-claude.sh` (retry wrapper)
- `scripts/navigator-multi-claude-poc.sh` (POC retry)

**Testing**:
- Simulate marker failure (delete marker mid-creation)
- Verify orchestrator retries
- Confirm success on retry

---

### 2. Timeout Detection in Sub-Claude

**Problem**: Sub-Claude doesn't know it's stuck, orchestrator times out externally

**Solution**: Sub-Claude monitors own progress, exits if stuck

**Implementation** (new file: `scripts/sub-claude-monitor.sh`):
```bash
#!/bin/bash
# Sub-Claude self-monitoring wrapper
# Runs alongside headless Claude, kills if stuck

PHASE=$1
TIMEOUT=${2:-180}  # 3 minutes default
PID=$3

start_time=$(date +%s)

while true; do
  sleep 10

  current_time=$(date +%s)
  elapsed=$((current_time - start_time))

  # Check if process still alive
  if ! kill -0 $PID 2>/dev/null; then
    echo "[Monitor] Process $PID completed"
    exit 0
  fi

  # Check if timeout exceeded
  if [ $elapsed -gt $TIMEOUT ]; then
    echo "[Monitor] ⚠️  Timeout exceeded ($elapsed > $TIMEOUT)"
    echo "[Monitor] Checking for progress markers..."

    # Check if marker exists (success despite timeout)
    if [ -f ".agent/tasks/$SESSION_ID-$PHASE-done" ]; then
      echo "[Monitor] ✅ Marker found, phase completed"
      exit 0
    fi

    # No marker, kill stuck process
    echo "[Monitor] ❌ No marker, killing stuck process"
    kill -9 $PID
    exit 1
  fi
done
```

**Usage in orchestrator**:
```bash
# Start Claude in background
claude -p "$PROMPT" --resume "$SESSION_ID" &
CLAUDE_PID=$!

# Start monitor
./scripts/sub-claude-monitor.sh "$PHASE" "$TIMEOUT" "$CLAUDE_PID" &
MONITOR_PID=$!

# Wait for Claude to finish
wait $CLAUDE_PID
CLAUDE_EXIT=$?

# Kill monitor
kill $MONITOR_PID 2>/dev/null

# Check exit code
if [ $CLAUDE_EXIT -ne 0 ]; then
  echo "❌ Sub-Claude exited with error: $CLAUDE_EXIT"
fi
```

**Files**:
- `scripts/sub-claude-monitor.sh` (new)
- `scripts/navigator-multi-claude.sh` (integrate monitor)

**Testing**:
- Simulate stuck Claude (infinite loop)
- Verify monitor kills after timeout
- Confirm orchestrator handles exit code

---

### 3. Phase Recovery Mechanism

**Problem**: Workflow fails completely if one phase times out

**Solution**: Save phase state, allow resume from last successful phase

**Implementation** (state file: `.agent/tasks/SESSION_ID-state.json`):
```json
{
  "session_id": "poc-1762006598",
  "task": "Add hello world function",
  "phases_completed": ["phase0", "phase1", "phase2"],
  "current_phase": "phase3",
  "phase_attempts": {
    "phase3": 2
  },
  "started_at": "2025-11-01T15:24:49Z",
  "last_update": "2025-11-01T15:26:51Z"
}
```

**Resume logic**:
```bash
resume_workflow() {
  local session_id=$1
  local state_file=".agent/tasks/$session_id-state.json"

  if [ ! -f "$state_file" ]; then
    echo "❌ No state file found: $state_file"
    return 1
  fi

  # Parse state
  local completed=$(jq -r '.phases_completed | join(",")' "$state_file")
  local current=$(jq -r '.current_phase' "$state_file")

  echo "📋 Resuming workflow: $session_id"
  echo "   Completed phases: $completed"
  echo "   Current phase: $current"
  echo ""
  echo "Resume from current phase? [Y/n]"

  read -r response
  if [[ "$response" =~ ^([yY][eE][sS]|[yY]|)$ ]]; then
    run_phase "$current"
  fi
}
```

**Files**:
- `scripts/navigator-multi-claude.sh` (state tracking)
- `scripts/resume-workflow.sh` (new, standalone resume tool)

**Testing**:
- Start workflow, kill during Phase 3
- Run resume script
- Verify Phase 3 restarts from checkpoint

---

### 4. Marker Verification & Logging

**Problem**: Marker creation fails silently, no visibility into why

**Solution**: Enhanced logging and verification in marker skill

**Implementation** (`skills/nav-marker/SKILL.md`):
```bash
# After marker creation
if [ -f "$MARKER_FILE" ]; then
  # Verify file is readable and non-empty
  if [ -s "$MARKER_FILE" ]; then
    # Log success with metadata
    echo "[$(date +%H:%M:%S)] ✅ Marker created: $MARKER_FILE"
    echo "[$(date +%H:%M:%S)]    Size: $(wc -c < "$MARKER_FILE") bytes"
    echo "[$(date +%H:%M:%S)]    Phase: $PHASE"

    # Create verification checksum
    md5sum "$MARKER_FILE" > "${MARKER_FILE}.md5"

    # Log to central marker log
    echo "$(date -Iseconds) | $PHASE | SUCCESS | $MARKER_FILE" >> .agent/.marker-log
  else
    echo "[$(date +%H:%M:%S)] ⚠️  Marker empty: $MARKER_FILE"
    echo "$(date -Iseconds) | $PHASE | EMPTY | $MARKER_FILE" >> .agent/.marker-log
  fi
else
  echo "[$(date +%H:%M:%S)] ❌ Marker creation failed: $MARKER_FILE"
  echo "$(date -Iseconds) | $PHASE | FAILED | $MARKER_FILE" >> .agent/.marker-log
fi
```

**Orchestrator verification**:
```bash
verify_marker() {
  local marker_file=$1

  # Check exists
  if [ ! -f "$marker_file" ]; then
    echo "❌ Marker missing: $marker_file"
    return 1
  fi

  # Check non-empty
  if [ ! -s "$marker_file" ]; then
    echo "❌ Marker empty: $marker_file"
    return 1
  fi

  # Verify checksum if available
  if [ -f "${marker_file}.md5" ]; then
    if md5sum -c "${marker_file}.md5" >/dev/null 2>&1; then
      echo "✅ Marker verified: $marker_file"
      return 0
    else
      echo "⚠️  Marker checksum mismatch: $marker_file"
      return 1
    fi
  fi

  echo "✅ Marker exists: $marker_file"
  return 0
}
```

**Files**:
- `skills/nav-marker/SKILL.md` (enhanced logging)
- `scripts/navigator-multi-claude.sh` (verification)

**Testing**:
- Create markers in all phases
- Verify logs capture all events
- Simulate corrupted marker, verify detection

---

### 5. Improved Sub-Claude Prompts

**Problem**: Sub-Claude doesn't consistently invoke marker skill

**Solution**: Explicit marker invocation in phase prompts

**Current prompt** (vague):
```
Complete Phase 3: Testing

1. Run tests
2. Verify results
3. Document findings
4. Signal completion
```

**Improved prompt** (explicit):
```
Complete Phase 3: Testing

CRITICAL: You MUST create a completion marker when done.

Steps:
1. Run tests with pytest
2. Verify all tests pass
3. Document test results
4. Create completion marker:

   INVOKE: nav-marker skill with name "phase3-testing-complete"

   This marker is REQUIRED for the orchestrator to proceed.
   Do NOT skip this step.

Session ID: {SESSION_ID}
Marker file: .agent/tasks/{SESSION_ID}-tests-done
```

**Files**:
- `scripts/navigator-multi-claude.sh` (update all phase prompts)
- `scripts/navigator-multi-claude-poc.sh` (update POC prompts)

**Testing**:
- Run workflow with updated prompts
- Monitor marker creation rate
- Target: 95%+ marker creation

---

## Implementation Plan

### Phase 1: Foundation (Days 1-2)
1. Create sub-claude-monitor.sh
2. Implement state tracking (.agent/tasks/SESSION_ID-state.json)
3. Add marker verification logic
4. Update marker skill logging

**Deliverable**: Infrastructure ready for retry/recovery

### Phase 2: Retry Logic (Days 3-4)
1. Implement wait_for_marker_with_retry()
2. Add restart_current_phase()
3. Update all phase transitions
4. Test retry on simulated failures

**Deliverable**: Orchestrator can retry failed phases

### Phase 3: Recovery (Days 5-6)
1. Create resume-workflow.sh script
2. Implement state persistence
3. Add resume option to orchestrator
4. Test mid-workflow interruption recovery

**Deliverable**: Users can resume interrupted workflows

### Phase 4: Prompts & Verification (Day 7)
1. Update all sub-Claude phase prompts
2. Add explicit marker invocation instructions
3. Enhance marker verification
4. Create central marker log

**Deliverable**: Sub-Claudes reliably create markers

### Phase 5: Testing (Days 8-10)
1. Run 10 simple POC workflows
2. Run 10 medium workflows
3. Run 5 complex workflows
4. Measure success rate
5. Debug remaining failures

**Deliverable**: 90%+ success rate verified

---

## Testing Strategy

### Unit Tests (Per Component)
- `test-retry-logic.sh` - Simulates marker failures
- `test-monitor.sh` - Simulates stuck Claude
- `test-recovery.sh` - Simulates mid-workflow kill
- `test-verification.sh` - Tests marker validation

### Integration Tests (Full Workflows)
- **Simple** (1-2 files): "Add hello world function"
- **Medium** (3-5 files): "Implement JWT authentication"
- **Complex** (6+ files): "Add OAuth2 with Google provider"

### Success Metrics
- Marker creation: 95%+ (measure via .agent/.marker-log)
- Phase transitions: 95%+ (measure via state.json)
- Recovery success: 80%+ (measure via resume tests)
- Overall success: 90%+ (9/10 workflows complete)

---

## Rollout Plan

### v4.5.0-alpha (Internal Testing)
- Ship to Navigator maintainer only
- Run 25 test workflows
- Collect failure logs
- Iterate on fixes

### v4.5.0-beta (Early Adopters)
- Ship as pre-release
- Announce in release notes
- Ask for bug reports
- Target: 85%+ success rate

### v4.5.0 (Stable)
- Ship as stable release
- Update status: Experimental → Beta
- Document known limitations
- Provide troubleshooting guide

---

## Files to Modify

### New Files
- `scripts/sub-claude-monitor.sh` (~60 lines)
- `scripts/resume-workflow.sh` (~100 lines)
- `tests/test-retry-logic.sh` (~50 lines)
- `tests/test-monitor.sh` (~40 lines)
- `tests/test-recovery.sh` (~60 lines)
- `.agent/.marker-log` (log file)

### Modified Files
- `scripts/navigator-multi-claude.sh` (+200 lines)
  - Retry logic
  - State tracking
  - Monitor integration
  - Verification
- `scripts/navigator-multi-claude-poc.sh` (+100 lines)
  - Retry logic
  - Updated prompts
- `skills/nav-marker/SKILL.md` (+30 lines)
  - Enhanced logging
  - Verification
- `skills/nav-start/SKILL.md` (+10 lines)
  - Update status: Experimental → Beta

### Documentation
- `RELEASE-NOTES-v4.5.0.md` (new)
- `.agent/sops/development/multi-claude-troubleshooting.md` (new)
- `scripts/POC-LEARNINGS.md` (update with v4.5 improvements)

**Total estimated**: ~600 new lines, ~340 modified lines

---

## Risk Assessment

### High Risk
- **Monitor killing legitimate Claude instances**
  - Mitigation: Conservative timeouts (3+ minutes)
  - Mitigation: Progress marker check before kill

- **Retry logic infinite loops**
  - Mitigation: Max 1 retry per phase
  - Mitigation: Global workflow timeout (30 minutes)

### Medium Risk
- **State file corruption**
  - Mitigation: JSON validation before parse
  - Mitigation: Atomic writes with temp files

- **Marker checksum false positives**
  - Mitigation: Make checksum optional
  - Mitigation: Fallback to file existence check

### Low Risk
- **Logging fills disk**
  - Mitigation: Log rotation (keep last 100 entries)
  - Mitigation: Cleanup on workflow completion

---

## Success Indicators

**Week 1**: Infrastructure complete, retries working
**Week 2**: 70%+ success rate (improvement from 30%)
**Week 3**: 85%+ success rate (beta quality)
**Week 4**: 90%+ success rate (stable quality)

**Ship when**: 90%+ success rate achieved consistently

---

## Execution Method

**Dogfooding**: Use multi-Claude workflow to implement multi-Claude fixes

**Command**:
```bash
navigator-multi-claude.sh "Implement v4.5.0 multi-Claude reliability fixes from TASK-25"
```

**Expected behavior**:
- Phase 1: Planning (read this task doc, create implementation plan)
- Phase 2: Implementation (modify scripts, add retry logic, etc.)
- Phase 3-4: Testing + Docs (run tests, update release notes)
- Phase 5: Review (verify all changes, check for regressions)

**If it fails**: Proves the problem, implement fixes manually
**If it succeeds**: Validates the approach, release v4.5.0

---

## Next Actions

1. Commit this task doc
2. Run multi-Claude workflow with this task
3. Monitor for marker timeouts
4. Iterate on fixes based on real failure modes

**Ready to execute?** 🚀
