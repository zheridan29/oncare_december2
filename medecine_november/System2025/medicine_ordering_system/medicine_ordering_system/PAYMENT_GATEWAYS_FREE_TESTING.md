# Payment Gateways - Free Testing & Sandbox Accounts Guide

## Overview

This guide identifies which payment gateways offer **free test/sandbox accounts** that you can use for development and testing without any cost or commitment.

---

## ✅ Best Options for Free Testing

### 1. **Stripe** ⭐⭐⭐⭐⭐ (HIGHLY RECOMMENDED)

**Free Testing Account**: ✅ **YES - Full Access**

**What You Get:**
- ✅ **100% Free** test account (no credit card required)
- ✅ Full API access in test mode
- ✅ Test card numbers provided
- ✅ Webhook testing tools (Stripe CLI)
- ✅ Complete documentation
- ✅ No time limits
- ✅ All features available in test mode

**Test Cards Available:**
```
Success: 4242 4242 4242 4242
Decline: 4000 0000 0000 0002
3D Secure: 4000 0025 0000 3155
```

**Setup:**
1. Go to https://stripe.com
2. Sign up for free account
3. Get test API keys immediately
4. No verification needed for test mode

**Limitations:**
- ❌ Test mode only (no real transactions)
- ❌ Test webhooks only
- ✅ Can switch to live mode anytime (requires verification)

**Best For**: Learning payment integration, testing, development

**Rating**: ⭐⭐⭐⭐⭐ Excellent for testing

---

### 2. **PayMongo** ⭐⭐⭐⭐ (RECOMMENDED for Philippines)

**Free Testing Account**: ✅ **YES - Full Access**

**What You Get:**
- ✅ **100% Free** test account
- ✅ Test API keys immediately
- ✅ Test mode for all payment methods (GCash, PayMaya, cards)
- ✅ Webhook testing support
- ✅ Good documentation
- ✅ No time limits

**Test Cards Available:**
```
Success: 4111 1111 1111 1111
Decline: 4000 0000 0000 0002
```

**Setup:**
1. Go to https://paymongo.com
2. Sign up for free account
3. Get test API keys from dashboard
4. No verification needed for test mode

**Limitations:**
- ❌ Test mode only (no real transactions)
- ❌ Requires business verification for live mode
- ✅ Can test all payment methods in sandbox

**Best For**: Philippines market testing, GCash/PayMaya integration

**Rating**: ⭐⭐⭐⭐ Very good for testing

---

### 3. **PayPal** ⭐⭐⭐⭐

**Free Testing Account**: ✅ **YES - Sandbox Accounts**

**What You Get:**
- ✅ **100% Free** sandbox accounts
- ✅ Create unlimited test accounts
- ✅ Test buyer and seller accounts
- ✅ Sandbox API credentials
- ✅ Webhook testing
- ✅ Good documentation

**Setup:**
1. Go to https://developer.paypal.com
2. Sign up for free developer account
3. Create sandbox business and personal accounts
4. Get sandbox API credentials

**Limitations:**
- ❌ Sandbox only (no real transactions)
- ❌ More complex setup than Stripe
- ❌ Requires business verification for live mode
- ✅ Can test full payment flow

**Best For**: International payment testing, PayPal-specific flows

**Rating**: ⭐⭐⭐⭐ Good for testing

---

### 4. **Square** ⭐⭐⭐

**Free Testing Account**: ✅ **YES - Sandbox**

**What You Get:**
- ✅ **100% Free** sandbox account
- ✅ Test API access
- ✅ Test card numbers
- ✅ Sandbox webhooks
- ✅ Documentation

**Setup:**
1. Go to https://squareup.com
2. Sign up for developer account
3. Access sandbox from developer dashboard

**Limitations:**
- ❌ Sandbox only
- ❌ Less comprehensive than Stripe
- ❌ Requires business verification for live

**Best For**: Retail/online unified testing

**Rating**: ⭐⭐⭐ Decent for testing

---

## ⚠️ Limited or No Free Testing

### 5. **GCash** ❌

**Free Testing Account**: ❌ **NO DIRECT API**

