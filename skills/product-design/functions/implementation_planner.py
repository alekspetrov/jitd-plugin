#!/usr/bin/env python3
"""
Generate implementation task documentation from design review analysis.
Creates phased breakdown with acceptance criteria and complexity estimates.
"""

import json
import argparse
from datetime import datetime
from typing import Dict, List, Any


def estimate_complexity(component_category: str, has_variants: bool, breaking_change: bool) -> tuple:
    """
    Estimate implementation complexity and time.

    Args:
        component_category: atom, molecule, organism, template
        has_variants: Whether component has variants/props
        breaking_change: Whether this is a breaking change

    Returns:
        Tuple of (complexity_level, estimated_hours)
    """
    base_hours = {
        'atom': 2,
        'molecule': 3,
        'organism': 5,
        'template': 8
    }

    hours = base_hours.get(component_category, 3)

    if has_variants:
        hours += 1

    if breaking_change:
        hours += 2

    if hours <= 2:
        complexity = 'Low'
    elif hours <= 4:
        complexity = 'Medium'
    else:
        complexity = 'High'

    return complexity, hours


def generate_token_phase(new_tokens: List[Dict[str, Any]],
                        modified_tokens: List[Dict[str, Any]]) -> Dict[str, Any]:
    """Generate Phase 1: Design Tokens implementation plan."""
    total_tokens = len(new_tokens) + len(modified_tokens)
    hours = max(1, total_tokens // 10 + 1)  # 10 tokens per hour estimate

    subtasks = [
        f"Add {len(new_tokens)} new tokens to design-tokens.json" if new_tokens else None,
        f"Update {len(modified_tokens)} modified tokens" if modified_tokens else None,
        "Run Style Dictionary build to generate platform outputs",
        "Update Tailwind @theme with new variables",
        "Verify token availability in Storybook tokens page"
    ]

    acceptance_criteria = [
        f"All {total_tokens} new/modified tokens available in Tailwind utilities",
        "No breaking changes to existing token references",
        "Style Dictionary build completes without errors",
        "Storybook tokens page shows all additions"
    ]

    return {
        'name': 'Design Tokens',
        'priority': 'High',
        'estimated_hours': hours,
        'description': f'Add and update {total_tokens} design tokens',
        'subtasks': [task for task in subtasks if task],
        'acceptance_criteria': acceptance_criteria,
        'files_to_modify': [
            '.agent/design-system/design-tokens.json',
            'tailwind.config.js (or CSS @theme)',
            'Storybook tokens documentation'
        ]
    }


def generate_component_phase(component: Dict[str, Any], phase_number: int) -> Dict[str, Any]:
    """Generate component implementation phase."""
    comp_name = component.get('name')
    category = component.get('category', 'molecule')
    properties = component.get('properties', {})
    similar_to = component.get('similar_to', [])

    has_variants = bool(properties.get('variants'))
    breaking_change = component.get('breaking_change', False)

    complexity, hours = estimate_complexity(category, has_variants, breaking_change)

    # Determine approach
    if similar_to and similar_to[0]['similarity'] >= 0.7:
        approach = f"Extend existing {similar_to[0]['name']} component"
        action = 'extend'
    else:
        approach = f"Create new {category} component"
        action = 'create'

    # Generate subtasks based on action
    if action == 'extend':
        subtasks = [
            f"Add new variant props to {similar_to[0]['name']}",
            "Update TypeScript interface with new props",
            "Add styles for new variants",
            "Update existing tests",
            "Add Storybook stories for new variants"
        ]
        files = [
            similar_to[0].get('path', f'src/components/{category}/{comp_name}.tsx'),
            f"src/components/{category}/{comp_name}.test.tsx",
            f"src/components/{category}/{comp_name}.stories.tsx"
        ]
    else:
        subtasks = [
            f"Create {comp_name} component file",
            "Implement TypeScript props interface",
            "Add styles (CSS modules/Tailwind)",
            "Write unit tests",
            "Create Storybook stories",
            "Add barrel export (index.ts)"
        ]
        files = [
            f"src/components/{category}/{comp_name}.tsx",
            f"src/components/{category}/{comp_name}.test.tsx",
            f"src/components/{category}/{comp_name}.stories.tsx",
            f"src/components/{category}/index.ts"
        ]

    acceptance_criteria = [
        f"{comp_name} renders correctly with all variants",
        "100% test coverage for new props/variants" if action == 'extend' else "90%+ test coverage",
        "Storybook shows all component states",
        "No visual regression in existing components" if action == 'extend' else "Passes visual regression tests",
        "Accessibility audit passes (a11y addon)"
    ]

    if breaking_change:
        acceptance_criteria.insert(0, "Migration guide created for breaking changes")
        subtasks.append("Create migration documentation")

    return {
        'number': phase_number,
        'name': comp_name,
        'category': category,
        'priority': 'High' if breaking_change else 'Medium',
        'complexity': complexity,
        'estimated_hours': hours,
        'approach': approach,
        'subtasks': subtasks,
        'files_to_modify': files,
        'acceptance_criteria': acceptance_criteria,
        'breaking_change': breaking_change
    }


def generate_task_document(task_id: str,
                          feature_name: str,
                          analysis_results: Dict[str, Any],
                          review_reference: str) -> str:
    """
    Generate complete Navigator task document.

    Args:
        task_id: Task identifier (e.g., "TASK-16")
        feature_name: Feature name (e.g., "Dashboard Redesign")
        analysis_results: Combined analysis from all functions
        review_reference: Path to design review report

    Returns:
        Markdown task document
    """
    date = datetime.now().strftime('%Y-%m-%d')

    # Extract data
    new_tokens = analysis_results.get('new_tokens', [])
    modified_tokens = analysis_results.get('token_diff', {}).get('modified', [])
    new_components = analysis_results.get('new_components', [])
    similar_components = analysis_results.get('similar_components', [])
    breaking_changes = analysis_results.get('breaking_changes', [])

    # Generate phases
    phases = []

    # Phase 1: Always start with tokens if any exist
    if new_tokens or modified_tokens:
        phases.append(generate_token_phase(new_tokens, modified_tokens))

    # Phase 2+: Component implementations
    for i, comp in enumerate(new_components + similar_components, start=2):
        phases.append(generate_component_phase(comp, i))

    # Calculate totals
    total_hours = sum(phase.get('estimated_hours', 0) for phase in phases)
    total_complexity = 'High' if total_hours > 10 else 'Medium' if total_hours > 5 else 'Low'

    # Build markdown document
    doc = f"""# {task_id}: {feature_name} Implementation

**Created**: {date}
**Status**: Ready for Development
**Priority**: High
**Complexity**: {total_complexity}
**Estimated Time**: {total_hours} hours

---

## Context

Implement {feature_name} from Figma mockup with design system integration.

**Design Review**: `{review_reference}`

---

## Overview

**Changes Required**:
- Design Tokens: {len(new_tokens)} new, {len(modified_tokens)} modified
- Components: {len(new_components)} new, {len(similar_components)} to extend
- Breaking Changes: {len(breaking_changes)}

**Implementation Strategy**: Phased approach following atomic design hierarchy

---

## Implementation Phases

"""

    # Add each phase
    for i, phase in enumerate(phases, start=1):
        doc += f"""### Phase {i}: {phase['name']}

**Priority**: {phase['priority']}
**Complexity**: {phase.get('complexity', 'Medium')}
**Estimated Time**: {phase['estimated_hours']} hours

#### Approach
{phase.get('approach', phase.get('description', 'Implement component following project patterns'))}

#### Subtasks
"""
        for subtask in phase['subtasks']:
            doc += f"- {subtask}\n"

        doc += f"""
#### Files to Modify
"""
        for file in phase.get('files_to_modify', []):
            doc += f"- `{file}`\n"

        doc += f"""
**Acceptance Criteria**:
"""
        for criterion in phase['acceptance_criteria']:
            doc += f"- [ ] {criterion}\n"

        doc += "\n---\n\n"

    # Add testing strategy
    doc += """## Testing Strategy

### Unit Tests
- All new/modified components
- Test all variants and props
- Error states and edge cases
- Target: 90%+ coverage

### Visual Regression
- Chromatic for all component stories
- Test all variants and states
- Verify no regressions in existing components

### Integration Tests
- Test component composition
- Verify design token usage
- Test responsive behavior

### Accessibility
- Run a11y addon in Storybook
- Keyboard navigation testing
- Screen reader verification
- WCAG 2.2 Level AA compliance

---

## Rollout Plan

1. **Phase 1: Tokens** (no visual changes, safe to deploy)
2. **Phase 2-N: Components** (incremental deployment)
   - Deploy each component after testing
   - Monitor for issues before next phase
3. **Final: Integration** (full feature integration)

**Rollback Strategy**: Each phase is independent and can be reverted

---

## Success Metrics

- [ ] 100% design fidelity vs Figma mockup
- [ ] All acceptance criteria met
- [ ] No visual regressions
- [ ] All accessibility checks pass
- [ ] Performance budget maintained (no layout shifts)

---

## Design System Impact

**UI Kit Inventory**: Update after each component completion

**Token Additions**: {len(new_tokens)} new tokens added to design system

**Component Reuse**: {len(similar_components)} opportunities to extend existing components

---

## Notes

{f"⚠️  **Breaking Changes**: {len(breaking_changes)} component(s) require migration - see phase details" if breaking_changes else "✅ No breaking changes - backward compatible implementation"}

---

**Last Updated**: {date}
**Navigator Version**: 3.2.0
"""

    return doc


def main():
    parser = argparse.ArgumentParser(
        description='Generate implementation task document from design review'
    )
    parser.add_argument(
        '--task-id',
        required=True,
        help='Task identifier (e.g., TASK-16)'
    )
    parser.add_argument(
        '--feature-name',
        required=True,
        help='Feature name (e.g., "Dashboard Redesign")'
    )
    parser.add_argument(
        '--analysis-results',
        required=True,
        help='Path to JSON file with combined analysis results'
    )
    parser.add_argument(
        '--review-reference',
        required=True,
        help='Path to design review report'
    )
    parser.add_argument(
        '--output',
        help='Output file path (default: stdout)'
    )

    args = parser.parse_args()

    # Load analysis results
    with open(args.analysis_results, 'r') as f:
        analysis_results = json.load(f)

    # Generate task document
    task_doc = generate_task_document(
        args.task_id,
        args.feature_name,
        analysis_results,
        args.review_reference
    )

    # Output
    if args.output:
        with open(args.output, 'w') as f:
            f.write(task_doc)
    else:
        print(task_doc)


if __name__ == '__main__':
    main()
