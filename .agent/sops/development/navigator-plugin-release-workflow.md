# Navigator Plugin Release Workflow

**Category**: development
**Created**: 2025-10-22
**Last Updated**: 2025-10-22

---

## Context

**When to use this SOP**:
- Releasing new Navigator plugin version with features
- Publishing updates to Claude Code marketplace
- Rolling out changes to existing Navigator users

**Problem it solves**:
- Ensures consistent release process across versions
- Prevents forgetting critical steps (marketplace update, docs, etc.)
- Provides clear upgrade path for existing users

**Prerequisites**:
- Changes committed and tested
- Release notes written
- Breaking changes documented (if any)

---

## The Problem

### Common Mistakes in Plugin Releases

**Symptom**: Users don't see updates or can't upgrade smoothly

**Mistakes**:
- ❌ Forgetting to bump `.claude-plugin/plugin.json` version
- ❌ Pushing code without marketplace metadata update
- ❌ No upgrade guide for existing users
- ❌ Missing breaking changes documentation
- ❌ Not testing `/nav:update` workflow

**Impact**:
- Users stuck on old version
- Broken upgrades
- Support burden from confused users

---

## The Solution

### Step 1: Prepare Release Materials

**Create release notes**:

```bash
# Create RELEASE-NOTES-v{X.Y.Z}.md
touch RELEASE-NOTES-v3.4.0.md
```

**Content structure**:
```markdown
# Navigator v3.4.0 Release Notes

**Release Date**: YYYY-MM-DD
**Type**: Major|Minor|Patch

## Major Feature: {Feature Name}

### What's New
- New feature 1
- New feature 2

## Breaking Changes
- Change 1 with migration path
- Change 2 with migration path

## Bug Fixes
- Fix 1
- Fix 2

## Installation
[Installation instructions]

## Migration Guide
[Upgrade steps from previous version]
```

**Create upgrade guide** (for major/minor releases):

```bash
touch UPGRADE-v3.4.0.md
```

**Content**:
```markdown
# Upgrading to Navigator v3.4.0

## Upgrade Steps

### Step 1: Update Navigator Plugin
/nav:update

### Step 2: Install New Dependencies (if any)
cd skills/{skill-name}
./setup.sh

### Step 3: Test
[Test commands]

## Breaking Changes
[What changed and how to fix]

## Rollback
cd .claude-plugins/navigator
git checkout v3.3.1
```

### Step 2: Update Plugin Metadata

**Update `.claude-plugin/plugin.json`**:

```json
{
  "name": "navigator",
  "version": "3.4.0",  // ← Bump this
  "description": "Navigator for Claude Code - [Add new feature summary]",
  // ... rest unchanged
}
```

**Version numbering**:
- **Major** (X.0.0): Breaking changes, major rewrites
- **Minor** (0.X.0): New features, backward compatible
- **Patch** (0.0.X): Bug fixes only

### Step 3: Update Skill Versions (if applicable)

**For modified skills**, update SKILL.md:

```yaml
---
name: product-design
version: 1.1.0  # ← Bump skill version
---
```

**Skill version rules**:
- Skills have independent versions from plugin
- Follow semantic versioning
- Update when skill changes

### Step 4: Commit and Push

**First commit: Feature changes**

```bash
git add -A
git commit -m "feat({skill-name}): {description} v{version}

{Detailed description}

New Features:
- Feature 1
- Feature 2

Breaking Changes:
- Change 1

Migration:
  {migration steps}

Tested with:
- {test environment details}

🤖 Generated with [Claude Code](https://claude.com/claude-code)

Co-Authored-By: Claude <noreply@anthropic.com>"

git push origin main
```

**Second commit: Plugin version bump**

```bash
git add .claude-plugin/plugin.json
git commit -m "chore: bump plugin version to {version}

🤖 Generated with [Claude Code](https://claude.com/claude-code)

Co-Authored-By: Claude <noreply@anthropic.com>"

git push origin main
```

**Third commit: Documentation** (if separate)

```bash
git add UPGRADE-v{version}.md
git commit -m "docs: add upgrade guide for v{version}

🤖 Generated with [Claude Code](https://claude.com/claude-code)

Co-Authored-By: Claude <noreply@anthropic.com>"

git push origin main
```

