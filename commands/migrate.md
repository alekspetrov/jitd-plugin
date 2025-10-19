---
description: Migrate Navigator plugin from v1.x (JITD) to v2.x+ (Navigator)
---

# Navigator Migration Tool

Migrate your project from JITD (v1.x) to Navigator (v2.x+).

## Overview

This command helps you migrate:
1. Config file: `.jitd-config.json` → `.nav-config.json`
2. Documentation: `/jitd:*` → `/nav:*` references
3. CLAUDE.md custom instructions
4. Task documentation

---

## Step 1: Config Migration

Checking for `.agent/.jitd-config.json`...

First, let's migrate the config file using the migration script.

Run this command:

```bash
bash scripts/migrate-config.sh .
```

Or if Navigator plugin is installed globally:

```bash
bash ~/.claude/plugins/marketplaces/navigator-marketplace/scripts/migrate-config.sh .
```

---

## Step 2: Scan for Old References

Now let's scan your documentation for `/jitd:*` command references.

Scanning files...

```bash
# Search for /jitd: references
grep -r "/jitd:" . \
  --include="*.md" \
  --exclude-dir=".git" \
  --exclude-dir="node_modules" \
  | grep -v ".claude/plugins"
```

---

## Step 3: Auto-Fix Documentation

Would you like me to automatically update the documentation references?

I'll replace:
- `/jitd:init` → `/nav:init`
- `/jitd:start` → `/nav:start`
- `/jitd:update-doc` → `/nav:doc`
- `/jitd:marker` → `/nav:marker`
- `/jitd:markers` → `/nav:markers`
- `/jitd:compact` → `/nav:compact`

This will update:
- `CLAUDE.md`
- `.agent/DEVELOPMENT-README.md`
- `.agent/tasks/*.md`
- `.agent/sops/**/*.md`
- `.agent/system/*.md`
- `README.md` (if exists)

**Proceed with auto-fix?** [y/N]

---

## Step 4: Show Changes

Here are the changes that will be made:

```bash
# Preview changes with sed (dry run)
find . -type f -name "*.md" \
  ! -path "./.git/*" \
  ! -path "./node_modules/*" \
  ! -path "./.claude/plugins/*" \
  -exec grep -l "/jitd:" {} \;
```

---

## Step 5: Execute Migration

Running migration...

```bash
# Replace /jitd: with /nav: in all markdown files
find . -type f -name "*.md" \
  ! -path "./.git/*" \
  ! -path "./node_modules/*" \
  ! -path "./.claude/plugins/*" \
  -exec sed -i '' 's|/jitd:init|/nav:init|g' {} \; \
  -exec sed -i '' 's|/jitd:start|/nav:start|g' {} \; \
  -exec sed -i '' 's|/jitd:update-doc|/nav:doc|g' {} \; \
  -exec sed -i '' 's|/jitd:marker|/nav:marker|g' {} \; \
  -exec sed -i '' 's|/jitd:markers|/nav:markers|g' {} \; \
  -exec sed -i '' 's|/jitd:compact|/nav:compact|g' {} \;
```

---

## Step 6: Verify Changes

Let's verify the migration was successful:

```bash
# Check for remaining /jitd: references
echo "Remaining /jitd: references:"
grep -r "/jitd:" . \
  --include="*.md" \
  --exclude-dir=".git" \
  --exclude-dir="node_modules" \
  | grep -v ".claude/plugins" \
  || echo "✅ None found - migration complete!"
```

---

## Step 7: Review with Git

Review all changes:

```bash
git diff
```

Check which files were modified:

```bash
git status
```

---

## Step 8: Commit Migration

If everything looks good, commit the migration:

```bash
git add .agent/
git add CLAUDE.md
git add README.md  # if modified
git commit -m "chore: migrate to Navigator v2.0

- Renamed .jitd-config.json → .nav-config.json
- Updated config version to 2.0.0
- Replaced all /jitd:* → /nav:* command references
- Updated documentation for Navigator branding

Migration performed by /nav:migrate
"
```

---

## Rollback (If Needed)

If something went wrong, rollback with git:

```bash
# Undo all changes
git checkout .

# Or restore specific files
git checkout .agent/.jitd-config.json
git checkout CLAUDE.md
git checkout .agent/DEVELOPMENT-README.md
```

---

## Migration Complete ✅

Your project has been migrated to Navigator v2.0!

### What Changed

- ✅ Config: `.jitd-config.json` → `.nav-config.json`
- ✅ Version: `1.0.0` → `2.0.0`
- ✅ Commands: `/jitd:*` → `/nav:*`
- ✅ Documentation updated

### What's New in Navigator v2.0

**Features**:
- 🎯 Skills: Auto-invocation based on natural language
- 📊 Session statistics: Real token usage tracking
- 🔧 Hybrid architecture: Agents for research, Skills for execution
- 📈 95%+ token efficiency (improved from 92%)

**New Commands**:
- `/nav:migrate` - Migration tool (this command)
- `/nav:doc` - Task documentation (renamed from `/nav:update-doc`)

**Skills** (auto-invoke via natural language):
- `nav-start` - "start session", "begin work"
- `nav-marker` - "save progress", "create checkpoint"
- `nav-compact` - "clear context", "start fresh"
- `nav-task` - "document feature", "create task"
- `nav-sop` - "save solution", "create SOP"

### Next Steps

1. **Try Skills**: Instead of `/nav:start`, just say "start my session"
2. **Explore v2.0**: Check out new features in README.md
3. **Plan for v2.1**: Predefined functions & nav-skill-creator coming soon

### Backward Compatibility

Don't worry! Old `/jitd:*` commands still work (with deprecation warnings).

You can gradually adopt new commands at your own pace.

---

## Troubleshooting

### Config file not found

**Problem**: No `.jitd-config.json` found

**Solution**: You may not have initialized Navigator yet
```bash
/nav:init
```

### Permission denied

**Problem**: Can't write to `.agent/` directory

**Solution**: Check file permissions
```bash
chmod -R u+w .agent/
```

### Git conflicts

**Problem**: Merge conflicts after migration

**Solution**: Resolve conflicts manually or use:
```bash
git checkout --theirs .agent/.nav-config.json
```

### Need help?

- Documentation: https://github.com/alekspetrov/navigator-plugin
- Issues: https://github.com/alekspetrov/navigator-plugin/issues
- Migration Guide: https://github.com/alekspetrov/navigator-plugin/blob/main/MIGRATION.md

---

**Last updated**: 2025-10-18 (Navigator v2.0)
