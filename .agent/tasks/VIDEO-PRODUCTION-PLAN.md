# Navigator Video Production Plan

**Created**: 2025-11-02
**Platform**: YouTube
**Format**: Engineering educational + product overview
**Style**: Technical screencast, no-nonsense, engineering-focused
**Target Length**: 8-12 minutes

---

## Research Findings

### Successful Engineering Video Patterns

**Channels that work** (Fireship, Traversy Media, Tech With Tim):
- Clear problem statement upfront
- Concise, information-dense content
- Live coding/terminal demos
- Real-world examples
- Practical outcomes shown

**Best practices for developer tools**:
- 60 seconds intro (problem)
- 2-3 minutes core demo
- 3-5 minutes deep dive
- 1-2 minutes results/recap
- No fluff, straight to value

**Avoid**:
- Marketing speak
- Long introductions
- Unclear benefits
- Abstract concepts without examples

---

## Video Structure (8-12 min total)

### Part 1: The Problem (90 sec)

**Hook** (0:00-0:15):
```
"I hit context limits in 7 exchanges. Claude forgot code I just wrote.
150k tokens loaded. 8k used. 94% wasted."
```

**Show terminal**:
- Real session stats (OpenTelemetry metrics)
- Context limit error message
- Token usage breakdown

**Problem statement** (0:15-0:45):
```
"The default approach—bulk loading docs—kills AI sessions.
Loading 150k tokens upfront means:
- Context 75% full before you start
- AI overwhelmed, signal lost in noise
- Sessions die in 5-7 exchanges
```

**Why this matters** (0:45-1:30):
```
"Context engineering ≠ Prompt engineering.
Anthropic's docs: Load strategically, not everything.
Navigator implements this for your codebase."
```

**Visual**: Split screen showing bulk loading vs strategic loading diagram

---

### Part 2: The Solution (2-3 min)

**Overview** (1:30-2:00):
```
"Navigator: Context-efficient AI development.
92% token savings. OpenTelemetry verified.
Sessions last 20+ exchanges instead of 5-7."
```

**Show architecture** (2:00-3:30):
- Navigator index (2k tokens) - map of what exists
- Load on-demand, not upfront
- Real session: 12k loaded vs 150k available
- Terminal showing token metrics

**Visual**: Live demo in terminal
- Show `.agent/` structure
- Display token counts
- Compare before/after metrics

---

### Part 3: Live Demo - Real Example (5-7 min)

**Setup** (3:30-4:00):
```
"Real example: Add multi-Claude workflow reliability.
TASK-25: 30% → 90% success rate.
Let me show you how Navigator guided this."
```

**Demo flow** (4:00-10:00):

**Step 1: Session start** (1 min)
```bash
# Terminal commands visible
$ claude

> "Start my Navigator session"

# Show:
- DEVELOPMENT-README.md loads (2k tokens)
- Task index displayed
- Context usage: 2k/200k (1%)
```

**Step 2: Task selection** (1 min)
```
> "Implement TASK-25"

# Show:
- Task doc loads (3k tokens)
- Context now: 5k/200k (2.5%)
- Still 97.5% free for work
```

**Step 3: Implementation** (2-3 min)
```
# Show real implementation
- Code being written
- Tests being created
- Token usage staying low
- Context window efficient
```

**Step 4: Multi-Claude workflow** (2 min)
```bash
$ ./scripts/navigator-multi-claude-poc.sh "Implement TASK-25"

# Show phases:
- Planning (marker created ✅)
- Implementation (marker created ✅)
- Testing (retry logic kicks in)
- Documentation
- Review (dogfooding test shown)
```

**Highlight key moments**:
- Retry logic activating (show logs)
- State persistence (show JSON file)
- Workflow resume (show recovery)
- Review phase completion

---

### Part 4: Results & Deep Dive (2-3 min)

**Metrics shown** (10:00-11:00):
```
Before Navigator:
- 150k tokens loaded upfront
- 5-7 exchanges before crash
- Multi-Claude: 30% success rate

After Navigator:
- 12k tokens loaded (92% savings)
- 20+ exchanges per session
- Multi-Claude: 90% success rate
```

