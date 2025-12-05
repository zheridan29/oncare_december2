# Quick Payment Gateway Setup Guide

Follow these steps to set up and configure your payment gateway.

---

## ✅ Step 1: Check Migration Status

Check if the migration has been applied:

```bash
python manage.py showmigrations transactions
```

**If you see `[ ]` (empty checkbox)**, the migration hasn't been applied yet.  
**If you see `[X]` (checked)**, the migration is already applied.

---

## 📦 Step 2: Apply Migration (If Needed)

If the migration shows `[ ]`, apply it:

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

✅ **Migration applied!**

---

## 🔧 Step 3: Install Stripe Package

```bash
pip install stripe==7.0.0
```

Or install all requirements:

```bash
pip install -r requirements.txt
```

✅ **Stripe installed!**

---

## 🔑 Step 4: Get Stripe Test API Keys (FREE)

### Quick Steps:

1. **Visit**: https://stripe.com
2. **Sign up** for free account (no credit card needed)
3. **Log in** and go to: https://dashboard.stripe.com/test/apikeys
4. **Make sure you're in Test Mode** (orange "Test mode" toggle at top right)
5. **Copy these keys**:
   - **Publishable key** (`pk_test_...`)
   - **Secret key** (`sk_test_...`)

**Keep these keys handy** - you'll need them in the next step!

---

## ⚙️ Step 5: Configure in Admin

### 5.1 Access Admin Panel

1. **Start server** (if not running):
   ```bash
   python manage.py runserver
   ```

2. **Open browser**: http://127.0.0.1:8000/admin/

3. **Log in** with your admin credentials

### 5.2 Add Payment Gateway

1. **Navigate**: Transactions → Payment Gateways
2. **Click**: "Add Payment Gateway" button (top right)

### 5.3 Fill in the Form

**Basic Information:**
- **Name**: `Stripe Test`
- **Gateway Type**: `Stripe`
- **Description**: `Stripe test gateway` (optional)

**Status:**
- ✅ **Is Active**: Check this box
- ✅ **Is Test Mode**: Check this box

**API Credentials:**
- **API Key Public**: Paste your `pk_test_...` key
- **API Key Secret**: Paste your `sk_test_...` key
- **Webhook Secret**: Leave blank for now

**Additional Configuration:**
- Leave as `{}`

### 5.4 Save

Click **"Save"** button.

You should see:
- ✅ Success message
- Your gateway listed with:
  - ● Active (green dot)
  - TEST MODE (orange)
  - ✓ Configured (green checkmark)

✅ **Gateway configured!**

---

## 🧪 Step 6: Test the Configuration

Test in Python shell:

```bash
python manage.py shell
```

Then run:

```python
from transactions.services import PaymentGatewayFactory

# Get active gateway
gateway = PaymentGatewayFactory.get_active_gateway()
print(f"Active Gateway: {gateway}")

# Create service
service = PaymentGatewayFactory.create_service()
print(f"✅ Service created: {type(service).__name__}")
print(f"Test Mode: {service.is_test_mode}")
```

**Expected Output:**
```
Active Gateway: Stripe - Active (Test)
✅ Service created: StripePaymentService
Test Mode: True
```

✅ **Everything is working!**

---

## 📋 Quick Checklist

- [ ] Migration applied (`python manage.py migrate transactions`)
- [ ] Stripe installed (`pip install stripe==7.0.0`)
- [ ] Stripe account created (https://stripe.com)
- [ ] Test API keys obtained (pk_test_ and sk_test_)
- [ ] Payment gateway added in admin
- [ ] Gateway is Active and Configured
- [ ] Test passed in Python shell

---

## 🎯 You're Done!

Your payment gateway is now configured and ready to use!

**What you can do now:**
- ✅ Switch between payment gateways in admin
- ✅ Process payments through Stripe
- ✅ Test with Stripe test cards
- ✅ Add more gateways later

---

## 🔗 Useful Links

- **Stripe Dashboard**: https://dashboard.stripe.com/test/apikeys
- **Admin Panel**: http://127.0.0.1:8000/admin/transactions/paymentgateway/
- **Test Cards**: 
  - Success: `4242 4242 4242 4242`
  - Decline: `4000 0000 0000 0002`

---

**Need detailed instructions?** See `PAYMENT_GATEWAY_SETUP_GUIDE.md`


