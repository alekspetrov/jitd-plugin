# TASK-09: Plugin Update Migration System

**Created**: 2025-10-18
**Status**: Planning
**Priority**: Critical
**Complexity**: High

---

## Context

Need robust migration system for updating Navigator plugin across versions (v1.6 → v2.0 → v3.0) without breaking existing user projects.

### Current Reality

**User projects found with old config**:
```
/Users/aleks.petrov/Projects/startups/linearinvoices/.agent/.jitd-config.json
/Users/aleks.petrov/Projects/startups/quant-flow-landing/.agent/.jitd-config.json
/Users/aleks.petrov/Projects/tmp/jitd-test/.agent/.jitd-config.json
```

**Migration challenges**:
1. Plugin name change: `jitd` → `navigator`
2. Config file rename: `.jitd-config.json` → `.nav-config.json`
3. Command changes: `/jitd:*` → `/nav:*`
4. Skills added (v2.0+)
5. Commands deprecated (v2.5+)
6. Commands removed (v3.0+)
7. User projects reference old names in documentation
8. CLAUDE.md in user projects has old `/jitd:*` commands

---

## Problem Statement

**When user updates plugin from v1.6 to v3.0**:
- ❌ Old config `.jitd-config.json` not recognized
- ❌ Old commands `/jitd:*` don't exist
- ❌ Documentation references broken links
- ❌ No automatic migration
- ❌ User doesn't know what to fix
- ❌ Breaking changes without warning

**What we need**:
- ✅ Automatic detection of old config
- ✅ Automatic migration of config file
- ✅ Backward compatibility layer
- ✅ Clear upgrade path with warnings
- ✅ Migration script for documentation
- ✅ Zero breaking changes for users
- ✅ Smooth transition across versions

---

## Migration System Architecture

### 1. Semantic Versioning Strategy

```
v1.x → v2.x: Minor breaking (deprecation warnings)
v2.x → v3.x: Major breaking (full migration required)

v1.6 (JITD)
  ├─ Config: .jitd-config.json
  ├─ Commands: /jitd:*
  └─ No skills

v2.0 (Navigator - Hybrid)
  ├─ Config: .nav-config.json (auto-migrate from .jitd-config.json)
  ├─ Commands: /nav:* (backward compat: /jitd:* → /nav:* redirect)
  ├─ Skills: 5 core skills
  └─ Deprecation warnings for /jitd:*

v2.1 (Enhanced)
  ├─ Config: .nav-config.json
  ├─ Commands: /nav:* (still supports /jitd:* with warnings)
  ├─ Skills: 6 skills + predefined functions
  └─ Migration helper: /nav:migrate command

v2.5 (Pre-v3)
  ├─ Config: .nav-config.json
  ├─ Commands: /nav:* (loud warnings for /jitd:*, suggest migration)
  ├─ Skills: 11+ skills (core + project-specific)
  └─ Migration required warning

v3.0 (Skills-Only)
  ├─ Config: .nav-config.json (auto-migrate, remove old)
  ├─ Commands: REMOVED (error with migration instructions)
  ├─ Skills: All automation via skills
  └─ Breaking: Old commands fail with helpful error
```

### 2. Config Migration System

**Location**: `scripts/migrate-config.sh`

```bash
#!/bin/bash
# Config migration script
# Called automatically on plugin update

PROJECT_ROOT="$1"
AGENT_DIR="$PROJECT_ROOT/.agent"

# Detect old config
if [ -f "$AGENT_DIR/.jitd-config.json" ] && [ ! -f "$AGENT_DIR/.nav-config.json" ]; then
    echo "🔄 Migrating Navigator config: .jitd-config.json → .nav-config.json"

    # Rename config
    mv "$AGENT_DIR/.jitd-config.json" "$AGENT_DIR/.nav-config.json"

    # Update version in config
    sed -i '' 's/"version": "1\.0\.0"/"version": "2.0.0"/' "$AGENT_DIR/.nav-config.json"

    echo "✅ Config migrated successfully"
    echo "📝 Old commands (/jitd:*) will work but are deprecated"
    echo "💡 Update to new commands: /jitd:start → /nav:start"
fi

# Detect both configs (user needs to clean up)
if [ -f "$AGENT_DIR/.jitd-config.json" ] && [ -f "$AGENT_DIR/.nav-config.json" ]; then
    echo "⚠️  Both .jitd-config.json and .nav-config.json found"
    echo "📝 Please remove .jitd-config.json (already migrated)"
fi
```

