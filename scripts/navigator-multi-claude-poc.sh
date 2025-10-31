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

# Wait for marker file to appear
wait_for_marker() {
  local marker_name="$1"
  local marker_path=".context-markers/${marker_name}.md"
  local timeout=300  # 5 minutes
  local elapsed=0

  log_info "Waiting for marker: $marker_name"

  while [ ! -f "$marker_path" ]; do
    if [ $elapsed -ge $timeout ]; then
      log_error "Timeout waiting for marker: $marker_name"
      return 1
    fi
    sleep 1
    ((elapsed++))
  done

  log_success "Marker received: $marker_name"
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

  # Step 1: Start session and create plan
  log_info "Orchestrator: Creating implementation plan..."

  orchestrator_output=$(claude -p \
    "Start Navigator session. Create a brief implementation plan for: $feature_description" \
    --output-format json 2>&1)

  if [ $? -ne 0 ]; then
    log_error "Orchestrator failed"
    echo "$orchestrator_output"
    exit 1
  fi

  # Extract session ID
  orchestrator_session=$(echo "$orchestrator_output" | jq -r '.session_id // empty')

  if [ -z "$orchestrator_session" ]; then
    log_error "Failed to get orchestrator session ID"
    exit 1
  fi

  log_success "Plan created (session: ${orchestrator_session:0:8}...)"

  # Step 2: Create marker in same session
  log_info "Creating marker..."

  marker_output=$(claude -p --resume "$orchestrator_session" \
    "Create marker 'poc-plan' with summary of the implementation plan" \
    --output-format json 2>&1)

  if [ $? -ne 0 ]; then
    log_error "Marker creation failed"
    echo "$marker_output"
    exit 1
  fi

  log_success "Marker creation requested"

  # Wait for plan marker
  if ! wait_for_marker "poc-plan"; then
    log_error "Planning phase failed - no marker created"
    log_info "Tip: Claude may need explicit marker skill invocation"
    exit 1
  fi

  log_phase "Phase 2: Implementation"

  # Launch implementation in headless mode
  log_info "Implementation: Building feature from plan..."

  impl_output=$(claude -p \
    "Load marker poc-plan. Implement the feature following the plan. Create marker 'poc-impl' when done." \
    --output-format json \
    --allowedTools "Read,Write,Edit,Bash" 2>&1)

  if [ $? -ne 0 ]; then
    log_error "Implementation failed"
    echo "$impl_output"
    exit 1
  fi

  impl_session=$(echo "$impl_output" | jq -r '.session_id // empty')

  if [ -n "$impl_session" ]; then
    log_success "Implementation complete (session: ${impl_session:0:8}...)"
  else
    log_success "Implementation complete"
  fi

  # Wait for implementation marker
  if ! wait_for_marker "poc-impl"; then
    log_error "Implementation phase failed - no marker created"
    exit 1
  fi

  log_phase "✅ POC Complete"
  log_success "Feature: $feature_description"
  log_success "Phases: Planning ✓ Implementation ✓"
  log_success "Markers: poc-plan.md, poc-impl.md"

  echo ""
  echo "Next steps:"
  echo "1. Review changes: git status"
  echo "2. Check markers: ls -la .context-markers/"
  echo "3. Verify implementation works"
  echo ""
}

# Trap errors
trap 'log_error "Script failed on line $LINENO"' ERR

# Run main
main "$@"
