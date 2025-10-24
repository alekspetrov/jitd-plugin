# Decision Framework: When to Compact

**Part of**: Navigator v4.0 Education Layer
**Type**: Decision Framework
**Use**: Quick reference for compact timing decisions

---

## Flowchart

```
┌─────────────────────────────────────────┐
│ Is your context usage > 60%?           │
└──────────────────┬──────────────────────┘
                   │
         ┌─────────┴──────────┐
         │                    │
        YES                  NO
         │                    │
         ▼                    │
┌─────────────────┐           │
│ Is current task │           │
│ complete?       │           │
└────────┬────────┘           │
         │                    │
   ┌─────┴──────┐             │
   │            │             │
  YES          NO             │
   │            │             │
   ▼            ▼             ▼
┌──────┐  ┌──────────┐  ┌─────────┐
│ COM- │  │ Are you  │  │ CONTIN- │
│ PACT │  │ at sub-  │  │ UE      │
│ NOW  │  │ task     │  │ WORKING │
│      │  │ break?   │  │         │
└──────┘  └─────┬────┘  └─────────┘
                │
          ┌─────┴──────┐
          │            │
         YES          NO
          │            │
          ▼            ▼
    ┌──────────┐  ┌─────────┐
    │ CREATE   │  │ WAIT    │
    │ MARKER + │  │ FOR     │
    │ COMPACT  │  │ BREAK   │
    └──────────┘  └─────────┘
```

---

## Decision Table

| Context Usage | Task Status | Subtask Status | Decision | Action |
|--------------|-------------|----------------|----------|---------|
| <40% | Any | Any | ✅ Continue | Keep working |
| 40-60% | In progress | Middle of subtask | ⚠️ Monitor | Plan compact soon |
| 40-60% | In progress | At breakpoint | ✅ Optional | Marker + compact if switching |
| 40-60% | Complete | Done | ✅ Compact | Clean up before next |
| 60-80% | In progress | Middle of subtask | ⚠️ Warning | Finish subtask, then compact |
| 60-80% | In progress | At breakpoint | ✅ Recommended | Marker + compact |
| 60-80% | Complete | Done | ✅ Required | Compact now |
| >80% | Any | Any | 🚨 Critical | Marker + compact immediately |

---

## Quick Reference Rules

### ✅ DO Compact When:

**1. Task Complete + High Usage**
```
Context: 65%
Status: Feature implemented, tested, committed
Action: Compact (clear for next task)
```

**2. Context Critical**
```
Context: 82%
Status: Any (urgent)
Action: Create marker + compact immediately
```

**3. Switching Contexts**
```
Context: 55%
Status: Pausing Task A to start Task B
Action: Marker for A + compact + start B fresh
```

**4. Natural Breakpoint**
```
Context: 48%
Status: Completed subtask, ready for next
Action: Marker + compact (optional but beneficial)
```

**5. End of Day**
```
Context: 50%+
Status: Stopping work for the day
Action: Marker + compact (resume fresh tomorrow)
```

---

### ❌ DON'T Compact When:

**1. Mid-Task**
```
Context: 55%
Status: Halfway through implementing function
Action: WAIT - finish current unit of work first
```

**2. Debugging Active Issue**
```
Context: 62%
Status: Tracing bug, have partial context loaded
Action: WAIT - finish debug session first
```

**3. Context Still Low**
```
Context: 35%
Status: Any
Action: NO NEED - plenty of space remaining
```

**4. About to Need Same Context**
```
Context: 58%
Status: Finishing subtask, next subtask needs same docs
Action: WAIT - compact after both subtasks done
```

**5. No Marker Created**
```
Context: 70%
Status: Important decisions not yet captured
Action: CREATE MARKER FIRST, then compact
```

---

## Context Usage Thresholds

### Green Zone (<40%)
```
Status: ✅ Excellent
Action: Continue working
Capacity: ~120k tokens available
Sessions: 15-20+ exchanges possible
```

### Yellow Zone (40-60%)
```
Status: ⚠️ Monitor
Action: Plan compact at next breakpoint
Capacity: ~80k tokens available
Sessions: 8-12 exchanges possible
```

### Orange Zone (60-80%)
```
Status: ⚠️ Warning
Action: Compact at next subtask completion
Capacity: ~40k tokens available
Sessions: 4-6 exchanges possible
```

### Red Zone (>80%)
```
Status: 🚨 Critical
Action: Marker + compact immediately
Capacity: <40k tokens available
Sessions: 1-3 exchanges before crash
```

---

## Subtask Breakpoint Recognition

### Good Breakpoints (Safe to Compact)

✅ **Function complete**
- Implementation done
- Tests passing
- Ready for next function

✅ **Bug fixed**
- Issue resolved
- Verified working
- Moving to next issue

✅ **Design decided**
- Architecture finalized
- Ready to implement
- Clear next steps

✅ **Component finished**
- Feature complete
- Integrated and tested
- Next component independent

✅ **Documentation updated**
- Docs written
- Ready for code work
- Clear separation

### Bad Breakpoints (Don't Compact)

❌ **Mid-function**
- Partially implemented
- Logic incomplete
- Would lose flow

❌ **Debugging in progress**
- Issue not resolved
- Hypothesis being tested
- Context critical

❌ **Design exploration**
- Evaluating options
- Not yet decided
- Discussion ongoing

❌ **Integration in progress**
- Connecting components
- Testing interactions
- Dependencies active

