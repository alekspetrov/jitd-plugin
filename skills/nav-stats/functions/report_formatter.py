#!/usr/bin/env python3
"""
Format Navigator efficiency metrics into visual, shareable report.
"""

import sys
import argparse

def format_number(num: int) -> str:
    """Format number with commas for readability."""
    return f"{num:,}"

def interpret_score(score: int) -> str:
    """Get rating label for score."""
    if score >= 90:
        return "excellent"
    elif score >= 80:
        return "good"
    elif score >= 70:
        return "fair"
    else:
        return "poor"

def get_recommendations(
    savings_percent: int,
    cache_efficiency: float,
    context_usage: int,
    efficiency_score: int
) -> list:
    """
    Generate actionable recommendations based on metrics.

    Returns:
        list: List of recommendation strings
    """
    recs = []

    # Check token savings
    if savings_percent < 70:
        recs.append(("⚠️", "Token savings below target (70%+)"))
        recs.append(("→", "Check: Are you loading more docs than needed?"))
        recs.append(("→", "Tip: Use navigator to find docs, don't load all upfront"))
        recs.append(("", "Read more: .agent/philosophy/CONTEXT-EFFICIENCY.md"))
    elif savings_percent >= 85:
        recs.append(("✅", "Excellent token savings - keep using lazy-loading strategy"))

    # Check cache efficiency
    if cache_efficiency < 80:
        recs.append(("⚠️", "Cache efficiency low (<80%)"))
        recs.append(("→", "Check: CLAUDE.md properly configured?"))
        recs.append(("→", "Tip: Ensure prompt caching enabled"))
        recs.append(("", "Read more: .agent/philosophy/PATTERNS.md (Caching pattern)"))
    elif cache_efficiency >= 95:
        recs.append(("✅", "Cache working perfectly - no optimization needed"))

    # Check context usage
    if context_usage > 80:
        recs.append(("⚠️", "Context usage high (80%+)"))
        recs.append(("→", "Consider: Create context marker and compact"))
        recs.append(("→", "Tip: Compact after completing sub-tasks"))
        recs.append(("", "Read more: .agent/philosophy/ANTI-PATTERNS.md"))
    elif context_usage < 40:
        recs.append(("✅", "Context usage healthy - plenty of room for work"))

    # Default excellent message
    if not recs and efficiency_score >= 90:
        recs.append(("✅", "Excellent efficiency - keep it up!"))
        recs.append(("", ""))
        recs.append(("", "Share your efficiency: Take a screenshot! #ContextEfficiency"))

    return recs

def format_report(
    baseline: int,
    loaded: int,
    saved: int,
    savings_percent: int,
    cache_efficiency: float,
    context_usage: int,
    efficiency_score: int,
    time_saved: int
) -> str:
    """
    Format efficiency report.

    Returns:
        str: Formatted report
    """
    rating = interpret_score(efficiency_score)
    recs = get_recommendations(savings_percent, cache_efficiency, context_usage, efficiency_score)

    report = f"""╔══════════════════════════════════════════════════════╗
║          NAVIGATOR EFFICIENCY REPORT                 ║
╚══════════════════════════════════════════════════════╝

📊 TOKEN USAGE
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Documentation loaded:    {format_number(loaded):>12} tokens
Baseline (all docs):     {format_number(baseline):>12} tokens
Tokens saved:            {format_number(saved):>12} tokens ({savings_percent}% ↓)

💾 CACHE PERFORMANCE
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Cache efficiency:        {cache_efficiency:>16.1f}% ({"perfect" if cache_efficiency >= 99 else "good" if cache_efficiency >= 90 else "fair"})

📈 SESSION METRICS
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Context usage:           {context_usage:>16}% ({rating})
Efficiency score:        {efficiency_score:>12}/100 ({rating})

⏱️  TIME SAVED
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Estimated time saved:    {time_saved:>13} minutes

💡 WHAT THIS MEANS
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Navigator loaded {savings_percent}% fewer tokens than loading all docs.
Your context window is {100 - context_usage}% available for actual work.
"""

    # Add recommendations section
    if recs:
        report += "\n🎯 RECOMMENDATIONS\n"
        report += "━" * 54 + "\n"
        for icon, text in recs:
            if icon:
                report += f"{icon}  {text}\n"
            else:
                report += f"{text}\n"

    return report

if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Format Navigator efficiency report"
    )
    parser.add_argument("--baseline", type=int, required=True, help="Baseline tokens (all docs)")
    parser.add_argument("--loaded", type=int, required=True, help="Actually loaded tokens")
    parser.add_argument("--saved", type=int, required=True, help="Tokens saved")
    parser.add_argument("--savings-percent", type=int, required=True, help="Savings percentage")
    parser.add_argument("--cache-efficiency", type=float, required=True, help="Cache efficiency %")
    parser.add_argument("--context-usage", type=int, required=True, help="Context usage %")
    parser.add_argument("--efficiency-score", type=int, required=True, help="Efficiency score (0-100)")
    parser.add_argument("--time-saved", type=int, required=True, help="Time saved (minutes)")

    args = parser.parse_args()

    report = format_report(
        args.baseline,
        args.loaded,
        args.saved,
        args.savings_percent,
        args.cache_efficiency,
        args.context_usage,
        args.efficiency_score,
        args.time_saved
    )

    print(report)
    sys.exit(0)
