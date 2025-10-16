# Project Architecture - Next.js SaaS

**Project**: AI Content Generator SaaS
**Tech Stack**: Next.js 15 (App Router), Tailwind, Supabase, Stripe
**Updated**: 2025-10-15

---

## Overview

This is a SaaS application for AI-powered content generation with a credit-based payment system.

**Core Features**:
- User authentication (email + OAuth)
- AI content generation (OpenAI GPT-4)
- Credits system (purchase, consume, track)
- Payment processing (Stripe Checkout)

---

## Technology Stack

### Frontend
- **Framework**: Next.js 15 (App Router, React 19)
- **Rendering**: Server-Side Rendering (SSR) with Server Components
- **Styling**: Tailwind CSS
- **TypeScript**: Strict mode enabled

### Backend
- **Runtime**: Node.js (via Next.js API Routes)
- **Database**: PostgreSQL (via Supabase)
- **Auth**: Supabase Auth (email + OAuth)
- **File Storage**: Supabase Storage (for user uploads)

### Third-Party Services
- **Payments**: Stripe (Checkout + Webhooks)
- **AI**: OpenAI API (GPT-4)
- **Hosting**: Vercel (frontend + serverless functions)
- **Database Hosting**: Supabase Cloud

---

## Folder Structure

```
nextjs-saas/
├── app/                          # Next.js App Router
│   ├── (auth)/                   # Auth route group (no layout)
│   │   ├── login/
│   │   │   └── page.tsx          # Login page (Client Component)
│   │   ├── signup/
│   │   │   └── page.tsx          # Signup page (Client Component)
│   │   └── auth/
│   │       └── callback/
│   │           └── route.ts      # OAuth callback handler
│   │
│   ├── (dashboard)/              # Dashboard route group (with layout)
│   │   ├── layout.tsx            # Dashboard layout (sidebar, header)
│   │   ├── dashboard/
│   │   │   └── page.tsx          # Dashboard home
│   │   ├── generate/
│   │   │   └── page.tsx          # AI generation page
│   │   ├── credits/
│   │   │   ├── page.tsx          # Purchase credits
│   │   │   └── history/
│   │   │       └── page.tsx      # Payment history
│   │   └── settings/
│   │       └── page.tsx          # User settings
│   │
│   ├── api/                      # API routes
│   │   ├── checkout/
│   │   │   └── route.ts          # Create Stripe Checkout session
│   │   ├── generate/
│   │   │   └── route.ts          # AI generation endpoint
│   │   └── webhooks/
│   │       └── stripe/
│   │           └── route.ts      # Stripe webhook handler
│   │
│   ├── layout.tsx                # Root layout
│   ├── page.tsx                  # Landing page
│   └── globals.css               # Tailwind imports
│
├── components/                   # React components
│   ├── ui/                       # UI primitives (buttons, inputs)
│   ├── dashboard/                # Dashboard-specific components
│   └── landing/                  # Landing page components
│
├── utils/                        # Utility functions
│   ├── supabase/
│   │   ├── server.ts             # Server-side Supabase client
│   │   └── client.ts             # Client-side Supabase client
│   ├── stripe.ts                 # Stripe utilities
│   └── openai.ts                 # OpenAI utilities
│
├── lib/                          # Business logic
│   ├── credits.ts                # Credit management functions
│   ├── ai.ts                     # AI generation logic
│   └── db.ts                     # Database helpers
│
├── middleware.ts                 # Route protection
├── .env.local                    # Environment variables (git-ignored)
├── next.config.js                # Next.js configuration
├── tailwind.config.ts            # Tailwind configuration
├── tsconfig.json                 # TypeScript configuration
└── package.json                  # Dependencies
```

---

## Data Flow

### Authentication Flow

```
┌─────────────┐
│   Browser   │
└──────┬──────┘
       │
       │ 1. Navigate to /dashboard
       │
       ▼
┌──────────────┐
│  Middleware  │ (runs BEFORE page render)
└──────┬───────┘
       │
       │ 2. Check auth cookie via Supabase
       │
       ▼
   Authenticated?
       │
       ├─ No ──► Redirect to /login
       │
       └─ Yes ─► Render /dashboard
```

### AI Generation Flow

```
┌─────────────┐
│   Browser   │ (User clicks "Generate")
└──────┬──────┘
       │
       │ 1. POST /api/generate { prompt: "..." }
       │
       ▼
┌──────────────┐
│  API Route   │ (/api/generate/route.ts)
└──────┬───────┘
       │
       │ 2. Verify user authenticated
       │ 3. Check user has credits
       │
       ▼
┌──────────────┐
│  OpenAI API  │ (GPT-4 generation)
└──────┬───────┘
       │
       │ 4. Stream response back
       │
       ▼
┌──────────────┐
│   Database   │ (Deduct credits, log usage)
└──────┬───────┘
       │
       │ 5. Return generated content
       │
       ▼
┌─────────────┐
│   Browser   │ (Display result)
└─────────────┘
```

### Payment Flow

