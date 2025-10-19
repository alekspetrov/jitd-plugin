#!/usr/bin/env python3
"""
Command Generator - Generate Navigator slash command markdown files

Generates properly structured command files following Navigator conventions.
"""

from typing import Dict, List, Optional
from datetime import datetime


def generate_command(
    name: str,
    description: str,
    complexity: str = "medium",
    sections: Optional[Dict] = None
) -> str:
    """
    Generate complete Navigator command markdown file.

    Args:
        name: Command name (kebab-case, without /nav: prefix)
        description: One-line purpose description
        complexity: Command complexity level ("simple", "medium", "complex")
        sections: Dictionary of section content (optional, uses templates if not provided)

    Returns:
        Complete markdown content for the command file

    Example:
        >>> content = generate_command(
        ...     name="example",
        ...     description="Example command for testing",
        ...     complexity="simple"
        ... )
        >>> "---" in content and "description:" in content
        True
    """
    if sections is None:
        sections = {}

    # Validate inputs
    valid, error = validate_command_name(name)
    if not valid:
        raise ValueError(f"Invalid command name: {error}")

    if complexity not in ["simple", "medium", "complex"]:
        raise ValueError(f"Complexity must be 'simple', 'medium', or 'complex', got: {complexity}")

    # Generate frontmatter
    frontmatter = f"""---
description: {description}
---"""

    # Generate title
    title = f"# {format_title(name)}"

    # Generate content based on complexity
    if complexity == "simple":
        content = generate_simple_command(name, description, sections)
    elif complexity == "medium":
        content = generate_medium_command(name, description, sections)
    else:  # complex
        content = generate_complex_command(name, description, sections)

    # Combine all parts
    return f"{frontmatter}\n\n{title}\n\n{content}"


def generate_simple_command(name: str, description: str, sections: Dict) -> str:
    """Generate content for a simple command."""
    what_this_does = sections.get("what_this_does", f"[Explain what /nav:{name} does in 2-3 sentences]")
    usage = sections.get("usage", f"/nav:{name}")
    when_to_use = sections.get("when_to_use", [
        "Scenario 1",
        "Scenario 2",
        "Scenario 3"
    ])
    output_format = sections.get("output_format", "[Example output]")
    troubleshooting = sections.get("troubleshooting", {
        "Issue 1": "Solution 1",
        "Issue 2": "Solution 2"
    })

    # Build when_to_use section
    when_to_use_content = "\n\n".join([
        f"**{scenario}**:\n```\n[Example]\n```" for scenario in when_to_use
    ])

    # Build troubleshooting section
    troubleshooting_content = "\n\n".join([
        f"### {issue}\n\n**Problem**: [Description]\n\n**Solution**:\n{solution}"
        for issue, solution in troubleshooting.items()
    ])

    return f"""## What This Does

{what_this_does}

---

## Usage

```bash
{usage}
```

---

## When to Use

{when_to_use_content}

---

## Output Format

```
{output_format}
```

---

## Troubleshooting

{troubleshooting_content}

---

**[Closing statement about the command]** 🚀"""


def generate_medium_command(name: str, description: str, sections: Dict) -> str:
    """Generate content for a medium complexity command."""
    overview = sections.get("overview", f"You are using Navigator's `/nav:{name}` command.\n\n[Explain context and purpose]")
    what_this_does = sections.get("what_this_does", "[Detailed explanation with comparisons]")
    when_to_use = sections.get("when_to_use", [f"Scenario {i+1}" for i in range(5)])
    execution_steps = sections.get("execution_steps", [f"Step {i+1}" for i in range(3)])
    troubleshooting = sections.get("troubleshooting", {f"Issue {i+1}": f"Solution {i+1}" for i in range(4)})

    # Build when_to_use section
    when_to_use_content = "\n\n".join([
        f"**{scenario}**:\n```\n[Example]\n```" for scenario in when_to_use
    ])

    # Build execution steps
    execution_content = "\n\n".join([
        f"### {step}\n\n[Instructions for this step]\n\n**Expected outcome**: [What happens]"
        for step in execution_steps
    ])

    # Build troubleshooting
    troubleshooting_content = "\n\n".join([
        f"### {issue}\n\n**Problem**: [Description]\n\n**Solutions**:\n1. {solution}\n2. [Additional solution]\n3. [Additional solution]"
        for issue, solution in troubleshooting.items()
    ])

    return f"""{overview}

---

## What This Does

{what_this_does}

---

## When to Use

{when_to_use_content}

---

## Execution Steps

{execution_content}

---

## Output Format

```
[Expected output format]
```

---

## Best Practices

- [Best practice 1]
- [Best practice 2]
- [Best practice 3]

---

## Troubleshooting

{troubleshooting_content}

---

**[Closing statement emphasizing key benefit]** 🚀"""


