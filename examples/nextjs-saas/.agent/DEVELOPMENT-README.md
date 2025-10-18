# Next.js SaaS - Development Documentation Navigator

**Project**: AI Content Generator SaaS
**Tech Stack**: Next.js 15 (App Router), Tailwind, Supabase, Stripe
**Updated**: 2025-10-15

---

## 🚀 Quick Start for Development

### New to This Project?
**Read in this order:**
1. [Project Architecture](./system/project-architecture.md) - App structure, routing, data flow
2. [Tech Stack Patterns](./system/tech-stack-patterns.md) - Next.js + Supabase conventions

### Working on a Feature?
1. Check if similar task exists in [`tasks/`](#implementation-plans-tasks)
2. Read relevant system docs from [`system/`](#system-architecture-system)
3. Check for integration SOPs in [`sops/`](#standard-operating-procedures-sops)

### Fixing a Bug?
1. Check [`sops/debugging/`](#debugging) for known issues
2. Review relevant system docs for context
3. After fixing, create SOP: `/nav:update-doc sop debugging [issue-name]`

---

## 🤖 Task Completion Protocol (CRITICAL)

### Autonomous Completion Expected

Navigator projects run in **full autonomy mode**. When task implementation is complete:

✅ **Execute automatically** (no human prompt needed):
1. **Commit changes** with conventional commit message
2. **Archive implementation plan** (`/nav:update-doc feature TASK-XX`)
3. **Create completion marker** (`TASK-XX-complete`)
4. **Suggest compact** for next task

❌ **Don't wait for**:
- "Please commit now"
- "Update documentation"
- "Create a marker"

### Exception Cases (Ask First)

Only interrupt autonomous flow if:
- Uncommitted files contain secrets (.env, credentials, API keys)
- Multiple unrelated tasks modified (unclear which to close)
- Tests failing or implementation incomplete

---

## 📂 Documentation Structure

```
.agent/
├── DEVELOPMENT-README.md     ← You are here (navigator)
│
├── tasks/                    ← Implementation plans
│   ├── TASK-01-auth-setup.md
│   ├── TASK-02-dashboard-layout.md
│   ├── TASK-03-credits-system.md
│   ├── TASK-04-stripe-integration.md
│   └── TASK-05-ai-api-integration.md
│
├── system/                   ← Living architecture documentation
│   ├── project-architecture.md
│   └── tech-stack-patterns.md
│
└── sops/                     ← Standard Operating Procedures
    ├── development/          # How to build features
    │   ├── adding-new-page.md
    │   ├── adding-protected-routes.md
    │   ├── database-migrations.md
    │   └── environment-setup.md
    ├── debugging/            # Common issues & solutions
    │   ├── hydration-mismatch.md
    │   └── supabase-auth-redirect.md
    └── integrations/         # Third-party service setups
        ├── stripe-webhooks.md
        └── openai-api-setup.md
```

---

## 📖 Documentation Index

### Implementation Plans (`tasks/`)

#### [TASK-01: Authentication Setup](./tasks/TASK-01-auth-setup.md)
**Status**: ✅ Completed
**Completed**: 2025-10-15

**What was built**:
- Supabase Auth integration (email/password + OAuth)
- Protected routes via middleware
- Session management
- Login/signup pages

**Impact**: Users can authenticate, sessions persist, routes protected

#### [TASK-02: Dashboard Layout](./tasks/TASK-02-dashboard-layout.md)
**Status**: ✅ Completed
**Completed**: 2025-10-15

**What was built**:
- App Router layout structure (`app/(dashboard)/layout.tsx`)
- Sidebar navigation component
- User profile dropdown
- Credits display widget

**Impact**: Consistent dashboard UX, navigation in place

#### [TASK-03: Credits System](./tasks/TASK-03-credits-system.md)
**Status**: ✅ Completed
**Completed**: 2025-10-15

**What was built**:
- PostgreSQL schema for credits
- Server Actions for credit operations
- Credit deduction on AI generation
- Credits display in UI

**Impact**: Users have credit balance, consumed on usage

#### [TASK-04: Stripe Integration](./tasks/TASK-04-stripe-integration.md)
**Status**: ✅ Completed
**Completed**: 2025-10-15

**What was built**:
- Stripe Checkout for credit purchases
- Webhook handler for payment confirmation
- Credit top-up flow
- Payment history page

**Impact**: Users can purchase credits, revenue system functional

#### [TASK-05: AI API Integration](./tasks/TASK-05-ai-api-integration.md)
**Status**: ✅ Completed
**Completed**: 2025-10-15

**What was built**:
- OpenAI API integration (GPT-4)
- Streaming response handler
- Content generation UI
- Usage tracking (credits deducted)

**Impact**: Core product feature working, credits consumed

---

### System Architecture (`system/`)

#### [Project Architecture](./system/project-architecture.md)
**When to read**: Starting work on project, understanding structure

**Contains**:
- App Router folder structure
- Data flow (client → server actions → Supabase)
- Authentication flow
- Environment variables
- Deployment strategy

**Updated**: Every major architecture change

#### [Tech Stack Patterns](./system/tech-stack-patterns.md)
**When to read**: Understanding conventions, code reviews

**Contains**:
- Next.js 15 patterns (Server Components, Server Actions)
- Tailwind CSS organization
- Supabase client setup (server vs client)
- TypeScript conventions
- Error handling patterns

**Updated**: When adding new patterns

---

### Standard Operating Procedures (`sops/`)

#### Development

##### [Adding New Page](./sops/development/adding-new-page.md)
**When to use**: Creating new route/page

**Contains**:
- App Router file structure
- Server Component vs Client Component decision
- Layout vs page separation
- Metadata for SEO

**Last Used**: TASK-05 (AI generation page)

##### [Adding Protected Routes](./sops/development/adding-protected-routes.md)
**When to use**: Creating authenticated pages

**Contains**:
- Middleware configuration
- Session validation
- Redirect patterns
- Layout-based protection

**Last Used**: TASK-02 (Dashboard layout)

##### [Database Migrations](./sops/development/database-migrations.md)
**When to use**: Changing database schema

**Contains**:
- Supabase migration workflow
- SQL migration files
- Rollback strategy
- Testing migrations locally

**Last Used**: TASK-03 (Credits table)

##### [Environment Setup](./sops/development/environment-setup.md)
**When to use**: Onboarding new developer

**Contains**:
- Required environment variables
- Supabase project setup
- Stripe test mode keys
- OpenAI API key setup

**Last Updated**: 2025-10-15

#### Debugging

##### [Hydration Mismatch](./sops/debugging/hydration-mismatch.md)
**When to use**: Seeing hydration errors in console

**Contains**:
- Common causes (date formatting, random IDs)
- Server vs client rendering differences
- suppressHydrationWarning usage
- Debugging steps

**Last Used**: TASK-02 (Credits display)

##### [Supabase Auth Redirect](./sops/debugging/supabase-auth-redirect.md)
**When to use**: OAuth redirect not working

**Contains**:
- Redirect URL configuration
- Localhost vs production differences
- Callback route setup
- Common misconfigurations

**Last Used**: TASK-01 (OAuth setup)

#### Integrations

##### [Stripe Webhooks](./sops/integrations/stripe-webhooks.md)
**When to use**: Setting up or debugging webhooks

**Contains**:
- Webhook endpoint creation
- Signature verification
- Event handling
- Local testing with Stripe CLI

**Last Used**: TASK-04 (Payment webhooks)

##### [OpenAI API Setup](./sops/integrations/openai-api-setup.md)
**When to use**: Integrating OpenAI features

**Contains**:
- API key management
- Rate limiting handling
- Streaming responses
- Error handling
- Cost optimization

**Last Used**: TASK-05 (AI generation)

---

## 🔄 When to Read What

### Scenario: Adding New Authenticated Page

**Read order**:
1. This navigator (DEVELOPMENT-README.md)
2. `sops/development/adding-new-page.md` → Page structure
3. `sops/development/adding-protected-routes.md` → Auth middleware
4. Check `tasks/TASK-02-dashboard-layout.md` → Similar work
5. Implement new page
6. Document: `/nav:update-doc feature TASK-XX`

### Scenario: Adding Payment Feature

**Read order**:
1. This navigator
2. `system/project-architecture.md` → Data flow
3. `tasks/TASK-04-stripe-integration.md` → Payment patterns
4. `sops/integrations/stripe-webhooks.md` → Webhook setup
5. Implement feature
6. Update SOP if new patterns discovered

### Scenario: Fixing Hydration Error

**Read order**:
1. Check `sops/debugging/hydration-mismatch.md` → Known solution?
2. `system/tech-stack-patterns.md` → Server/Client Component rules
3. Debug issue
4. If new issue, create SOP: `/nav:update-doc sop debugging [issue-name]`

### Scenario: Onboarding New Developer

**Read order**:
1. This navigator (DEVELOPMENT-README.md)
2. `sops/development/environment-setup.md` → Get running locally
3. `system/project-architecture.md` → Understand structure
4. `system/tech-stack-patterns.md` → Learn conventions
5. Pick simple task from `tasks/` to get familiar

---

## 🛠️ Development Workflow

### Local Development Setup

```bash
# 1. Clone repo
git clone <repo-url>
cd nextjs-saas

# 2. Follow environment setup SOP
# Read: .agent/sops/development/environment-setup.md

# 3. Install dependencies
npm install

# 4. Set up Supabase (local or cloud)
# Follow: .agent/sops/integrations/supabase-local-dev.md (if exists)

# 5. Run dev server
npm run dev
```

### Making Changes

```bash
# 1. Start Navigator session
/nav:start

# 2. Load relevant task
Read .agent/tasks/TASK-XX-feature.md

# 3. Load relevant SOPs
Read .agent/sops/development/pattern-name.md

# 4. Implement feature
# Follow project patterns from tech-stack-patterns.md

# 5. Test changes
npm run build
npm run test (if tests exist)

# 6. Document changes
/nav:update-doc feature TASK-XX

# 7. If new pattern discovered
/nav:update-doc sop development pattern-name
```

---

## 📊 Token Optimization Strategy

**This project follows Navigator principles**:

1. **Always load**: `DEVELOPMENT-README.md` (~2k tokens)
2. **Load for current work**: Specific task doc (~3k tokens)
3. **Load if needed**: Relevant system doc (~5k tokens)
4. **Load as needed**: Specific SOP (~2k tokens)

**Total**: ~12k tokens vs ~150k (loading everything)

---

## 🎯 Success Metrics

### Documentation Coverage
- [x] 100% completed features have task docs
- [x] 90%+ integrations have SOPs
- [x] System docs updated with each feature
- [x] Zero repeated mistakes (SOPs prevent them)

### Development Efficiency
- [ ] New developer productive in 48 hours
- [ ] Common bugs documented in debugging SOPs
- [ ] Architecture decisions findable in <30 seconds
- [ ] Pattern consistency across features

---

## 🚀 Quick Commands Reference

```bash
# Start session (every new conversation)
/nav:start

# Update documentation
/nav:update-doc feature TASK-XX
/nav:update-doc sop debugging [issue]
/nav:update-doc system [doc-name]

# Create context marker
/nav:marker [name] "optional note"

# Smart compact
/nav:compact
```

---

**This documentation system keeps the project context-efficient while maintaining comprehensive knowledge.**

**Last Updated**: 2025-10-15
**Powered By**: Navigator (Navigator)
