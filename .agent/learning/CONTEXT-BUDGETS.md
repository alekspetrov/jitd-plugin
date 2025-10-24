# Context Budgets: How to Think About Token Allocation

**Part of**: Navigator v4.0 Education Layer
**Level**: Fundamental
**Read Time**: 8 minutes
**Prerequisites**: Basic understanding of LLM context windows

---

## The Mental Model

Think of your context window like **RAM in a computer**:
- **Fixed capacity**: 200k tokens (Claude Sonnet)
- **Shared resource**: System, tools, conversation, documentation
- **Performance degrades**: As it fills up
- **Crashes when full**: Session restart required

Most developers don't think about token allocation until it's too late.

**Navigator's principle**: Budget tokens upfront, prevent crashes downstream.

---

## Your Context Budget Breakdown

### Typical Claude Code Session (200k total)

```
┌─────────────────────────────────────────┐
│ System + Tools:        ~50k (25%)       │  Fixed overhead
│ ─────────────────────────────────────── │
│ CLAUDE.md:             ~15k (7.5%)      │  Project configuration
│ ─────────────────────────────────────── │
│ Documentation:         ~66k (33%)       │  ⚠️ This is where you optimize
│ ─────────────────────────────────────── │
│ Conversation History:  ~60k (30%)       │  Grows with each exchange
│ ─────────────────────────────────────── │
│ Available Buffer:       ~9k (4.5%)      │  Safety margin
└─────────────────────────────────────────┘
```

**The problem**: Documentation is the largest controllable cost.

**The opportunity**: Reduce 66k → 12k without losing capability.

---

## The Default Approach (Why It Fails)

### Anti-Pattern: Load Everything Upfront

**Logic**: "Better to have it available just in case"

**Reality**:
```
Session Start:
├── Load all system architecture docs     (20k)
├── Load all API documentation            (15k)
├── Load all SOPs                         (12k)
├── Load all integration guides           (10k)
├── Load all examples                      (9k)
└── Total loaded:                         66k tokens

5 exchanges later:
├── Documentation used:                    5k tokens
├── Documentation wasted:                 61k tokens
├── Context remaining:                     4k tokens
└── Session status:                       💥 CRASHED
```

**Efficiency**: 7.5% (used 5k of 66k loaded)
**Result**: Session dies in 5-7 exchanges

---

## The Navigator Approach

### Pattern: Lazy Load + Progressive Refinement

**Logic**: "Load what you need, when you need it"

**Reality**:
```
Session Start:
└── Load navigator only                    (2k)

Exchange 1: "I need to understand authentication"
├── Navigate to auth system doc location
└── Load auth architecture                 (5k)

Exchange 3: "How do I add a new endpoint?"
├── Navigate to API patterns
└── Load endpoint SOP                      (2k)

Exchange 7: "Debug login failure"
└── Load auth debugging SOP                (2k)

Session total:
├── Documentation loaded:                 11k tokens
├── Context remaining:                    60k tokens
└── Session status:                       ✅ HEALTHY (15+ exchanges)
```

**Efficiency**: 92% reduction vs upfront (11k vs 66k)
**Result**: 3x longer sessions

---

## Calculating Your Budget

### Formula: Available Context

```
Available = Total - (System + Config + Loaded + History)

Example (Exchange 5):
Available = 200k - (50k + 15k + 11k + 45k)
Available = 79k tokens
Usage = 60.5%  ✅ EXCELLENT

Example (Exchange 5, upfront loading):
Available = 200k - (50k + 15k + 66k + 45k)
Available = 24k tokens
Usage = 88%  ⚠️ DANGER ZONE
```

**Thresholds**:
- **<40% used**: Excellent (can work for hours)
- **40-60% used**: Good (10+ exchanges comfortable)
- **60-80% used**: Warning (consider compact)
- **>80% used**: Critical (compact now or session dies)

---

## Token Costs: What Actually Uses Tokens?

### High Cost Operations

| Operation | Token Cost | When Needed |
|-----------|-----------|-------------|
| Load all system docs | 20-30k | Almost never |
| Read 20+ files manually | 50-80k | Use agent instead |
| Load comprehensive API docs | 15-25k | Load specific endpoints |
| Full codebase search results | 40-60k | Use agent (returns 3-5k summary) |

### Low Cost Operations

| Operation | Token Cost | When Needed |
|-----------|-----------|-------------|
| Load navigator | 2-3k | Every session start |
| Load single system doc | 3-5k | When relevant to task |
| Load single SOP | 2-3k | When encountering issue |
| Agent search result | 3-5k | Instead of manual file reads |
| Context marker | 0.5-2k | Compressed decisions only |

