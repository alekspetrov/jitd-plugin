#!/usr/bin/env python3
"""
Storybook Story Generator

Analyzes React/Vue/Svelte components and generates comprehensive Storybook stories
with variants, accessibility tests, and interaction tests.

Usage:
    python story_generator.py <component_path> <framework> [template_path]
"""

import json
import os
import re
import sys
from pathlib import Path
from typing import Dict, List, Optional


def extract_component_name(file_path: str) -> str:
    """Extract component name from file path."""
    return Path(file_path).stem


def analyze_react_component(component_path: str) -> Dict:
    """
    Analyze React/TypeScript component to extract props and metadata.

    Args:
        component_path: Path to component file

    Returns:
        Dict with component info: name, props, prop_types, exports
    """
    with open(component_path, 'r') as f:
        content = f.read()

    component_name = extract_component_name(component_path)

    result = {
        'name': component_name,
        'path': component_path,
        'props': [],
        'has_typescript': component_path.endswith(('.tsx', '.ts')),
        'is_default_export': False,
        'story_title': f'Components/{component_name}'
    }

    # Check for default export
    if re.search(r'export\s+default\s+' + component_name, content):
        result['is_default_export'] = True

    # Extract TypeScript interface/type props
    if result['has_typescript']:
        # Match interface or type definition
        interface_pattern = r'(?:interface|type)\s+' + component_name + r'Props\s*{([^}]+)}'
        match = re.search(interface_pattern, content, re.DOTALL)

        if match:
            props_block = match.group(1)
            # Parse each prop
            prop_pattern = r'(\w+)(\?)?:\s*([^;]+);?'
            for prop_match in re.finditer(prop_pattern, props_block):
                prop_name = prop_match.group(1)
                is_optional = prop_match.group(2) == '?'
                prop_type = prop_match.group(3).strip()

                # Determine control type based on prop type
                control = infer_control_type(prop_type)

                # Extract possible values for enums
                values = extract_enum_values(prop_type)

                result['props'].append({
                    'name': prop_name,
                    'type': prop_type,
                    'optional': is_optional,
                    'control': control,
                    'values': values,
                    'default': infer_default_value(prop_type, prop_name)
                })

    # Fallback: extract props from function signature
    if not result['props']:
        func_pattern = r'(?:function|const)\s+' + component_name + r'\s*(?:<[^>]+>)?\s*\(\s*{\s*([^}]+)\s*}'
        match = re.search(func_pattern, content)

        if match:
            props_str = match.group(1)
            # Simple extraction of prop names
            prop_names = [p.strip().split(':')[0].strip() for p in props_str.split(',')]

            for prop_name in prop_names:
                result['props'].append({
                    'name': prop_name,
                    'type': 'any',
                    'optional': False,
                    'control': 'text',
                    'values': None,
                    'default': None
                })

    return result


def infer_control_type(prop_type: str) -> str:
    """
    Infer Storybook control type from TypeScript type.

    Args:
        prop_type: TypeScript type string

    Returns:
        Storybook control type
    """
    prop_type_lower = prop_type.lower()

    # Boolean
    if 'boolean' in prop_type_lower:
        return 'boolean'

    # Number
    if 'number' in prop_type_lower:
        return 'number'

    # Union types (enums)
    if '|' in prop_type:
        return 'select'

    # Objects
    if prop_type_lower in ['object', 'record']:
        return 'object'

    # Arrays
    if '[]' in prop_type or prop_type.startswith('array'):
        return 'object'

    # Functions
    if '=>' in prop_type or prop_type.startswith('('):
        return 'function'

    # Default to text
    return 'text'


def extract_enum_values(prop_type: str) -> Optional[List[str]]:
    """
    Extract possible values from union type.

    Args:
        prop_type: TypeScript type string (e.g., "'sm' | 'md' | 'lg'")

    Returns:
        List of possible values or None
    """
    if '|' not in prop_type:
        return None

    # Extract string literals
    values = re.findall(r"['\"]([^'\"]+)['\"]", prop_type)

    return values if values else None


