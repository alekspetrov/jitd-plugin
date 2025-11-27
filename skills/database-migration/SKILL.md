---
name: database-migration
description: Create database migration with schema changes and rollback. Auto-invoke when user says "create migration", "add table", "modify schema", or "change database".
allowed-tools: Read, Write, Edit, Grep, Glob, Bash
version: 1.0.0
---

# Database Migration Generator

Generate database migrations with rollback capability for schema changes.

## When to Invoke

Auto-invoke when user mentions:
- "Create migration"
- "Add table"
- "Modify schema"
- "Change database"
- "Database migration for [change]"

## What This Does

1. Generates migration file with timestamp
2. Creates schema change SQL (up migration)
3. Creates rollback SQL (down migration)
4. Validates SQL syntax
5. Follows migration tool conventions (Knex, Prisma, TypeORM)

## Success Criteria

- [ ] Migration file generated with unique timestamp
- [ ] Up migration creates/modifies schema correctly
- [ ] Down migration rolls back changes
- [ ] SQL syntax is valid
- [ ] Follows naming conventions

**Auto-invoke when creating database schema changes** 🗄️
