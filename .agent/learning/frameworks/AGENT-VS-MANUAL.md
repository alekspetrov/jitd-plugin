# Decision Framework: Agent vs Manual Read

**Part of**: Navigator v4.0 Education Layer
**Type**: Decision Framework
**Use**: Quick reference for choosing between agent search and manual file reading

---

## Decision Tree

```
┌─────────────────────────────────────────┐
│ How many files are potentially          │
│ relevant to your question?              │
└──────────────────┬──────────────────────┘
                   │
         ┌─────────┴──────────┐
         │                    │
       1-2                  3+
         │                    │
         ▼                    ▼
┌──────────────────┐  ┌───────────────────┐
│ Do you know      │  │ Do you know       │
│ exactly which    │  │ exactly which     │
│ files?           │  │ files?            │
└────────┬─────────┘  └────────┬──────────┘
         │                     │
    ┌────┴────┐           ┌────┴────┐
    │         │           │         │
   YES       NO          YES       NO
    │         │           │         │
    ▼         ▼           ▼         ▼
┌────────┐ ┌──────┐ ┌──────────┐ ┌────────┐
│ READ   │ │ USE  │ │ USE      │ │ USE    │
│ MANUAL │ │ AGENT│ │ AGENT    │ │ AGENT  │
│ (3-6k) │ │ (3k) │ │ (4-6k)   │ │ (4-6k) │
└────────┘ └──────┘ └──────────┘ └────────┘
```

---

## Decision Matrix

| Files Involved | Know Exact Files? | Complexity | Best Choice | Token Cost | Savings |
|----------------|-------------------|------------|-------------|-----------|---------|
| 1 file | Yes | Simple | **Manual Read** | 2-4k | - |
| 1 file | No | Must search | **Agent** | 3k | 0k (same) |
| 2 files | Yes | Simple | **Manual Read** | 4-8k | - |
| 2 files | No | Must search | **Agent** | 3-4k | 1-4k |
| 3-5 files | Yes | Known | **Agent** | 4-5k | 5-15k (50-70%) |
| 3-5 files | No | Exploration | **Agent** | 4-5k | 10-20k (70-80%) |
| 6-10 files | Any | Complex | **Agent** | 4-6k | 15-40k (75-85%) |
| 10+ files | Any | Very complex | **Agent** | 5-7k | 30-80k (85-95%) |

---

## File Count Quick Reference

### 1-2 Files → Manual Read

**When**:
- You know exactly which files
- Files are small (<5k tokens each)
- Simple question about specific code

**Example**:
```
"Read AuthService.ts and show me the login method"

Cost: 3k tokens (one file)
Why manual: Direct, no overhead
```

### 3-5 Files → Agent (Usually)

**When**:
- Exploring related functionality
- Comparing implementations
- Understanding patterns across files

**Example**:
```
"Use agent to find how error handling works across the API layer"

Agent reads 4 files (12k if manual)
Returns summary: 4k tokens
Savings: 8k (67%)
```

### 6-10 Files → Agent (Always)

**When**:
- Architecture understanding
- Pattern discovery
- Multi-component interactions

**Example**:
```
"Use agent to explain the authentication flow through all components"

Agent reads 8 files (24k if manual)
Returns summary: 5k tokens
Savings: 19k (79%)
```

### 10+ Files → Agent (Required)

**When**:
- Codebase exploration
- Finding all usages
- System-wide patterns

**Example**:
```
"Use agent to find all files using the deprecated API"

Agent reads 25 files (75k if manual)
Returns summary: 6k tokens
Savings: 69k (92%)
```

---

## Scenario-Based Decisions

### Scenario 1: Understanding Specific Function

**Question**: "How does the `processPayment()` function work?"

**Analysis**:
- Files involved: 1 (PaymentService.ts)
- Know location: Yes
- Complexity: Simple

**Decision**: **Manual Read**
```
"Read src/services/PaymentService.ts and explain processPayment()"
Cost: 3k tokens
```

---

### Scenario 2: Finding Implementation Pattern

**Question**: "How does error handling work in this project?"

**Analysis**:
- Files involved: Unknown, likely 5-10
- Know location: No
- Complexity: Pattern across codebase

