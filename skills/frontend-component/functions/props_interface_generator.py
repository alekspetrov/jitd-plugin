#!/usr/bin/env python3
"""
Generate TypeScript props interface from user input.

Converts simple prop specifications into proper TypeScript interface definitions.
"""

import sys
import argparse
from typing import List, Tuple

# Type mapping from simple names to TypeScript types
TYPE_MAPPING = {
    'string': 'string',
    'str': 'string',
    'number': 'number',
    'num': 'number',
    'int': 'number',
    'boolean': 'boolean',
    'bool': 'boolean',
    'function': '() => void',
    'func': '() => void',
    'callback': '() => void',
    'array': 'any[]',
    'arr': 'any[]',
    'object': 'Record<string, any>',
    'obj': 'Record<string, any>',
    'react-node': 'React.ReactNode',
    'node': 'React.ReactNode',
    'children': 'React.ReactNode',
    'element': 'React.ReactElement',
    'style': 'React.CSSProperties',
    'class': 'string',
    'classname': 'string',
}

def parse_prop_spec(prop_spec: str) -> Tuple[str, str, bool]:
    """
    Parse a single prop specification.

    Format: "propName:type" or "propName:type:optional"

    Args:
        prop_spec: Prop specification string

    Returns:
        tuple: (prop_name, ts_type, is_optional)
    """
    parts = prop_spec.strip().split(':')

    if len(parts) < 2:
        raise ValueError(f"Invalid prop specification: '{prop_spec}'. Expected format: 'propName:type' or 'propName:type:optional'")

    prop_name = parts[0].strip()
    type_name = parts[1].strip().lower()
    is_optional = len(parts) > 2 and parts[2].strip().lower() in ('optional', 'opt', '?', 'true')

    # Map to TypeScript type
    ts_type = TYPE_MAPPING.get(type_name, type_name)

    return prop_name, ts_type, is_optional

def generate_props_interface(name: str, props: List[str], include_common: bool = True) -> str:
    """
    Generate TypeScript props interface.

    Args:
        name: Component name (will become {name}Props)
        props: List of prop specifications
        include_common: Whether to include common props (children, className, etc.)

    Returns:
        str: TypeScript interface definition
    """
    interface_name = f"{name}Props"
    lines = [f"interface {interface_name} {{"]

    # Add custom props
    for prop_spec in props:
        if not prop_spec.strip():
            continue

        prop_name, ts_type, is_optional = parse_prop_spec(prop_spec)
        optional_marker = '?' if is_optional else ''
        lines.append(f"  {prop_name}{optional_marker}: {ts_type};")

    # Add common props if requested
    if include_common:
        # Only add children if not already specified
        if not any('children' in prop for prop in props):
            lines.append("  children?: React.ReactNode;")

        # Only add className if not already specified
        if not any('className' in prop or 'class' in prop.lower() for prop in props):
            lines.append("  className?: string;")

    lines.append("}")

    return '\n'.join(lines)

def main():
    parser = argparse.ArgumentParser(description='Generate TypeScript props interface')
    parser.add_argument('--name', required=True, help='Component name')
    parser.add_argument('--props', required=True, help='Comma-separated prop specifications (e.g., "userId:string,onUpdate:function,isActive:boolean:optional")')
    parser.add_argument('--no-common', action='store_true', help='Do not include common props (children, className)')

    args = parser.parse_args()

    # Parse prop specifications
    prop_specs = [p.strip() for p in args.props.split(',') if p.strip()]

    try:
        interface = generate_props_interface(
            args.name,
            prop_specs,
            include_common=not args.no_common
        )
        print(interface)
        sys.exit(0)
    except ValueError as e:
        print(f"❌ Error: {e}", file=sys.stderr)
        sys.exit(1)

if __name__ == '__main__':
    main()
