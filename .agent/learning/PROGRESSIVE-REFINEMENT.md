# Progressive Refinement: Metadata → Details On-Demand

**Part of**: Navigator v4.0 Education Layer
**Level**: Intermediate
**Read Time**: 9 minutes
**Prerequisites**: [CONTEXT-BUDGETS.md](./CONTEXT-BUDGETS.md), [PREPROCESSING-VS-LLM.md](./PREPROCESSING-VS-LLM.md)

---

## The Pattern

Instead of loading complete documentation upfront, fetch in stages:

```
Stage 1: Index (2k tokens)
  └── What exists

Stage 2: Metadata (0 additional tokens)
  └── Summaries, headers, file names

Stage 3: Specific Content (3-5k tokens)
  └── Only what's relevant

Stage 4: Deep Dive (2k tokens)
  └── Related details if needed
```

**Total**: 7-9k tokens instead of 150k

**Savings**: 94%

---

## Why It Works

### The Problem with Upfront Loading

**Traditional approach**:
```
Load everything → Find what you need → Use 5%
```

**Result**:
- 95% of loaded content is never used
- Context window fills immediately
- Session crashes after 5-7 exchanges

### Progressive Refinement Approach

**Navigator approach**:
```
Load index → Navigate to relevant section → Load only that section → Use 100%
```

**Result**:
- 100% of loaded content is used
- Context window stays efficient
- Sessions last 20+ exchanges

**The insight**: Most decisions don't need full content—metadata is enough.

---

## The Core Pattern: Three-Stage Refinement

### Stage 1: The Navigator (Index)

**What it is**: Lightweight index of what documentation exists

**Example**: `.agent/DEVELOPMENT-README.md`
```markdown
## Documentation Index

### System Architecture
- [Project Architecture](./system/project-architecture.md) - Plugin structure, templates
- [Plugin Patterns](./system/plugin-patterns.md) - Claude Code plugin best practices

### Implementation Plans
- [TASK-01: Session Start](./tasks/TASK-01-session-start-pm-integration.md) - ✅ Completed
- [TASK-18: Principle to Product](./tasks/TASK-18-principle-to-product-v3.5.md) - 📋 Planning

### Standard Operating Procedures
- [Version Management](./sops/development/version-management.md) - Pre-release checklist
- [Plugin Release](./sops/development/plugin-release-workflow.md) - Step-by-step process
```

**Token cost**: ~2k

**What you learn**:
- What documentation exists
- Where to find it
- High-level status
- When to read each doc

**Decision enabled**: "Do I need system architecture or an SOP?"

### Stage 2: Metadata (Implicit)

**What it is**: File names, section headers, summaries from the navigator

**Example**: From navigator entry
```
[Project Architecture](./system/project-architecture.md) - Plugin structure, templates
```

**Token cost**: 0 additional (already in navigator)

**What you learn**:
- Topic coverage
- Relevance to current task
- Estimated detail level

**Decision enabled**: "Is this the right doc to load?"

### Stage 3: Specific Content

**What it is**: Load ONE relevant document, not all of them

**Example**: Load `project-architecture.md` after deciding it's relevant

**Token cost**: 3-5k per document

**What you learn**:
- Implementation details
- Architecture decisions
- Code patterns
- Specific procedures

**Decision enabled**: "How do I implement this?"

### Stage 4: Deep Dive (Optional)

**What it is**: Load related documents if needed

**Example**: Project architecture mentions testing → Load testing SOP

**Token cost**: 2k per additional document

**What you learn**:
- Edge cases
- Integration details
- Examples and troubleshooting

**Decision enabled**: "How do I handle this specific case?"

---

## Real-World Examples

### Example 1: Adding New Feature

**❌ Upfront Loading Approach**:
```
Session start:
├── Load all system docs (30k)
├── Load all SOPs (15k)
├── Load all task docs (20k)
├── Load all examples (10k)
└── Total: 75k tokens

Find relevant section: "Oh, I only needed plugin-patterns.md"
Used: 4k tokens
Wasted: 71k tokens (95% waste)
```

**✅ Progressive Refinement**:
```
Session start:
└── Load navigator (2k)

Exchange 1: "I need to add a new command"
├── Navigate index → "Plugin Patterns looks relevant"
└── Decision: Load plugin-patterns.md

Exchange 2:
└── Load plugin-patterns.md (4k)

Exchange 5: "How do I test this?"
├── Plugin patterns mentions testing SOP
└── Load testing SOP (2k)

Total loaded: 8k tokens
Waste: 0 tokens (100% used)
Savings: 67k tokens (89%)
```