```
┌─────────────┐
│   Browser   │ (User clicks "Purchase 100 credits")
└──────┬──────┘
       │
       │ 1. POST /api/checkout { priceId: "price_xxx" }
       │
       ▼
┌──────────────┐
│  API Route   │ (/api/checkout/route.ts)
└──────┬───────┘
       │
       │ 2. Create Stripe Checkout session
       │    metadata: { user_id: "..." }
       │
       ▼
┌──────────────┐
│    Stripe    │ (Checkout page)
└──────┬───────┘
       │
       │ 3. User enters card, pays
       │
       ▼
┌──────────────┐
│    Stripe    │ (Sends webhook event)
└──────┬───────┘
       │
       │ 4. POST /api/webhooks/stripe
       │    event: checkout.session.completed
       │
       ▼
┌──────────────┐
│  Webhook     │ (Verify signature, add credits)
└──────┬───────┘
       │
       │ 5. Update database (add credits)
       │
       ▼
┌──────────────┐
│   Database   │ (User balance updated)
└──────┬───────┘
       │
       │ 6. Redirect to success page
       │
       ▼
┌─────────────┐
│   Browser   │ (Show success, new balance)
└─────────────┘
```

---

## Database Schema

### Tables

**users** (Supabase Auth table):
```sql
id          UUID PRIMARY KEY
email       TEXT UNIQUE NOT NULL
created_at  TIMESTAMP
```

**user_credits**:
```sql
user_id     UUID PRIMARY KEY REFERENCES auth.users(id)
balance     INTEGER NOT NULL DEFAULT 0
created_at  TIMESTAMP
updated_at  TIMESTAMP
```

**credit_transactions**:
```sql
id                  UUID PRIMARY KEY
user_id             UUID REFERENCES auth.users(id)
amount              INTEGER NOT NULL          -- positive = added, negative = consumed
description         TEXT
stripe_session_id   TEXT UNIQUE               -- for payments, NULL for usage
created_at          TIMESTAMP
```

**generations** (AI generation history):
```sql
id          UUID PRIMARY KEY
user_id     UUID REFERENCES auth.users(id)
prompt      TEXT NOT NULL
output      TEXT NOT NULL
credits_used INTEGER NOT NULL
created_at  TIMESTAMP
```

### Row-Level Security (RLS)

**user_credits**:
```sql
-- Users can only read their own credits
CREATE POLICY "Users can view own credits"
ON user_credits FOR SELECT
USING (auth.uid() = user_id);

-- Only server can update credits (via service role)
CREATE POLICY "Service can update credits"
ON user_credits FOR UPDATE
USING (auth.role() = 'service_role');
```

**credit_transactions**:
```sql
-- Users can only see their own transactions
CREATE POLICY "Users can view own transactions"
ON credit_transactions FOR SELECT
USING (auth.uid() = user_id);

-- Only server can insert transactions
CREATE POLICY "Service can insert transactions"
ON credit_transactions FOR INSERT
WITH CHECK (auth.role() = 'service_role');
```

---

## Environment Variables

### Required (All Environments)

```env
# Next.js
NEXT_PUBLIC_APP_URL=http://localhost:3000  # or https://yourdomain.com

# Supabase
NEXT_PUBLIC_SUPABASE_URL=https://xxx.supabase.co
NEXT_PUBLIC_SUPABASE_ANON_KEY=eyJxxx...
SUPABASE_SERVICE_ROLE_KEY=eyJxxx...  # Server-side only, DO NOT expose to client

# Stripe
NEXT_PUBLIC_STRIPE_PUBLISHABLE_KEY=pk_test_xxx
STRIPE_SECRET_KEY=sk_test_xxx
STRIPE_WEBHOOK_SECRET=whsec_xxx  # Different for local vs production

# OpenAI
OPENAI_API_KEY=sk-proj-xxx
```

### Local vs Production Differences

| Variable | Local | Production |
|----------|-------|------------|
| `NEXT_PUBLIC_APP_URL` | `http://localhost:3000` | `https://yourdomain.com` |
| `STRIPE_WEBHOOK_SECRET` | From Stripe CLI (`whsec_xxx`) | From Stripe Dashboard |
| Stripe keys | `pk_test_xxx` / `sk_test_xxx` | `pk_live_xxx` / `sk_live_xxx` |

---

## Server Components vs Client Components

### When to Use Server Components (Default)

**Use for**:
- Pages that don't need interactivity
- Data fetching from database
- Calling APIs with secrets
- SEO-critical pages

**Example**:
```typescript
// app/(dashboard)/dashboard/page.tsx
import { createClient } from '@/utils/supabase/server'

export default async function DashboardPage() {
  const supabase = createClient()
  const { data: credits } = await supabase
    .from('user_credits')
    .select('balance')
    .single()

  return <div>Credits: {credits.balance}</div>
}
```

### When to Use Client Components ('use client')

**Use for**:
- Interactive UI (buttons, forms, modals)
- React hooks (useState, useEffect, etc.)
- Browser APIs (localStorage, window, etc.)
- Event handlers (onClick, onChange, etc.)

