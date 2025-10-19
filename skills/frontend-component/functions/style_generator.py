#!/usr/bin/env python3
"""
Generate style file (CSS Modules or Styled Components).

Creates scoped styles for React components.
"""

import sys
import argparse
import os

def read_template(template_path: str) -> str:
    """Read template file content."""
    try:
        with open(template_path, 'r') as f:
            return f.read()
    except FileNotFoundError:
        raise FileNotFoundError(f"Template file not found: {template_path}")

def generate_style(name: str, approach: str, template_content: str) -> str:
    """
    Generate style code by substituting placeholders in template.

    Args:
        name: Component name (PascalCase)
        approach: Styling approach (css-modules, styled-components, tailwind)
        template_content: Template file content

    Returns:
        str: Generated style code
    """
    # Convert PascalCase to kebab-case
    kebab_name = ''.join(['-' + c.lower() if c.isupper() else c for c in name]).lstrip('-')

    # Perform substitutions
    substitutions = {
        '${COMPONENT_NAME}': name,
        '${COMPONENT_NAME_KEBAB}': kebab_name,
        '${BASE_STYLES}': """  display: flex;
  flex-direction: column;
  gap: 1rem;""",
    }

    result = template_content
    for placeholder, value in substitutions.items():
        result = result.replace(placeholder, value)

    return result

def main():
    parser = argparse.ArgumentParser(description='Generate React component style file')
    parser.add_argument('--name', required=True, help='Component name (PascalCase)')
    parser.add_argument('--approach', default='css-modules', choices=['css-modules', 'styled-components', 'tailwind'], help='Styling approach')
    parser.add_argument('--template', required=True, help='Style template file path')
    parser.add_argument('--output', help='Output file path (optional, prints to stdout if not provided)')

    args = parser.parse_args()

    try:
        # Read template
        template_content = read_template(args.template)

        # Generate style
        style_code = generate_style(
            args.name,
            args.approach,
            template_content
        )

        # Output
        if args.output:
            os.makedirs(os.path.dirname(args.output), exist_ok=True)
            with open(args.output, 'w') as f:
                f.write(style_code)
            print(f"✅ Style file generated: {args.output}")
        else:
            print(style_code)

        sys.exit(0)
    except Exception as e:
        print(f"❌ Error: {e}", file=sys.stderr)
        sys.exit(1)

if __name__ == '__main__':
    main()
