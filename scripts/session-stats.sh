#!/bin/bash

# Extract Claude Code session statistics from ~/.claude/ data
# Usage: ./session-stats.sh [project-path]
# If no path provided, uses current directory

project_path="${1:-$(pwd)}"

# Encode path: replace /. with - (Claude Code's encoding scheme)
encoded_path=$(echo "$project_path" | tr '/.' '--')
claude_dir="$HOME/.claude/projects/$encoded_path"

if [ ! -d "$claude_dir" ]; then
    echo "❌ No Claude Code session data found"
    echo "   Project: $project_path"
    echo "   Expected: $claude_dir"
    exit 1
fi

# Find most recent conversation file (current session)
latest_session=$(ls -t "$claude_dir"/*.jsonl 2>/dev/null | head -1)

if [ -z "$latest_session" ]; then
    echo "❌ No conversation files found in $claude_dir"
    exit 1
fi

# Extract token statistics from JSONL using Python
python3 - "$latest_session" << 'EOF'
import json
import sys

session_file = sys.argv[1]

total_input = 0
total_output = 0
total_cache_creation = 0
total_cache_read = 0
message_count = 0

try:
    with open(session_file, 'r') as f:
        for line in f:
            try:
                data = json.loads(line.strip())
                if 'message' in data and 'usage' in data['message']:
                    usage = data['message']['usage']
                    total_input += usage.get('input_tokens', 0)
                    total_output += usage.get('output_tokens', 0)
                    total_cache_creation += usage.get('cache_creation_input_tokens', 0)
                    total_cache_read += usage.get('cache_read_input_tokens', 0)
                    message_count += 1
            except json.JSONDecodeError:
                pass
except FileNotFoundError:
    print(f"ERROR: Session file not found: {session_file}", file=sys.stderr)
    sys.exit(1)

# Calculate aggregates
total_fresh_input = total_input + total_cache_creation
total_with_cache = total_input + total_cache_read
cache_efficiency = (total_cache_read / total_with_cache * 100) if total_with_cache > 0 else 0

# Output as shell-parseable format
print(f"MESSAGES={message_count}")
print(f"INPUT_TOKENS={total_input}")
print(f"OUTPUT_TOKENS={total_output}")
print(f"CACHE_CREATION={total_cache_creation}")
print(f"CACHE_READ={total_cache_read}")
print(f"TOTAL_FRESH={total_fresh_input}")
print(f"TOTAL_CACHED={total_with_cache}")
print(f"CACHE_EFFICIENCY={cache_efficiency:.1f}")
EOF