**Issue:**
- GCash doesn't offer public developer API
- No sandbox/test environment
- Must integrate through aggregators (PayMongo, etc.)

**Workaround:**
- ✅ Use **PayMongo** test mode (supports GCash)
- ✅ Test GCash payments through PayMongo sandbox

**Rating**: ❌ Not directly testable

---

### 6. **PayMaya** ⚠️

**Free Testing Account**: ⚠️ **LIMITED**

**Issue:**
- PayMaya Business requires business registration
- Limited public test environment
- Better to use through PayMongo aggregator

**Workaround:**
- ✅ Use **PayMongo** test mode (supports PayMaya wallet)
- ✅ Test PayMaya through PayMongo sandbox

**Rating**: ⚠️ Limited direct testing

---

### 7. **DragonPay** ⚠️

**Free Testing Account**: ⚠️ **REQUIRES MERCHANT ACCOUNT**

**Issue:**
- Requires merchant account application
- May have setup fees
- Test environment may require approval

**Best For**: Production use only (not ideal for initial testing)

**Rating**: ⚠️ Not ideal for free testing

---

## 🎯 Recommended Testing Strategy

### Phase 1: Learn & Develop (FREE)

**Use Stripe Test Mode:**
1. ✅ Sign up for free Stripe account
2. ✅ Get test API keys immediately
3. ✅ Build payment integration
4. ✅ Test all payment flows
5. ✅ Test webhooks with Stripe CLI
6. ✅ **Cost: $0**

**Why Stripe First:**
- Best documentation
- Easiest to set up
- Most comprehensive test environment
- Can learn payment integration concepts
- Code can be adapted to other gateways

---

### Phase 2: Philippines-Specific Testing (FREE)

**Use PayMongo Test Mode:**
1. ✅ Sign up for free PayMongo account
2. ✅ Get test API keys
3. ✅ Test GCash, PayMaya, card payments
4. ✅ Test webhooks
5. ✅ **Cost: $0**

**Why PayMongo:**
- Supports multiple Philippines payment methods
- Single API for all methods
- Good for testing local payment flows

---

### Phase 3: Production (When Ready)

**Choose Based on Market:**
- **Philippines**: PayMongo (live account)
- **International**: Stripe (live account)
- **PayPal Users**: PayPal (live account)

---

## 💰 Cost Comparison for Testing

| Gateway | Test Account | Setup Fee | Monthly Fee | Transaction Fee (Test) |
|---------|-------------|-----------|-------------|------------------------|
| **Stripe** | ✅ Free | $0 | $0 | $0 (test mode) |
| **PayMongo** | ✅ Free | $0 | $0 | $0 (test mode) |
| **PayPal** | ✅ Free | $0 | $0 | $0 (sandbox) |
| **Square** | ✅ Free | $0 | $0 | $0 (sandbox) |
| **GCash** | ❌ N/A | N/A | N/A | Use PayMongo |
| **PayMaya** | ⚠️ Limited | Varies | Varies | Use PayMongo |
| **DragonPay** | ⚠️ Requires Account | Varies | Varies | Varies |

---

## 🚀 Quick Start: Free Testing Setup

### Option 1: Stripe (Recommended for Learning)

```bash
# 1. Sign up at https://stripe.com (free)
# 2. Get test API keys from dashboard
# 3. Install SDK
pip install stripe

# 4. Use test keys
STRIPE_PUBLIC_KEY = "pk_test_..."
STRIPE_SECRET_KEY = "sk_test_..."
```

**Test Card**: `4242 4242 4242 4242` (any future date, any CVC)

**Webhook Testing**: Use Stripe CLI (free)
```bash
stripe listen --forward-to localhost:8000/webhooks/stripe/
```

---

### Option 2: PayMongo (Recommended for Philippines)

```bash
# 1. Sign up at https://paymongo.com (free)
# 2. Get test API keys from dashboard
# 3. Install SDK
pip install paymongo

# 4. Use test keys
PAYMONGO_PUBLIC_KEY = "pk_test_..."
PAYMONGO_SECRET_KEY = "sk_test_..."
```

**Test Card**: `4111 1111 1111 1111` (any future date, any CVC)

