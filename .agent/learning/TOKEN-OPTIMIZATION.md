# Token Optimization: Complete Strategy Guide

**Part of**: Navigator v4.0 Education Layer
**Level**: Advanced
**Read Time**: 12 minutes
**Prerequisites**: [CONTEXT-BUDGETS.md](./CONTEXT-BUDGETS.md), [PREPROCESSING-VS-LLM.md](./PREPROCESSING-VS-LLM.md), [PROGRESSIVE-REFINEMENT.md](./PROGRESSIVE-REFINEMENT.md)

---

## Overview

Token optimization is the practice of **maximizing work per token spent**.

This guide consolidates all Navigator optimization strategies into a single reference.

---

## The 10 Core Strategies

### 1. Lazy Loading (70-90% savings)

**Principle**: Load documentation only when needed

**Implementation**:
```
❌ Session start: Load all docs (150k)
✅ Session start: Load navigator (2k)
✅ Exchange 3: Load specific doc (4k)
✅ Exchange 7: Load related SOP (2k)

Savings: 142k tokens (95%)
```

**When to use**: Every session, always

**Metrics**:
- Target: <15k docs loaded per session
- Excellent: <10k
- Baseline: 150k (all docs)

**See**: [PROGRESSIVE-REFINEMENT.md](./PROGRESSIVE-REFINEMENT.md)

---

### 2. Agent-Assisted Search (60-80% savings)

**Principle**: Use agents to read many files, return summary

**Implementation**:
```
❌ Read 20 files manually (80k tokens)
✅ Agent reads 20 files, returns 4k summary

Savings: 76k tokens (95%)
```

**When to use**:
- Multi-file code exploration
- Understanding unfamiliar patterns
- Finding examples across codebase
- Answering "how does X work?"

**Metrics**:
- Agent search: 3-5k result
- Manual reads: 40-80k for same info
- Savings: 92-95%

**See**: [PREPROCESSING-VS-LLM.md](./PREPROCESSING-VS-LLM.md)

---

### 3. Context Markers (97%+ compression)

**Principle**: Compress decisions into markers, avoid re-reading docs

**Implementation**:
```
Session 1:
├── Load docs (15k)
├── Make decisions
└── Create marker (0.5k) - compressed decisions only

Session 2:
└── Load marker (0.5k) - resume without re-loading docs

Savings: 14.5k tokens (97%)
```

**When to use**:
- Completing isolated subtask
- Taking break mid-feature
- Switching between unrelated tasks
- Before/after compact

**Metrics**:
- Original context: 15-30k tokens
- Marker size: 0.5-2k tokens
- Compression: 95-98%

**See**: README.md § Context Markers

---

### 4. Preprocessing (0 tokens)

**Principle**: Use scripts/functions for deterministic tasks

**Implementation**:
```
❌ LLM parsing JSON (15k tokens, 85% accuracy)
✅ Python json.load() (0 tokens, 100% accuracy)

❌ LLM counting files (2k tokens)
✅ Bash ls | wc -l (0 tokens)

❌ LLM formatting dates (3k tokens)
✅ Python datetime (0 tokens)

Savings: 100% (preprocessing costs 0 tokens)
```

**When to use**:
- Parsing structured data (JSON, XML, CSV)
- Pattern matching (regex, file search)
- Math calculations
- Format conversions
- Data validation

**Metrics**:
- Preprocessing: 0 tokens always
- LLM alternative: 2-20k tokens
- Savings: 100%

**See**: [PREPROCESSING-VS-LLM.md](./PREPROCESSING-VS-LLM.md)

---

### 5. Predefined Functions (80-95% savings)

**Principle**: Template-based generation with 0-token functions

**Implementation**:
```
❌ LLM generates task doc (5k tokens per doc)
✅ Predefined function generates template (0 tokens)
✅ LLM fills semantic content only (1k tokens)

Savings: 4k tokens per task doc (80%)
```

**When to use**:
- Generating consistent structured content
- Formatting reports
- Creating boilerplate code
- Validating schemas

**Metrics**:
- Pure LLM: 5-10k tokens
- Function + LLM: 1-2k tokens
- Savings: 60-80%

**See**: Navigator skills (nav-task, nav-sop, etc.)

---

### 6. Direct MCP (Eliminate Middleware)

**Principle**: Connect directly to tools without orchestration overhead

