# Success Patterns: Context Efficiency in Practice

**Proven strategies that work**

---

## Introduction

These patterns saved 92% of context tokens. Not theoretical—implemented, tested, verified.

Each pattern shows:
- **Principle**: The core insight
- **Implementation**: How it works
- **Proof**: Measured results
- **When to use**: Application guidance
- **Proven by**: Where Navigator uses this

---

## 1. Lazy Loading

### Principle

**Load what you need, when you need it**

Not "load everything just in case."

### Implementation

**Session architecture**:
```
Start:
├── Navigator/index (2k) ✓ Always
└── Current task (3k) ✓ For work

On-demand:
├── System docs (5k) ← When implementing core features
├── SOPs (2k each) ← When hitting specific scenarios
└── Integration docs (3k) ← When needed

Progressive, strategic, curated
```

### Proof

**Measured results**:
```
Your project docs available: 150,000 tokens
Navigator loads: 12,000 tokens
Savings: 138,000 tokens (92%)

Context usage: 6% (Navigator + task)
Available for work: 94%
```

Verified via OpenTelemetry (TASK-06 metrics).

### When to Use

**Always.** This is the foundation pattern.

**Workflow**:
1. Start every session: `"Start my Navigator session"`
2. Navigator loads (2k) + Current task (3k)
3. Work begins with 195k tokens available
4. Load additional docs only when relevant

**Decision tree**:
```
Need to implement feature?
├─ Do you need architecture docs?
│  └─ Yes → Load system/architecture.md (5k)
│  └─ No → Continue with current context
│
├─ Do you need integration details?
│  └─ Yes → Load relevant integration doc (3k)
│  └─ No → Continue
│
└─ Hit unexpected issue?
   └─ Load relevant SOP (2k)
```

**Load on-demand, not upfront.**

### Proven By

**Navigator's documentation system**:
- `.agent/` directory: 100k+ tokens available
- Session start: 5k tokens loaded
- **Success**: 95% savings, sessions last 20+ exchanges

---

## 2. Direct MCP (Eliminate Middleware)

### Principle

**Connect directly when possible, eliminate orchestration overhead**

### Implementation

**Before** (Navigator v3.3.0 - Figma via Claude):
```
User request
  ↓
Claude orchestrates
  ↓
Call MCP tool manually
  ↓
Save to /tmp/file.json
  ↓
Call another MCP tool
  ↓
Save to /tmp/file2.json
  ↓
Run Python script
  ↓
Process all temp files
  ↓
Return results

Steps: 15-20
Tokens: 150k (orchestration + data)
Time: 15 minutes
```

**After** (Navigator v3.4.0 - Direct MCP):
```
User request
  ↓
Python connects to MCP directly
  ↓
Fetches data (no temp files)
  ↓
Processes immediately
  ↓
Returns results

Steps: 1
Tokens: 12k (just data)
Time: 5 minutes
```

### Proof

**v3.4.0 Figma integration**:
```
Orchestration: 15-20 steps → 1 step (95% ↓)
Token usage: 150k → 12k (92% ↓)
Time: 15 min → 5 min (67% ↓)
Reliability: Variable → Deterministic
```

### When to Use

**Use when**:
- MCP server available (Figma, Linear, GitHub, etc.)
- Multi-step orchestration required
- Same operation repeated frequently
- Data needs preprocessing before LLM

**Pattern**:
```python
# Direct MCP connection
import mcp

client = mcp.Client("http://localhost:3845/mcp")
data = client.call("tool_name", params)

# Preprocess with Python
processed = normalize_data(data)

# Return to LLM (clean, small)
return processed
```

**Don't use when**:
- Single-use operation
- Simple Claude tool call sufficient
- No preprocessing needed
- Building the bridge costs more than orchestration

### Proven By

**Navigator v3.4.0**:
- `skills/product-design/functions/figma_mcp_client.py`
- 309 lines, fully documented
- Uses official Anthropic MCP SDK
- **Result**: 95% orchestration reduction

