# Design Review: {{FEATURE_NAME}}

**Date**: {{DATE}}
**Figma**: {{FIGMA_LINK}}
**Reviewer**: Navigator Product Design Skill

---

## Summary

{{SUMMARY_DESCRIPTION}}

**Changes Overview**:
- Design Tokens: {{NEW_TOKENS_COUNT}} new, {{MODIFIED_TOKENS_COUNT}} modified
- Components: {{NEW_COMPONENTS_COUNT}} new, {{EXTEND_COMPONENTS_COUNT}} to extend
- Breaking Changes: {{BREAKING_CHANGES_COUNT}}

---

## New Design Tokens

### Colors
{{#each NEW_COLOR_TOKENS}}
- **{{name}}**: `{{value}}` ({{type}})
  {{#if description}}_{{description}}_{{/if}}
{{/each}}

### Spacing
{{#each NEW_SPACING_TOKENS}}
- **{{name}}**: `{{value}}`
{{/each}}

### Typography
{{#each NEW_TYPOGRAPHY_TOKENS}}
- **{{name}}**: `{{value}}`
{{/each}}

### Other Tokens
{{#each OTHER_TOKENS}}
- **{{name}}**: `{{value}}` ({{type}})
{{/each}}

---

## Modified Design Tokens

{{#each MODIFIED_TOKENS}}
### {{path}}
- **Old Value**: `{{old_value}}`
- **New Value**: `{{new_value}}`
- **Impact**: {{impact_description}}
{{/each}}

{{#if NO_MODIFIED_TOKENS}}
_No tokens modified - all changes are additive._
{{/if}}

---

## New Components Required

### Atoms (Basic Elements)

{{#each ATOM_COMPONENTS}}
#### {{name}}

**Purpose**: {{purpose}}
**Variants**: {{variants}}
**States**: {{states}}
**Similar to**: {{similar_component}} ({{similarity_score}}% match)

**Recommendation**: {{recommendation}}
{{/each}}

### Molecules (Simple Combinations)

{{#each MOLECULE_COMPONENTS}}
#### {{name}}

**Purpose**: {{purpose}}
**Composition**: {{composition}}
**Variants**: {{variants}}
**Similar to**: {{similar_component}} ({{similarity_score}}% match)

**Recommendation**: {{recommendation}}
{{/each}}

### Organisms (Complex Components)

{{#each ORGANISM_COMPONENTS}}
#### {{name}}

**Purpose**: {{purpose}}
**Composition**: {{composition}}
**Responsive**: {{responsive_behavior}}
**Similar to**: {{similar_component}} ({{similarity_score}}% match)

**Recommendation**: {{recommendation}}
{{/each}}

---

## Component Reuse Opportunities

{{#each REUSE_OPPORTUNITIES}}
### {{figma_component}} → Extend {{existing_component}}

**Similarity**: {{similarity}}%
**Recommendation**: {{recommendation}}
**Time Saved**: {{time_saved}}

**Approach**: {{approach_description}}
{{/each}}

{{#if NO_REUSE_OPPORTUNITIES}}
_No reuse opportunities identified - all components are net new._
{{/if}}

---

## Design System Impact

### Token Health

- **In Sync**: {{IN_SYNC_COUNT}} tokens
- **Drift Detected**: {{DRIFT_COUNT}} tokens
- **Missing in Code**: {{MISSING_COUNT}} tokens
- **Unused in Design**: {{UNUSED_COUNT}} tokens

**Sync Status**: {{SYNC_STATUS}}
**Priority Level**: {{PRIORITY_LEVEL}}

### High Impact Changes

{{#each HIGH_IMPACT_CHANGES}}
- {{change_description}}
  - **Impact**: {{impact_type}}
  - **Action Required**: {{action_required}}
{{/each}}

### Low Impact Changes

{{#each LOW_IMPACT_CHANGES}}
- {{change_description}}
{{/each}}

---

## Implementation Recommendations

### Phased Approach

**Phase 1: Design Tokens** ({{PHASE_1_HOURS}} hours)
- Priority: {{PHASE_1_PRIORITY}}
- Add {{NEW_TOKENS_COUNT}} new tokens to design-tokens.json
- Update {{MODIFIED_TOKENS_COUNT}} existing tokens
- Run Style Dictionary build
- Update Tailwind @theme

**Phase 2: Atomic Components** ({{PHASE_2_HOURS}} hours)
- Priority: {{PHASE_2_PRIORITY}}
{{#each ATOM_COMPONENTS}}
- Implement {{name}} ({{complexity}}, {{estimated_hours}}h)
{{/each}}

**Phase 3: Molecule Components** ({{PHASE_3_HOURS}} hours)
- Priority: {{PHASE_3_PRIORITY}}
{{#each MOLECULE_COMPONENTS}}
- Implement {{name}} ({{complexity}}, {{estimated_hours}}h)
{{/each}}

**Phase 4: Organism Components** ({{PHASE_4_HOURS}} hours)
- Priority: {{PHASE_4_PRIORITY}}
{{#each ORGANISM_COMPONENTS}}
- Implement {{name}} ({{complexity}}, {{estimated_hours}}h)
{{/each}}

### Total Estimated Time

**{{TOTAL_HOURS}} hours** ({{TOTAL_COMPLEXITY}} complexity)

---

## Breaking Changes

{{#each BREAKING_CHANGES}}
### {{component_name}}

**Issue**: {{issue_description}}
**Previous Mapping**: `{{previous_mapping}}`
**Recommendation**: {{recommendation}}

**Migration Steps**:
{{#each migration_steps}}
- {{step}}
{{/each}}
{{/each}}

{{#if NO_BREAKING_CHANGES}}
✅ **No breaking changes** - all updates are backward compatible.
{{/if}}

---

## Next Steps

1. **Review Implementation Plan**: `.agent/tasks/TASK-{{TASK_NUMBER}}-{{FEATURE_SLUG}}.md`
2. **Update Design Tokens**: Phase 1 implementation
3. **Implement Components**: Follow atomic design hierarchy
4. **Test & Verify**: Visual regression, accessibility, unit tests
5. **Update UI Kit Inventory**: After each component completion

---

## Design Fidelity Checklist

- [ ] All design tokens extracted and added to design system
- [ ] Component structure matches Figma composition
- [ ] Variants and states implemented correctly
- [ ] Responsive behavior preserved
- [ ] Spacing and layout match pixel-perfect
- [ ] Typography styles applied correctly
- [ ] Colors and themes consistent
- [ ] Interactive states (hover, active, disabled) implemented

---

**Generated**: {{TIMESTAMP}}
**Navigator Version**: {{NAVIGATOR_VERSION}}
**Next Review**: After implementation completion
