#!/usr/bin/env python3
"""
Command Validator - Validate Navigator slash command files

Validates command markdown files follow Navigator conventions and standards.
"""

import re
from typing import List, Tuple, Optional
from pathlib import Path


def validate_command_file(file_path: str) -> Tuple[bool, List[str]]:
    """
    Validate complete command markdown file.

    Args:
        file_path: Path to command .md file

    Returns:
        Tuple of (is_valid, list_of_errors)

    Example:
        >>> valid, errors = validate_command_file("commands/marker.md")
        >>> valid or len(errors) > 0
        True
    """
    errors = []

    # Check file exists
    path = Path(file_path)
    if not path.exists():
        return False, [f"File not found: {file_path}"]

    # Read content
    try:
        content = path.read_text()
    except Exception as e:
        return False, [f"Cannot read file: {e}"]

    # Validate sections
    errors.extend(validate_frontmatter(content))
    errors.extend(validate_structure(content))
    errors.extend(validate_formatting(content))
    errors.extend(validate_style(content))

    return len(errors) == 0, errors


def validate_frontmatter(content: str) -> List[str]:
    """
    Validate YAML frontmatter.

    Args:
        content: File content

    Returns:
        List of errors (empty if valid)
    """
    errors = []

    # Check frontmatter exists
    if not content.startswith("---"):
        errors.append("Missing YAML frontmatter (must start with '---')")
        return errors

    # Extract frontmatter
    parts = content.split("---", 2)
    if len(parts) < 3:
        errors.append("Invalid frontmatter structure (must be surrounded by '---')")
        return errors

    frontmatter = parts[1].strip()

    # Check description field
    if "description:" not in frontmatter:
        errors.append("Missing 'description' field in frontmatter")
    else:
        # Extract description value
        desc_match = re.search(r'description:\s*(.+)', frontmatter)
        if desc_match:
            desc = desc_match.group(1).strip()
            if not desc:
                errors.append("Description field is empty")
            elif len(desc) > 150:
                errors.append(f"Description too long ({len(desc)} chars, max 150)")
        else:
            errors.append("Cannot parse description field")

    # Check for invalid fields (Navigator commands use minimal frontmatter)
    valid_fields = ["description", "author", "version", "deprecated"]
    for line in frontmatter.split("\n"):
        if ":" in line:
            field = line.split(":")[0].strip()
            if field and field not in valid_fields:
                errors.append(f"Unexpected frontmatter field: '{field}'")

    return errors


def validate_structure(content: str) -> List[str]:
    """
    Validate document structure and required sections.

    Args:
        content: File content

    Returns:
        List of errors (empty if valid)
    """
    errors = []

    # Extract markdown body (after frontmatter)
    parts = content.split("---", 2)
    if len(parts) < 3:
        return ["Cannot extract markdown body"]

    body = parts[2].strip()

    # Check for title (# heading)
    if not body.startswith("#"):
        errors.append("Missing main title (must start with # heading)")
    else:
        title_match = re.match(r'^#\s+(.+)$', body.split("\n")[0])
        if not title_match:
            errors.append("Invalid title format")
        else:
            title = title_match.group(1)
            # Navigator commands typically end with " - Navigator"  or context
            if "navigator" not in title.lower() and "jitd" not in title.lower():
                errors.append(f"Title should include Navigator branding: '{title}'")

    # Check for required sections (vary by complexity, so we check for minimum)
    required_keywords = ["what", "usage", "when"]
    for keyword in required_keywords:
        if keyword.lower() not in body.lower():
            errors.append(f"Missing section with '{keyword}' (recommended sections: What This Does, Usage, When to Use)")

    # Check for code blocks (commands should have examples)
    if "```" not in body:
        errors.append("No code blocks found (commands should include examples)")

    # Check for closing statement
    last_line = body.strip().split("\n")[-1]
    if not last_line.startswith("**") or not last_line.endswith("**"):
        errors.append("Missing closing statement (should be bold text at end)")

    return errors


