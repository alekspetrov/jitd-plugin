#!/usr/bin/env python3
"""
Extract design tokens from Figma variables and convert to DTCG format.
Compares with existing tokens and generates diff summary.
"""

import json
import sys
import argparse
from typing import Dict, List, Any, Tuple


def normalize_token_name(figma_name: str) -> str:
    """
    Normalize Figma variable name to DTCG semantic naming.

    Examples:
        "Primary 500" → "color.primary.500"
        "Spacing MD" → "spacing.md"
        "Font Heading Large" → "typography.heading.large"

    Args:
        figma_name: Original Figma variable name

    Returns:
        Normalized DTCG token path
    """
    name = figma_name.strip()

    # Convert to lowercase and split
    parts = name.lower().replace('-', ' ').replace('_', ' ').split()

    # Detect token type from name
    if any(keyword in parts for keyword in ['color', 'colour']):
        token_type = 'color'
        parts = [p for p in parts if p not in ['color', 'colour']]
    elif any(keyword in parts for keyword in ['spacing', 'space', 'gap', 'padding', 'margin']):
        token_type = 'spacing'
        parts = [p for p in parts if p not in ['spacing', 'space', 'gap', 'padding', 'margin']]
    elif any(keyword in parts for keyword in ['font', 'typography', 'text']):
        token_type = 'typography'
        parts = [p for p in parts if p not in ['font', 'typography', 'text']]
    elif any(keyword in parts for keyword in ['radius', 'border']):
        token_type = 'radius'
        parts = [p for p in parts if p not in ['radius', 'border']]
    elif any(keyword in parts for keyword in ['shadow', 'elevation']):
        token_type = 'shadow'
        parts = [p for p in parts if p not in ['shadow', 'elevation']]
    else:
        # Infer from first part
        first_part = parts[0] if parts else ''
        if first_part in ['primary', 'secondary', 'success', 'error', 'warning', 'info']:
            token_type = 'color'
        elif first_part in ['xs', 'sm', 'md', 'lg', 'xl', '2xl', '3xl']:
            token_type = 'spacing'
        else:
            token_type = 'other'

    # Build token path
    if parts:
        return f"{token_type}.{'.'.join(parts)}"
    else:
        return token_type


def detect_token_type(name: str, value: Any) -> str:
    """
    Detect DTCG token type from name and value.

    Args:
        name: Token name
        value: Token value

    Returns:
        DTCG type string
    """
    name_lower = name.lower()

    # Check by name first
    if 'color' in name_lower or 'colour' in name_lower:
        return 'color'
    elif 'spacing' in name_lower or 'gap' in name_lower or 'padding' in name_lower or 'margin' in name_lower:
        return 'dimension'
    elif 'font' in name_lower or 'typography' in name_lower:
        if isinstance(value, dict):
            return 'typography'
        else:
            return 'fontFamily' if 'family' in name_lower else 'dimension'
    elif 'radius' in name_lower or 'border' in name_lower:
        return 'dimension'
    elif 'shadow' in name_lower or 'elevation' in name_lower:
        return 'shadow'
    elif 'duration' in name_lower or 'transition' in name_lower:
        return 'duration'
    elif 'opacity' in name_lower or 'alpha' in name_lower:
        return 'number'

    # Infer from value
    if isinstance(value, str):
        if value.startswith('#') or value.startswith('rgb'):
            return 'color'
        elif value.endswith('px') or value.endswith('rem') or value.endswith('em'):
            return 'dimension'
        elif value.endswith('ms') or value.endswith('s'):
            return 'duration'
    elif isinstance(value, (int, float)):
        return 'number'
    elif isinstance(value, dict):
        if 'fontFamily' in value or 'fontSize' in value:
            return 'typography'
        elif 'x' in value and 'y' in value:
            return 'shadow'

    return 'other'


def convert_to_dtcg(figma_variables: Dict[str, Any]) -> Dict[str, Any]:
    """
    Convert Figma variables to DTCG format.

    Args:
        figma_variables: Figma get_variable_defs response

    Returns:
        DTCG formatted tokens
    """
    dtcg_tokens = {}

    for var_name, var_data in figma_variables.items():
        # Extract value and type
        if isinstance(var_data, dict):
            value = var_data.get('$value') or var_data.get('value')
            var_type = var_data.get('$type') or var_data.get('type')
            description = var_data.get('$description') or var_data.get('description', '')
        else:
            value = var_data
            var_type = None
            description = ''

        # Detect type if not provided
        if not var_type:
            var_type = detect_token_type(var_name, value)

        # Normalize token name to DTCG path
        token_path = normalize_token_name(var_name)

        # Build nested structure
        path_parts = token_path.split('.')
        current = dtcg_tokens

        for i, part in enumerate(path_parts):
            if i == len(path_parts) - 1:
                # Last part - add token definition
                current[part] = {
                    '$value': value,
                    '$type': var_type
                }
                if description:
                    current[part]['$description'] = description
            else:
                # Intermediate path - create nested dict
                if part not in current:
                    current[part] = {}
                current = current[part]

    return dtcg_tokens


