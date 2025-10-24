# Decision Framework: Preprocessing vs LLM

**Part of**: Navigator v4.0 Education Layer
**Type**: Decision Framework
**Use**: Choose the right tool for data processing tasks

---

## Primary Decision Tree

```
┌─────────────────────────────────────────┐
│ Is the task deterministic?              │
│ (Same input always gives same output)   │
└──────────────────┬──────────────────────┘
                   │
         ┌─────────┴──────────┐
         │                    │
        YES                  NO
         │                    │
         ▼                    ▼
┌──────────────────┐  ┌────────────────────┐
│ Can it be solved │  │ Does it require    │
│ with regex,      │  │ semantic           │
│ parsing, or      │  │ understanding or   │
│ math?            │  │ creativity?        │
└────────┬─────────┘  └─────────┬──────────┘
         │                      │
    ┌────┴────┐           ┌─────┴─────┐
    │         │           │           │
   YES       NO          YES         NO
    │         │           │           │
    ▼         ▼           ▼           ▼
┌──────────┐ ┌────────┐ ┌─────────┐ ┌──────────┐
│ PREPRO-  │ │ CHECK  │ │ USE LLM │ │ TRY      │
│ CESSING  │ │ IF     │ │ (3-10k) │ │ HYBRID:  │
│ (0 tokens│ │ HYBRID │ │         │ │ PREPRO + │
│ )        │ │ WORKS  │ │         │ │ LLM      │
└──────────┘ └────────┘ └─────────┘ └──────────┘
```

---

## Task Classification Matrix

| Task Type | Deterministic? | Right Tool | Token Cost | Accuracy |
|-----------|---------------|-----------|-----------|----------|
| Parse JSON/XML | ✅ Yes | **Preprocessing** | 0 | 100% |
| Extract with regex | ✅ Yes | **Preprocessing** | 0 | 100% |
| Math calculations | ✅ Yes | **Preprocessing** | 0 | 100% |
| Format conversion | ✅ Yes | **Preprocessing** | 0 | 100% |
| Count occurrences | ✅ Yes | **Preprocessing** | 0 | 100% |
| Validate schemas | ✅ Yes | **Preprocessing** | 0 | 100% |
| Explain code | ❌ No | **LLM** | 3-8k | 95% |
| Generate code | ❌ No | **LLM** | 3-10k | 90% |
| Name variables | ❌ No | **LLM** | 1-3k | 95% |
| Suggest architecture | ❌ No | **LLM** | 5-15k | 90% |
| Find similar patterns | ❌ No | **LLM** | 4-10k | 85% |
| Extract tokens → Match patterns | ⚠️ Hybrid | **Preprocessing + LLM** | 1-4k | 98% |
| Parse data → Suggest improvements | ⚠️ Hybrid | **Preprocessing + LLM** | 2-6k | 95% |

---

## Detailed Decision Paths

### Path 1: Structured Data Tasks

```
Task: Parse JSON, XML, CSV, YAML
         ↓
Is structure well-defined?
         ↓
    ┌────┴────┐
    │         │
   YES       NO
    │         │
    ▼         ▼
┌────────┐ ┌─────────┐
│ USE    │ │ USE LLM │
│ json.  │ │ to      │
│ loads  │ │ under-  │
│ (0 tok)│ │ stand   │
└────────┘ └─────────┘
```

**Examples**:

✅ **Preprocessing** (0 tokens):
```python
# Parse JSON
import json
data = json.loads(content)

# Parse CSV
import csv
rows = list(csv.reader(content))

# Parse YAML
import yaml
config = yaml.safe_load(content)

# Parse XML
import xml.etree.ElementTree as ET
root = ET.fromstring(content)
```

❌ **LLM** (15k+ tokens):
```
Load file → Ask Claude to extract data
Problem: May hallucinate, inconsistent format
Cost: 15k tokens
Accuracy: 85-90%
```

---

### Path 2: Pattern Matching Tasks

