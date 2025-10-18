#!/usr/bin/env python3
"""
JITD Navigator - Session Statistics Calculator

Calculates token usage from file sizes for JITD session start.
"""

import os
import sys


def calculate_file_tokens(file_path):
    """
    Calculate token count from file size.
    Standard estimation: bytes / 4 = tokens
    """
    try:
        if os.path.exists(file_path):
            file_bytes = os.path.getsize(file_path)
            tokens = file_bytes // 4
            return {
                "path": file_path,
                "bytes": file_bytes,
                "tokens": tokens,
                "exists": True
            }
        else:
            return {
                "path": file_path,
                "bytes": 0,
                "tokens": 0,
                "exists": False
            }
    except Exception as e:
        return {
            "path": file_path,
            "bytes": 0,
            "tokens": 0,
            "exists": False,
            "error": str(e)
        }


def main():
    # Files to measure
    navigator_path = ".agent/DEVELOPMENT-README.md"
    claude_md_path = "CLAUDE.md"

    # Calculate tokens
    navigator = calculate_file_tokens(navigator_path)
    claude_md = calculate_file_tokens(claude_md_path)

    # Total tokens
    total_tokens = navigator["tokens"] + claude_md["tokens"]

    # Available context (200k total, ~50k system overhead)
    system_overhead = 50000
    total_context = 200000
    available = total_context - system_overhead - total_tokens
    percent = int((available / total_context) * 100)

    # Output formatted for display
    print(f"Navigator ({navigator_path}):")
    if navigator["exists"]:
        print(f"  Size: {navigator['bytes']:,} bytes = {navigator['tokens']:,} tokens")
    else:
        print(f"  ❌ Not found")

    print(f"\nCLAUDE.md (auto-loaded):")
    if claude_md["exists"]:
        print(f"  Size: {claude_md['bytes']:,} bytes = {claude_md['tokens']:,} tokens")
    else:
        print(f"  ⚠️  Not found (recommended to create)")

    print(f"\n━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━")
    print(f"Total documentation:     {total_tokens:,} tokens")
    print(f"Available for work:      {available:,} tokens ({percent}%)")
    print(f"━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━")

    return 0


if __name__ == "__main__":
    sys.exit(main())
