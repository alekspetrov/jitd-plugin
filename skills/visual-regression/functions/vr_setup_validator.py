#!/usr/bin/env python3
"""
Visual Regression Setup Validator

Detects existing Storybook setup, VR tools, CI platform, and validates component paths.
Returns comprehensive validation report to guide skill execution.

Usage:
    python vr_setup_validator.py <project_root> [component_path]
"""

import json
import os
import sys
from pathlib import Path
from typing import Dict, List, Optional


def detect_framework(project_root: str) -> Optional[str]:
    """
    Detect frontend framework from package.json dependencies.

    Args:
        project_root: Path to project root directory

    Returns:
        Framework name ('react', 'vue', 'svelte') or None
    """
    package_json_path = Path(project_root) / 'package.json'

    if not package_json_path.exists():
        return None

    try:
        with open(package_json_path, 'r') as f:
            package_data = json.load(f)

        dependencies = {
            **package_data.get('dependencies', {}),
            **package_data.get('devDependencies', {})
        }

        if 'react' in dependencies:
            return 'react'
        elif 'vue' in dependencies:
            return 'vue'
        elif 'svelte' in dependencies:
            return 'svelte'

        return None
    except (json.JSONDecodeError, FileNotFoundError):
        return None


def detect_storybook_config(project_root: str) -> Dict:
    """
    Detect Storybook version and configuration.

    Args:
        project_root: Path to project root directory

    Returns:
        Dict with version, addons, framework, and config path
    """
    storybook_dir = Path(project_root) / '.storybook'
    package_json_path = Path(project_root) / 'package.json'

    result = {
        'installed': False,
        'version': None,
        'config_path': None,
        'main_js_path': None,
        'addons': [],
        'framework': None
    }

    # Check if .storybook directory exists
    if not storybook_dir.exists():
        return result

    result['installed'] = True
    result['config_path'] = str(storybook_dir)

    # Check for main.js or main.ts
    main_js = storybook_dir / 'main.js'
    main_ts = storybook_dir / 'main.ts'

    if main_js.exists():
        result['main_js_path'] = str(main_js)
    elif main_ts.exists():
        result['main_js_path'] = str(main_ts)

    # Extract version from package.json
    if package_json_path.exists():
        try:
            with open(package_json_path, 'r') as f:
                package_data = json.load(f)

            dependencies = {
                **package_data.get('dependencies', {}),
                **package_data.get('devDependencies', {})
            }

            # Find Storybook version
            for dep in dependencies:
                if dep.startswith('@storybook/'):
                    result['version'] = dependencies[dep].replace('^', '').replace('~', '')
                    break

            # Extract addons from dependencies
            result['addons'] = [
                dep for dep in dependencies.keys()
                if dep.startswith('@storybook/addon-') or dep == '@chromatic-com/storybook'
            ]
        except (json.JSONDecodeError, FileNotFoundError):
            pass

    # Try to parse main.js for framework
    if result['main_js_path']:
        try:
            with open(result['main_js_path'], 'r') as f:
                content = f.read()
                if '@storybook/react' in content:
                    result['framework'] = 'react'
                elif '@storybook/vue' in content:
                    result['framework'] = 'vue'
                elif '@storybook/svelte' in content:
                    result['framework'] = 'svelte'
        except FileNotFoundError:
            pass

    return result


def detect_vr_tool(project_root: str) -> Optional[str]:
    """
    Detect existing visual regression tool from package.json.

    Args:
        project_root: Path to project root directory

    Returns:
        Tool name ('chromatic', 'percy', 'backstopjs') or None
    """
    package_json_path = Path(project_root) / 'package.json'

    if not package_json_path.exists():
        return None

    try:
        with open(package_json_path, 'r') as f:
            package_data = json.load(f)

        dependencies = {
            **package_data.get('dependencies', {}),
            **package_data.get('devDependencies', {})
        }

        if 'chromatic' in dependencies or '@chromatic-com/storybook' in dependencies:
            return 'chromatic'
        elif '@percy/cli' in dependencies or '@percy/storybook' in dependencies:
            return 'percy'
        elif 'backstopjs' in dependencies:
            return 'backstopjs'

        return None
    except (json.JSONDecodeError, FileNotFoundError):
        return None


def detect_ci_platform(project_root: str) -> Optional[str]:
    """
    Detect CI/CD platform from existing configuration files.

    Args:
        project_root: Path to project root directory

    Returns:
        Platform name ('github', 'gitlab', 'circleci', 'bitbucket') or None
    """
    root = Path(project_root)

    # GitHub Actions
    if (root / '.github' / 'workflows').exists():
        return 'github'

    # GitLab CI
    if (root / '.gitlab-ci.yml').exists():
        return 'gitlab'

    # CircleCI
    if (root / '.circleci' / 'config.yml').exists():
        return 'circleci'

    # Bitbucket Pipelines
    if (root / 'bitbucket-pipelines.yml').exists():
        return 'bitbucket'

    return None


