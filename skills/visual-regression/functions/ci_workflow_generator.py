#!/usr/bin/env python3
"""
CI/CD Workflow Generator for Visual Regression

Generates GitHub Actions, GitLab CI, and CircleCI workflows for Chromatic/Percy/BackstopJS.

Usage:
    python ci_workflow_generator.py <project_root> <ci_platform> <vr_tool>
"""

import json
import os
import sys
from pathlib import Path
from typing import Dict


def detect_node_version(project_root: str) -> str:
    """
    Detect Node.js version from .nvmrc or package.json.

    Args:
        project_root: Project root directory

    Returns:
        Node version string (default: '20')
    """
    # Check .nvmrc
    nvmrc = Path(project_root) / '.nvmrc'
    if nvmrc.exists():
        with open(nvmrc, 'r') as f:
            return f.read().strip()

    # Check package.json engines.node
    package_json = Path(project_root) / 'package.json'
    if package_json.exists():
        with open(package_json, 'r') as f:
            try:
                data = json.load(f)
                node_version = data.get('engines', {}).get('node')
                if node_version:
                    # Extract version number (handle ">=18.0.0" format)
                    import re
                    match = re.search(r'\d+', node_version)
                    if match:
                        return match.group(0)
            except json.JSONDecodeError:
                pass

    return '20'  # Default


def detect_package_manager(project_root: str) -> str:
    """
    Detect package manager from lock files.

    Args:
        project_root: Project root directory

    Returns:
        Package manager name ('npm', 'yarn', 'pnpm')
    """
    root = Path(project_root)

    if (root / 'pnpm-lock.yaml').exists():
        return 'pnpm'
    elif (root / 'yarn.lock').exists():
        return 'yarn'
    else:
        return 'npm'


def get_install_command(package_manager: str) -> str:
    """Get install command for package manager."""
    commands = {
        'npm': 'npm ci',
        'yarn': 'yarn install --frozen-lockfile',
        'pnpm': 'pnpm install --frozen-lockfile'
    }
    return commands.get(package_manager, 'npm ci')


def detect_branches(project_root: str) -> list:
    """
    Detect main branches from git config.

    Args:
        project_root: Project root directory

    Returns:
        List of branch names
    """
    git_head = Path(project_root) / '.git' / 'HEAD'

    if git_head.exists():
        with open(git_head, 'r') as f:
            content = f.read().strip()
            if 'refs/heads/main' in content:
                return ['main', 'develop']
            elif 'refs/heads/master' in content:
                return ['master', 'develop']

    return ['main', 'develop']


def generate_github_workflow_chromatic(project_info: Dict) -> str:
    """
    Generate GitHub Actions workflow for Chromatic.

    Args:
        project_info: Project information

    Returns:
        YAML workflow content
    """
    node_version = project_info.get('node_version', '20')
    package_manager = project_info.get('package_manager', 'npm')
    install_command = get_install_command(package_manager)
    branches = project_info.get('branches', ['main', 'develop'])

    workflow = f"""name: Visual Regression Tests

on:
  push:
    branches: {json.dumps(branches)}
  pull_request:
    branches: ['main']

jobs:
  chromatic:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
        with:
          fetch-depth: 0  # Required for Chromatic

      - name: Setup Node.js
        uses: actions/setup-node@v4
        with:
          node-version: '{node_version}'
          cache: '{package_manager}'

      - name: Install dependencies
        run: {install_command}

      - name: Run Chromatic
        uses: chromaui/action@latest
        with:
          projectToken: ${{{{ secrets.CHROMATIC_PROJECT_TOKEN }}}}
          exitZeroOnChanges: true
          onlyChanged: true
          autoAcceptChanges: 'main'  # Auto-accept on main branch
"""
    return workflow


