# Try This: Agent-Assisted Search

**Part of**: Navigator v4.0 Education Layer
**Time**: 15 minutes
**Difficulty**: Intermediate
**Goal**: Experience 60-80% token savings from agent searches

---

## What You'll Learn

By the end of this exercise, you'll:
- See the token difference between manual file reading and agent search
- Understand when agents optimize better than direct reads
- Measure preprocessing vs LLM token costs
- Experience the "right tool for the job" principle

---

## Setup

**Prerequisites**:
- Navigator installed in a project
- Codebase with 10+ files
- Completion of [TRY-THIS-LAZY-LOADING.md](./TRY-THIS-LAZY-LOADING.md)

**Starting point**: Fresh Claude Code session

---

## Exercise 1: The Manual Approach (Baseline)

### Step 1: Simulate Manual File Reading

**Scenario**: Find all files that handle user authentication

**Traditional approach** (DON'T DO THIS):
```
1. Use Glob to find potential files
2. Read each file manually
3. Analyze which ones are relevant

find . -name "*auth*" -o -name "*login*" -o -name "*user*"
→ Returns 20 files

Read file 1 (3k tokens)
Read file 2 (4k tokens)
Read file 3 (2k tokens)
... (17 more files)

Total: 60k+ tokens
Time: 10+ minutes
Result: Found 3 relevant files out of 20
```

### Step 2: Calculate Cost

**Token cost**:
```
20 files × 3k average = 60k tokens
Context usage: +30%
Time: 10+ minutes reading files you don't need
Efficiency: 15% (3 relevant files / 20 read)
```

**Problem**:
- Loaded 17 irrelevant files
- Wasted 51k tokens (85%)
- Context window significantly fuller

---

## Exercise 2: The Agent Approach

### Step 1: Start Session

**In Claude Code**:
```
"Start my Navigator session"
```

**Token cost**: ~3k (navigator)

### Step 2: Use Agent Search

**In Claude Code**:
```
"Use an agent to find all files that handle user authentication.
I want to understand the auth flow."
```

**What happens**:
1. Claude Code launches exploration agent
2. Agent searches codebase using optimized strategy
3. Agent reads 20 files (happens in agent's context, not yours)
4. Agent returns summary (3-5k tokens)

**Agent summary example**:
```
Found 3 core authentication files:

1. src/auth/AuthService.ts (main auth logic)
   - Handles login/logout
   - JWT token generation
   - Session management

2. src/auth/middleware.ts (request validation)
   - Token verification
   - Protected route middleware

3. src/models/User.ts (user model)
   - Password hashing
   - User authentication methods

Authentication flow:
1. User submits credentials → AuthService.login()
2. AuthService validates → generates JWT
3. Middleware verifies JWT on protected routes
4. User model handles password operations

17 other files are not core auth (profile management, etc.)
```

**Token cost**: 4k (summary only)

### Step 3: Targeted Loading

**In Claude Code**:
```
"Based on that summary, load AuthService.ts for me"
```

**Token cost**: 3k (one specific file)

**Total tokens used**:
- Navigator: 3k
- Agent summary: 4k
- Specific file: 3k
- **Total**: 10k tokens

### Step 4: Compare Results

| Approach | Tokens | Time | Files Read | Efficiency |
|----------|--------|------|-----------|-----------|
| Manual | 60k | 10+ min | 20 | 15% |
| Agent | 10k | 2 min | 3 (targeted) | 100% |
| **Savings** | **50k (83%)** | **8 min** | **17 fewer** | **85% better** |

---

## Exercise 3: Preprocessing Pattern

### Step 5: Deterministic Search

**Scenario**: Count how many times a function is called

**In Claude Code**:
```
"How many times is the getCwd() function called in this codebase?"
```

**What happens**:
1. Claude Code uses Grep tool (preprocessing)
2. Tool searches all files instantly
3. Returns count and locations

**Example output**:
```
Found 15 occurrences of getCwd():
- src/utils/file.ts: 5 times
- src/services/process.ts: 3 times
- src/commands/init.ts: 7 times
```

**Token cost**: ~0 (tool execution, not LLM processing)

### Step 6: Compare to LLM Approach

**If using pure LLM** (DON'T DO THIS):
```
Load all .ts files → Ask Claude to count getCwd() calls

Files to load: 50+ TypeScript files
Token cost: 150k+ tokens
Accuracy: 85-90% (may miss edge cases)
Time: 15+ minutes
```

**Using preprocessing tool**:
```
Grep tool execution
Token cost: ~0
Accuracy: 100%
Time: <1 second
```

**Savings**: 150k tokens (100%), instant, more accurate

---

## Exercise 4: Hybrid Pattern

### Step 7: Extract + Interpret

**Scenario**: Analyze API endpoints and suggest optimizations

**Phase 1: Preprocessing (Extract)**

**In Claude Code**:
```
"Use grep to find all API endpoint definitions in this project"
```

**Grep result**:
```
src/routes/users.ts:10: router.get('/users', getUsers);
src/routes/users.ts:15: router.post('/users', createUser);
src/routes/auth.ts:8: router.post('/login', login);
src/routes/auth.ts:12: router.post('/logout', logout);
... (20 more endpoints)
```

**Token cost**: ~1k (structured list)

**Phase 2: LLM (Interpret)**

**In Claude Code**:
```
"Based on these endpoints, suggest rate limiting strategy"
```

**Claude analysis**:
```
Rate limiting recommendations:

1. POST /login - Strict: 5 attempts/15min (brute force protection)
2. POST /users - Moderate: 10/hour (prevent spam)
3. GET /users - Lenient: 100/hour (read-heavy)
4. POST /logout - Lenient: 20/hour (low risk)

Suggested implementation:
- Use express-rate-limit middleware
- Configure per-route limits
- Add Redis for distributed rate limiting
```

**Token cost**: 3k (semantic analysis)

**Total cost**:
- Phase 1 (preprocessing): 1k
- Phase 2 (LLM): 3k
- **Total**: 4k tokens

### Step 8: Compare to Pure LLM

**Pure LLM approach** (DON'T DO THIS):
```
Load all route files → Ask Claude to extract endpoints and suggest limits

Files to load: 10 route files
Token cost: 30k (files) + 5k (analysis) = 35k
Accuracy: 90% (may miss some endpoints)
```

**Hybrid approach**:
```
Grep extracts endpoints → Claude analyzes

Token cost: 4k tokens
Accuracy: 100% (grep is exhaustive)
```

**Savings**: 31k tokens (88%)

---

## Exercise 5: Real-World Scenario

### Step 9: Understanding Unfamiliar Codebase

**Scenario**: You join new project, need to understand architecture

**❌ Wrong Approach**:
```
1. Glob for all files
2. Read 50+ files manually
3. Try to piece together architecture

Token cost: 150k+ tokens
Context: Overloaded
Result: Overwhelmed, unclear picture
```

**✅ Right Approach with Agent**:

**In Claude Code**:
```
"Use an agent to explain the architecture of this codebase.
I want to understand:
1. Main entry point
2. Key components
3. Data flow
4. External dependencies"
```

**Agent explores** (in its own context):
- Reads 50+ files
- Identifies patterns
- Traces data flow
- Maps dependencies

**Agent returns summary**:
```
Architecture Overview (4k tokens):

Entry Point: src/index.ts
├── Initializes Express server
├── Loads middleware (auth, logging, error handling)
└── Mounts route modules

Key Components:
├── Auth System (src/auth/) - JWT-based
├── Database Layer (src/models/) - Mongoose/MongoDB
├── Business Logic (src/services/) - Core features
└── API Routes (src/routes/) - RESTful endpoints

Data Flow:
Request → Middleware → Route → Service → Model → Database

External Dependencies:
- Express (web framework)
- Mongoose (MongoDB ORM)
- JWT (authentication)
- Winston (logging)

Key Files to Read for Details:
- src/auth/AuthService.ts (auth logic)
- src/services/UserService.ts (business logic example)
- src/models/User.ts (data model example)
```

**Token cost**: 4k (summary)

### Step 10: Deep Dive on Demand

**Now load specific files for details**:

**In Claude Code**:
```
"Load the AuthService.ts file"
```

**Token cost**: 3k

**Total for comprehensive understanding**:
- Agent summary: 4k
- 1-2 specific files: 6k
- **Total**: 10k tokens

**vs Manual reading**:
- 50+ files: 150k tokens
- **Savings**: 140k tokens (93%)

---

## Exercise 6: Measure Your Results

### Step 11: Check Session Statistics

**In Claude Code**:
```
"Show me my session statistics"
```

**Expected output**:
```
Session Efficiency Report
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Agent searches:          3 used
Manual file reads saved: ~47 files (141k tokens)

Documentation loaded:    10k tokens
Context usage:           38% (excellent)
Efficiency score:        96/100

Time saved this session: ~28 minutes
```

### Step 12: Calculate Your Savings

**Without agents**:
```
Files you would have read manually: 47
Average file size: 3k tokens
Total tokens: 141k
Context usage: 85% (nearly full)
Time: 25+ minutes
```

**With agents**:
```
Agent searches: 3
Token cost: 12k (3 summaries × 4k)
Context usage: 38% (healthy)
Time: 5 minutes
```

**Your savings**:
```
Tokens saved: 129k (91%)
Time saved: 20 minutes
Context efficiency: 2.2x better
Session extension: 3x longer possible
```

---

## Key Takeaways

### When Agents Excel

✅ **Multi-file exploration**
- Need to understand patterns across 10+ files
- Agent reads all, returns summary
- Savings: 85-95%

✅ **Unfamiliar codebases**
- Don't know where to start
- Agent explores and maps architecture
- Saves: Hours of manual exploration

✅ **Pattern discovery**
- "Find all files using pattern X"
- Agent searches exhaustively
- Returns: Relevant subset only

✅ **Architecture understanding**
- How components interact
- Agent traces data flow
- Returns: High-level picture

### When to Use Direct Reads

✅ **Specific known file** (1-2 files)
- You know exactly what you need
- Read tool more efficient
- Cost: 3-6k tokens

✅ **Already loaded context**
- File already in conversation
- No need to re-read

✅ **Small scope**
- 2-3 related files
- Direct reading is fine

### When to Use Preprocessing

✅ **Deterministic searches**
- Count occurrences
- Find patterns (regex)
- List files
- Cost: 0 tokens (tool execution)

✅ **Structured data extraction**
- Parse JSON/YAML
- Extract API schemas
- List dependencies
- Cost: 0 tokens

✅ **Math/calculations**
- Count files
- Calculate averages
- Sum values
- Cost: 0 tokens

---

## Decision Matrix

```
How many files involved?
├── 1-2 files → Read directly (3-6k)
├── 3-10 files → Use agent (3-5k summary)
└── 10+ files → Use agent (4-6k summary)

Is the task deterministic?
├── Yes → Use preprocessing tools (0 tokens)
└── No → Use agent or LLM (3-10k)

Do you know what you're looking for?
├── Yes (specific file) → Read directly
├── No (exploration) → Use agent
└── Maybe (pattern) → Use preprocessing + agent
```

---

## Common Mistakes

### Mistake 1: Reading Files Without Agent

**Symptom**: Loading 10+ files manually

**Fix**: Use agent: "Find files related to [topic]"

**Savings**: 85-95%

### Mistake 2: Using Agent for 1 File

**Symptom**: "Use agent to understand AuthService.ts"

**Fix**: "Read AuthService.ts" (more efficient)

**Why**: Agent overhead not worth it for single file

### Mistake 3: LLM for Deterministic Tasks

**Symptom**: "Count how many times X appears"

**Fix**: Use Grep tool (0 tokens, 100% accuracy)

**Savings**: 100%

### Mistake 4: Not Leveraging Agent Summaries

**Symptom**: Agent returns summary → You re-read files anyway

**Fix**: Trust agent summary, only load 1-2 specific files if needed

**Savings**: 70-90%

---

## Variations to Try

### Variation 1: Comparative Analysis

**Scenario**: Compare two implementations

```
"Use agent to compare authentication implementation in auth-v1/ vs auth-v2/
What are the key differences?"

Agent reads both implementations, returns comparison (5k)
vs Reading all files manually (40k)
Savings: 88%
```

### Variation 2: Dependency Tracing

**Scenario**: Understand what uses a specific function

```
"Use agent to find all places that call getUserProfile()
and explain the different use cases"

Agent searches codebase, categorizes uses, returns summary (4k)
vs Manual grep + reading each file (50k)
Savings: 92%
```

### Variation 3: Migration Analysis

**Scenario**: Plan migration from old API to new API

```
"Use agent to find all files using the old API endpoints
and estimate migration complexity"

Agent identifies files, assesses complexity, returns report (6k)
vs Reading each file and manually tracking (80k)
Savings: 93%
```

---

## Next Steps

### Try More Exercises

- **[TRY-THIS-MARKERS.md](./TRY-THIS-MARKERS.md)** - Context compression
- **[TRY-THIS-LAZY-LOADING.md](./TRY-THIS-LAZY-LOADING.md)** - Lazy loading basics

### Deep Dive into Theory

- **[PREPROCESSING-VS-LLM.md](../PREPROCESSING-VS-LLM.md)** - Full right-tool principle
- **[TOKEN-OPTIMIZATION.md](../TOKEN-OPTIMIZATION.md)** - Complete strategies

### Apply to Your Work

1. Next time you need to explore code, try agent first
2. Measure token savings in your session stats
3. Share results with team
4. Document patterns you discover

---

## Success Criteria

You've mastered agent-assisted search when:

- [ ] You use agents for 5+ file explorations automatically
- [ ] You achieve 80%+ token savings vs manual reads
- [ ] You can explain when to use agent vs direct read
- [ ] Your context usage stays below 60% even with exploration
- [ ] You combine preprocessing + agents for best results

**Congratulations! You now understand how to explore codebases efficiently.**
