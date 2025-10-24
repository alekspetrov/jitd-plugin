# Try This: Context Markers for 97% Compression

**Part of**: Navigator v4.0 Education Layer
**Time**: 12 minutes
**Difficulty**: Intermediate
**Goal**: Experience context compression and session resumption

---

## What You'll Learn

By the end of this exercise, you'll:
- See 97%+ compression of decisions into markers
- Resume sessions without re-loading documentation
- Understand when to create markers
- Master the compact + marker workflow

---

## Setup

**Prerequisites**:
- Navigator installed in a project
- Completion of [TRY-THIS-LAZY-LOADING.md](./TRY-THIS-LAZY-LOADING.md)
- 20+ minutes for complete exercise (includes break between sessions)

**Starting point**: Fresh Claude Code session

---

## Exercise 1: The Problem (No Markers)

### Step 1: Simulate Traditional Session Break

**Scenario**: You're implementing a feature, need to take a break

**Traditional approach** (what happens without markers):
```
Session 1:
├── Load all relevant docs (15k tokens)
├── Make architectural decisions
├── Implement 50% of feature
└── Take break → Close Claude Code

Session 2 (after break):
├── Re-load all docs (15k tokens again)
├── Read previous code to remember context
├── Try to recall decisions made
├── Continue implementation
└── Total: 30k tokens (loaded same docs twice)
```

**Problem**:
- Loaded same 15k docs twice
- Wasted 15k tokens (50%)
- Lost subtle context (why decisions were made)
- Time wasted reconstructing mental model

---

## Exercise 2: Context Markers Solution

### Step 2: Start Feature Implementation

**In Claude Code**:
```
"Start my Navigator session"
```

**Token cost**: ~3k (navigator)

### Step 3: Begin Work

**In Claude Code**:
```
"I want to add a new skill for handling database migrations.
Load the relevant documentation."
```

**What loads**:
- plugin-patterns.md (5k)
- Existing migration examples (3k)

**Total loaded**: 11k tokens

### Step 4: Make Decisions

**In Claude Code**:
```
"Design the migration skill architecture.
What components do we need?"
```

**Claude response** (example):
```
Migration Skill Architecture:

1. Predefined Functions:
   - migration_generator.py - Creates migration files
   - migration_validator.py - Validates schema changes
   - migration_rollback.py - Generates rollback logic

2. Templates:
   - migration.sql.template - SQL migration format
   - migration.md.template - Documentation format

3. Skill Workflow:
   - User describes schema change
   - Generator creates migration file
   - Validator checks for common issues
   - Rollback generator adds undo logic

Decision: Use timestamp-based migration naming (YYYYMMDDHHMMSS_description.sql)
```

**Context at this point**:
- Navigator: 3k
- Documentation: 8k
- Conversation decisions: 4k
- **Total**: 15k tokens in context

### Step 5: Create Context Marker

**In Claude Code**:
```
"Create a context marker for this migration skill work"
```

**What happens**:
1. Claude extracts key decisions (not raw conversation)
2. Compresses to essential information
3. Saves marker file

**Marker content** (example):
```markdown
# Context Marker: Migration Skill Implementation

**Created**: 2025-10-24
**Task**: Implementing database migration skill

## Decisions Made

**Architecture**:
- 3 predefined functions (generator, validator, rollback)
- 2 templates (SQL, docs)
- Timestamp-based naming: YYYYMMDDHHMMSS_description.sql

**Rationale**:
- Generator ensures consistent format (0 tokens)
- Validator catches common schema mistakes
- Rollback auto-generation for safety

**Implementation Status**:
- Design complete
- Ready to implement functions

**Next Steps**:
1. Create migration_generator.py
2. Create migration_validator.py
3. Create rollback generator
4. Add templates
5. Test with example migration

**Files to reference**:
- .agent/system/plugin-patterns.md (loaded, understood)
- skills/nav-task/ (example predefined functions)
```

**Marker size**: 0.5k tokens (compressed from 15k context)

**Compression**: 97% (0.5k / 15k)

---

## Exercise 3: Session Resumption

### Step 6: Take Break (Close Session)

**Close Claude Code completely**

**Wait 5+ minutes** (simulate break, work on something else)

### Step 7: Resume from Marker

**Open Claude Code in same project**

**In Claude Code**:
```
"Continue my Navigator session from the migration skill marker"
```

**What happens**:
1. Claude finds marker in `.context-markers/`
2. Loads marker (0.5k tokens)
3. Understands decisions made
4. Ready to continue implementation

**Token cost**: 0.5k (marker only)

**NOT loaded**:
- plugin-patterns.md (8k) - was read in previous session
- Conversation history (4k) - compressed into marker

**Savings**: 11.5k tokens (96%)

### Step 8: Continue Work

**In Claude Code**:
```
"Let's implement the migration_generator.py function"
```

