# Try This: Lazy Loading in Action

**Part of**: Navigator v4.0 Education Layer
**Time**: 10 minutes
**Difficulty**: Beginner
**Goal**: Experience the token savings of lazy loading first-hand

---

## What You'll Learn

By the end of this exercise, you'll:
- See the difference between upfront loading and lazy loading
- Measure actual token savings
- Understand when to load documentation
- Experience Navigator's progressive refinement pattern

---

## Setup

**Prerequisites**:
- Navigator installed in a project
- Basic understanding of context windows

**Starting point**: Fresh Claude Code session

---

## Exercise 1: The Upfront Loading Anti-Pattern

### Step 1: Simulate Traditional Approach

```
DON'T ACTUALLY DO THIS - Just imagine:

Session start:
├── Load all system architecture docs
├── Load all SOPs
├── Load all task docs
├── Load all examples
└── "Now I'm ready to work!"
```

### Step 2: Estimate Token Cost

**Check your .agent/ directory**:
```bash
# Count total documentation size
find .agent -name "*.md" -exec wc -c {} + | tail -1
```

**Convert to tokens**: Characters ÷ 4 ≈ tokens

**Example**:
```
Total characters: 600,000
Estimated tokens: 150,000
Context used: 75% (before you start working!)
```

### Step 3: Predict Session Length

**With 75% context used at start**:
- Available for conversation: 50k tokens
- Each exchange: ~8-10k tokens (input + output)
- **Predicted session length**: 5-7 exchanges before crash

**Result**: Session dies mid-feature, restart required

---

## Exercise 2: The Navigator Approach

### Step 1: Start with Navigator

**In Claude Code**:
```
"Start my Navigator session"
```

**What loads**:
- `.agent/DEVELOPMENT-README.md` (navigator)
- Token cost: ~2-3k

**Check efficiency**:
```
"Show me my current context usage"
```

**Expected**: ~26% (50k system + 15k CLAUDE.md + 3k navigator ÷ 200k)

### Step 2: Navigate to What You Need

**Scenario**: You want to add a new feature

**In Claude Code**:
```
"What documentation exists for adding features?"
```

**Navigator response** (paraphrased):
```
Check navigator:
- system/project-architecture.md - Plugin structure
- system/plugin-patterns.md - Development patterns
- tasks/ - Existing implementation examples
```

**Token cost**: 0 additional (already in navigator)

### Step 3: Load Specific Documentation

**In Claude Code**:
```
"Load the plugin-patterns.md file"
```

**What loads**:
- `system/plugin-patterns.md` only
- Token cost: ~4-5k

**Check efficiency**:
```
"Show me my current context usage"
```

**Expected**: ~30% (previous 26% + 4k doc ÷ 200k)

### Step 4: Work on Feature

**In Claude Code**:
```
"I want to create a new skill for database migrations"
```

Claude Code implements the feature using:
- Navigator context (already loaded)
- plugin-patterns.md (already loaded)
- No additional doc loading needed

**After 5 exchanges**:
```
"Show me my current context usage"
```

**Expected**: ~42% (comfortable, can continue)

### Step 5: Load Additional Documentation On-Demand

**Scenario**: Need testing guidance

**In Claude Code**:
```
"How should I test this skill?"
```

**Navigator response**:
```
Check testing SOPs in navigator, load if needed
```

**Token cost**: ~2k (testing SOP)

**Total loaded so far**:
- Navigator: 3k
- Plugin patterns: 5k
- Testing SOP: 2k
- **Total**: 10k tokens

**Context usage**: ~47%

---

## Exercise 3: Compare Results

### Upfront Loading (Simulated)

```
Documentation loaded: 150k tokens
Context usage at start: 75%
Available for work: 50k tokens
Session length: 5-7 exchanges
Efficiency: 5% (used 8k of 150k loaded)
```

### Lazy Loading (Your Session)

```
Documentation loaded: 10k tokens
Context usage after feature: 47%
Available remaining: 106k tokens
Session length: 15-20+ exchanges
Efficiency: 100% (used all 10k loaded)
```

### Savings Calculation

```
Tokens saved: 150k - 10k = 140k
Savings percentage: 93%
Session extension: 3x longer
Time saved: ~14 minutes
```

---

## Exercise 4: Test Session Extension

### Step 6: Continue Without Restart

**In Claude Code**:
```
"Now I want to add another feature: API rate limiting"
```

**Navigator approach**:
- Checks navigator (already loaded)
- Loads additional doc if needed (~3k)
- Continues working

**After 10 total exchanges**:
```
"Show me my current context usage"
```

**Expected**: ~55% (still healthy)

### Step 7: Compare to Traditional Approach

**Traditional (simulated)**:
```
Exchange 7: Context full (90%)
Exchange 8: Session crashes
Result: Lost work, need to restart
```

**Navigator (your session)**:
```
Exchange 10: Context at 55%
Exchange 15: Context at 68%
Exchange 20: Context at 80% (still functional)
Result: 3x longer session, zero restarts
```

---

