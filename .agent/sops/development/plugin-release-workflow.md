# Plugin Release Workflow

**Category**: Development
**Created**: 2025-10-12
**Last Used**: v1.3.0 release

---

## Context

Standard operating procedure for releasing new versions of the JITD Claude Code plugin. This workflow ensures consistent releases with proper versioning, documentation, and GitHub distribution.

---

## When to Use

Use this SOP when:
- Releasing a new plugin version (patch, minor, or major)
- After completing features that need distribution
- Publishing bug fixes to users
- Any change that affects plugin functionality

---

## Prerequisites

- [ ] All features implemented and tested
- [ ] Local testing completed in jitd-test project
- [ ] Documentation updated (task docs, system docs)
- [ ] Working directory clean (no uncommitted changes)

---

## Step-by-Step Release Process

### 1. Determine Version Number

**Semantic Versioning Rules**:
- **Patch** (1.3.1): Bug fixes, typos, minor docs updates
- **Minor** (1.4.0): New features, new commands, non-breaking changes
- **Major** (2.0.0): Breaking changes, major refactoring

**Example**:
```
Current: 1.2.3
Adding /jitd-start command → 1.3.0 (minor - new feature)
Fixing typo in template → 1.2.4 (patch - bug fix)
Changing command structure → 2.0.0 (major - breaking change)
```

### 2. Update Version in marketplace.json

**File**: `.claude-plugin/marketplace.json`

**Update BOTH locations**:
```json
{
  "metadata": {
    "version": "1.3.0"  // <-- Update here
  },
  "plugins": [
    {
      "version": "1.3.0"  // <-- And here
    }
  ]
}
```

**Verify versions match**:
```bash
grep -A 2 -B 2 version .claude-plugin/marketplace.json
```

### 3. Update System Documentation

**Files to update**:
- `.agent/system/project-architecture.md` - Update version references
- `.agent/DEVELOPMENT-README.md` - Update timestamps
- Any docs referencing old version

**Search for old version**:
```bash
grep -r "1.2.0" .agent/
```

### 4. Commit Changes

**Use conventional commit format**:
```bash
git add -A
git commit -m "feat: add /jitd-start command and PM tool auto-configuration

- New /jitd-start command for session initialization
- Enhanced /jitd-init with PM tool integration guidance
- Auto-generates Linear and GitHub integration SOPs
- Stronger CLAUDE.md enforcement of JITD workflow
- Version bump to 1.3.0

🤖 Generated with [Claude Code](https://claude.com/claude-code)

Co-Authored-By: Claude <noreply@anthropic.com>"
```

**Commit message format**:
- First line: `type(scope): description`
- Body: Bullet points of changes
- Include Claude Code attribution
- Include Co-Authored-By line

**Commit types**:
- `feat:` - New feature
- `fix:` - Bug fix
- `docs:` - Documentation only
- `chore:` - Maintenance (version bump)
- `refactor:` - Code restructuring

### 5. Create Git Tag

**Create annotated tag**:
```bash
git tag -a v1.3.0 -m "Version 1.3.0: Session start command and PM integration

Features:
- /jitd-start command for consistent session initialization
- Automated PM tool integration setup (Linear, GitHub)
- Auto-generated integration SOPs
- Stronger JITD workflow enforcement in CLAUDE.md

This release dramatically improves the onboarding experience and ensures
consistent JITD workflow adoption across all sessions."
```

**Tag message format**:
- First line: "Version X.Y.Z: Brief description"
- Blank line
- "Features:" or "Changes:" section
- Bullet points of key changes
- Optional: Additional context paragraph

### 6. Push to GitHub

**Push commit and tag together**:
```bash
git push origin main && git push origin v1.3.0
```

**Verify push succeeded**:
```bash
git log --oneline -3
git tag -l | tail -3
```

**Check on GitHub**:
- Visit: https://github.com/alekspetrov/jitd-plugin/tags
- Confirm new tag appears

### 7. Create GitHub Release

**Using gh CLI**:
```bash
gh release create v1.3.0 \
  --title "JITD v1.3.0: Session Start Command & PM Integration" \
  --notes "$(cat <<'EOF'
# JITD v1.3.0: Session Start Command & PM Integration

## 🎯 What's New

[Detailed release notes with sections:]
- What's new
- Why it matters
- Upgrade instructions
- Documentation links
- Feedback section

**Full Changelog**: https://github.com/alekspetrov/jitd-plugin/compare/v1.2.3...v1.3.0
EOF
)"
```

**Release notes structure**:
1. **Title** with version and key feature
2. **What's New** - Feature highlights with examples
3. **Why This Matters** - Problem solved, benefits
4. **Upgrade Instructions** - For new and existing users
5. **Impact** - Metrics and improvements
6. **Documentation** - Links to task docs, architecture
7. **Feedback** - How to contribute or report issues
8. **Full Changelog** - Link to compare view

