#!/bin/bash
# Test JSON extraction

set -euo pipefail

echo "Step 1: Call Claude..."
output=$(claude -p "Say: Test" --output-format json 2>&1)

echo "Step 2: Check exit code: $?"

echo "Step 3: Extract session ID..."
session_id=$(echo "$output" | jq -r '.session_id')

echo "Session ID: $session_id"

if [ -n "$session_id" ]; then
  echo "✅ SUCCESS - Got session ID"
else
  echo "❌ FAILED - No session ID"
  echo "Raw output:"
  echo "$output"
fi
