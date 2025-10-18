---
description: Create context markers on-demand - save your progress anytime
---

# Navigator Marker - Save Points for Your Conversation

Create context markers during work to capture your current state. Think of it as **git commits for your AI conversation**.

---

## What This Does

Creates a snapshot of your current work state that you can restore later.

**Traditional approach**: Work until compact, lose intermediate context

**With markers**:
- Save progress anytime
- Multiple markers per session
- Resume from any point
- Safety nets before risky changes

---

## When to Use

### ✅ Perfect Times for Markers

**Before taking breaks**:
```
You: "Implemented auth flow, going to lunch"
You: /nav:marker lunch-break
Result: Resume perfectly after lunch
```

**Before exploring approaches**:
```
You: /nav:marker before-refactor
You: "Let's try refactoring X"
*doesn't work*
You: Read @.agent/.context-markers/before-refactor.md
Result: Back to known good state
```

**During long features**:
```
Day 1: Core implementation → /nav:marker day1-core
Day 2: Add integrations → /nav:marker day2-integrations
Day 3: Tests & polish → /nav:marker day3-complete
Result: Checkpoints throughout multi-day work
```

**Before risky changes**:
```
You: "About to refactor entire routing system"
You: /nav:marker pre-routing-refactor
Result: Safety net if things go wrong
```

**End of day**:
```
You: /nav:marker eod-2025-10-12
Result: Tomorrow starts with perfect context
```

**After important decisions**:
```
You: "We decided to use PostgreSQL instead of MongoDB"
You: /nav:marker architecture-decision
Result: Decision captured with full context
```

---

## Usage

### Basic Usage

```bash
/nav:marker
```

Creates marker with auto-generated name: `marker-2025-10-12-143022.md`

### Named Markers

```bash
/nav:marker before-refactor
/nav:marker lunch-break
/nav:marker pre-deployment
/nav:marker day1-complete
```

Creates marker with your name: `before-refactor-2025-10-12-143022.md`

### With Description

```bash
/nav:marker oauth-working "OAuth flow implemented and tested"
```

Adds description to marker content.

---

## Marker Creation Process

### Step 1: Analyze Current State

Scan conversation for:

**Active work**:
- Current task/feature
- Files being modified
- What's implemented
- What's remaining

**Recent context**:
- Technical decisions made
- Approaches tried (successful and failed)
- Dependencies added
- Blockers encountered

**Next steps**:
- What you planned to do next
- Open questions
- Ideas to explore

### Step 2: Generate Marker Content

Create comprehensive marker:

```markdown
# Navigator Context Marker: [Name]

**Created**: 2025-10-12 14:30:22
**Type**: On-demand marker
**Navigator**: .agent/DEVELOPMENT-README.md

---

## 📍 Current Location

**Task**: TASK-123 - Implement OAuth authentication
**Phase**: Integration complete, testing pending
**Files**:
- src/auth/oauth.ts (implemented)
- src/routes/auth.ts (updated)
- tests/auth.test.ts (needs work)

**Progress**: 70% complete

---

## 🎯 What's Done

- ✅ OAuth flow implemented with passport.js
- ✅ JWT token generation working
- ✅ Login/logout endpoints created
- ✅ Session management configured
- ✅ Google OAuth provider integrated

---

## 🔧 Technical Decisions

**OAuth Library**: Chose passport.js over next-auth
- Reason: More control over flow, simpler for our use case
- Trade-off: More manual config, but cleaner integration

**Token Strategy**: JWT in httpOnly cookies
- Reason: XSS protection, no localStorage needed
- Expiration: 7 days, refresh token pattern

**Session Store**: Redis
- Reason: Fast, scalable, easy invalidation
- Config: TTL matches JWT expiration

---

## ⚠️ Challenges & Solutions

**Challenge**: CORS issues with OAuth callback
**Solution**: Added credentials: 'include' and proper CORS headers
**File**: src/middleware/cors.ts

**Challenge**: Token not persisting across requests
**Solution**: Missing httpOnly flag in cookie options
**File**: src/auth/tokens.ts:45

---

## 📝 Next Steps

1. Write comprehensive tests for OAuth flow
   - Happy path: successful login
   - Error cases: invalid tokens, expired sessions
   - Edge cases: concurrent logins, token refresh

2. Add error handling for failed OAuth
   - Network errors
   - Provider downtime
   - Invalid credentials

3. Document OAuth setup in README
   - Environment variables needed
   - Provider setup instructions
   - Local development flow

---

## 🔗 Related Documentation

**Already documented**:
- .agent/system/auth-architecture.md - Auth system design
- .agent/sops/integrations/oauth-setup.md - OAuth provider config

**Needs documentation**:
- Testing strategy for OAuth
- Production deployment checklist

---

## 💡 Ideas to Explore

- Add more OAuth providers (GitHub, Twitter)
- Implement OAuth scope management
- Add "Sign in with" UI component library
- Consider magic link as alternative auth method

---

## 🚫 Don't Load Again

These are already documented, don't reload:
- .agent/tasks/TASK-123-oauth-auth.md
- .agent/system/auth-architecture.md
- Previous markers (if any)

---

## 🔄 Restore Instructions

To resume from this marker:

1. Read this marker:
   ```
   Read @.agent/.context-markers/oauth-working-2025-10-12-143022.md
   ```

2. Continue with: "Write tests for OAuth flow"

**Context restored in ~3k tokens instead of replaying 130k token conversation.**

---

Generated by: /nav:marker oauth-working
```