### Example 2: Debugging Production Issue

**❌ Upfront Loading**:
```
Load all debugging docs (20k)
Load all system architecture (30k)
Load all integration SOPs (15k)
Total: 65k tokens

Actually needed: One debugging SOP (2k)
Waste: 63k tokens (97%)
```

**✅ Progressive Refinement**:
```
Load navigator (2k)
→ Check debugging SOPs section
→ Load specific SOP for issue type (2k)
→ Issue resolved

Total: 4k tokens
Savings: 61k tokens (94%)
```

### Example 3: Understanding Unfamiliar Codebase

**❌ Traditional Exploration**:
```
Read 20 files manually to understand structure:
├── src/index.ts (3k)
├── src/components/Button.tsx (2k)
├── src/components/Modal.tsx (4k)
├── ... (15 more files)
└── Total: 60k tokens

Result: Overwhelmed, context full, unclear architecture
```

**✅ Progressive Refinement with Agent**:
```
Load navigator (2k)
→ Use agent: "Explain the codebase structure"

Agent explores 20 files, returns summary:
├── Architecture: "React app with feature-based structure"
├── Key files: index.ts (entry), App.tsx (root), routes.ts (routing)
├── Patterns: "Uses custom hooks pattern, Context for state"
└── Summary: 4k tokens

Now load 2-3 specific files based on need (6k)

Total: 12k tokens
Savings: 48k tokens (80%)
Result: Clear understanding, context efficient
```

---

## The Navigator Index: Design Principles

### What Makes a Good Navigator

**1. Hierarchical Organization**
```markdown
## System Architecture (`system/`)
### Core Patterns
- File 1 - Brief description
- File 2 - Brief description

### Advanced Topics
- File 3 - Brief description
```

**Why it works**: Categories help decide which section to explore

**2. Brief Descriptions**
```markdown
- [Project Architecture](./system/project-architecture.md) - Plugin structure, templates
```

**Not**:
```markdown
- [Project Architecture](./system/project-architecture.md) - This document describes the complete architecture of the Navigator plugin including the file structure, template organization, slash command implementations, configuration schema, development workflow, testing strategies, and deployment procedures.
```

**Why it works**:
- First version: 10 tokens, enough to decide relevance
- Second version: 40 tokens, overwhelming, defeats purpose

**3. Status Indicators**
```markdown
- [TASK-01: Session Start](./tasks/TASK-01.md) - ✅ Completed
- [TASK-18: Principle to Product](./tasks/TASK-18.md) - 📋 Planning
```

**Why it works**: Immediately know if it's active work or reference

**4. "When to Read" Guidance**
```markdown
### System Architecture
**When to read**: Starting work on plugin, understanding structure
```

**Why it works**: Guides decision without reading the doc

### Token Budget for Navigator

**Target**: 2-3k tokens total

**Breakdown**:
- Project overview: 300 tokens
- Documentation index: 800 tokens
- Current work status: 400 tokens
- Guidelines and "when to read": 500 tokens
- Quick reference: 200 tokens

**Total**: ~2,200 tokens

**Coverage**: 100% of available documentation (indexed)

---

## Advanced Patterns

### Pattern 1: Agent-Assisted Refinement

**Use case**: Need to understand something but unsure which docs to load

**Approach**:
```
1. Load navigator (2k)
2. Use agent: "Find files related to authentication"
3. Agent searches, returns summary (3k)
4. Load 1-2 specific files if needed (4k)

Total: 9k tokens
vs Reading all auth-related files manually: 40k+ tokens
Savings: 77%
```

**When to use**:
- Unfamiliar codebase
- Broad exploratory questions
- Unclear what documentation exists

### Pattern 2: Contextual Breadcrumbs

**Use case**: Documents reference each other

**Approach**:
```markdown
# Plugin Release Workflow

**Prerequisites**: Read [Version Management](./version-management.md) first

**Related**:
- [Testing SOP](./testing-workflow.md) - If adding features
- [Migration Guide](./migration-guide.md) - If breaking changes
```

**Benefit**:
- Don't load related docs upfront
- Load only if prerequisites missing
- Follow breadcrumbs as needed

