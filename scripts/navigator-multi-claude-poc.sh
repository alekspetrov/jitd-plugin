#!/bin/bash
# Navigator Multi-Claude Proof of Concept
# Tests basic automation with 2-phase workflow (plan → implement)

set -euo pipefail

# Colors for output
GREEN='\033[0;32m'
BLUE='\033[0;34m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m' # No Color

# Logging helpers
log_info() {
  echo -e "${BLUE}[$(date '+%H:%M:%S')]${NC} $1"
}

log_success() {
  echo -e "${GREEN}[$(date '+%H:%M:%S')] ✅${NC} $1"
}

log_error() {
  echo -e "${RED}[$(date '+%H:%M:%S')] ❌${NC} $1"
}

log_phase() {
  echo ""
  echo -e "${YELLOW}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
  echo -e "${YELLOW}$1${NC}"
  echo -e "${YELLOW}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
  echo ""
}

# Wait for file to appear
wait_for_file() {
  local file_path="$1"
  local timeout=120  # 2 minutes
  local elapsed=0

  log_info "Waiting for file: $file_path"

  while [ ! -f "$file_path" ]; do
    if [ $elapsed -ge $timeout ]; then
      log_error "Timeout waiting for file: $file_path"
      return 1
    fi
    sleep 1
    ((elapsed++))
  done

  log_success "File created: $file_path"
  return 0
}

# Main workflow
main() {
  local feature_description="${1:-Add health check endpoint}"

  log_phase "🎯 Navigator Multi-Claude POC"
  log_info "Feature: $feature_description"

  # Ensure we're in project root
  if [ ! -f "CLAUDE.md" ]; then
    log_error "Must run from Navigator project root"
    exit 1
  fi

  # Check if claude CLI exists
  if ! command -v claude &> /dev/null; then
    log_error "Claude Code CLI not found. Install from: https://install.claude.com"
    exit 1
  fi

  # Check if jq exists
  if ! command -v jq &> /dev/null; then
    log_error "jq not found. Install with: brew install jq"
    exit 1
  fi

  log_phase "Phase 1: Planning (Orchestrator)"

  # Generate unique task ID
  local task_id="poc-$(date +%s)"
  local plan_file=".agent/tasks/${task_id}-plan.md"

  # Step 1: Create plan and save to file
  log_info "Orchestrator: Creating implementation plan..."

  orchestrator_output=$(claude -p \
    "Start Navigator session. Create a brief implementation plan for: $feature_description. Save the plan to ${plan_file} using the Write tool. Include: 1) Feature description 2) Implementation steps 3) Files to modify 4) Expected outcome." \
    --output-format json \
    --dangerously-skip-permissions 2>&1)

  if [ $? -ne 0 ]; then
    log_error "Orchestrator failed"
    echo "$orchestrator_output"
    exit 1
  fi

  log_success "Plan creation requested"

  # Wait for plan file
  if ! wait_for_file "$plan_file"; then
    log_error "Planning phase failed - no plan file created"
    exit 1
  fi

  log_success "Plan saved to: $plan_file"

  log_phase "Phase 2: Implementation"

  # Launch implementation in headless mode
  log_info "Implementation: Building feature from plan..."

  local impl_done_file=".agent/tasks/${task_id}-done"

  impl_output=$(claude -p \
    "Read the plan from ${plan_file}. Implement the feature following the plan. When done, create empty file ${impl_done_file} using: touch ${impl_done_file}" \
    --output-format json \
    --allowedTools "Read,Write,Edit,Bash" \
    --dangerously-skip-permissions 2>&1)

  if [ $? -ne 0 ]; then
    log_error "Implementation failed"
    echo "$impl_output"
    exit 1
  fi

  log_success "Implementation requested"

  # Wait for completion marker file
  if ! wait_for_file "$impl_done_file"; then
    log_error "Implementation phase failed - no completion marker"
    exit 1
  fi

  log_success "Implementation complete"

  log_phase "Phase 3 & 4: Parallel Testing + Documentation"

  local test_done_file=".agent/tasks/${task_id}-tests-done"
  local docs_done_file=".agent/tasks/${task_id}-docs-done"

  # Launch testing Claude in background
  log_info "Testing: Validating implementation and generating tests... (parallel)"

  (
    test_output=$(claude -p \
      "Read the plan from ${plan_file}. Review the implementation and generate comprehensive tests. Run the tests to validate the implementation. When done, create empty file ${test_done_file} using: touch ${test_done_file}" \
      --output-format json \
      --allowedTools "Read,Write,Edit,Bash" \
      --dangerously-skip-permissions 2>&1)

    if [ $? -ne 0 ]; then
      echo "TEST_FAILED" > ".agent/tasks/${task_id}-tests-failed"
      log_error "Testing failed"
    fi
  ) &
  local test_pid=$!

  # Launch documentation Claude in parallel
  log_info "Documentation: Generating comprehensive docs... (parallel)"

  (
    docs_output=$(claude -p \
      "Read the plan from ${plan_file}. Review the implementation and generate comprehensive documentation (README sections, JSDoc improvements, usage examples). When done, create empty file ${docs_done_file} using the Bash tool: touch ${docs_done_file}" \
      --output-format json \
      --allowedTools "Read,Write,Edit,Bash" \
      --dangerously-skip-permissions 2>&1)

    if [ $? -ne 0 ]; then
      echo "DOCS_FAILED" > ".agent/tasks/${task_id}-docs-failed"
      log_error "Documentation failed"
    fi
  ) &
  local docs_pid=$!

  log_success "Parallel execution started (Testing + Documentation)"

  # Wait for both processes to complete
  log_info "Waiting for parallel phases to complete..."

  # Wait for testing
  if ! wait_for_file "$test_done_file"; then
    log_error "Testing phase timeout - no completion marker"
    kill $test_pid $docs_pid 2>/dev/null
    exit 1
  fi
  log_success "Testing complete"

  # Wait for documentation
  if ! wait_for_file "$docs_done_file"; then
    log_error "Documentation phase timeout - no completion marker"
    kill $docs_pid 2>/dev/null
    exit 1
  fi
  log_success "Documentation complete"

  # Wait for background processes to fully exit
  wait $test_pid $docs_pid 2>/dev/null

  # Check quality gates
  log_info "Checking quality gates..."

  if [ -f ".agent/tasks/${task_id}-tests-failed" ]; then
    log_error "Tests failed - quality gate not met"
    cat ".agent/tasks/${task_id}-tests-failed"
    exit 1
  fi

  if [ -f ".agent/tasks/${task_id}-docs-failed" ]; then
    log_error "Documentation generation failed"
    cat ".agent/tasks/${task_id}-docs-failed"
    exit 1
  fi

  log_success "All quality gates passed ✓"

  log_phase "✅ POC Complete"
  log_success "Feature: $feature_description"
  log_success "Phases: Planning ✓ Implementation ✓ [Testing+Docs] ✓"
  log_success "Plan: $plan_file"

  echo ""
  echo "Next steps:"
  echo "1. Review changes: git status"
  echo "2. Check plan: cat $plan_file"
  echo "3. Review tests: find . -name '*.test.*' -newer $plan_file"
  echo "4. Review docs: git diff '*.md'"
  echo ""
}

# Trap errors
trap 'log_error "Script failed on line $LINENO"' ERR

# Run main
main "$@"
