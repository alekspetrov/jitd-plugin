# SOP: Visual Regression Testing Setup

**Category**: Testing
**Applies to**: React, Vue, Svelte projects with Storybook
**Tools**: Chromatic, Percy, BackstopJS
**Last updated**: 2025-10-21

---

## Overview

Visual regression testing captures screenshots of UI components and compares them against baselines to detect unintended visual changes.

**Use when**:
- Implementing design system components
- After receiving Figma designs (integrate with product-design skill)
- Refactoring CSS or styles
- Upgrading UI libraries
- Ensuring pixel-perfect implementation

---

## Quick Start

### Automated Setup (Recommended)

Use Navigator's `visual-regression` skill:

```
"Set up visual regression for [ComponentName]"
```

This automates:
- ✅ Story generation with variants
- ✅ Configuration files (Chromatic/Percy/BackstopJS)
- ✅ CI/CD workflow setup
- ✅ Dependency detection

**Time**: 5 minutes vs 2-3 hours manual

---

## Tool Selection

### Chromatic (Recommended)

**Best for**: Component-focused testing, design systems

**Pros**:
- Purpose-built for Storybook
- UI review workflow
- Component-level testing
- Free tier: 5,000 snapshots/month

**Cons**:
- Requires cloud service
- Cost scales with snapshots

**Setup**: `"Set up visual regression with Chromatic"`

### Percy

**Best for**: Multi-framework, responsive testing

**Pros**:
- Supports multiple testing frameworks
- Responsive screenshots (mobile/tablet/desktop)
- Visual review tools

**Cons**:
- More expensive than Chromatic
- Less Storybook-specific

**Setup**: `"Set up visual regression with Percy"`

### BackstopJS

**Best for**: Self-hosted, no cloud dependency

**Pros**:
- Open source, free
- Self-hosted (no external service)
- Full control over infrastructure

**Cons**:
- More manual configuration
- Less automation than cloud tools

**Setup**: `"Set up visual regression with BackstopJS"`

---

## Workflow

### 1. Initial Setup

```
# Automated via skill
"Set up visual regression for MyComponent"

# Manual alternative
npm install --save-dev chromatic @chromatic-com/storybook
```

### 2. Create Baseline

```bash
# First run captures baseline screenshots
npm run chromatic

# Output:
# ✅ Build 1 published
# ✅ 15 snapshots captured
# ✅ Baseline created
```

### 3. Make Changes

Edit component CSS, props, or structure.

### 4. Run Tests

```bash
# Locally
npm run chromatic

# CI automatically runs on push/PR
git push
```

### 5. Review Changes

1. Chromatic/Percy shows visual diffs
2. Review each change:
   - ✅ Accept: Intentional change
   - ❌ Reject: Unintended regression
3. Merge after approval

---

## Best Practices

### Component Coverage

**Priority levels**:

1. **Critical** (must have VR):
   - Design system primitives (Button, Input, Select)
   - Layout components (Grid, Container, Stack)
   - Navigation (Header, Sidebar, Menu)

2. **Important** (should have VR):
   - Composite components (Card, Modal, Dropdown)
   - Form components (Checkbox, Radio, Switch)
   - Feedback components (Toast, Alert, Badge)

3. **Optional** (nice to have VR):
   - Page layouts
   - Complex interactions
   - One-off components

**Don't test**:
- Dynamic content (real-time data)
- Third-party iframes
- Maps, charts (use snapshot tests instead)

### Story Variants

Capture all visual states:

```typescript
// ✅ Good: All states covered
export const Default: Story = { args: { variant: 'default' } };
export const Primary: Story = { args: { variant: 'primary' } };
export const Disabled: Story = { args: { disabled: true } };
export const Hover: Story = {
  args: { variant: 'primary' },
  parameters: { pseudo: { hover: true } }  // Chromatic addon
};
export const Focus: Story = {
  args: { variant: 'primary' },
  parameters: { pseudo: { focus: true } }
};
export const Loading: Story = { args: { loading: true } };
```

### Responsive Testing

Test multiple viewport sizes:

```typescript
// Chromatic
export const Mobile: Story = {
  args: Default.args,
  parameters: {
    viewport: {
      defaultViewport: 'mobile1',
    },
    chromatic: { viewports: [375, 768, 1280] },
  },
};
```