def generate_github_workflow_percy(project_info: Dict) -> str:
    """
    Generate GitHub Actions workflow for Percy.

    Args:
        project_info: Project information

    Returns:
        YAML workflow content
    """
    node_version = project_info.get('node_version', '20')
    package_manager = project_info.get('package_manager', 'npm')
    install_command = get_install_command(package_manager)
    branches = project_info.get('branches', ['main', 'develop'])

    workflow = f"""name: Visual Regression Tests

on:
  push:
    branches: {json.dumps(branches)}
  pull_request:
    branches: ['main']

jobs:
  percy:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4

      - name: Setup Node.js
        uses: actions/setup-node@v4
        with:
          node-version: '{node_version}'
          cache: '{package_manager}'

      - name: Install dependencies
        run: {install_command}

      - name: Build Storybook
        run: npm run build-storybook

      - name: Run Percy
        run: npx percy storybook storybook-static
        env:
          PERCY_TOKEN: ${{{{ secrets.PERCY_TOKEN }}}}
"""
    return workflow


def generate_github_workflow_backstop(project_info: Dict) -> str:
    """
    Generate GitHub Actions workflow for BackstopJS.

    Args:
        project_info: Project information

    Returns:
        YAML workflow content
    """
    node_version = project_info.get('node_version', '20')
    package_manager = project_info.get('package_manager', 'npm')
    install_command = get_install_command(package_manager)
    branches = project_info.get('branches', ['main', 'develop'])

    workflow = f"""name: Visual Regression Tests

on:
  push:
    branches: {json.dumps(branches)}
  pull_request:
    branches: ['main']

jobs:
  backstop:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4

      - name: Setup Node.js
        uses: actions/setup-node@v4
        with:
          node-version: '{node_version}'
          cache: '{package_manager}'

      - name: Install dependencies
        run: {install_command}

      - name: Run BackstopJS
        run: npm run backstop:test

      - name: Upload test results
        if: failure()
        uses: actions/upload-artifact@v3
        with:
          name: backstop-results
          path: backstop_data/
"""
    return workflow


def generate_gitlab_ci_chromatic(project_info: Dict) -> str:
    """
    Generate GitLab CI job for Chromatic.

    Args:
        project_info: Project information

    Returns:
        YAML job content
    """
    node_version = project_info.get('node_version', '20')
    install_command = get_install_command(project_info.get('package_manager', 'npm'))

    job = f"""# Add to .gitlab-ci.yml

chromatic:
  stage: test
  image: node:{node_version}
  cache:
    paths:
      - node_modules/
  script:
    - {install_command}
    - npx chromatic --exit-zero-on-changes --only-changed
  variables:
    CHROMATIC_PROJECT_TOKEN: $CHROMATIC_PROJECT_TOKEN
  only:
    - main
    - develop
    - merge_requests
"""
    return job


def generate_gitlab_ci_percy(project_info: Dict) -> str:
    """
    Generate GitLab CI job for Percy.

    Args:
        project_info: Project information

    Returns:
        YAML job content
    """
    node_version = project_info.get('node_version', '20')
    install_command = get_install_command(project_info.get('package_manager', 'npm'))

    job = f"""# Add to .gitlab-ci.yml

percy:
  stage: test
  image: node:{node_version}
  cache:
    paths:
      - node_modules/
  script:
    - {install_command}
    - npm run build-storybook
    - npx percy storybook storybook-static
  variables:
    PERCY_TOKEN: $PERCY_TOKEN
  only:
    - main
    - develop
    - merge_requests
"""
    return job


def generate_circleci_config_chromatic(project_info: Dict) -> str:
    """
    Generate CircleCI job for Chromatic.

    Args:
        project_info: Project information

    Returns:
        YAML job content
    """
    node_version = project_info.get('node_version', '20')
    install_command = get_install_command(project_info.get('package_manager', 'npm'))

    config = f"""# Add to .circleci/config.yml

version: 2.1

executors:
  node:
    docker:
      - image: cimg/node:{node_version}

jobs:
  chromatic:
    executor: node
    steps:
      - checkout
      - restore_cache:
          keys:
            - v1-dependencies-{{{{ checksum "package.json" }}}}
      - run: {install_command}
      - save_cache:
          paths:
            - node_modules
          key: v1-dependencies-{{{{ checksum "package.json" }}}}
      - run:
          name: Run Chromatic
          command: npx chromatic --exit-zero-on-changes --only-changed
          environment:
            CHROMATIC_PROJECT_TOKEN: $CHROMATIC_PROJECT_TOKEN

workflows:
  version: 2
  test:
    jobs:
      - chromatic
"""
    return config


