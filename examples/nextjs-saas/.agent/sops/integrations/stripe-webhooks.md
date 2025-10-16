# SOP: Stripe Webhooks Setup

**Category**: Integrations
**Created**: 2025-10-15 (from TASK-04)
**Last Used**: TASK-04
**Tech Stack**: Next.js 15, Stripe SDK, Stripe CLI

---

## When to Use This SOP

Use this when you need to:
- Set up Stripe webhook handling
- Test webhooks locally
- Deploy webhooks to production
- Debug webhook issues
- Add new webhook event handlers

---

## Prerequisites

- [x] Stripe account created (test mode OK for development)
- [x] Stripe SDK installed (`npm install stripe`)
- [x] Stripe CLI installed (for local testing)
- [x] Environment variables configured

---

## Quick Reference

**Local Development**:
1. Run `stripe listen --forward-to localhost:3000/api/webhooks/stripe`
2. Use webhook secret from CLI output
3. Test with `stripe trigger checkout.session.completed`

**Production**:
1. Create webhook endpoint in Stripe dashboard
2. Use webhook secret from dashboard
3. Point to `https://yourdomain.com/api/webhooks/stripe`

---

## Step-by-Step Setup

### Part 1: Local Development

#### Step 1: Install Stripe CLI

**macOS**:
```bash
brew install stripe/stripe-cli/stripe
```

**Linux**:
```bash
wget https://github.com/stripe/stripe-cli/releases/latest/download/stripe_linux_x86_64.tar.gz
tar -xvf stripe_linux_x86_64.tar.gz
sudo mv stripe /usr/local/bin
```

**Windows**:
```bash
scoop install stripe
```

#### Step 2: Authenticate Stripe CLI

```bash
stripe login
```

This opens browser to authorize CLI access to your Stripe account.

#### Step 3: Forward Webhooks to Localhost

```bash
stripe listen --forward-to localhost:3000/api/webhooks/stripe
```

**Output**:
```
> Ready! Your webhook signing secret is whsec_xxxxxxxxxxxxxxxxxxxxxxxx (^C to quit)
```

**Copy this secret** → Add to `.env.local`:
```env
STRIPE_WEBHOOK_SECRET=whsec_xxxxxxxxxxxxxxxxxxxxxxxx
```

**Why forward?**
- Stripe can't reach `localhost` directly
- CLI creates secure tunnel
- Receives real webhook events

#### Step 4: Test Webhook with Sample Event

**In another terminal**:
```bash
# Trigger test event
stripe trigger checkout.session.completed

# Or send custom event
stripe trigger payment_intent.succeeded --add customer=cus_xxx
```

**Check your app logs** to verify webhook received and processed.

---

### Part 2: Create Webhook Handler

#### Step 1: Create API Route

**File**: `app/api/webhooks/stripe/route.ts`

```typescript
import { NextResponse } from 'next/server'
import Stripe from 'stripe'

const stripe = new Stripe(process.env.STRIPE_SECRET_KEY!, {
  apiVersion: '2023-10-16',
})

export async function POST(request: Request) {
  // Step 1: Get raw body and signature
  const body = await request.text()
  const sig = request.headers.get('stripe-signature')!

  let event: Stripe.Event

  try {
    // Step 2: Verify webhook signature
    event = stripe.webhooks.constructEvent(
      body,
      sig,
      process.env.STRIPE_WEBHOOK_SECRET!
    )
  } catch (err) {
    console.error('⚠️ Webhook signature verification failed:', err.message)
    return NextResponse.json(
      { error: 'Invalid signature' },
      { status: 400 }
    )
  }

  // Step 3: Handle different event types
  try {
    switch (event.type) {
      case 'checkout.session.completed':
        await handleCheckoutCompleted(event.data.object as Stripe.Checkout.Session)
        break

      case 'payment_intent.succeeded':
        await handlePaymentSucceeded(event.data.object as Stripe.PaymentIntent)
        break

      case 'payment_intent.payment_failed':
        await handlePaymentFailed(event.data.object as Stripe.PaymentIntent)
        break

      default:
        console.log(`Unhandled event type: ${event.type}`)
    }

    return NextResponse.json({ received: true })
  } catch (err) {
    console.error(`❌ Webhook handler failed for ${event.type}:`, err)
    return NextResponse.json(
      { error: 'Handler failed' },
      { status: 500 }
    )
  }
}

async function handleCheckoutCompleted(session: Stripe.Checkout.Session) {
  console.log('✅ Checkout completed:', session.id)

  // Your business logic here
  // e.g., add credits, send email, update database
}

async function handlePaymentSucceeded(paymentIntent: Stripe.PaymentIntent) {
  console.log('✅ Payment succeeded:', paymentIntent.id)
}

async function handlePaymentFailed(paymentIntent: Stripe.PaymentIntent) {
  console.log('❌ Payment failed:', paymentIntent.id)
}
```