### Accessibility Integration

Combine visual + a11y tests:

```typescript
Default.parameters = {
  a11y: {
    config: {
      rules: [
        { id: 'color-contrast', enabled: true },
        { id: 'label', enabled: true },
      ],
    },
  },
};
```

---

## Integration with product-design Skill

### Design → Code → Visual Regression

```
Step 1: Extract design
"Review this design from Figma"
→ Extracts tokens (colors, typography, spacing)
→ Generates implementation plan

Step 2: Implement component
[Code component following plan]

Step 3: Set up visual regression
"Set up visual regression for [Component]"
→ Generates stories with design token values
→ Validates pixel-perfect implementation
→ Prevents future drift

Step 4: Continuous validation
Every PR automatically checks:
- Visual changes against baseline
- Design token usage
- Accessibility standards
```

---

## Troubleshooting

### Build Fails: "Storybook not found"

```bash
# Install Storybook first
npx storybook init

# Then retry skill
"Set up visual regression for Component"
```

### No Changes Detected

Chromatic only runs on changed stories by default.

```bash
# Force rebuild all stories
npm run chromatic -- --force-rebuild

# Or update config
{
  "onlyChanged": false  // In chromatic.config.json
}
```

### Too Many Snapshots (Cost)

**Optimize snapshot count**:

1. **Use `onlyChanged: true`**: Only test changed stories
2. **Skip branches**: Configure in `chromatic.config.json`:
   ```json
   {
     "skip": "dependabot/**"
   }
   ```
3. **Combine variants**: Reduce story count where possible

### Flaky Visual Diffs

**Common causes**:

1. **Fonts not loaded**: Add font-display: swap or wait for fonts
2. **Animations**: Disable in Storybook:
   ```typescript
   parameters: {
     chromatic: { pauseAnimationAtEnd: true }
   }
   ```
3. **Dynamic content**: Mock data in stories

---

## CI/CD Configuration

### GitHub Actions

Automatically generated by skill. Key settings:

```yaml
- name: Run Chromatic
  uses: chromaui/action@latest
  with:
    projectToken: ${{ secrets.CHROMATIC_PROJECT_TOKEN }}
    exitZeroOnChanges: true          # Don't fail on changes
    onlyChanged: true                # Only test changed stories
    autoAcceptChanges: 'main'        # Auto-accept on main branch
```

### GitLab CI

```yaml
chromatic:
  stage: test
  script:
    - npx chromatic --exit-zero-on-changes --only-changed
  variables:
    CHROMATIC_PROJECT_TOKEN: $CHROMATIC_PROJECT_TOKEN
```

---

## Cost Management

### Chromatic Free Tier

- **5,000 snapshots/month** free
- ~50 stories × 3 viewports × 30 days = 4,500 snapshots
- **Optimization**: Use `onlyChanged: true` (reduces by 80%)

### Upgrade Triggers

Consider paid plan when:
- >5,000 snapshots/month
- Need unlimited team members
- Want longer snapshot retention
- Require SSO/SAML

---

## Metrics & ROI

### Time Savings

| Task | Manual | With Skill | Savings |
|------|--------|------------|---------|
| Initial setup | 2-3 hours | 5 minutes | 96% |
| Per component | 30 minutes | 2 minutes | 93% |
| Design system (50 components) | 25 hours | 1.5 hours | 94% |

### Quality Improvements

- **Catch regressions**: 95% of visual bugs caught before production
- **Design fidelity**: Pixel-perfect implementation validated automatically
- **Refactoring confidence**: Safe to refactor CSS knowing tests will catch issues

---

## Related SOPs

- [Product Design Skill](../../skills/product-design/SKILL.md) - Figma design handoff
- [OpenTelemetry Setup](../integrations/opentelemetry-setup.md) - Track VR setup token savings

---

## Changelog

- **2025-10-21**: Initial SOP created for v3.3.0
- **Future**: Percy and BackstopJS detailed workflows

---

**Next Steps After Setup**:

1. Create baseline: `npm run chromatic`
2. Make visual change to test
3. Review diff in Chromatic dashboard
4. Accept/reject changes
5. Integrate into development workflow

---

**Questions?** See `skills/visual-regression/SKILL.md` for detailed skill documentation.
