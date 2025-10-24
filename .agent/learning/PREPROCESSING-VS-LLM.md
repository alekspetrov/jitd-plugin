# Preprocessing vs LLM: The Right Tool for the Job

**Part of**: Navigator v4.0 Education Layer
**Level**: Fundamental
**Read Time**: 10 minutes
**Prerequisites**: [CONTEXT-BUDGETS.md](./CONTEXT-BUDGETS.md)

---

## The Core Principle

**Not every problem needs an LLM.**

In fact, forcing LLMs to solve deterministic problems wastes tokens, time, and accuracy.

**Navigator's principle**: Use preprocessing (scripts, functions, tools) for structured tasks. Reserve LLMs for semantic understanding.

---

## The Realization

### v3.4.0: The Figma Integration That Proved It

**Problem**: Extract design tokens from Figma (colors, typography, spacing)

**Attempted Solution 1: LLM Extraction**
```
Prompt: "Extract all colors, typography, and spacing from this Figma file"

Result:
├── Colors: 78% accurate
├── Typography: 65% accurate (missed font weights)
├── Spacing: 45% accurate (confused margins/padding)
├── Token cost: 45k tokens
└── Time: 12 minutes
```

**Attempted Solution 2: Preprocessing + LLM**
```
1. Preprocessing (Python):
   - Extract raw Figma JSON via API
   - Parse colors → DTCG format (deterministic)
   - Parse typography → structured data
   - Parse spacing → consistent values
   Result: 98% accurate, 0 tokens, 30 seconds

2. LLM (Semantic Layer):
   - Match components to design system
   - Identify naming inconsistencies
   - Suggest implementation approach
   Result: Excellent, 3k tokens, 15 seconds

Total: 98% accurate, 3k tokens, 45 seconds
```

**Savings**: 42k tokens (93%), 11 minutes, 33% better accuracy

---

## Why LLMs Fail at Structured Tasks

### Example 1: Parsing JSON

**Task**: Extract all API endpoints from OpenAPI spec

**❌ LLM Approach**:
```
Read openapi.json → Claude Code
Prompt: "List all endpoints with methods"

Problems:
├── May miss nested endpoints
├── May hallucinate endpoints
├── May format inconsistently
├── Costs: 15k tokens for large spec
└── Accuracy: 85-90%
```

**✅ Preprocessing Approach**:
```python
import json

with open('openapi.json') as f:
    spec = json.load(f)

for path, methods in spec['paths'].items():
    for method in methods.keys():
        print(f"{method.upper()} {path}")

Result:
├── 100% accurate (no hallucinations)
├── Consistent format
├── Cost: 0 tokens
└── Time: <1 second
```

### Example 2: Counting Occurrences

**Task**: Find all files using deprecated function `getCwd()`

**❌ LLM Approach**:
```
Search codebase → Read all matches → Count

Problems:
├── Loads 20+ files into context (60k tokens)
├── May miss edge cases (strings, comments)
├── Slow (reads every file in full)
└── Accuracy: ~80% (pattern matching is fuzzy)
```

**✅ Preprocessing Approach**:
```bash
grep -r "getCwd" --include="*.ts" | wc -l
# Or use Grep tool

Result:
├── 100% accurate
├── Cost: 0 tokens (tool execution)
├── Time: <1 second
└── Shows exact locations
```

### Example 3: Formatting Dates

**Task**: Convert all dates in log file to ISO 8601

**❌ LLM Approach**:
```
Load log file → Prompt: "Convert dates to ISO 8601"

Problems:
├── May misinterpret ambiguous formats (MM/DD vs DD/MM)
├── May miss dates in edge case formats
├── Token cost: Entire file loaded
└── Risk: Data corruption if wrong
```

**✅ Preprocessing Approach**:
```python
from datetime import datetime
import re

pattern = r'(\d{2})/(\d{2})/(\d{4})'
def convert(match):
    return datetime.strptime(match.group(), '%m/%d/%Y').isoformat()

processed = re.sub(pattern, convert, log_content)

Result:
├── 100% consistent
├── No ambiguity (explicit format string)
├── Cost: 0 tokens
└── Repeatable (same input = same output)
```

---

## When to Use What

### Decision Matrix

| Task Type | Right Tool | Why |
|-----------|-----------|-----|
| **Parse structured data** | Preprocessing | Deterministic, zero error tolerance |
| **Extract specific patterns** | Preprocessing | Regex/tools faster and accurate |
| **Transform formats** | Preprocessing | Repeatable, no hallucination risk |
| **Count/aggregate** | Preprocessing | Math is deterministic |
| **Search codebase** | Agent + Preprocessing | Agent optimizes search, tools execute |
| **Understand architecture** | LLM | Semantic understanding needed |
| **Name variables** | LLM | Creative, context-aware |
| **Design component API** | LLM | Judgment call, pattern recognition |
| **Explain legacy code** | LLM | Requires inference |
| **Match similar patterns** | LLM | Semantic similarity |

