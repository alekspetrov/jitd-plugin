---
name: example-feature-generator
description: Generate boilerplate for new features following project conventions. Use when user says "create feature", "add feature", or "new feature scaffolding".
allowed-tools: Read, Write, Edit, Grep, Glob, Bash
version: 1.0.0
---

# Example Feature Generator

This is an example of a generated skill created by nav-skill-creator.

## When to Invoke

Auto-invoke when user says:
- "Create a new feature"
- "Add feature scaffolding"
- "Generate feature boilerplate"

## What This Does

1. Asks for feature name and type
2. Analyzes existing features for patterns
3. Generates feature files following project conventions
4. Creates tests and documentation

## Execution Steps

### Step 1: Gather Feature Requirements

Ask user:
- Feature name (kebab-case)
- Feature type (API, UI, background job, etc.)
- Dependencies needed
- Testing requirements

### Step 2: Analyze Existing Patterns

Use Task agent to explore codebase:
```
"Find existing features similar to [feature-type]:
 - Locate feature files
 - Identify structure patterns
 - Extract naming conventions
 - Find test patterns"
```

### Step 3: Generate Feature Files

Use predefined function: `functions/feature_generator.py`

```python
# Generates feature structure based on analysis
generate_feature(name, feature_type, config)
```

Creates:
- Feature implementation file
- Test file
- Configuration file (if needed)
- Documentation stub

### Step 4: Validate Generated Files

Check:
- [ ] Files follow naming conventions
- [ ] Imports are correct
- [ ] Tests are generated
- [ ] Documentation is created

### Step 5: Show Summary

Display created files and next steps for user.

---

## Output Format

```
✅ Feature Created: [feature-name]

Files generated:
- features/[feature-name]/index.ts
- features/[feature-name]/[feature-name].test.ts
- features/[feature-name]/README.md

Next steps:
1. Implement feature logic in index.ts
2. Add test cases in [feature-name].test.ts
3. Document usage in README.md
```

---

**This is an example - actual generated skills will vary based on project patterns**
