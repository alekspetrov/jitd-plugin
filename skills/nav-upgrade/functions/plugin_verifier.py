#!/usr/bin/env python3
"""
Navigator Plugin Verifier

Verifies that Navigator plugin update completed successfully.

Usage:
    python plugin_verifier.py --expected-version 3.3.0
"""

import argparse
import json
import os
import re
import subprocess
import sys
from pathlib import Path
from typing import Dict, List


def get_installed_version() -> str:
    """
    Get installed Navigator version from /plugin list.

    Returns:
        Version string or None
    """
    try:
        result = subprocess.run(
            ['claude', 'plugin', 'list'],
            capture_output=True,
            text=True,
            timeout=10
        )

        for line in result.stdout.split('\n'):
            if 'navigator' in line.lower():
                match = re.search(r'v?(\d+\.\d+\.\d+)', line)
                if match:
                    return match.group(1)

        return None
    except Exception:
        return None


def find_plugin_directory() -> Path:
    """
    Find Navigator plugin installation directory.

    Returns:
        Path to plugin directory or None
    """
    possible_paths = [
        Path.home() / '.config' / 'claude' / 'plugins' / 'navigator',
        Path.home() / '.claude' / 'plugins' / 'navigator',
        Path.home() / 'Library' / 'Application Support' / 'Claude' / 'plugins' / 'navigator',
    ]

    for path in possible_paths:
        if path.exists() and path.is_dir():
            return path

    return None


def verify_skills_exist(plugin_dir: Path, expected_skills: List[str]) -> Dict:
    """
    Verify that expected skills exist in plugin directory.

    Args:
        plugin_dir: Path to plugin directory
        expected_skills: List of skill names to check

    Returns:
        Dict with verification results
    """
    skills_dir = plugin_dir / 'skills'

    if not skills_dir.exists():
        return {
            'success': False,
            'error': 'Skills directory not found'
        }

    results = {}
    for skill_name in expected_skills:
        skill_path = skills_dir / skill_name / 'SKILL.md'
        results[skill_name] = skill_path.exists()

    all_exist = all(results.values())

    return {
        'success': all_exist,
        'skills_checked': results,
        'missing_skills': [name for name, exists in results.items() if not exists]
    }


def verify_plugin_json(plugin_dir: Path, expected_skills: List[str]) -> Dict:
    """
    Verify that skills are registered in plugin.json.

    Args:
        plugin_dir: Path to plugin directory
        expected_skills: List of skill names to check

    Returns:
        Dict with verification results
    """
    plugin_json_path = plugin_dir / '.claude-plugin' / 'plugin.json'

    if not plugin_json_path.exists():
        return {
            'success': False,
            'error': 'plugin.json not found'
        }

    try:
        with open(plugin_json_path, 'r') as f:
            data = json.load(f)

        registered_skills = data.get('skills', [])

        # Check each expected skill
        results = {}
        for skill_name in expected_skills:
            skill_path = f'./skills/{skill_name}'
            results[skill_name] = skill_path in registered_skills

        all_registered = all(results.values())

        return {
            'success': all_registered,
            'skills_checked': results,
            'unregistered_skills': [name for name, registered in results.items() if not registered]
        }
    except (json.JSONDecodeError, FileNotFoundError) as e:
        return {
            'success': False,
            'error': str(e)
        }


def verify_update(expected_version: str, expected_new_skills: List[str] = None) -> Dict:
    """
    Comprehensive verification of Navigator plugin update.

    Args:
        expected_version: Expected version after update (e.g., "3.3.0")
        expected_new_skills: List of new skills expected in this version

    Returns:
        Complete verification report
    """
    report = {
        'expected_version': expected_version,
        'checks': {},
        'overall_success': False,
        'needs_restart': False
    }

    # Check 1: Version matches
    installed_version = get_installed_version()
    report['checks']['version'] = {
        'expected': expected_version,
        'actual': installed_version,
        'success': installed_version == expected_version
    }

    # Check 2: Plugin directory exists
    plugin_dir = find_plugin_directory()
    report['checks']['plugin_directory'] = {
        'success': plugin_dir is not None,
        'path': str(plugin_dir) if plugin_dir else None
    }

    if not plugin_dir:
        report['recommendation'] = 'Plugin directory not found. Reinstall Navigator.'
        return report

    # Check 3: New skills exist (if specified)
    if expected_new_skills:
        skills_check = verify_skills_exist(plugin_dir, expected_new_skills)
        report['checks']['skills_exist'] = skills_check

        # Check 4: Skills registered in plugin.json
        registration_check = verify_plugin_json(plugin_dir, expected_new_skills)
        report['checks']['skills_registered'] = registration_check

        # If skills exist but verification shows they're not accessible, needs restart
        if skills_check['success'] and not registration_check['success']:
            report['needs_restart'] = True

    # Overall success
    all_checks_passed = all(
        check.get('success', False)
        for check in report['checks'].values()
    )

    report['overall_success'] = all_checks_passed

    # Generate recommendation
    if all_checks_passed:
        report['recommendation'] = 'Update verified successfully!'
    elif report['needs_restart']:
        report['recommendation'] = 'Update completed. Restart Claude Code to reload skills.'
    else:
        failed_checks = [name for name, check in report['checks'].items() if not check.get('success')]
        report['recommendation'] = f"Verification failed: {', '.join(failed_checks)}"

    return report


def main():
    """CLI entry point."""
    parser = argparse.ArgumentParser(description='Verify Navigator plugin update')
    parser.add_argument('--expected-version', required=True, help='Expected version (e.g., 3.3.0)')
    parser.add_argument('--new-skills', nargs='*', help='New skills to verify', default=[])
    args = parser.parse_args()

    # Run verification
    report = verify_update(args.expected_version, args.new_skills or None)

    # Output as JSON
    print(json.dumps(report, indent=2))

    # Exit code
    if report['overall_success']:
        sys.exit(0)
    elif report['needs_restart']:
        sys.exit(2)  # Special exit code for restart needed
    else:
        sys.exit(1)


if __name__ == '__main__':
    main()