**Implementation**:
```
❌ Load Figma docs (30k) → Ask LLM to call API → Parse result
✅ Direct MCP to Figma → Python extracts data → Return summary

Traditional approach: 30k tokens loaded + 5k orchestration = 35k
Direct MCP: 0k loaded + 3k summary = 3k

Savings: 32k tokens (91%)
```

**When to use**:
- External integrations (Figma, Linear, GitHub)
- Database queries
- API interactions
- File system operations

**Metrics**:
- With docs + orchestration: 20-50k tokens
- Direct MCP: 2-5k tokens
- Savings: 85-95%

**See**: [PATTERNS.md](../philosophy/PATTERNS.md) § Direct MCP

---

### 7. Smart Compact (Reset Without Losing Context)

**Principle**: Clear conversation history, preserve decisions via markers

**Implementation**:
```
Task 1: Complete feature (context: 45%)
├── Create marker (1k)
└── Compact (clear history)

Task 2: Start fresh (context: 15%)
└── Load marker (1k) - decisions preserved

Result: Two tasks in one session instead of restart
```

**When to use**:
- Between independent subtasks
- After completing isolated work
- Before switching contexts
- When context usage >60%

**Metrics**:
- Before compact: 60-80% context used
- After compact: 15-25% context used
- Sessions extended: 2-3x longer

**See**: CLAUDE.md § Smart Compact Strategy

---

### 8. Incremental Section Loading (50-80% savings)

**Principle**: Load specific sections of large docs, not entire files

**Implementation**:
```
❌ Load entire 10k architecture doc
✅ Load Testing section only (2k)

Savings: 8k tokens (80%)
```

**When to use**:
- Large documentation files (>5k tokens)
- Only need specific subsection
- Exploring table of contents first

**Metrics**:
- Full doc: 5-15k tokens
- Specific section: 1-3k tokens
- Savings: 60-80%

**Implementation**:
- Read tool supports offset + limit
- Request lines 100-300 instead of 1-500

---

### 9. Cache Optimization (Write Once, Read Free)

**Principle**: Leverage Claude Code's prompt caching

**Implementation**:
```
CLAUDE.md (15k tokens):
├── First exchange: 15k tokens (cache creation)
└── All subsequent exchanges: 0 tokens (cache read)

Session with 10 exchanges:
Without caching: 15k × 10 = 150k tokens
With caching: 15k + (0 × 9) = 15k tokens

Savings: 135k tokens (90%)
```

**When to use**: Automatic for CLAUDE.md and system messages

**Metrics**:
- Cache efficiency: Aim for >95%
- Cache read tokens: Should be 10-20x cache creation
- Session stats show cache performance

**See**: OpenTelemetry metrics

---

### 10. Autonomous Completion (Save Manual Orchestration)

**Principle**: AI executes finish protocol without prompts

**Implementation**:
```
❌ Traditional:
User: "Please commit these changes"
User: "Now close the ticket"
User: "Update documentation"
User: "Create a marker"
Result: 4 round trips, 8k tokens orchestration

✅ Autonomous:
AI automatically:
├── Commits changes
├── Closes ticket
├── Updates docs
└── Creates marker
Result: 0 orchestration tokens

Savings: 8k tokens per task (100%)
```

**When to use**: Every task completion

**Metrics**:
- Manual: 6-10k orchestration tokens per task
- Autonomous: 0 tokens
- Savings: 100%

**See**: [autonomous-completion.md](../sops/development/autonomous-completion.md)

---

## Combined Strategies: Real Workflows

### Workflow 1: Implementing New Feature

**Optimized approach**:
```
1. Lazy Loading
   └── Load navigator (2k), not all docs (150k)

2. Progressive Refinement
   ├── Load task doc (3k)
   └── Load system doc (5k)

3. Agent Search
   └── Find similar patterns (4k summary vs 40k manual reads)

4. Preprocessing
   └── Generate boilerplate with scripts (0 tokens)

5. Predefined Functions
   └── Create consistent test files (1k vs 5k pure LLM)

6. Autonomous Completion
   └── Finish without prompts (0 orchestration tokens)

7. Smart Compact + Marker
   └── Archive work (1k marker), ready for next task

Total: 16k tokens
Baseline (traditional): 250k tokens
Savings: 234k tokens (94%)
```

### Workflow 2: Design Review (Figma → Implementation)

