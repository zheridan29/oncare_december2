# Step-by-Step Payment Gateway Setup Guide

## ✅ Migration Already Created!

The migration file exists: `0002_paymentgateway_transaction_payment_gateway.py`

You just need to **apply it** and configure the gateway in admin.

---

## Step 1: Apply Migration (1 minute) ⚙️

### Open Terminal/Command Prompt

**Navigate to your project directory:**
```bash
cd "C:\Users\Ace Z Gutierrez\Videos\Masteral November\medecine_november\System2025\medicine_ordering_system\medicine_ordering_system"
```

**Check if migration is already applied:**
```bash
python manage.py showmigrations transactions
```

**If you see `[ ] 0002_paymentgateway_transaction_payment_gateway`, apply it:**
```bash
python manage.py migrate transactions
```

**Expected Output:**
```
Operations to perform:
  Apply all migrations: transactions
Running migrations:
  Applying transactions.0002_paymentgateway_transaction_payment_gateway... OK
```

✅ **If you see `[X] 0002_...`**, the migration is already applied - skip to Step 2!

---

## Step 2: Install Stripe Package (30 seconds) 📦

```bash
pip install stripe==7.0.0
```

**Verify:**
```bash
python -c "import stripe; print('Stripe', stripe.__version__, 'installed successfully')"
```

**Expected Output:**
```
Stripe 7.0.0 installed successfully
```

✅ **Stripe installed!**

---

## Step 3: Get Stripe Test API Keys (FREE - 3 minutes) 🔑

### 3.1 Create Stripe Account

1. **Go to**: https://stripe.com
2. Click **"Sign in"** (or **"Create account"**)
3. **Fill in**:
   - Email address
   - Password
   - Country (Philippines or your country)
4. Click **"Create account"**
   - ✅ **NO CREDIT CARD REQUIRED!**

### 3.2 Get Test API Keys

1. **After login**, you'll see the Dashboard
2. **Click "Developers"** in the left sidebar
   - Or go directly to: https://dashboard.stripe.com/test/apikeys
3. **Verify "Test mode" toggle is ON** (orange/brown)
   - Should say "Test mode" at the top
4. **Find your keys**:
   
   **Publishable key:**
   - Starts with `pk_test_...`
   - Visible immediately
   - **Copy this key**
   
   **Secret key:**
   - Starts with `sk_test_...`
   - Click **"Reveal test key"** button to see it
   - **Copy this key**

### 3.3 Save Your Keys

**Example format** (yours will be different):
```
Publishable key: pk_test_51AbCdEfGhIjKlMnOpQrStUvWxYz1234567890AbCdEf
Secret key: sk_test_51AbCdEfGhIjKlMnOpQrStUvWxYz1234567890AbCdEf
```

**⚠️ Keep these safe** - you'll paste them into Django admin in Step 4.

---

## Step 4: Configure Gateway in Django Admin (2 minutes) 🎛️

### 4.1 Start Django Server

**In your terminal:**
```bash
python manage.py runserver
```

**You should see:**
```
Starting development server at http://127.0.0.1:8000/
```

✅ **Server running!**

### 4.2 Open Admin Panel

1. **Open browser**
2. **Go to**: http://127.0.0.1:8000/admin/
3. **Login** with your admin username and password

### 4.3 Navigate to Payment Gateways

1. **Find "TRANSACTIONS" section** in the admin dashboard
2. **Look for "Payment Gateways"** link
3. **Click "Payment Gateways"**

### 4.4 Add New Payment Gateway

1. **Click "Add Payment Gateway"** button (top right, green button)

2. **Fill in the form** exactly as shown:

   ```
   ┌─────────────────────────────────────────────────┐
   │ Basic Information                                │
   ├─────────────────────────────────────────────────┤
   │ Name:                                           │
   │ [Stripe Test                          ]         │
   │                                                  │
   │ Gateway Type:                                    │
   │ [Stripe ▼]                                       │
   │    Options:                                      │
   │    - Stripe                                      │
   │    - PayMongo                                    │
   │    - PayPal                                      │
   │    - etc.                                        │
   │                                                  │
   │ Description: (optional)                          │
   │ [Stripe payment gateway for testing    ]        │
   └─────────────────────────────────────────────────┘
   
   ┌─────────────────────────────────────────────────┐
   │ Status                                           │
   ├─────────────────────────────────────────────────┤
   │ ☑ Is Active                                     │
   │    ↑ CHECK THIS BOX (only one can be active)    │
   │                                                  │
   │ ☑ Is Test Mode                                  │
   │    ↑ CHECK THIS BOX (for test/sandbox mode)     │
   └─────────────────────────────────────────────────┘
   
   ┌─────────────────────────────────────────────────┐
   │ API Credentials                                  │
   ├─────────────────────────────────────────────────┤
   │ API Key Public:                                  │
   │ [pk_test_51AbCdEfGhIjKlMnOpQrStUvWx...]         │
   │ ↑ Paste your Publishable key here               │
   │                                                  │
   │ API Key Secret:                                  │
   │ [sk_test_51AbCdEfGhIjKlMnOpQrStUvWx...]         │
   │ ↑ Paste your Secret key here                    │
   │                                                  │
   │ Webhook Secret:                                  │
   │ [                                    ]           │
   │ ↑ Leave empty for now                           │
   └─────────────────────────────────────────────────┘
   
   ┌─────────────────────────────────────────────────┐
   │ Additional Configuration                         │
   ├─────────────────────────────────────────────────┤
   │ Config:                                          │
   │ [{}                                    ]         │
   │ ↑ Leave as empty JSON or use {}                 │
   └─────────────────────────────────────────────────┘
   ```

