# Version Management - Standard Operating Procedure

**Category**: Development
**Created**: 2025-10-13
**Last Updated**: 2025-10-13

---

## Context

This SOP ensures version numbers stay consistent across all files during releases. Version drift creates user confusion and erodes documentation trust.

**Problem**: Version references scattered across 7+ locations
**Solution**: Single source of truth + automated checklist
**Result**: Zero version drift

---

## When to Use

Use this SOP:
- Before every plugin release (patch, minor, major)
- When updating version references
- To audit version consistency
- When onboarding contributors to release process

---

## Single Source of Truth

**Primary**: `.claude-plugin/marketplace.json`

```json
{
  "metadata": {
    "version": "1.5.0"  // ← SSOT
  },
  "plugins": [
    {
      "version": "1.5.0"  // ← Must match metadata.version
    }
  ]
}
```

**All other files reference this version**.

---

## Version Reference Map

| File | Location | Format | Update Frequency |
|------|----------|--------|------------------|
| `marketplace.json` | `metadata.version` | `"1.5.0"` | Every release |
| `marketplace.json` | `plugins[0].version` | `"1.5.0"` | Every release |
| `README.md` | Line ~5 (status) | `v1.5.0` | Every release |
| `README.md` | Line ~8 (badge) | `1.5.0` | Every release |
| `README.md` | Line ~435 (roadmap) | `v1.5.0` | Every release |
| `README.md` | Line ~506 (footer) | `1.5.0` | Every release |
| `DEVELOPMENT-README.md` | Bottom | `(v1.5.0)` | Every release |
| Git tag | Tag name | `v1.5.0` | Every release |
| GitHub release | Release version | `v1.5.0` | Every release |

**Total**: 9 locations must match

---

## Pre-Release Version Sync Checklist

**Run this checklist BEFORE making any release commits**.

### 1. Determine New Version

```bash
# Check current version
cat .claude-plugin/marketplace.json | jq -r '.metadata.version'

# Determine bump type:
# - Patch (1.5.0 → 1.5.1): Bug fixes only
# - Minor (1.5.0 → 1.6.0): New features, backward compatible
# - Major (1.5.0 → 2.0.0): Breaking changes
```

**Set target version**:
```bash
NEW_VERSION="1.6.0"  # Update this value
```

### 2. Update All Version References

**Files to update** (use NEW_VERSION from above):

#### File 1: `.claude-plugin/marketplace.json` (2 locations)

```json
{
  "metadata": {
    "version": "1.6.0"  // ← Update here
  },
  "plugins": [
    {
      "version": "1.6.0"  // ← And here
    }
  ]
}
```

#### File 2: `README.md` (4 locations)

```markdown
# Line ~5
**Status**: ✅ Published v1.6.0

# Line ~8
[![Version](https://img.shields.io/badge/version-1.6.0-blue.svg)]

# Line ~435 (roadmap section)
- v1.6.0 published

# Line ~506 (footer)
**Version**: 1.6.0
**Last Updated**: 2025-10-XX  # Update date too
```

#### File 3: `.agent/DEVELOPMENT-README.md` (1 location)

```markdown
# Bottom of file
**Last Updated**: 2025-10-XX (v1.6.0)
```

### 3. Verify Consistency (Audit Script)

**Run this script to verify all references match**:

```bash
#!/bin/bash
# Save as: scripts/audit-version.sh

NEW_VERSION="1.6.0"  # Set your target version

echo "🔍 Auditing version consistency for v${NEW_VERSION}..."
echo ""

ERRORS=0

# Check marketplace.json (metadata)
echo "Checking .claude-plugin/marketplace.json (metadata.version)..."
RESULT=$(jq -r '.metadata.version' .claude-plugin/marketplace.json)
if [ "$RESULT" = "$NEW_VERSION" ]; then
  echo "✅ metadata.version: $RESULT"
else
  echo "❌ metadata.version: $RESULT (expected: $NEW_VERSION)"
  ERRORS=$((ERRORS + 1))
fi

# Check marketplace.json (plugins)
echo "Checking .claude-plugin/marketplace.json (plugins[0].version)..."
RESULT=$(jq -r '.plugins[0].version' .claude-plugin/marketplace.json)
if [ "$RESULT" = "$NEW_VERSION" ]; then
  echo "✅ plugins[0].version: $RESULT"
else
  echo "❌ plugins[0].version: $RESULT (expected: $NEW_VERSION)"
  ERRORS=$((ERRORS + 1))
fi

# Check README.md (status)
echo "Checking README.md (status line)..."
if grep -q "Published v${NEW_VERSION}" README.md; then
  echo "✅ Status line contains v${NEW_VERSION}"
else
  echo "❌ Status line missing v${NEW_VERSION}"
  ERRORS=$((ERRORS + 1))
fi

# Check README.md (badge)
echo "Checking README.md (badge)..."
if grep -q "version-${NEW_VERSION}-blue" README.md; then
  echo "✅ Badge contains version-${NEW_VERSION}"
else
  echo "❌ Badge missing version-${NEW_VERSION}"
  ERRORS=$((ERRORS + 1))
fi

# Check README.md (roadmap)
echo "Checking README.md (roadmap)..."
if grep -q "v${NEW_VERSION} published" README.md; then
  echo "✅ Roadmap contains v${NEW_VERSION} published"
else
  echo "❌ Roadmap missing v${NEW_VERSION} published"
  ERRORS=$((ERRORS + 1))
fi

# Check README.md (footer)
echo "Checking README.md (footer version)..."
if grep -q "^\*\*Version\*\*: ${NEW_VERSION}" README.md; then
  echo "✅ Footer contains Version: ${NEW_VERSION}"
else
  echo "❌ Footer missing Version: ${NEW_VERSION}"
  ERRORS=$((ERRORS + 1))
fi

# Check DEVELOPMENT-README.md
echo "Checking .agent/DEVELOPMENT-README.md..."
if grep -q "(v${NEW_VERSION})" .agent/DEVELOPMENT-README.md; then
  echo "✅ DEVELOPMENT-README contains (v${NEW_VERSION})"
else
  echo "❌ DEVELOPMENT-README missing (v${NEW_VERSION})"
  ERRORS=$((ERRORS + 1))
fi

echo ""
if [ $ERRORS -eq 0 ]; then
  echo "🎉 All version references consistent! Ready to commit."
  exit 0
else
  echo "⚠️  Found $ERRORS version mismatch(es). Fix before committing!"
  exit 1
fi
```

**Quick audit** (manual):

```bash
# Set your target version
NEW_VERSION="1.6.0"

# Check all references
echo "marketplace.json (metadata):"
jq -r '.metadata.version' .claude-plugin/marketplace.json

echo "marketplace.json (plugins):"
jq -r '.plugins[0].version' .claude-plugin/marketplace.json

echo "README.md references:"
grep -E "Published v|version-.*-blue|v[0-9]+\.[0-9]+\.[0-9]+ published|^\*\*Version\*\*:" README.md

echo "DEVELOPMENT-README.md:"
grep -E "\(v[0-9]+\.[0-9]+\.[0-9]+\)" .agent/DEVELOPMENT-README.md
```

### 4. Commit Version Bump

**After all references match, commit separately**:

```bash
git add .claude-plugin/marketplace.json README.md .agent/DEVELOPMENT-README.md
git commit -m "chore: bump version to v1.6.0

Prepare for v1.6.0 release. Updated version references in:
- marketplace.json (metadata + plugins)
- README.md (status, badge, roadmap, footer)
- DEVELOPMENT-README.md (footer)

🤖 Generated with [Claude Code](https://claude.com/claude-code)

Co-Authored-By: Claude <noreply@anthropic.com>"
```

---

## Post-Release Checklist

**After feature commits are done**:

- [ ] Create Git tag: `git tag -a v1.6.0 -m "Version 1.6.0: Description"`
- [ ] Push commit: `git push origin main`
- [ ] Push tag: `git push origin v1.6.0`
- [ ] Create GitHub release with notes
- [ ] Verify badge renders correctly (may take 5-10 min for cache)
- [ ] Test installation in fresh project

---

## Semantic Versioning Guide

### Patch (1.5.0 → 1.5.1)

**When to use**:
- Bug fixes only
- Typo corrections
- Documentation fixes
- No new features
- No breaking changes

**Examples**:
- Fix template syntax error
- Correct typo in README
- Fix broken link in docs

### Minor (1.5.0 → 1.6.0)

**When to use**:
- New features
- New commands
- Backward compatible changes
- Enhanced functionality
- No breaking changes

**Examples**:
- Add new `/nav:markers` command
- Add auto-resume feature
- Enhance existing command output
- Add new template option