**Show Grafana dashboard** (if available):
- Token savings over time
- Session length improvements
- Success rate metrics

**Quick architecture walkthrough** (11:00-12:00):
```
.agent/
├── DEVELOPMENT-README.md  (Navigator - loads first)
├── tasks/                  (On-demand)
├── system/                 (When needed)
└── sops/                   (If relevant)

Lazy loading saves 92% of context for actual work.
```

---

### Part 5: Recap & Next Steps (1 min)

**Summary** (12:00-12:30):
```
Navigator:
- Context engineering for your codebase
- 92% token savings (verified)
- Multi-Claude workflows that actually work
- Open source, MIT license
```

**Call to action** (12:30-13:00):
```
Try it yourself:
1. Install: claude plugin install navigator
2. Initialize: /nav:init
3. Start session: "Start my Navigator session"

Links in description:
- GitHub: github.com/alekspetrov/navigator
- Docs: DEVELOPMENT-README.md
- Release notes: v4.5.0
```

---

## Production Plan

### Phase 1: Preparation (Week 1)

**Technical setup**:
- [ ] Screen recording software (OBS Studio or ScreenFlow)
- [ ] Terminal setup (clean theme, visible font)
- [ ] Audio recording (USB mic or laptop)
- [ ] Test project prepared

**Content prep**:
- [ ] Script finalized
- [ ] Test workflow validated (TASK-25 example)
- [ ] Grafana dashboard ready (if showing metrics)
- [ ] Terminal commands scripted

**Example preparation**:
- [ ] Clean Navigator installation
- [ ] Fresh test project
- [ ] TASK-25 ready to demonstrate
- [ ] Multi-Claude POC workflow tested

---

### Phase 2: Recording (Week 2)

**Recording sessions**:

**Session 1: Problem/Solution (Part 1-2)**
- Record terminal showing token waste
- Record Navigator overview
- Record architecture walkthrough
- Time: 3-4 hours (including retakes)

**Session 2: Live Demo (Part 3)**
- Record TASK-25 implementation
- Record multi-Claude workflow
- Record retry/recovery features
- Time: 4-6 hours (multiple takes expected)

**Session 3: Results/Recap (Part 4-5)**
- Record metrics/dashboard
- Record summary
- Record call to action
- Time: 2-3 hours

**Recording tips**:
- Do dry runs first
- Record in segments (easier editing)
- Keep terminal commands visible
- Speak naturally, not reading script
- Show real outcomes, not staged demos

---

### Phase 3: Editing (Week 3)

**Editing workflow**:
- [ ] Import all recordings
- [ ] Cut dead air / mistakes
- [ ] Add transitions between sections
- [ ] Add text overlays for key points
- [ ] Add timestamps for chapters
- [ ] Export 1080p60 (or 4K if source supports)

**Tools**:
- DaVinci Resolve (free, professional)
- iMovie (if Mac, simple)
- Camtasia (good for screencasts)

**Editing guidelines**:
- Keep pace fast (engineering audience)
- Cut aggressively (no dead time)
- Add captions for technical terms
- Highlight terminal output when relevant

---

### Phase 4: Publishing (Week 4)

**YouTube upload**:

**Title options**:
1. "Navigator: 92% Token Savings for Claude Code (Verified)"
2. "Context Engineering: How I Fixed Claude Code Sessions"
3. "Building Reliable Multi-Claude Workflows (30% → 90%)"

**Description template**:
```
Navigator: Context-efficient AI development for your codebase.

PROBLEM: Bulk loading docs wastes 94% of context window. Sessions crash in 5-7 exchanges.

SOLUTION: Strategic lazy loading. Load what you need, when you need it.

RESULTS:
• 92% token savings (OpenTelemetry verified)
• 20+ exchanges per session (vs 5-7)
• Multi-Claude workflows: 90% success rate (vs 30%)

TIMESTAMPS:
0:00 The Problem
1:30 The Solution
3:30 Live Demo: TASK-25
10:00 Results & Metrics
12:00 Next Steps

LINKS:
• GitHub: https://github.com/alekspetrov/navigator
• Install: claude plugin install navigator
• Docs: .agent/DEVELOPMENT-README.md
• Release v4.5.0: [link]

#AI #ClaudeCode #ContextEngineering #DeveloperTools
```