---

## The Hybrid Pattern: Preprocessing → LLM

Best results come from combining both:

```
┌─────────────────────────────────────────┐
│ 1. Preprocessing (Deterministic Layer)  │
│    ├── Extract structured data          │
│    ├── Parse formats                     │
│    ├── Validate schemas                  │
│    └── Normalize values                  │
└──────────────────┬──────────────────────┘
                   │
                   ▼
┌─────────────────────────────────────────┐
│ 2. LLM (Semantic Layer)                  │
│    ├── Interpret meanings                │
│    ├── Identify patterns                 │
│    ├── Make judgments                    │
│    └── Generate human language           │
└─────────────────────────────────────────┘
```

### Example: Design Token Extraction (v3.4.0)

**Step 1: Preprocessing**
```python
# functions/token_extractor.py
def extract_colors(figma_json):
    """Extract all color values from Figma JSON."""
    colors = {}
    for node in figma_json['document']['children']:
        if node['type'] == 'RECTANGLE' and 'fills' in node:
            for fill in node['fills']:
                if fill['type'] == 'SOLID':
                    colors[node['name']] = rgb_to_hex(fill['color'])
    return colors

Result: {
  "primary-blue": "#1E40AF",
  "secondary-gray": "#6B7280",
  ...
}
# 100% accurate, 0 tokens, instant
```

**Step 2: LLM Interpretation**
```
Input to Claude Code: Extracted color tokens + existing design system

Prompt: "Match these Figma colors to our existing design system.
Flag any new colors that don't fit our palette."

LLM Output:
├── "primary-blue matches theme.colors.primary ✓"
├── "secondary-gray is close to theme.colors.gray-600 (suggest using existing)"
└── "Warning: 'accent-purple' is new - add to design system or use existing?"

# Semantic understanding, context-aware, 2k tokens
```

**Result**: Deterministic extraction + intelligent matching = 98% automation

---

## Real-World Case Studies

### Case Study 1: Codebase Refactoring

**Task**: Rename function `getCwd()` to `getCurrentWorkingDirectory()` across 50 files

**❌ Pure LLM Approach**:
```
1. Search for getCwd
2. Read all 50 files (150k tokens)
3. Ask Claude Code to rename in each file
4. Review changes

Problems:
├── 150k tokens loaded (context full)
├── May miss string occurrences
├── May change comments/docs inconsistently
└── Time: 30 minutes, multiple sessions
```

**✅ Hybrid Approach**:
```
1. Preprocessing: Search for getCwd
   grep -r "getCwd" → List of 50 files (0 tokens)

2. LLM: Strategic decision
   "Found 50 files. Strategy?"
   → Claude: "Use search/replace for function calls,
              manually review docs/comments" (2k tokens)

3. Preprocessing: Execute rename
   sed -i 's/getCwd(/getCurrentWorkingDirectory(/g' *.ts
   (0 tokens, instant, 100% consistent)

4. LLM: Review edge cases
   Show 3 comment examples → Claude confirms or adjusts
   (1k tokens)

Result: 3k tokens (98% savings), 5 minutes, 100% accurate
```

### Case Study 2: API Integration

**Task**: Integrate third-party payment API

**❌ Pure LLM Approach**:
```
1. Load API documentation (30k tokens)
2. Ask Claude to implement integration
3. Debug issues by re-reading docs

Problems:
├── 30k tokens for docs
├── May misinterpret auth flow
├── Context fills up during debugging
└── Result: Multiple restarts, 2 hours
```

**✅ Hybrid Approach**:
```
1. Preprocessing: Extract API schema
   curl api.example.com/openapi.json > schema.json
   Parse schema → List endpoints (0 tokens)

2. LLM: Design integration architecture
   "Here are the endpoints. Design integration class."
   → Claude suggests structure (5k tokens)

3. Preprocessing: Generate boilerplate
   Python script generates TypeScript interfaces from schema
   (0 tokens, perfect type safety)

4. LLM: Implement business logic
   Claude writes error handling, retries, validation
   (8k tokens, focuses on logic not structure)

5. Preprocessing: Validate integration
   curl to test all endpoints (0 tokens, instant feedback)

Result: 13k tokens (57% savings), 45 minutes, type-safe
```

