#!/usr/bin/env python3
"""
Chromatic Configuration Generator

Generates Chromatic config files, updates Storybook configuration,
and adds package.json scripts for visual regression testing.

Usage:
    python chromatic_config_generator.py <project_root> [vr_tool]
"""

import json
import os
import re
import sys
from pathlib import Path
from typing import Dict, Optional


def generate_chromatic_config(project_info: Dict) -> str:
    """
    Generate chromatic.config.json content.

    Args:
        project_info: Project information (main_branch, etc.)

    Returns:
        JSON config as string
    """
    main_branch = project_info.get('main_branch', 'main')

    config = {
        "projectId": "<PROJECT_ID_PLACEHOLDER>",
        "buildScriptName": "build-storybook",
        "exitZeroOnChanges": True,
        "exitOnceUploaded": True,
        "onlyChanged": True,
        "externals": ["public/**"],
        "skip": "dependabot/**",
        "ignoreLastBuildOnBranch": main_branch
    }

    return json.dumps(config, indent=2)


def generate_percy_config(project_info: Dict) -> str:
    """
    Generate .percy.yml content for Percy.

    Args:
        project_info: Project information

    Returns:
        YAML config as string
    """
    config = """version: 2
static:
  build-dir: storybook-static
  clean-urls: false
snapshot:
  widths:
    - 375
    - 768
    - 1280
  min-height: 1024
  percy-css: ''
"""
    return config


def generate_backstop_config(project_info: Dict) -> str:
    """
    Generate backstop.config.js for BackstopJS.

    Args:
        project_info: Project information

    Returns:
        JS config as string
    """
    config = """module.exports = {
  id: 'backstop_default',
  viewports: [
    {
      label: 'phone',
      width: 375,
      height: 667
    },
    {
      label: 'tablet',
      width: 768,
      height: 1024
    },
    {
      label: 'desktop',
      width: 1280,
      height: 1024
    }
  ],
  scenarios: [],
  paths: {
    bitmaps_reference: 'backstop_data/bitmaps_reference',
    bitmaps_test: 'backstop_data/bitmaps_test',
    engine_scripts: 'backstop_data/engine_scripts',
    html_report: 'backstop_data/html_report',
    ci_report: 'backstop_data/ci_report'
  },
  report: ['browser'],
  engine: 'puppeteer',
  engineOptions: {
    args: ['--no-sandbox']
  },
  asyncCaptureLimit: 5,
  asyncCompareLimit: 50,
  debug: false,
  debugWindow: false
};
"""
    return config


def update_storybook_main_config(main_js_path: str, vr_tool: str = 'chromatic') -> str:
    """
    Update .storybook/main.js to include VR tool addon.

    Args:
        main_js_path: Path to main.js file
        vr_tool: VR tool name ('chromatic', 'percy', 'backstopjs')

    Returns:
        Updated main.js content
    """
    # Read existing config
    if not os.path.exists(main_js_path):
        # Generate new config if doesn't exist
        return generate_new_storybook_config(vr_tool)

    with open(main_js_path, 'r') as f:
        content = f.read()

    # Determine addon to add
    if vr_tool == 'chromatic':
        addon = '@chromatic-com/storybook'
    elif vr_tool == 'percy':
        addon = '@percy/storybook'
    else:
        return content  # BackstopJS doesn't need addon

    # Check if addon already exists
    if addon in content:
        return content  # Already configured

    # Find addons array and insert
    addons_pattern = r'addons:\s*\[(.*?)\]'
    match = re.search(addons_pattern, content, re.DOTALL)

    if match:
        existing_addons = match.group(1).strip()
        # Add new addon
        updated_addons = f"{existing_addons},\n    '{addon}'"
        updated_content = content.replace(match.group(0), f"addons: [\n    {updated_addons}\n  ]")
        return updated_content
    else:
        # No addons array found - append at end
        return content + f"\n// Added by Navigator visual-regression skill\nmodule.exports.addons.push('{addon}');\n"


def generate_new_storybook_config(vr_tool: str = 'chromatic') -> str:
    """
    Generate new .storybook/main.js from scratch.

    Args:
        vr_tool: VR tool name

    Returns:
        main.js content
    """
    addon = '@chromatic-com/storybook' if vr_tool == 'chromatic' else '@percy/storybook'

    config = f"""module.exports = {{
  stories: ['../src/**/*.stories.@(js|jsx|ts|tsx)'],
  addons: [
    '@storybook/addon-links',
    '@storybook/addon-essentials',
    '{addon}',
    '@storybook/addon-interactions',
  ],
  framework: {{
    name: '@storybook/react-vite',
    options: {{}},
  }},
}};
"""
    return config