**Webhook Testing**: Use ngrok (free) or PayMongo webhook testing

---

### Option 3: PayPal (For International Testing)

```bash
# 1. Sign up at https://developer.paypal.com (free)
# 2. Create sandbox app
# 3. Get sandbox credentials
# 4. Install SDK
pip install paypalrestsdk

# 5. Use sandbox credentials
PAYPAL_CLIENT_ID = "sandbox_client_id"
PAYPAL_CLIENT_SECRET = "sandbox_client_secret"
PAYPAL_MODE = "sandbox"
```

**Test Accounts**: Create unlimited sandbox buyer/seller accounts

---

## 📋 Testing Checklist

### What You Can Test for FREE:

✅ **Payment Processing**
- Create payment intents
- Process test payments
- Handle payment success/failure
- Test different card types

✅ **Webhooks**
- Receive webhook callbacks
- Test webhook signature verification
- Handle different webhook events

✅ **Error Handling**
- Test declined cards
- Test network failures
- Test invalid data
- Test timeout scenarios

✅ **Refunds**
- Process test refunds
- Partial refunds
- Refund status tracking

✅ **Payment Methods**
- Credit/debit cards
- Digital wallets (through aggregators)
- Multiple currencies (test mode)

❌ **What You CANNOT Test:**
- Real money transactions
- Actual bank settlements
- Real customer payments
- Production-level performance
- Real fraud detection

---

## 🎓 Learning Path Recommendation

### Week 1: Stripe Test Mode (FREE)
1. Sign up for free Stripe account
2. Complete Stripe integration tutorial
3. Build payment flow
4. Test all scenarios
5. **Cost: $0**

### Week 2: PayMongo Test Mode (FREE)
1. Sign up for free PayMongo account
2. Integrate PayMongo API
3. Test GCash/PayMaya flows
4. Test webhooks
5. **Cost: $0**

### Week 3: Combine & Test (FREE)
1. Test both gateways
2. Compare implementations
3. Choose best for production
4. **Cost: $0**

### When Ready for Production:
1. Choose gateway based on market
2. Complete business verification
3. Switch to live mode
4. Start accepting real payments

---

## 🔒 Security Note for Testing

**Important**: Even in test mode:
- ✅ Never commit test API keys to public repositories
- ✅ Use environment variables
- ✅ Treat test keys like production keys
- ✅ Rotate keys if exposed
- ✅ Use `.env` files (add to `.gitignore`)

---

## 📊 Summary: Best Free Testing Options

### For Learning & Development:
1. **Stripe** ⭐⭐⭐⭐⭐ - Best overall
2. **PayMongo** ⭐⭐⭐⭐ - Best for Philippines
3. **PayPal** ⭐⭐⭐⭐ - Good for international

### For Philippines Market:
1. **PayMongo** ⭐⭐⭐⭐ - Supports GCash, PayMaya, cards
2. **Stripe** ⭐⭐⭐ - Can test card payments

### For International Market:
1. **Stripe** ⭐⭐⭐⭐⭐ - Best developer experience
2. **PayPal** ⭐⭐⭐⭐ - Popular payment method

---

## ✅ Final Recommendation

**Start with Stripe Test Mode:**
- ✅ 100% free
- ✅ No credit card required
- ✅ Best documentation
- ✅ Easiest to learn
- ✅ Can adapt code to other gateways later

**Then add PayMongo Test Mode:**
- ✅ 100% free
- ✅ Test Philippines payment methods
- ✅ Single API for multiple methods
- ✅ Good for local market

**Total Cost for Testing: $0** 💰

---

## 🚀 Next Steps

1. **Sign up for Stripe** (5 minutes)
   - https://stripe.com
   - Get test API keys
   - Start building

2. **Sign up for PayMongo** (5 minutes)
   - https://paymongo.com
   - Get test API keys
   - Test Philippines methods

3. **Build Integration** (Free)
   - Use test mode
   - No costs
   - Learn payment processing

4. **Switch to Live** (When Ready)
   - Complete verification
   - Start accepting real payments
   - Pay transaction fees only

---

**Last Updated**: December 2025  
**Status**: All information verified for free testing accounts