### Case Study 3: Migration Script

**Task**: Migrate 100 user records from old schema to new schema

**❌ Pure LLM Approach**:
```
Prompt: "Migrate these 100 records to new format"
Load all records → Ask Claude to transform

Problems:
├── May format inconsistently
├── May make mistakes on edge cases
├── No verification of output
└── Risk: Data corruption
```

**✅ Hybrid Approach**:
```
1. LLM: Design migration strategy
   "Old schema: {...}, New schema: {...}. Strategy?"
   → Claude explains transformation logic (3k tokens)

2. Preprocessing: Write migration function
   Based on Claude's strategy, write Python script
   (Human-written or Claude-generated once, 2k tokens)

3. Preprocessing: Execute migration
   Run script on all 100 records
   (0 tokens per record, instant, deterministic)

4. Preprocessing: Validate output
   Check all records match new schema
   (0 tokens, instant verification)

5. LLM: Review edge cases
   Show 5 problematic records → Claude suggests fixes
   (1k tokens)

Result: 6k tokens (vs 80k for LLM-per-record), 100% accurate
```

---

## Navigator's Implementation: Predefined Functions

Navigator uses this principle extensively:

### Example: Task Document Generation

**Without predefined functions** (Pure LLM):
```
Prompt: "Create task document for TASK-XX with proper format"

Claude generates document:
├── May miss required sections
├── May format inconsistently
├── May not follow template
└── Cost: 5k tokens per task doc
```

**With predefined functions** (Preprocessing + LLM):
```python
# skills/nav-task/functions/task_formatter.py
def format_task_doc(task_id, title, description, deliverables):
    """Generate task doc with consistent structure."""
    return f"""# {task_id}: {title}

**Status**: 📋 Planning
**Created**: {datetime.now().strftime('%Y-%m-%d')}

## Objective
{description}

## Deliverables
{format_list(deliverables)}

## Implementation Plan
[To be filled]

## Success Criteria
[To be filled]
"""

Result:
├── 100% consistent format (always)
├── Zero tokens (function execution)
├── Instant generation
└── Claude fills in semantic content only
```

**Separation of concerns**:
- **Preprocessing**: Structure, format, validation (0 tokens)
- **LLM**: Content, descriptions, decisions (2k tokens)

**Total savings**: 3k tokens per task doc (60%)

---

## Anti-Patterns to Avoid

### Anti-Pattern 1: LLM for Math

**❌ Bad**:
```
Prompt: "Calculate average token usage across 10 sessions"
Token cost: 2k
Risk: Rounding errors, incorrect math
```

**✅ Good**:
```python
avg = sum(session_tokens) / len(session_tokens)
Token cost: 0
Accuracy: Perfect
```

### Anti-Pattern 2: LLM for Regex

**❌ Bad**:
```
Prompt: "Find all email addresses in this text"
Token cost: Text size + generation
Risk: May miss edge cases
```

**✅ Good**:
```python
import re
re.findall(r'[\w\.-]+@[\w\.-]+\.\w+', text)
Token cost: 0
Accuracy: Defined by regex (adjustable)
```

### Anti-Pattern 3: LLM for Sorting

**❌ Bad**:
```
Prompt: "Sort these 50 files by date modified"
Token cost: 8k
Risk: May misinterpret dates
```

**✅ Good**:
```bash
ls -lt
# Or use Glob tool with built-in sorting
Token cost: 0
Accuracy: OS-level precision
```

### Anti-Pattern 4: LLM for JSON Validation

**❌ Bad**:
```
Prompt: "Check if this JSON is valid"
Token cost: JSON size + response
Risk: May miss subtle errors
```

**✅ Good**:
```python
import json
try:
    json.loads(content)
    print("Valid")
except json.JSONDecodeError as e:
    print(f"Invalid: {e}")

Token cost: 0
Accuracy: Spec-compliant
```

---

## When LLMs Excel

Don't avoid LLMs where they shine:

### Semantic Understanding

**Good LLM use**:
```
"Explain how this authentication system works"
"Why might this function cause a memory leak?"
"What's the difference between these two approaches?"
```

LLMs understand context, infer intent, explain tradeoffs.

### Code Generation

**Good LLM use**:
```
"Write error handling for this API call"
"Generate test cases for this function"
"Implement retry logic with exponential backoff"
```

LLMs apply patterns, follow conventions, handle edge cases.

### Naming & Documentation

**Good LLM use**:
```
"Suggest a better name for this function"
"Write JSDoc comments for this API"
"Generate commit message for these changes"
```

LLMs understand semantics, follow conventions, write clear prose.

### Design Decisions

