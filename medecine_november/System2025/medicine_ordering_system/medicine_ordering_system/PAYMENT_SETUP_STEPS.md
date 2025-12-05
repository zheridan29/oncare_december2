# Payment Gateway Setup - Step-by-Step Instructions

Follow these steps exactly to set up your payment gateway.

---

## Step 1: Apply Database Migration

The migration file already exists. You just need to apply it to your database.

### Run this command:

```bash
python manage.py migrate transactions
```

**What this does:**
- Creates the `PaymentGateway` table in your database
- Adds the `payment_gateway` field to the `Transaction` table

**Expected Output:**
```
Operations to perform:
  Apply all migrations: transactions
Running migrations:
  Applying transactions.0002_paymentgateway_transaction_payment_gateway... OK
```

✅ **If you see "OK"**, the migration was successful!

---

## Step 2: Install Stripe Package

### Run this command:

```bash
pip install stripe==7.0.0
```

**Expected Output:**
```
Successfully installed stripe-7.0.0
```

✅ **Stripe package is now installed!**

---

## Step 3: Get Stripe Test API Keys (FREE - Takes 5 minutes)

### 3.1 Create Stripe Account

1. **Open your web browser**
2. **Go to**: https://stripe.com
3. **Click "Sign up"** (top right)
4. **Fill in**:
   - Email address
   - Password
   - Company name (optional)
5. **Verify your email** (check your inbox and click verification link)

**Note**: This is completely FREE - no credit card required for test mode!

### 3.2 Get Test API Keys

1. **Log in** to Stripe Dashboard: https://dashboard.stripe.com/login

2. **Check Test Mode**:
   - Look at the top right corner
   - Should see **"Test mode"** in orange
   - If you see "Live mode", click the toggle to switch to "Test mode"

3. **Go to API Keys**:
   - Click **"Developers"** in the left sidebar
   - Click **"API keys"**
   - Or go directly to: https://dashboard.stripe.com/test/apikeys

4. **Copy Your Keys**:

   **Publishable key** (starts with `pk_test_`):
   ```
   Example: pk_test_51AbCdEfGhIjKlMnOpQrStUvWxYz1234567890...
   ```
   - Click the "Reveal" button or copy icon
   - Copy the entire key

   **Secret key** (starts with `sk_test_`):
   ```
   Example: sk_test_51AbCdEfGhIjKlMnOpQrStUvWxYz1234567890...
   ```
   - Click the "Reveal" button or copy icon
   - Copy the entire key

5. **Save these keys** - you'll paste them in the admin form next!

✅ **You now have your Stripe test API keys!**

---

## Step 4: Configure Payment Gateway in Django Admin

### 4.1 Start Django Server

Open a new terminal/command prompt and run:

```bash
python manage.py runserver
```

**Expected Output:**
```
Starting development server at http://127.0.0.1:8000/
```

✅ **Server is running!**

### 4.2 Access Admin Panel

1. **Open your web browser**
2. **Go to**: http://127.0.0.1:8000/admin/
3. **Log in** with your admin username and password

### 4.3 Navigate to Payment Gateways

1. **Look for "TRANSACTIONS"** section in the left sidebar
2. **Click "Payment Gateways"** (under Transactions)
3. **You should see**: "0 Payment Gateways" (if none exist yet)
4. **Click "Add Payment Gateway"** button (top right, green button)

### 4.4 Fill in the Form

**Section: Basic Information**
- **Name**: Type `Stripe Test`
- **Gateway Type**: Select **"Stripe"** from the dropdown
- **Description**: Type `Stripe payment gateway for testing` (optional)

**Section: Status**
- **Is Active**: ✅ **Check this box** (important!)
- **Is Test Mode**: ✅ **Check this box** (important!)

**Section: API Credentials**
- **API Key Public**: Paste your **Publishable key** (pk_test_...)
  - Should look like: `pk_test_51AbCdEfGhIjKlMnOpQrStUvWxYz...`
  
- **API Key Secret**: Paste your **Secret key** (sk_test_...)
  - Should look like: `sk_test_51AbCdEfGhIjKlMnOpQrStUvWxYz...`
  
- **Webhook Secret**: Leave this **blank** for now

**Section: Additional Configuration**
- Leave as `{}` (default)

### 4.5 Save the Payment Gateway

1. **Scroll down** to the bottom
2. **Click "Save"** button
3. **You should see**:
   - A green success message at the top
   - Your gateway listed in the Payment Gateways page

### 4.6 Verify Configuration

On the Payment Gateways list page, you should see:

| Name | Gateway Type | Status | Mode | Configuration |
|------|--------------|--------|------|---------------|
| Stripe Test | Stripe | ● Active | TEST MODE | ✓ Configured |

✅ **Gateway is configured and active!**

---

## Step 5: Test the Configuration

### 5.1 Test in Python Shell

Open a new terminal/command prompt (keep the server running) and run:

```bash
python manage.py shell
```

### 5.2 Run Test Commands

Copy and paste these commands one by one:

```python
# Import required modules
from transactions.services import PaymentGatewayFactory
from transactions.models import PaymentGateway

# Check if active gateway exists
gateway = PaymentGatewayFactory.get_active_gateway()
print(f"Active Gateway: {gateway}")
print(f"Gateway Type: {gateway.gateway_type}")
print(f"Is Test Mode: {gateway.is_test_mode}")
print(f"Is Configured: {gateway.is_configured}")
```

**Expected Output:**
```
Active Gateway: Stripe - Active (Test)
Gateway Type: stripe
Is Test Mode: True
Is Configured: True
```

### 5.3 Test Payment Service Creation

```python
# Create payment service
service = PaymentGatewayFactory.create_service()
print(f"✅ Payment service created: {type(service).__name__}")
print(f"Service test mode: {service.is_test_mode}")
```

**Expected Output:**
```
✅ Payment service created: StripePaymentService
Service test mode: True
```

### 5.4 Test Payment Intent Creation (Optional)

```python
# Get a test order
from orders.models import Order
from decimal import Decimal

order = Order.objects.first()  # Get any order

if order:
    # Create payment intent
    result = service.create_payment_intent(
        order=order,
        amount=Decimal('100.00'),
        currency='PHP'
    )
    print(f"✅ Payment Intent Created!")
    print(f"Payment Intent ID: {result['payment_intent_id']}")
    print(f"Status: {result['status']}")
else:
    print("No orders found. Create an order first to test payment intent.")
```

**Expected Output:**
```
✅ Payment Intent Created!
Payment Intent ID: pi_3AbCdEfGhIjKlMnOpQrStUv
Status: requires_payment_method
```

### 5.5 Exit Shell

```python
exit()
```

✅ **Everything is working correctly!**

---

## Troubleshooting

### Problem: "No changes detected" when running makemigrations

**Solution**: The migration already exists. Just run:
```bash
python manage.py migrate transactions
```

### Problem: "No active payment gateway found"

**Solution**: 
- Go to Admin → Payment Gateways
- Make sure "Is Active" is checked ✅
- Save the gateway again

### Problem: "Payment gateway is not properly configured"

**Solution**:
- Check that you pasted the **Secret key** (sk_test_...)
- Make sure you copied the **entire key** (they're very long!)
- Verify keys start with `pk_test_` and `sk_test_` (not `pk_live_` or `sk_live_`)

### Problem: "Invalid API Key" error

**Solution**:
- Double-check you copied the keys correctly
- Make sure you're using **test keys** (start with `pk_test_` and `sk_test_`)
- Try regenerating keys in Stripe dashboard

### Problem: Migration error

**Solution**:
```bash
# Check migration status
python manage.py showmigrations transactions

# If migration shows [X], it's already applied
# If migration shows [ ], apply it:
python manage.py migrate transactions
```

---

## Success Indicators

You'll know everything is set up correctly when:

✅ **Migration applied** - No errors when running `migrate`  
✅ **Stripe installed** - `pip list | grep stripe` shows stripe package  
✅ **Gateway in admin** - Payment Gateway appears in admin list  
✅ **Gateway is Active** - Shows green dot (●) in admin  
✅ **Gateway is Configured** - Shows green checkmark (✓) in admin  
✅ **Service creates successfully** - No errors in Python shell test  

---

## Quick Command Reference

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

## Next Steps After Setup

Once your gateway is configured:

1. ✅ **Gateway is ready** - You can now process payments
2. 🚀 **Create payment views** - Build checkout pages
3. 🧪 **Test payments** - Use Stripe test cards
4. 📱 **Add webhooks** - For automatic payment confirmations
5. 🔄 **Add more gateways** - PayMongo, PayPal, etc.

---

## Summary

**Three Simple Steps:**

1. **Apply migration**: `python manage.py migrate transactions`
2. **Install Stripe**: `pip install stripe==7.0.0`
3. **Configure in admin**: Add payment gateway with your Stripe test keys

**That's it!** Your payment gateway is now ready to use. 🎉

---

**Questions?** Check the detailed guide: `PAYMENT_GATEWAY_SETUP_GUIDE.md`


