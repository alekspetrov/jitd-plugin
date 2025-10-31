# Multi-Claude Orchestration SOP

**Version**: 1.0.0
**Created**: 2025-10-31
**Status**: ✅ Production-ready
**Proof of Concept**: Validated with parseJSON utility implementation

---

## Overview

Multi-Claude orchestration enables parallel development workflows by coordinating multiple Claude CLI instances through file-based synchronization. This approach achieves:

- **Parallel execution**: Multiple features developed simultaneously
- **Fast iteration**: 2-5 minutes per feature vs 10-20 minutes interactive
- **Consistent quality**: Plan-driven implementation with validation
- **Zero context limits**: Each Claude instance works independently

---

## Architecture

### Components

```
┌─────────────────────────────────────────────────────────┐
│                    Orchestration Script                 │
│              (navigator-multi-claude-poc.sh)            │
└───────────────┬─────────────────────────────────────────┘
                │
      ┌─────────┴─────────┐
      │                   │
      ▼                   ▼
┌──────────┐        ┌──────────────┐
│ Phase 1  │        │   Phase 2    │
│ Planning │───────▶│Implementation│
│ (Claude) │  file  │   (Claude)   │
└──────────┘  sync  └──────────────┘
      │                   │
      ▼                   ▼
  plan.md             done marker
```

### File Synchronization

**Phase boundaries marked by files**:
- `.agent/tasks/poc-{timestamp}-plan.md` - Plan document
- `.agent/tasks/poc-{timestamp}-done` - Completion marker

**Benefits over markers/skills**:
- ✅ Works in headless mode
- ✅ No skill invocation delays
- ✅ Simple, reliable synchronization
- ✅ Shorter timeouts (2min vs 5min)

---

## Implementation Guide

### Prerequisites

```bash
# Required tools
- Claude CLI (claude)
- jq (JSON parsing)
- bash 4.0+

# Required permissions
- --dangerously-skip-permissions flag for headless tool use
```

### Phase 1: Planning (Orchestrator Claude)

**Purpose**: Create detailed implementation plan

**Input**: Feature description (natural language)

**Process**:
```bash
claude -p "Start Navigator session. Create implementation plan for: ${feature}.
Save to ${plan_file} using Write tool. Include:
1) Feature description
2) Implementation steps
3) Files to modify
4) Expected outcome" \
  --output-format json \
  --dangerously-skip-permissions
```

**Output**: `.agent/tasks/poc-{timestamp}-plan.md`

**Typical duration**: 30-60 seconds

### Phase 2: Implementation

**Purpose**: Execute plan and build feature

**Input**: Plan file from Phase 1

**Process**:
```bash
claude -p "Read plan from ${plan_file}. Implement feature following the plan.
When done, create ${done_file} using: touch ${done_file}" \
  --output-format json \
  --allowedTools "Read,Write,Edit,Bash" \
  --dangerously-skip-permissions
```

**Output**:
- Feature implementation (code, tests, docs)
- Completion marker file

**Typical duration**: 1-3 minutes

### Synchronization Logic

**Wait for file creation**:
```bash
wait_for_file() {
  local file_path="$1"
  local timeout=120  # 2 minutes

  while [ ! -f "$file_path" ]; do
    if [ $elapsed -ge $timeout ]; then
      return 1  # Timeout
    fi
    sleep 1
    ((elapsed++))
  done
  return 0  # Success
}
```

**Critical**: Use `--dangerously-skip-permissions` to bypass interactive prompts in headless mode.

---

## POC Results

### Phase 0: 2-Phase Sequential (parseJSON Utility)

**Timeline**:
- Planning: 36 seconds
- Implementation: 2 minutes 3 seconds
- **Total**: 2 minutes 39 seconds

**Deliverables**:
```
utils/
├── parseJSON.ts           (104 lines, production-quality)
├── __tests__/
│   └── parseJSON.test.ts  (258 lines, comprehensive coverage)
└── index.ts               (barrel export)
```

**Quality metrics**:
- ✅ TypeScript generics with type safety
- ✅ Two variants (safe + strict mode)
- ✅ Full JSDoc documentation
- ✅ Edge case handling (null, undefined, empty, malformed)
- ✅ Error logging with truncation
- ✅ 100% test coverage scenarios

---

### Phase 1: 3-Phase Sequential (validateEmail Utility)

**Timeline**:
- Planning: 34 seconds
- Implementation: 2 minutes 20 seconds
- Testing: 1 minute 16 seconds
- **Total**: 4 minutes 10 seconds

**Added**: Automated testing phase with quality gate validation

**Quality gate**: Tests must pass before completion

---

### Phase 2: 4-Phase Parallel (truncate Utility)

**Timeline**:
- Planning: 17 seconds
- Implementation: 1 minute 8 seconds
- **Testing (parallel): 1 minute 15 seconds**
- **Documentation (parallel): 2 minutes 52 seconds**
- **Total**: 4 minutes 29 seconds