**Example**:
```typescript
// app/(auth)/login/page.tsx
'use client'

import { useState } from 'react'

export default function LoginPage() {
  const [email, setEmail] = useState('')

  async function handleSubmit(e) {
    e.preventDefault()
    // ... login logic
  }

  return <form onSubmit={handleSubmit}>...</form>
}
```

### Mixed (Layout with Server + Client Children)

**Layout** (Server Component):
```typescript
// app/(dashboard)/layout.tsx
import { createClient } from '@/utils/supabase/server'
import { Sidebar } from '@/components/dashboard/Sidebar'

export default async function DashboardLayout({ children }) {
  const supabase = createClient()
  const { data: user } = await supabase.auth.getUser()

  return (
    <div>
      <Sidebar user={user} />  {/* Pass data to Client Component */}
      {children}
    </div>
  )
}
```

**Sidebar** (Client Component):
```typescript
// components/dashboard/Sidebar.tsx
'use client'

export function Sidebar({ user }) {
  const [isOpen, setIsOpen] = useState(false)

  return <nav>...</nav>
}
```

---

## API Routes Best Practices

### Pattern: Authentication Check

```typescript
// app/api/protected/route.ts
import { createClient } from '@/utils/supabase/server'
import { NextResponse } from 'next/server'

export async function GET() {
  const supabase = createClient()
  const { data: { user }, error } = await supabase.auth.getUser()

  if (error || !user) {
    return NextResponse.json({ error: 'Unauthorized' }, { status: 401 })
  }

  // ... protected logic
}
```

### Pattern: Error Handling

```typescript
export async function POST(request: Request) {
  try {
    const body = await request.json()

    // Validate input
    if (!body.prompt || body.prompt.length < 10) {
      return NextResponse.json(
        { error: 'Prompt must be at least 10 characters' },
        { status: 400 }
      )
    }

    // Business logic
    const result = await generateContent(body.prompt)

    return NextResponse.json({ result })
  } catch (error) {
    console.error('API error:', error)

    return NextResponse.json(
      { error: 'Internal server error' },
      { status: 500 }
    )
  }
}
```

### Pattern: Streaming Responses

```typescript
// app/api/generate/route.ts
export async function POST(request: Request) {
  const { prompt } = await request.json()

  const encoder = new TextEncoder()

  const stream = new ReadableStream({
    async start(controller) {
      const openai = new OpenAI()

      const completion = await openai.chat.completions.create({
        model: 'gpt-4',
        messages: [{ role: 'user', content: prompt }],
        stream: true,
      })

      for await (const chunk of completion) {
        const text = chunk.choices[0]?.delta?.content || ''
        controller.enqueue(encoder.encode(text))
      }

      controller.close()
    },
  })

  return new Response(stream, {
    headers: { 'Content-Type': 'text/plain' },
  })
}
```

---

## Deployment Strategy

### Vercel Deployment

**Automatic deploys**:
- Push to `main` branch → Production deploy
- Push to feature branch → Preview deploy

**Environment variables**:
- Set in Vercel dashboard
- Separate values for Preview vs Production
- Stripe webhook secret MUST be different per environment

**Build settings**:
- Framework: Next.js
- Build command: `npm run build`
- Output directory: `.next` (auto-detected)

### Database Migrations

**Supabase**:
- Migrations run in Supabase dashboard
- Or via Supabase CLI: `supabase db push`
- Always test in staging project first

---

## Performance Considerations

### Server Components
- Reduce client JavaScript bundle
- Faster initial page load
- Better SEO

### Caching Strategy
- Static pages cached at edge (Vercel)
- Dynamic data via Server Components (fresh on request)
- Client-side caching for user data (SWR or React Query)

### Database Optimization
- Indexes on `user_id` (all tables)
- Index on `stripe_session_id` (idempotency checks)
- Connection pooling (Supabase handles automatically)

---

## Security Considerations

### Authentication
- ✅ Middleware protects routes
- ✅ Server Components verify auth
- ✅ API routes check auth
- ✅ Database RLS enforces user isolation

### Payments
- ✅ Webhook signature verification
- ✅ Idempotency checks (prevent duplicate credits)
- ✅ Server-side fulfillment (don't trust client)
- ✅ Stripe handles PCI compliance

### API Keys
- ✅ Never expose secrets to client
- ✅ Environment variables for all keys
- ✅ `.env.local` git-ignored
- ✅ Separate keys for test vs production

---

## Monitoring & Logging

### Application Logs
- Vercel dashboard → Logs
- Real-time function logs
- Error tracking (consider Sentry)

### Stripe Webhooks
- Stripe dashboard → Webhooks → Endpoint
- View delivery attempts
- Retry failed webhooks

### Database
- Supabase dashboard → Table Editor
- Query performance
- Connection stats

---

## Related Documentation

- [Task: Authentication Setup](../tasks/TASK-01-auth-setup.md)
- [Task: Stripe Integration](../tasks/TASK-04-stripe-integration.md)
- [SOP: Adding Protected Routes](../sops/development/adding-protected-routes.md)
- [SOP: Stripe Webhooks](../sops/integrations/stripe-webhooks.md)

---

**Last Updated**: 2025-10-15
**Architecture Version**: 1.0