---

## Budget Strategies by Task Type

### Strategy 1: Feature Implementation

**Budget allocation**:
```
Start: Navigator (2k)
Task: Load task doc (3k)
Architecture: Load relevant system doc (5k)
Total: 10k tokens (95% cheaper than loading all docs)
```

**When to load more**:
- Integration needed → Load integration SOP (2k)
- Unfamiliar pattern → Use agent to search (3k result)
- Testing approach → Load testing guide (2k)

**Budget rule**: Load <15k for entire feature

### Strategy 2: Debugging

**Budget allocation**:
```
Start: Navigator (2k)
Context: Load debugging SOP (2k)
Architecture: Load relevant system doc if needed (5k)
Total: 9k tokens
```

**When to load more**:
- Complex issue → Use agent to find similar bugs (3k)
- Integration issue → Load integration SOP (2k)
- Need examples → Load specific example (1k)

**Budget rule**: Load <12k for entire debug session

### Strategy 3: Research/Discovery

**Budget allocation**:
```
Start: Navigator (2k)
Research: Use agent for multi-file search (4k result)
Deep dive: Load 1-2 specific files (3k)
Total: 9k tokens
```

**Why agent matters**:
- **Manual approach**: Read 20 files = 80k tokens
- **Agent approach**: Agent reads 20 files, returns 4k summary
- **Savings**: 95% token reduction

**Budget rule**: Use agents for exploration, load <10k

---

## Progressive Refinement: The Key Pattern

### How It Works

Instead of loading full documentation, fetch in stages:

```
Stage 1: Navigator (2k)
  ├── Shows: What documentation exists
  └── Cost: 2k tokens

Stage 2: Metadata (0k additional)
  ├── Shows: File names, headings, summaries
  └── Cost: Already in navigator

Stage 3: Specific Document (3-5k)
  ├── Shows: Full content of ONE relevant doc
  └── Cost: 3-5k tokens only

Stage 4: Deep Dive (2k)
  ├── Shows: Related SOP or example if needed
  └── Cost: 2k tokens only

Total: 7-9k tokens vs 66k (87% savings)
```

### Example: Adding Authentication

**❌ Upfront approach**:
```
1. Load all system docs (30k)
2. Load all security SOPs (10k)
3. Load all API examples (8k)
Total: 48k tokens
Context: 76% used after 2 exchanges
```

**✅ Navigator approach**:
```
1. Load navigator (2k)
2. Navigate → "Need auth system architecture"
3. Load auth system doc (4k)
4. Later: "How to implement JWT?"
5. Load JWT SOP (2k)
Total: 8k tokens
Context: 42% used after 10 exchanges
```

---

## Measuring Your Efficiency

### Use Navigator's Session Stats

```bash
# Check your current session efficiency
"Show me my session statistics"
```

**What to look for**:

```
Session Efficiency Report
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Documentation loaded:    12k tokens
Baseline (all docs):     150k tokens
Tokens saved:            138k (92%)

Context usage:           35% (excellent)
Efficiency score:        94/100

Time saved this session: ~42 minutes
```

**Good scores**:
- **Savings**: >70% vs baseline
- **Context usage**: <60%
- **Efficiency score**: >70/100

**If scores are low**:
- Using upfront loading instead of navigator?
- Reading files manually instead of using agents?
- Loading docs "just in case" instead of on-demand?

---

## Common Budget Mistakes

### Mistake 1: "Just in Case" Loading

**Thinking**: "I might need these 10 docs later"

**Reality**:
- Use 1-2 of the 10 docs
- Waste 25k tokens
- Session crashes before finishing task

**Fix**: Load navigator, fetch on-demand

### Mistake 2: Manual File Reading Spree

**Thinking**: "Let me read these 15 files to understand the codebase"

**Reality**:
- 60k tokens spent reading
- Retain 10% of information
- Context window nearly full

**Fix**: Use Task agent (reads 15 files, returns 4k summary)

### Mistake 3: Forgetting Conversation Growth

**Thinking**: "I have 50k tokens free, I'm fine"

**Reality**:
- Each exchange adds 5-10k (input + output)
- 5 exchanges = 30k tokens
- Suddenly at 85% capacity

**Fix**: Target <40% usage after doc loading

### Mistake 4: No Compact Strategy

**Thinking**: "I'll compact when I hit the limit"

