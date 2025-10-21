# Example: Visual Regression for Full Design System

Setup visual regression for entire design system with token validation.

---

## Scenario

You have a design system with multiple components:
- Button, Input, Card, Avatar, Badge, Modal, etc.
- Design tokens extracted from Figma (via product-design skill)
- Want to ensure pixel-perfect implementation

---

## Usage

```
"Set up visual regression for entire design system in src/components"
```

---

## What Skill Does

1. **Discovers components**: Scans `src/components/` directory
2. **Generates stories**: Creates `.stories.tsx` for each component
3. **Token validation**: Compares CSS values to design tokens
4. **Bulk setup**: Single Chromatic config for all components

---

## Generated Files

```
src/components/
├── Button/
│   ├── Button.tsx
│   └── Button.stories.tsx       # ← Generated
├── Input/
│   ├── Input.tsx
│   └── Input.stories.tsx        # ← Generated
├── Card/
│   ├── Card.tsx
│   └── Card.stories.tsx         # ← Generated
...

chromatic.config.json              # ← Generated
.github/workflows/chromatic.yml    # ← Generated
```

---

## Integration with product-design Skill

If you used `product-design` skill to extract Figma tokens:

```
1. "Review this design from Figma"
   → Extracts tokens to tokens.json

2. "Set up visual regression for design system"
   → Generates stories with token values
   → Validates implementation matches tokens
```

---

## Token Validation Example

**Design token** (from Figma):
```json
{
  "color": {
    "primary": {
      "value": "#3B82F6"
    }
  }
}
```

**Story validation**:
```typescript
export const Primary: Story = {
  args: { variant: 'primary' },
  play: async ({ canvasElement }) => {
    const button = within(canvasElement).getByRole('button');
    const computedStyle = window.getComputedStyle(button);
    expect(computedStyle.backgroundColor).toBe('rgb(59, 130, 246)'); // #3B82F6
  },
};
```

---

## Benefits

- **Prevent drift**: Catch when code diverges from designs
- **Scale testing**: Test 50+ components in one workflow
- **Token enforcement**: Ensure design tokens are used correctly
- **Design review**: Designers see visual diffs in Chromatic

---

**Time saved**: 6-10 hours → 15 minutes (95% reduction)
**Components**: All in design system
**Tokens validated**: Automatically