**Optimized approach**:
```
1. Direct MCP
   └── Figma MCP connection (no docs loaded)

2. Preprocessing
   ├── Python extracts design tokens (0 tokens)
   ├── DTCG format conversion (0 tokens)
   └── Component detection (0 tokens)

3. LLM (Semantic Layer)
   ├── Match components to design system (3k)
   ├── Identify naming inconsistencies (1k)
   └── Generate implementation plan (2k)

4. Predefined Functions
   └── Format report with template (0 tokens)

5. Autonomous Completion
   └── Create task doc, archive plan (0 orchestration)

Total: 6k tokens
Baseline (manual + docs): 80k tokens
Savings: 74k tokens (92%)
Time: 5 minutes vs 6-10 hours
```

### Workflow 3: Debugging Production Issue

**Optimized approach**:
```
1. Lazy Loading
   └── Load navigator (2k)

2. Progressive Refinement
   └── Navigate to debugging SOP (2k)

3. Agent Search
   └── Find similar past issues (3k summary)

4. Preprocessing
   └── Extract error logs with grep (0 tokens)

5. LLM Analysis
   └── Interpret logs, suggest fix (4k)

6. Cache Optimization
   └── CLAUDE.md cached (0 tokens re-read)

7. Marker Creation
   └── Document solution (1k compressed)

Total: 12k tokens
Baseline: 65k tokens (load all debugging docs + system architecture)
Savings: 53k tokens (82%)
```

---

## Decision Trees

### When to Load Documentation

```
┌─────────────────────────────────┐
│ Do I know what doc I need?      │
└──────────┬──────────────────────┘
           │
     ┌─────┴─────┐
     │           │
    YES         NO
     │           │
     ▼           ▼
┌─────────┐  ┌──────────────┐
│ Load    │  │ Load         │
│ specific│  │ navigator    │
│ doc     │  │ first        │
│ (3-5k)  │  │ (2k)         │
└─────────┘  └──────┬───────┘
                    │
                    ▼
             ┌──────────────┐
             │ Check index, │
             │ then load    │
             │ specific doc │
             └──────────────┘
```

### When to Use Agent vs Manual Read

```
┌─────────────────────────────────┐
│ How many files involved?        │
└──────────┬──────────────────────┘
           │
     ┌─────┴─────┐
     │           │
    1-2        3+
     │           │
     ▼           ▼
┌─────────┐  ┌──────────────┐
│ Read    │  │ Use agent    │
│ manually│  │ search       │
│ (3-6k)  │  │ (3-5k total) │
└─────────┘  └──────────────┘
                    │
                    ▼
             ┌──────────────┐
             │ Load 1-2     │
             │ specific     │
             │ files if     │
             │ needed       │
             └──────────────┘
```

### When to Compact

```
┌─────────────────────────────────┐
│ Context usage > 60%?            │
└──────────┬──────────────────────┘
           │
     ┌─────┴─────┐
     │           │
    YES         NO
     │           │
     ▼           │
┌─────────┐      │
│ Current │      │
│ task    │      │
│ done?   │      │
└────┬────┘      │
     │           │
  ┌──┴──┐        │
  │     │        │
 YES   NO        │
  │     │        │
  ▼     ▼        ▼
┌────┐ ┌────┐ ┌────┐
│COM-│ │WAIT│ │CON-│
│PACT│ │FOR│ │TIN-│
│NOW │ │TASK│ │UE  │
└────┘ └────┘ └────┘
```

### When to Use Preprocessing vs LLM

```
┌─────────────────────────────────┐
│ Is task deterministic?          │
│ (same input = same output)      │
└──────────┬──────────────────────┘
           │
     ┌─────┴─────┐
     │           │
    YES         NO
     │           │
     ▼           ▼
┌─────────┐  ┌──────────────┐
│ PRE-    │  │ Semantic     │
│ PROCESS │  │ under-       │
│ (0      │  │ standing     │
│ tokens) │  │ needed?      │
└─────────┘  └──────┬───────┘
                    │
              ┌─────┴─────┐
              │           │
             YES         NO
              │           │
              ▼           ▼
         ┌────────┐  ┌──────────┐
         │ USE    │  │ HYBRID:  │
         │ LLM    │  │ PRE +    │
         │ (3-10k)│  │ LLM      │
         └────────┘  └──────────┘
```