❌ **Refactoring underway**
- Changes across files
- Pattern not complete
- State transitional

---

## Common Scenarios

### Scenario 1: Feature Implementation

```
Phase 1: Design (context: 35%)
├── Research patterns
├── Make architectural decisions
└── Breakpoint: ✅ Good time to marker + compact

Phase 2: Implementation (context: 28% after compact)
├── Write function 1 (context: 38%)
├── Write function 2 (context: 48%)
└── Breakpoint: ✅ Good time to marker + compact

Phase 3: Testing (context: 25% after compact)
├── Write tests (context: 42%)
├── Fix bugs (context: 58%)
└── Breakpoint: ✅ Good time to marker + compact

Phase 4: Documentation (context: 22% after compact)
├── Update docs (context: 32%)
└── Complete: ✅ Compact before next task
```

### Scenario 2: Multi-Bug Fix Session

```
Bug 1: Fix auth issue
├── Debug (context: 42%)
├── Fix (context: 48%)
├── Test (context: 52%)
└── Marker + compact (context → 20%)

Bug 2: Fix validation error
├── Debug (context: 32%)
├── Fix (context: 38%)
├── Test (context: 44%)
└── Marker + compact (context → 18%)

Bug 3: Fix UI glitch
├── Debug (context: 28%)
├── Fix (context: 34%)
└── Complete: ✅ Compact

Result: 3 bugs fixed in one extended session
Without compact: Would crash after bug 1.5
```

### Scenario 3: Research Session

```
Research Phase:
├── Use agent to explore (context: 28%)
├── Load relevant docs (context: 42%)
├── Understand patterns (context: 55%)
└── DON'T COMPACT YET - need context for next phase

Implementation Phase:
├── Apply learnings (context: 63%)
├── Implement solution (context: 72%)
└── NOW COMPACT - research done, implementation complete

Next Task:
└── Start fresh (context: 18%)
```

---

## Integration with Markers

### Always Pair Compact with Markers

**Wrong**:
```
Context at 70%
└── Compact immediately
    └── Lost all decisions and context
    └── Can't resume effectively
```

**Right**:
```
Context at 70%
├── Create marker (compress decisions)
├── Compact (clear history)
└── Resume from marker anytime
    └── Decisions preserved, context efficient
```

### Marker Creation Triggers

Create marker **before** compact in these situations:

1. **Incomplete work**
   - Will continue later
   - Decisions need preservation

2. **Complex context**
   - Multiple architectural decisions made
   - Would be hard to reconstruct

3. **Multi-session feature**
   - Won't finish in one session
   - Need checkpoint for resume

4. **Switching tasks**
   - May return to current task
   - Preserve state for later

---

## Cost-Benefit Analysis

### When Compact Benefits Outweigh Costs

**Benefits**:
- Free up 40-80k tokens
- Extend session 2-3x
- Prevent context crash
- Start next task fresh

**Costs**:
- 1 exchange to create marker (~1k tokens)
- 1 exchange to compact (0 tokens)
- 1 exchange to resume from marker (~0.5k)

**Total cost**: ~1.5k tokens

**Break-even**: If continuing work would use >1.5k tokens in freed space

**Analysis**:
```
Context at 65% (70k used, 130k total)
Remaining: 65k tokens

If you need >1.5k tokens more work:
└── Compact saves tokens overall

Typical next task: 10-30k tokens
└── Compact is worth it
```

---

## Anti-Patterns

### Anti-Pattern 1: Compact Too Early

```
Context: 35%
Action: Compact
Result: Wasted 1.5k tokens on unnecessary compact
Fix: Wait until >60% or task complete
```

### Anti-Pattern 2: Compact Too Late

```
Context: 88%
Action: Keep working
Result: Session crashes mid-task
Fix: Compact at 60-70% proactively
```

### Anti-Pattern 3: Compact Without Marker

```
Context: 70%
Important decisions made
Action: Compact without marker
Result: Lost context, can't resume
Fix: Always marker first
```

### Anti-Pattern 4: Never Compact

```
Session 1: Context fills to 90%, restart
Session 2: Context fills to 90%, restart
Session 3: Context fills to 90%, restart
Fix: Compact between tasks proactively
```

---

## Quick Decision Checklist

Before compacting, verify:

- [ ] **Context >60%** OR **task complete**?
- [ ] **At natural breakpoint** (not mid-subtask)?
- [ ] **Marker created** if work incomplete?
- [ ] **Next task is different** (new context needed)?
- [ ] **Ready to clear conversation** history?

If all yes → ✅ Compact now
If any no → ⚠️ Wait or create marker first

---

## Next Steps

### Learn More
- **[PROGRESSIVE-REFINEMENT.md](../PROGRESSIVE-REFINEMENT.md)** - Load less, compact less often
- **[TOKEN-OPTIMIZATION.md](../TOKEN-OPTIMIZATION.md)** - Complete strategies
- **[TRY-THIS-MARKERS.md](../examples/TRY-THIS-MARKERS.md)** - Practice compact workflow

### Related Frameworks
- **[AGENT-VS-MANUAL.md](./AGENT-VS-MANUAL.md)** - When to use agents
- **[PREPROCESSING-DECISION-TREE.md](./PREPROCESSING-DECISION-TREE.md)** - Right tool choices

---

**Bottom line**: Compact when context >60% AND at a natural breakpoint. Always create marker first if work is incomplete. This prevents crashes while preserving ability to resume efficiently.