def generate_workflow(project_root: str, ci_platform: str, vr_tool: str) -> Dict:
    """
    Generate CI/CD workflow for specified platform and VR tool.

    Args:
        project_root: Project root directory
        ci_platform: CI platform ('github', 'gitlab', 'circleci')
        vr_tool: VR tool ('chromatic', 'percy', 'backstopjs')

    Returns:
        Dict with workflow path and content
    """
    # Gather project info
    project_info = {
        'node_version': detect_node_version(project_root),
        'package_manager': detect_package_manager(project_root),
        'branches': detect_branches(project_root)
    }

    result = {
        'platform': ci_platform,
        'vr_tool': vr_tool,
        'workflow_path': None,
        'workflow_content': None,
        'instructions': None
    }

    # Generate workflow based on platform and tool
    if ci_platform == 'github':
        workflow_dir = Path(project_root) / '.github' / 'workflows'
        workflow_file = 'chromatic.yml' if vr_tool == 'chromatic' else f'{vr_tool}.yml'
        result['workflow_path'] = str(workflow_dir / workflow_file)

        if vr_tool == 'chromatic':
            result['workflow_content'] = generate_github_workflow_chromatic(project_info)
        elif vr_tool == 'percy':
            result['workflow_content'] = generate_github_workflow_percy(project_info)
        elif vr_tool == 'backstopjs':
            result['workflow_content'] = generate_github_workflow_backstop(project_info)

        result['instructions'] = f"""
GitHub Actions workflow created: {result['workflow_path']}

Next steps:
1. Add secret: Repository Settings → Secrets → Actions
2. Create secret: CHROMATIC_PROJECT_TOKEN (or PERCY_TOKEN)
3. Commit and push this file
4. Workflow will run automatically on push/PR
"""

    elif ci_platform == 'gitlab':
        result['workflow_path'] = str(Path(project_root) / '.gitlab-ci.yml')

        if vr_tool == 'chromatic':
            result['workflow_content'] = generate_gitlab_ci_chromatic(project_info)
        elif vr_tool == 'percy':
            result['workflow_content'] = generate_gitlab_ci_percy(project_info)

        result['instructions'] = """
GitLab CI job generated. Add to your .gitlab-ci.yml file.

Next steps:
1. Add variable: Project Settings → CI/CD → Variables
2. Create variable: CHROMATIC_PROJECT_TOKEN (or PERCY_TOKEN)
3. Commit and push .gitlab-ci.yml
4. Pipeline will run automatically
"""

    elif ci_platform == 'circleci':
        result['workflow_path'] = str(Path(project_root) / '.circleci' / 'config.yml')

        if vr_tool == 'chromatic':
            result['workflow_content'] = generate_circleci_config_chromatic(project_info)

        result['instructions'] = """
CircleCI job generated. Add to your .circleci/config.yml file.

Next steps:
1. Add environment variable in CircleCI project settings
2. Variable name: CHROMATIC_PROJECT_TOKEN
3. Commit and push config.yml
4. Build will run automatically
"""

    return result


def main():
    """CLI entry point."""
    if len(sys.argv) < 4:
        print("Usage: python ci_workflow_generator.py <project_root> <ci_platform> <vr_tool>", file=sys.stderr)
        print("  ci_platform: github, gitlab, circleci", file=sys.stderr)
        print("  vr_tool: chromatic, percy, backstopjs", file=sys.stderr)
        sys.exit(1)

    project_root = sys.argv[1]
    ci_platform = sys.argv[2].lower()
    vr_tool = sys.argv[3].lower()

    if ci_platform not in ['github', 'gitlab', 'circleci']:
        print(f"Unsupported CI platform: {ci_platform}", file=sys.stderr)
        sys.exit(1)

    if vr_tool not in ['chromatic', 'percy', 'backstopjs']:
        print(f"Unsupported VR tool: {vr_tool}", file=sys.stderr)
        sys.exit(1)

    result = generate_workflow(project_root, ci_platform, vr_tool)

    # Output as JSON
    print(json.dumps(result, indent=2))


if __name__ == '__main__':
    main()