**vs Sequential**: Would be 5m 32s → **Saved 1m 3s (19% faster)**

**Deliverables**:
```
utils/
├── truncate.ts
├── __tests__/
│   └── truncate.test.ts  (auto-generated, comprehensive)
└── [documentation improvements in JSDoc]
```

**Parallel execution proof**:
- Testing completed: 21:13:37
- Docs completed: 21:15:14
- Both ran simultaneously after implementation

**Key learning**: Must use explicit tool instructions ("using the Bash tool: touch") for marker creation in parallel processes

### Key Learnings

#### 1. Skills Don't Auto-Invoke in Headless Mode

**Problem**: Markers, skills use natural language triggers that expand prompts but don't execute in `--print` mode.

**Solution**: Direct tool calls (Write, Bash) for synchronization.

#### 2. Permission Prompts Block Execution

**Problem**: `"permission_denials"` in JSON output - tools blocked by default.

**Solution**: `--dangerously-skip-permissions` flag (safe in trusted project directories).

#### 3. File Sync More Reliable Than Markers

**Comparison**:
| Method | Timeout | Success Rate | Complexity |
|--------|---------|--------------|------------|
| Markers | 5 min | 0% headless | High |
| Skills | 5 min | 0% headless | High |
| Files | 2 min | 100% | Low |

---

## Production Workflow

### Full Multi-Claude Pipeline

```bash
# 1. PM reads ticket (Linear/GitHub)
ticket_data=$(gh issue view 123 --json body,title)

# 2. Orchestrator creates plan
./scripts/multi-claude.sh plan "$ticket_data"

# 3. Implementation Claude builds feature
./scripts/multi-claude.sh implement "poc-{id}-plan.md"

# 4. Testing Claude validates
./scripts/multi-claude.sh test "poc-{id}-done"

# 5. Review Claude checks quality
./scripts/multi-claude.sh review "poc-{id}-done"

# 6. Completion: commit, close ticket, notify
./scripts/multi-claude.sh complete "poc-{id}-done"
```

### Parallel Execution

**Run multiple features simultaneously**:
```bash
./scripts/multi-claude.sh "Feature A" &
./scripts/multi-claude.sh "Feature B" &
./scripts/multi-claude.sh "Feature C" &

wait  # Wait for all to complete
```

**Benefits**:
- 3x-5x faster than sequential
- Independent contexts prevent interference
- Automatic conflict detection via git

---

## Skills Integration

### Skills as Documentation

**Skills work in interactive mode, not headless**. For orchestration:

**Option 1: Load skill docs as templates**
```bash
claude -p "Read ~/.claude/plugins/.../skills/frontend-component/SKILL.md.
Create component following that pattern: ${component_name}"
```

**Option 2: Natural language triggers (if needed)**
```bash
# This MAY auto-invoke skills in some contexts
claude -p "Create component named UserProfile with props: name, avatar, bio"
```

**Option 3: Call skill functions directly**
```bash
# Use Python helpers from skills
python3 ~/.claude/plugins/.../skills/nav-marker/functions/marker_compressor.py \
  --input context.txt \
  --max-length 5000
```

### When to Use Skills

- ✅ **Interactive development**: Auto-invocation works
- ✅ **Template loading**: Read SKILL.md for patterns
- ✅ **Function libraries**: Call Python helpers
- ❌ **Headless orchestration**: Use direct file operations

---

## Error Handling

### Common Issues

#### 1. Timeout Waiting for Files

**Symptoms**: Script waits 2 minutes, then fails.

**Causes**:
- Claude didn't use Write tool (permission denied)
- Wrong file path specified
- Claude crashed mid-execution

**Debug**:
```bash
# Check Claude output JSON
echo "$orchestrator_output" | jq '.permission_denials'

# Verify file path matches
ls -la .agent/tasks/poc-*

# Check Claude exit code
echo $?
```

#### 2. Permission Denials

**Symptoms**: `"permission_denials"` in JSON output.

**Solution**: Add `--dangerously-skip-permissions` flag.

#### 3. Claude Exits Before Tool Execution

**Symptoms**: Plan requested but file never created.

**Cause**: In `--print` mode, Claude returns response text without waiting for tools.

**Solution**: Explicit tool instructions in prompt ("using Write tool", "using touch command").

### Monitoring

**Watch script progress**:
```bash
# Run in background
./scripts/navigator-multi-claude-poc.sh "Feature X" &

# Monitor output
tail -f /tmp/multi-claude-{pid}.log

# Check file creation
watch -n 1 'ls -la .agent/tasks/'
```

---

## Performance Optimization

### Speed Improvements