---

## 3. Preprocessing Before LLM

### Principle

**Python for deterministic, LLM for semantic**

Right tool for the job.

### Implementation

**Pattern**:
```
1. Traditional code handles deterministic tasks
   └─ Parsing, traversal, normalization, validation

2. Output clean, structured data
   └─ JSON, simple formats

3. LLM receives structured data
   └─ Semantic understanding, code generation, decisions
```

**Example** (Figma design extraction):

**Wrong approach** (LLM parsing):
```xml
<!-- 150k tokens of nested XML -->
<frame id="1:303" name="/dashboard">
  <instance id="7:1290" name="Avatar">
    <frame id="8:123">
      <rect fill="#FF0000"/>
      <text>John Doe</text>
    </frame>
  </instance>
  <!-- 26 levels deep... -->
</frame>

Ask LLM: "Extract components"
Result: Hallucinations, missed elements, inconsistent
```

**Right approach** (Python preprocessing):
```python
# Python does deterministic work
import xml.etree.ElementTree as ET

def extract_components(xml_data):
    tree = ET.fromstring(xml_data)
    components = []

    for elem in tree.findall('.//component'):
        components.append({
            'name': elem.get('name'),
            'type': classify_component(elem),
            'props': extract_properties(elem)
        })

    return json.dumps(components)

# Returns 12k tokens of clean JSON
```

```json
{
  "components": [
    {"name": "Avatar", "type": "atom", "size": "40x40"},
    {"name": "Button", "type": "atom", "variant": "primary"}
  ]
}
```

**LLM receives clean data**:
- No parsing needed
- Clear structure
- Semantic work only (map to design system, generate code)

### Proof

**v3.4.0 Figma integration**:
```
Before (LLM parsing):
├─ Input: 150k tokens XML
├─ Process: Pattern matching
├─ Output: Unreliable (hallucinations)
└─ Tokens: 150k

After (Python preprocessing):
├─ Input: 150k XML → Python parser
├─ Process: Deterministic extraction
├─ Output: 12k JSON → LLM
└─ Tokens: 12k (92% savings)

Reliability: Hallucinations → Deterministic
```

### When to Use

**Use preprocessing for**:
- ✅ XML/HTML parsing
- ✅ Deeply nested JSON
- ✅ CSV/tabular data (use pandas)
- ✅ Log file analysis (use awk/grep)
- ✅ Binary formats
- ✅ Recursive hierarchies

**Use LLM directly for**:
- ✅ Natural language understanding
- ✅ Code generation
- ✅ Semantic decisions
- ✅ Contextual analysis
- ✅ API responses (simple JSON)

**Decision rule**:
```
Is the task deterministic? (Same input → Same output always)
├─ Yes → Use traditional code
└─ No → Use LLM

Does it require semantic understanding?
├─ Yes → Use LLM
└─ No → Use traditional code
```

### Proven By

**Navigator v3.4.0**:
- Figma XML → Python → Clean JSON → LLM
- **Pattern proven**: 92% token savings, deterministic output

**Applies broadly**:
- CSV parsing: pandas → LLM
- Log analysis: awk/grep → LLM
- API transformation: jq → LLM

---

## 4. Progressive Refinement

### Principle

**Fetch metadata first, drill down only if needed**

### Implementation

**Pattern**:
```
Level 1: Metadata/Overview (2-3k tokens)
  ├─ High-level structure
  ├─ Component names
  ├─ Relationships
  └─ Enough to decide what's needed

Level 2: Specific details (3-5k tokens) ← Only if needed
  ├─ Implementation details for relevant parts
  ├─ Properties for selected components
  └─ Targeted, not everything

Level 3: Deep dive (5-10k tokens) ← Only if still needed
  ├─ Full implementation
  ├─ Edge cases
  └─ Comprehensive details
```

**Example** (API documentation):

