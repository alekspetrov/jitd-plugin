# TASK-18.3: Metrics Enhancement - Make Savings Visible

**Parent**: TASK-18 (Principle to Product v3.5.0)
**Timeline**: Week 3
**Effort**: 3-4 days
**Priority**: High

---

## Objective

Extend TASK-06 session statistics to provide real-time efficiency reporting with baseline comparisons, making Navigator's value quantifiable and shareable.

---

## Context

TASK-06 proved Navigator caching works (100% cache efficiency, 14.8M cached tokens).

**Missing**:
- Comparison to baseline ("without Navigator")
- Efficiency scoring (how well are you using Navigator?)
- Time savings estimation
- Shareable efficiency reports

**Goal**: Users screenshot efficiency reports and share: "Navigator saved me 138k tokens today"

---

## Deliverables

### 1. Enhanced `scripts/session-stats.sh`

**New Calculations**:

```bash
# Baseline Calculation (upfront loading)
BASELINE_TOKENS=$(calculate_all_docs_size)  # All .agent/ docs
CURRENT_TOKENS=$(get_loaded_docs_size)      # Actually loaded
TOKENS_SAVED=$((BASELINE_TOKENS - CURRENT_TOKENS))
SAVINGS_PERCENT=$((TOKENS_SAVED * 100 / BASELINE_TOKENS))

# Efficiency Score (0-100)
EFFICIENCY_SCORE=$(calculate_efficiency_score)
# Formula:
# - Token savings: 40 points (max at >85% savings)
# - Cache efficiency: 30 points (100% = 30 points)
# - Context usage: 30 points (<40% = 30 points, >80% = 0 points)

# Time Savings Estimation
TIME_SAVED=$(estimate_time_saved)
# Formula:
# - Per 1k tokens: ~6 seconds read time
# - Tokens saved * 6s / 1000 = seconds saved
# - Convert to minutes
```

**Output Format** (shell-parseable):
```bash
# Existing (from TASK-06)
MESSAGES=183
INPUT_TOKENS=811
OUTPUT_TOKENS=66408
CACHE_CREATION=1403986
CACHE_READ=14861372
TOTAL_FRESH=1404797
TOTAL_CACHED=14862183
CACHE_EFFICIENCY=100.0

# New
BASELINE_TOKENS=150000
LOADED_TOKENS=12000
TOKENS_SAVED=138000
SAVINGS_PERCENT=92
EFFICIENCY_SCORE=94
TIME_SAVED_MINUTES=42
CONTEXT_USAGE_PERCENT=35
```

---

### 2. New `nav-stats` Skill

**Location**: `skills/nav-stats/`

**Purpose**: Display user-friendly efficiency report (Navigator v3.0+ uses skills-only architecture)

**Output Format**:
```
╔══════════════════════════════════════════════════════╗
║          NAVIGATOR EFFICIENCY REPORT                 ║
╚══════════════════════════════════════════════════════╝

📊 TOKEN USAGE
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Documentation loaded:        12,000 tokens
Baseline (all docs):        150,000 tokens
Tokens saved:               138,000 tokens (92% ↓)

💾 CACHE PERFORMANCE
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Cache creation:           1,403,986 tokens (loaded once)
Cache read:              14,861,372 tokens (reused 10.5x)
Cache efficiency:              100.0% (perfect)

📈 SESSION METRICS
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Messages in session:               183
Context usage:                      35% (excellent)
Efficiency score:                94/100 (excellent)

⏱️  TIME SAVED
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Estimated time saved:          ~42 minutes

💡 WHAT THIS MEANS
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Navigator loaded 92% fewer tokens than loading all docs.
Documentation was cached perfectly (zero fresh re-reads).
Your context window is 65% available for actual work.

🎯 RECOMMENDATIONS
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
✅ Excellent efficiency - keep using lazy-loading strategy
✅ Cache working perfectly - no optimization needed
✅ Context usage healthy - plenty of room for work

Share your efficiency: Take a screenshot! #ContextEfficiency
```

**Variations**:

If efficiency < 70:
```
⚠️  RECOMMENDATIONS
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
⚠️  Token savings below target (70%+)
→ Check: Are you loading more docs than needed?
→ Tip: Use navigator to find docs, don't load all upfront

Read more: .agent/philosophy/CONTEXT-EFFICIENCY.md
```