def generate_complex_command(name: str, description: str, sections: Dict) -> str:
    """Generate content for a complex command."""
    return f"""You are executing the `/nav:{name}` command.

[Comprehensive overview explaining the command's role in Navigator workflow]

---

## What This Does

[Detailed explanation with comparisons to alternative approaches]

**Traditional approach**: [Manual process]

**With `/nav:{name}`**:
- [Benefit 1]
- [Benefit 2]
- [Benefit 3]

---

## EXECUTION PLAN

You will execute these steps in order. Each step has explicit outcomes.

---

### Step 1: Pre-Flight Checks

[Validation and preparation steps]

**Checks**:
- [ ] Check 1
- [ ] Check 2
- [ ] Check 3

---

### Step 2: [Main Operation]

[Detailed implementation instructions]

**Process**:
1. [Substep 1]
2. [Substep 2]
3. [Substep 3]

**Expected outcome**: [What should happen]

---

### Step 3: Validation

[Verification steps]

**Verify**:
- [ ] Verification 1
- [ ] Verification 2
- [ ] Verification 3

---

### Step 4: Completion

[Finalization and user feedback]

**Show summary**:
```
✅ [Success message]

[Summary of what was accomplished]
```

---

## Integration Notes

[How this command integrates with other Navigator features or external tools]

---

## Success Criteria

**This command succeeds when**:
- [ ] Criterion 1
- [ ] Criterion 2
- [ ] Criterion 3
- [ ] Criterion 4

---

## Troubleshooting

### Common Issue 1

**Error**: [Error message or symptom]

**Solution**:
[Detailed solution with commands]

### Common Issue 2

**Error**: [Error message or symptom]

**Solution**:
[Detailed solution]

### Edge Case 1

**Scenario**: [When this happens]

**Handling**:
[How to handle this case]

---

## Performance Notes

[Any performance considerations, optimization tips, or scalability notes]

---

**[Comprehensive closing statement]** 🚀"""


def validate_command_name(name: str) -> tuple[bool, Optional[str]]:
    """
    Validate command name follows Navigator conventions.

    Args:
        name: Command name to validate

    Returns:
        Tuple of (is_valid, error_message)

    Example:
        >>> validate_command_name("my-command")
        (True, None)
        >>> validate_command_name("MyCommand")
        (False, 'Command name must be kebab-case')
    """
    import re

    if not name:
        return False, "Command name cannot be empty"

    if not re.match(r'^[a-z][a-z0-9]*(-[a-z0-9]+)*$', name):
        return False, "Command name must be kebab-case (lowercase, hyphens only)"

    if len(name) > 50:
        return False, "Command name too long (max 50 characters)"

    # Reserved names
    reserved = ["help", "clear", "reset"]
    if name in reserved:
        return False, f"Command name '{name}' is reserved"

    return True, None


def format_title(name: str) -> str:
    """
    Format command name as title.

    Args:
        name: Command name (kebab-case)

    Returns:
        Formatted title string

    Example:
        >>> format_title("update-doc")
        'Update Doc - Navigator'
        >>> format_title("marker")
        'Marker - Navigator'
    """
    # Convert kebab-case to Title Case
    title = name.replace('-', ' ').title()

    # Add Navigator branding
    return f"{title} - Navigator"


def generate_description(name: str, purpose: str) -> str:
    """
    Generate command description for YAML frontmatter.

    Args:
        name: Command name
        purpose: Brief purpose statement

    Returns:
        Formatted description (under 100 chars)

    Example:
        >>> desc = generate_description("marker", "save conversation state")
        >>> len(desc) < 100
        True
    """
    # Ensure it starts with a verb and is concise
    if len(purpose) > 90:
        purpose = purpose[:87] + "..."

    return purpose


if __name__ == "__main__":
    # Example usage
    print("Generating simple command...")
    simple = generate_command(
        name="example",
        description="Example command for demonstration",
        complexity="simple"
    )

    print("\n" + "=" * 50)
    print(simple[:500] + "...")
    print("=" * 50)

    # Validate names
    test_names = ["my-command", "MyCommand", "my_command", "valid-name-123"]
    print("\nValidation Tests:")
    for name in test_names:
        valid, error = validate_command_name(name)
        status = "✅" if valid else "❌"
        print(f"{status} {name}: {error or 'Valid'}")
