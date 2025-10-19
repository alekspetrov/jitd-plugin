#!/usr/bin/env python3
"""
Format Standard Operating Procedure markdown with proper structure.
"""

import sys
import argparse
from datetime import datetime

def format_sop(title, category, problem="", solution="", when_to_use=""):
    """
    Generate formatted SOP markdown.

    Args:
        title: SOP title (e.g., "Linear MCP Setup")
        category: SOP category (integrations, debugging, development, deployment)
        problem: Problem description
        solution: Solution steps
        when_to_use: When to use this SOP

    Returns:
        str: Formatted markdown content
    """
    today = datetime.now().strftime("%Y-%m-%d")

    template = f"""# {title}

**Category**: {category}
**Created**: {today}
**Last Updated**: {today}

---

## When to Use This SOP

{when_to_use or "[Describe when this SOP applies]"}

**Triggers**:
- [Situation 1]
- [Situation 2]
- [Situation 3]

---

## Problem Statement

{problem or "[Describe the problem this SOP solves]"}

**Symptoms**:
- [Symptom 1]
- [Symptom 2]

**Root Cause**: [Why does this problem occur?]

---

## Solution

### Prerequisites

- [Requirement 1]
- [Requirement 2]

### Step-by-Step Instructions

#### Step 1: [Action Name]

```bash
# Example command
command --flag value
```

**Expected Output**:
```
[Show what success looks like]
```

**If this fails**:
- Check [common issue 1]
- Verify [common issue 2]

#### Step 2: [Next Action]

[Continue with detailed steps...]

---

## Verification

**How to verify the solution worked**:

```bash
# Verification command
test-command
```

**Expected Result**: [What you should see]

---

## Troubleshooting

### Issue: [Common Problem]

**Symptoms**: [How you know this is happening]

**Solution**:
1. [Fix step 1]
2. [Fix step 2]

### Issue: [Another Problem]

**Symptoms**: [Indicators]

**Solution**: [How to fix]

---

## Related SOPs

- [Link to related procedure 1]
- [Link to related procedure 2]

---

## Notes

- [Important considerations]
- [Edge cases to be aware of]
- [Future improvements needed]

---

**Created**: {today}
**Category**: {category}
**Maintained By**: Navigator System
"""
    return template

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Format Navigator SOP markdown")
    parser.add_argument("--title", required=True, help="SOP title")
    parser.add_argument("--category", required=True,
                       choices=["integrations", "debugging", "development", "deployment"],
                       help="SOP category")
    parser.add_argument("--problem", default="", help="Problem description")
    parser.add_argument("--solution", default="", help="Solution steps")
    parser.add_argument("--when", default="", help="When to use this SOP")

    args = parser.parse_args()

    output = format_sop(
        title=args.title,
        category=args.category,
        problem=args.problem,
        solution=args.solution,
        when_to_use=args.when
    )

    print(output)
