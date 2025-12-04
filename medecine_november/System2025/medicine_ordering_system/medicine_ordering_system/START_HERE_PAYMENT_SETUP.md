# 🚀 Payment Gateway Setup - Start Here!

Complete step-by-step guide to set up your payment gateway.

---

## 📋 Overview

You need to do **3 main things**:
1. ✅ Apply database migration
2. ✅ Install Stripe package  
3. ✅ Configure gateway in admin

**Total time: ~10-15 minutes**

---

## Step 1: Apply Database Migration ⚙️

### Open Terminal/Command Prompt

Navigate to your project directory:
```bash
cd "C:\Users\Ace Z Gutierrez\Videos\Masteral November\medecine_november\System2025\medicine_ordering_system\medicine_ordering_system"
```

### Run Migration Command

```bash
python manage.py migrate transactions
```

**What you should see:**
```
Operations to perform:
  Apply all migrations: transactions
Running migrations:
  Applying transactions.0002_paymentgateway_transaction_payment_gateway... OK
```

✅ **If you see "OK"**, you're done with this step!

**If you see "No migrations to apply"**, that's fine too - it means it's already applied!

---

## Step 2: Install Stripe Package 📦

### Run Installation Command

```bash
pip install stripe==7.0.0
```

**What you should see:**
```
Successfully installed stripe-7.0.0
```

✅ **Stripe is now installed!**

---

## Step 3: Get Stripe Test API Keys (FREE) 🔑

### 3.1 Sign Up for Stripe (FREE)

1. **Go to**: https://stripe.com
2. **Click "Sign up"** (top right)
3. **Enter**:
   - Email address
   - Password
   - Company name (optional)
4. **Verify email** (check your inbox)

**No credit card needed!** Test accounts are completely free.

### 3.2 Get Your Test Keys

1. **Log in**: https://dashboard.stripe.com/login

2. **Verify Test Mode**:
   - Top right should show **"Test mode"** in orange
   - If you see "Live mode", click the toggle to switch

3. **Get API Keys**:
   - Click **"Developers"** → **"API keys"**
   - Or go directly: https://dashboard.stripe.com/test/apikeys

4. **Copy These Two Keys**:

   **🔑 Publishable key** (pk_test_...):
   - Click "Reveal" or copy icon
   - Copy the entire key
   - Example: `pk_test_51AbCdEfGhIjKlMnOpQrStUvWxYz1234567890...`

   **🔐 Secret key** (sk_test_...):
   - Click "Reveal" or copy icon  
   - Copy the entire key
   - Example: `sk_test_51AbCdEfGhIjKlMnOpQrStUvWxYz1234567890...`

**Save both keys** - you'll paste them in admin next!

---

## Step 4: Configure in Django Admin 🎛️

### 4.1 Start Django Server

In your terminal, run:

```bash
python manage.py runserver
```

**You should see:**
```
Starting development server at http://127.0.0.1:8000/
Quit the server with CTRL-BREAK.
```

**Keep this terminal open!** The server must be running.

### 4.2 Open Admin Panel

1. **Open your web browser**
2. **Go to**: http://127.0.0.1:8000/admin/
3. **Log in** with your admin username and password

### 4.3 Add Payment Gateway

1. **In the left sidebar**, find **"TRANSACTIONS"** section
2. **Click "Payment Gateways"** (under Transactions)
3. **Click "Add Payment Gateway"** button (green button, top right)

### 4.4 Fill in the Form

#### Basic Information:
- **Name**: `Stripe Test`
- **Gateway Type**: Select **"Stripe"** from dropdown
- **Description**: `Stripe payment gateway for testing` (optional)

#### Status:
- ✅ **Is Active**: Check this box
- ✅ **Is Test Mode**: Check this box

#### API Credentials:
- **API Key Public**: 
  - Paste your **Publishable key** here
  - Should start with `pk_test_`
  
- **API Key Secret**: 
  - Paste your **Secret key** here
  - Should start with `sk_test_`
  
- **Webhook Secret**: 
  - Leave **blank** (we'll set this up later)

#### Additional Configuration:
- Leave as `{}` (default)

### 4.5 Save

1. **Scroll to bottom**
2. **Click "Save"** button

**You should see:**
- Green success message: "Payment Gateway was added successfully"
- Your gateway in the list with:
  - ● Active (green dot)
  - TEST MODE (orange)
  - ✓ Configured (green checkmark)

✅ **Gateway is configured!**

---

## Step 5: Test It Works ✅

### 5.1 Open Python Shell

Open a **new terminal** (keep server running) and run:

```bash
python manage.py shell
```

### 5.2 Test Commands

Copy and paste these commands:

```python
from transactions.services import PaymentGatewayFactory

# Get active gateway
gateway = PaymentGatewayFactory.get_active_gateway()
print(f"✅ Active Gateway: {gateway}")

# Create payment service
service = PaymentGatewayFactory.create_service()
print(f"✅ Service Created: {type(service).__name__}")
print(f"✅ Test Mode: {service.is_test_mode}")
```

**Expected Output:**
```
✅ Active Gateway: Stripe - Active (Test)
✅ Service Created: StripePaymentService
✅ Test Mode: True
```

### 5.3 Exit Shell

```python
exit()
```

✅ **Everything is working!**

---

## ✅ Checklist

Before moving on, verify:

- [ ] Migration applied (`python manage.py migrate transactions`)
- [ ] Stripe installed (`pip install stripe==7.0.0`)
- [ ] Stripe account created
- [ ] Test API keys obtained (pk_test_ and sk_test_)
- [ ] Payment gateway added in admin
- [ ] Gateway shows "Active" and "Configured" in admin
- [ ] Test passed in Python shell

---

## 🎉 You're Done!

Your payment gateway is now configured and ready!

**What you can do:**
- ✅ Switch between gateways in admin
- ✅ Process payments through Stripe
- ✅ Test with Stripe test cards
- ✅ Add more gateways later

---

## 📚 Next Steps

1. **Create payment views** - Build checkout pages
2. **Integrate payment processing** - Add to order flow
3. **Test payments** - Use Stripe test cards
4. **Add webhooks** - Automatic payment confirmations

---

## 🆘 Need Help?

**Common Issues:**

❌ **"No active gateway found"**
- Solution: Check "Is Active" box in admin

❌ **"Not configured"**  
- Solution: Make sure you pasted the Secret key (sk_test_...)

❌ **"Invalid API key"**
- Solution: Double-check keys, make sure they're test keys (start with pk_test_/sk_test_)

---

## 📝 Quick Commands Reference

```bash
# Apply migration
python manage.py migrate transactions

# Install Stripe
pip install stripe==7.0.0

# Start server
python manage.py runserver

# Test in shell
python manage.py shell
```

---

**Setup Complete!** 🎊

Follow the steps above and you'll have your payment gateway configured in no time!