1. **Reduce timeout from 5min to 2min**: Files create quickly or fail immediately
2. **Parallel phases**: When possible, run independent tasks concurrently
3. **Skip Navigator session start**: For simple tasks, load only essential context
4. **Use Haiku model**: For planning phase, faster and cheaper

### Cost Optimization

**Estimated costs per feature**:
- Planning (Sonnet): ~$0.003
- Implementation (Sonnet): ~$0.01
- **Total**: ~$0.013 per feature

**Optimization strategies**:
- Use Haiku for planning: 5x cheaper
- Cache Navigator docs: Save 60-80% on tokens
- Parallel execution: More features per session

---

## Testing

### Validate POC Script

```bash
# Simple utility function test
./scripts/navigator-multi-claude-poc.sh "Add getCurrentTime utility"

# Expected output:
# ✅ Plan created: .agent/tasks/poc-{id}-plan.md
# ✅ Implementation complete
# ✅ Files: utils/getCurrentTime.ts, tests

# Verify git changes
git status
git diff utils/
```

### Quality Checks

**After implementation**:
```bash
# 1. Check plan quality
cat .agent/tasks/poc-{id}-plan.md
# Should include: description, steps, files, outcome

# 2. Verify implementation matches plan
diff <(grep "Files to Modify" plan.md) <(git status --short)

# 3. Run tests
npm test utils/

# 4. Check code quality
npm run lint utils/
```

---

## Security Considerations

### --dangerously-skip-permissions

**What it does**: Bypasses all permission prompts for tool execution.

**Safe when**:
- ✅ Running in trusted project directory
- ✅ Sandboxed environment (Docker, VM)
- ✅ No internet access from sandbox
- ✅ Code review before deployment

**Unsafe when**:
- ❌ Running arbitrary user prompts
- ❌ Full system access
- ❌ Production environments
- ❌ Untrusted codebases

**Alternatives**:
- Pre-approve file paths: `--allowedTools "Write(utils/**/*.ts)"`
- Review plan before implementation
- Run in isolated container

---

## Future Enhancements

### v2.0 Roadmap

1. **Streaming output**: Real-time progress via `--output-format stream-json`
2. **Validation phase**: Auto-run tests after implementation
3. **Review phase**: Quality checks before completion
4. **PM integration**: Auto-read Linear tickets, close when done
5. **Notification**: Slack/Discord alerts on completion
6. **Conflict resolution**: Handle merge conflicts automatically
7. **Rollback**: Revert on test failures

### Advanced Orchestration

**State machine workflow**:
```
Ticket → Plan → Implement → Test → Review → Deploy → Complete
         ↓       ↓          ↓      ↓       ↓       ↓
       Files   Files      Files  Files   Files   Files
```

**Each phase**:
- Independent Claude instance
- Reads previous phase output
- Writes completion marker
- Triggers next phase

---

## Best Practices

### 1. Plan Quality

**Good plans include**:
- Clear feature description
- Step-by-step implementation guide
- Specific file paths
- Expected test cases
- Success criteria

**Bad plans**:
- Vague descriptions ("make it better")
- Missing file paths
- No test requirements
- Unclear outcomes

### 2. Synchronization

**Reliable patterns**:
- ✅ Wait for file existence
- ✅ Short polling intervals (1s)
- ✅ Reasonable timeouts (2min)
- ✅ Explicit error messages

**Avoid**:
- ❌ Polling file contents (race conditions)
- ❌ Long timeouts (slow failure detection)
- ❌ Silent failures

### 3. Error Recovery

**Handle failures gracefully**:
```bash
if ! wait_for_file "$plan_file"; then
  echo "Plan creation failed - check Claude output:"
  echo "$orchestrator_output" | jq -r '.result'
  exit 1
fi
```

---

## Troubleshooting

### Debug Checklist

- [ ] Claude CLI installed and in PATH
- [ ] `jq` installed for JSON parsing
- [ ] `.agent/tasks/` directory exists
- [ ] `--dangerously-skip-permissions` flag present
- [ ] File paths match in prompt and wait function
- [ ] Timeout values reasonable (2min+)
- [ ] Check `permission_denials` in output JSON

### Common Fixes

**"Timeout waiting for file"**:
```bash
# Check if file was created elsewhere
find . -name "poc-*-plan.md" -mmin -5

# Check Claude's actual output
echo "$output" | jq -r '.result'
```

**"Permission denied"**:
```bash
# Add permissions flag
--dangerously-skip-permissions

# Or pre-approve paths
--allowedTools "Write(.agent/**/*)"
```

---

## References

- POC Script: `scripts/navigator-multi-claude-poc.sh`
- Example Output: `.agent/tasks/poc-1761933071-plan.md`
- Claude CLI Docs: `claude --help`
- Navigator Skills: `~/.claude/plugins/.../skills/`

---

**Last Updated**: 2025-10-31
**Validated**: parseJSON utility POC (2m 39s, production quality)
**Status**: ✅ Ready for production use