**Claude response**:
```
Based on our architecture decisions (from marker):
- Timestamp-based naming
- SQL template format
- Consistent structure

Here's migration_generator.py:
[Implementation code]
```

**Key observation**: Claude knows all decisions without re-loading docs

---

## Exercise 4: Marker + Compact Pattern

### Step 9: Complete Subtask

**After implementing generator function**:

**In Claude Code**:
```
"The generator function is complete. Create a marker."
```

**New marker created**:
```markdown
# Context Marker: Migration Skill - Generator Complete

**Previous marker**: migration-skill-implementation
**Updated**: 2025-10-24

## Completed
- ✅ migration_generator.py implemented
  - Timestamp naming working
  - SQL template integration
  - Schema change parsing

## Current State
- Ready for validator implementation

## Next Steps
1. Implement migration_validator.py
2. Test generator + validator together
```

**Marker size**: 0.4k tokens

### Step 10: Compact Session

**In Claude Code**:
```
"Clear context and preserve this marker"
```

**What happens**:
1. Conversation history cleared (frees 40k tokens)
2. Marker preserved (0.4k tokens)
3. Navigator remains loaded (3k tokens)

**Context usage**:
- Before compact: 65%
- After compact: 18%

**Freed**: 94k tokens

### Step 11: Continue to Next Subtask

**In Claude Code**:
```
"Load the marker and implement the validator function"
```

**Token cost**:
- Marker: 0.4k
- Continue work

**Total context**: 22% (still very efficient)

**Benefit**: Completed 2 subtasks in one extended session instead of restart

---

## Exercise 5: Multi-Session Workflow

### Step 12: Simulate Complete Feature Across Days

**Day 1 (Session 1)**:
```
Load navigator (3k)
Design architecture (15k total context)
Create marker "migration-skill-design" (0.5k compressed)
```

**Day 2 (Session 2)**:
```
Load marker (0.5k)
Implement generator function (12k total context)
Create marker "migration-skill-generator" (0.4k compressed)
Compact
```

**Day 3 (Session 3)**:
```
Load marker (0.4k)
Implement validator function (10k total context)
Create marker "migration-skill-validator" (0.4k compressed)
Compact
```

**Day 4 (Session 4)**:
```
Load marker (0.4k)
Implement rollback generator (11k total context)
Feature complete
Create final marker "migration-skill-complete" (0.6k compressed)
```

**Total token cost across 4 sessions**:
- Markers: 2.3k total
- Per-session work: ~40k
- **Total**: 42.3k tokens

**Without markers** (traditional):
- Session 1: Load docs (15k) + work
- Session 2: Re-load docs (15k) + work
- Session 3: Re-load docs (15k) + work
- Session 4: Re-load docs (15k) + work
- **Total**: 100k+ tokens

**Savings**: 58k tokens (58%)

---

## Exercise 6: Measure Compression

### Step 13: Check Marker Efficiency

**In Claude Code**:
```
"Show me the compression ratio for my context markers"
```

**Expected analysis**:
```
Marker Compression Analysis:

Original Context:
├── Documentation: 11k
├── Conversation: 8k
├── Decisions: 4k
└── Total: 23k tokens

Marker Size: 0.5k tokens

Compression: 97.8% (0.5k / 23k)

What's Preserved:
├── Key decisions ✓
├── Architecture choices ✓
├── Implementation status ✓
├── Next steps ✓
└── File references ✓

What's Discarded:
├── Full documentation content (can re-load if needed)
├── Back-and-forth conversation (decisions extracted)
├── Exploratory dead-ends (only final choices kept)
└── Verbose explanations (compressed to essentials)
```

### Step 14: Compare to Raw Context

**Marker content** (0.5k):
```markdown
Architecture: 3 functions + 2 templates
Naming: YYYYMMDDHHMMSS_description.sql
Next: Implement generator function
```

**Original conversation** (23k):
```
Full plugin-patterns.md documentation
Complete back-and-forth about architecture options
All examples read and discussed
Exploratory questions and answers
Detailed explanations of each decision
```

**Key insight**: Marker preserves what matters (decisions), discards what doesn't (exploration process)

---

## Key Takeaways

### When to Create Markers

✅ **Completing isolated subtask**
- Finished one function, ready for next
- Natural breakpoint in work

✅ **Taking break mid-feature**
- End of day, switching contexts
- Preserve state for later

✅ **Before compact**
- Context usage >60%
- Need to clear history but preserve decisions

✅ **Switching between unrelated tasks**
- Finish Task A, start Task B
- May return to Task A later

### What Markers Preserve

✅ **Architectural decisions**
- "We chose pattern X because Y"

✅ **Implementation status**
- What's done, what's next

✅ **Key rationale**
- Why decisions were made

