#!/usr/bin/env python3
"""
Analyze Figma design data and extract patterns, components, and tokens.
Compares against existing UI kit to identify new components and potential reuse opportunities.
"""

import json
import sys
import argparse
from typing import Dict, List, Any
from difflib import SequenceMatcher


def calculate_similarity(str1: str, str2: str) -> float:
    """
    Calculate similarity ratio between two strings.

    Args:
        str1: First string
        str2: Second string

    Returns:
        float: Similarity ratio (0.0 to 1.0)
    """
    return SequenceMatcher(None, str1.lower(), str2.lower()).ratio()


def extract_components_from_metadata(metadata: Dict[str, Any]) -> List[Dict[str, Any]]:
    """
    Extract component information from Figma metadata.

    Args:
        metadata: Figma MCP get_metadata response or manual structure

    Returns:
        List of components with their properties
    """
    components = []

    def traverse_nodes(node, depth=0):
        """Recursively traverse Figma node tree."""
        if not isinstance(node, dict):
            return

        node_type = node.get('type', '')
        node_name = node.get('name', 'Unnamed')
        node_id = node.get('id', '')

        # Identify components (COMPONENT, COMPONENT_SET, or instances)
        if node_type in ['COMPONENT', 'COMPONENT_SET', 'INSTANCE']:
            components.append({
                'id': node_id,
                'name': node_name,
                'type': node_type,
                'depth': depth,
                'properties': extract_node_properties(node)
            })

        # Traverse children
        children = node.get('children', [])
        for child in children:
            traverse_nodes(child, depth + 1)

    # Handle both MCP format and manual format
    if 'document' in metadata:
        traverse_nodes(metadata['document'])
    elif 'nodes' in metadata:
        for node in metadata['nodes']:
            traverse_nodes(node)
    elif isinstance(metadata, dict):
        traverse_nodes(metadata)

    return components


def extract_node_properties(node: Dict[str, Any]) -> Dict[str, Any]:
    """
    Extract relevant properties from Figma node.

    Args:
        node: Figma node data

    Returns:
        Dictionary of extracted properties
    """
    properties = {}

    # Extract layout properties
    if 'layoutMode' in node:
        properties['layout'] = {
            'mode': node.get('layoutMode'),
            'direction': node.get('layoutDirection'),
            'gap': node.get('itemSpacing'),
            'padding': {
                'top': node.get('paddingTop'),
                'right': node.get('paddingRight'),
                'bottom': node.get('paddingBottom'),
                'left': node.get('paddingLeft')
            }
        }

    # Extract sizing
    if 'absoluteBoundingBox' in node:
        bbox = node['absoluteBoundingBox']
        properties['size'] = {
            'width': bbox.get('width'),
            'height': bbox.get('height')
        }

    # Extract variant properties
    if 'componentProperties' in node:
        properties['variants'] = node['componentProperties']

    return properties


def categorize_component_by_name(component_name: str) -> str:
    """
    Categorize component by atomic design level based on name patterns.

    Args:
        component_name: Component name from Figma

    Returns:
        'atom', 'molecule', 'organism', or 'template'
    """
    name_lower = component_name.lower()

    # Atoms: Basic elements
    atoms = ['button', 'input', 'icon', 'text', 'badge', 'avatar', 'checkbox',
             'radio', 'switch', 'label', 'link', 'image']

    # Molecules: Simple combinations
    molecules = ['field', 'card', 'list-item', 'menu-item', 'tab', 'breadcrumb',
                 'tooltip', 'dropdown', 'search', 'pagination']

    # Organisms: Complex components
    organisms = ['header', 'footer', 'sidebar', 'navigation', 'modal', 'form',
                 'table', 'dashboard', 'profile', 'chart', 'grid']

    for atom in atoms:
        if atom in name_lower:
            return 'atom'

    for molecule in molecules:
        if molecule in name_lower:
            return 'molecule'

    for organism in organisms:
        if organism in name_lower:
            return 'organism'

    # Default to molecule if unclear
    return 'molecule'