def update_package_json_scripts(package_json_path: str, vr_tool: str = 'chromatic') -> Dict:
    """
    Add VR tool scripts to package.json.

    Args:
        package_json_path: Path to package.json
        vr_tool: VR tool name

    Returns:
        Updated package.json data
    """
    with open(package_json_path, 'r') as f:
        package_data = json.load(f)

    scripts = package_data.get('scripts', {})

    # Add VR tool scripts
    if vr_tool == 'chromatic':
        scripts['chromatic'] = 'npx chromatic'
        scripts['chromatic:ci'] = 'npx chromatic --exit-zero-on-changes'
    elif vr_tool == 'percy':
        scripts['percy'] = 'percy storybook storybook-static'
        scripts['percy:ci'] = 'percy storybook storybook-static --partial'
    elif vr_tool == 'backstopjs':
        scripts['backstop:reference'] = 'backstop reference'
        scripts['backstop:test'] = 'backstop test'
        scripts['backstop:approve'] = 'backstop approve'

    # Ensure build-storybook script exists
    if 'build-storybook' not in scripts:
        scripts['build-storybook'] = 'storybook build'

    package_data['scripts'] = scripts

    return package_data


def detect_main_branch(project_root: str) -> str:
    """
    Detect main branch name from git.

    Args:
        project_root: Project root directory

    Returns:
        Branch name ('main' or 'master')
    """
    git_head = Path(project_root) / '.git' / 'HEAD'

    if git_head.exists():
        with open(git_head, 'r') as f:
            content = f.read().strip()
            if 'refs/heads/main' in content:
                return 'main'
            elif 'refs/heads/master' in content:
                return 'master'

    return 'main'  # Default


def generate_configs(project_root: str, vr_tool: str = 'chromatic') -> Dict:
    """
    Generate all configuration files for VR setup.

    Args:
        project_root: Project root directory
        vr_tool: VR tool to configure

    Returns:
        Dict with file paths and contents
    """
    project_info = {
        'main_branch': detect_main_branch(project_root)
    }

    result = {
        'configs_generated': [],
        'configs_updated': [],
        'errors': []
    }

    # Generate tool-specific config
    if vr_tool == 'chromatic':
        config_path = os.path.join(project_root, 'chromatic.config.json')
        config_content = generate_chromatic_config(project_info)
        result['configs_generated'].append({
            'path': config_path,
            'content': config_content
        })

    elif vr_tool == 'percy':
        config_path = os.path.join(project_root, '.percy.yml')
        config_content = generate_percy_config(project_info)
        result['configs_generated'].append({
            'path': config_path,
            'content': config_content
        })

    elif vr_tool == 'backstopjs':
        config_path = os.path.join(project_root, 'backstop.config.js')
        config_content = generate_backstop_config(project_info)
        result['configs_generated'].append({
            'path': config_path,
            'content': config_content
        })

    # Update Storybook main.js
    storybook_dir = Path(project_root) / '.storybook'
    main_js_candidates = [
        storybook_dir / 'main.js',
        storybook_dir / 'main.ts'
    ]

    main_js_path = None
    for candidate in main_js_candidates:
        if candidate.exists():
            main_js_path = str(candidate)
            break

    if main_js_path:
        main_js_content = update_storybook_main_config(main_js_path, vr_tool)
        result['configs_updated'].append({
            'path': main_js_path,
            'content': main_js_content
        })
    elif storybook_dir.exists():
        # Create new main.js
        main_js_path = str(storybook_dir / 'main.js')
        main_js_content = generate_new_storybook_config(vr_tool)
        result['configs_generated'].append({
            'path': main_js_path,
            'content': main_js_content
        })

    # Update package.json
    package_json_path = os.path.join(project_root, 'package.json')
    if os.path.exists(package_json_path):
        updated_package = update_package_json_scripts(package_json_path, vr_tool)
        result['configs_updated'].append({
            'path': package_json_path,
            'content': json.dumps(updated_package, indent=2)
        })

    return result


def main():
    """CLI entry point."""
    if len(sys.argv) < 2:
        print("Usage: python chromatic_config_generator.py <project_root> [vr_tool]", file=sys.stderr)
        sys.exit(1)

    project_root = sys.argv[1]
    vr_tool = sys.argv[2] if len(sys.argv) > 2 else 'chromatic'

    if vr_tool not in ['chromatic', 'percy', 'backstopjs']:
        print(f"Unsupported VR tool: {vr_tool}. Use: chromatic, percy, or backstopjs", file=sys.stderr)
        sys.exit(1)

    result = generate_configs(project_root, vr_tool)

    # Output as JSON
    print(json.dumps(result, indent=2))


if __name__ == '__main__':
    main()