### 3. Backward Compatibility Layer

**Location**: `commands/_backward_compat.md` (hidden command)

```markdown
---
description: "[INTERNAL] Backward compatibility redirects for deprecated commands"
---

# Backward Compatibility Layer

This file provides redirects from old `/jitd:*` commands to new `/nav:*` commands.

## Redirect Map

When user types:          Execute:           Show warning:
/jitd:init         →      /nav:init          ⚠️ Deprecated, use /nav:init
/jitd:start        →      /nav:start         ⚠️ Deprecated, use /nav:start
/jitd:update-doc   →      /nav:doc           ⚠️ Deprecated, use /nav:doc
/jitd:marker       →      /nav:marker        ⚠️ Deprecated, use /nav:marker
/jitd:markers      →      /nav:markers       ⚠️ Deprecated, use /nav:markers
/jitd:compact      →      /nav:compact       ⚠️ Deprecated, use /nav:compact

## Implementation

Slash commands registered in plugin.json:
```json
{
  "commands": [
    "./commands/init.md",
    "./commands/start.md",
    "./commands/doc.md",
    "./commands/marker.md",
    "./commands/markers.md",
    "./commands/compact.md",
    "./commands/_jitd_init.md",        // Redirect with warning
    "./commands/_jitd_start.md",       // Redirect with warning
    "./commands/_jitd_update_doc.md",  // Redirect with warning
    "./commands/_jitd_marker.md",      // Redirect with warning
    "./commands/_jitd_markers.md",     // Redirect with warning
    "./commands/_jitd_compact.md"      // Redirect with warning
  ]
}
```

Each `_jitd_*.md` file shows warning and calls new command.
```

**Example**: `commands/_jitd_start.md`

```markdown
---
description: "[DEPRECATED] Use /nav:start instead"
---

⚠️ **DEPRECATION WARNING**

The `/jitd:start` command is deprecated. Please use `/nav:start` instead.

**Navigator plugin was renamed from JITD to Navigator in v2.0**

Update your workflow:
- ~~`/jitd:start`~~ → `/nav:start`
- ~~`/jitd:marker`~~ → `/nav:marker`
- ~~`/jitd:compact`~~ → `/nav:compact`

This backward compatibility will be removed in v3.0.

---

**Executing /nav:start for you...**

<!-- Include actual /nav:start content here -->
{{INCLUDE:commands/start.md}}
```

### 4. Migration Command

**Location**: `commands/migrate.md`

```markdown
---
description: Migrate Navigator plugin from v1.x to v2.x+
---

# Navigator Migration Tool

Migrate your project from JITD (v1.x) to Navigator (v2.x+).

## What This Does

1. ✅ Renames `.jitd-config.json` → `.nav-config.json`
2. ✅ Updates config version to 2.0.0
3. ✅ Scans CLAUDE.md for `/jitd:*` references
4. ✅ Scans `.agent/` docs for `/jitd:*` references
5. ✅ Generates migration report
6. ✅ Optionally auto-fixes documentation

## Usage

```bash
/nav:migrate
```

## Migration Steps

### Step 1: Detect Old Config

Checking for `.agent/.jitd-config.json`...

**Found**: `.agent/.jitd-config.json`
**Action**: Rename to `.nav-config.json`

### Step 2: Scan Documentation

Scanning for `/jitd:*` references...

**Files with old references**:
- `CLAUDE.md` (5 references)
- `.agent/DEVELOPMENT-README.md` (12 references)
- `.agent/tasks/TASK-01.md` (3 references)

### Step 3: Show Changes

**Config Migration**:
```diff
- .agent/.jitd-config.json
+ .agent/.nav-config.json
```

**Config Updates**:
```diff
{
-  "version": "1.0.0"
+  "version": "2.0.0"
}
```

**Documentation Updates**:
```diff
CLAUDE.md:
-  /jitd:start
+  /nav:start