def generate_diff(new_tokens: Dict[str, Any],
                 existing_tokens: Dict[str, Any]) -> Dict[str, List[Dict[str, Any]]]:
    """
    Generate diff between new and existing tokens.

    Args:
        new_tokens: New tokens from Figma (DTCG format)
        existing_tokens: Existing tokens from design-tokens.json

    Returns:
        Diff summary with added, modified, removed, unchanged
    """
    diff = {
        'added': [],
        'modified': [],
        'removed': [],
        'unchanged': []
    }

    # Flatten tokens for comparison
    new_flat = flatten_tokens(new_tokens)
    existing_flat = flatten_tokens(existing_tokens)

    # Find added and modified
    for token_path, token_data in new_flat.items():
        if token_path not in existing_flat:
            diff['added'].append({
                'path': token_path,
                'value': token_data.get('$value'),
                'type': token_data.get('$type')
            })
        else:
            existing_value = existing_flat[token_path].get('$value')
            new_value = token_data.get('$value')

            if existing_value != new_value:
                diff['modified'].append({
                    'path': token_path,
                    'old_value': existing_value,
                    'new_value': new_value,
                    'type': token_data.get('$type')
                })
            else:
                diff['unchanged'].append({
                    'path': token_path,
                    'value': new_value
                })

    # Find removed
    for token_path, token_data in existing_flat.items():
        if token_path not in new_flat:
            diff['removed'].append({
                'path': token_path,
                'value': token_data.get('$value'),
                'type': token_data.get('$type')
            })

    return diff


def flatten_tokens(tokens: Dict[str, Any], prefix: str = '') -> Dict[str, Any]:
    """
    Flatten nested DTCG tokens to dot notation paths.

    Args:
        tokens: Nested DTCG token structure
        prefix: Current path prefix

    Returns:
        Flattened dictionary with dot notation keys
    """
    flat = {}

    for key, value in tokens.items():
        current_path = f"{prefix}.{key}" if prefix else key

        if isinstance(value, dict) and '$value' in value:
            # This is a token definition
            flat[current_path] = value
        elif isinstance(value, dict):
            # This is a nested group
            flat.update(flatten_tokens(value, current_path))

    return flat


def generate_summary(diff: Dict[str, List[Dict[str, Any]]]) -> Dict[str, Any]:
    """
    Generate summary statistics from diff.

    Args:
        diff: Token diff

    Returns:
        Summary statistics
    """
    total_new = len(diff['added']) + len(diff['unchanged'])
    total_existing = len(diff['modified']) + len(diff['removed']) + len(diff['unchanged'])

    return {
        'total_new_tokens': total_new,
        'total_existing_tokens': total_existing,
        'added_count': len(diff['added']),
        'modified_count': len(diff['modified']),
        'removed_count': len(diff['removed']),
        'unchanged_count': len(diff['unchanged']),
        'sync_status': 'in_sync' if len(diff['added']) == 0 and len(diff['modified']) == 0 and len(diff['removed']) == 0 else 'drift_detected',
        'drift_percentage': f"{((len(diff['modified']) + len(diff['removed'])) / max(total_existing, 1)) * 100:.1f}%"
    }


def extract_tokens(figma_variables: Dict[str, Any],
                  existing_tokens: Dict[str, Any] = None) -> Dict[str, Any]:
    """
    Main extraction function: convert Figma variables to DTCG and generate diff.

    Args:
        figma_variables: Figma get_variable_defs response
        existing_tokens: Current design-tokens.json (optional)

    Returns:
        Extraction results with DTCG tokens, diff, and summary
    """
    # Convert to DTCG format
    dtcg_tokens = convert_to_dtcg(figma_variables)

    # Generate diff if existing tokens provided
    if existing_tokens:
        diff = generate_diff(dtcg_tokens, existing_tokens)
        summary = generate_summary(diff)
    else:
        # No existing tokens - all are new
        flat = flatten_tokens(dtcg_tokens)
        diff = {
            'added': [
                {
                    'path': path,
                    'value': data.get('$value'),
                    'type': data.get('$type')
                }
                for path, data in flat.items()
            ],
            'modified': [],
            'removed': [],
            'unchanged': []
        }
        summary = {
            'total_new_tokens': len(flat),
            'total_existing_tokens': 0,
            'added_count': len(flat),
            'modified_count': 0,
            'removed_count': 0,
            'unchanged_count': 0,
            'sync_status': 'initial_extraction',
            'drift_percentage': '0.0%'
        }

    return {
        'dtcg_tokens': dtcg_tokens,
        'diff': diff,
        'summary': summary
    }


def main():
    parser = argparse.ArgumentParser(
        description='Extract design tokens from Figma and convert to DTCG format'
    )
    parser.add_argument(
        '--figma-variables',
        required=True,
        help='Path to JSON file with Figma variables (get_variable_defs response)'
    )
    parser.add_argument(
        '--existing-tokens',
        help='Path to existing design-tokens.json (optional)'
    )
    parser.add_argument(
        '--output',
        help='Output file path (default: stdout)'
    )
    parser.add_argument(
        '--format',
        choices=['full', 'tokens-only', 'diff-only'],
        default='full',
        help='Output format (default: full)'
    )

    args = parser.parse_args()

    # Load Figma variables
    with open(args.figma_variables, 'r') as f:
        figma_variables = json.load(f)

    # Load existing tokens if provided
    existing_tokens = None
    if args.existing_tokens:
        with open(args.existing_tokens, 'r') as f:
            existing_tokens = json.load(f)

    # Run extraction
    results = extract_tokens(figma_variables, existing_tokens)

    # Format output based on --format flag
    if args.format == 'tokens-only':
        output = results['dtcg_tokens']
    elif args.format == 'diff-only':
        output = {
            'diff': results['diff'],
            'summary': results['summary']
        }
    else:
        output = results

    output_json = json.dumps(output, indent=2)

    # Write output
    if args.output:
        with open(args.output, 'w') as f:
            f.write(output_json)
    else:
        print(output_json)


if __name__ == '__main__':
    main()