---

## Optimization Checklist

### Before Every Session

- [ ] Start with navigator (not upfront loading)
- [ ] Understand what docs exist before loading
- [ ] Plan which docs you'll likely need
- [ ] Check context budget allocation

### During Session

- [ ] Load docs on-demand (not preemptively)
- [ ] Use agents for multi-file exploration
- [ ] Use preprocessing for deterministic tasks
- [ ] Monitor context usage (stay below 60%)
- [ ] Create markers between subtasks

### After Task Completion

- [ ] Review session efficiency stats
- [ ] Create marker if continuing later
- [ ] Compact if switching contexts
- [ ] Archive completed task docs
- [ ] Note what worked for future sessions

### Continuous Improvement

- [ ] Check efficiency scores regularly
- [ ] Learn from low-scoring sessions
- [ ] Update documentation based on patterns
- [ ] Share optimizations with team

---

## Measuring Optimization Success

### Key Metrics

**1. Token Savings Rate**
```
Savings Rate = (Baseline - Loaded) / Baseline × 100%

Example:
Baseline: 150k (all docs)
Loaded: 12k (navigator + 2 docs)
Savings: 92%

Target: >70%
Excellent: >85%
```

**2. Context Efficiency**
```
Efficiency = Tokens Used / Tokens Loaded × 100%

Example:
Loaded: 12k
Actually referenced: 11k
Efficiency: 92%

Target: >80%
Excellent: >90%
```

**3. Session Extension Factor**
```
Extension = Optimized Exchanges / Baseline Exchanges

Example:
Baseline approach: 5-7 exchanges before crash
Optimized approach: 15-20 exchanges
Extension: 3x

Target: >2x
Excellent: >3x
```

