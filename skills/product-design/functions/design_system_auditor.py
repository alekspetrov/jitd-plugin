#!/usr/bin/env python3
"""
Audit design system for drift between Figma design and code implementation.
Compares tokens, components, and generates recommendations.
"""

import json
import argparse
from typing import Dict, List, Any


def audit_token_alignment(figma_tokens: Dict[str, Any],
                          code_tokens: Dict[str, Any]) -> Dict[str, Any]:
    """
    Audit token alignment between Figma and code.

    Args:
        figma_tokens: Tokens from Figma (DTCG format)
        code_tokens: Tokens from code (design-tokens.json)

    Returns:
        Alignment report with drift analysis
    """
    def flatten_tokens(tokens, prefix=''):
        """Flatten nested tokens to dot notation."""
        flat = {}
        for key, value in tokens.items():
            path = f"{prefix}.{key}" if prefix else key
            if isinstance(value, dict) and '$value' in value:
                flat[path] = value
            elif isinstance(value, dict):
                flat.update(flatten_tokens(value, path))
        return flat

    figma_flat = flatten_tokens(figma_tokens)
    code_flat = flatten_tokens(code_tokens)

    alignment = {
        'in_sync': [],
        'drift_detected': [],
        'missing_in_code': [],
        'unused_in_design': []
    }

    # Compare Figma tokens with code
    for token_path, figma_data in figma_flat.items():
        figma_value = figma_data.get('$value')

        if token_path in code_flat:
            code_value = code_flat[token_path].get('$value')

            if figma_value == code_value:
                alignment['in_sync'].append({
                    'path': token_path,
                    'value': figma_value
                })
            else:
                alignment['drift_detected'].append({
                    'path': token_path,
                    'figma_value': figma_value,
                    'code_value': code_value,
                    'type': figma_data.get('$type')
                })
        else:
            alignment['missing_in_code'].append({
                'path': token_path,
                'value': figma_value,
                'type': figma_data.get('$type')
            })

    # Find tokens in code but not in Figma
    for token_path in code_flat.keys():
        if token_path not in figma_flat:
            alignment['unused_in_design'].append({
                'path': token_path,
                'value': code_flat[token_path].get('$value'),
                'type': code_flat[token_path].get('$type')
            })

    return alignment


def analyze_component_reuse(figma_components: List[Dict[str, Any]],
                           component_mappings: Dict[str, Any]) -> List[Dict[str, Any]]:
    """
    Analyze component reuse opportunities.

    Args:
        figma_components: Components from design_analyzer
        component_mappings: Mappings from component_mapper

    Returns:
        List of reuse opportunities
    """
    opportunities = []

    # Get similar components from mappings
    similar_components = component_mappings.get('low_confidence', [])

    for similar in similar_components:
        confidence = similar.get('confidence', 0)
        figma_name = similar.get('figma_name')
        code_component = similar.get('code_component')

        if confidence >= 0.7:
            # Strong similarity - suggest extending existing
            opportunities.append({
                'figma_component': figma_name,
                'existing_component': code_component,
                'code_path': similar.get('code_path'),
                'similarity': confidence,
                'recommendation': f"Extend {code_component} with new variant/prop instead of creating new component",
                'estimated_time_saved': '2-3 hours'
            })
        elif confidence >= 0.5:
            # Moderate similarity - suggest reviewing for shared patterns
            opportunities.append({
                'figma_component': figma_name,
                'existing_component': code_component,
                'code_path': similar.get('code_path'),
                'similarity': confidence,
                'recommendation': f"Review {code_component} for shared patterns before implementing",
                'estimated_time_saved': '1-2 hours'
            })

    return opportunities


def audit_tailwind_config(tokens: Dict[str, Any], tailwind_config_path: str = None) -> Dict[str, Any]:
    """
    Audit Tailwind config alignment with design tokens.

    Args:
        tokens: Design tokens (DTCG format)
        tailwind_config_path: Path to tailwind.config.js (optional)

    Returns:
        Tailwind alignment report
    """
    # This is a simplified version - real implementation would parse tailwind.config.js
    # For now, return structure for manual audit

    alignment = {
        'status': 'manual_audit_required',
        'recommendations': []
    }

    def flatten_tokens(tokens, prefix=''):
        flat = {}
        for key, value in tokens.items():
            path = f"{prefix}.{key}" if prefix else key
            if isinstance(value, dict) and '$value' in value:
                flat[path] = value
            elif isinstance(value, dict):
                flat.update(flatten_tokens(value, path))
        return flat

    flat_tokens = flatten_tokens(tokens)

    # Generate recommendations based on token types
    color_tokens = [t for t in flat_tokens.keys() if t.startswith('color.')]
    spacing_tokens = [t for t in flat_tokens.keys() if t.startswith('spacing.')]
    typography_tokens = [t for t in flat_tokens.keys() if t.startswith('typography.')]

    if color_tokens:
        alignment['recommendations'].append({
            'category': 'colors',
            'action': f'Add {len(color_tokens)} color tokens to Tailwind theme.extend.colors',
            'example': f'"{color_tokens[0]}": "var(--{color_tokens[0].replace(".", "-")})"'
        })

    if spacing_tokens:
        alignment['recommendations'].append({
            'category': 'spacing',
            'action': f'Add {len(spacing_tokens)} spacing tokens to Tailwind theme.extend.spacing',
            'example': f'"{spacing_tokens[0].split(".")[-1]}": "var(--{spacing_tokens[0].replace(".", "-")})"'
        })

    if typography_tokens:
        alignment['recommendations'].append({
            'category': 'typography',
            'action': f'Add {len(typography_tokens)} typography tokens to Tailwind theme.extend.fontSize',
            'example': 'Use Style Dictionary to generate Tailwind @theme directive'
        })

    return alignment


