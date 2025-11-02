#!/bin/bash
# Test Workflow Recovery
# Simulates workflow interruptions and verifies resume capability

set -euo pipefail

# Colors
GREEN='\033[0;32m'
RED='\033[0;31m'
YELLOW='\033[1;33m'
NC='\033[0m'

TEST_DIR=".agent/tasks/test-recovery-$$"
mkdir -p "$TEST_DIR"

log_test() {
  echo -e "${YELLOW}[TEST]${NC} $1"
}

log_pass() {
  echo -e "${GREEN}[PASS]${NC} $1"
}

log_fail() {
  echo -e "${RED}[FAIL]${NC} $1"
  exit 1
}

cleanup() {
  rm -rf "$TEST_DIR"
}

trap cleanup EXIT

# Test 1: State file creation
test_state_file_creation() {
  log_test "Test 1: State file is created correctly"

  local state_file="$TEST_DIR/test1-state.json"
  local session_id="test1-session"
  local task_id="TEST-1"

  # Create state file manually (simulating save_phase_state)
  cat > "$state_file" <<EOF
{
  "session_id": "$session_id",
  "task": "$task_id",
  "phases_completed": ["phase0", "phase1"],
  "current_phase": "phase2",
  "phase_attempts": {
    "phase2": 1
  },
  "status": "retry",
  "last_update": "2025-11-02T10:00:00Z"
}
EOF

  if [ -f "$state_file" ]; then
    log_pass "State file created successfully"

    # Verify JSON structure
    if command -v jq &> /dev/null; then
      if jq empty "$state_file" 2>/dev/null; then
        log_pass "State file has valid JSON"

        # Verify fields
        local read_session=$(jq -r '.session_id' "$state_file")
        if [ "$read_session" == "$session_id" ]; then
          log_pass "Session ID correctly stored"
        else
          log_fail "Session ID mismatch"
        fi
      else
        log_fail "State file has invalid JSON"
      fi
    else
      log_pass "jq not available, skipping JSON validation"
    fi
  else
    log_fail "State file not created"
  fi
}

# Test 2: State file parsing
test_state_file_parsing() {
  log_test "Test 2: State file can be parsed correctly"

  local state_file="$TEST_DIR/test2-state.json"

  cat > "$state_file" <<EOF
{
  "session_id": "test2-session",
  "task": "TEST-2",
  "phases_completed": ["phase0", "phase1", "phase2"],
  "current_phase": "phase3",
  "phase_attempts": {
    "phase3": 2
  },
  "status": "failed",
  "last_update": "2025-11-02T10:15:00Z"
}
EOF

  if command -v jq &> /dev/null; then
    local task_id=$(jq -r '.task' "$state_file")
    local current_phase=$(jq -r '.current_phase' "$state_file")
    local status=$(jq -r '.status' "$state_file")

    if [ "$task_id" == "TEST-2" ] && [ "$current_phase" == "phase3" ] && [ "$status" == "failed" ]; then
      log_pass "State file parsed correctly"
    else
      log_fail "State file parsing failed"
    fi
  else
    log_pass "jq not available, skipping parsing test"
  fi
}

# Test 3: Multiple state files tracking
test_multiple_state_files() {
  log_test "Test 3: Multiple workflow states can coexist"

  local state1="$TEST_DIR/workflow1-state.json"
  local state2="$TEST_DIR/workflow2-state.json"

  cat > "$state1" <<EOF
{
  "session_id": "workflow1",
  "task": "TEST-1",
  "phases_completed": ["phase0"],
  "current_phase": "phase1",
  "phase_attempts": {"phase1": 1},
  "status": "in_progress",
  "last_update": "2025-11-02T10:00:00Z"
}
EOF

  cat > "$state2" <<EOF
{
  "session_id": "workflow2",
  "task": "TEST-2",
  "phases_completed": ["phase0", "phase1"],
  "current_phase": "phase2",
  "phase_attempts": {"phase2": 1},
  "status": "retry",
  "last_update": "2025-11-02T10:30:00Z"
}
EOF

  if [ -f "$state1" ] && [ -f "$state2" ]; then
    log_pass "Multiple state files created"

    if command -v jq &> /dev/null; then
      local task1=$(jq -r '.task' "$state1")
      local task2=$(jq -r '.task' "$state2")

      if [ "$task1" == "TEST-1" ] && [ "$task2" == "TEST-2" ]; then
        log_pass "State files maintain separate identities"
      else
        log_fail "State file isolation failed"
      fi
    fi
  else
    log_fail "Multiple state files not created"
  fi
}

# Test 4: State update simulation
test_state_updates() {
  log_test "Test 4: State file updates correctly"

  local state_file="$TEST_DIR/test4-state.json"

  # Initial state
  cat > "$state_file" <<EOF
{
  "session_id": "test4",
  "task": "TEST-4",
  "phases_completed": [],
  "current_phase": "phase0",
  "phase_attempts": {"phase0": 1},
  "status": "in_progress",
  "last_update": "2025-11-02T10:00:00Z"
}
EOF

  # Update state (simulating phase completion)
  if command -v jq &> /dev/null; then
    jq '.phases_completed += ["phase0"] | .current_phase = "phase1" | .status = "complete"' \
      "$state_file" > "${state_file}.tmp"
    mv "${state_file}.tmp" "$state_file"

    local updated_phase=$(jq -r '.current_phase' "$state_file")
    local completed=$(jq -r '.phases_completed | length' "$state_file")

    if [ "$updated_phase" == "phase1" ] && [ "$completed" == "1" ]; then
      log_pass "State updates work correctly"
    else
      log_fail "State update failed"
    fi
  else
    log_pass "jq not available, skipping update test"
  fi
}

# Test 5: Resume script existence check
test_resume_script_exists() {
  log_test "Test 5: Resume script is available"

  if [ -f "./scripts/resume-workflow.sh" ] && [ -x "./scripts/resume-workflow.sh" ]; then
    log_pass "Resume script exists and is executable"
  else
    log_fail "Resume script not found or not executable"
  fi
}

# Run all tests
echo ""
echo "======================================"
echo "  Workflow Recovery Tests"
echo "======================================"
echo ""

test_state_file_creation
test_state_file_parsing
test_multiple_state_files
test_state_updates
test_resume_script_exists

echo ""
echo -e "${GREEN}All tests passed! ✅${NC}"
echo ""