def validate_component_path(component_path: str, project_root: str = '.') -> Dict:
    """
    Validate component file exists and extract basic information.

    Args:
        component_path: Path to component file (relative or absolute)
        project_root: Project root directory

    Returns:
        Dict with validation status and component info
    """
    # Handle relative paths
    if not os.path.isabs(component_path):
        component_path = os.path.join(project_root, component_path)

    component_file = Path(component_path)

    result = {
        'valid': False,
        'path': component_path,
        'name': None,
        'extension': None,
        'directory': None,
        'error': None
    }

    # Check if file exists
    if not component_file.exists():
        result['error'] = f"Component file not found: {component_path}"
        return result

    # Check if it's a file (not directory)
    if not component_file.is_file():
        result['error'] = f"Path is not a file: {component_path}"
        return result

    # Validate extension
    valid_extensions = ['.tsx', '.ts', '.jsx', '.js', '.vue', '.svelte']
    if component_file.suffix not in valid_extensions:
        result['error'] = f"Invalid file extension. Expected one of: {', '.join(valid_extensions)}"
        return result

    # Extract component name (filename without extension)
    result['name'] = component_file.stem
    result['extension'] = component_file.suffix
    result['directory'] = str(component_file.parent)
    result['valid'] = True

    return result


def check_dependencies(project_root: str, vr_tool: Optional[str] = 'chromatic') -> Dict:
    """
    Check which required dependencies are installed.

    Args:
        project_root: Path to project root directory
        vr_tool: VR tool to check for ('chromatic', 'percy', 'backstopjs')

    Returns:
        Dict with installed and missing dependencies
    """
    package_json_path = Path(project_root) / 'package.json'

    result = {
        'installed': [],
        'missing': []
    }

    if not package_json_path.exists():
        result['missing'] = ['package.json not found']
        return result

    try:
        with open(package_json_path, 'r') as f:
            package_data = json.load(f)

        dependencies = {
            **package_data.get('dependencies', {}),
            **package_data.get('devDependencies', {})
        }

        # Core Storybook dependencies
        required_deps = [
            '@storybook/addon-essentials',
            '@storybook/addon-interactions',
        ]

        # Add VR tool specific dependencies
        if vr_tool == 'chromatic':
            required_deps.extend(['chromatic', '@chromatic-com/storybook'])
        elif vr_tool == 'percy':
            required_deps.extend(['@percy/cli', '@percy/storybook'])
        elif vr_tool == 'backstopjs':
            required_deps.append('backstopjs')

        # Check each dependency
        for dep in required_deps:
            if dep in dependencies:
                result['installed'].append(dep)
            else:
                result['missing'].append(dep)

    except (json.JSONDecodeError, FileNotFoundError):
        result['missing'] = ['Error reading package.json']

    return result


def get_package_manager(project_root: str) -> str:
    """
    Detect package manager from lock files.

    Args:
        project_root: Path to project root directory

    Returns:
        Package manager name ('npm', 'yarn', 'pnpm')
    """
    root = Path(project_root)

    if (root / 'pnpm-lock.yaml').exists():
        return 'pnpm'
    elif (root / 'yarn.lock').exists():
        return 'yarn'
    else:
        return 'npm'  # Default to npm


def validate_setup(project_root: str, component_path: Optional[str] = None) -> Dict:
    """
    Comprehensive validation of VR setup requirements.

    Args:
        project_root: Path to project root directory
        component_path: Optional path to component file

    Returns:
        Complete validation report
    """
    report = {
        'project_root': project_root,
        'framework': detect_framework(project_root),
        'storybook': detect_storybook_config(project_root),
        'vr_tool': detect_vr_tool(project_root),
        'ci_platform': detect_ci_platform(project_root),
        'package_manager': get_package_manager(project_root),
        'component': None,
        'dependencies': None,
        'ready': False,
        'warnings': [],
        'errors': []
    }

    # Validate component if path provided
    if component_path:
        report['component'] = validate_component_path(component_path, project_root)
        if not report['component']['valid']:
            report['errors'].append(report['component']['error'])

    # Check framework
    if not report['framework']:
        report['errors'].append('Framework not detected. Ensure React, Vue, or Svelte is installed.')

    # Check Storybook
    if not report['storybook']['installed']:
        report['errors'].append('Storybook not installed. Run: npx storybook init')

    # Determine VR tool (use detected or default to Chromatic)
    vr_tool = report['vr_tool'] or 'chromatic'
    report['dependencies'] = check_dependencies(project_root, vr_tool)

    # Add warnings for missing dependencies
    if report['dependencies']['missing']:
        report['warnings'].append(
            f"Missing dependencies: {', '.join(report['dependencies']['missing'])}"
        )

    # Determine if ready to proceed
    report['ready'] = (
        report['framework'] is not None and
        report['storybook']['installed'] and
        len(report['errors']) == 0
    )

    return report


def main():
    """CLI entry point."""
    if len(sys.argv) < 2:
        print("Usage: python vr_setup_validator.py <project_root> [component_path]", file=sys.stderr)
        sys.exit(1)

    project_root = sys.argv[1]
    component_path = sys.argv[2] if len(sys.argv) > 2 else None

    report = validate_setup(project_root, component_path)

    # Output as JSON
    print(json.dumps(report, indent=2))

    # Exit with error code if not ready
    sys.exit(0 if report['ready'] else 1)


if __name__ == '__main__':
    main()