### Major (1.5.0 → 2.0.0)

**When to use**:
- Breaking changes
- API changes requiring user action
- Command renames or removals
- File structure changes
- Configuration schema changes

**Examples**:
- Rename `/nav:init` to `/nav:setup`
- Change `.agent/` folder structure
- Remove deprecated command
- Change config file format

---

## Troubleshooting

### Issue: Version Mismatch Detected

**Symptoms**: Audit script shows different versions across files

**Solution**:
1. Identify which files are out of sync
2. Determine correct version (from `marketplace.json`)
3. Update all mismatched files manually
4. Re-run audit script
5. Commit fix separately with `chore:` prefix

### Issue: Badge Not Rendering

**Symptoms**: Version badge shows old version or 404

**Solutions**:
1. Check README.md badge URL format:
   ```markdown
   [![Version](https://img.shields.io/badge/version-1.6.0-blue.svg)]
   ```
2. Verify version number has no typos or spaces
3. Shield.io CDN cache takes 5-10 minutes to update
4. Force refresh browser with Cmd+Shift+R
5. Try adding cache-busting param: `?v=timestamp`

### Issue: Git Tag Already Exists

**Symptoms**: `fatal: tag 'v1.6.0' already exists`

**Solution**:
```bash
# Delete local tag
git tag -d v1.6.0

# Delete remote tag (if pushed)
git push origin :refs/tags/v1.6.0

# Recreate tag with correct version
git tag -a v1.6.0 -m "Version 1.6.0: Description"

# Push corrected tag
git push origin v1.6.0
```

### Issue: README Still Shows Old Version After Update

**Symptoms**: Updated file but version still shows old number

**Solutions**:
1. Check you saved the file
2. Verify you edited correct file (not a copy)
3. Check line numbers haven't shifted (search for pattern instead)
4. Use `grep` to find all occurrences: `grep -n "1.5.0" README.md`
5. Look for version in comments or code blocks (should update too)

---

## Prevention & Automation

### Current Process

**Manual checklist** with audit script (current approach)
- **Pros**: Works now, catches errors, simple
- **Cons**: Manual, requires discipline

### Future Improvements

#### Option 1: Pre-commit Hook

```bash
#!/bin/bash
# .git/hooks/pre-commit

# Run version audit if marketplace.json changed
if git diff --cached --name-only | grep -q "marketplace.json"; then
  echo "⚠️  marketplace.json changed. Running version audit..."
  ./scripts/audit-version.sh
  if [ $? -ne 0 ]; then
    echo "❌ Commit blocked: Version mismatch detected!"
    echo "Fix version references and try again."
    exit 1
  fi
fi
```

#### Option 2: Version Bump Script

```bash
#!/bin/bash
# scripts/bump-version.sh NEW_VERSION

# Automatically updates all version references
# Usage: ./scripts/bump-version.sh 1.6.0
```

#### Option 3: GitHub Action

```yaml
# .github/workflows/version-check.yml
name: Version Consistency Check
on: [pull_request]
jobs:
  check:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - run: ./scripts/audit-version.sh
```

**Decision**: Start with manual checklist, add automation if version drift becomes frequent.

---

## Related Documentation

**System Docs**:
- [Project Architecture](../system/project-architecture.md)
- [Plugin Patterns](../system/plugin-patterns.md)

**Other SOPs**:
- [Plugin Release Workflow](./plugin-release-workflow.md) - Complete release process

**Task Docs**:
- [TASK-04: Version Sync Fix](../tasks/TASK-04-version-sync-release-process.md)

---

## Version History

- **2025-10-13**: Created during TASK-04 (version sync fix)
- **Last Updated**: 2025-10-13

---

## Notes

### Why This SOP Exists

On 2025-10-13, v1.5.0 was released with `marketplace.json` showing v1.5.0 but `README.md` still showing v1.4.0. This created user confusion and eroded documentation trust.

**Root cause**: No systematic checklist for version updates
**Solution**: This SOP with pre-release checklist and audit script
**Prevention**: Make version sync mandatory part of release workflow

### Success Criteria

- [ ] Zero version mismatches in future releases
- [ ] New contributors can follow checklist without errors
- [ ] Audit script catches issues before commit
- [ ] Users always see consistent version numbers

---

**This SOP prevents version drift and ensures professional release quality** 🚀
