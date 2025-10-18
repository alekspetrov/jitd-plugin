# Stack Choices for Next.js SaaS Example

This document explains **why** specific technologies were chosen for this example and provides **alternatives** for your project.

**Remember**: Navigator works with any stack. These choices make the example concrete, not prescriptive.

---

## Framework: Next.js 15 (App Router)

**Why chosen**:
- Most popular React framework (learning transferable)
- App Router shows modern React patterns (Server Components, SSR)
- Good developer experience (hot reload, TypeScript support)
- Deploy-friendly (Vercel, anywhere Node.js runs)

**Alternatives**:
- **Remix**: Better data loading patterns, simpler mental model
- **SvelteKit**: Faster, smaller bundles, less JavaScript
- **Nuxt 3**: Vue ecosystem, similar patterns to Next.js
- **Astro**: Content-focused, islands architecture

**Navigator impact**: None. `.agent/` structure identical, just change framework names in docs.

---

## Rendering: Server-Side Rendering (SSR)

**Why chosen**:
- Better SEO (content rendered server-side)
- Faster initial page load (HTML sent immediately)
- Shows Server Component patterns (modern Next.js)

**Alternatives**:
- **Static Site Generation (SSG)**: Faster, cheaper hosting, less flexible
- **Client-Side Rendering (CSR)**: Simpler, worse SEO, slower initial load
- **Incremental Static Regeneration (ISR)**: Hybrid approach, more complex

**Navigator impact**: None. Rendering strategy is implementation detail, not workflow.

---

## Styling: Tailwind CSS

**Why chosen**:
- Utility-first (fast prototyping)
- Widely adopted (easy to find help)
- No CSS-in-JS runtime cost
- Good TypeScript support (via tailwind.config)

**Alternatives**:
- **CSS Modules**: Scoped styles, no utilities, more verbose
- **styled-components**: CSS-in-JS, runtime cost, better theming
- **Panda CSS**: Zero-runtime CSS-in-JS, type-safe
- **Vanilla CSS**: No framework, full control, more manual

**Navigator impact**: None. Styling doesn't affect documentation workflow.

---

## Database: Supabase (PostgreSQL)

**Why chosen**:
- PostgreSQL (powerful, reliable, widely known)
- Good free tier (easy to try)
- Integrated auth (fewer services to manage)
- Real-time subscriptions (nice for SaaS features)

**Alternatives**:
- **Prisma + PostgreSQL**: More control, self-hosted, no vendor lock-in
- **Drizzle ORM**: Type-safe, lightweight, better performance
- **Firebase**: NoSQL, real-time by default, different mental model
- **PlanetScale**: MySQL, serverless, schema branching

**Navigator impact**: None. Database choice affects `.agent/sops/development/` patterns, not structure.

---

## Authentication: Supabase Auth

**Why chosen**:
- Integrated with Supabase DB (fewer services)
- Built-in OAuth providers (Google, GitHub, etc.)
- Row-Level Security (RLS) support
- Email/password + magic links

**Alternatives**:
- **NextAuth (Auth.js)**: More flexible, self-hosted, more setup
- **Clerk**: Better UX, paid service, great components
- **Auth0**: Enterprise features, more expensive, OAuth specialist
- **Custom JWT**: Full control, more work, security responsibility

**Navigator impact**: None. Auth provider affects `.agent/sops/integrations/` docs, not workflow.

---

## Payments: Stripe

**Why chosen**:
- Industry standard (most integrations available)
- Good documentation (easy to learn)
- Subscription support (recurring revenue for SaaS)
- Solid TypeScript SDK

**Alternatives**:
- **Paddle**: Merchant of record (handles taxes), higher fees
- **LemonSqueezy**: Simpler, merchant of record, fewer features
- **PayPal**: Widely trusted, worse developer experience
- **Crypto payments**: Niche, volatile, regulatory unclear

**Navigator impact**: None. Payment provider affects `.agent/tasks/TASK-XX-payments.md`, not structure.

---

## AI Integration: OpenAI API

**Why chosen**:
- Most mature API (GPT-4, GPT-3.5)
- Good documentation
- Streaming support
- Function calling (structured outputs)

**Alternatives**:
- **Anthropic (Claude)**: Better reasoning, longer context, similar API
- **Google (Gemini)**: Multimodal, free tier, less mature
- **Ollama**: Self-hosted, open models, no API costs
- **Replicate**: Many models, pay-per-use, good for experiments

**Navigator impact**: None. AI provider affects `.agent/sops/integrations/` docs.

---

## Hosting: Vercel

**Why chosen**:
- Created by Next.js team (best integration)
- Zero-config deploys (git push → live)
- Good free tier
- Edge functions support

**Alternatives**:
- **Netlify**: Similar DX, different edge story
- **Railway**: Simpler pricing, Docker support, databases included
- **Fly.io**: Full VM control, global deployment, more complex
- **AWS/GCP/Azure**: More control, more complexity, better at scale

**Navigator impact**: None. Hosting affects `.agent/sops/deployment/` docs.

---

## Type Safety: TypeScript

**Why chosen**:
- Industry standard for React projects
- Catches errors at compile time
- Better IDE support (autocomplete, refactoring)
- Required for modern Next.js patterns

**Alternatives**:
- **JavaScript**: Simpler, faster prototyping, more runtime errors
- **JSDoc**: Type hints without compilation, less safety
- **Flow**: Facebook's type checker, less adoption

**Navigator impact**: None. Language choice doesn't affect documentation workflow.

---

## Testing: (Not Included in Example)

**If building real project, consider**:
- **Vitest**: Fast, modern, good DX
- **Jest**: Industry standard, more mature, slower
- **Playwright**: E2E testing, multi-browser
- **Cypress**: E2E testing, better DX, slower

**Navigator impact**: Test strategy affects `.agent/sops/development/testing-workflow.md`

---

## How to Adapt This Example

### If You Use Different Stack

1. **Copy `.agent/` structure** → Keep organization
2. **Replace framework names** → Update docs to match your stack
3. **Adapt patterns** → Rewrite SOPs for your tools
4. **Keep workflow** → Navigator → tasks → SOPs → compact

### What Stays the Same

- Navigator pattern (`.agent/DEVELOPMENT-README.md`)
- Task documentation (`.agent/tasks/TASK-XX-*.md`)
- SOP organization (`.agent/sops/{development,debugging,integrations}/`)
- System docs (`.agent/system/`)
- Navigator workflow (`/nav:start` → work → `/nav:compact`)

### What Changes

- Framework-specific patterns (Next.js → Remix → SvelteKit)
- Tool names (Supabase → Prisma → Firebase)
- Commands (npm → pnpm → bun)
- File structure (App Router → Pages Router → SvelteKit routes)

---

## Philosophy

**This example makes concrete choices** to show real patterns, not abstract concepts.

**Your project will differ** and that's fine. Navigator is stack-agnostic.

**Copy the `.agent/` structure, not the tech stack.**

---

**Version Note**: Created 2025-10-15. Use latest versions of chosen tools when building.