def infer_default_value(prop_type: str, prop_name: str) -> any:
    """
    Infer reasonable default value for prop.

    Args:
        prop_type: TypeScript type string
        prop_name: Prop name

    Returns:
        Default value
    """
    prop_type_lower = prop_type.lower()
    prop_name_lower = prop_name.lower()

    # Boolean
    if 'boolean' in prop_type_lower:
        return False

    # Number
    if 'number' in prop_type_lower:
        if 'count' in prop_name_lower:
            return 0
        return 1

    # Union types - return first value
    values = extract_enum_values(prop_type)
    if values:
        return values[0]

    # Strings - context-aware defaults
    if 'name' in prop_name_lower:
        return 'John Doe'
    if 'title' in prop_name_lower:
        return 'Example Title'
    if 'description' in prop_name_lower or 'bio' in prop_name_lower:
        return 'This is an example description'
    if 'email' in prop_name_lower:
        return 'user@example.com'
    if 'url' in prop_name_lower or 'href' in prop_name_lower:
        return 'https://example.com'
    if 'image' in prop_name_lower or 'avatar' in prop_name_lower:
        return 'https://via.placeholder.com/150'

    return 'Example text'


def generate_variants(component_info: Dict) -> List[Dict]:
    """
    Generate story variants based on component props.

    Args:
        component_info: Component analysis result

    Returns:
        List of variant definitions
    """
    variants = []

    # Generate variants for enum props
    for prop in component_info['props']:
        if prop['values'] and len(prop['values']) > 1:
            # Create variant for each enum value
            for value in prop['values']:
                if value != prop['default']:  # Skip default (already in Default story)
                    variant_name = value.capitalize()
                    variants.append({
                        'name': variant_name,
                        'prop_name': prop['name'],
                        'value': value
                    })

    # Generate boolean state variants
    for prop in component_info['props']:
        if prop['type'].lower() == 'boolean' and not prop['default']:
            variant_name = prop['name'].capitalize()
            variants.append({
                'name': variant_name,
                'prop_name': prop['name'],
                'value': True
            })

    return variants


def generate_story_content(component_info: Dict, framework: str = 'react') -> str:
    """
    Generate complete Storybook story file content.

    Args:
        component_info: Component analysis result
        framework: Framework name ('react', 'vue', 'svelte')

    Returns:
        Story file content as string
    """
    if framework == 'react':
        return generate_react_story(component_info)
    elif framework == 'vue':
        return generate_vue_story(component_info)
    elif framework == 'svelte':
        return generate_svelte_story(component_info)
    else:
        raise ValueError(f"Unsupported framework: {framework}")