```
Task: Find/count/replace patterns
         ↓
Is pattern clearly defined?
         ↓
    ┌────┴────┐
    │         │
   YES       NO
    │         │
    ▼         ▼
┌────────┐ ┌─────────┐
│ USE    │ │ USE LLM │
│ REGEX  │ │ for     │
│ or     │ │ fuzzy   │
│ GREP   │ │ match   │
│ (0 tok)│ │ (3-5k)  │
└────────┘ └─────────┘
```

**Examples**:

✅ **Preprocessing** (0 tokens):
```bash
# Find all email addresses
grep -r "[\w\.-]+@[\w\.-]+\.\w+" .

# Count function calls
grep -c "getCwd()" *.ts

# Find TODO comments
grep -r "// TODO" .
```

❌ **LLM** (2-8k tokens):
```
Load files → Ask Claude to find patterns
Problem: May miss edge cases
Cost: 2-8k tokens per search
Accuracy: 85-95%
```

⚠️ **Hybrid** (1-3k tokens):
```
1. Grep finds all matches (0 tokens)
2. LLM categorizes results (3k tokens)
Result: Best of both worlds
```

---

### Path 3: Mathematical Tasks

```
Task: Calculate, aggregate, compare numbers
         ↓
Always use preprocessing
         ↓
┌─────────────────┐
│ Python/Bash     │
│ calculations    │
│ (0 tokens)      │
│ 100% accurate   │
└─────────────────┘
```

**Examples**:

✅ **Preprocessing** (0 tokens):
```python
# Average
avg = sum(values) / len(values)

# Aggregate
total = sum(session_tokens)

# Compare
if value_a > value_b * 1.5:
    print("Significantly higher")

# Percentage
percentage = (part / whole) * 100
```

❌ **LLM** (2k+ tokens):
```
"Calculate the average of these 50 numbers"
Problem: Rounding errors, slower
Cost: 2k tokens
Accuracy: 99% (not 100%)
```

---

### Path 4: Format Conversion Tasks

```
Task: Convert between formats
         ↓
Is conversion rule-based?
         ↓
    ┌────┴────┐
    │         │
   YES       NO
    │         │
    ▼         ▼
┌────────┐ ┌─────────┐
│ USE    │ │ USE LLM │
│ SCRIPT │ │ for     │
│ (0 tok)│ │ context-│
│        │ │ aware   │
└────────┘ └─────────┘
```

**Examples**:

✅ **Preprocessing** (0 tokens):
```python
# Date format
from datetime import datetime
iso_date = datetime.strptime(date, '%m/%d/%Y').isoformat()

# Case conversion
snake_case = camelCase.replace(/([A-Z])/g, '_$1').lower()

# File format
json.dumps(yaml.safe_load(content))  # YAML → JSON
```

❌ **LLM** (3-5k tokens):
```
"Convert these dates to ISO 8601 format"
Problem: May misinterpret ambiguous dates
Cost: 3-5k tokens
Accuracy: 90-95%
```

---

### Path 5: Semantic Understanding Tasks

```
Task: Explain, suggest, design, name
         ↓
Requires human-like understanding
         ↓
┌─────────────────┐
│ USE LLM         │
│ (3-15k tokens)  │
│ This is what    │
│ LLMs excel at   │
└─────────────────┘
```

**Examples**:

✅ **LLM** (3-10k tokens):
```
"Explain how this authentication system works"
"Suggest a better name for this function"
"Design the API for this feature"
"What's the tradeoff between approach A and B?"
"Generate documentation for this code"
```

❌ **Preprocessing** (impossible):
```
Can't automate semantic understanding
Can't script creativity
Can't regex explain context
```

---

## Hybrid Pattern Deep Dive

### When to Use Hybrid Approach

**Scenario**: Task has both deterministic and semantic components

**Pattern**:
```
Step 1: Preprocessing (extract/parse/structure)
         ↓
Step 2: LLM (interpret/suggest/decide)
```

### Example 1: Design Token Extraction