**Token savings**: 60-70% (load 2 docs instead of 5)

### Pattern 3: Lazy Deep Dive

**Use case**: High-level understanding first, details later

**Approach**:
```
Exchange 1:
└── "How does authentication work?"
    └── Load architecture doc (4k)
    └── Get overview

Exchange 5:
└── "How do I implement JWT refresh?"
    └── Load JWT SOP (2k)
    └── Get implementation details

Total: 6k tokens, loaded on-demand
```

**vs**:
```
Load auth architecture + all auth SOPs upfront = 15k tokens
```

**Savings**: 60%

### Pattern 4: Incremental Loading for Long Docs

**Use case**: Document is 10k+ tokens, only need part of it

**Approach**:
```
1. Check navigator for section summaries
2. Ask: "What's in the Testing section of plugin-patterns.md?"
3. Load only Testing section (2k) instead of entire doc (10k)

Savings: 80%
```

**Implementation**:
- Read tool supports offset + limit
- Request specific sections
- Avoid loading 5k token doc when you need 500 tokens

---

## Common Mistakes

### Mistake 1: Loading "Just in Case"

**Thinking**: "I might need system architecture later, let me load it now"

**Result**:
- 5k tokens loaded
- Never referenced
- Context window fuller

**Fix**: Load navigator, fetch when actually needed

### Mistake 2: No Navigator (Blind Searching)

**Thinking**: "Let me search for 'authentication' and read what I find"

**Result**:
- Read 10 files blindly (30k tokens)
- 8 files irrelevant
- Missed the actual auth doc

**Fix**: Load navigator first, understand structure, then target specific doc

### Mistake 3: Loading Too Much Detail

**Thinking**: "Let me read the entire 8k token architecture doc"

**Result**:
- 8k tokens loaded
- Only needed section 3 (1k tokens)
- 7k wasted

**Fix**: Check table of contents, read specific section

### Mistake 4: Re-Loading Same Content

**Thinking**: "What was that SOP about again? Let me re-read it"

**Result**:
- Load same 3k doc twice
- 6k tokens total for same info

**Fix**: Use markers to preserve decisions, avoid re-reading

---

## Measuring Refinement Efficiency

### Metrics to Track

**1. Load Ratio**
```
Load Ratio = Tokens Loaded / Baseline (All Docs)

Example:
Loaded: 12k
Baseline: 150k
Load Ratio: 8% (excellent)

Target: <15%
```

**2. Usage Ratio**
```
Usage Ratio = Content Actually Referenced / Content Loaded

Example:
Loaded: 12k
Referenced in conversation: 11k
Usage Ratio: 92% (excellent)

Target: >80%
```

**3. Refinement Stages**
```
Stages Used = Number of separate loads

Example:
1. Navigator (2k)
2. System doc (4k)
3. SOP (2k)
Stages: 3 (good - incremental)

Target: 2-4 stages (not 1 upfront load, not 10 tiny loads)
```

### Using Navigator's Session Stats

```bash
"Show me my session statistics"
```

**Look for**:
```
Documentation loaded:    12k tokens
Baseline (all docs):     150k tokens
Tokens saved:            138k (92%)

Context usage:           35% (excellent)
Efficiency score:        94/100
```

**If efficiency is low**:
- Are you loading upfront instead of on-demand?
- Are you reading files manually instead of using navigator?
- Are you loading complete docs when sections would suffice?

---

## Implementing Progressive Refinement

### For Documentation Authors

**1. Create a Strong Navigator**
```markdown
# Project Navigator

## Quick Start
[3-line overview]

## Documentation Index
[Hierarchical list with brief descriptions]

## When to Read What
[Decision tree for common scenarios]
```

**2. Use Descriptive Headers**
```markdown
## Authentication System (`system/auth/`)

### [Auth Architecture](./auth/architecture.md)
**When to read**: Designing new auth features
**Contains**: OAuth flow, JWT handling, session management
**Token cost**: ~4k
```

**3. Include Breadcrumbs**
```markdown
**See also**:
- [Related Topic 1](./link1.md) - Brief context
- [Related Topic 2](./link2.md) - Brief context
```

**4. Organize by Use Case**
```markdown
## For New Contributors
- Start here: [Project Overview](./overview.md)
- Then read: [Development Setup](./setup.md)

## For Adding Features
- Start here: [Architecture](./architecture.md)
- Then read: [Patterns](./patterns.md)
```