3. **Click "SAVE"** button (bottom right)

### 4.5 Verify Configuration

**After clicking Save, you should see:**

```
✅ Success!
Payment Gateway 'Stripe Test' was added successfully.
```

**In the Payment Gateways list, you should see:**

```
┌────────────────────────────────────────────────────────┐
│ Payment Gateways                                       │
├────────────────────────────────────────────────────────┤
│ Name        │ Type   │ Status │ Mode      │ Config    │
├─────────────┼────────┼────────┼───────────┼───────────┤
│ Stripe Test │ Stripe │ ●Active│ TEST MODE │ ✓Config'd │
└────────────────────────────────────────────────────────┘
```

**Verify:**
- ✅ **Status**: Shows green dot "● Active"
- ✅ **Mode**: Shows orange "TEST MODE"
- ✅ **Configuration**: Shows green checkmark "✓ Configured"

---

## Step 5: Test the Setup (1 minute) ✅

### Option A: Quick Test Script

**Run the verification script:**
```bash
python setup_payment_gateway.py
```

**Expected Output:**
```
============================================================
Payment Gateway Setup Verification
============================================================

1. Checking Stripe installation...
   ✅ Stripe installed (version 7.0.0)

2. Checking PaymentGateway model...
   ✅ PaymentGateway model exists (1 gateway(s) configured)

3. Checking active payment gateway...
   ✅ Active Gateway: Stripe Test
      Type: Stripe
      Mode: TEST
      Configured: Yes

4. Testing payment service creation...
   ✅ Payment service created: StripePaymentService

============================================================
Setup Check Complete!
============================================================
```

### Option B: Test in Django Shell

```bash
python manage.py shell
```

Then run:
```python
from transactions.services import PaymentGatewayFactory

# Get active gateway
gateway = PaymentGatewayFactory.get_active_gateway()
print(f"Active: {gateway.name if gateway else 'None'}")

# Create service
service = PaymentGatewayFactory.create_service()
print(f"Service: {service.__class__.__name__ if service else 'None'}")
```

**Expected Output:**
```
Active: Stripe Test
Service: StripePaymentService
```

---

## ✅ Setup Complete!

You've successfully:
- ✅ Applied the migration
- ✅ Installed Stripe package
- ✅ Got free Stripe test API keys
- ✅ Configured payment gateway in admin
- ✅ Verified the setup works

---

## What's Next? 🚀

### 1. Test Payment Processing (Optional)

You can test creating a payment intent:

```python
from transactions.services import PaymentGatewayFactory
from orders.models import Order
from decimal import Decimal

# Get service
service = PaymentGatewayFactory.create_service()

# Get an order
order = Order.objects.first()

# Create payment intent
result = service.create_payment_intent(
    order=order,
    amount=order.total_amount,
    currency='PHP'
)

print(f"Payment Intent: {result['payment_intent_id']}")
```

### 2. Use in Your Code

Now you can use the payment service anywhere in your code:

```python
from transactions.services import PaymentGatewayFactory

# Get active payment service
payment_service = PaymentGatewayFactory.create_service()

# Use it to process payments
# ... (your payment processing code)
```

### 3. Switch Gateways Later

When you want to add PayMongo or another gateway:
1. Go to Admin → Payment Gateways
2. Add new gateway with its API keys
3. Activate it (old one auto-deactivates)

---

## Troubleshooting 🔧

### Issue: "No module named 'stripe'"

**Fix:**
```bash
pip install stripe==7.0.0
```

### Issue: Payment Gateway not showing in admin

**Fix:**
1. Check migration applied: `python manage.py migrate transactions`
2. Restart server: Stop (Ctrl+C) and run `python manage.py runserver` again
3. Hard refresh browser: Ctrl+F5

### Issue: Gateway shows "Not Configured"

**Fix:**
1. Make sure you entered the **Secret Key** (sk_test_...)
2. Check for extra spaces when copying
3. Edit the gateway and re-save

### Issue: Cannot find "Payment Gateways" in admin

**Fix:**
1. Make sure migration is applied
2. Check if PaymentGateway model exists in `transactions/models.py`
3. Restart Django server

---

## Quick Command Reference

```bash
# Apply migration
python manage.py migrate transactions

# Install Stripe
pip install stripe==7.0.0

# Run server
python manage.py runserver

# Test setup
python setup_payment_gateway.py

# Django shell
python manage.py shell
```

---

## Summary Checklist ✅

- [ ] Step 1: Migration applied
- [ ] Step 2: Stripe installed
- [ ] Step 3: Stripe test account created
- [ ] Step 3: API keys obtained
- [ ] Step 4: Gateway configured in admin
- [ ] Step 4: Gateway shows as Active and Configured
- [ ] Step 5: Verification script passes

---

**All done!** Your payment gateway is now configured and ready to use! 🎉

For detailed information, see:
- `PAYMENT_GATEWAY_SETUP_GUIDE.md` - Comprehensive guide
- `QUICK_START_PAYMENT_GATEWAY.md` - Quick reference
- `PAYMENT_SERVICE_IMPLEMENTATION.md` - Technical details

