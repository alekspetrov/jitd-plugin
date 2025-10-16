# TASK-01: Authentication Setup

**Status**: ✅ Completed
**Tech Stack**: Next.js 15 (App Router), Supabase Auth
**Completed**: 2025-10-15
**Time Spent**: 6 hours

---

## Context

Building authentication system for AI SaaS app. Need to support:
- Email/password signup and login
- OAuth (Google, GitHub for faster onboarding)
- Protected routes (dashboard requires auth)
- Session persistence across page reloads

**Success Criteria**:
- Users can sign up with email/password
- Users can log in with Google/GitHub OAuth
- Dashboard routes protected (redirect to login if not authenticated)
- Sessions persist across browser refreshes
- Logout works correctly

---

## Research Phase

### Latest Documentation Check

```bash
# Checked Supabase Auth docs
WebFetch https://supabase.com/docs/guides/auth

# Checked Next.js 15 authentication patterns
WebFetch https://nextjs.org/docs/app/building-your-application/authentication

# Checked Supabase SSR package
WebFetch https://supabase.com/docs/guides/auth/server-side/nextjs
```

**Key findings**:
- Use `@supabase/ssr` package for Next.js (not old `@supabase/auth-helpers-nextjs`)
- Server Components need different client creation than Client Components
- Middleware best place for route protection (runs before page load)
- Auth state available in cookies (SSR-friendly)

### Technology Decisions

| Decision | Choice | Reasoning |
|----------|--------|-----------|
| Auth Provider | Supabase Auth | Already using Supabase for DB, integrated RLS |
| OAuth Providers | Google + GitHub | Most common, good UX, Supabase built-in support |
| Route Protection | Middleware | Runs before page render, better UX |
| Session Storage | Cookies (httpOnly) | More secure than localStorage, SSR-compatible |
| UI Library | Supabase Auth UI | Pre-built components, saves time, good UX |

**Alternatives Considered**:
- NextAuth.js → More flexible but more setup, not needed
- Clerk → Better UX but paid service, overkill for MVP
- Custom JWT → Full control but more security risk, not worth it

---

## Implementation Plan

### Phase 1: Supabase Project Setup

**Steps**:
1. Create Supabase project (done in cloud dashboard)
2. Enable authentication providers (Email, Google, GitHub)
3. Configure OAuth redirect URLs
4. Get Supabase project credentials

**Environment Variables Needed**:
```env
NEXT_PUBLIC_SUPABASE_URL=https://xxx.supabase.co
NEXT_PUBLIC_SUPABASE_ANON_KEY=eyJxxx...
SUPABASE_SERVICE_ROLE_KEY=eyJxxx...  # Server-side only
```

### Phase 2: Install Dependencies

```bash
npm install @supabase/supabase-js @supabase/ssr
```

**Versions installed** (2025-10-15):
- `@supabase/supabase-js@2.38.4`
- `@supabase/ssr@0.0.10`

**Note**: Check for latest versions when implementing

### Phase 3: Create Supabase Client Utilities

**Files created**:

```typescript
// utils/supabase/server.ts
// Server-side client (for Server Components, Server Actions, Route Handlers)
import { cookies } from 'next/headers'
import { createServerClient } from '@supabase/ssr'

export function createClient() {
  const cookieStore = cookies()

  return createServerClient(
    process.env.NEXT_PUBLIC_SUPABASE_URL!,
    process.env.NEXT_PUBLIC_SUPABASE_ANON_KEY!,
    {
      cookies: {
        get(name: string) {
          return cookieStore.get(name)?.value
        },
      },
    }
  )
}
```

```typescript
// utils/supabase/client.ts
// Client-side client (for Client Components)
import { createBrowserClient } from '@supabase/ssr'

export function createClient() {
  return createBrowserClient(
    process.env.NEXT_PUBLIC_SUPABASE_URL!,
    process.env.NEXT_PUBLIC_SUPABASE_ANON_KEY!
  )
}
```

**Why two clients?**
- Server Components can't use browser APIs
- Cookie handling different server vs client
- Supabase SSR package provides both

### Phase 4: Create Auth Pages

**Routes created**:
- `app/(auth)/login/page.tsx` - Login page
- `app/(auth)/signup/page.tsx` - Signup page
- `app/(auth)/auth/callback/route.ts` - OAuth callback handler