## Exercise 5: Measure Your Efficiency

### Step 8: Check Session Statistics

**In Claude Code**:
```
"Show me my session statistics"
```

**Expected output**:
```
Session Efficiency Report
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Documentation loaded:    13k tokens
Baseline (all docs):     150k tokens
Tokens saved:            137k (91%)

Context usage:           58% (excellent)
Efficiency score:        92/100

Time saved this session: ~41 minutes
```

### Step 9: Analyze Efficiency

**Questions to answer**:

1. **What was your token savings percentage?**
   - Target: >70%
   - Excellent: >85%

2. **What was your context usage?**
   - Target: <60%
   - Excellent: <50%

3. **How many exchanges did you complete?**
   - Baseline: 5-7
   - Target: >10
   - Excellent: >15

4. **Did you load any unnecessary documentation?**
   - Review what you loaded
   - Was 100% of it used?
   - Could you have been more selective?

---

## Key Takeaways

### What You Experienced

✅ **Lazy loading saves 90%+ tokens**
- Loaded 10-15k instead of 150k
- Achieved same results

✅ **Sessions last 3x longer**
- 15-20 exchanges vs 5-7
- Zero context crashes

✅ **100% utilization efficiency**
- Every loaded doc was used
- No waste

✅ **Progressive refinement works**
- Navigator → Specific doc → Additional docs as needed
- Each stage informed the next

### Common Patterns You Discovered

1. **Navigator is always first**
   - Provides index and navigation
   - Costs ~2k, saves 140k+

2. **Load on-demand, not "just in case"**
   - Don't preload testing docs if you're not testing yet
   - Fetch when actually needed

3. **Specific beats comprehensive**
   - Load plugin-patterns.md (5k), not all system docs (30k)
   - Target exactly what you need

4. **Context stays efficient**
   - Never approached 80% limit
   - Could continue for hours

---

## Variations to Try

### Variation 1: Agent-Assisted Loading

**Scenario**: You don't know which doc you need

```
"I need to understand how authentication works in this project"

Navigator approach:
1. Load navigator (2k)
2. Use agent: "Find auth-related documentation" (4k summary)
3. Load 1-2 specific files based on agent's findings (6k)

Total: 12k tokens
vs Reading all files manually: 60k tokens
Savings: 80%
```

### Variation 2: Multi-Task Session

**Scenario**: Complete 3 small tasks in one session

```
Task 1: Add feature (load 8k docs)
Create marker (0.5k compressed)
Compact (clear history, keep marker)

Task 2: Fix bug (load 5k docs + marker 0.5k)
Create marker (0.5k compressed)
Compact

Task 3: Update docs (load 3k docs + marker 0.5k)
Complete

Total loaded: 17.5k tokens across 3 tasks
vs 3 separate sessions with upfront loading: 450k tokens
Savings: 96%
```

### Variation 3: Deep Dive

**Scenario**: Need comprehensive understanding

```
Even for deep dives, lazy loading wins:

Load navigator (2k)
Load architecture doc (6k)
Load 3 integration SOPs (6k)
Load 2 examples (4k)

Total: 18k tokens (still 88% savings vs upfront 150k)
Difference: Loaded incrementally as needed, not all at once
```

---

## Troubleshooting

### "My savings aren't 90%+"

**Possible causes**:
- Loading docs before checking navigator
- Reading files manually instead of using navigator index
- Loading complete docs when sections would suffice

**Fix**: Start every decision with "What does navigator say?"

### "I had to re-load a document"

**Possible causes**:
- Loaded too early, context filled, had to compact
- Didn't create marker before compact

**Fix**: Load closer to when needed, use markers between tasks

### "I'm not sure when to load"

**Rule of thumb**:
- Starting task → Load navigator + task doc
- Implementing → Load relevant system doc
- Debugging → Load debugging SOP
- Unfamiliar → Use agent search first

**Fix**: When in doubt, check navigator first

---

## Next Steps

### Try More Exercises

- **[TRY-THIS-AGENT-SEARCH.md](./TRY-THIS-AGENT-SEARCH.md)** - Agent-assisted exploration
- **[TRY-THIS-MARKERS.md](./TRY-THIS-MARKERS.md)** - Context compression

### Deep Dive into Theory

- **[PROGRESSIVE-REFINEMENT.md](../PROGRESSIVE-REFINEMENT.md)** - Full pattern explanation
- **[CONTEXT-BUDGETS.md](../CONTEXT-BUDGETS.md)** - Token allocation strategies

### Apply to Your Project

1. Create `.agent/DEVELOPMENT-README.md` (your navigator)
2. Practice lazy loading in real work
3. Measure your session efficiency
4. Share results with team

---

## Success Criteria

You've mastered lazy loading when:

- [ ] You instinctively load navigator first
- [ ] You check navigator before loading any doc
- [ ] You achieve >70% token savings consistently
- [ ] Your sessions last 15+ exchanges without restart
- [ ] You can explain why upfront loading fails

**Congratulations! You now understand one of Navigator's core optimizations.**