**Thumbnail ideas**:
- Split screen: "150k loaded" vs "12k loaded"
- Before/after session length
- "92% savings" big text
- Terminal screenshot with metrics

**Tags**:
- Claude Code
- AI coding assistant
- Context engineering
- Developer tools
- Productivity
- Multi-Claude
- Token optimization

---

## Test Examples for Demo

### Example 1: TASK-25 (Primary - Already Done)

**Perfect because**:
- Real implementation (not staged)
- Shows all features (retry, recovery, monitoring)
- Dogfooding (multi-Claude implementing itself)
- Actual failure mode demonstrated
- Review phase tested and completed

**Demo flow**:
1. Show TASK-25 in `.agent/tasks/`
2. Run multi-Claude workflow
3. Show Phase 1 (planning) success
4. Show Phase 2 (implementation) timeout
5. Show retry logic kicking in
6. Show state file created
7. Show resume workflow capability
8. Show review phase completion

**Outcome to show**:
- 5 new scripts created
- 3 scripts modified
- Comprehensive review (8.5/10)
- v4.5.0 shipped

---

### Example 2: Simple POC (Backup - If TASK-25 Too Complex)

**Task**: "Add health check endpoint to Express server"

**Why simpler**:
- Easier to follow
- Faster workflow
- Clear outcome
- Shows all phases

**Demo flow**:
1. Show empty project
2. Run POC workflow
3. Show all 5 phases completing
4. Show final code
5. Run tests
6. Review output

**Time**: 5-7 minutes (vs 10+ for TASK-25)

---

### Example 3: Context Efficiency Demo

**Task**: Show token savings in real session

**Demo**:
1. Start without Navigator (show 150k loaded)
2. Session crashes after 7 exchanges
3. Restart with Navigator
4. Show 12k loaded
5. Complete 20+ exchanges
6. Show Grafana metrics

**Visual**: Side-by-side comparison

---

## Success Metrics

**Video goals**:
- [ ] Views: 1,000+ in first month
- [ ] Engagement: 5%+ like ratio
- [ ] Comments: Positive technical feedback
- [ ] GitHub: 20+ stars from video traffic
- [ ] Installs: 50+ plugin installs attributed to video

**Audience**:
- Professional developers
- Claude Code users
- AI tooling enthusiasts
- Engineering managers

**Value proposition**:
"See exactly how to save 92% of context window with real code, real metrics, real outcomes."

---

## Resources Needed

**Software** (all free options available):
- Screen recorder: OBS Studio (free)
- Video editor: DaVinci Resolve (free)
- Audio editor: Audacity (free)

**Hardware** (minimum):
- MacBook with decent screen resolution
- USB microphone (Blue Yeti, ~$100) or built-in
- Quiet recording space

**Assets**:
- Navigator v4.5.0 installed
- Test project ready
- TASK-25 prepared
- Terminal configured (readable font/theme)

**Time estimate**:
- Preparation: 8-12 hours
- Recording: 10-15 hours
- Editing: 15-20 hours
- Publishing: 2-3 hours
- **Total**: 35-50 hours over 4 weeks

---

## Next Steps

1. **Commit this plan** to `.agent/tasks/VIDEO-PRODUCTION-PLAN.md`
2. **Set timeline**: Target publish date 4 weeks from start
3. **Prepare test environment**: Clean Navigator installation
4. **Script writing**: Expand outline into full script
5. **Dry run**: Test TASK-25 workflow end-to-end
6. **Start recording**: Begin with simplest section first

**Priority**: High (marketing asset for v4.5.0 launch)
**Owner**: Navigator maintainer
**Status**: Planning complete, ready to execute

---

**Created**: 2025-11-02
**Last Updated**: 2025-11-02
**Version**: 1.0
