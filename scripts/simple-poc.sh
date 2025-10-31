#!/bin/bash
# Simplified POC - just test 2-phase coordination without Navigator

set -euo pipefail

echo "🎯 Simple Multi-Claude POC"
echo ""

# Phase 1: Create plan
echo "Phase 1: Planning..."
plan_output=$(claude -p "Create a brief 3-step plan for: Add timestamp utility function" --output-format json 2>&1)
plan_session=$(echo "$plan_output" | jq -r '.session_id')
echo "✅ Plan created (session: ${plan_session:0:8})"

# Write plan to file (simulating marker)
echo "$plan_output" | jq -r '.result' > /tmp/simple-poc-plan.txt
echo "✅ Plan saved to /tmp/simple-poc-plan.txt"

# Phase 2: Implementation
echo ""
echo "Phase 2: Implementation..."
impl_prompt="Read this plan and implement it:

$(cat /tmp/simple-poc-plan.txt)

Create a simple timestamp utility function."

impl_output=$(claude -p "$impl_prompt" --output-format json --allowedTools "Write" 2>&1)
impl_session=$(echo "$impl_output" | jq -r '.session_id')
echo "✅ Implementation complete (session: ${impl_session:0:8})"

echo ""
echo "✅ POC Complete!"
echo "Plan session: $plan_session"
echo "Impl session: $impl_session"
echo ""
echo "Check what was created:"
echo "git status"