**Bulk loading**:
```
Load api-docs.md (entire file, 15k tokens)
Use overview section (2k worth)
Waste 13k tokens
```

**Progressive refinement**:
```
Step 1: Load api-docs/README.md (2k)
  └─ Shows API structure, available endpoints

Step 2: User needs authentication
  └─ Load api-docs/authentication.md (3k)
  └─ Now have what's needed

Step 3: User needs specific endpoint details
  └─ Load api-docs/endpoints/users.md (2k)

Total: 7k tokens (vs 15k bulk)
Savings: 53%
```

### Proof

**v3.4.0 Figma integration**:
```
Progressive approach:
├─ Fetch metadata (file structure, component names): 12k
├─ Analyze metadata → Identify needs
├─ Fetch details for relevant components only: +5-8k
└─ Total: ~20k tokens

Bulk approach:
├─ Fetch everything (all components, all properties): 150k
└─ Total: 150k tokens

Savings: 87%
Time: 15 min → 5 min (67% faster)
```

### When to Use

**Use for**:
- Large documentation sets
- API documentation
- Design file analysis
- Codebase exploration
- Multi-level hierarchies

**Pattern application**:
```
Always ask:
1. Do I need full details now?
   └─ No → Load summary/overview only

2. Can I decide next step from metadata?
   └─ Yes → Load metadata, decide, then drill down

3. Will I use all this information?
   └─ No → Load selectively
```

**Real workflow**:
```
Implementing payment integration:

Progressive:
1. Load payments/README.md
   └─ "We use Stripe, see stripe-integration.md"

2. Load payments/stripe-integration.md
   └─ Overview of setup, now understand approach

3. Implement based on overview
   └─ IF hit issues, load specific troubleshooting docs

Total: ~7k tokens

Bulk (loading all payment docs): ~20k tokens
Savings: 65%
```

### Proven By

**Navigator v3.4.0 Figma MCP client**:
- `skills/product-design/functions/figma_mcp_client.py`
- Implements progressive fetching
- Metadata → Details on-demand
- **Result**: 87% token savings

---

## 5. Autonomous Completion

### Principle

**Eliminate deterministic human prompts**

AI should handle predictable workflows autonomously.

### Implementation

**Pattern**:
```
Feature completion workflow:
1. Tests pass ✓
2. Code reviewed (by AI or human) ✓
3. Implementation complete ✓

Autonomous actions (no prompts needed):
├─ Commit changes (conventional commit format)
├─ Update documentation (if changes affect docs)
├─ Close ticket (if PM tool configured)
├─ Create context marker (for future resume)
└─ Suggest compact (if context >80%)
```

**Before** (manual prompts):
```
You: "Please commit these changes"
AI: Creates commit
You: "Please update the docs"
AI: Updates docs
You: "Please close the ticket"
AI: Closes ticket
You: "Please create a marker"
AI: Creates marker

4 manual prompts (interruptions)
```

**After** (autonomous):
```
AI detects: Tests pass, implementation complete
AI executes:
├─ Commits with message
├─ Updates docs
├─ Closes ticket
├─ Creates marker
└─ Suggests compact

0 manual prompts (autonomous)
```

### Proof

**Navigator completion protocol**:
```
Measured elimination:
├─ Manual prompts before: 4-5 per feature
├─ Manual prompts after: 0
└─ Reduction: 100%

Time savings:
├─ Prompt + wait per action: ~30 seconds
├─ Actions per feature: 4-5
├─ Time saved: 2-2.5 minutes per feature
└─ Over 20 features: 40-50 minutes saved
```

### When to Use

**Automate deterministic endpoints**:
- ✅ Tests pass + feature complete → Commit
- ✅ Docs changed → Update related docs
- ✅ Task done → Close ticket
- ✅ Context >80% → Suggest compact
- ✅ Switching tasks → Create marker

