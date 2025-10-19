#!/usr/bin/env python3
"""
Compress conversation context into a concise marker summary.
"""

import sys
import argparse
from datetime import datetime

def compress_context(context_text, max_length=5000):
    """
    Compress conversation context while preserving key information.

    Args:
        context_text: Full conversation context
        max_length: Maximum compressed length (default: 5000 chars)

    Returns:
        str: Compressed summary
    """
    # In a real implementation, this would use AI summarization
    # For now, we'll use simple truncation with smart extraction

    # Extract key sections (simplified for v2.0)
    lines = context_text.split('\n')

    # Priority extraction:
    # 1. Code blocks
    # 2. File paths mentioned
    # 3. Error messages
    # 4. Task descriptions
    # 5. Recent conversation

    code_blocks = []
    file_paths = []
    errors = []
    recent_context = []

    in_code_block = False
    code_buffer = []

    for line in lines[-200:]:  # Focus on recent 200 lines
        # Extract code blocks
        if line.strip().startswith('```'):
            if in_code_block:
                code_blocks.append('\n'.join(code_buffer))
                code_buffer = []
            in_code_block = not in_code_block
        elif in_code_block:
            code_buffer.append(line)

        # Extract file paths
        if '.md' in line or '.py' in line or '.json' in line or '.sh' in line:
            file_paths.append(line.strip())

        # Extract errors
        if 'error' in line.lower() or 'failed' in line.lower():
            errors.append(line.strip())

        # Keep recent context
        if len(recent_context) < 50:
            recent_context.append(line)

    # Build compressed summary
    summary_parts = []

    if file_paths:
        summary_parts.append("**Files Modified**:\n" + '\n'.join(set(file_paths[:10])))

    if code_blocks:
        summary_parts.append("**Code Snippets**:\n```\n" + '\n\n'.join(code_blocks[:3]) + "\n```")

    if errors:
        summary_parts.append("**Errors/Issues**:\n" + '\n'.join(set(errors[:5])))

    summary_parts.append("**Recent Context**:\n" + '\n'.join(recent_context[-20:]))

    compressed = '\n\n---\n\n'.join(summary_parts)

    # Ensure within max_length
    if len(compressed) > max_length:
        compressed = compressed[:max_length] + "\n\n[... truncated ...]"

    return compressed

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Compress conversation context for markers")
    parser.add_argument("--input", help="Input file (default: stdin)")
    parser.add_argument("--max-length", type=int, default=5000, help="Max compressed length")

    args = parser.parse_args()

    if args.input:
        with open(args.input, 'r') as f:
            context = f.read()
    else:
        context = sys.stdin.read()

    compressed = compress_context(context, args.max_length)
    print(compressed)