### Step 3: Save Marker

**Create directory if needed**:
```bash
mkdir -p .agent/.context-markers
```

**Save with naming convention**:
```
Format: [user-name]-YYYY-MM-DD-HHMMSS.md
Example: oauth-working-2025-10-12-143022.md
```

**Write marker**:
```
Write(
  file_path: ".agent/.context-markers/oauth-working-2025-10-12-143022.md"
  content: [marker content from Step 2]
)
```

### Step 4: Confirm to User

Show clear confirmation:

```
✅ Marker saved!

📍 Location: .agent/.context-markers/oauth-working-2025-10-12-143022.md

🔄 To restore this state later:
   Read @.agent/.context-markers/oauth-working-2025-10-12-143022.md

💾 Marker size: ~3k tokens
📊 Current session: ~85k tokens

Tip: You can continue working or use /nav:compact to free up space.
```

---

## Advanced Features

### List All Markers

```bash
/nav:marker list
```

Shows all available markers:

```
📍 Available Context Markers

Recent markers (last 7 days):
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

1. oauth-working-2025-10-12-143022.md
   Created: 2 hours ago
   Task: TASK-123 - OAuth authentication
   Size: 3.2k tokens

2. before-refactor-2025-10-12-091500.md
   Created: 7 hours ago
   Task: TASK-122 - Routing refactor
   Size: 2.8k tokens

3. day1-complete-2025-10-11-170000.md
   Created: yesterday
   Task: TASK-121 - User dashboard
   Size: 3.5k tokens

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Total: 3 markers | Combined size: 9.5k tokens

To restore: Read @.agent/.context-markers/[filename]
To clean up: /nav:marker clean
```

### Clean Old Markers

```bash
/nav:marker clean
```

Interactive cleanup:

```
🧹 Marker Cleanup

Found 15 markers older than 7 days:
- [list with dates and sizes]

Keep only:
1. Last 7 days (recommended)
2. Last 30 days
3. Keep all, just show me
4. Custom selection

Choice [1-4]:
```

### Compare Markers

```bash
/nav:marker diff oauth-working before-refactor
```

Shows what changed between two markers:

```
📊 Marker Comparison

From: before-refactor (7 hours ago)
To: oauth-working (2 hours ago)

Changes:
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Tasks:
  - Completed: TASK-122 (routing refactor)
  + Started: TASK-123 (OAuth auth)

Files Modified:
  + src/auth/oauth.ts (new)
  + src/auth/tokens.ts (new)
  ~ src/routes/auth.ts (modified)

Decisions Made:
  + Using passport.js for OAuth
  + JWT in httpOnly cookies
  + Redis for session storage

Progress: 30% → 70% (task)
```

---

## Marker Strategies

### Checkpoint Strategy

Create markers at natural checkpoints:

```
Feature Planning:
/nav:marker planning-complete

Core Implementation:
/nav:marker core-working

Integration:
/nav:marker integration-done

Testing:
/nav:marker tests-passing

Ready for Review:
/nav:marker ready-for-pr
```

**Benefit**: Clear progression, easy to resume at any stage

### Daily Markers

End each day with a marker:

```bash
/nav:marker eod-2025-10-12 "Finished OAuth, need tests tomorrow"
```

**Benefit**: Perfect context on Monday for Friday's work

### Experiment Markers

Before trying new approaches:

```bash
/nav:marker before-experiment
# Try risky refactor
# Doesn't work?
# Restore from marker, try different approach
```

