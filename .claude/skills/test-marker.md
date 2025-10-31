---
name: test-marker
description: Create a simple test marker file for POC validation
---

# Test Marker Skill

Create a marker file to signal task completion.

## Task

Create a file at the path specified by the user with timestamp content.

## Instructions

1. Ask user for marker file path if not provided
2. Create the file with current timestamp
3. Confirm creation

## Example

User: "Create marker at .agent/tasks/poc-plan"
Assistant: Creates file `.agent/tasks/poc-plan` with timestamp content