.agent/DEVELOPMENT-README.md:
-  Use `/jitd:marker` to save progress
+  Use `/nav:marker` to save progress
```

### Step 4: Confirm Migration

**Proceed with migration?** [y/N]

### Step 5: Execute Migration

✅ Renamed `.jitd-config.json` → `.nav-config.json`
✅ Updated config version to 2.0.0
✅ Updated CLAUDE.md (5 references)
✅ Updated .agent/DEVELOPMENT-README.md (12 references)
✅ Updated .agent/tasks/TASK-01.md (3 references)

**Migration complete!**

**Next steps**:
1. Review changes with `git diff`
2. Test new commands: `/nav:start`, `/nav:marker`, etc.
3. Commit migration: `git add . && git commit -m "chore: migrate to Navigator v2.0"`

## Rollback

If migration fails, restore from git:
```bash
git checkout .agent/.jitd-config.json
git checkout CLAUDE.md .agent/
```
```

### 5. Auto-Migration on Plugin Update

**Location**: `scripts/post-install.sh`

```bash
#!/bin/bash
# Post-install hook for Navigator plugin
# Called automatically by Claude Code after plugin install/update

PLUGIN_DIR="$(cd "$(dirname "$0")/.." && pwd)"
PLUGIN_VERSION="$(jq -r '.version' "$PLUGIN_DIR/.claude-plugin/plugin.json")"

echo "🔧 Navigator Plugin Post-Install (v$PLUGIN_VERSION)"

# Function to migrate a single project
migrate_project() {
    local project_dir="$1"
    local agent_dir="$project_dir/.agent"

    # Skip if no .agent directory
    [ ! -d "$agent_dir" ] && return

    # Check for old config
    if [ -f "$agent_dir/.jitd-config.json" ]; then
        echo ""
        echo "📦 Found Navigator project: $project_dir"
        echo "🔄 Migration needed: .jitd-config.json detected"

        # Ask user for migration (or auto-migrate based on config)
        echo ""
        echo "Migrate automatically? [Y/n]"
        read -r response

        if [[ "$response" =~ ^([yY][eE][sS]|[yY]|)$ ]]; then
            # Run migration
            bash "$PLUGIN_DIR/scripts/migrate-config.sh" "$project_dir"

            echo ""
            echo "💡 Tip: Run '/nav:migrate' in Claude Code to update documentation"
        else
            echo "⏭️  Skipped migration for $project_dir"
            echo "💡 Run '/nav:migrate' when ready"
        fi
    fi
}

# Find all Navigator projects in common locations
echo ""
echo "🔍 Scanning for Navigator projects..."

# Scan ~/Projects (customize based on user's workspace)
if [ -d "$HOME/Projects" ]; then
    while IFS= read -r -d '' project; do
        migrate_project "$(dirname "$(dirname "$project")")"
    done < <(find "$HOME/Projects" -name ".jitd-config.json" -print0 2>/dev/null)
fi

echo ""
echo "✅ Post-install complete"
echo ""
echo "📚 Documentation: https://github.com/alekspetrov/navigator-plugin"
echo "💬 Issues: https://github.com/alekspetrov/navigator-plugin/issues"
```

### 6. Version Detection in Commands

**All commands should detect config version and adapt**:

**Example**: `commands/start.md`

