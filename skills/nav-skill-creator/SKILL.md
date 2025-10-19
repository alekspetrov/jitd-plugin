---
name: nav-skill-creator
description: Analyze codebase patterns and create custom skills for repetitive workflows. Use when project needs automation or pattern enforcement. Auto-invoke when user says "create a skill for...", "automate this workflow", or "we keep doing X manually".
allowed-tools: Read, Write, Edit, Grep, Glob, Bash, Task
version: 1.0.0
---

# Navigator Skill Creator

Create project-specific skills by analyzing codebase patterns and automating repetitive workflows.

## When to Invoke

Auto-invoke when user mentions:
- "Create a skill for [pattern]"
- "Automate this workflow"
- "We keep doing X manually"
- "Enforce this pattern"
- "Generate boilerplate for [feature type]"
- "We need consistency for [task type]"

## What This Does

1. Analyzes codebase to understand project patterns
2. Identifies best practices from existing code
3. Generates skill with:
   - Auto-invocation triggers
   - Predefined functions
   - Templates
   - Examples
4. Tests the generated skill
5. Documents the new skill

## Execution Steps

### Step 1: Understand Skill Request

Ask clarifying questions:
- What pattern/workflow to automate?
- What triggers should invoke this skill?
- What output format is expected?
- Are there existing examples in the codebase?

**Example dialogue**:
```
User: "Create a skill for adding React components"