**Why verify signature?**
- Anyone can POST to your webhook URL
- Signature proves event came from Stripe
- Prevents fake events

#### Step 2: Implement Idempotency

**Problem**: Stripe may send same event multiple times

**Solution**: Check if already processed

```typescript
async function handleCheckoutCompleted(session: Stripe.Checkout.Session) {
  const supabase = createClient()

  // Check if already processed
  const { data: existing } = await supabase
    .from('credit_transactions')
    .select('id')
    .eq('stripe_session_id', session.id)
    .single()

  if (existing) {
    console.log(`⏭️ Session ${session.id} already processed, skipping`)
    return
  }

  // Process payment (add credits, etc.)
  await addCreditsToUser(session.metadata.user_id, 100)

  // Record transaction
  await supabase.from('credit_transactions').insert({
    user_id: session.metadata.user_id,
    stripe_session_id: session.id,
    amount: 100,
    description: 'Purchased 100 credits',
  })

  console.log(`✅ Processed session ${session.id}`)
}
```

**Why idempotency matters**:
- Prevents duplicate credits
- Safe to retry on errors
- Stripe best practice

---

### Part 3: Production Deployment

#### Step 1: Create Webhook in Stripe Dashboard

1. Go to [Stripe Dashboard → Webhooks](https://dashboard.stripe.com/webhooks)
2. Click "Add endpoint"
3. Enter URL: `https://yourdomain.com/api/webhooks/stripe`
4. Select events to listen for:
   - `checkout.session.completed`
   - `payment_intent.succeeded`
   - `payment_intent.payment_failed`
5. Click "Add endpoint"

#### Step 2: Get Production Webhook Secret

In webhook details page:
- Copy "Signing secret" (starts with `whsec_`)
- Add to production environment variables

**Vercel**:
```bash
vercel env add STRIPE_WEBHOOK_SECRET production
# Paste secret when prompted
```

**Or in Vercel Dashboard**:
Settings → Environment Variables → Add:
- Name: `STRIPE_WEBHOOK_SECRET`
- Value: `whsec_xxxxxxxxxxxxxxxxxxxxxxxx`
- Environment: Production

#### Step 3: Test Production Webhook

**Stripe Dashboard → Webhooks → Your endpoint**:
1. Click "Send test webhook"
2. Select event type (e.g., `checkout.session.completed`)
3. Click "Send test webhook"
4. Check webhook logs to verify received

---

## Common Event Types

### checkout.session.completed

**When**: User completes Stripe Checkout

**Use for**:
- Add purchased credits
- Create user account
- Start subscription

**Data available**:
```typescript
session.id                    // Stripe session ID
session.customer              // Stripe customer ID
session.customer_email        // User email
session.metadata              // Your custom data
session.amount_total          // Total amount paid
session.payment_status        // 'paid' | 'unpaid'
```

### payment_intent.succeeded

**When**: Payment successfully processed

**Use for**:
- Confirm order
- Send receipt email
- Update order status

### payment_intent.payment_failed

**When**: Payment failed

**Use for**:
- Send failure email
- Log failed payment
- Retry logic (if applicable)

### customer.subscription.created

**When**: Subscription created

**Use for**:
- Grant subscription access
- Send welcome email
- Update user tier

### customer.subscription.deleted

**When**: Subscription canceled

**Use for**:
- Revoke subscription access
- Send cancellation email
- Update user tier

---

## Troubleshooting

### Issue: Signature Verification Failed

**Symptoms**:
```
⚠️ Webhook signature verification failed: No signatures found matching the expected signature for payload
```

**Causes**:
1. Using wrong webhook secret (local vs production)
2. Body modified before verification
3. Missing `stripe-signature` header

**Solutions**:

**Check secret**:
```bash
# Local (from Stripe CLI)
stripe listen --print-secret

# Production (from dashboard)
# Stripe Dashboard → Webhooks → Endpoint → Reveal signing secret
```

**Don't parse body before verification**:
```typescript
// ❌ Bad
const body = await request.json() // Parses body
event = stripe.webhooks.constructEvent(body, sig, secret) // Fails

// ✅ Good
const body = await request.text() // Raw body
event = stripe.webhooks.constructEvent(body, sig, secret) // Works
```

### Issue: Webhook Not Receiving Events

**Symptoms**: No webhook calls in logs

**Causes**:
1. Webhook URL incorrect
2. Firewall blocking Stripe
3. Stripe CLI not running (local)

**Solutions**:

**Check URL**:
```bash
# Should be publicly accessible (production)
curl https://yourdomain.com/api/webhooks/stripe
# Should return 405 Method Not Allowed (means endpoint exists)
```

**Check Stripe CLI (local)**:
```bash
stripe listen --forward-to localhost:3000/api/webhooks/stripe
# Should show "Ready! Your webhook signing secret is..."
```

**Check Stripe dashboard**:
Webhooks → Your endpoint → Attempts
- Shows delivery attempts
- Shows response codes
- Shows errors

### Issue: Duplicate Events

**Symptoms**: Same event processed multiple times

**Cause**: Stripe retries if your endpoint returns non-2xx

**Solution**: Implement idempotency (see above)

```typescript
// Check if already processed
const { data: existing } = await db.query(
  'SELECT id FROM transactions WHERE stripe_event_id = $1',
  [event.id]
)

if (existing) {
  console.log(`Event ${event.id} already processed`)
  return NextResponse.json({ received: true }) // Return 200 to stop retries
}
```

### Issue: Webhook Timeout

**Symptoms**: Stripe shows 504 timeout errors

**Cause**: Webhook handler takes >30 seconds

**Solution**: Process asynchronously

```typescript
// ❌ Bad (synchronous, slow)
export async function POST(request: Request) {
  const event = verifyWebhook(request)
  await processOrder(event) // Takes 2 minutes
  return NextResponse.json({ received: true })
}

// ✅ Good (async, fast)
export async function POST(request: Request) {
  const event = verifyWebhook(request)

  // Queue for background processing
  await queue.add('process-order', { eventId: event.id })

  // Return immediately
  return NextResponse.json({ received: true })
}
```

**Or use database queue**:
```typescript
// Insert to processing queue
await db.insert('webhook_queue', {
  event_id: event.id,
  event_type: event.type,
  payload: event,
  status: 'pending',
})

// Return 200 immediately
return NextResponse.json({ received: true })

// Separate worker processes queue
```

---

## Testing Checklist

- [ ] Local webhook receives events (Stripe CLI)
- [ ] Signature verification works
- [ ] Event handlers execute correctly
- [ ] Idempotency prevents duplicates
- [ ] Error handling returns proper status codes
- [ ] Production webhook configured in dashboard
- [ ] Production webhook receives events
- [ ] Logs show successful processing

---

## Monitoring & Logging

### Recommended Logging

```typescript
export async function POST(request: Request) {
  const eventId = crypto.randomUUID()

  console.log(`[${eventId}] Webhook received`)

  try {
    const event = stripe.webhooks.constructEvent(body, sig, secret)
    console.log(`[${eventId}] Event type: ${event.type}`)
    console.log(`[${eventId}] Event ID: ${event.id}`)

    // Handle event
    await handleEvent(event)

    console.log(`[${eventId}] ✅ Success`)
    return NextResponse.json({ received: true })
  } catch (error) {
    console.error(`[${eventId}] ❌ Error:`, error)
    return NextResponse.json({ error: error.message }, { status: 500 })
  }
}
```

### Stripe Dashboard Monitoring

**Webhooks → Your endpoint**:
- Attempts (all webhook deliveries)
- Response codes (2xx = success, 4xx/5xx = error)
- Retry attempts (failed deliveries)

**Set up alerts**:
- Email on webhook failures
- Slack/Discord on critical events

---

## Security Best Practices

### 1. Always Verify Signature

```typescript
// ✅ Required
event = stripe.webhooks.constructEvent(body, sig, secret)

// ❌ Never skip verification
const event = JSON.parse(body) // Accepts any payload!
```

### 2. Use HTTPS in Production

```
// ❌ Bad
http://yourdomain.com/api/webhooks/stripe

// ✅ Good
https://yourdomain.com/api/webhooks/stripe
```

### 3. Don't Trust Client-Side Success

```typescript
// ❌ Bad (client can fake this)
if (searchParams.get('success') === 'true') {
  addCreditsToUser() // INSECURE
}

// ✅ Good (server validates via webhook)
// Webhook receives checkout.session.completed
// Server verifies signature and processes
```

### 4. Store Webhook Secrets Securely

```
// ❌ Bad
const SECRET = 'whsec_xxx' // Hardcoded

// ✅ Good
const SECRET = process.env.STRIPE_WEBHOOK_SECRET // Environment variable
```

---

## Related SOPs

- [Stripe Integration](../../tasks/TASK-04-stripe-integration.md) - Full payment setup
- [Environment Setup](../development/environment-setup.md) - Stripe credentials

---

## References

- [Stripe Webhooks Guide](https://stripe.com/docs/webhooks)
- [Stripe CLI Documentation](https://stripe.com/docs/stripe-cli)
- [Webhook Best Practices](https://stripe.com/docs/webhooks/best-practices)

---

**Last Updated**: 2025-10-15
**Maintained By**: Development team
