# Example: Visual Regression for Simple Component

This example shows how to set up visual regression testing for a single React component.

---

## Scenario

You have a `ProfileCard` component that you want to test for visual regressions.

**Component**: `src/components/ProfileCard.tsx`

```typescript
interface ProfileCardProps {
  name: string;
  avatar: string;
  bio: string;
  size?: 'sm' | 'md' | 'lg';
  variant?: 'default' | 'compact';
}

export function ProfileCard({ name, avatar, bio, size = 'md', variant = 'default' }: ProfileCardProps) {
  // Component implementation
}
```

---

## Usage

### Step 1: Invoke Skill

```
"Set up visual regression for ProfileCard component"
```

### Step 2: Skill Auto-Invokes

Navigator detects the command and invokes `visual-regression` skill.

### Step 3: Validation

Skill executes `vr_setup_validator.py`:

```json
{
  "framework": "react",
  "storybook": {
    "installed": true,
    "version": "7.6.0"
  },
  "vr_tool": null,
  "ci_platform": "github",
  "component": {
    "valid": true,
    "path": "src/components/ProfileCard.tsx",
    "name": "ProfileCard"
  },
  "dependencies": {
    "installed": ["@storybook/react", "@storybook/addon-essentials"],
    "missing": ["chromatic", "@chromatic-com/storybook"]
  },
  "ready": true
}
```

### Step 4: Generate Story

Skill executes `story_generator.py`:

**Created**: `src/components/ProfileCard.stories.tsx`

```typescript
import type { Meta, StoryObj } from '@storybook/react';
import { ProfileCard } from './ProfileCard';

const meta = {
  title: 'Components/ProfileCard',
  component: ProfileCard,
  parameters: {
    layout: 'centered',
  },
  tags: ['autodocs'],
  argTypes: {
    size: { control: 'select', options: ['sm', 'md', 'lg'] },
    variant: { control: 'select', options: ['default', 'compact'] },
  },
} satisfies Meta<typeof ProfileCard>;

export default meta;
type Story = StoryObj<typeof meta>;

export const Default: Story = {
  args: {
    name: 'John Doe',
    avatar: 'https://via.placeholder.com/150',
    bio: 'Software Engineer',
    size: 'md',
    variant: 'default',
  },
};

export const Small: Story = {
  args: {
    ...Default.args,
    size: 'sm',
  },
};

export const Large: Story = {
  args: {
    ...Default.args,
    size: 'lg',
  },
};

export const Compact: Story = {
  args: {
    ...Default.args,
    variant: 'compact',
  },
};

// Accessibility tests
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

### Step 5: Generate Chromatic Config

Skill executes `chromatic_config_generator.py`:

**Created**: `chromatic.config.json`

```json
{
  "projectId": "<PROJECT_ID_PLACEHOLDER>",
  "buildScriptName": "build-storybook",
  "exitZeroOnChanges": true,
  "exitOnceUploaded": true,
  "onlyChanged": true,
  "externals": ["public/**"],
  "skip": "dependabot/**",
  "ignoreLastBuildOnBranch": "main"
}
```

**Updated**: `.storybook/main.js`

```diff
  addons: [
    '@storybook/addon-links',
    '@storybook/addon-essentials',
+   '@chromatic-com/storybook',
    '@storybook/addon-interactions',
  ],
```

**Updated**: `package.json`

```diff
  "scripts": {
+   "chromatic": "npx chromatic",
+   "chromatic:ci": "npx chromatic --exit-zero-on-changes",
    "build-storybook": "storybook build"
  }
```

### Step 6: Generate CI Workflow

Skill executes `ci_workflow_generator.py`:

**Created**: `.github/workflows/chromatic.yml`

```yaml
name: Visual Regression Tests

on:
  push:
    branches: ['main', 'develop']
  pull_request:
    branches: ['main']

jobs:
  chromatic:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
        with:
          fetch-depth: 0

      - name: Setup Node.js
        uses: actions/setup-node@v4
        with:
          node-version: '20'
          cache: 'npm'

      - name: Install dependencies
        run: npm ci

      - name: Run Chromatic
        uses: chromaui/action@latest
        with:
          projectToken: ${{ secrets.CHROMATIC_PROJECT_TOKEN }}
          exitZeroOnChanges: true
          onlyChanged: true
          autoAcceptChanges: 'main'
```

### Step 7: Setup Instructions

Skill outputs:

```markdown
✅ Visual regression testing setup complete!

## Files Created/Modified

✅ ProfileCard.stories.tsx (Storybook story with 4 variants)
✅ chromatic.config.json (Chromatic configuration)
✅ .storybook/main.js (Added @chromatic-com/storybook addon)
✅ package.json (Added chromatic scripts)
✅ .github/workflows/chromatic.yml (CI workflow)

## Next Steps

### 1. Install Dependencies

```bash
npm install --save-dev chromatic @chromatic-com/storybook
```

### 2. Create Chromatic Project

1. Go to https://www.chromatic.com/start
2. Sign in with GitHub
3. Create new project
4. Copy project token

### 3. Add Secret to GitHub

1. Go to repository Settings → Secrets and variables → Actions
2. Create secret: `CHROMATIC_PROJECT_TOKEN`
3. Paste your project token

### 4. Update chromatic.config.json

Replace `<PROJECT_ID_PLACEHOLDER>` with your actual project ID.

### 5. Create Baseline

```bash
npm run chromatic
```

### 6. Test Visual Regression

1. Make a visual change to ProfileCard
2. Commit and push
3. CI will run Chromatic automatically
4. Review changes in Chromatic dashboard
```

---

## Result

**Time saved**: 2-3 hours → 5 minutes (96% reduction)

**Files created**: 4
**Lines of code generated**: ~150
**Token usage**: 3k tokens (vs 50k manual)

---

## Follow-up Tasks

After setup, you can:

1. **Add more variants**: Edit `ProfileCard.stories.tsx` to add edge cases
2. **Customize Chromatic**: Adjust `chromatic.config.json` settings
3. **Add interaction tests**: Use `@storybook/test` for click/focus states
4. **Review visual diffs**: Monitor Chromatic dashboard for changes

---

**Skill used**: visual-regression
**Time to complete**: ~5 minutes
**Automated**: Story generation, config creation, CI setup