**Good LLM use**:
```
"Should I use Redux or Context API here?"
"What's the best pattern for handling pagination?"
"How should I structure this component?"
```

LLMs weigh tradeoffs, consider best practices, suggest approaches.

---

## Decision Framework

Use this flowchart when approaching any task:

```
┌─────────────────────────────┐
│ Is the task deterministic?  │
│ (Same input → Same output)  │
└──────────┬──────────────────┘
           │
     ┌─────┴─────┐
     │           │
    YES         NO
     │           │
     ▼           ▼
┌─────────┐  ┌──────────┐
│ Use     │  │ Is       │
│ Pre-    │  │ semantic │
│ process │  │ under-   │
└─────────┘  │ standing │
             │ needed?  │
             └────┬─────┘
                  │
            ┌─────┴─────┐
            │           │
           YES         NO
            │           │
            ▼           ▼
       ┌────────┐  ┌──────────┐
       │ Use    │  │ Try      │
       │ LLM    │  │ Pre-     │
       └────────┘  │ process  │
                   │ + LLM    │
                   └──────────┘
```

**Examples**:
- Parse JSON? → Deterministic → **Preprocessing**
- Explain code? → Semantic understanding → **LLM**
- Extract tokens + match to design system? → Hybrid → **Preprocessing + LLM**

---

## Measuring the Impact

### Token Savings

**Before (Pure LLM)**:
- Load all data into context
- Process with LLM
- Cost: Data size × task complexity

**After (Preprocessing + LLM)**:
- Preprocess data (0 tokens)
- Load summary into context
- Process decisions with LLM
- Cost: Summary size only

**Typical savings**: 60-95% depending on task

### Accuracy Gains

| Task Type | Pure LLM | Preprocessing | Improvement |
|-----------|----------|---------------|-------------|
| JSON parsing | 85% | 100% | +15% |
| Pattern matching | 90% | 100% | +10% |
| Math calculations | 95% | 100% | +5% |
| Format conversion | 80% | 100% | +20% |
| Semantic understanding | 95% | N/A | -5% (worse) |

**Lesson**: Use the right tool for maximum accuracy.

### Time Savings

**Example: Design token extraction**

| Approach | Time | Accuracy |
|----------|------|----------|
| Manual (human) | 6-10 hours | 100% |
| Pure LLM | 12 minutes | 78% |
| Preprocessing + LLM | 5 minutes | 98% |

**Savings**: 95% time reduction vs manual, 58% vs pure LLM

---

## Implementation Guidelines

### For Navigator Users

1. **Start with preprocessing**: Can tools/scripts solve this?
2. **Add LLM layer**: What needs semantic understanding?
3. **Measure results**: Check token costs and accuracy
4. **Iterate**: Adjust boundary between preprocessing/LLM

### For Skill Creators

When creating Navigator skills:

1. **Identify deterministic steps** → Predefined functions (0 tokens)
2. **Identify semantic steps** → LLM prompts (minimal tokens)
3. **Create templates** → Consistent structure (0 tokens)
4. **Document pattern** → Reusable for others

**Example structure**:
```
skill/
├── functions/          # Preprocessing (Python)
│   ├── parser.py      # Deterministic extraction
│   ├── validator.py   # Schema checking
│   └── formatter.py   # Output templating
├── templates/          # Structured outputs
│   └── result.md      # Consistent format
└── SKILL.md           # LLM instructions (semantic layer)
```

---

## Next Steps

### Learn More
- **[PROGRESSIVE-REFINEMENT.md](./PROGRESSIVE-REFINEMENT.md)** - Fetch metadata → details pattern
- **[TOKEN-OPTIMIZATION.md](./TOKEN-OPTIMIZATION.md)** - Complete optimization strategies
- **[CONTEXT-BUDGETS.md](./CONTEXT-BUDGETS.md)** - Token allocation thinking

### Try It Yourself
- **[TRY-THIS-AGENT-SEARCH.md](./examples/TRY-THIS-AGENT-SEARCH.md)** - See preprocessing in action
- **Product Design Skill** - Real-world example of preprocessing + LLM

### References
- **[PATTERNS.md](../philosophy/PATTERNS.md)** - Direct MCP pattern (eliminate middleware)
- **[ANTI-PATTERNS.md](../philosophy/ANTI-PATTERNS.md)** - Forcing LLMs to parse structured data

---

**Bottom line**: LLMs are powerful, but not universal. Preprocessing handles structure, LLMs handle semantics. Use both strategically.

**Navigator's role**: Predefined functions + skills architecture makes it easy to separate preprocessing from LLM usage automatically.