**Reality**:
- Hit limit mid-task
- Lose flow and context
- Start over from scratch

**Fix**: Compact between independent tasks (proactive)

---

## Budget Optimization Checklist

Before starting any task:

- [ ] **Load navigator first** (establishes baseline)
- [ ] **Check what docs exist** (avoid loading unknown)
- [ ] **Load only relevant docs** (not entire categories)
- [ ] **Use agents for exploration** (60-80% token savings)
- [ ] **Monitor context usage** (stay below 60%)
- [ ] **Compact between tasks** (reset for next task)

During task:

- [ ] **Load docs on-demand** (not preemptively)
- [ ] **Fetch specific sections** (not entire files)
- [ ] **Use agent searches** (instead of reading 10+ files)
- [ ] **Check stats periodically** (catch budget issues early)

After task:

- [ ] **Review efficiency score** (learn from session)
- [ ] **Archive task docs** (reduce baseline for next session)
- [ ] **Compact if needed** (clear for unrelated work)

---

## Real-World Examples

### Example 1: Adding New Feature (Good Budget)

```
Start:       Navigator (2k) → 26% context used
Exchange 2:  Task doc (3k) → 29% context used
Exchange 4:  System doc (5k) → 34% context used
Exchange 8:  Integration SOP (2k) → 42% context used
Exchange 15: Complete feature → 58% context used
Status: ✅ Healthy, can continue to next task
```

### Example 2: Adding New Feature (Bad Budget)

```
Start:       Load all docs (66k) → 58% context used
Exchange 2:  Begin work → 64% context used
Exchange 4:  Debug issue → 72% context used
Exchange 6:  Almost done → 84% context used
Exchange 7:  Session crashes → 💥 Restart required
Status: ❌ Incomplete, lost 1+ hours
```

**Difference**: 92k tokens saved, 2x longer session

---

## Advanced: Budget for Multi-Task Sessions

### Strategy: Progressive Compact

Instead of one session = one task, use markers + compact:

```
Task 1: Feature A
├── Load navigator (2k)
├── Load task doc (3k)
├── Load system doc (5k)
├── Complete feature
├── Create marker (1k compressed)
└── Context: 38% used

Compact (clear conversation history)
└── Context reset: 15% used

Task 2: Feature B
├── Resume from marker (1k)
├── Load new task doc (3k)
├── Load new system doc (5k)
├── Complete feature
└── Context: 42% used

Result: 2 features in one extended session
```

**Without markers + compact**:
- Feature A: 38% context
- Feature B: 76% context (cumulative)
- Session crashes before completing B

**With markers + compact**:
- Feature A: 38% → marker (1k)
- Reset to 15%
- Feature B: 42%
- Both complete in one session

---

## Measuring ROI

### Time Saved Calculation

```
Tokens saved: 138k
Time per token: ~6ms (reading + processing)
Time saved: 138k × 6ms = 828 seconds = 14 minutes per session

Sessions per day: 4
Daily time saved: 56 minutes
Weekly time saved: 4.7 hours
Monthly time saved: 20 hours
```

**What you get back**:
- 20 hours/month = 2.5 extra work days
- Zero context crashes = zero frustrating restarts
- Longer sessions = deeper flow state

---

## Next Steps

### Learn More
- **[PREPROCESSING-VS-LLM.md](./PREPROCESSING-VS-LLM.md)** - When to use agents vs manual reads
- **[PROGRESSIVE-REFINEMENT.md](./PROGRESSIVE-REFINEMENT.md)** - Metadata → details pattern
- **[TOKEN-OPTIMIZATION.md](./TOKEN-OPTIMIZATION.md)** - Complete optimization strategies

### Try It Yourself
- **[TRY-THIS-LAZY-LOADING.md](./examples/TRY-THIS-LAZY-LOADING.md)** - Hands-on proof of lazy loading
- **[TRY-THIS-AGENT-SEARCH.md](./examples/TRY-THIS-AGENT-SEARCH.md)** - See agent token savings live

### References
- **[CONTEXT-EFFICIENCY.md](../philosophy/CONTEXT-EFFICIENCY.md)** - The manifesto
- **[PATTERNS.md](../philosophy/PATTERNS.md)** - Success patterns in detail

---

**Bottom line**: Context budgets are like financial budgets—easy to overspend, hard to recover. Plan ahead, spend strategically, measure results.

**Navigator's role**: Provides the tools (navigator, agents, markers, stats) to stay within budget automatically.