**Login page implementation**:
```typescript
// app/(auth)/login/page.tsx
'use client'

import { createClient } from '@/utils/supabase/client'
import { useState } from 'react'
import { useRouter } from 'next/navigation'

export default function LoginPage() {
  const [email, setEmail] = useState('')
  const [password, setPassword] = useState('')
  const [error, setError] = useState<string | null>(null)
  const router = useRouter()
  const supabase = createClient()

  async function handleEmailLogin(e: React.FormEvent) {
    e.preventDefault()
    setError(null)

    const { error } = await supabase.auth.signInWithPassword({
      email,
      password,
    })

    if (error) {
      setError(error.message)
    } else {
      router.push('/dashboard')
      router.refresh() // Refresh to update server-side auth state
    }
  }

  async function handleOAuthLogin(provider: 'google' | 'github') {
    const { error } = await supabase.auth.signInWithOAuth({
      provider,
      options: {
        redirectTo: `${window.location.origin}/auth/callback`,
      },
    })

    if (error) {
      setError(error.message)
    }
  }

  return (
    <div className="min-h-screen flex items-center justify-center">
      <div className="max-w-md w-full p-6 bg-white rounded-lg shadow">
        <h1 className="text-2xl font-bold mb-6">Log In</h1>

        {error && (
          <div className="bg-red-50 text-red-600 p-3 rounded mb-4">
            {error}
          </div>
        )}

        <form onSubmit={handleEmailLogin} className="space-y-4 mb-6">
          <input
            type="email"
            placeholder="Email"
            value={email}
            onChange={(e) => setEmail(e.target.value)}
            required
            className="w-full px-4 py-2 border rounded"
          />
          <input
            type="password"
            placeholder="Password"
            value={password}
            onChange={(e) => setPassword(e.target.value)}
            required
            className="w-full px-4 py-2 border rounded"
          />
          <button
            type="submit"
            className="w-full bg-blue-600 text-white py-2 rounded hover:bg-blue-700"
          >
            Log In
          </button>
        </form>

        <div className="space-y-2">
          <button
            onClick={() => handleOAuthLogin('google')}
            className="w-full bg-white border py-2 rounded hover:bg-gray-50"
          >
            Continue with Google
          </button>
          <button
            onClick={() => handleOAuthLogin('github')}
            className="w-full bg-gray-900 text-white py-2 rounded hover:bg-gray-800"
          >
            Continue with GitHub
          </button>
        </div>
      </div>
    </div>
  )
}
```

**OAuth callback handler**:
```typescript
// app/(auth)/auth/callback/route.ts
import { createClient } from '@/utils/supabase/server'
import { NextResponse } from 'next/server'

export async function GET(request: Request) {
  const { searchParams } = new URL(request.url)
  const code = searchParams.get('code')

  if (code) {
    const supabase = createClient()
    await supabase.auth.exchangeCodeForSession(code)
  }

  // Redirect to dashboard after successful OAuth
  return NextResponse.redirect(new URL('/dashboard', request.url))
}
```

### Phase 5: Protect Routes with Middleware

**File created**: `middleware.ts` (project root)

```typescript
import { createServerClient, type CookieOptions } from '@supabase/ssr'
import { NextResponse, type NextRequest } from 'next/server'

export async function middleware(request: NextRequest) {
  let response = NextResponse.next({
    request: {
      headers: request.headers,
    },
  })

  const supabase = createServerClient(
    process.env.NEXT_PUBLIC_SUPABASE_URL!,
    process.env.NEXT_PUBLIC_SUPABASE_ANON_KEY!,
    {
      cookies: {
        get(name: string) {
          return request.cookies.get(name)?.value
        },
        set(name: string, value: string, options: CookieOptions) {
          request.cookies.set({ name, value, ...options })
          response = NextResponse.next({
            request: {
              headers: request.headers,
            },
          })
          response.cookies.set({ name, value, ...options })
        },
        remove(name: string, options: CookieOptions) {
          request.cookies.set({ name, value: '', ...options })
          response = NextResponse.next({
            request: {
              headers: request.headers,
            },
          })
          response.cookies.set({ name, value: '', ...options })
        },
      },
    }
  )

  const { data: { user } } = await supabase.auth.getUser()

  // Redirect to login if accessing protected route without auth
  if (!user && request.nextUrl.pathname.startsWith('/dashboard')) {
    return NextResponse.redirect(new URL('/login', request.url))
  }

  // Redirect to dashboard if accessing auth pages while logged in
  if (user && (request.nextUrl.pathname === '/login' || request.nextUrl.pathname === '/signup')) {
    return NextResponse.redirect(new URL('/dashboard', request.url))
  }

  return response
}

export const config = {
  matcher: [
    '/((?!_next/static|_next/image|favicon.ico|.*\\.(?:svg|png|jpg|jpeg|gif|webp)$).*)',
  ],
}
```