def generate_react_story(component_info: Dict) -> str:
    """Generate React/TypeScript story."""
    name = component_info['name']
    props = component_info['props']
    variants = generate_variants(component_info)

    # Build imports
    imports = f"""import type {{ Meta, StoryObj }} from '@storybook/react';
import {{ {name} }} from './{name}';
"""

    # Build argTypes
    arg_types = []
    for prop in props:
        if prop['values']:
            arg_types.append(f"    {prop['name']}: {{ control: '{prop['control']}', options: {json.dumps(prop['values'])} }}")
        else:
            arg_types.append(f"    {prop['name']}: {{ control: '{prop['control']}' }}")

    arg_types_str = ',\n'.join(arg_types) if arg_types else ''

    # Build default args
    default_args = []
    for prop in props:
        if prop['default'] is not None:
            if isinstance(prop['default'], str):
                default_args.append(f"    {prop['name']}: '{prop['default']}'")
            else:
                default_args.append(f"    {prop['name']}: {json.dumps(prop['default'])}")

    default_args_str = ',\n'.join(default_args) if default_args else ''

    # Build meta
    meta = f"""
const meta = {{
  title: '{component_info['story_title']}',
  component: {name},
  parameters: {{
    layout: 'centered',
  }},
  tags: ['autodocs'],
  argTypes: {{
{arg_types_str}
  }},
}} satisfies Meta<typeof {name}>;

export default meta;
type Story = StoryObj<typeof meta>;
"""

    # Default story
    default_story = f"""
export const Default: Story = {{
  args: {{
{default_args_str}
  }},
}};
"""

    # Variant stories
    variant_stories = []
    for variant in variants:
        if isinstance(variant['value'], str):
            value_str = f"'{variant['value']}'"
        else:
            value_str = json.dumps(variant['value'])

        variant_stories.append(f"""
export const {variant['name']}: Story = {{
  args: {{
    ...Default.args,
    {variant['prop_name']}: {value_str},
  }},
}};
""")

    variant_stories_str = ''.join(variant_stories)

    # Accessibility tests
    a11y = f"""
// Accessibility tests
Default.parameters = {{
  a11y: {{
    config: {{
      rules: [
        {{ id: 'color-contrast', enabled: true }},
        {{ id: 'label', enabled: true }},
      ],
    }},
  }},
}};
"""

    return imports + meta + default_story + variant_stories_str + a11y


def generate_vue_story(component_info: Dict) -> str:
    """Generate Vue story (simplified)."""
    name = component_info['name']

    return f"""import type {{ Meta, StoryObj }} from '@storybook/vue3';
import {name} from './{name}.vue';

const meta = {{
  title: 'Components/{name}',
  component: {name},
  tags: ['autodocs'],
}} satisfies Meta<typeof {name}>;

export default meta;
type Story = StoryObj<typeof meta>;

export const Default: Story = {{
  args: {{}},
}};
"""


def generate_svelte_story(component_info: Dict) -> str:
    """Generate Svelte story (simplified)."""
    name = component_info['name']

    return f"""import type {{ Meta, StoryObj }} from '@storybook/svelte';
import {name} from './{name}.svelte';

const meta = {{
  title: 'Components/{name}',
  component: {name},
  tags: ['autodocs'],
}} satisfies Meta<typeof {name}>;

export default meta;
type Story = StoryObj<typeof meta>;

export const Default: Story = {{
  args: {{}},
}};
"""


def write_story_file(component_path: str, story_content: str) -> str:
    """
    Write story file next to component file.

    Args:
        component_path: Path to component file
        story_content: Generated story content

    Returns:
        Path to created story file
    """
    component_file = Path(component_path)
    story_file = component_file.parent / f"{component_file.stem}.stories{component_file.suffix}"

    with open(story_file, 'w') as f:
        f.write(story_content)

    return str(story_file)


def main():
    """CLI entry point."""
    if len(sys.argv) < 3:
        print("Usage: python story_generator.py <component_path> <framework>", file=sys.stderr)
        sys.exit(1)

    component_path = sys.argv[1]
    framework = sys.argv[2].lower()

    if framework not in ['react', 'vue', 'svelte']:
        print(f"Unsupported framework: {framework}. Use: react, vue, or svelte", file=sys.stderr)
        sys.exit(1)

    if not os.path.exists(component_path):
        print(f"Component file not found: {component_path}", file=sys.stderr)
        sys.exit(1)

    # Analyze component
    if framework == 'react':
        component_info = analyze_react_component(component_path)
    else:
        # Simplified for Vue/Svelte
        component_info = {
            'name': extract_component_name(component_path),
            'path': component_path,
            'props': [],
            'story_title': f'Components/{extract_component_name(component_path)}'
        }

    # Generate story
    story_content = generate_story_content(component_info, framework)

    # Write story file
    story_file_path = write_story_file(component_path, story_content)

    # Output result
    result = {
        'component': component_info,
        'story_file': story_file_path,
        'success': True
    }

    print(json.dumps(result, indent=2))


if __name__ == '__main__':
    main()
