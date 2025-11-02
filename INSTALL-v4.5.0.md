# Installing Navigator v4.5.0

**For users wanting to upgrade to the latest version with multi-Claude reliability improvements.**

---

## Prerequisites

- Claude Code CLI installed ([install.claude.com](https://install.claude.com))
- Git installed
- Terminal access

---

## Installation Methods

### Method 1: Fresh Install (Recommended for New Users)

```bash
# 1. Clone the repository
git clone https://github.com/alekspetrov/navigator.git
cd navigator

# 2. Checkout v4.5.0
git checkout v4.5.0

# 3. Install via Claude Code
# (From your project directory, not Navigator directory)
cd /path/to/your/project
claude plugin install /path/to/navigator

# 4. Verify installation
claude plugin list | grep navigator
# Should show: navigator (4.5.0)
```

---

### Method 2: Upgrade from Previous Version

**If you have Navigator v4.3.1 or earlier:**

```bash
# 1. Navigate to your project directory
cd /path/to/your/project

# 2. Update Navigator plugin
claude plugin update navigator

# 3. Verify new version
claude plugin list | grep navigator
# Should show: navigator (4.5.0)

# 4. Update your project's CLAUDE.md
# Start new Claude session and run:
# "Update my Navigator configuration to v4.5.0"
# Or use skill (if available):
# /nav:update-claude
```

---

### Method 3: Manual Git Update (For Development)

```bash
# 1. Navigate to Navigator installation directory
cd ~/.claude/plugins/navigator  # Or your installation path

# 2. Fetch latest changes
git fetch origin

# 3. Checkout v4.5.0
git checkout v4.5.0

# 4. Verify
git describe --tags
# Should show: v4.5.0

# 5. Restart Claude Code if running
# The plugin will reload automatically
```

---

## Verify Installation

```bash
# Check plugin version
claude plugin list | grep navigator

# Expected output:
# navigator (4.5.0) - Context-Efficient AI Development Framework

# Check available skills (optional)
claude plugin info navigator
```

---

## What's New in v4.5.0

**Multi-Claude Workflow Reliability**: 30% → 90%+ success rate

**New Features**:
1. **Automatic retry logic** - Phases retry on marker timeout
2. **Timeout monitoring** - Sub-Claude processes monitored for hangs
3. **State persistence** - Workflow state saved for recovery
4. **Resume capability** - Continue interrupted workflows
5. **Enhanced verification** - Marker validation with central logging
6. **Improved prompts** - Explicit marker instructions

**New Scripts**:
- `scripts/sub-claude-monitor.sh` - Timeout detection
- `scripts/resume-workflow.sh` - Workflow recovery
- `tests/test-*.sh` - Test suite for reliability

**See full details**: [RELEASE-NOTES-v4.5.0.md](RELEASE-NOTES-v4.5.0.md)

---

## Testing the Installation

### Quick Test: Run Multi-Claude POC

```bash
# Navigate to Navigator directory
cd /path/to/navigator

# Run simple test workflow
./scripts/navigator-multi-claude-poc.sh "Add a hello world function to utils.js"

# Expected behavior:
# - Phase 1 (Planning): Creates plan file
# - Phase 2 (Implementation): Creates function
# - Phase 3 (Testing): Generates tests
# - Phase 4 (Documentation): Adds docs
# - Phase 5 (Review): Reviews implementation

# If workflow completes successfully, v4.5.0 is working correctly
```

### Test Retry Logic

```bash
# This will test if retry mechanism works when markers timeout
# (Simulated failure - for testing only)

cd /path/to/navigator

# Run test suite
chmod +x tests/test-*.sh
./tests/test-retry-logic.sh
./tests/test-monitor.sh

# All tests should pass
```

---

## Post-Installation: Update Your CLAUDE.md

**Important**: Your project's `CLAUDE.md` should match the Navigator version.

**Automatic update** (recommended):
```bash
# In your project directory
# Start new Claude session and say:
"Update my Navigator configuration to match plugin version"

# This will:
# 1. Detect installed Navigator version (4.5.0)
# 2. Fetch matching CLAUDE.md template from GitHub
# 3. Preserve your customizations
# 4. Update to v4.5.0 template
```

**Manual update** (if automatic fails):
```bash
# Copy template from Navigator installation
cp /path/to/navigator/templates/CLAUDE.md /path/to/your/project/CLAUDE.md

# Or download from GitHub
curl -o CLAUDE.md https://raw.githubusercontent.com/alekspetrov/navigator/v4.5.0/templates/CLAUDE.md
```

---

## Troubleshooting

### Issue: Plugin not found

```bash
# Verify plugin installed
claude plugin list

# If not listed, install manually:
claude plugin install https://github.com/alekspetrov/navigator.git
```

### Issue: Version shows 4.3.1 after update

```bash
# Uninstall old version
claude plugin uninstall navigator

# Install fresh v4.5.0
git clone https://github.com/alekspetrov/navigator.git /tmp/navigator-v4.5.0
cd /tmp/navigator-v4.5.0
git checkout v4.5.0
claude plugin install /tmp/navigator-v4.5.0

# Verify
claude plugin list | grep navigator
```

### Issue: Multi-Claude workflows still failing

```bash
# Check marker log for errors
tail -50 .agent/.marker-log

# Review state file if workflow interrupted
ls -la .agent/tasks/*-state.json

# Resume interrupted workflow
./scripts/resume-workflow.sh {session-id}
```

---

## Rollback to Previous Version

If you encounter issues with v4.5.0:

```bash
# Method 1: Via plugin
claude plugin uninstall navigator
git clone https://github.com/alekspetrov/navigator.git /tmp/navigator-v4.3.1
cd /tmp/navigator-v4.3.1
git checkout v4.3.1
claude plugin install /tmp/navigator-v4.3.1

# Method 2: Manual git
cd ~/.claude/plugins/navigator
git checkout v4.3.1
# Restart Claude Code
```

---

## Next Steps

1. **Read release notes**: See [RELEASE-NOTES-v4.5.0.md](RELEASE-NOTES-v4.5.0.md) for full feature details

2. **Try multi-Claude workflow**: Test the improved reliability
   ```bash
   ./scripts/navigator-multi-claude-poc.sh "Your feature description"
   ```

3. **Explore new scripts**:
   - `scripts/sub-claude-monitor.sh` - Understand timeout monitoring
   - `scripts/resume-workflow.sh` - Learn workflow recovery
   - `tests/` - Review test suite

4. **Check Navigator documentation**: `.agent/DEVELOPMENT-README.md`

---

## Support

**Issues**: https://github.com/alekspetrov/navigator/issues
**Release**: https://github.com/alekspetrov/navigator/releases/tag/v4.5.0
**Docs**: `.agent/DEVELOPMENT-README.md` (after installation)

---

**Last Updated**: 2025-11-02
**Navigator Version**: 4.5.0
