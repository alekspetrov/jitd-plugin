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


# Enhanced metrics for Navigator v3.5.0+
# Pass session metrics to Python for baseline comparison
python3 - "$project_path" "$latest_session" << 'ENHANCED_EOF'
import sys
import os
import glob
import json

project_path = sys.argv[1]
session_file = sys.argv[2]

# Check if Navigator initialized
agent_dir = os.path.join(project_path, ".agent")
if not os.path.exists(agent_dir):
    # Not initialized - output zeros
    print("BASELINE_TOKENS=0")
    print("LOADED_TOKENS=0")
    print("TOKENS_SAVED=0")
    print("SAVINGS_PERCENT=0")
    print("CONTEXT_USAGE_PERCENT=0")
    print("TIME_SAVED_MINUTES=0")
    sys.exit(0)

# Calculate baseline: all .agent/ markdown files
# Convert bytes to tokens (4 chars ≈ 1 token)
baseline_bytes = 0
for md_file in glob.glob(os.path.join(agent_dir, "**/*.md"), recursive=True):
    try:
        baseline_bytes += os.path.getsize(md_file)
    except OSError:
        pass

baseline_tokens = baseline_bytes // 4

# Extract actual loaded tokens from session cache creation
# CACHE_CREATION represents docs loaded fresh in this session
total_input = 0
total_output = 0
total_cache_creation = 0
total_cache_read = 0

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
            except json.JSONDecodeError:
                pass
except FileNotFoundError:
    pass

# Loaded tokens = cache creation (docs loaded for first time this session)
# This represents actual Navigator documentation loaded
loaded_tokens = total_cache_creation if total_cache_creation > 0 else max(baseline_tokens // 10, 5000)

# Calculate savings
tokens_saved = baseline_tokens - loaded_tokens
savings_percent = int((tokens_saved / baseline_tokens * 100)) if baseline_tokens > 0 else 0

# Calculate actual context usage
# Claude Code uses 200k context window
# Context = fresh input + output tokens (cached tokens don't count - deduplicated)
# Fresh input = total_input + total_cache_creation
total_fresh_input = total_input + total_cache_creation
total_conversation_tokens = total_fresh_input + total_output
context_window_size = 200000
context_usage_percent = min(100, int((total_conversation_tokens / context_window_size) * 100))

# Estimate time saved (6 seconds per 1k tokens read time)
time_saved_minutes = (tokens_saved * 6) // 60000

print(f"BASELINE_TOKENS={baseline_tokens}")
print(f"LOADED_TOKENS={loaded_tokens}")
print(f"TOKENS_SAVED={tokens_saved}")
print(f"SAVINGS_PERCENT={savings_percent}")
print(f"CONTEXT_USAGE_PERCENT={context_usage_percent}")
print(f"TIME_SAVED_MINUTES={time_saved_minutes}")
ENHANCED_EOF