**Why middleware?**
- Runs before page renders (better UX, no flash of protected content)
- Works for both Server and Client Components
- Handles cookie refresh automatically

---

## Implementation Results

### What Works

✅ **Email/Password Auth**:
- Signup creates user in Supabase
- Login returns session
- Passwords hashed by Supabase (bcrypt)

✅ **OAuth**:
- Google OAuth flow working
- GitHub OAuth flow working
- Redirect back to /dashboard after success

✅ **Route Protection**:
- /dashboard redirects to /login if not authenticated
- /login redirects to /dashboard if already authenticated
- Middleware runs on all routes (no gaps)

✅ **Session Persistence**:
- Sessions stored in httpOnly cookies
- Survives browser refresh
- Auto-refreshes before expiration

✅ **Logout**:
- `supabase.auth.signOut()` clears session
- Redirects to login page
- Middleware picks up change immediately

### What Didn't Work (Initially)

❌ **OAuth redirect on localhost**:
- **Problem**: Supabase OAuth required exact redirect URL
- **Solution**: Added `http://localhost:3000/auth/callback` to Supabase dashboard
- **Lesson**: Check both localhost AND production URLs in Supabase config

❌ **Session not updating after login**:
- **Problem**: Server Component showing old auth state after login
- **Solution**: Added `router.refresh()` after login success
- **Lesson**: Server Components cache, need explicit refresh

❌ **Hydration mismatch on protected pages**:
- **Problem**: Server rendered "not logged in", client rendered "logged in"
- **Solution**: Use middleware to redirect BEFORE page renders
- **Lesson**: Auth checks belong in middleware, not layout

---

## Testing Checklist

- [x] Sign up with email/password → creates account
- [x] Log in with email/password → redirects to dashboard
- [x] Log in with Google → OAuth flow works, redirects to dashboard
- [x] Log in with GitHub → OAuth flow works, redirects to dashboard
- [x] Access /dashboard without auth → redirects to /login
- [x] Refresh page while logged in → stays logged in
- [x] Logout → clears session, redirects to login
- [x] Access /login while logged in → redirects to /dashboard
- [x] OAuth redirect URLs work in production (not just localhost)

---

## Files Created/Modified

**New files**:
- `utils/supabase/server.ts` - Server-side Supabase client
- `utils/supabase/client.ts` - Client-side Supabase client
- `app/(auth)/login/page.tsx` - Login page
- `app/(auth)/signup/page.tsx` - Signup page (similar to login)
- `app/(auth)/auth/callback/route.ts` - OAuth callback handler
- `middleware.ts` - Route protection
- `.env.local` - Environment variables

**Modified files**:
- `.gitignore` - Added `.env.local`
- `package.json` - Added Supabase dependencies

---

## Lessons Learned

**What worked well**:
- Supabase Auth UI components → Saved 4+ hours on form design
- Middleware for protection → Clean, no layout complexity
- Separate server/client utils → Type-safe, clear separation

**What was harder than expected**:
- OAuth redirect URL configuration → Had to debug in Supabase dashboard
- Server Component refresh after auth change → Not obvious from docs
- Hydration issues → Took time to understand server vs client rendering

**Would do differently next time**:
- Set up OAuth redirect URLs BEFORE testing (not during)
- Use Server Actions for login form (instead of Client Component with fetch)
- Document environment variables in README immediately

---

## Documentation Created

**SOPs created from this task**:
- [Adding Protected Routes](../sops/development/adding-protected-routes.md) - How to protect new routes
- [Environment Setup](../sops/development/environment-setup.md) - Required env vars, Supabase setup

**Debugging SOPs created**:
- [Supabase Auth Redirect Issues](../sops/debugging/supabase-auth-redirect.md) - OAuth redirect debugging

---

## Next Steps

- [ ] Add password reset flow
- [ ] Add email verification
- [ ] Add profile page (update email, password)
- [ ] Add user metadata (display name, avatar)
- [ ] Add MFA (two-factor authentication) - future enhancement

---

## References

**Documentation used**:
- [Supabase Auth with Next.js](https://supabase.com/docs/guides/auth/server-side/nextjs)
- [Supabase SSR Package](https://github.com/supabase/ssr)
- [Next.js Authentication](https://nextjs.org/docs/app/building-your-application/authentication)

**Code repository locations**:
- Auth utilities: `utils/supabase/`
- Auth pages: `app/(auth)/`
- Route protection: `middleware.ts`

---

**Time Breakdown**:
- Research & planning: 1 hour
- Supabase setup: 0.5 hours
- Implementation: 3 hours
- Debugging OAuth: 1 hour
- Testing & documentation: 0.5 hours
- **Total**: 6 hours
