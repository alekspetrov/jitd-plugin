#!/usr/bin/env python3
"""
Social Media Post Analyzer

Extracts key points and structures content for social media posts.

Usage:
    python post_analyzer.py --input "announcement text" [--context file.md]
"""

import argparse
import json
import sys
from typing import Dict, List


def extract_key_points(content: str, max_points: int = 5) -> List[str]:
    """Extract key points from content."""
    # Simple extraction: look for bullet points, numbered lists, or key sentences
    lines = content.split('\n')
    points = []

    for line in lines:
        stripped = line.strip()
        # Extract from bullet points
        if stripped.startswith(('- ', '* ', '• ', '✅ ', '→ ')):
            point = stripped.lstrip('-*•✅→ ').strip()
            if point and len(point) < 100:
                points.append(point)

        # Extract from numbered lists
        elif stripped and stripped[0].isdigit() and '.' in stripped[:3]:
            point = stripped.split('.', 1)[1].strip()
            if point and len(point) < 100:
                points.append(point)

    # Return top N points
    return points[:max_points]


def identify_value_proposition(content: str) -> str:
    """Identify main value proposition."""
    # Look for common value indicators
    value_keywords = [
        'reduce', 'increase', 'automate', 'eliminate', 'simplify',
        'faster', 'easier', 'better', 'savings', 'efficiency'
    ]

    lines = content.lower().split('\n')
    for line in lines:
        if any(keyword in line for keyword in value_keywords):
            # Return the sentence containing value keyword
            return line.strip().capitalize()[:200]

    # Fallback: return first non-empty line
    for line in content.split('\n'):
        if line.strip():
            return line.strip()[:200]

    return "Improves workflow efficiency"


def determine_tone(content: str) -> str:
    """
    Determine content tone.

    Returns: technical-casual, professional, educational, promotional
    """
    content_lower = content.lower()

    # Check for technical indicators
    technical_terms = ['api', 'cli', 'code', 'function', 'plugin', 'skill', 'npm']
    has_technical = sum(1 for term in technical_terms if term in content_lower)

    # Check for casual indicators
    casual_terms = ['just', 'awesome', 'cool', 'amazing', 'finally']
    has_casual = sum(1 for term in casual_terms if term in content_lower)

    # Check for promotional indicators
    promo_terms = ['new', 'launch', 'release', 'now available', 'get it']
    has_promo = sum(1 for term in promo_terms if term in content_lower)

    if has_technical >= 2 and has_casual >= 1:
        return 'technical-casual'
    elif has_technical >= 2:
        return 'technical-professional'
    elif has_promo >= 2:
        return 'promotional'
    else:
        return 'informative'


def suggest_platforms(content: str, tone: str) -> List[str]:
    """Suggest best platforms for content."""
    platforms = []

    # Always include Threads for conversational content
    if tone in ['technical-casual', 'informative']:
        platforms.append('threads')

    # X for concise technical announcements
    if len(content) < 1000 or tone in ['technical-casual', 'promotional']:
        platforms.append('x')

    # LinkedIn for professional/technical deep dives
    if len(content) > 500 or tone in ['technical-professional', 'informative']:
        platforms.append('linkedin')

    return platforms or ['threads', 'x']  # Default


def extract_call_to_action(content: str) -> str:
    """Extract or generate call to action."""
    # Look for common CTA patterns
    cta_patterns = [
        'install', 'update', 'try', 'get started', 'download',
        'sign up', 'learn more', 'check out'
    ]

    lines = content.lower().split('\n')
    for line in lines:
        if any(pattern in line for pattern in cta_patterns):
            return line.strip().capitalize()[:100]

    # Default CTA based on content type
    if 'install' in content.lower():
        return "Install and try it today"
    elif 'update' in content.lower():
        return "Update to get new features"
    else:
        return "Learn more"


def analyze_content(content: str, context: str = None) -> Dict:
    """
    Analyze content and extract structured information.

    Args:
        content: Main announcement text
        context: Optional additional context

    Returns:
        Structured analysis
    """
    # Combine content and context
    full_text = content
    if context:
        full_text = f"{content}\n\n{context}"

    # Extract information
    key_points = extract_key_points(full_text)
    value_prop = identify_value_proposition(full_text)
    tone = determine_tone(full_text)
    platforms = suggest_platforms(full_text, tone)
    cta = extract_call_to_action(full_text)

    # Identify topic (first line or first sentence)
    topic = content.split('\n')[0].strip() if '\n' in content else content[:100]

    return {
        'topic': topic,
        'key_points': key_points,
        'value_proposition': value_prop,
        'tone': tone,
        'suggested_platforms': platforms,
        'call_to_action': cta,
        'content_length': len(full_text),
        'estimated_read_time': f"{len(full_text.split()) // 200 + 1} min"
    }


def main():
    """CLI entry point."""
    parser = argparse.ArgumentParser(description='Analyze content for social media posts')
    parser.add_argument('--input', required=True, help='Announcement or content text')
    parser.add_argument('--context', help='Optional context file path')
    args = parser.parse_args()

    # Read context file if provided
    context = None
    if args.context:
        try:
            with open(args.context, 'r') as f:
                context = f.read()
        except FileNotFoundError:
            print(f"Warning: Context file not found: {args.context}", file=sys.stderr)

    # Analyze
    analysis = analyze_content(args.input, context)

    # Output as JSON
    print(json.dumps(analysis, indent=2))


if __name__ == '__main__':
    main()
