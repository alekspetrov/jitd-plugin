#!/usr/bin/env python3
"""
Template customization for Navigator initialization.

Replaces placeholders in templates with project-specific values.
"""

import re
from datetime import datetime
from typing import Dict


def customize_template(template_content: str, project_info: Dict[str, str]) -> str:
    """
    Replace placeholders in template with project-specific values.

    Args:
        template_content: Template file content with placeholders
        project_info: Dictionary from project_detector.py

    Returns:
        Customized template content

    Placeholders:
        ${PROJECT_NAME} - Project name (capitalized)
        ${project_name} - Project name (lowercase)
        ${TECH_STACK} - Technology stack
        ${DATE} - Current date (YYYY-MM-DD)
        ${YEAR} - Current year
        ${DETECTED_FROM} - Source of detection
    """
    now = datetime.now()

    # Prepare replacement values
    project_name = project_info.get("name", "My Project")
    tech_stack = project_info.get("tech_stack", "Unknown")
    detected_from = project_info.get("detected_from", "manual")

    # Create title-cased version for display
    project_name_title = _title_case(project_name)

    replacements = {
        "${PROJECT_NAME}": project_name_title,
        "${project_name}": project_name.lower(),
        "${TECH_STACK}": tech_stack,
        "${DATE}": now.strftime("%Y-%m-%d"),
        "${YEAR}": str(now.year),
        "${DETECTED_FROM}": detected_from,
    }

    # Apply replacements
    result = template_content
    for placeholder, value in replacements.items():
        result = result.replace(placeholder, value)

    return result


def _title_case(text: str) -> str:
    """
    Convert kebab-case, snake_case, or camelCase to Title Case.

    Examples:
        my-saas-app -> My SaaS App
        user_management -> User Management
        myAwesomeProject -> My Awesome Project
    """
    # Replace separators with spaces
    text = re.sub(r'[-_]', ' ', text)

    # Add spaces before capitals in camelCase
    text = re.sub(r'([a-z])([A-Z])', r'\1 \2', text)

    # Title case
    return text.title()


def validate_customization(content: str) -> bool:
    """
    Check if template was properly customized (no placeholders remaining).

    Args:
        content: Template content after customization

    Returns:
        True if no placeholders found, False otherwise
    """
    placeholder_pattern = r'\$\{[A-Z_]+\}'
    return not bool(re.search(placeholder_pattern, content))


if __name__ == "__main__":
    # Test customization
    template = """
# ${PROJECT_NAME} - Development Documentation

**Project**: ${PROJECT_NAME}
**Tech Stack**: ${TECH_STACK}
**Last Updated**: ${DATE}

Detected from: ${DETECTED_FROM}
"""

    project_info = {
        "name": "my-saas-app",
        "tech_stack": "Next.js, TypeScript, Prisma",
        "detected_from": "package.json",
    }

    result = customize_template(template, project_info)
    print(result)
    print(f"\nValid: {validate_customization(result)}")