def generate_audit_summary(token_alignment: Dict[str, Any],
                          component_reuse: List[Dict[str, Any]]) -> Dict[str, Any]:
    """
    Generate overall audit summary with priority levels.

    Args:
        token_alignment: Token alignment report
        component_reuse: Component reuse opportunities

    Returns:
        Summary with priority levels and recommendations
    """
    total_tokens = (
        len(token_alignment['in_sync']) +
        len(token_alignment['drift_detected']) +
        len(token_alignment['missing_in_code']) +
        len(token_alignment['unused_in_design'])
    )

    drift_count = len(token_alignment['drift_detected'])
    missing_count = len(token_alignment['missing_in_code'])

    # Determine priority
    if drift_count > 10 or (drift_count / max(total_tokens, 1)) > 0.2:
        priority = 'critical'
    elif drift_count > 5 or missing_count > 10:
        priority = 'high'
    elif drift_count > 0 or missing_count > 0:
        priority = 'medium'
    else:
        priority = 'low'

    summary = {
        'token_health': {
            'total': total_tokens,
            'in_sync': len(token_alignment['in_sync']),
            'drift_detected': drift_count,
            'missing_in_code': missing_count,
            'unused_in_design': len(token_alignment['unused_in_design']),
            'sync_percentage': f"{(len(token_alignment['in_sync']) / max(total_tokens, 1)) * 100:.1f}%"
        },
        'component_reuse': {
            'opportunities_found': len(component_reuse),
            'estimated_time_savings': f"{len(component_reuse) * 2}-{len(component_reuse) * 3} hours"
        },
        'priority': priority,
        'top_recommendations': generate_top_recommendations(
            token_alignment,
            component_reuse,
            priority
        )
    }

    return summary


def generate_top_recommendations(token_alignment: Dict[str, Any],
                                component_reuse: List[Dict[str, Any]],
                                priority: str) -> List[str]:
    """Generate top 3-5 recommendations based on audit results."""
    recommendations = []

    drift_count = len(token_alignment['drift_detected'])
    missing_count = len(token_alignment['missing_in_code'])

    if drift_count > 0:
        recommendations.append(
            f"⚠️  Fix {drift_count} drifted tokens - update design-tokens.json with Figma values"
        )

    if missing_count > 0:
        recommendations.append(
            f"➕ Add {missing_count} new tokens to design system - run Style Dictionary build after"
        )

    if len(token_alignment['unused_in_design']) > 5:
        recommendations.append(
            f"🗑️  Clean up {len(token_alignment['unused_in_design'])} unused tokens in codebase"
        )

    if component_reuse:
        top_reuse = component_reuse[0]
        recommendations.append(
            f"♻️  Reuse opportunity: Extend {top_reuse['existing_component']} instead of creating {top_reuse['figma_component']}"
        )

    if priority == 'low':
        recommendations.append("✅ Design system is well-aligned - good maintenance!")

    return recommendations[:5]


def audit_design_system(figma_data: Dict[str, Any],
                       code_data: Dict[str, Any]) -> Dict[str, Any]:
    """
    Main audit function: comprehensive design system health check.

    Args:
        figma_data: Combined Figma data (tokens, components, mappings)
        code_data: Combined code data (design-tokens.json, ui-kit-inventory, etc.)

    Returns:
        Complete audit report with recommendations
    """
    # Extract data
    figma_tokens = figma_data.get('tokens', {})
    figma_components = figma_data.get('components', [])
    component_mappings = figma_data.get('component_mappings', {})

    code_tokens = code_data.get('design_tokens', {})
    ui_kit_inventory = code_data.get('ui_kit_inventory', {})

    # Run audits
    token_alignment = audit_token_alignment(figma_tokens, code_tokens)
    component_reuse = analyze_component_reuse(figma_components, component_mappings)
    tailwind_alignment = audit_tailwind_config(code_tokens)

    # Generate summary
    summary = generate_audit_summary(token_alignment, component_reuse)

    return {
        'token_alignment': token_alignment,
        'component_reuse_opportunities': component_reuse,
        'tailwind_alignment': tailwind_alignment,
        'summary': summary
    }


def main():
    parser = argparse.ArgumentParser(
        description='Audit design system for drift and reuse opportunities'
    )
    parser.add_argument(
        '--figma-data',
        required=True,
        help='Path to JSON file with Figma data (tokens, components, mappings)'
    )
    parser.add_argument(
        '--code-data',
        required=True,
        help='Path to JSON file with code data (design-tokens.json, ui-kit-inventory)'
    )
    parser.add_argument(
        '--output',
        help='Output file path (default: stdout)'
    )

    args = parser.parse_args()

    # Load data
    with open(args.figma_data, 'r') as f:
        figma_data = json.load(f)

    with open(args.code_data, 'r') as f:
        code_data = json.load(f)

    # Run audit
    audit_results = audit_design_system(figma_data, code_data)

    # Output results
    output_json = json.dumps(audit_results, indent=2)

    if args.output:
        with open(args.output, 'w') as f:
            f.write(output_json)
    else:
        print(output_json)


if __name__ == '__main__':
    main()