```markdown
---
description: Start Navigator session - load navigator, set context, check tasks
---

# Start Navigator Session

<!-- Version detection -->
{{#if config.version < 2.0.0}}
⚠️ **Old config detected**: You're using Navigator v1.x config format.

**Recommended**: Migrate to v2.0 for new features (Skills, improved token efficiency)

Run: `/nav:migrate`

---
{{/if}}

<!-- Rest of command -->
Initialize your development session with Navigator workflow...
```

### 7. Breaking Changes in v3.0

**v3.0 removes all commands** - only Skills remain

**Strategy**: Hard fail with migration instructions

**Location**: `commands/_deprecated_all.md` (registered for all old commands in v3.0)

```markdown
---
description: "[REMOVED IN v3.0] Commands have been replaced by Skills"
---

# ❌ Command Removed in Navigator v3.0

Commands have been replaced by **Skills** for better auto-invocation and token efficiency.

## What Happened?

Navigator v3.0 is **Skills-only**. Manual `/nav:*` commands have been removed.

## How to Migrate

### Before (v2.x - Commands):
```
User types: /nav:start
→ Manual command execution
```

### After (v3.0 - Skills):
```
User types: "Start my work session"
→ nav-start skill auto-invokes automatically
→ No manual command needed
```

## Migration Steps

1. **Remove command usage from your workflow**
   - ~~`/nav:start`~~ → Just say "start session" or "begin work"
   - ~~`/nav:marker`~~ → Just say "save my progress"
   - ~~`/nav:compact`~~ → Just say "clear context"

2. **Update CLAUDE.md** (if you customized it)
   ```bash
   # Run migration tool
   /nav:migrate  # (this still works as transition helper)
   ```

3. **Learn Skills**
   - Skills auto-invoke based on natural language
   - No need to remember command syntax
   - More intuitive workflow

## Available Skills (v3.0)

Core Skills:
- `nav-start` - Triggers on: "start session", "begin work", "load navigator"
- `nav-marker` - Triggers on: "save progress", "create checkpoint"
- `nav-compact` - Triggers on: "clear context", "start fresh"
- `nav-task` - Triggers on: "document feature", "create task"
- `nav-sop` - Triggers on: "save this solution", "create SOP"
- `nav-skill-creator` - Triggers on: "create a skill for...", "automate this"

Project Skills (generated by nav-skill-creator):
- `frontend-component` - Triggers on: "create component"
- `backend-endpoint` - Triggers on: "add endpoint"
- `database-migration` - Triggers on: "create migration"
- And more...

## Need Help?

- Documentation: https://github.com/alekspetrov/navigator-plugin
- Migration Guide: https://github.com/alekspetrov/navigator-plugin/blob/main/MIGRATION.md
- Issues: https://github.com/alekspetrov/navigator-plugin/issues

## Rollback to v2.x

If you need commands back temporarily:

```bash
claude plugins install alekspetrov/navigator-plugin@2.5.0
```

**Note**: v2.x will receive security updates only (no new features)
```

---

## Migration Paths

### Path 1: v1.6 → v2.0 (Smooth)

**User experience**:
1. User updates plugin: `claude plugins update jitd-marketplace`
2. Post-install script runs, detects old config
3. Asks: "Migrate automatically? [Y/n]"
4. User presses Enter (yes)
5. Config renamed automatically
6. Message: "💡 Run '/nav:migrate' to update documentation"
7. User continues working with `/jitd:*` commands (they still work with warnings)
8. User runs `/nav:migrate` when ready
9. Documentation updated automatically
10. User commits migration

**No breaking changes** - everything still works

### Path 2: v1.6 → v2.5 (Warning Phase)

**User experience**:
1. Same as Path 1 (config auto-migrates)
2. Old commands work but show LOUD warnings:
   ```
   ⚠️ ⚠️ ⚠️  DEPRECATION WARNING  ⚠️ ⚠️ ⚠️

   /jitd:start will be REMOVED in v3.0

   Please migrate: Run /nav:migrate

   This is your last warning before breaking changes

   Continuing with /nav:start...
   ```
