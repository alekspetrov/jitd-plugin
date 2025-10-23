#!/usr/bin/env python3
"""
Calculate Navigator efficiency score (0-100).

Weights:
- Token savings: 40 points (85%+ = max)
- Cache efficiency: 30 points (100% = max)
- Context usage: 30 points (<40% = max, >80% = 0)
"""

import sys
import argparse

def calculate_efficiency_score(
    tokens_saved_percent: float,
    cache_efficiency: float,
    context_usage_percent: float
) -> int:
    """
    Calculate Navigator efficiency score (0-100).

    Args:
        tokens_saved_percent: Percentage of tokens saved vs baseline (0-100)
        cache_efficiency: Cache hit rate (0-100)
        context_usage_percent: Percentage of context window used (0-100)

    Returns:
        int: Efficiency score (0-100)
    """
    # Token savings (40 points max)
    # 85%+ savings = 40 points, linear scale below
    token_score = min(40, (tokens_saved_percent / 85) * 40)

    # Cache efficiency (30 points max)
    # 100% = 30 points, linear scale
    cache_score = (cache_efficiency / 100) * 30

    # Context usage (30 points max)
    # <40% = 30 points (excellent)
    # 40-80% = linear from 30 to 0 (good → fair)
    # >80% = 0 points (poor - context overloaded)
    if context_usage_percent < 40:
        context_score = 30
    elif context_usage_percent <= 80:
        # Linear decay from 30 (at 40%) to 0 (at 80%)
        context_score = 30 - ((context_usage_percent - 40) / 40) * 30
    else:
        context_score = 0

    total_score = int(token_score + cache_score + context_score)

    # Ensure score is in valid range
    return max(0, min(100, total_score))

def interpret_score(score: int) -> str:
    """
    Interpret efficiency score into human-readable rating.

    Args:
        score: Efficiency score (0-100)

    Returns:
        str: Rating (excellent, good, fair, poor)
    """
    if score >= 90:
        return "excellent"
    elif score >= 80:
        return "good"
    elif score >= 70:
        return "fair"
    else:
        return "poor"

if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Calculate Navigator efficiency score"
    )
    parser.add_argument(
        "--tokens-saved-percent",
        type=float,
        required=True,
        help="Percentage of tokens saved vs baseline (0-100)"
    )
    parser.add_argument(
        "--cache-efficiency",
        type=float,
        required=True,
        help="Cache hit rate percentage (0-100)"
    )
    parser.add_argument(
        "--context-usage",
        type=float,
        required=True,
        help="Context window usage percentage (0-100)"
    )
    parser.add_argument(
        "--verbose",
        action="store_true",
        help="Show detailed breakdown"
    )

    args = parser.parse_args()

    score = calculate_efficiency_score(
        args.tokens_saved_percent,
        args.cache_efficiency,
        args.context_usage
    )

    if args.verbose:
        rating = interpret_score(score)
        print(f"Efficiency Score: {score}/100 ({rating})")
        print(f"  Token savings: {args.tokens_saved_percent}%")
        print(f"  Cache efficiency: {args.cache_efficiency}%")
        print(f"  Context usage: {args.context_usage}%")
    else:
        # Output just the score (parseable)
        print(score)

    sys.exit(0)