def find_similar_components(new_component: Dict[str, Any],
                           ui_kit_inventory: List[Dict[str, Any]],
                           threshold: float = 0.7) -> List[Dict[str, Any]]:
    """
    Find similar components in existing UI kit.

    Args:
        new_component: Component from Figma design
        ui_kit_inventory: List of existing UI kit components
        threshold: Similarity threshold (0.0 to 1.0)

    Returns:
        List of similar components with similarity scores
    """
    similar = []
    new_name = new_component.get('name', '')

    for existing in ui_kit_inventory:
        existing_name = existing.get('name', '')
        similarity = calculate_similarity(new_name, existing_name)

        if similarity >= threshold:
            similar.append({
                'name': existing_name,
                'path': existing.get('path', ''),
                'similarity': similarity,
                'recommendation': generate_recommendation(similarity, new_name, existing_name)
            })

    # Sort by similarity descending
    similar.sort(key=lambda x: x['similarity'], reverse=True)

    return similar


def generate_recommendation(similarity: float, new_name: str, existing_name: str) -> str:
    """
    Generate recommendation based on similarity score.

    Args:
        similarity: Similarity ratio
        new_name: New component name
        existing_name: Existing component name

    Returns:
        Recommendation string
    """
    if similarity >= 0.9:
        return f"Very similar to {existing_name}. Consider reusing existing component."
    elif similarity >= 0.7:
        return f"Similar to {existing_name}. Consider extending with new variant/prop."
    else:
        return f"Some similarity to {existing_name}. Review for potential shared patterns."


def analyze_design(figma_data: Dict[str, Any],
                  ui_kit_inventory: Dict[str, Any]) -> Dict[str, Any]:
    """
    Main analysis function: extract patterns from Figma and compare with UI kit.

    Args:
        figma_data: Combined Figma MCP data (metadata, variables, code_connect_map)
        ui_kit_inventory: Current UI kit inventory

    Returns:
        Analysis results with new tokens, components, similarities, breaking changes
    """
    results = {
        'new_tokens': [],
        'new_components': [],
        'similar_components': [],
        'breaking_changes': [],
        'summary': {}
    }

    # Extract components from Figma metadata
    metadata = figma_data.get('metadata', {})
    figma_components = extract_components_from_metadata(metadata)

    # Extract existing UI kit components
    existing_components = ui_kit_inventory.get('components', [])

    # Analyze each Figma component
    for figma_comp in figma_components:
        comp_name = figma_comp.get('name', '')

        # Skip system components (starting with _, . or #)
        if comp_name.startswith(('_', '.', '#')):
            continue

        # Find similar components
        similar = find_similar_components(figma_comp, existing_components, threshold=0.7)

        if similar:
            # Component has similarities - potential reuse
            results['similar_components'].append({
                'figma_component': comp_name,
                'figma_id': figma_comp.get('id'),
                'category': categorize_component_by_name(comp_name),
                'similar_to': similar,
                'properties': figma_comp.get('properties', {})
            })
        else:
            # New component - needs creation
            results['new_components'].append({
                'name': comp_name,
                'id': figma_comp.get('id'),
                'category': categorize_component_by_name(comp_name),
                'properties': figma_comp.get('properties', {}),
                'depth': figma_comp.get('depth', 0)
            })

    # Analyze design tokens from variables
    variables = figma_data.get('variables', {})
    if variables:
        results['new_tokens'] = analyze_tokens(variables, ui_kit_inventory)

    # Analyze breaking changes
    code_connect_map = figma_data.get('code_connect_map', {})
    if code_connect_map:
        results['breaking_changes'] = detect_breaking_changes(
            figma_components,
            code_connect_map,
            existing_components
        )

    # Generate summary
    results['summary'] = {
        'total_figma_components': len(figma_components),
        'new_components_count': len(results['new_components']),
        'similar_components_count': len(results['similar_components']),
        'new_tokens_count': len(results['new_tokens']),
        'breaking_changes_count': len(results['breaking_changes']),
        'reuse_potential': f"{(len(results['similar_components']) / max(len(figma_components), 1)) * 100:.1f}%"
    }

    return results