3. User motivated to migrate

**Still no breaking changes** - just warnings

### Path 3: v1.6 → v3.0 (Hard Break with Guidance)

**User experience**:
1. User updates plugin: `claude plugins update navigator-marketplace`
2. Post-install detects v1.6, shows migration guide
3. User types `/jitd:start` (old habit)
4. **FAILS** with helpful error:
   ```
   ❌ Command removed in Navigator v3.0

   Commands replaced by Skills (auto-invocation)

   Instead of: /nav:start
   Just say: "start session" or "begin work"

   Migration guide: /nav:migrate (transition helper)
   ```
5. User learns about Skills
6. User says "start my session"
7. nav-start skill auto-invokes
8. User realizes this is better (no command syntax to remember)

**Breaking change** - but clear path forward

### Path 4: v2.0 → v2.5 → v3.0 (Recommended)

**Best user experience** (gradual adoption):

**v2.0** (user learns Skills exist):
- Commands work fine
- Skills auto-invoke alongside commands
- User discovers: "Oh, I can just say 'start session' instead of /nav:start"

**v2.5** (user motivated to switch):
- Commands show warnings
- Skills work great
- User switches naturally

**v3.0** (user already using Skills):
- Commands removed
- User doesn't notice (already using Skills)
- Smooth transition

---

## Implementation Checklist

### v2.0 (Immediate)

- [ ] Create `scripts/migrate-config.sh`
- [ ] Create `scripts/post-install.sh`
- [ ] Create `commands/migrate.md`
- [ ] Add backward compat commands (`commands/_jitd_*.md`)
- [ ] Update plugin.json with both command sets
- [ ] Test migration v1.6 → v2.0
- [ ] Document migration in README.md
- [ ] Create MIGRATION.md guide

### v2.1 (Enhanced Migration)

- [ ] Add version detection to all commands
- [ ] Add auto-fix for common migration issues
- [ ] Create migration report generator
- [ ] Add rollback capability
- [ ] Test migration with real user projects

### v2.5 (Warning Phase)

- [ ] Add loud warnings to deprecated commands
- [ ] Create v3.0 migration preview
- [ ] Add Skills tutorial in deprecation warnings
- [ ] Send email to users about upcoming v3.0
- [ ] Create migration timeline

### v3.0 (Skills-Only)

- [ ] Remove all command files (except migrate helper)
- [ ] Replace with `commands/_deprecated_all.md`
- [ ] Update plugin.json (remove command references)
- [ ] Test that Skills auto-invoke correctly
- [ ] Create v3.0 migration completion report
- [ ] Update marketplace listing

---

## File Structure Evolution

### v1.6 (JITD)
```
.claude/plugins/marketplaces/jitd-marketplace/
├── .claude-plugin/
│   └── plugin.json
├── commands/
│   ├── init.md
│   ├── start.md
│   ├── update-doc.md
│   ├── marker.md
│   ├── markers.md
│   └── compact.md
└── scripts/
    └── session-stats.sh
```

### v2.0 (Navigator - Hybrid)
```
.claude/plugins/marketplaces/navigator-marketplace/
├── .claude-plugin/
│   ├── plugin.json (both /nav:* and /jitd:*)
│   └── marketplace.json
├── commands/
│   ├── init.md
│   ├── start.md
│   ├── doc.md (renamed from update-doc.md)
│   ├── marker.md
│   ├── markers.md
│   ├── compact.md
│   ├── migrate.md (NEW)
│   ├── _jitd_init.md (backward compat)
│   ├── _jitd_start.md
│   ├── _jitd_update_doc.md
│   ├── _jitd_marker.md
│   ├── _jitd_markers.md
│   └── _jitd_compact.md
├── skills/ (NEW)
│   ├── nav-start/
│   ├── nav-marker/
│   ├── nav-compact/
│   ├── nav-task/
│   └── nav-sop/
└── scripts/
    ├── migrate-config.sh (NEW)
    ├── post-install.sh (NEW)
    └── session_stats.py
```