✅ **File references**
- "See system-doc.md for details" (don't re-load)

### What Markers Discard

❌ **Exploratory conversation**
- "Let's try approach A... no, B is better"
- Keep final choice only

❌ **Complete documentation**
- Don't copy docs into marker
- Reference file names only

❌ **Verbose explanations**
- Compress to essentials

❌ **Dead ends**
- Approaches that didn't work

---

## Common Mistakes

### Mistake 1: Creating Marker Too Early

**Symptom**: Marker every 2 exchanges

**Fix**: Create at natural breakpoints (subtask done, taking break)

**Why**: Overhead of marker creation outweighs benefit

### Mistake 2: Too Verbose Markers

**Symptom**: Marker is 5k tokens

**Fix**: Compress to decisions only, reference docs by name

**Why**: Defeats purpose of compression

### Mistake 3: Never Using Markers

**Symptom**: Re-loading same docs every session

**Fix**: Create marker before break, load marker on resume

**Savings**: 50-97% token reduction

### Mistake 4: Not Compacting with Markers

**Symptom**: Context full, marker exists, but no compact

**Fix**: Compact + marker = reset context while preserving decisions

**Why**: Gets full benefit of compression

---

## Advanced Patterns

### Pattern 1: Marker Chain

**For long-running features**:
```
Day 1: marker-v1 (design decisions)
Day 2: marker-v2 (generator done) [references marker-v1]
Day 3: marker-v3 (validator done) [references marker-v2]
Day 4: marker-v4 (complete) [references marker-v3]

Each marker: 0.4-0.6k tokens
Total chain: 2k tokens
vs Re-loading context: 60k tokens
Savings: 97%
```

### Pattern 2: Active Marker

**Auto-resume pattern**:
```
Create marker → Mark as active
Next session: Auto-loads active marker
Zero manual "load marker" commands needed
```

### Pattern 3: Differential Markers

**Update existing marker**:
```
Original marker: 0.5k
New decision: +0.1k delta
Updated marker: 0.6k total
vs Re-creating from scratch: 0.8k
Savings: 25%
```

---

## Variations to Try

### Variation 1: Multi-Task Session

**Scenario**: Work on 3 unrelated tasks in one extended session

```
Task A: Implement feature (15k context)
├── Create marker-A (0.5k)
└── Compact

Task B: Fix bug (12k context)
├── Create marker-B (0.4k)
└── Compact

Task C: Update docs (8k context)
└── Create marker-C (0.3k)

Total: 36.2k tokens
Without markers: 105k tokens
Savings: 65%
```

### Variation 2: Collaborative Handoff

**Scenario**: Pass work to another developer

```
You: Create detailed marker with context
Them: Load marker, understand state
Result: Onboard in 30 seconds (0.5k tokens)
vs Traditional: Explain everything (20 minutes, 15k tokens)
```

### Variation 3: Experimental Branch

**Scenario**: Try risky approach, may need to revert

```
Main approach: marker-main (0.5k)
Try experiment: 10k context exploration
Experiment fails: Discard, load marker-main
Resume from checkpoint: 0 wasted tokens
```

---

## Exercise 7: Full Workflow Practice

### Step 15: Complete Feature with Markers

**Full workflow**:
```
1. "Start Navigator session"
   └── Load navigator (3k)

2. "Design migration skill"
   └── Load docs (8k), make decisions

3. "Create marker: migration-skill-design"
   └── Compress to 0.5k

4. "Implement generator function"
   └── Work (context: 35%)

5. "Create marker: generator-complete"
   └── Update marker (0.6k)

6. "Clear context and preserve marker"
   └── Compact (context: 15%)

7. "Load marker and implement validator"
   └── Resume (0.6k)

8. "Complete and create final marker"
   └── Feature done, marker preserved

Total markers: 1.7k
Total session tokens: 35k
Traditional approach: 90k+
Savings: 61%
```

---

## Next Steps

### Try More Exercises

- **[TRY-THIS-LAZY-LOADING.md](./TRY-THIS-LAZY-LOADING.md)** - Lazy loading basics
- **[TRY-THIS-AGENT-SEARCH.md](./TRY-THIS-AGENT-SEARCH.md)** - Agent-assisted exploration

### Deep Dive into Theory

- **[PROGRESSIVE-REFINEMENT.md](../PROGRESSIVE-REFINEMENT.md)** - Metadata → details pattern
- **[TOKEN-OPTIMIZATION.md](../TOKEN-OPTIMIZATION.md)** - Complete strategies

### Apply to Your Work

1. Next feature: Create marker at each subtask
2. Measure compression ratios
3. Practice compact + marker workflow
4. Share patterns with team

---

## Success Criteria

You've mastered context markers when:

- [ ] You create markers at natural breakpoints automatically
- [ ] You achieve >95% compression consistently
- [ ] You resume sessions without re-loading docs
- [ ] You compact proactively using markers
- [ ] Your sessions extend 2-3x longer with marker workflow

**Congratulations! You now understand context compression and session management.**
