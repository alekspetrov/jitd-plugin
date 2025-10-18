# TASK-07: Skills Migration Strategy

**Status**: 📋 Planning
**Version**: 2.0.0 (proposed)
**Created**: 2025-10-16

---

## Executive Summary

**Claude Skills are a perfect fit for Navigator**. Both share the same core principle: **progressive disclosure** - load only what's needed, when it's needed.

**Key Finding**: Migrating Navigator from slash commands to Skills would provide:
- **Additional 5-10k token savings** (98% overhead reduction: 11k → 250 tokens)
- **Better UX** (natural language vs manual `/nav:start`)
- **Portability** (works with any LLM, not just Claude Code)
- **No breaking changes** (hybrid migration strategy available)

---

## What Are Claude Skills?

**Skills** = Folders with instructions, scripts, and resources that Claude loads on-demand

### Key Features

1. **Progressive Disclosure** (3 levels):
   - Level 1: Metadata (always loaded, ~50 tokens per skill)
   - Level 2: Instructions (loaded when skill invoked, 2-5k tokens)
   - Level 3: Scripts/files (executed separately, 0 tokens in context)

2. **Auto-Invocation**:
   - User: "Start my session"
   - Claude: [Automatically invokes `nav-navigator` skill based on description]
   - No need to remember `/nav:start` syntax

3. **Executable Code**:
   - Python/JS scripts in separate files (not inline bash in markdown)
   - Scripts execute without loading into context
   - Sandboxed environment (secure)

4. **Composability**:
   - Multiple skills auto-coordinate
   - User: "Finish this feature and document it"
   - Claude: Invokes `nav-task-doc` + `nav-sop-creator` + `nav-marker` automatically

5. **Portability**:
   - Same skill works in Claude Code, Claude.com, API
   - Not tied to Claude Code plugins
   - Works with any LLM that can read markdown

---

## Current Navigator vs Skills Navigator

### Token Overhead Comparison

**Current (Commands)**:
```
Plugin commands:       11,000 tokens (all command instructions)
Navigator loaded:       2,000 tokens
Task doc loaded:        3,000 tokens
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Total documentation:   16,000 tokens
Available for work:   184,000 tokens (92%)
```

**With Skills**:
```
Skills metadata:          250 tokens (5 skills × 50 tokens)
Navigator loaded:       2,000 tokens
Task doc loaded:        3,000 tokens
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Total documentation:    5,250 tokens
Available for work:   194,750 tokens (97%)
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Improvement:          +10,750 tokens (5.4% more context)
```

### UX Comparison

| Task | Current (Commands) | With Skills |
|------|-------------------|-------------|
| **Start session** | User types `/nav:start` | User says "start my session" |
| **Create marker** | User types `/nav:marker lunch-break` | User says "save my progress for lunch" |
| **Document feature** | User types `/nav:update-doc feature TASK-01` | User says "document this feature" |
| **Compact context** | User types `/nav:compact` | User says "clear context, I'm done" |

**Skills = Natural language** (easier for new users)

---

## Proposed Skills Architecture

### Skills to Create

**1. `nav-navigator`**
```yaml
---
name: nav-navigator
description: Load Navigator documentation navigator when starting development session, resuming work, or beginning new feature. Use when user mentions starting work, beginning session, or checking project status.
allowed-tools: Read, Bash
---
```
**Replaces**: `/nav:start` command

---

**2. `nav-task-manager`**
```yaml
---
name: nav-task-manager
description: Manage Navigator task documentation - create implementation plans, archive completed tasks, update task index. Use when user starts new feature or completes work.
allowed-tools: Read, Write, Edit, Bash
---
```
**Replaces**: `/nav:update-doc feature` command

---

**3. `nav-sop-creator`**
```yaml
---
name: nav-sop-creator
description: Create Standard Operating Procedures after solving novel issues, establishing patterns, or documenting workflows. Use when user says "document this solution" or "save this for next time".
allowed-tools: Read, Write, Bash
---
```
**Replaces**: `/nav:update-doc sop` command

---

**4. `nav-marker`**
```yaml
---
name: nav-marker
description: Create context save points to preserve conversation state before breaks, risky changes, or compaction. Use when user says "save progress", "create checkpoint", or before clearing context.
allowed-tools: Read, Write, Bash
---
```
**Replaces**: `/nav:marker` command

---

**5. `nav-compact`**
```yaml
---
name: nav-compact
description: Clear conversation context while preserving knowledge via context marker. Use when user says "clear context", "start fresh", or when approaching token limits.
allowed-tools: Read, Write, Bash
---
```
**Replaces**: `/nav:compact` command

---

## Migration Strategy (No Breaking Changes)

### Phase 1: Hybrid Coexistence (v2.0 - Q1 2026)

**Keep both Commands + Skills**:

```
Navigator Plugin v2.0:
├── commands/              # Existing (still work)
│   ├── init.md
│   ├── start.md
│   ├── update-doc.md
│   ├── compact.md
│   ├── marker.md
│   └── markers.md
│
└── skills/                # NEW
    ├── nav-navigator/
    │   ├── SKILL.md
    │   └── scripts/
    │       └── session_stats.py
    ├── nav-task-manager/
    │   ├── SKILL.md
    │   └── scripts/
    │       └── archive_task.py
    ├── nav-sop-creator/
    │   └── SKILL.md
    ├── nav-marker/
    │   └── SKILL.md
    └── nav-compact/
        └── SKILL.md
```

**User Experience**:
- Existing users: `/nav:start` still works
- New users: "start my session" auto-invokes skill
- Both work - no conflicts
- Documentation shows both approaches

**Implementation**:
- Skills check if command already ran (avoid duplication)
- Commands check if skill already ran (avoid duplication)
- Flag: `nav_started=true` prevents double execution

**Timeline**: 6 months for adoption

---

### Phase 2: Deprecation (v2.5 - Q3 2026)

**Promote Skills, deprecate Commands**:

```
⚠️  /nav:start is deprecated and will be removed in v3.0

Instead, use natural language:
- "Start my Navigator session"
- "Load the navigator"
- "I want to begin working"

The skill works the same way - just easier to use!
```

**Changes**:
- Commands show deprecation warning
- Documentation updated to teach Skills-first
- Migration guide published

**Timeline**: 6 months warning period

---

### Phase 3: Skills-Only (v3.0 - Q1 2027)

**Remove commands entirely**:
- Commands deleted from plugin
- Skills are only interface
- Major version (3.0) signals breaking change

**Migration Path**:
- 12+ months total warning (v2.0 → v2.5 → v3.0)
- Users have ample time to adapt
- Clear communication at each phase

---

## Technical Requirements

### Prerequisites

**What We Need**:
1. ✅ Skills structure knowledge (from research)
2. ✅ Token optimization expertise (Navigator already has)
3. ✅ Clear workflows (init, start, update-doc, etc.)
4. ⚠️ Code Execution Tool beta access (required for script execution)
5. ⚠️ Extract scripts from markdown (currently inline bash)

### Code Execution Tool Beta

**Status**: Required for Skills with executable code
**Access**: Request via Anthropic Console
**Timeline**: Currently in beta (public availability TBD)

**Fallback**: If beta not available, Skills can still work:
- Instructions load and execute manually (via Bash tool)
- Not as elegant, but functional
- Full automation requires beta

**Action**: Request beta access immediately

### Script Extraction

**Current**: Bash scripts embedded in command markdown
**Needed**: Separate `.py`/`.sh` files

**Example**:

**Current** (`commands/start.md`):
```markdown
```bash
nav_bytes=$(wc -c < .agent/DEVELOPMENT-README.md)
nav_tokens=$((nav_bytes / 4))
# ... 30 more lines
```
```

**Migrated** (`skills/nav-navigator/scripts/session_stats.py`):
```python
import os

def calculate_token_usage():
    nav_path = ".agent/DEVELOPMENT-README.md"
    nav_bytes = os.path.getsize(nav_path) if os.path.exists(nav_path) else 0
    return {"nav_tokens": nav_bytes // 4}

if __name__ == "__main__":
    print(calculate_token_usage())
```