**Decision**: **Use Agent**
```
"Use agent to find how error handling is implemented across the codebase"
Cost: 5k tokens (vs 30k manual)
Savings: 25k (83%)
```

---

### Scenario 3: Comparing Two Approaches

**Question**: "What's the difference between AuthV1 and AuthV2?"

**Analysis**:
- Files involved: 2 implementations (4-6 files total)
- Know location: Yes (two directories)
- Complexity: Comparison needed

**Decision**: **Use Agent**
```
"Use agent to compare auth-v1/ vs auth-v2/ implementations"
Cost: 4k tokens (vs 18k manual)
Savings: 14k (78%)
```

---

### Scenario 4: Debugging Specific Issue

**Question**: "Why is this test failing?" (test file open)

**Analysis**:
- Files involved: 1-2 (test + source)
- Know location: Yes
- Complexity: Focused debugging

**Decision**: **Manual Read**
```
"Read UserService.ts to understand why the test is failing"
Cost: 3k tokens
```

---

### Scenario 5: Learning Codebase Architecture

**Question**: "How is this project structured?"

**Analysis**:
- Files involved: 20+ (entire codebase)
- Know location: No (exploration)
- Complexity: Very complex

**Decision**: **Use Agent**
```
"Use agent to explain the project architecture and main components"
Cost: 6k tokens (vs 80k+ manual)
Savings: 74k (93%)
```

---

## Question Type Mapping

### Specific Questions → Manual Read

**Patterns**:
- "Show me function X in file Y"
- "Read this specific file"
- "What does this code block do?"
- "Explain this function"

**Why manual**: Direct answer, no exploration needed

### Exploratory Questions → Use Agent

**Patterns**:
- "How does X work across the system?"
- "Find all places that use Y"
- "Compare implementation A vs B"
- "Explain the architecture"
- "What pattern is used for Z?"

**Why agent**: Requires reading multiple files, benefits from summary

---

## Token Cost Comparison

### Manual Reading Pattern

```
File 1: 3k
File 2: 4k
File 3: 3k
File 4: 5k
File 5: 4k
────────────
Total: 19k tokens

Efficiency: 60% (used 3 files, read 5)
Waste: 7k tokens
```

### Agent Search Pattern

```
Agent reads 5 files internally (not in your context)
Agent returns summary: 4k tokens
You load 1 specific file: 3k tokens
────────────
Total: 7k tokens

Efficiency: 100% (used all loaded content)
Savings: 12k tokens (63%)
```

---

## When Agent Isn't Worth It

### Case 1: Single Known File

```
❌ "Use agent to read AuthService.ts"
✅ "Read AuthService.ts"

Agent overhead: Not worth it for 1 file
Manual is faster: 3k vs 4k (agent has overhead)
```

### Case 2: File Already Loaded

```
❌ "Use agent to re-analyze this file"
✅ "Based on AuthService.ts above, ..."

Agent cost: 3k to re-read
Manual cost: 0k (already in context)
Savings: Don't use agent
```

### Case 3: Very Small Files

```
❌ "Use agent to read config.json (20 lines)"
✅ "Read config.json"

Agent overhead: ~2k (setup + summary)
Manual read: 0.5k (tiny file)
Manual wins: 4x more efficient
```

---

## When Agent Shines

### Case 1: Unknown File Locations

```
"Find all files that implement caching"

Without agent:
├── Guess which files (10 guesses)
├── Read each one (30k tokens)
└── Find 3 relevant files

With agent:
├── Agent searches all files
├── Returns 3 relevant files (4k summary)
└── You load 1 for details (3k)

Savings: 23k tokens (77%)
```

### Case 2: Pattern Discovery

```
"How do different components handle validation?"

Without agent:
├── Read 15 components (45k)
├── Mentally compare patterns
└── Synthesize understanding

With agent:
├── Agent reads 15 components
├── Identifies 3 validation patterns (5k summary)
└── You understand immediately

Savings: 40k tokens (89%)
```

### Case 3: Codebase Mapping

```
"Explain the data flow from API to database"

Without agent:
├── Read route files (12k)
├── Read service files (15k)
├── Read model files (10k)
├── Try to connect pieces
└── Total: 37k tokens

With agent:
├── Agent traces flow through all files
├── Returns data flow diagram in text (6k)
└── Clear understanding immediately

Savings: 31k tokens (84%)
```