**Step 1 - Preprocessing** (0 tokens):
```python
# Extract all colors from Figma JSON
def extract_colors(figma_json):
    colors = {}
    for node in figma_json['nodes']:
        if 'fills' in node:
            colors[node['name']] = rgb_to_hex(node['fills'][0])
    return colors

Result: {"primary": "#1E40AF", "secondary": "#6B7280", ...}
```

**Step 2 - LLM** (3k tokens):
```
Input: Extracted colors + existing design system
Prompt: "Match these Figma colors to our design system. Flag new colors."

LLM Output:
- "primary matches theme.colors.primary ✓"
- "secondary close to gray-600, suggest using existing"
- "Warning: accent-purple is new color"

Cost: 3k tokens
```

**Total**: 3k tokens (vs 45k pure LLM)
**Savings**: 42k (93%)
**Accuracy**: 98% (vs 78% pure LLM)

---

### Example 2: API Endpoint Analysis

**Step 1 - Preprocessing** (0 tokens):
```bash
# Extract all endpoint definitions
grep -r "router\.(get|post|put|delete)" src/routes/ | \
  awk '{print $2}' > endpoints.txt

Result:
POST /api/users
GET /api/users/:id
DELETE /api/users/:id
POST /api/auth/login
... (20 endpoints)
```

**Step 2 - LLM** (3k tokens):
```
Input: List of endpoints
Prompt: "Suggest rate limiting strategy for these endpoints"

LLM Output:
- POST /auth/login → Strict (5/15min)
- POST /users → Moderate (10/hour)
- GET /users → Lenient (100/hour)
- Reasoning: [explanation]

Cost: 3k tokens
```

**Total**: 3k tokens (vs 35k pure LLM)
**Savings**: 32k (91%)

---

### Example 3: Codebase Migration

**Step 1 - Preprocessing** (0 tokens):
```bash
# Find all old API usage
grep -r "oldApi\." --include="*.ts" | wc -l
# Result: 47 occurrences in 23 files
```

**Step 2 - LLM** (5k tokens):
```
Input: "Found 47 usages in 23 files"
Prompt: "What's the migration strategy?"

LLM Output:
1. Create adapter layer (backwards compatible)
2. Migrate high-traffic endpoints first
3. Deprecate old API after 2 sprints
4. Estimated effort: 3 days

Cost: 5k tokens
```

**Total**: 5k tokens (vs 70k reading all files)
**Savings**: 65k (93%)

---

## Common Task Catalog

### Preprocessing Tasks (0 tokens)

| Task | Tool | Example |
|------|------|---------|
| Parse JSON | `json.loads()` | `data = json.loads(content)` |
| Parse CSV | `csv.reader()` | `rows = list(csv.reader(file))` |
| Regex match | `re.findall()` | `emails = re.findall(pattern, text)` |
| Count lines | `wc -l` | `wc -l file.txt` |
| Find files | Glob tool | `**/*.ts` |
| Search code | Grep tool | `grep -r "pattern" .` |
| Calculate sum | Python | `sum(values)` |
| Format date | `datetime` | `datetime.fromisoformat(date)` |
| Validate JSON | `json.loads()` | Try/except for validation |
| List files | `ls` | `ls -la directory/` |

### LLM Tasks (3-10k tokens)

| Task | Token Cost | Example |
|------|-----------|---------|
| Explain code | 4-8k | "How does this auth system work?" |
| Suggest names | 1-3k | "Better name for this function?" |
| Design API | 5-10k | "Design REST API for users" |
| Generate code | 3-8k | "Implement error handling" |
| Write docs | 3-6k | "Document this API endpoint" |
| Refactor advice | 4-8k | "How to improve this code?" |
| Debug help | 3-7k | "Why is this test failing?" |
| Architecture | 8-15k | "Design system architecture" |

### Hybrid Tasks (1-6k tokens)

