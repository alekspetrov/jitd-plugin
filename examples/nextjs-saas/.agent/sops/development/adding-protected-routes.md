# SOP: Adding Protected Routes

**Category**: Development
**Created**: 2025-10-15 (from TASK-01)
**Last Used**: TASK-02
**Tech Stack**: Next.js 15 App Router, Supabase Auth

---

## When to Use This SOP

Use this when you need to:
- Create a new page that requires authentication
- Protect an existing page
- Add role-based access control (RBAC)
- Redirect unauthenticated users

---

## Prerequisites

- [x] Authentication system working (TASK-01 completed)
- [x] Middleware configured (`middleware.ts` exists)
- [x] Supabase client utilities created (`utils/supabase/`)

---

## Quick Reference

**For simple protection** (just require login):
1. Add route pattern to middleware matcher
2. Check auth in middleware
3. Redirect if not authenticated

**For role-based protection** (admin-only, etc.):
1. Add route pattern to middleware
2. Check user role in middleware
3. Return 403 if insufficient permissions

---

## Step-by-Step Guide

### Step 1: Add Route to Middleware Matcher

**File**: `middleware.ts`

```typescript
export const config = {
  matcher: [
    '/dashboard/:path*',       // Protect all dashboard routes
    '/admin/:path*',           // Protect all admin routes
    '/api/protected/:path*',   // Protect API routes
  ],
}
```

**Pattern matching**:
- `/dashboard` → Only `/dashboard` (not `/dashboard/settings`)
- `/dashboard/:path*` → `/dashboard` AND all sub-routes
- `/((?!public).*)` → Everything except `/public/*`

### Step 2: Check Authentication in Middleware

**File**: `middleware.ts`

```typescript
export async function middleware(request: NextRequest) {
  // ... (Supabase client setup)

  const { data: { user } } = await supabase.auth.getUser()

  // Redirect to login if accessing protected route without auth
  if (!user && request.nextUrl.pathname.startsWith('/dashboard')) {
    const redirectUrl = new URL('/login', request.url)
    redirectUrl.searchParams.set('redirect', request.nextUrl.pathname) // Remember where they were going
    return NextResponse.redirect(redirectUrl)
  }

  return response
}
```

**Why in middleware?**
- Runs BEFORE page renders (no flash of protected content)
- Works for both Server and Client Components
- Centralized auth logic (not scattered across pages)

### Step 3: Handle Redirect After Login

**File**: `app/(auth)/login/page.tsx`

```typescript
'use client'

import { useRouter, useSearchParams } from 'next/navigation'

export default function LoginPage() {
  const router = useRouter()
  const searchParams = useSearchParams()
  const redirect = searchParams.get('redirect') || '/dashboard'

  async function handleLogin() {
    // ... login logic

    if (!error) {
      router.push(redirect) // Go to original destination
      router.refresh()
    }
  }

  // ... rest of component
}
```

**Why save redirect?**
- Better UX (returns to original destination)
- Works for deep links (e.g., /dashboard/settings)

---

## Advanced: Role-Based Protection

### Step 1: Add User Roles to Database

**Supabase migration**:
```sql
ALTER TABLE auth.users ADD COLUMN role TEXT DEFAULT 'user';

-- Or use a separate table
CREATE TABLE user_roles (
  user_id UUID REFERENCES auth.users(id),
  role TEXT NOT NULL,
  PRIMARY KEY (user_id)
);
```

### Step 2: Check Role in Middleware

**File**: `middleware.ts`

```typescript
export async function middleware(request: NextRequest) {
  // ... (auth check)

  // Get user role from database
  const { data: profile } = await supabase
    .from('user_roles')
    .select('role')
    .eq('user_id', user.id)
    .single()

  // Protect admin routes
  if (request.nextUrl.pathname.startsWith('/admin')) {
    if (profile?.role !== 'admin') {
      return NextResponse.redirect(new URL('/dashboard', request.url))
    }
  }

  return response
}
```

### Step 3: Check Role in Page (Optional, for UI)

**File**: `app/(dashboard)/admin/page.tsx`

```typescript
import { createClient } from '@/utils/supabase/server'
import { redirect } from 'next/navigation'

export default async function AdminPage() {
  const supabase = createClient()
  const { data: { user } } = await supabase.auth.getUser()

  if (!user) {
    redirect('/login')
  }

  const { data: profile } = await supabase
    .from('user_roles')
    .select('role')
    .eq('user_id', user.id)
    .single()

  if (profile?.role !== 'admin') {
    redirect('/dashboard') // Or show 403 error
  }

  return <div>Admin Dashboard</div>
}
```

**Note**: Middleware already protects, this is defense-in-depth

---