### Step 5: Tag Release

**Create Git tag**:

```bash
git tag -a v3.4.0 -m "Navigator v3.4.0: Direct Figma MCP Integration

- Direct Python → Figma MCP client
- 95% orchestration reduction
- One-command setup

See RELEASE-NOTES-v3.4.0.md for details"

git push origin v3.4.0
```

**Why tag**: Allows users to checkout specific versions

### Step 6: Update Marketplace (if applicable)

**For Claude Code marketplace**:

1. Navigate to marketplace submission
2. Update plugin metadata from `.claude-plugin/plugin.json`
3. Add release notes
4. Submit for review

**For self-hosted/GitHub**:
- Tag pushed = release published
- Users pull via `/nav:update` or `git pull`

### Step 7: Test Upgrade Path

**In test project with Navigator installed**:

```bash
# Simulate user upgrade
/nav:update
```

OR:

```bash
cd .claude-plugins/navigator
git pull origin main
```

**Verify**:
- ✅ New version shows in plugin.json
- ✅ New features work
- ✅ No errors during update
- ✅ Existing functionality intact

### Step 8: Announce Release

**Update README.md** (version badge):

```markdown
![Version](https://img.shields.io/badge/version-3.4.0-blue)
```

**Create GitHub Release** (if using GitHub):

1. Go to repository → Releases → New Release
2. Tag: `v3.4.0`
3. Title: `Navigator v3.4.0 - Direct Figma MCP Integration`
4. Description: Copy from RELEASE-NOTES-v3.4.0.md
5. Publish

**Notify users** (if you have channels):
- Discord/Slack announcement
- Twitter/social media post
- Email newsletter

---

## Complete Example: v3.4.0 Release

### Step-by-Step Walkthrough

**What was released**: Direct Figma MCP integration for product-design skill

**1. Prepared release materials**:
- Created `RELEASE-NOTES-v3.4.0.md` (detailed changelog)
- Created `UPGRADE-v3.4.0.md` (upgrade guide)
- Created `skills/product-design/README.md` (feature docs)

**2. Updated versions**:
```bash
# Plugin version
vim .claude-plugin/plugin.json
# Changed: "version": "3.3.1" → "3.4.0"

# Skill version
vim skills/product-design/SKILL.md
# Changed: version: 1.0.0 → 1.1.0
```

**3. Committed changes**:
```bash
# Feature commit
git add skills/product-design/
git commit -m "feat(product-design): add direct Figma MCP integration v3.4.0

Major feature release: Python directly connects to Figma Desktop MCP server

New Features:
- Direct Python → Figma MCP client
- One-command setup script (./setup.sh)
- Progressive refinement for smart token usage

Performance Improvements:
- 95% reduction in orchestration steps
- 92% reduction in token usage
- 75% faster design reviews

Breaking Changes:
- Requires Python 3.10+ (was 3.8+)
- Requires Figma Desktop with MCP enabled

Migration:
  cd skills/product-design && ./setup.sh"

# Version bump commit
git add .claude-plugin/plugin.json
git commit -m "chore: bump plugin version to 3.4.0"

# Docs commit
git add UPGRADE-v3.4.0.md
git commit -m "docs: add upgrade guide for v3.4.0"

git push origin main
```

**4. Tagged release**:
```bash
git tag -a v3.4.0 -m "Navigator v3.4.0: Direct Figma MCP Integration"
git push origin v3.4.0
```

**5. Tested upgrade**:
```bash
# In test project
/nav:update

# Verified:
✅ New files present
✅ ./setup.sh works
✅ Figma MCP connects
✅ Existing features work
```

**6. Announced**:
- GitHub Release created
- README badge updated
- Users notified via upgrade guide

---

## Testing

### Test 1: Fresh Install

**Simulate new user installing Navigator**:

```bash
cd .claude-plugins
git clone https://github.com/alekspetrov/navigator.git
```

**Verify**:
- ✅ Correct version in plugin.json
- ✅ All skills present
- ✅ Documentation complete

### Test 2: Upgrade from Previous Version

**Simulate existing user upgrading**:

```bash
cd .claude-plugins/navigator
git checkout v3.3.1  # Go to old version
git pull origin main  # Upgrade to latest
```

**Verify**:
- ✅ Upgrade succeeds without errors
- ✅ New features available
- ✅ Old features still work
- ✅ Breaking changes documented

### Test 3: Skill-Specific Setup

**For skills with new dependencies**:

```bash
cd skills/product-design
./setup.sh
```

**Verify**:
- ✅ Dependencies install correctly
- ✅ Tests pass
- ✅ Feature works end-to-end

---

## Prevention

**How to avoid release issues**:

1. **Use release checklist** (see below)
2. **Test upgrade path** before pushing
3. **Document breaking changes** immediately
4. **Create upgrade guide** for major/minor releases
5. **Version skills independently** from plugin

**Red flags to watch for**:
- ⚠️ Forgot to bump version number
- ⚠️ Breaking changes without migration guide
- ⚠️ No test of upgrade workflow
- ⚠️ Missing dependencies in setup script

---

## Troubleshooting

### Issue: Users can't see new version

**Symptoms**: `/nav:update` doesn't pull changes

**Cause**: Git tag not pushed or version in plugin.json not updated

**Fix**:
```bash
# Verify tag pushed
git tag -l | grep v3.4.0

# If missing
git tag -a v3.4.0 -m "Release notes"
git push origin v3.4.0

# Verify plugin.json updated
cat .claude-plugin/plugin.json | grep version
```

### Issue: Upgrade breaks existing setup

**Symptoms**: Features stop working after update

**Cause**: Missing migration steps or undocumented breaking changes

**Fix**:
1. Document breaking change in UPGRADE guide
2. Add rollback instructions
3. Test upgrade path from previous version
4. Consider making change backward compatible

### Issue: New dependencies not installed

**Symptoms**: `ModuleNotFoundError` after upgrade

**Cause**: Users don't know to run setup script

**Fix**:
1. Add prominent notice in UPGRADE guide
2. Include step in `/nav:update` output
3. Add check in skill to detect missing deps

---

## Release Checklist

Use this checklist for every release:

### Pre-Release
- [ ] All features tested and working
- [ ] Breaking changes documented
- [ ] Migration path tested
- [ ] Release notes written
- [ ] Upgrade guide created (major/minor releases)

### Version Updates
- [ ] `.claude-plugin/plugin.json` version bumped
- [ ] Skill versions updated (if modified)
- [ ] Version consistent across all docs

### Documentation
- [ ] `RELEASE-NOTES-v{X.Y.Z}.md` created
- [ ] `UPGRADE-v{X.Y.Z}.md` created (if needed)
- [ ] README updated (version badge, features)
- [ ] Breaking changes documented

### Commits & Tags
- [ ] Feature changes committed
- [ ] Version bump committed separately
- [ ] Docs committed
- [ ] Git tag created (`v{X.Y.Z}`)
- [ ] All pushed to origin

### Testing
- [ ] Fresh install tested
- [ ] Upgrade from previous version tested
- [ ] New features work
- [ ] Old features still work
- [ ] Setup scripts work (if added)

### Publication
- [ ] GitHub Release created (if applicable)
- [ ] Marketplace updated (if applicable)
- [ ] Users notified
- [ ] Announcement posted

---

## Related Documentation

**Navigator Docs**:
- System: `.agent/DEVELOPMENT-README.md` (Navigator overview)
- Task: Related task that introduced feature

**Git**:
- [Semantic Versioning](https://semver.org/)
- [Conventional Commits](https://www.conventionalcommits.org/)

**Claude Code**:
- Plugin marketplace guidelines
- Version management

---

## Maintenance Notes

**Update this SOP when**:
- Release process changes
- New marketplace requirements
- Different commit conventions adopted
- Automated release tooling added

**Owner**: Navigator maintainers

---

## Version History

| Date | Version | Changes |
|------|---------|---------|
| 2025-10-22 | 1.0.0 | Initial SOP based on v3.4.0 release |

---

**Last Updated**: 2025-10-22
**Tested With**: Navigator v3.4.0 release
**Next Review**: After next major release