**Don't automate when**:
- ❌ Secrets in files (warn, don't commit)
- ❌ Multiple unrelated changes (ask to split)
- ❌ Tests failing (don't commit)
- ❌ Ambiguous completion state

**Implementation**:
```markdown
# In CLAUDE.md

## Autonomous Completion Protocol

When implementation complete:
1. Verify tests pass
2. Review changes
3. Execute completion:
   - Commit (conventional format)
   - Update docs (if needed)
   - Close ticket (if configured)
   - Create marker
4. Suggest compact (if context >80%)

NO PROMPTS NEEDED
```

### Proven By

**Navigator's CLAUDE.md**:
- Autonomous protocol documented
- Zero "please commit" prompts
- **Result**: 100% elimination of completion prompts

---

## 6. Context Markers (Compress Decisions)

### Principle

**Preserve decisions, not raw data**

### Implementation

**Pattern**:
```
Context marker contains:
├─ What was decided (not full conversation)
├─ Why (rationale, key points)
├─ What was built (summary, not full code)
├─ Next steps (what's pending)
└─ References (where to find details)

Compressed: 5k tokens (vs 200k full session)
Compression: 97.5%
```

**Example**:

**Full session** (200k tokens):
```
User: "Let's implement authentication"
AI: "What approach?"
User: "JWT tokens"
AI: "Here's the implementation..."
[50 exchanges, full code, questions, answers, iterations]
```

**Context marker** (5k tokens):
```markdown
# Auth Implementation - v1

## Decision
JWT-based authentication with refresh tokens

## Rationale
- Stateless (scales horizontally)
- Refresh tokens for security
- Standard implementation

## Implementation
- Added auth middleware (src/middleware/auth.ts)
- Created token service (src/services/tokens.ts)
- Updated user routes (src/routes/users.ts)

## Next Steps
- Add rate limiting
- Implement password reset
- Add 2FA support

## References
- Task doc: .agent/tasks/TASK-05-auth.md
- API design: .agent/system/api-design.md
```

**Resume from marker**:
- Load 5k tokens
- Understand decisions
- Continue work
- No information loss (preserved what matters)

### Proof

**Navigator's marker system**:
```
Full session context: ~200k tokens
Context marker: ~5k tokens
Compression: 97.5%

Preserved:
✓ What was decided
✓ Why it was decided
✓ What was built
✓ What's next

Lost (intentionally):
✗ Full conversation transcript
✗ All code iterations (final version in codebase)
✗ Exploratory dead ends
```

**Git-tracked**, project-specific, resumable instantly.

### When to Use

**Create markers when**:
- ✅ Switching tasks (preserve current work)
- ✅ Taking break (resume later)
- ✅ Before risky changes (save point)
- ✅ After major decisions (document choice)
- ✅ Context >60% (prepare for compact)

**Don't create when**:
- ❌ Just started (nothing to preserve)
- ❌ Mid-conversation (not at decision point)
- ❌ No significant decisions made

**Workflow**:
```
Option 1: Manual
"Create context marker: feature-name-v1"

Option 2: Automatic (Navigator)
Feature complete → Auto-creates marker

Resume:
"Resume from marker: feature-name-v1"
→ Loads 5k tokens
→ Full context restored (decisions preserved)
```

### Proven By

**Navigator's marker system**:
- `.agent/markers/` directory
- Git-tracked (version controlled)
- 97.7% compression measured
- **Result**: Resume in seconds, not hours

---

## 7. Agent-Optimized Search

### Principle

**Use Task agent for exploration, manual Read for known files**

### Implementation

**Pattern**:
```
Multi-file exploration → Task agent
├─ Agent searches codebase
├─ Reads relevant files
├─ Summarizes findings
├─ Returns curated results (8k vs 80k)
└─ Optimization: 90% token savings

Known file → Manual Read
├─ You know exact path
├─ Single file needed
├─ No exploration required
└─ Direct, efficient
```

**Example** (Finding authentication flow):

**Manual approach**:
```
Read src/auth/login.ts (5k)
Read src/auth/signup.ts (4k)
Read src/auth/middleware.ts (3k)
Read src/auth/tokens.ts (4k)
Read src/auth/validation.ts (3k)
...
Total: 80k tokens (reading 15 files)
Time: 10 minutes
```

**Agent approach**:
```
"Find all authentication implementation files
and explain the auth flow"

Agent:
├─ Searches for auth-related files
├─ Identifies relevant files (15 files)
├─ Reads them (understands structure)
├─ Extracts relevant parts
└─ Summarizes: "Auth flow uses JWT with..."

Returns: 8k tokens (curated summary)
Time: 30 seconds
Savings: 90%
```

### Proof

**Measured comparisons**:
```
Task: Find all API endpoints
Manual: Read 20 route files = 80k tokens, 10 min
Agent: Search + summarize = 8k tokens, 30 sec
Savings: 90% tokens, 95% time

Task: Understand database schema
Manual: Read 15 model files = 60k tokens, 8 min
Agent: Analyze + explain = 6k tokens, 20 sec
Savings: 90% tokens, 96% time
```

### When to Use

**Use Task agent for**:
- ✅ "Find all X in the codebase"
- ✅ "How does Y work?" (multi-file)
- ✅ "Where is Z implemented?"
- ✅ Pattern discovery
- ✅ Unfamiliar code exploration

**Use manual Read for**:
- ✅ Known file, known path
- ✅ Single file needed
- ✅ File already in context
- ✅ Small targeted edits

**Decision tree**:
```
Do you know exact file?
├─ Yes → Manual Read
└─ No → Task agent

Will you need multiple files?
├─ Yes (>3 files) → Task agent
└─ No → Manual Read

Are you exploring unfamiliar code?
├─ Yes → Task agent
└─ No → Manual Read
```

### Proven By

**Navigator's agent integration**:
- Task agent for multi-file searches
- 80-90% token savings measured
- **Result**: Exploration without context bloat

---

## Summary Table

| Pattern | Principle | Savings | When to Use |
|---------|-----------|---------|-------------|
| **Lazy Loading** | Load on-demand | 92% tokens | Always (foundation) |
| **Direct MCP** | Eliminate middleware | 95% steps | MCP integrations |
| **Preprocessing** | Right tool for job | 92% tokens | Structured data |
| **Progressive Refinement** | Metadata first | 50-87% tokens | Large docs |
| **Autonomous Completion** | No manual prompts | 100% prompts | Deterministic workflows |
| **Context Markers** | Compress decisions | 97.5% tokens | Task switching |
| **Agent Search** | Curated exploration | 90% tokens | Multi-file search |

---

## Combining Patterns

**Patterns work together**:

```
Feature implementation workflow:

1. Lazy Loading (Pattern #1)
   └─ Start: Navigator + Task doc (5k)

2. Agent Search (Pattern #7)
   └─ Explore relevant code (8k curated)

3. Progressive Refinement (Pattern #4)
   └─ Load system docs only if needed (5k)

4. Preprocessing (Pattern #3) [if needed]
   └─ Parse structured data with Python

5. Autonomous Completion (Pattern #5)
   └─ Commit, docs, ticket (no prompts)

6. Context Marker (Pattern #6)
   └─ Preserve decisions (5k compressed)

Total context: ~25k tokens (vs 150k bulk loading)
Savings: 83%
```

---

## Learning More

**Philosophy**:
→ [Context Efficiency Manifesto](./CONTEXT-EFFICIENCY.md)

**Failure modes**:
→ [Anti-Patterns](./ANTI-PATTERNS.md)

**Application guides**:
→ `.agent/learning/` (detailed guides with examples)

**Start using**:
```
"Start my Navigator session"
```

---

**These patterns are proven, not theoretical.**

**92% token savings. Verified via OpenTelemetry.**

**Apply them. Measure results. Share your efficiency score.**

**Check your baseline: `"Show me my session statistics"`**