**4. Overall Efficiency Score** (Navigator's metric)
```
Score = Weighted average of:
├── Token savings (40 points)
├── Cache efficiency (30 points)
└── Context usage (30 points)

Target: >70/100
Excellent: >85/100
```

### Using Session Stats

```bash
"Show me my session statistics"
```

**Example output**:
```
Session Efficiency Report
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Documentation loaded:    12k tokens
Baseline (all docs):     150k tokens
Tokens saved:            138k (92%)

Agent searches:          3 used
Manual reads saved:      ~15 files

Cache efficiency:        99.7%
Context usage:           35% (excellent)
Efficiency score:        94/100

Time saved this session: ~42 minutes
```

**What to optimize if scores are low**:
- **Savings <70%**: Using upfront loading, not lazy loading
- **Context >60%**: Too many docs loaded, use agents more
- **Cache <95%**: Session too short to leverage caching
- **Score <70**: Review all strategies, multiple issues

---

## Anti-Patterns (What NOT to Do)

### 1. Upfront Loading
```
❌ Load all docs at session start "just in case"
✅ Load navigator, fetch on-demand

Waste: 90-95% of loaded tokens
```

### 2. Manual File Reading Spree
```
❌ Read 20 files manually to understand codebase
✅ Use agent (reads 20 files, returns 4k summary)

Waste: 75-90k tokens
```

### 3. LLM for Deterministic Tasks
```
❌ Ask LLM to parse JSON, count files, format dates
✅ Use preprocessing (Python, bash, tools)

Waste: 100% (preprocessing costs 0)
```

### 4. No Compact Strategy
```
❌ Work until context full, then restart
✅ Compact proactively between tasks

Waste: Entire session context lost
```

### 5. Ignoring Markers
```
❌ Re-load same 15k docs every session
✅ Create marker (0.5k), load marker next time

Waste: 14.5k tokens per session (97%)
```

### 6. Re-Reading Documentation
```
❌ "What was that SOP again?" → Re-load 3k doc
✅ Use marker to preserve key decisions

Waste: 3k tokens every re-read
```

### 7. Loading Complete Files
```
❌ Load 10k architecture doc for one section
✅ Load specific section (2k) using offset/limit

Waste: 8k tokens (80%)
```

### 8. Manual Orchestration
```
❌ "Please commit" "Close ticket" "Update docs" (8k tokens)
✅ Autonomous completion (0 tokens)

Waste: 6-10k per task
```

---

## Advanced Techniques

### Technique 1: Layered Loading

Load documentation in tiers based on likelihood:

```
Tier 1 (Always): Navigator (2k)
Tier 2 (Likely): Current task doc (3k)
Tier 3 (Maybe): Related system doc (5k)
Tier 4 (Rarely): Deep dive SOP (2k)

Load Tier 1 immediately
Load Tier 2 at first need
Load Tier 3 only if required
Load Tier 4 only for edge cases

Typical session: Tier 1 + Tier 2 = 5k tokens
vs loading all tiers: 12k tokens
Savings: 58%
```

### Technique 2: Selective Context Preservation

In markers, preserve decisions but not raw data:

```
❌ Store: "We decided to use JWT. Here are all the token formats, expiry times, refresh logic..."
✅ Store: "We decided to use JWT (see auth-sop.md for implementation)"

Bad marker: 2k tokens
Good marker: 0.3k tokens
Savings: 85%
```

### Technique 3: Agent Chaining

Use multiple agent calls strategically:

```
Agent 1: "Find all authentication-related files"
Result: List of 15 files (1k)

Agent 2: "From these 15 files, which implement JWT?"
Result: 3 specific files (1k)

Load manually: Read 3 files (9k)

Total: 11k tokens
vs Reading all 15 files: 45k tokens
Savings: 76%
```

### Technique 4: Differential Updates

Update markers with only new information:

```
Session 1:
├── Create marker (1k)
└── Base context preserved

Session 2:
├── Load marker (1k)
├── New decision made
└── Update marker: +0.2k (delta only)

Total marker: 1.2k
vs Re-creating from scratch: 2k
Savings: 40%
```

---

## ROI Calculations

### Time Saved

```
Token savings: 138k per session
Time per token: ~6ms (reading + processing)
Time saved: 138k × 6ms = 828 seconds = 14 minutes

Sessions per day: 4
Daily time saved: 56 minutes
Weekly time saved: 4.7 hours
Monthly time saved: 20 hours

Value: 2.5 extra work days per month
```

### Cost Saved (API Pricing)

```
Baseline session: 150k input tokens
Optimized session: 12k input tokens
Savings: 138k tokens per session

Pricing (Sonnet): $3 per million input tokens
Cost per session saved: $0.414
Sessions per month: 80
Monthly savings: $33.12

Annual savings: ~$400 per developer
Team of 10: $4,000/year
```

### Quality Improvements

**Fewer context restarts**:
- Baseline: Restart every 5-7 exchanges
- Optimized: Restart every 20+ exchanges
- Productivity: 3x longer deep work sessions

**Better accuracy**:
- Preprocessing: 100% accuracy (vs 85-95% LLM)
- Fewer hallucinations: Context not overloaded
- Consistent output: Templates + functions

**Reduced cognitive load**:
- No manual orchestration (autonomous completion)
- No "which doc do I need?" (navigator guides)
- No "did I already read this?" (markers track state)

---

## Next Steps

### Apply What You Learned

- **[TRY-THIS-LAZY-LOADING.md](./examples/TRY-THIS-LAZY-LOADING.md)** - Hands-on lazy loading exercise
- **[TRY-THIS-AGENT-SEARCH.md](./examples/TRY-THIS-AGENT-SEARCH.md)** - See agent optimization live
- **[TRY-THIS-MARKERS.md](./examples/TRY-THIS-MARKERS.md)** - Context compression demo

### Deep Dives

- **[CONTEXT-BUDGETS.md](./CONTEXT-BUDGETS.md)** - Token allocation strategies
- **[PREPROCESSING-VS-LLM.md](./PREPROCESSING-VS-LLM.md)** - Right tool decisions
- **[PROGRESSIVE-REFINEMENT.md](./PROGRESSIVE-REFINEMENT.md)** - Metadata → details pattern

### Philosophy

- **[CONTEXT-EFFICIENCY.md](../philosophy/CONTEXT-EFFICIENCY.md)** - The manifesto
- **[PATTERNS.md](../philosophy/PATTERNS.md)** - All success patterns
- **[ANTI-PATTERNS.md](../philosophy/ANTI-PATTERNS.md)** - Common mistakes

---

**Bottom line**: Token optimization compounds. Each strategy saves 60-95%. Combined, they deliver 92-95% total savings. This transforms AI development from "fight the context window" to "context is never a concern."

**Navigator's role**: Implements all 10 strategies automatically through its architecture, giving you 90%+ optimization without thinking about it.