def validate_formatting(content: str) -> List[str]:
    """
    Validate markdown formatting and syntax.

    Args:
        content: File content

    Returns:
        List of errors (empty if valid)
    """
    errors = []

    # Check for proper heading hierarchy
    headings = re.findall(r'^(#{1,6})\s+(.+)$', content, re.MULTILINE)
    prev_level = 0
    for heading, text in headings:
        level = len(heading)
        if level > prev_level + 1:
            errors.append(f"Heading hierarchy skip: {heading} {text} (jumped from h{prev_level} to h{level})")
        prev_level = level

    # Check for unclosed code blocks
    code_block_count = content.count("```")
    if code_block_count % 2 != 0:
        errors.append(f"Unclosed code block (found {code_block_count} backticks, must be even)")

    # Check for proper list formatting
    lines = content.split("\n")
    in_list = False
    for i, line in enumerate(lines, 1):
        if re.match(r'^\s*[-*+]\s+', line):
            in_list = True
            # Check indentation consistency
            if not re.match(r'^(    |\t)?[-*+]\s+\S', line):
                errors.append(f"Line {i}: Improper list item format (needs space after bullet)")
        elif in_list and line.strip() and not line.startswith(" ") and not line.startswith("\t"):
            in_list = False

    # Check for broken links (markdown links with empty href)
    broken_links = re.findall(r'\[([^\]]+)\]\(\s*\)', content)
    if broken_links:
        errors.append(f"Broken markdown links found: {broken_links}")

    return errors


def validate_style(content: str) -> List[str]:
    """
    Validate Navigator style conventions.

    Args:
        content: File content

    Returns:
        List of errors (empty if valid)
    """
    errors = []

    # Check for 2nd person perspective (Navigator style)
    first_person = ["I am", "I will", "I have", "we are", "we will", "we have"]
    for phrase in first_person:
        if phrase.lower() in content.lower():
            errors.append(f"Use 2nd person perspective ('you are') not 1st person ('{phrase}')")

    # Check emoji usage (Navigator commands use emojis sparingly)
    # Common Navigator emojis: ✅ ❌ 📖 🚀 ⚠️ 💡 🔹
    emoji_count = len(re.findall(r'[\U0001F300-\U0001F9FF]', content))
    if emoji_count > 15:
        errors.append(f"Too many emojis ({emoji_count} found, keep under 15 for professionalism)")

    # Check for proper bash/shell syntax in code blocks
    bash_blocks = re.findall(r'```(?:bash|shell|sh)\n(.*?)\n```', content, re.DOTALL)
    for block in bash_blocks:
        if "$(" in block and not re.search(r'\)\s*$', block, re.MULTILINE):
            errors.append("Potential unclosed command substitution in bash block")

    # Check for Navigator command references (should use /nav: prefix)
    nav_cmds = re.findall(r'`/(?:jitd|nav):([a-z-]+)`', content)
    jitd_cmds = re.findall(r'`/jitd:([a-z-]+)`', content)
    if len(jitd_cmds) > len(nav_cmds) * 0.5:  # More than 50% use old prefix
        errors.append("Prefer /nav: prefix over /jitd: (for consistency)")

    return errors


def validate_example_realism(content: str) -> List[str]:
    """
    Check if examples are realistic (not placeholders).

    Args:
        content: File content

    Returns:
        List of warnings (empty if examples look good)
    """
    warnings = []

    # Check for common placeholder patterns
    placeholders = [
        r'\[.*?\]',  # [placeholder]
        r'<.*?>',    # <placeholder>
        r'\.\.\.+',  # ...
        r'TODO',
        r'FIXME',
        r'XXX',
    ]

    code_blocks = re.findall(r'```.*?\n(.*?)\n```', content, re.DOTALL)
    for block in code_blocks:
        for pattern in placeholders:
            if re.search(pattern, block):
                warnings.append(f"Code block contains placeholder-like content: {pattern}")
                break  # One warning per block

    return warnings


def quick_validate(file_path: str) -> bool:
    """
    Quick validation check (returns only boolean).

    Args:
        file_path: Path to command file

    Returns:
        True if valid, False otherwise
    """
    valid, _ = validate_command_file(file_path)
    return valid


def print_validation_report(file_path: str):
    """
    Print formatted validation report.

    Args:
        file_path: Path to command file
    """
    valid, errors = validate_command_file(file_path)

    print(f"\n{'='*60}")
    print(f"Validation Report: {Path(file_path).name}")
    print(f"{'='*60}\n")

    if valid:
        print("✅ All validations passed!")
        print("\nFile is ready to use.")
    else:
        print(f"❌ Found {len(errors)} issue(s):\n")
        for i, error in enumerate(errors, 1):
            print(f"{i}. {error}")

        print("\n" + "="*60)
        print("Fix these issues before using the command.")

    print()


if __name__ == "__main__":
    import sys

    if len(sys.argv) < 2:
        print("Usage: python command_validator.py <command-file.md>")
        print("\nExample:")
        print("  python command_validator.py commands/marker.md")
        sys.exit(1)

    file_path = sys.argv[1]
    print_validation_report(file_path)

    # Exit with error code if validation failed
    if not quick_validate(file_path):
        sys.exit(1)