### v2.5 (Warning Phase)
```
Same as v2.0, but:
- _jitd_*.md files show LOUD warnings
- migrate.md enhanced with v3.0 preview
```

### v3.0 (Skills-Only)
```
.claude/plugins/marketplaces/navigator-marketplace/
├── .claude-plugin/
│   ├── plugin.json (skills only)
│   └── marketplace.json
├── commands/
│   └── _deprecated_all.md (shows helpful error)
├── skills/
│   ├── nav-start/
│   ├── nav-marker/
│   ├── nav-compact/
│   ├── nav-task/
│   ├── nav-sop/
│   ├── nav-skill-creator/
│   ├── frontend-component/ (project-specific)
│   ├── backend-endpoint/
│   ├── database-migration/
│   ├── backend-test/
│   └── frontend-test/
└── scripts/
    ├── migrate-config.sh (still works for stragglers)
    ├── post-install.sh (updated for v3.0)
    └── session_stats.py
```

---

## Testing Strategy

### Test Scenario 1: Fresh Install v2.0

**Steps**:
1. User installs Navigator v2.0 (never had JITD)
2. Runs `/nav:init`
3. Creates `.nav-config.json`
4. No migration needed

**Expected**: Clean install, no warnings

### Test Scenario 2: Update v1.6 → v2.0

**Steps**:
1. User has JITD v1.6 with `.jitd-config.json`
2. User runs `claude plugins update`
3. Post-install detects old config
4. Prompts for migration
5. User accepts
6. Config renamed
7. User runs `/nav:migrate` for docs
8. Documentation updated

**Expected**: Smooth migration, old commands still work

### Test Scenario 3: Update v1.6 → v2.0 (Decline Migration)

**Steps**:
1. User has JITD v1.6
2. Update to v2.0
3. Decline auto-migration
4. User types `/jitd:start`
5. Gets warning but command works
6. User later runs `/nav:migrate` manually

**Expected**: Backward compat works, user migrates when ready

### Test Scenario 4: Update v1.6 → v3.0 (Direct Jump)

**Steps**:
1. User has JITD v1.6
2. Update directly to v3.0
3. Post-install shows migration guide
4. User types `/jitd:start`
5. Command fails with helpful error
6. User says "start my session"
7. Skill auto-invokes

**Expected**: Breaking change with clear guidance

### Test Scenario 5: Multiple Projects

**Steps**:
1. User has 3 projects with `.jitd-config.json`
2. Update to v2.0
3. Post-install finds all 3
4. Migrates each one
5. All projects updated

**Expected**: Batch migration works

---

## Success Metrics

**v2.0 Migration Success**:
- [ ] 100% of users can update without breaking
- [ ] < 5% users report migration issues
- [ ] Auto-migration works for 95%+ projects
- [ ] Clear documentation for edge cases

**v2.5 Warning Success**:
- [ ] 80%+ users migrate to new commands before v3.0
- [ ] Clear timeline communicated
- [ ] Migration guide easily accessible

**v3.0 Transition Success**:
- [ ] < 10% users surprised by command removal
- [ ] Clear error messages for old commands
- [ ] Skills work seamlessly
- [ ] Positive user feedback on auto-invocation

---

## Related Tasks

- TASK-08: Skills enhancements (v2.1-v2.2 roadmap)
- TASK-07: Skills migration (v2.0 implementation)
- TASK-01: Session start PM integration

---

## Notes

- Migration must be **idempotent** (safe to run multiple times)
- Always preserve user data (configs, docs)
- Clear communication > forced migration
- Gradual deprecation > hard breaks
- Skills are better UX than commands (user will realize this)
- v3.0 breaking change justified by better experience