## Common Patterns

### Pattern 1: Protect Entire Route Group

**Folder structure**:
```
app/
├── (auth)/           # Public (login, signup)
├── (dashboard)/      # Protected (requires login)
└── (admin)/          # Protected (requires admin role)
```

**Middleware**:
```typescript
if (!user && request.nextUrl.pathname.startsWith('/(dashboard)')) {
  // Redirect to login
}
```

### Pattern 2: Protect API Routes

**File**: `app/api/protected/route.ts`

```typescript
import { createClient } from '@/utils/supabase/server'
import { NextResponse } from 'next/server'

export async function GET() {
  const supabase = createClient()
  const { data: { user } } = await supabase.auth.getUser()

  if (!user) {
    return NextResponse.json({ error: 'Unauthorized' }, { status: 401 })
  }

  // ... protected logic
}
```

**Why not middleware for APIs?**
- API routes need to return JSON (not redirect)
- More flexibility for error responses
- Can check permissions per-endpoint

### Pattern 3: Conditional UI Based on Auth

**File**: `components/Header.tsx`

```typescript
'use client'

import { createClient } from '@/utils/supabase/client'
import { useEffect, useState } from 'react'

export function Header() {
  const [user, setUser] = useState(null)
  const supabase = createClient()

  useEffect(() => {
    supabase.auth.getUser().then(({ data: { user } }) => {
      setUser(user)
    })
  }, [])

  return (
    <header>
      {user ? (
        <a href="/dashboard">Dashboard</a>
      ) : (
        <a href="/login">Log In</a>
      )}
    </header>
  )
}
```

**Better approach (Server Component)**:
```typescript
import { createClient } from '@/utils/supabase/server'

export async function Header() {
  const supabase = createClient()
  const { data: { user } } = await supabase.auth.getUser()

  return (
    <header>
      {user ? (
        <a href="/dashboard">Dashboard</a>
      ) : (
        <a href="/login">Log In</a>
      )}
    </header>
  )
}
```

**Why Server Component?**
- No useEffect needed
- No loading state
- No hydration mismatch

---

## Troubleshooting

### Issue: Flash of Protected Content

**Symptom**: See protected page briefly before redirect

**Cause**: Auth check in layout/page, not middleware

**Solution**: Move auth check to middleware

```typescript
// ❌ Bad (in page)
export default async function DashboardPage() {
  const user = await getUser()
  if (!user) redirect('/login') // Flash happens before redirect
}

// ✅ Good (in middleware)
export async function middleware(request) {
  const user = await getUser()
  if (!user) return NextResponse.redirect('/login') // Intercepts before render
}
```

### Issue: Redirect Loop

**Symptom**: Infinite redirects between /login and /dashboard

**Cause**: Middleware redirects /login to /dashboard, but dashboard redirects back

**Solution**: Exclude auth pages from protection

```typescript
// Check if accessing login page while authenticated
if (user && request.nextUrl.pathname === '/login') {
  return NextResponse.redirect(new URL('/dashboard', request.url))
}

// Only protect dashboard if not authenticated
if (!user && request.nextUrl.pathname.startsWith('/dashboard')) {
  return NextResponse.redirect(new URL('/login', request.url))
}
```

### Issue: Server Component Shows Old Auth State

**Symptom**: After login, dashboard still shows "not logged in"

**Cause**: Server Component cached during build

**Solution**: Call `router.refresh()` after login

```typescript
async function handleLogin() {
  const { error } = await supabase.auth.signInWithPassword({ email, password })

  if (!error) {
    router.push('/dashboard')
    router.refresh() // Force Server Component to re-render with new auth state
  }
}
```

---

## Testing Checklist

- [ ] Access protected route while logged out → Redirects to login
- [ ] Log in → Redirects to original destination (or /dashboard)
- [ ] Access protected route while logged in → Page loads
- [ ] Logout → Can't access protected routes anymore
- [ ] Direct navigation to protected route → Auth check works
- [ ] Browser refresh on protected page → Stays authenticated
- [ ] No flash of protected content (middleware working)

---

## Related SOPs

- [Environment Setup](./environment-setup.md) - Supabase credentials
- [Adding New Page](./adding-new-page.md) - General page creation
- [Supabase Auth Redirect](../debugging/supabase-auth-redirect.md) - OAuth issues

---

## References

- [Next.js Middleware](https://nextjs.org/docs/app/building-your-application/routing/middleware)
- [Supabase Auth with Next.js](https://supabase.com/docs/guides/auth/server-side/nextjs)
- [Protected routes example (TASK-01)](../../tasks/TASK-01-auth-setup.md)

---

**Last Updated**: 2025-10-15
**Maintained By**: Development team
