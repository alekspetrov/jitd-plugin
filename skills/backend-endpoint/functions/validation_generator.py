#!/usr/bin/env python3
"""
Generate request validation schema.

Creates Zod/Joi/Yup validation schemas for API endpoints.
"""

import sys
import argparse

# Type mapping for different validation libraries
ZOD_TYPE_MAP = {
    'string': 'z.string()',
    'number': 'z.number()',
    'boolean': 'z.boolean()',
    'email': 'z.string().email()',
    'url': 'z.string().url()',
    'uuid': 'z.string().uuid()',
    'date': 'z.date()',
    'array': 'z.array(z.any())',
    'object': 'z.object({})',
}

def parse_field_spec(field_spec: str):
    """
    Parse field specification.

    Format: "fieldName:type:required" or "fieldName:type:optional"

    Args:
        field_spec: Field specification string

    Returns:
        tuple: (field_name, field_type, is_required)
    """
    parts = field_spec.strip().split(':')

    if len(parts) < 2:
        raise ValueError(f"Invalid field spec: '{field_spec}'. Expected format: 'name:type' or 'name:type:required'")

    field_name = parts[0].strip()
    field_type = parts[1].strip().lower()
    is_required = len(parts) < 3 or parts[2].strip().lower() not in ('optional', 'opt', '?', 'false')

    return field_name, field_type, is_required

def generate_zod_schema(resource: str, method: str, fields: list) -> str:
    """
    Generate Zod validation schema.

    Args:
        resource: Resource name (PascalCase)
        method: HTTP method
        fields: List of field specifications

    Returns:
        str: Zod schema code
    """
    schema_name = f"{method.lower()}{resource}Schema"
    type_name = f"{method.capitalize()}{resource}Input"

    lines = [
        "import { z } from 'zod';\n",
        f"export const {schema_name} = z.object({{",
    ]

    for field_spec in fields:
        if not field_spec.strip():
            continue

        field_name, field_type, is_required = parse_field_spec(field_spec)
        zod_type = ZOD_TYPE_MAP.get(field_type, 'z.any()')

        if not is_required:
            zod_type += '.optional()'

        lines.append(f"  {field_name}: {zod_type},")

    lines.append("});\n")
    lines.append(f"export type {type_name} = z.infer<typeof {schema_name}>;")

    return '\n'.join(lines)

def main():
    parser = argparse.ArgumentParser(description='Generate request validation schema')
    parser.add_argument('--resource', required=True, help='Resource name (PascalCase)')
    parser.add_argument('--method', required=True, help='HTTP method (GET, POST, etc.)')
    parser.add_argument('--fields', required=True, help='Comma-separated field specifications')
    parser.add_argument('--library', default='zod', choices=['zod', 'joi', 'yup'], help='Validation library')
    parser.add_argument('--output', help='Output file path (optional, prints to stdout if not provided)')

    args = parser.parse_args()

    # Parse field specifications
    field_specs = [f.strip() for f in args.fields.split(',') if f.strip()]

    try:
        if args.library == 'zod':
            schema_code = generate_zod_schema(args.resource, args.method, field_specs)
        else:
            print(f"❌ Library '{args.library}' not yet implemented. Use 'zod' for now.", file=sys.stderr)
            sys.exit(1)

        # Output
        if args.output:
            import os
            os.makedirs(os.path.dirname(args.output), exist_ok=True)
            with open(args.output, 'w') as f:
                f.write(schema_code)
            print(f"✅ Validation schema generated: {args.output}")
        else:
            print(schema_code)

        sys.exit(0)
    except ValueError as e:
        print(f"❌ Error: {e}", file=sys.stderr)
        sys.exit(1)

if __name__ == '__main__':
    main()