**Verify release**:
- Visit: https://github.com/alekspetrov/jitd-plugin/releases
- Confirm release appears with notes

### 8. Document the Release (JITD)

**Create task documentation**:
```bash
/update-doc feature TASK-XX
```

**This creates**:
- `.agent/tasks/TASK-XX-feature.md` - Implementation plan
- Updates `.agent/DEVELOPMENT-README.md` - Adds to index
- Updates `.agent/system/project-architecture.md` - Version references

**Update SOP (this doc)**:
- Add "Last Used" date
- Note any issues encountered
- Add lessons learned section

### 9. Verify Installation

**Test in fresh project**:
```bash
cd /path/to/test/project
/plugin marketplace add alekspetrov/jitd-plugin
/plugin install jitd
/jitd-init
/jitd-start
```

**Verify**:
- [ ] Plugin installs without errors
- [ ] Commands available (/jitd-init, /jitd-start, etc.)
- [ ] Templates copy correctly
- [ ] Version shows correctly in marketplace

---

## Troubleshooting

### Issue: Version Mismatch in marketplace.json

**Symptoms**: Two version fields don't match

**Solution**:
```bash
# Check both versions
grep version .claude-plugin/marketplace.json

# Update to match
# Edit file manually or use jq
```

### Issue: Git Tag Already Exists

**Symptoms**: `fatal: tag 'v1.3.0' already exists`

**Solution**:
```bash
# Delete local tag
git tag -d v1.3.0

# Delete remote tag (if pushed)
git push origin :refs/tags/v1.3.0

# Recreate tag
git tag -a v1.3.0 -m "..."
```

### Issue: GitHub Release Fails

**Symptoms**: `gh release create` errors

**Solutions**:
1. Check gh CLI authentication: `gh auth status`
2. Verify tag exists: `git tag -l | grep v1.3.0`
3. Check if release already exists: `gh release list`
4. Re-authenticate: `gh auth login`

### Issue: GitHub CDN Cache

**Symptoms**: Users still getting old version after hours

**Solutions**:
1. Wait 1-2 hours for CDN refresh
2. Users can force specific commit:
   ```bash
   /plugin marketplace add alekspetrov/jitd-plugin#422875d
   ```
3. Users can use local file for testing:
   ```bash
   /plugin marketplace add file:///path/to/jitd-plugin
   ```

---

## Prevention

### Before Starting Release

- [ ] Run tests in jitd-test project
- [ ] Verify all commands work
- [ ] Check for hardcoded version references
- [ ] Review CHANGELOG or commit history

### During Release

- [ ] Double-check version numbers match
- [ ] Test commands in release notes work
- [ ] Verify commit message follows conventions
- [ ] Check tag annotation has details

### After Release

- [ ] Verify tag on GitHub
- [ ] Check release notes render correctly
- [ ] Test installation in fresh project
- [ ] Update this SOP with any issues

---

## Checklist

Complete release checklist:

- [ ] Determine version (patch/minor/major)
- [ ] Update `.claude-plugin/marketplace.json` (both locations)
- [ ] Update version references in `.agent/system/`
- [ ] Update timestamps in `.agent/DEVELOPMENT-README.md`
- [ ] Commit with conventional commit message
- [ ] Create annotated git tag
- [ ] Push commit and tag to GitHub
- [ ] Create GitHub release with detailed notes
- [ ] Document with `/update-doc feature TASK-XX`
- [ ] Test installation in fresh project
- [ ] Verify commands work
- [ ] Update this SOP with lessons learned

---

## Metrics

### v1.3.0 Release (Example)

**Time to Release**: ~30 minutes
- Version update: 2 minutes
- Documentation: 10 minutes
- Git operations: 5 minutes
- GitHub release: 5 minutes
- Verification: 8 minutes

**Steps Completed**: 9/9

**Issues Encountered**: None

**Lessons Learned**:
- Using `gh release create` with heredoc for notes is much cleaner than web UI
- Documenting with `/update-doc` immediately after saves time
- Testing in jitd-test project catches issues early

---

## Related Documentation

**System Docs**:
- [Project Architecture](./../system/project-architecture.md) - Plugin structure
- [Plugin Patterns](./../system/plugin-patterns.md) - Development patterns

**Task Docs**:
- [TASK-01: Session Start & PM Integration](./../tasks/TASK-01-session-start-pm-integration.md)

**Other SOPs**:
- None yet (this is the first development SOP)

---

## Notes

### Version History of This SOP
- **2025-10-12**: Created during v1.3.0 release
- **Last Updated**: 2025-10-12

### Contributing
If you find issues with this workflow or have improvements:
1. Update this SOP
2. Add to "Lessons Learned" section
3. Update "Last Used" date
4. Commit changes

---

**This SOP ensures consistent, documented, and error-free plugin releases** 🚀