| Task | Preprocessing | LLM | Total Tokens |
|------|---------------|-----|--------------|
| Token extraction | Parse Figma JSON (0) | Match to system (3k) | 3k |
| Endpoint analysis | Grep endpoints (0) | Suggest limits (3k) | 3k |
| Migration plan | Find usages (0) | Strategy (5k) | 5k |
| Performance audit | Extract metrics (0) | Analyze (4k) | 4k |
| Security review | Scan patterns (0) | Assess (6k) | 6k |

---

## Anti-Patterns

### Anti-Pattern 1: LLM for Math

**❌ Wrong**:
```
Prompt: "Calculate the average token usage from these 10 sessions"
Files loaded: Session data (5k)
LLM processing: 2k
Total: 7k tokens
Accuracy: 99%
```

**✅ Right**:
```python
avg = sum(session_tokens) / len(session_tokens)
print(f"Average: {avg:.2f}")

Total: 0 tokens
Accuracy: 100%
```

---

### Anti-Pattern 2: LLM for Parsing

**❌ Wrong**:
```
Prompt: "Extract all color values from this JSON"
JSON loaded: 10k tokens
LLM extraction: 3k
Total: 13k tokens
Accuracy: 85%
```

**✅ Right**:
```python
import json
data = json.loads(content)
colors = [node['color'] for node in data['styles']]

Total: 0 tokens
Accuracy: 100%
```

---

### Anti-Pattern 3: Preprocessing for Creativity

**❌ Wrong**:
```python
# Trying to script variable naming
def generate_name(purpose):
    return f"{purpose}_handler"  # Generic, not context-aware

Result: Poor names, no semantic understanding
```

**✅ Right**:
```
Prompt: "Suggest a better name for this function that handles user authentication"
LLM: "authenticateUser() or validateUserCredentials()"

Total: 2k tokens
Result: Context-aware, meaningful names
```

---

## Quick Reference Card

```
┌───────────────────────────────────────────┐
│ PREPROCESSING (0 tokens, 100% accurate)  │
├───────────────────────────────────────────┤
│ ✅ Parse JSON/XML/CSV/YAML                │
│ ✅ Regex pattern matching                 │
│ ✅ Math calculations                      │
│ ✅ Format conversions                     │
│ ✅ Count/aggregate                        │
│ ✅ Validate schemas                       │
│ ✅ Find files (Glob)                      │
│ ✅ Search code (Grep)                     │
└───────────────────────────────────────────┘

┌───────────────────────────────────────────┐
│ LLM (3-15k tokens, 90-95% accurate)      │
├───────────────────────────────────────────┤
│ ✅ Explain code/architecture              │
│ ✅ Suggest names/improvements             │
│ ✅ Design APIs/systems                    │
│ ✅ Generate code                          │
│ ✅ Write documentation                    │
│ ✅ Debug reasoning                        │
│ ✅ Make judgments/tradeoffs               │
└───────────────────────────────────────────┘

┌───────────────────────────────────────────┐
│ HYBRID (1-6k tokens, 95-98% accurate)    │
├───────────────────────────────────────────┤
│ ✅ Extract data → LLM interprets          │
│ ✅ Parse structure → LLM suggests         │
│ ✅ Find patterns → LLM categorizes        │
│ ✅ Calculate metrics → LLM analyzes       │
└───────────────────────────────────────────┘
```

---

## Next Steps

### Learn More
- **[AGENT-VS-MANUAL.md](./AGENT-VS-MANUAL.md)** - When to use agents
- **[WHEN-TO-COMPACT.md](./WHEN-TO-COMPACT.md)** - Context management
- **[PREPROCESSING-VS-LLM.md](../PREPROCESSING-VS-LLM.md)** - Full guide

### Try It
- **[TRY-THIS-AGENT-SEARCH.md](../examples/TRY-THIS-AGENT-SEARCH.md)** - Practice hybrid approach

---

**Bottom line**: Preprocessing for deterministic tasks (0 tokens, 100% accurate). LLM for semantic tasks (3-10k tokens, 90-95% accurate). Hybrid for best results (1-6k tokens, 95-98% accurate).