def analyze_tokens(variables: Dict[str, Any],
                   ui_kit_inventory: Dict[str, Any]) -> List[Dict[str, Any]]:
    """
    Analyze design tokens from Figma variables.

    Args:
        variables: Figma variables data
        ui_kit_inventory: Current UI kit inventory with existing tokens

    Returns:
        List of new tokens not in current inventory
    """
    new_tokens = []
    existing_tokens = ui_kit_inventory.get('tokens', {})

    # Handle different variable formats
    for var_name, var_data in variables.items():
        if isinstance(var_data, dict):
            value = var_data.get('$value') or var_data.get('value')
            var_type = var_data.get('$type') or var_data.get('type')
        else:
            value = var_data
            var_type = infer_token_type(var_name, value)

        # Check if token exists
        if var_name not in existing_tokens:
            new_tokens.append({
                'name': var_name,
                'value': value,
                'type': var_type,
                'status': 'new'
            })

    return new_tokens


def infer_token_type(name: str, value: Any) -> str:
    """
    Infer token type from name and value.

    Args:
        name: Token name
        value: Token value

    Returns:
        Token type string
    """
    name_lower = name.lower()

    if 'color' in name_lower or (isinstance(value, str) and value.startswith('#')):
        return 'color'
    elif 'spacing' in name_lower or 'gap' in name_lower or 'padding' in name_lower:
        return 'dimension'
    elif 'font' in name_lower or 'typography' in name_lower:
        return 'typography'
    elif 'radius' in name_lower or 'border' in name_lower:
        return 'dimension'
    elif 'shadow' in name_lower:
        return 'shadow'
    else:
        return 'unknown'


def detect_breaking_changes(figma_components: List[Dict[str, Any]],
                           code_connect_map: Dict[str, Any],
                           existing_components: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    """
    Detect breaking changes in component mappings.

    Args:
        figma_components: Components from Figma
        code_connect_map: Figma Code Connect mappings
        existing_components: Existing UI kit components

    Returns:
        List of breaking changes detected
    """
    breaking_changes = []

    for figma_comp in figma_components:
        comp_id = figma_comp.get('id')
        comp_name = figma_comp.get('name')

        # Check if component was previously mapped
        if comp_id in code_connect_map:
            mapping = code_connect_map[comp_id]
            mapped_path = mapping.get('codeConnectSrc')

            # Check if mapped component still exists
            exists = any(
                existing.get('path') == mapped_path
                for existing in existing_components
            )

            if not exists:
                breaking_changes.append({
                    'figma_component': comp_name,
                    'figma_id': comp_id,
                    'previous_mapping': mapped_path,
                    'issue': 'Mapped component no longer exists in codebase',
                    'recommendation': 'Re-map to new component or create new implementation'
                })

    return breaking_changes


def main():
    parser = argparse.ArgumentParser(
        description='Analyze Figma design data and compare with UI kit'
    )
    parser.add_argument(
        '--figma-data',
        required=True,
        help='Path to JSON file with Figma MCP data'
    )
    parser.add_argument(
        '--ui-kit-inventory',
        required=True,
        help='Path to UI kit inventory JSON file'
    )
    parser.add_argument(
        '--output',
        help='Output file path (default: stdout)'
    )

    args = parser.parse_args()

    # Load Figma data
    with open(args.figma_data, 'r') as f:
        figma_data = json.load(f)

    # Load UI kit inventory
    with open(args.ui_kit_inventory, 'r') as f:
        ui_kit_inventory = json.load(f)

    # Run analysis
    results = analyze_design(figma_data, ui_kit_inventory)

    # Output results
    output_json = json.dumps(results, indent=2)

    if args.output:
        with open(args.output, 'w') as f:
            f.write(output_json)
    else:
        print(output_json)


if __name__ == '__main__':
    main()