**Benefit**: Safe exploration, easy rollback

### Decision Markers

After important decisions:

```bash
/nav:marker architecture-decision "Chose PostgreSQL over MongoDB"
```

**Benefit**: Capture why decisions were made with full context

---

## Marker Best Practices

### ✅ Do

- Create markers before breaks (lunch, end of day)
- Name markers descriptively (`oauth-working` not `marker-1`)
- Add descriptions for important markers
- Clean up old markers monthly
- Use markers as conversation save points

### ❌ Don't

- Don't create markers every 5 minutes (too granular)
- Don't use generic names (`test`, `stuff`, `work`)
- Don't forget to clean up (markers accumulate)
- Don't rely solely on markers (still commit code!)

---

## Integration with Navigator Workflow

### Markers + Compact

```
Work on feature → /nav:marker feature-done
Continue to polish → Token usage high
/nav:compact
Result: Marker preserved, conversation cleared
```

**Benefit**: Markers survive compacts

### Markers + Tasks

```
Start task → Load task doc
Make progress → /nav:marker progress-update
Complete → /nav:update-doc feature TASK-XX
```

**Benefit**: Markers complement task documentation

### Markers + SOPs

```
Hit bug → Debug → Solve
/nav:marker bug-solved "Fixed CORS issue with OAuth"
/nav:update-doc sop debugging cors-oauth-fix
```

**Benefit**: Markers capture point-in-time, SOPs capture solution

---

## Technical Implementation

### Marker Storage

```
.agent/.context-markers/
├── oauth-working-2025-10-12-143022.md
├── before-refactor-2025-10-12-091500.md
├── day1-complete-2025-10-11-170000.md
└── .gitkeep
```

**Naming**: `[name]-YYYY-MM-DD-HHMMSS.md`

**Size**: ~3k tokens each

**Git**: Ignored by default (in .gitignore)

### Marker Format

**Required sections**:
- Current Location (task, files, progress)
- What's Done (achievements)
- Technical Decisions (with rationale)
- Next Steps (what's remaining)
- Restore Instructions (how to resume)

**Optional sections**:
- Challenges & Solutions
- Ideas to Explore
- Related Documentation

---

## Examples

### Example 1: End of Day Marker

```bash
You: "Finished implementing user settings page, need to add tests tomorrow"
You: /nav:marker eod-settings-done

Result:
✅ Marker saved: .agent/.context-markers/eod-settings-done-2025-10-12-170000.md

Tomorrow: Read @.agent/.context-markers/eod-settings-done-2025-10-12-170000.md
```

### Example 2: Before Risky Change

```bash
You: "Current routing works. About to refactor to use new router"
You: /nav:marker before-routing-refactor
You: "Refactor the routing system to use express-router"

*After testing...*

You: "The refactor broke auth. Let me restore"
You: Read @.agent/.context-markers/before-routing-refactor.md
You: "Take different approach - migrate gradually"
```

### Example 3: Multi-Day Feature

```bash
Monday:
You: /nav:marker day1-foundation "Built database models and API structure"

Tuesday:
You: Read @.agent/.context-markers/day1-foundation.md
You: *continues work*
You: /nav:marker day2-integration "Integrated with frontend, working on auth"

Wednesday:
You: Read @.agent/.context-markers/day2-integration.md
You: *continues work*
You: /nav:marker day3-complete "Feature complete, tests passing"
```

---

## Success Metrics

**Without markers**:
- Resume after break: 5-10 min re-explaining context
- Session restart: Lose all context
- Risky changes: No safety net
- Multi-day work: Fragmented understanding

**With markers**:
- Resume after break: 30 seconds (read marker)
- Session restart: Full context restored
- Risky changes: Rollback point available
- Multi-day work: Continuous context thread

**Token efficiency**:
- Marker: 3k tokens to restore full context
- Re-explaining: 20-30k tokens of back-and-forth
- **Savings**: 85-90% fewer tokens to resume

---

## Future Enhancements

**Auto-markers**:
```json
{
  "auto_marker": {
    "on_task_complete": true,
    "on_break_detected": true,
    "every_n_hours": 2
  }
}
```

**Marker search**:
```bash
/nav:marker search "OAuth"
# Returns all markers mentioning OAuth
```

**Marker merge**:
```bash
/nav:marker merge day1 day2 day3 → feature-complete
# Combines multiple markers into one
```

---

**Markers transform your AI workflow from stateless to stateful. Never lose context again.** 🎯