If context usage > 80%:
```
⚠️  RECOMMENDATIONS
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
⚠️  Context usage high (80%+)
→ Consider: Running /nav:compact to clear old context
→ Tip: Compact after completing sub-tasks

Read more: .agent/philosophy/ANTI-PATTERNS.md
```

---

### 3. Predefined Functions

**Location**: `skills/nav-stats/functions/`

#### `efficiency_scorer.py`

Calculate Navigator efficiency score (0-100):

```python
def calculate_efficiency_score(
    tokens_saved_percent: float,
    cache_efficiency: float,
    context_usage_percent: float
) -> int:
    """
    Calculate Navigator efficiency score (0-100)

    Weights:
    - Token savings: 40 points
    - Cache efficiency: 30 points
    - Context usage: 30 points
    """
    # Token savings (40 points max)
    # 85%+ savings = 40 points, linear scale
    token_score = min(40, (tokens_saved_percent / 85) * 40)

    # Cache efficiency (30 points max)
    # 100% = 30 points, linear scale
    cache_score = (cache_efficiency / 100) * 30

    # Context usage (30 points max)
    # <40% = 30 points, 40-80% linear, >80% = 0 points
    if context_usage_percent < 40:
        context_score = 30
    elif context_usage_percent <= 80:
        # Linear from 30 (at 40%) to 0 (at 80%)
        context_score = 30 - ((context_usage_percent - 40) / 40) * 30
    else:
        context_score = 0

    return int(token_score + cache_score + context_score)
```

#### `report_formatter.py`

Format efficiency report output (visual, shareable format)

**Score Interpretation**:
- 90-100: Excellent (optimal Navigator usage)
- 80-89: Good (minor improvements possible)
- 70-79: Fair (review lazy-loading strategy)
- <70: Needs improvement (check anti-patterns)

---

### 4. Time Savings Estimation

**Formula**:
```bash
# Average reading speed: ~10 tokens/second for comprehension
# 1,000 tokens = ~100 seconds = ~1.7 minutes

TIME_SAVED_SECONDS=$((TOKENS_SAVED / 10))
TIME_SAVED_MINUTES=$((TIME_SAVED_SECONDS / 60))

# Display:
if [ $TIME_SAVED_MINUTES -lt 60 ]; then
    echo "~${TIME_SAVED_MINUTES} minutes"
else
    HOURS=$((TIME_SAVED_MINUTES / 60))
    MINS=$((TIME_SAVED_MINUTES % 60))
    echo "~${HOURS}h ${MINS}m"
fi
```

**Conservative estimate** (reading only, not processing time)

---

### 5. Baseline Calculation

**Baseline = All documentation tokens without Navigator**

```bash
calculate_baseline() {
    local baseline=0

    # All .agent/ docs
    if [ -d ".agent" ]; then
        # Find all .md files, calculate tokens
        baseline=$(find .agent -name "*.md" -type f -exec wc -c {} + | \
                   awk '{sum+=$1} END {print int(sum/4)}')
    fi

    # CLAUDE.md
    if [ -f "CLAUDE.md" ]; then
        baseline=$((baseline + $(wc -c < CLAUDE.md) / 4))
    fi

    # README.md (if relevant)
    if [ -f "README.md" ]; then
        baseline=$((baseline + $(wc -c < README.md) / 4))
    fi

    echo $baseline
}
```

---

## Implementation Details

### File Structure

```
scripts/
├── session-stats.sh           # Enhanced with new metrics
└── lib/
    ├── baseline-calc.sh       # Baseline calculation logic
    ├── efficiency-score.sh    # Scoring algorithm
    └── time-estimate.sh       # Time savings estimation

commands/
└── stats.md                   # New "Show me my session statistics" command
```

### Integration Points

1. **`commands/start.md`** (optional enhancement)
   - Add one-line efficiency preview
   - "Session efficiency: 94/100 (excellent)"

2. **Navigator index** (DEVELOPMENT-README.md)
   - Add reference to `"Show me my session statistics"`
   - Link to philosophy for score interpretation

3. **CLAUDE.md** (optional)
   - Mention efficiency scoring
   - Encourage periodic `"Show me my session statistics"` checks

---

## Testing Plan

### Unit Tests (shell functions)

