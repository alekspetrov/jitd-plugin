# Version Note

**Created**: 2025-10-15

## Versions at Time of Creation

This example was documented with the following versions in mind:

### Framework & Runtime
- **Next.js**: 15.0.x (App Router)
- **React**: 19.0.x
- **Node.js**: 20.x LTS
- **TypeScript**: 5.3.x

### Third-Party Services
- **Supabase JS**: 2.38.x
- **Supabase SSR**: 0.0.10
- **Stripe SDK**: 14.10.x
- **Stripe JS**: 2.4.x
- **OpenAI SDK**: 4.20.x (hypothetical, check actual latest)

### Styling & UI
- **Tailwind CSS**: 3.4.x
- **PostCSS**: 8.4.x

---

## Important: Versions Will Be Outdated

**These versions will change.** Don't copy-paste exact version numbers.

**When you implement**:
1. Check latest stable versions of each package
2. Read current documentation (not outdated tutorials)
3. Use `npm install <package>@latest` or check npm for stable versions

**What won't change**:
- JITD workflow (navigator → tasks → SOPs → compact)
- Documentation patterns (`.agent/` structure)
- On-demand loading strategy (12k vs 150k tokens)

---

## Breaking Changes to Watch For

### Next.js
- App Router is relatively new → Expect refinements
- Server Components patterns may evolve
- Check [Next.js blog](https://nextjs.org/blog) for major updates

### Supabase
- Auth library changed from `auth-helpers` to `ssr` → May change again
- Check [Supabase docs](https://supabase.com/docs) for current patterns

### Stripe
- API versions change (currently `2023-10-16`)
- Webhook structure may evolve
- Check [Stripe API changelog](https://stripe.com/docs/upgrades)

---

## How to Adapt

**If versions changed**:
1. Update package versions in `package.json`
2. Check migration guides for breaking changes
3. Update task docs with new patterns
4. Update SOPs if workflows changed
5. Keep `.agent/` structure (it's universal)

**The value of this example**:
- Documentation workflow (timeless)
- Task planning patterns (universal)
- SOP organization (framework-agnostic)

**Not the value**:
- Exact code snippets (these will drift)
- Specific API calls (these will change)
- Version numbers (always outdated)

---

## Fetching Latest Docs

When implementing, always fetch latest:

```bash
# Example: Check Supabase Auth docs
WebFetch https://supabase.com/docs/guides/auth/server-side/nextjs

# Example: Check Next.js authentication
WebFetch https://nextjs.org/docs/app/building-your-application/authentication

# Example: Check Stripe Checkout
WebFetch https://stripe.com/docs/checkout/quickstart
```

**Document what you found** → Update task docs and SOPs with current patterns

---

## Summary

**Copy from this example**:
- ✅ `.agent/` documentation structure
- ✅ Task planning workflow
- ✅ SOP organization and format
- ✅ Navigator pattern
- ✅ Token optimization strategy

**Don't copy from this example**:
- ❌ Exact version numbers
- ❌ Code snippets (check current docs instead)
- ❌ Deprecated packages or patterns

**The JITD workflow is forever. The code is not.**

---

**Last Updated**: 2025-10-15
**Advice**: Re-read this every 6 months. Update outdated parts. Keep JITD structure.