### For Navigator Users

**1. Always Start with Navigator**
```
"Start my Navigator session"
→ Loads navigator (~2k)
→ Understand what exists
→ Decide what to load
```

**2. Use Navigator for Decisions**
```
Don't: "Let me load all SOPs to see if one helps"
Do: "Check navigator → debugging section → load specific SOP"
```

**3. Load On-Demand**
```
Exchange 1: Work with navigator only
Exchange 3: "Need system doc" → Load it then
Exchange 7: "Need related SOP" → Load it then
```

**4. Review Efficiency**
```
End of session: Check stats
Did I load docs I didn't use? (Adjust next time)
Did I struggle without docs? (Add to navigator)
```

---

## Integration with Other Patterns

### Progressive Refinement + Lazy Loading

**Synergy**: Both delay loading until needed

**Combined approach**:
```
1. Navigator (index) - Lazy load
2. Decide relevance (metadata) - Progressive refinement
3. Load specific doc (content) - Lazy load
4. Deep dive if needed (details) - Progressive refinement
```

**Result**: Maximum efficiency (load minimum, use maximum)

### Progressive Refinement + Agents

**Synergy**: Agents read many files, return summary

**Combined approach**:
```
1. Navigator (what exists)
2. Agent search (which files relevant)
3. Agent summary (what they contain)
4. Load 1-2 specific files (details)
```

**Result**: Explore 50 files with 10k tokens instead of 150k

### Progressive Refinement + Markers

**Synergy**: Markers preserve decisions, avoid re-reading

**Combined approach**:
```
Session 1:
├── Load navigator (2k)
├── Load system doc (4k)
├── Make architectural decision
└── Create marker (0.5k compressed)

Session 2:
├── Load marker (0.5k)
└── Continue without re-loading docs

Savings: 5.5k tokens not re-loaded
```

---

## Case Study: Navigator Plugin Development

**Scenario**: Adding new skill to Navigator plugin

### Without Progressive Refinement

```
Session start:
├── Load DEVELOPMENT-README.md (8k)
├── Load project-architecture.md (6k)
├── Load plugin-patterns.md (5k)
├── Load all 5 existing skills for reference (15k)
├── Load skill creation SOP (3k)
└── Total: 37k tokens

Exchange 4: Start work
Context: 65% used already

Exchange 7: Context full, compact required
Lost flow, restart
```

### With Progressive Refinement

```
Session start:
└── Load DEVELOPMENT-README.md (8k) [This IS the navigator]

Exchange 1: "I want to add a new skill"
├── Check navigator → skills section
├── Decision: Need plugin-patterns.md
└── Load plugin-patterns.md (5k)

Exchange 3: "What structure should I follow?"
├── Patterns doc references existing skills
├── Decision: Read one example skill
└── Load nav-stats skill (3k)

Exchange 7: Implement skill
├── Have enough context
└── No additional loading needed

Total loaded: 16k tokens
Context: 38% used
Session: Continues smoothly for 15+ exchanges
Savings: 21k tokens (57%)
```

---

## Next Steps

### Learn More
- **[TOKEN-OPTIMIZATION.md](./TOKEN-OPTIMIZATION.md)** - Complete optimization strategies
- **[CONTEXT-BUDGETS.md](./CONTEXT-BUDGETS.md)** - Token allocation thinking
- **[PREPROCESSING-VS-LLM.md](./PREPROCESSING-VS-LLM.md)** - Right tool for the job

### Try It Yourself
- **[TRY-THIS-LAZY-LOADING.md](./examples/TRY-THIS-LAZY-LOADING.md)** - Hands-on progressive refinement
- **[TRY-THIS-AGENT-SEARCH.md](./examples/TRY-THIS-AGENT-SEARCH.md)** - Agent + refinement combo

### References
- **[PATTERNS.md](../philosophy/PATTERNS.md)** - Lazy Loading pattern detailed
- **[ANTI-PATTERNS.md](../philosophy/ANTI-PATTERNS.md)** - Upfront Loading anti-pattern

---

**Bottom line**: Loading everything "just in case" wastes 90%+ of tokens. Progressive refinement loads 10% upfront, fetches the rest on-demand, and uses 100% of what's loaded.

**Navigator's role**: Provides the index (navigator), search capability (agents), and compression (markers) to make progressive refinement automatic.