```bash
# Test: Baseline calculation
test_baseline() {
    # Given: Known .agent/ size (50k tokens)
    # When: calculate_baseline
    # Then: Returns ~50000
}

# Test: Efficiency score
test_efficiency_score() {
    # Given: 90% savings, 100% cache, 30% context
    # When: calculate_efficiency_score 90 100 30
    # Then: Returns ~96
}

# Test: Time estimation
test_time_estimate() {
    # Given: 138000 tokens saved
    # When: estimate_time_saved 138000
    # Then: Returns ~23 minutes
}
```

### Integration Tests

```bash
# Test: Full stats command
test_nav_stats_command() {
    # Given: Active session with known metrics
    # When: "Show me my session statistics"
    # Then: Displays report with all sections
    # And: No errors
}

# Test: Score interpretation
test_score_recommendations() {
    # Given: Low efficiency (60)
    # When: "Show me my session statistics"
    # Then: Shows warning recommendations
}
```

### Real-World Validation

1. Run on Navigator's own repo (known baseline)
2. Compare calculated vs manual metrics
3. Verify efficiency score makes sense
4. Test recommendations logic

---

## Acceptance Criteria

### Functionality
- [ ] `scripts/session-stats.sh` calculates all new metrics
- [ ] `"Show me my session statistics"` command displays formatted report
- [ ] Efficiency score algorithm implemented correctly
- [ ] Time estimation reasonable (within 20% of manual calc)
- [ ] Baseline calculation accurate

### User Experience
- [ ] Report is visually clear (ASCII formatting)
- [ ] Recommendations are actionable
- [ ] Scores are intuitive (90+ = excellent feels right)
- [ ] Shareable (fits in screenshot)

### Technical
- [ ] No breaking changes to TASK-06 output
- [ ] Backwards compatible (works if baseline unavailable)
- [ ] Graceful degradation (missing data handled)
- [ ] Performance: <1s to generate report

### Documentation
- [ ] `"Show me my session statistics"` usage documented
- [ ] Efficiency score explained
- [ ] Philosophy docs linked for context

---

## Success Metrics

### Immediate
- [ ] Report generates correctly on test session
- [ ] Efficiency score matches manual calculation
- [ ] 3 users screenshot and share (internal beta)

### Week 4
- [ ] Users understand their efficiency score
- [ ] Recommendations lead to behavior change
- [ ] "I saved X tokens" becomes common phrase

### Long-term (post-v3.5.0)
- [ ] 50+ social shares of efficiency reports
- [ ] "Efficiency score" becomes Navigator metric
- [ ] Users optimize to improve score (gamification)

---

## Visual Assets Created

From this task, generate:

1. **Before/After Screenshot**
   - Before: Claude session with 150k context
   - After: Navigator stats showing 12k loaded

2. **Efficiency Score Visualization**
   ```
   Your Efficiency: 94/100

   Token Savings    ████████████████████ 40/40
   Cache Efficiency ███████████████████  28/30
   Context Usage    █████████████████    26/30
   ```

3. **Time Savings Graph** (optional)
   - Cumulative time saved across sessions
   - "You've saved 14 hours this month"

---

## Dependencies

**Requires**:
- TASK-06 (session-stats.sh foundation)

**Blocks**:
- TASK-18.4 (case studies need metrics)
- Social media content (proof points)

**Enables**:
- Marketing ("92% savings" becomes "Score: 94/100")
- Community competition (efficiency leaderboard)
- User advocacy (shareable proof)

---

## Open Questions

1. **Baseline calculation**: Include archived tasks?
   - **Answer**: No - only active docs count

2. **Time estimation**: Conservative or aggressive?
   - **Answer**: Conservative (reading only, not processing)

3. **Score weighting**: 40/30/30 optimal?
   - **Answer**: Test with beta users, adjust if needed

4. **Frequency**: Should `"Show me my session statistics"` auto-run?
   - **Answer**: No - on-demand only (user control)

---

## Migration Notes

### From TASK-06

No breaking changes required:
- Enhanced script adds new output variables
- Old output format preserved
- `/nav:start` continues working unchanged

### For Existing Users

- `"Show me my session statistics"` available immediately after upgrade
- No configuration needed
- Backwards compatible with v3.4.0 data

---

## Next Steps After Completion

1. **Create case studies** (TASK-18.4) using real efficiency reports
2. **Update marketing materials** with efficiency scores
3. **Social media templates** for sharing stats
4. **Blog post**: "How Navigator calculates efficiency"

---

**This makes Navigator's value visible, quantifiable, and shareable.**

**Users go from "Navigator is fast" to "Navigator saved me 138k tokens and 42 minutes."**
