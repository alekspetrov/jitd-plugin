#!/usr/bin/env python3
"""
Navigator Version Detector

Detects current Navigator version and checks for updates from GitHub releases.

Usage:
    python version_detector.py
"""

import json
import os
import re
import subprocess
import sys
from pathlib import Path
from typing import Dict, Optional
from urllib import request


def get_current_version() -> Optional[str]:
    """
    Get currently installed Navigator version from /plugin list.

    Returns:
        Version string (e.g., "3.3.0") or None if not found
    """
    try:
        # Try to run claude plugin list command
        result = subprocess.run(
            ['claude', 'plugin', 'list'],
            capture_output=True,
            text=True,
            timeout=10
        )

        # Parse output for navigator version
        for line in result.stdout.split('\n'):
            if 'navigator' in line.lower():
                # Extract version (e.g., "navigator (v3.3.0)" or "navigator (3.3.0)")
                match = re.search(r'v?(\d+\.\d+\.\d+)', line)
                if match:
                    return match.group(1)

        return None
    except (subprocess.TimeoutExpired, FileNotFoundError, subprocess.SubprocessError):
        return None


def get_plugin_json_version() -> Optional[str]:
    """
    Fallback: Get version from plugin.json in Navigator plugin directory.

    Returns:
        Version string or None
    """
    # Common plugin installation paths
    possible_paths = [
        Path.home() / '.config' / 'claude' / 'plugins' / 'navigator' / '.claude-plugin' / 'plugin.json',
        Path.home() / '.claude' / 'plugins' / 'navigator' / '.claude-plugin' / 'plugin.json',
        Path.home() / 'Library' / 'Application Support' / 'Claude' / 'plugins' / 'navigator' / '.claude-plugin' / 'plugin.json',
    ]

    for path in possible_paths:
        if path.exists():
            try:
                with open(path, 'r') as f:
                    data = json.load(f)
                    return data.get('version')
            except (json.JSONDecodeError, FileNotFoundError, PermissionError):
                continue

    return None


def get_latest_version_from_github() -> Dict:
    """
    Get latest Navigator version from GitHub releases API.

    Returns:
        Dict with version, release_url, and changes
    """
    try:
        url = 'https://api.github.com/repos/alekspetrov/navigator/releases/latest'

        req = request.Request(url)
        req.add_header('User-Agent', 'Navigator-Version-Detector')

        with request.urlopen(req, timeout=10) as response:
            data = json.load(response)

            # Extract version from tag_name (e.g., "v3.3.0" → "3.3.0")
            tag_name = data.get('tag_name', '')
            version = tag_name.lstrip('v')

            # Parse release notes for key changes
            body = data.get('body', '')
            changes = parse_release_notes(body)

            return {
                'version': version,
                'release_url': data.get('html_url', ''),
                'release_date': data.get('published_at', '').split('T')[0],
                'changes': changes
            }
    except Exception as e:
        return {
            'version': None,
            'error': str(e)
        }


def parse_release_notes(body: str) -> Dict:
    """
    Parse release notes to extract key changes.

    Args:
        body: Release notes markdown

    Returns:
        Dict with new_skills, updated_skills, new_features, breaking_changes
    """
    changes = {
        'new_skills': [],
        'updated_skills': [],
        'new_features': [],
        'breaking_changes': []
    }

    # Extract new skills
    skill_pattern = r'-\s+\*\*(\w+-[\w-]+)\*\*:.*\(NEW\)'
    for match in re.finditer(skill_pattern, body):
        changes['new_skills'].append(match.group(1))

    # Extract features from "What's New" section
    features_section = re.search(r'##\s+.*What.*s New(.*?)(?=##|\Z)', body, re.DOTALL | re.IGNORECASE)
    if features_section:
        # Find bullet points
        for line in features_section.group(1).split('\n'):
            if line.strip().startswith('-') or line.strip().startswith('*'):
                feature = line.strip().lstrip('-*').strip()
                if feature and len(feature) < 100:  # Reasonable feature description
                    changes['new_features'].append(feature)

    # Check for breaking changes
    if 'breaking change' in body.lower() or '⚠️' in body:
        breaking_section = re.search(r'##\s+.*Breaking.*Changes(.*?)(?=##|\Z)', body, re.DOTALL | re.IGNORECASE)
        if breaking_section:
            for line in breaking_section.group(1).split('\n'):
                if line.strip().startswith('-') or line.strip().startswith('*'):
                    change = line.strip().lstrip('-*').strip()
                    if change:
                        changes['breaking_changes'].append(change)

    return changes


def compare_versions(current: str, latest: str) -> int:
    """
    Compare two semantic versions.

    Args:
        current: Current version (e.g., "3.2.0")
        latest: Latest version (e.g., "3.3.0")

    Returns:
        -1 if current < latest (update available)
         0 if current == latest (up to date)
         1 if current > latest (ahead of latest, e.g., dev version)
    """
    try:
        current_parts = [int(x) for x in current.split('.')]
        latest_parts = [int(x) for x in latest.split('.')]

        # Pad to same length
        while len(current_parts) < len(latest_parts):
            current_parts.append(0)
        while len(latest_parts) < len(current_parts):
            latest_parts.append(0)

        # Compare
        for c, l in zip(current_parts, latest_parts):
            if c < l:
                return -1
            elif c > l:
                return 1

        return 0
    except (ValueError, AttributeError):
        return 0  # Can't compare, assume equal


def detect_version() -> Dict:
    """
    Detect current and latest Navigator versions.

    Returns:
        Complete version detection report
    """
    # Get current version
    current_version = get_current_version()

    if not current_version:
        # Fallback to plugin.json
        current_version = get_plugin_json_version()

    # Get latest version from GitHub
    latest_info = get_latest_version_from_github()
    latest_version = latest_info.get('version')

    # Determine if update available
    update_available = False
    if current_version and latest_version:
        comparison = compare_versions(current_version, latest_version)
        update_available = (comparison == -1)

    # Build report
    report = {
        'current_version': current_version,
        'latest_version': latest_version,
        'update_available': update_available,
        'release_url': latest_info.get('release_url', ''),
        'release_date': latest_info.get('release_date', ''),
        'changes': latest_info.get('changes', {}),
        'error': latest_info.get('error'),
        'recommendation': get_recommendation(current_version, latest_version, update_available)
    }

    return report


def get_recommendation(current: Optional[str], latest: Optional[str], update_available: bool) -> str:
    """Generate recommendation based on version status."""
    if not current:
        return "Navigator not detected. Install: /plugin marketplace add alekspetrov/navigator && /plugin install navigator"

    if not latest:
        return "Could not check for updates. Try again later or check GitHub releases manually."

    if update_available:
        return f"Update recommended: v{current} → v{latest}. Run: /plugin update navigator"

    return f"You're on the latest version (v{current}). No update needed."


def main():
    """CLI entry point."""
    report = detect_version()

    # Output as JSON
    print(json.dumps(report, indent=2))

    # Exit with code
    # 0 = up to date
    # 1 = update available
    # 2 = error
    if report.get('error'):
        sys.exit(2)
    elif report.get('update_available'):
        sys.exit(1)
    else:
        sys.exit(0)


if __name__ == '__main__':
    main()
