#!/bin/bash
# Test Retry Logic
# Simulates marker creation failures and verifies retry mechanism

set -euo pipefail

# Colors
GREEN='\033[0;32m'
RED='\033[0;31m'
YELLOW='\033[1;33m'
NC='\033[0m'

TEST_DIR=".agent/tasks/test-retry-$$"
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

# Source the retry functions
source scripts/navigator-multi-claude.sh

# Test 1: Marker created on first attempt
test_first_attempt_success() {
  log_test "Test 1: Marker created on first attempt"

  local marker_file="$TEST_DIR/test1-marker"

  # Create marker immediately
  touch "$marker_file"

  if wait_for_marker_with_retry "$marker_file" "test1" 1 5; then
    log_pass "First attempt success verified"
  else
    log_fail "Should succeed on first attempt"
  fi

  rm -f "$marker_file"
}

# Test 2: Marker created on second attempt (retry)
test_second_attempt_success() {
  log_test "Test 2: Marker created on second attempt (retry)"

  local marker_file="$TEST_DIR/test2-marker"

  # Create marker after 3 seconds (simulating delay)
  (sleep 3 && touch "$marker_file") &
  local bg_pid=$!

  if wait_for_marker_with_retry "$marker_file" "test2" 1 2; then
    log_pass "Retry mechanism worked correctly"
  else
    log_fail "Should succeed on retry"
  fi

  wait $bg_pid 2>/dev/null || true
  rm -f "$marker_file"
}

# Test 3: Marker never created (both attempts fail)
test_both_attempts_fail() {
  log_test "Test 3: Both attempts fail (no marker created)"

  local marker_file="$TEST_DIR/test3-marker"

  # Don't create marker at all
  if wait_for_marker_with_retry "$marker_file" "test3" 1 2; then
    log_fail "Should fail when marker never created"
  else
    log_pass "Correctly failed after retry attempts"
  fi
}

# Test 4: Empty marker file detection
test_empty_marker_detection() {
  log_test "Test 4: Empty marker file detection"

  local marker_file="$TEST_DIR/test4-marker"

  # Create empty marker (invalid)
  touch "$marker_file"

  # Should be accepted (empty markers are valid per implementation)
  if wait_for_marker_with_retry "$marker_file" "test4" 0 2; then
    log_pass "Empty marker accepted (as designed)"
  else
    log_fail "Empty marker should be accepted"
  fi

  rm -f "$marker_file"
}

# Test 5: State file creation
test_state_file_creation() {
  log_test "Test 5: State file creation on retry"

  export STATE_FILE="$TEST_DIR/test5-state.json"
  export session_id="test5-session"
  export task_id="TEST-5"
  export PHASES_COMPLETED='"phase0"'

  save_phase_state "test-phase" 1 "retry"

  if [ -f "$STATE_FILE" ]; then
    log_pass "State file created successfully"

    # Verify JSON structure
    if command -v jq &> /dev/null; then
      if jq empty "$STATE_FILE" 2>/dev/null; then
        log_pass "State file has valid JSON"
      else
        log_fail "State file has invalid JSON"
      fi
    fi
  else
    log_fail "State file not created"
  fi

  rm -f "$STATE_FILE"
}

# Run all tests
echo ""
echo "======================================"
echo "  Multi-Claude Retry Logic Tests"
echo "======================================"
echo ""

test_first_attempt_success
test_second_attempt_success
test_both_attempts_fail
test_empty_marker_detection
test_state_file_creation

echo ""
echo -e "${GREEN}All tests passed! ✅${NC}"
echo ""
