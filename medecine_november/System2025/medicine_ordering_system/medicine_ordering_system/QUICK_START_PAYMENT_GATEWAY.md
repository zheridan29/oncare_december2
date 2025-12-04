# Quick Start: Payment Gateway Setup

## 🚀 Step-by-Step Setup (5 Minutes)

---

## Step 1: Create Migration ⚙️

**Open Terminal/Command Prompt** in your project directory:

```bash
# Navigate to project directory
cd "C:\Users\Ace Z Gutierrez\Videos\Masteral November\medecine_november\System2025\medicine_ordering_system\medicine_ordering_system"

# Create migration
python manage.py makemigrations transactions

# Apply migration
python manage.py migrate transactions
```

**Expected Output:**
```
Migrations for 'transactions':
  transactions/migrations/XXXX_add_paymentgateway.py
    - Create model PaymentGateway
    - Add field payment_gateway to transaction

Operations to perform:
  Apply all migrations: transactions
Running migrations:
  Applying transactions.XXXX_add_paymentgateway... OK
```

✅ **If successful**, proceed to Step 2.

---

## Step 2: Install Stripe Package 📦

```bash
pip install stripe==7.0.0
```

**Verify Installation:**
```bash
python -c "import stripe; print('Stripe version:', stripe.__version__)"
```

✅ **Should output**: `Stripe version: 7.0.0`

---

## Step 3: Get Stripe Test Keys (FREE) 🔑

### Quick Steps:

1. **Visit**: https://stripe.com
2. **Sign Up** (free, no credit card needed)
3. **Login** to Dashboard
4. **Go to**: Developers → API keys (or visit https://dashboard.stripe.com/test/apikeys)
5. **Make sure**: Test mode is **ON** (orange toggle)
6. **Copy** your keys:
   - **Publishable key**: `pk_test_...` (visible)
   - **Secret key**: `sk_test_...` (click "Reveal" to see)

**Save these keys** - you'll need them in Step 4!

---

## Step 4: Configure in Django Admin 🎛️

### 4.1 Start Django Server

```bash
python manage.py runserver
```

### 4.2 Open Admin Panel

1. Open browser: **http://127.0.0.1:8000/admin/**
2. **Login** with admin credentials

### 4.3 Add Payment Gateway

1. **Navigate**: TRANSACTIONS → **Payment Gateways**
2. Click **"Add Payment Gateway"** button (top right)

3. **Fill in the form**:

   ```
   Basic Information:
   ┌─────────────────────────────────────────┐
   │ Name: Stripe Test                       │
   │ Gateway Type: [Stripe ▼]                │
   │ Description: (optional)                 │
   └─────────────────────────────────────────┘
   
   Status:
   ┌─────────────────────────────────────────┐
   │ ☑ Is Active                             │
   │ ☑ Is Test Mode                          │
   └─────────────────────────────────────────┘
   
   API Credentials:
   ┌─────────────────────────────────────────┐
   │ API Key Public: pk_test_51AbCd...       │
   │ API Key Secret: sk_test_51AbCd...       │
   │ Webhook Secret: (leave empty)           │
   └─────────────────────────────────────────┘
   
   Additional Configuration:
   ┌─────────────────────────────────────────┐
   │ Config: {}                              │
   └─────────────────────────────────────────┘
   ```

4. Click **"Save"**

### 4.4 Verify Configuration

After saving, you should see:

```
✅ Payment Gateway 'Stripe Test' was added successfully.
```

**In the list view, verify:**
- Status: ● **Active** (green)
- Mode: **TEST MODE** (orange)
- Configuration: ✓ **Configured** (green checkmark)

---

## Step 5: Test Configuration ✅

### Option A: Quick Test in Django Shell

```bash
python manage.py shell
```

Then run:

```python
from transactions.services import PaymentGatewayFactory

# Check active gateway
gateway = PaymentGatewayFactory.get_active_gateway()
print(f"Active Gateway: {gateway}")
print(f"Gateway Type: {gateway.gateway_type if gateway else 'None'}")
print(f"Test Mode: {gateway.is_test_mode if gateway else 'N/A'}")
print(f"Configured: {gateway.is_configured if gateway else 'N/A'}")

# Create payment service
try:
    service = PaymentGatewayFactory.create_service()
    print(f"✅ Payment service created: {service.__class__.__name__}")
except Exception as e:
    print(f"❌ Error: {e}")
```

**Expected Output:**
```
Active Gateway: Stripe - Active (Test)
Gateway Type: stripe
Test Mode: True
Configured: True
✅ Payment service created: StripePaymentService
```

### Option B: Check Admin Interface

1. Go to **Admin → Payment Gateways**
2. You should see your gateway with:
   - ✅ Green dot (Active)
   - ✅ Orange "TEST MODE"
   - ✅ Green checkmark (Configured)

---

## Troubleshooting 🔧

### Problem: "No changes detected" when creating migration

**Solution:**
1. Make sure you saved `transactions/models.py`
2. Check if PaymentGateway model exists in the file
3. Try:
   ```bash
   python manage.py makemigrations --name add_paymentgateway transactions
   ```

### Problem: Migration error about existing field

**Solution:**
- The payment_gateway field might already exist
- Check migration files in `transactions/migrations/`
- You may need to manually remove conflicting migration or use `--fake`

### Problem: Cannot find "Payment Gateways" in admin

**Solution:**
1. Make sure migration was applied:
   ```bash
   python manage.py migrate transactions
   ```
2. Restart Django server:
   ```bash
   # Stop server (Ctrl+C)
   python manage.py runserver
   ```
3. Refresh admin page (Ctrl+F5)

### Problem: Gateway shows "Not Configured"

**Solution:**
1. Make sure you entered the **Secret Key** (starts with `sk_test_...`)
2. Check for extra spaces when copying
3. Edit the gateway and re-enter the secret key

---

## Visual Guide: Admin Configuration

### Admin Form Fields Explained:

```
┌─────────────────────────────────────────────────────────┐
│              ADD PAYMENT GATEWAY                        │
├─────────────────────────────────────────────────────────┤
│                                                         │
│ Basic Information:                                      │
│   Name: [Stripe Test              ]                     │
│        ↑ Friendly name you'll recognize                │
│                                                         │
│   Gateway Type: [Stripe ▼]                             │
│                ↑ Select from dropdown                   │
│                                                         │
│   Description: [Optional description]                   │
│                                                         │
│ Status:                                                 │
│   ☑ Is Active                                          │
│     ↑ Check this to activate (only one can be active)  │
│                                                         │
│   ☑ Is Test Mode                                       │
│     ↑ Check for test/sandbox, uncheck for live         │
│                                                         │
│ API Credentials:                                        │
│   API Key Public: [pk_test_51AbCdEfGhIj...]            │
│                ↑ From Stripe dashboard                  │
│                                                         │
│   API Key Secret: [sk_test_51AbCdEfGhIj...]            │
│                ↑ From Stripe dashboard (Reveal button)  │
│                                                         │
│   Webhook Secret: [                    ]                │
│                ↑ Leave empty for now                    │
│                                                         │
│   [Save]  [Save and add another]  [Save and continue]  │
└─────────────────────────────────────────────────────────┘
```

---

## Checklist ✅

Before proceeding, make sure:

- [ ] Migration created: `python manage.py makemigrations transactions`
- [ ] Migration applied: `python manage.py migrate transactions`
- [ ] Stripe installed: `pip install stripe==7.0.0`
- [ ] Stripe account created (test mode)
- [ ] API keys copied from Stripe dashboard
- [ ] Payment Gateway added in Django admin
- [ ] Gateway shows as "Active" and "Configured"
- [ ] Test in Django shell passes

---

## What You Can Do Now 🎉

Once configured:

1. ✅ **Use Payment Service in Code**:
   ```python
   from transactions.services import PaymentGatewayFactory
   service = PaymentGatewayFactory.create_service()
   ```

2. ✅ **Switch Gateways**:
   - Add another gateway in admin
   - Activate it (old one auto-deactivates)

3. ✅ **Test Payments** (when you implement payment views):
   - Use Stripe test cards
   - Process test transactions
   - No real money involved

---

## Quick Commands Reference

```bash
# Create migration
python manage.py makemigrations transactions

# Apply migration
python manage.py migrate transactions

# Install Stripe
pip install stripe==7.0.0

# Run server
python manage.py runserver

# Django shell
python manage.py shell

# Check migrations
python manage.py showmigrations transactions
```

---

## Need Help?

- Check `PAYMENT_GATEWAY_SETUP_GUIDE.md` for detailed instructions
- Check `PAYMENT_SERVICE_IMPLEMENTATION.md` for code examples
- Common issues in Troubleshooting section above

---

**Ready to start?** Begin with Step 1! 🚀

