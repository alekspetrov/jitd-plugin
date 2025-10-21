#!/usr/bin/env python3
"""
Map Figma components to codebase components using Code Connect data and fuzzy matching.
"""

import json
import argparse
import os
from typing import Dict, List, Any
from difflib import SequenceMatcher


def calculate_similarity(str1: str, str2: str) -> float:
    """Calculate similarity ratio between two strings."""
    return SequenceMatcher(None, str1.lower(), str2.lower()).ratio()


def find_component_files(project_root: str, extensions: List[str] = None) -> List[Dict[str, str]]:
    """
    Find all component files in project.

    Args:
        project_root: Project root directory
        extensions: File extensions to search (default: ['tsx', 'jsx', 'vue'])

    Returns:
        List of component file info (path, name)
    """
    if extensions is None:
        extensions = ['tsx', 'jsx', 'vue', 'svelte']

    components = []

    for root, dirs, files in os.walk(project_root):
        # Skip node_modules, dist, build directories
        dirs[:] = [d for d in dirs if d not in ['node_modules', 'dist', 'build', '.git', '.next']]

        for file in files:
            if any(file.endswith(f'.{ext}') for ext in extensions):
                full_path = os.path.join(root, file)
                rel_path = os.path.relpath(full_path, project_root)

                # Extract component name (filename without extension)
                comp_name = os.path.splitext(file)[0]

                # Skip test files, stories, etc.
                if any(suffix in comp_name.lower() for suffix in ['.test', '.spec', '.stories', '.story']):
                    continue

                components.append({
                    'name': comp_name,
                    'path': rel_path,
                    'full_path': full_path
                })

    return components


def fuzzy_match_component(figma_name: str, codebase_components: List[Dict[str, str]],
                         threshold: float = 0.6) -> List[Dict[str, Any]]:
    """
    Fuzzy match Figma component name to codebase components.

    Args:
        figma_name: Figma component name
        codebase_components: List of codebase component info
        threshold: Minimum similarity threshold

    Returns:
        List of matches with confidence scores
    """
    matches = []

    # Clean Figma name (remove variant info)
    # "Button/Primary/Large" → "Button"
    base_name = figma_name.split('/')[0].strip()

    for comp in codebase_components:
        comp_name = comp['name']
        similarity = calculate_similarity(base_name, comp_name)

        if similarity >= threshold:
            matches.append({
                'figma_name': figma_name,
                'code_component': comp_name,
                'code_path': comp['path'],
                'confidence': round(similarity, 3),
                'match_type': 'fuzzy'
            })

    # Sort by confidence
    matches.sort(key=lambda x: x['confidence'], reverse=True)

    return matches


def extract_variant_mapping(figma_name: str) -> Dict[str, str]:
    """
    Extract variant information from Figma component name.

    Examples:
        "Button/Primary/Large" → {"variant": "primary", "size": "lg"}
        "Card/Elevated" → {"variant": "elevated"}

    Args:
        figma_name: Figma component name with variants

    Returns:
        Dictionary of variant properties
    """
    parts = [p.strip() for p in figma_name.split('/')]

    if len(parts) == 1:
        return {}

    # Base component is first part
    variants = parts[1:]

    # Map common variant patterns
    mapping = {}

    for variant in variants:
        variant_lower = variant.lower()

        # Size variants
        if variant_lower in ['small', 'sm', 'xs', 'tiny']:
            mapping['size'] = 'sm'
        elif variant_lower in ['medium', 'md', 'base']:
            mapping['size'] = 'md'
        elif variant_lower in ['large', 'lg']:
            mapping['size'] = 'lg'
        elif variant_lower in ['xl', 'xlarge', 'extra-large']:
            mapping['size'] = 'xl'

        # Style variants
        elif variant_lower in ['primary', 'main']:
            mapping['variant'] = 'primary'
        elif variant_lower in ['secondary', 'outline', 'outlined']:
            mapping['variant'] = 'secondary'
        elif variant_lower in ['tertiary', 'ghost', 'link', 'text']:
            mapping['variant'] = 'ghost'

        # State variants
        elif variant_lower in ['disabled', 'inactive']:
            mapping['state'] = 'disabled'
        elif variant_lower in ['loading', 'busy']:
            mapping['state'] = 'loading'

        # Type variants
        elif variant_lower in ['solid', 'filled']:
            mapping['type'] = 'solid'
        elif variant_lower in ['elevated', 'raised']:
            mapping['type'] = 'elevated'
        elif variant_lower in ['flat', 'plain']:
            mapping['type'] = 'flat'

        # If no pattern matches, use as generic variant
        else:
            if 'variant' not in mapping:
                mapping['variant'] = variant_lower

    return mapping


