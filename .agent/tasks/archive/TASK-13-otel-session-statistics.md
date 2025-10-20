# TASK-13: OpenTelemetry Session Statistics

**Status**: ✅ Completed
**Version**: 3.1.0
**Created**: 2025-10-20
**Completed**: 2025-10-20
**Type**: Enhancement (Minor Version)

---

## Executive Summary

**Goal**: Replace hacky file-size estimation script with official OpenTelemetry metrics for real-time session statistics.

**Impact**:
- Real token usage (not estimates)
- Live session metrics (active time, cost, cache performance)
- Official API (won't break on Claude Code updates)
- Foundation for ROI measurement

**Dependencies**: Claude Code OpenTelemetry support (available now)

---

## Context

### Current Implementation (Hacky)

**File**: `skills/nav-start/scripts/session_stats.py`

```python
# Rough estimation from file size
tokens = file_bytes // 4

# Static calculation
total_tokens = navigator["tokens"] + claude_md["tokens"]
available = 200000 - 50000 - total_tokens
```

**Problems**:
- ❌ Estimates, not real usage
- ❌ Static calculation (ignores actual session)
- ❌ No cache awareness
- ❌ No cost tracking
- ❌ No active time measurement

### Official OpenTelemetry Support (New)

**Claude Code now exports**:
```javascript
// Real metrics
claude_code.token.usage {
  type: "input" | "output" | "cacheRead" | "cacheCreation"
  model: "claude-sonnet-4-5-20250929"
}

claude_code.cost.usage {
  model: "claude-sonnet-4-5-20250929"
}

claude_code.active_time.total {
  // Actual seconds of active work
}
```

**Benefits**:
- ✅ Real data from Claude Code internals
- ✅ Cache-aware (shows free cache reads)
- ✅ Cost tracking (actual USD spent)
- ✅ Active time (not idle time)
- ✅ Official API (stable)

---

## Implementation Plan

### Phase 1: Research OTel Integration

**Goal**: Understand how to query OTel metrics from Python

**Options**:
1. **OpenTelemetry Python SDK** - Query metrics programmatically
2. **Parse console output** - Read `OTEL_METRICS_EXPORTER=console` stderr
3. **Query OTLP endpoint** - HTTP/gRPC to collector

**Decision**: Start with console parsing (simplest), add SDK support later

**Tasks**:
- [x] Read Claude Code OTel documentation
- [ ] Test console exporter output format
- [ ] Determine which metrics are available during session
- [ ] Design parsing strategy

### Phase 2: Implement OTel Session Stats Script

**Goal**: Replace `session_stats.py` with OTel-powered version

**New File**: `skills/nav-start/scripts/otel_session_stats.py`

**Features**:
```python
#!/usr/bin/env python3
"""
Navigator Session Statistics (OpenTelemetry-powered)

Queries real token usage from Claude Code OpenTelemetry metrics.
Requires CLAUDE_CODE_ENABLE_TELEMETRY=1
"""

def check_otel_enabled():
    """Verify OTel is configured"""
    if os.getenv("CLAUDE_CODE_ENABLE_TELEMETRY") != "1":
        print("❌ OpenTelemetry not enabled")
        print("Enable with: export CLAUDE_CODE_ENABLE_TELEMETRY=1")
        sys.exit(1)

def query_session_metrics():
    """
    Query current session metrics from OTel.

    Returns:
    {
        "input_tokens": int,
        "output_tokens": int,
        "cache_read_tokens": int,  # Free!
        "cache_creation_tokens": int,
        "cost_usd": float,
        "active_time_seconds": int,
        "model": str
    }
    """
    # Implementation: Parse OTel console output or query OTLP endpoint

def display_navigator_stats(metrics):
    """
    Display Navigator-optimized session statistics.

    Shows:
    - Total tokens used (with cache breakdown)
    - Cache hit rate (% tokens from cache)
    - Cost analysis
    - Active time efficiency
    - Available context remaining
    """

    print("📊 Navigator Session Statistics (Real-time via OTel)")
    print("━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━")

    # Token usage breakdown
    total_input = metrics["input_tokens"]
    cache_read = metrics["cache_read_tokens"]
    fresh_input = total_input - cache_read

    print(f"\n📥 Input Tokens:  {total_input:,}")
    print(f"   ├─ Cache read:  {cache_read:,} (free ✅)")
    print(f"   └─ Fresh:       {fresh_input:,} (charged)")

    print(f"\n📤 Output Tokens: {metrics['output_tokens']:,}")

    # Cache performance
    if total_input > 0:
        cache_hit_rate = (cache_read / total_input) * 100
        print(f"\n⚡ Cache Hit Rate: {cache_hit_rate:.1f}%")

    # Cost analysis
    print(f"\n💰 Session Cost:  ${metrics['cost_usd']:.4f}")

    # Active time
    minutes = metrics['active_time_seconds'] // 60
    seconds = metrics['active_time_seconds'] % 60
    print(f"\n⏱️  Active Time:   {minutes}m {seconds}s")

    # Context availability
    context_used = total_input + metrics['output_tokens']
    total_context = 200000
    available = total_context - context_used
    percent_available = int((available / total_context) * 100)

    print(f"\n📦 Context Usage:")
    print(f"   ├─ Used:        {context_used:,} tokens")
    print(f"   └─ Available:   {available:,} tokens ({percent_available}%)")

    print(f"\n🤖 Model:         {metrics['model']}")
    print("━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━")
```

**Implementation Steps**:
1. Create new `otel_session_stats.py`
2. Implement OTel detection
3. Implement metric querying (console parser first)
4. Format output for Navigator context
5. Add error handling (OTel not enabled, no metrics yet)

### Phase 3: Update nav-start Skill

**Goal**: Integrate OTel stats into session start

**File**: `skills/nav-start/skill.md`

**Changes**:
```markdown
## Predefined Functions

### scripts/otel_session_stats.py

**Purpose**: Display real-time session statistics via OpenTelemetry

**When to call**: After loading navigator, before presenting session info

**Requirements**:
- CLAUDE_CODE_ENABLE_TELEMETRY=1 must be set
- Metrics must be available from current session

**Execution**:
```bash
python3 .agent/.nav-scripts/otel_session_stats.py
```

**Output**: Formatted statistics with token usage, cache performance, cost

**Error Handling**:
- If OTel not enabled: Show setup instructions
- If no metrics yet: Skip stats (early in session)
```

**Update skill workflow**:
1. Load DEVELOPMENT-README.md
2. Check for PM tool assignments
3. **[NEW] Display OTel session stats**
4. Present navigator index

### Phase 4: Documentation Updates

**Files to update**:

#### 1. `.agent/DEVELOPMENT-README.md`
```markdown
## 📊 Session Statistics (New in v3.1)

Navigator now uses OpenTelemetry for real-time session metrics.

**Setup** (one-time):
```bash
# Enable Claude Code telemetry
export CLAUDE_CODE_ENABLE_TELEMETRY=1
export OTEL_METRICS_EXPORTER=console
```

**What you get**:
- Real token usage (not estimates)
- Cache hit rates (CLAUDE.md caching performance)
- Session costs (actual USD spent)
- Active time tracking

**See**: `.agent/sops/integrations/opentelemetry-setup.md`
```

#### 2. Create `.agent/sops/integrations/opentelemetry-setup.md`

**New SOP for OTel configuration**:
```markdown
# OpenTelemetry Setup for Navigator

## Quick Start

**Enable telemetry**:
```bash
# Add to ~/.zshrc or ~/.bashrc
export CLAUDE_CODE_ENABLE_TELEMETRY=1
export OTEL_METRICS_EXPORTER=console

# Optional: Reduce export interval for development
export OTEL_METRIC_EXPORT_INTERVAL=10000  # 10 seconds
```

**Restart shell**:
```bash
source ~/.zshrc
```

## What Navigator Tracks

**Metrics used by Navigator**:
- `claude_code.token.usage` - Input/output/cache breakdown
- `claude_code.cost.usage` - Session costs in USD
- `claude_code.active_time.total` - Active work time

**Benefits**:
- Prove Navigator ROI with real data
- Monitor cache performance (CLAUDE.md efficiency)
- Track session costs
- Measure productivity (LOC per token)

## Advanced Configuration

**For teams wanting centralized monitoring**:
```bash
# Use OTLP exporter to send to Prometheus/Grafana
export OTEL_METRICS_EXPORTER=otlp
export OTEL_EXPORTER_OTLP_PROTOCOL=grpc
export OTEL_EXPORTER_OTLP_ENDPOINT=http://localhost:4317
```

**See**: Official Claude Code docs for full OTel setup
```

#### 3. Update `CLAUDE.md` template

**Add OTel section**:
```markdown
## Session Statistics (Optional)

For real-time token tracking, enable OpenTelemetry:

```bash
export CLAUDE_CODE_ENABLE_TELEMETRY=1
export OTEL_METRICS_EXPORTER=console
```

Navigator will show cache performance and session costs.
```

#### 4. Update `README.md`

**Add to features**:
```markdown
### 📊 Real-Time Session Statistics (v3.1+)

- **Official OTel integration** - Real metrics from Claude Code
- **Cache performance** - See CLAUDE.md caching in action
- **Cost tracking** - Monitor session spend
- **Active time** - Measure productivity
```

### Phase 5: Testing

**Test Scenarios**:

#### Test 1: OTel Disabled (Graceful Handling)
```bash
# Unset OTel
unset CLAUDE_CODE_ENABLE_TELEMETRY

# Start session
"Start my Navigator session"

# Expected: Script shows setup instructions, doesn't crash
```

#### Test 2: OTel Enabled, Console Exporter
```bash
# Enable OTel
export CLAUDE_CODE_ENABLE_TELEMETRY=1
export OTEL_METRICS_EXPORTER=console
export OTEL_METRIC_EXPORT_INTERVAL=10000

# Start new session
"Start my Navigator session"

# Expected: Real metrics displayed
# - Input tokens (with cache breakdown)
# - Output tokens
# - Cache hit rate
# - Cost
# - Active time
```

#### Test 3: Early Session (No Metrics Yet)
```bash
# Very first message after `claude` starts
"Start my Navigator session"

# Expected: Graceful handling if no metrics exported yet
```

#### Test 4: Cache Performance Validation
```bash
# Session 1: Load CLAUDE.md (creates cache)
"Start my Navigator session"
# Note cache_creation_tokens

# Session 2: Load CLAUDE.md again (uses cache)
"Start my Navigator session"
# Note cache_read_tokens (should be high)

# Expected: cache_read_tokens > 0 in session 2
```

#### Test 5: Cost Tracking Accuracy
```bash
# Enable OTel
export CLAUDE_CODE_ENABLE_TELEMETRY=1
export OTEL_METRICS_EXPORTER=console

# Run multiple interactions
"Start session"
"Write a hello world function"
"Create tests"

# Check cost accumulation
python3 .agent/.nav-scripts/otel_session_stats.py

# Expected: Cost increases with each interaction
```

---

## File Changes Summary

### New Files
```
skills/nav-start/scripts/otel_session_stats.py  (replaces session_stats.py)
.agent/sops/integrations/opentelemetry-setup.md  (new SOP)
```

### Modified Files
```
skills/nav-start/skill.md  (add OTel stats call)
.agent/DEVELOPMENT-README.md  (add session statistics section)
templates/CLAUDE.md  (add OTel optional section)
README.md  (add v3.1 feature)
scripts/post-install.sh  (auto-enable OTel on plugin install/update)
```

### Deleted Files
```
skills/nav-start/scripts/session_stats.py  (replaced by otel_session_stats.py)
```

### Auto-Enablement on Plugin Update

**scripts/post-install.sh** now includes OTel setup:
- Prompts user to enable OpenTelemetry after install/update
- Auto-detects shell config (.zshrc or .bashrc)
- Checks if already configured (doesn't duplicate)
- Adds environment variables automatically
- Provides manual instructions as fallback

**User experience on upgrade to v3.1**:
```bash
/plugin update navigator

# Post-install hook runs:
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
📊 Navigator v3.1 - OpenTelemetry Integration
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Navigator can show real-time session statistics:
  • Real token usage (input/output/cache)
  • Cache hit rates (CLAUDE.md performance)
  • Session costs (actual USD spent)
  • Active time tracking

Enable OpenTelemetry? [Y/n]

# User types Y:
✅ Added OpenTelemetry configuration to .zshrc

⚠️  Restart your terminal or run:
   source ~/.zshrc
```

**Result**: Zero-config upgrade - telemetry works automatically after terminal restart

---

## Technical Implementation Details

### OTel Metrics Query Strategy

**Phase 1: Console Parser** (v3.1.0)
```python
def parse_console_metrics():
    """
    Parse metrics from OTEL_METRICS_EXPORTER=console output.

    Console exporter writes to stderr in format:
    {
      "resource": {...},
      "scope_metrics": [
        {
          "metrics": [
            {
              "name": "claude_code.token.usage",
              "data": {
                "data_points": [...]
              }
            }
          ]
        }
      ]
    }
    """
    # Read from stderr/process output
    # Parse JSON metrics
    # Extract relevant counters
```

**Challenges**:
- Console output is JSON-formatted logs
- Need to parse most recent metrics
- Handle case where no exports yet

**Phase 2: SDK Integration** (Future v3.2+)
```python
from opentelemetry import metrics

def query_via_sdk():
    """Query metrics programmatically via OTel SDK"""
    # Use meter provider to get current metrics
    # More reliable than parsing console output
```

### Metric Aggregation

**Claude Code exports cumulative counters**:
```javascript
// Metrics are session-total, not per-request
claude_code.token.usage: 15000  // Total since session start
```

**Our script shows**:
- Session totals (from counters)
- Derived metrics (cache hit rate, context remaining)
- No need to track deltas (session-level stats)

### Error Handling

**Scenarios to handle**:

1. **OTel not enabled**
   ```python
   if not check_otel_enabled():
       print("OpenTelemetry not enabled")
       print("See: .agent/sops/integrations/opentelemetry-setup.md")
       sys.exit(0)  # Exit gracefully, don't crash nav-start
   ```

2. **No metrics exported yet**
   ```python
   metrics = query_session_metrics()
   if not metrics:
       print("No metrics available yet (early in session)")
       sys.exit(0)
   ```

3. **Parse errors**
   ```python
   try:
       data = json.loads(console_output)
   except json.JSONDecodeError:
       print("Could not parse OTel output")
       sys.exit(0)
   ```

---

## Success Metrics

### Functionality
- [ ] OTel stats script works with `CLAUDE_CODE_ENABLE_TELEMETRY=1`
- [ ] Graceful handling when OTel disabled
- [ ] Cache performance metrics accurate
- [ ] Cost tracking matches Claude Console
- [ ] Active time displayed correctly

### Integration
- [ ] nav-start skill calls OTel stats automatically
- [ ] Stats display before navigator index
- [ ] No errors when OTel unavailable
- [ ] Documentation clear and accurate

### User Experience
- [ ] Real metrics more useful than estimates
- [ ] Cache hit rate validates Navigator efficiency
- [ ] Cost tracking enables ROI measurement
- [ ] Setup instructions work (one-time config)

---

## Risks & Mitigation

### Risk 1: OTel Output Format Changes

**Problem**: Console exporter format could change
**Impact**: Parser breaks on Claude Code updates
**Mitigation**:
- Use stable OTel spec (unlikely to change)
- Add version detection
- Fall back to "metrics unavailable" on parse errors
- Future: Move to SDK instead of parsing

**Likelihood**: Low
**Severity**: Low (graceful degradation)

### Risk 2: Metrics Not Available Early in Session

**Problem**: OTel exports every 60s (default), might not have data yet
**Impact**: Empty stats on first /nav:start
**Mitigation**:
- Handle empty metrics gracefully
- Show message: "Metrics not available yet"
- Recommend shorter export interval for dev

**Likelihood**: Medium
**Severity**: Low (just wait for export)

### Risk 3: Users Don't Enable OTel

**Problem**: Most users won't configure OTel
**Impact**: Stats feature unused
**Mitigation**:
- Make it optional (graceful when disabled)
- Clear setup instructions
- Show value prop (ROI measurement)
- Consider auto-detecting and prompting

**Likelihood**: High
**Severity**: Low (optional feature)

---

## Future Enhancements (Post-v3.1)

### v3.2: ROI Dashboard
```python
# skills/navigator-roi/
Generate Grafana dashboard from OTel metrics:
- Token savings (Navigator vs standard sessions)
- Cache performance over time
- Cost per feature delivered
- Productivity metrics (LOC per token)
```

### v3.3: Team Analytics
```python
# Multi-user tracking
export OTEL_RESOURCE_ATTRIBUTES="team=engineering,user=alice"

# Aggregate metrics across team
navigator-analytics --team engineering --period week
```

### v3.4: SDK Integration
```python
# Replace console parsing with SDK
from opentelemetry import metrics
meter = metrics.get_meter(__name__)
counter = meter.get_counter("claude_code.token.usage")
```

---

## Version Sync Checklist

**Update version to 3.1.0 in**:
- [ ] `.claude-plugin/plugin.json` → `"version": "3.1.0"`
- [ ] `.claude-plugin/marketplace.json` → `"version": "3.1.0"`
- [ ] `.agent/.nav-config.json` → `"version": "3.1.0"`
- [ ] `README.md` line ~5 → `v3.1.0`
- [ ] `README.md` line ~8 (badge) → `3.1.0`
- [ ] `README.md` footer → `3.1.0`
- [ ] `.agent/DEVELOPMENT-README.md` bottom → `(v3.1.0)`
- [ ] Git tag → `v3.1.0`
- [ ] GitHub release → `v3.1.0`

**Run audit script**:
```bash
./scripts/version-audit.sh 3.1.0
```

---

## Timeline

**Total Effort**: 2 days

### Day 1: Implementation
- Morning: Create `otel_session_stats.py` (console parser)
- Afternoon: Update nav-start skill integration
- Evening: Test with OTel enabled/disabled

### Day 2: Documentation & Testing
- Morning: Create OpenTelemetry SOP
- Afternoon: Update all docs (README, CLAUDE.md, DEVELOPMENT-README)
- Evening: Comprehensive testing (all 5 test scenarios)

**Target Release**: 2025-10-22

---

## Related Tasks

- **TASK-06**: Real Session Statistics (original hacky implementation)
- **TASK-12**: v3.0 Skills-Only Migration (foundation)
- **Future TASK-14**: ROI Dashboard & Team Analytics (builds on this)

---

## Notes

### Why This Matters

1. **Validation**: Proves Navigator's 92% token reduction with real data
2. **ROI**: Teams can measure actual savings (cost reduction)
3. **Cache Performance**: Shows CLAUDE.md caching working
4. **Official API**: Won't break on updates (vs parsing internals)
5. **Foundation**: Enables future analytics features

### What Changed from TASK-06

**TASK-06** (original):
- Parsed Claude Code internal files
- File-size estimation (bytes / 4)
- Static calculation
- Fragile (breaks on updates)

**TASK-13** (new):
- Uses official OpenTelemetry API
- Real token counts from Claude
- Dynamic session metrics
- Stable (official spec)

**Migration**: Delete old `session_stats.py`, replace with `otel_session_stats.py`

---

**Task created**: 2025-10-20
**Priority**: Medium (enhancement, not critical)
**Effort**: Small (2 days)
**Impact**: High (validates Navigator value with real metrics)