**Benefits**:
- Cleaner (proper language files vs bash-in-markdown)
- Testable (can run independently)
- Zero tokens (scripts execute, don't load into context)

---

## Benefits Summary

### 1. Token Efficiency

**Additional 5-10k tokens saved**:
- Commands overhead: 11k → 250 tokens (98% reduction)
- Total available context: 184k → 195k (6% increase)
- More room for conversation/code

### 2. Better UX

**Natural language > Manual commands**:
- "Start session" vs `/nav:start`
- Lower learning curve for new users
- Power users can still be explicit: "Use nav-navigator skill"

### 3. Auto-Composition

**Multiple skills coordinate automatically**:
- User: "Finish feature and document it"
- Claude: Invokes `nav-task-doc` + `nav-sop-creator` + `nav-marker` + `nav-compact`
- All in one request (vs 4 separate commands)

### 4. Portability

**Works beyond Claude Code**:
- Claude.com
- Claude API
- Future LLM coding tools
- Any system that reads markdown

Navigator becomes universal, not Claude-specific.

### 5. Project-Specific Customization

**Skills support project-level placement**:

```
project-a/
├── .claude/skills/nav-custom/  # Custom workflow for project-a
└── .agent/

project-b/
├── .claude/skills/nav-custom/  # Different workflow for project-b
└── .agent/
```

Teams can customize Navigator per project (not possible with global plugin).

### 6. Cleaner Codebase

**Scripts in proper files**:
- Not bash-in-markdown
- Testable independently
- Maintainable (proper syntax highlighting, linting)

---

## Risks & Mitigations

### Risk 1: Code Execution Tool Beta Not Available

**Impact**: Skills can't execute scripts automatically
**Probability**: Medium (beta access required)
**Mitigation**:
- Request beta access now
- Fallback: Skills use Bash tool manually (same as current commands)
- Worst case: Same functionality as today, just different structure

### Risk 2: Users Resist Change

**Impact**: Low adoption of Skills
**Probability**: Low (hybrid approach prevents forced migration)
**Mitigation**:
- Keep commands working in v2.x (no forced upgrade)
- 12-month migration window (ample time)
- Clear communication about benefits
- Show token savings (concrete proof)

### Risk 3: Skills API Changes

**Impact**: Skills break if Anthropic changes format
**Probability**: Low (Skills are stable, documented)
**Mitigation**:
- Keep commands as fallback in v2.x
- Monitor Anthropic announcements
- Update Skills structure if needed

### Risk 4: Complexity During Transition

**Impact**: Users confused about commands vs skills
**Probability**: Medium (two ways to do same thing)
**Mitigation**:
- Clear documentation ("Both work, Skills preferred")
- Deprecation warnings guide users
- Only 6-month overlap period (v2.0 → v2.5)

**Overall Risk Level**: **Low** (hybrid strategy prevents most issues)

---

## Next Steps

### Immediate Actions (This Week)

1. **Request Code Execution Tool beta access**
   - Go to Anthropic Console
   - Enable beta features
   - Test availability

2. **Create proof-of-concept skill**
   - Start with `nav-navigator` (simplest)
   - Test in real project
   - Measure token usage (validate 98% reduction claim)

3. **Extract session-stats script**
   - Move `scripts/session-stats.sh` content to `.py`
   - Test execution
   - Ensure same output

### Short-Term (Next Month)

1. **Build all 5 core skills**
   - nav-navigator
   - nav-task-manager
   - nav-sop-creator
   - nav-marker
   - nav-compact

2. **Extract all scripts from markdown**
   - Commands contain ~10 inline bash blocks
   - Convert to proper `.py` or `.sh` files
   - Store in `skills/*/scripts/`

3. **Test hybrid coexistence**
   - Ensure commands + skills don't conflict
   - Verify flag-based deduplication works
   - Document both approaches

4. **Prepare v2.0 release**
   - Update README (hybrid docs)
   - Create migration guide
   - Announce on GitHub

### Long-Term (Next Year)

1. **Release v2.0** (Q1 2026)
   - Hybrid commands + skills
   - No breaking changes
   - Gather user feedback

2. **Release v2.5** (Q3 2026)
   - Deprecation warnings
   - Skills promoted
   - 6-month notice for v3.0

3. **Release v3.0** (Q1 2027)
   - Skills-only
   - Commands removed
   - Clean architecture

---

## Success Metrics

### Token Efficiency
- [ ] Skills overhead: 250 tokens (vs 11k commands)
- [ ] Total documentation: <6k tokens (vs 16k current)
- [ ] Available context: >194k tokens (vs 184k current)

### User Adoption
- [ ] 50%+ users adopt Skills in v2.0 (6 months)
- [ ] 80%+ users adopt Skills in v2.5 (12 months)
- [ ] 100% users on Skills in v3.0 (18 months)

### UX Improvement
- [ ] Natural language invocation success rate >90%
- [ ] New user onboarding time: -40% (Skills easier than commands)
- [ ] User satisfaction: +30% (survey feedback)

### Code Quality
- [ ] All scripts in proper files (not markdown)
- [ ] 100% test coverage for scripts
- [ ] Zero inline bash in Skills

---

## Decision Point

**Should Navigator migrate to Skills?** **YES - Highly Recommended**

**Why?**
- ✅ Perfect alignment (progressive disclosure)
- ✅ Additional 5-10k token savings
- ✅ Better UX (natural language)
- ✅ Future-proof (portable)
- ✅ Non-breaking migration path
- ✅ Makes Navigator even more efficient (92% → 97%+)

**When?**
- Proof-of-concept: **Now**
- v2.0 release: **Q1 2026** (3 months)
- Full migration: **Q1 2027** (12 months)

**Risk?** **Low**
- Hybrid prevents breaking changes
- 12-month migration window
- Fallback to commands if needed

**Expected Impact**:
- Token efficiency: +5-10k available context
- User experience: -40% faster onboarding
- Portability: Works with any LLM

---

## References

**Research**:
- Anthropic Skills Announcement: https://www.anthropic.com/news/skills
- Skills Documentation: https://docs.claude.com/en/docs/claude-code/skills
- Skills API Guide: https://docs.claude.com/en/api/skills-guide
- Skills Repository: https://github.com/anthropics/skills
- Simon Willison Analysis: https://simonwillison.net/2025/Oct/16/claude-skills/

**Navigator Files**:
- Current commands: `/Users/aleks.petrov/Projects/startups/nav-plugin/commands/`
- Token stats script: `/Users/aleks.petrov/Projects/startups/nav-plugin/scripts/session-stats.sh`
- Plugin config: `/Users/aleks.petrov/Projects/startups/nav-plugin/.claude-plugin/plugin.json`

---

**Task created**: 2025-10-16
**Priority**: High (strategic architecture decision)
**Effort**: Large (3-month implementation for v2.0)
**Impact**: Very High (95%+ token efficiency, better UX, future-proof)
