#!/usr/bin/env python3
"""
Skill Generator - Example predefined function for nav-skill-creator

This is a reference implementation showing how predefined functions work.
Actual implementations will vary based on the skill being created.
"""

from typing import Dict, List, Optional


def generate_skill_structure(
    skill_name: str,
    description: str,
    triggers: List[str],
    tools: List[str] = None
) -> Dict[str, str]:
    """
    Generate basic skill structure with YAML frontmatter and markdown body.

    Args:
        skill_name: Name of the skill (kebab-case)
        description: When to auto-invoke and what the skill does
        triggers: List of phrases that should auto-invoke the skill
        tools: List of allowed tools (default: Read, Write, Edit, Grep, Glob, Bash)

    Returns:
        Dictionary with 'frontmatter' and 'body' keys containing the generated content

    Example:
        >>> generate_skill_structure(
        ...     "example-skill",
        ...     "Example skill for demo",
        ...     ["create example", "add example"]
        ... )
        {'frontmatter': '---\\nname: example-skill\\n...', 'body': '# Example Skill\\n...'}
    """
    if tools is None:
        tools = ["Read", "Write", "Edit", "Grep", "Glob", "Bash"]

    # Generate YAML frontmatter
    frontmatter = f"""---
name: {skill_name}
description: {description}
allowed-tools: {', '.join(tools)}
version: 1.0.0
---"""

    # Generate markdown body
    trigger_list = '\n'.join([f'- "{trigger}"' for trigger in triggers])

    body = f"""
# {skill_name.replace('-', ' ').title()}

[Brief description of what this skill does]

## When to Invoke

Auto-invoke when user says:
{trigger_list}

## What This Does

1. [Step 1 overview]
2. [Step 2 overview]
3. [Step 3 overview]

## Execution Steps

### Step 1: [Step Name]

[Detailed instructions for this step]

### Step 2: [Step Name]

[Detailed instructions for this step]

### Step 3: [Step Name]

[Detailed instructions for this step]

---

## Output Format

```
✅ [Task Complete]

[Summary of what was generated or accomplished]
```

---

## Best Practices

- [Best practice 1]
- [Best practice 2]
- [Best practice 3]

---

**[Closing statement about the skill]**
"""

    return {
        'frontmatter': frontmatter,
        'body': body.strip(),
        'full': f"{frontmatter}\n\n{body.strip()}"
    }


def validate_skill_name(name: str) -> tuple[bool, Optional[str]]:
    """
    Validate skill name follows conventions.

    Args:
        name: Skill name to validate

    Returns:
        Tuple of (is_valid, error_message)

    Example:
        >>> validate_skill_name("my-skill")
        (True, None)
        >>> validate_skill_name("MySkill")
        (False, "Skill name must be kebab-case")
    """
    import re

    if not name:
        return False, "Skill name cannot be empty"

    if not re.match(r'^[a-z][a-z0-9]*(-[a-z0-9]+)*$', name):
        return False, "Skill name must be kebab-case (lowercase, hyphens only)"

    if len(name) > 50:
        return False, "Skill name too long (max 50 characters)"

    return True, None


def format_tool_list(tools: List[str]) -> str:
    """
    Format list of tools for YAML frontmatter.

    Args:
        tools: List of tool names

    Returns:
        Comma-separated string of tools

    Example:
        >>> format_tool_list(["Read", "Write", "Edit"])
        'Read, Write, Edit'
    """
    return ', '.join(tools)


if __name__ == "__main__":
    # Example usage
    result = generate_skill_structure(
        skill_name="example-generator",
        description="Generate examples following project patterns",
        triggers=["create example", "add example", "new example"]
    )

    print("Generated Skill:")
    print("=" * 50)
    print(result['full'])
    print("=" * 50)

    # Validate some names
    test_names = ["my-skill", "MySkill", "my_skill", "skill-123"]
    print("\nValidation Tests:")
    for name in test_names:
        valid, error = validate_skill_name(name)
        status = "✅" if valid else "❌"
        print(f"{status} {name}: {error or 'Valid'}")