def map_components(figma_components: List[Dict[str, Any]],
                  code_connect_map: Dict[str, Any],
                  project_root: str) -> Dict[str, Any]:
    """
    Main mapping function: map Figma components to codebase components.

    Args:
        figma_components: List of Figma components from design_analyzer
        code_connect_map: Figma Code Connect mappings
        project_root: Project root directory for component search

    Returns:
        Component mappings with confidence scores
    """
    # Find all component files in codebase
    codebase_components = find_component_files(project_root)

    mappings = {
        'mapped': [],
        'unmapped': [],
        'low_confidence': [],
        'summary': {}
    }

    for figma_comp in figma_components:
        comp_id = figma_comp.get('id')
        comp_name = figma_comp.get('name')

        # Check Code Connect first (highest confidence)
        if comp_id and comp_id in code_connect_map:
            code_connect_data = code_connect_map[comp_id]
            mappings['mapped'].append({
                'figma_id': comp_id,
                'figma_name': comp_name,
                'code_component': code_connect_data.get('codeConnectName'),
                'code_path': code_connect_data.get('codeConnectSrc'),
                'confidence': 1.0,
                'match_type': 'code_connect',
                'props_mapping': extract_variant_mapping(comp_name)
            })
        else:
            # Fallback to fuzzy matching
            matches = fuzzy_match_component(comp_name, codebase_components, threshold=0.6)

            if matches and matches[0]['confidence'] >= 0.8:
                # High confidence match
                best_match = matches[0]
                best_match['figma_id'] = comp_id
                best_match['props_mapping'] = extract_variant_mapping(comp_name)
                mappings['mapped'].append(best_match)

            elif matches:
                # Low confidence match (manual review needed)
                for match in matches[:3]:  # Top 3 matches
                    match['figma_id'] = comp_id
                    match['props_mapping'] = extract_variant_mapping(comp_name)
                    mappings['low_confidence'].append(match)

            else:
                # No match found
                mappings['unmapped'].append({
                    'figma_id': comp_id,
                    'figma_name': comp_name,
                    'recommendation': 'Create new component',
                    'props_mapping': extract_variant_mapping(comp_name)
                })

    # Generate summary
    total = len(figma_components)
    mappings['summary'] = {
        'total_figma_components': total,
        'mapped_count': len(mappings['mapped']),
        'low_confidence_count': len(mappings['low_confidence']),
        'unmapped_count': len(mappings['unmapped']),
        'mapping_coverage': f"{(len(mappings['mapped']) / max(total, 1)) * 100:.1f}%"
    }

    return mappings


def main():
    parser = argparse.ArgumentParser(
        description='Map Figma components to codebase components'
    )
    parser.add_argument(
        '--figma-components',
        required=True,
        help='Path to JSON file with Figma components (from design_analyzer)'
    )
    parser.add_argument(
        '--code-connect-map',
        help='Path to Code Connect map JSON (optional)'
    )
    parser.add_argument(
        '--project-root',
        required=True,
        help='Project root directory'
    )
    parser.add_argument(
        '--output',
        help='Output file path (default: stdout)'
    )

    args = parser.parse_args()

    # Load Figma components
    with open(args.figma_components, 'r') as f:
        figma_components = json.load(f)

    # Load Code Connect map if provided
    code_connect_map = {}
    if args.code_connect_map:
        with open(args.code_connect_map, 'r') as f:
            code_connect_map = json.load(f)

    # Run mapping
    mappings = map_components(figma_components, code_connect_map, args.project_root)

    # Output results
    output_json = json.dumps(mappings, indent=2)

    if args.output:
        with open(args.output, 'w') as f:
            f.write(output_json)
    else:
        print(output_json)


if __name__ == '__main__':
    main()
