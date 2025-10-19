#!/usr/bin/env python3
"""
Validate component naming conventions.

Ensures component names follow PascalCase, are descriptive, and avoid reserved words.
"""

import sys
import re
import argparse

# Reserved component names that should be avoided
RESERVED_WORDS = {
    'Component', 'Element', 'Node', 'React', 'ReactNode', 'Fragment',
    'Props', 'State', 'Context', 'Provider', 'Consumer', 'Children',
    'Ref', 'Key', 'Type', 'Class', 'Function', 'Object', 'Array',
    'String', 'Number', 'Boolean', 'Symbol', 'Null', 'Undefined'
}

def is_pascal_case(name):
    """
    Check if name is in PascalCase format.

    Args:
        name: String to validate

    Returns:
        bool: True if PascalCase, False otherwise
    """
    # PascalCase: starts with uppercase, contains only alphanumeric
    pattern = r'^[A-Z][a-zA-Z0-9]*$'
    return bool(re.match(pattern, name))

def validate_component_name(name):
    """
    Validate component name against conventions.

    Args:
        name: Component name to validate

    Returns:
        tuple: (is_valid: bool, error_message: str or None)
    """
    # Check length
    if len(name) < 2:
        return False, "Component name must be at least 2 characters long"

    # Check for special characters
    if not name.replace('_', '').isalnum():
        return False, "Component name should only contain alphanumeric characters"

    # Check PascalCase
    if not is_pascal_case(name):
        return False, f"Component name '{name}' must be in PascalCase (e.g., UserProfile, TodoList)"

    # Check reserved words
    if name in RESERVED_WORDS:
        return False, f"'{name}' is a reserved word. Choose a more descriptive name."

    # Check descriptiveness (not too generic)
    if len(name) < 4:
        return False, f"Component name '{name}' is too short. Use a more descriptive name (e.g., UserCard, not UC)"

    # Check doesn't start with common anti-patterns
    anti_patterns = ['My', 'The', 'New', 'Test']
    if any(name.startswith(pattern) for pattern in anti_patterns):
        return False, f"Avoid starting component names with '{name[:3]}...'. Be more specific about what it does."

    return True, None

def suggest_valid_name(name):
    """
    Suggest a valid component name if the provided one is invalid.

    Args:
        name: Invalid component name

    Returns:
        str: Suggested valid name
    """
    # Convert to PascalCase
    suggested = ''.join(word.capitalize() for word in re.split(r'[-_\s]+', name))

    # Remove special characters
    suggested = re.sub(r'[^a-zA-Z0-9]', '', suggested)

    # Ensure starts with uppercase
    if suggested and not suggested[0].isupper():
        suggested = suggested.capitalize()

    return suggested if suggested else "MyComponent"

def main():
    parser = argparse.ArgumentParser(description='Validate React component naming conventions')
    parser.add_argument('--name', required=True, help='Component name to validate')
    parser.add_argument('--suggest', action='store_true', help='Suggest a valid name if invalid')

    args = parser.parse_args()

    is_valid, error = validate_component_name(args.name)

    if is_valid:
        print(f"✅ '{args.name}' is a valid component name")
        sys.exit(0)
    else:
        print(f"❌ Invalid component name: {error}", file=sys.stderr)

        if args.suggest:
            suggested = suggest_valid_name(args.name)
            print(f"💡 Suggested name: {suggested}", file=sys.stderr)

        sys.exit(1)

if __name__ == '__main__':
    main()