---

## Advanced Decision Factors

### Factor 1: Context Already Full

**Situation**: Context at 65%

**Decision Shift**:
- Manual read (3-6k): Might push over 70% → Use agent (4k summary)
- Agent (4k summary): Safer, prevents context overflow

**Rule**: When context >60%, prefer agent even for 2-3 files

### Factor 2: Iterative Exploration

**Situation**: Don't know what you're looking for exactly

**Example**:
```
"I need to understand how users are authenticated, but I'm not sure of the details"

Approach:
1. Agent: High-level summary (4k)
2. Review summary, identify key areas
3. Manual: Read 1-2 specific files (6k)

Total: 10k tokens
vs Reading all auth files blindly: 30k+ tokens
Savings: 67%
```

### Factor 3: Time Sensitivity

**Fast exploration**:
- Agent: 30-60 seconds for summary
- Manual: 5-10 minutes reading multiple files

**When time matters**: Use agent for speed + token efficiency

---

## Common Mistakes

### Mistake 1: Agent for Everything

**Wrong**:
```
"Use agent to read this one specific file I'm looking at"
Cost: 4k (agent overhead)
```

**Right**:
```
"Read the specific file"
Cost: 3k (direct)
```

**Fix**: Use manual for 1-2 known files

### Mistake 2: Manual for Everything

**Wrong**:
```
Read file 1 (3k)
Read file 2 (4k)
Read file 3 (3k)
... (10 more files)
Total: 40k tokens
```

**Right**:
```
"Use agent to find relevant files"
Agent summary: 5k tokens
Load 1 specific file: 3k
Total: 8k tokens
```

**Fix**: Use agent for 3+ files

### Mistake 3: Not Leveraging Agent Summaries

**Wrong**:
```
Agent returns summary (4k)
Then: "Now read all those files manually" (20k)
Total: 24k
```

**Right**:
```
Agent returns summary (4k)
Decision: Summary is enough, or load 1 file for details (3k)
Total: 7k
```

**Fix**: Trust agent summaries, load details only if needed

---

## Quick Reference Card

```
┌──────────────────────────────────────────┐
│ HOW MANY FILES?                          │
├──────────────────────────────────────────┤
│ 1 file (known)        → Manual Read      │
│ 1 file (unknown)      → Agent Search     │
│ 2 files (simple)      → Manual Read      │
│ 2 files (compare)     → Agent Search     │
│ 3-5 files             → Agent Search     │
│ 6-10 files            → Agent Search     │
│ 10+ files             → Agent Required   │
├──────────────────────────────────────────┤
│ QUESTION TYPE?                           │
├──────────────────────────────────────────┤
│ "Show me X"           → Manual Read      │
│ "How does X work?"    → Agent Search     │
│ "Find all Y"          → Agent Search     │
│ "Compare A vs B"      → Agent Search     │
│ "Explain arch"        → Agent Search     │
├──────────────────────────────────────────┤
│ CONTEXT USAGE?                           │
├──────────────────────────────────────────┤
│ <40%                  → Either works     │
│ 40-60%                → Prefer agent     │
│ >60%                  → Agent required   │
└──────────────────────────────────────────┘
```

---

## Next Steps

### Learn More
- **[PREPROCESSING-DECISION-TREE.md](./PREPROCESSING-DECISION-TREE.md)** - Preprocessing vs LLM
- **[WHEN-TO-COMPACT.md](./WHEN-TO-COMPACT.md)** - Context management
- **[TRY-THIS-AGENT-SEARCH.md](../examples/TRY-THIS-AGENT-SEARCH.md)** - Hands-on practice

### Related Guides
- **[PREPROCESSING-VS-LLM.md](../PREPROCESSING-VS-LLM.md)** - Right tool principle
- **[TOKEN-OPTIMIZATION.md](../TOKEN-OPTIMIZATION.md)** - Complete strategies

---

**Bottom line**: Use agents for 3+ files or exploratory questions. Use manual reads for 1-2 specific known files. When in doubt and context is high, use agent.
