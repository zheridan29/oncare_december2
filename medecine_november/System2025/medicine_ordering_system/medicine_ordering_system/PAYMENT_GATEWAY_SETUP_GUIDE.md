# Payment Gateway Setup Guide - Step by Step

This guide will walk you through setting up and configuring payment gateways in your system.

---

## Step 1: Create Database Migration

### 1.1 Generate Migration File

Open your terminal/command prompt in the project directory and run:

```bash
python manage.py makemigrations transactions
```

**What this does:**
- Creates a migration file for the new `PaymentGateway` model
- Analyzes the model changes
- Generates SQL statements to create the table

**Expected Output:**
```
Migrations for 'transactions':
  transactions/migrations/XXXX_paymentgateway.py
    - Create model PaymentGateway
```

### 1.2 Apply Migration to Database

Run the migration to create the table in your database:

```bash
python manage.py migrate transactions
```

**What this does:**
- Executes the migration
- Creates the `transactions_paymentgateway` table in your database
- Creates the `payment_gateway` field in the `transactions_transaction` table

**Expected Output:**
```
Operations to perform:
  Apply all migrations: transactions
Running migrations:
  Applying transactions.XXXX_paymentgateway... OK
```

✅ **Step 1 Complete!** The PaymentGateway table is now in your database.

---

## Step 2: Install Stripe Package

### 2.1 Install Stripe

Run the following command to install Stripe:

```bash
pip install stripe==7.0.0
```

**Or if you want to install all requirements:**

```bash
pip install -r requirements.txt
```

**Expected Output:**
```
Successfully installed stripe-7.0.0
```

✅ **Step 2 Complete!** Stripe package is now installed.

---

## Step 3: Get Stripe Test API Keys (FREE)

### 3.1 Create Stripe Account

1. **Go to Stripe Website**: https://stripe.com
2. **Click "Sign Up"** (top right corner)
3. **Fill in your details**:
   - Email address
   - Password
   - Basic information
4. **Verify your email** (check your inbox)

**Note**: Stripe test accounts are 100% FREE - no credit card required!

### 3.2 Access Stripe Dashboard

1. **Log in** to your Stripe account
2. **Toggle to Test Mode** (top right, toggle switch should say "Test mode")
   - Should show: **"Test mode"** in orange
   - This is important - you want TEST keys, not LIVE keys

### 3.3 Get Your Test API Keys

1. **Click "Developers"** in the left sidebar
2. **Click "API keys"** under Developers
3. **You'll see two keys**:

   **Publishable key** (starts with `pk_test_`):
   ```
   pk_test_51AbCdEfGhIjKlMnOpQrStUvWxYz1234567890...
   ```

   **Secret key** (starts with `sk_test_`):
   ```
   sk_test_51AbCdEfGhIjKlMnOpQrStUvWxYz1234567890...
   ```

4. **Copy both keys** - you'll need them in the next step

**Important**: 
- ✅ **Test keys** start with `pk_test_` and `sk_test_`
- ❌ **Live keys** start with `pk_live_` and `sk_live_`
- Make sure you're in **Test Mode** when copying keys!

✅ **Step 3 Complete!** You now have Stripe test API keys.

---

## Step 4: Configure Payment Gateway in Admin

### 4.1 Access Django Admin

1. **Start your Django server** (if not already running):
   ```bash
   python manage.py runserver
   ```

2. **Open your browser** and go to:
   ```
   http://127.0.0.1:8000/admin/
   ```

3. **Log in** with your admin credentials

### 4.2 Navigate to Payment Gateways

1. **Find "Transactions"** section in the admin sidebar
2. **Click "Payment Gateways"** under Transactions
3. **Click "Add Payment Gateway"** button (top right)

### 4.3 Fill in Payment Gateway Form

Fill in the form with the following information:

#### Basic Information:
- **Name**: `Stripe Test` (or any name you prefer)
- **Gateway Type**: Select **"Stripe"** from dropdown
- **Description**: `Stripe payment gateway for testing` (optional)

#### Status:
- **Is Active**: ✅ **Check this box** (to activate the gateway)
- **Is Test Mode**: ✅ **Check this box** (we're using test keys)

#### API Credentials:
- **API Key Public**: Paste your **Publishable key** (pk_test_...)
  ```
  pk_test_51AbCdEfGhIjKlMnOpQrStUvWxYz...
  ```

- **API Key Secret**: Paste your **Secret key** (sk_test_...)
  ```
  sk_test_51AbCdEfGhIjKlMnOpQrStUvWxYz...
  ```

- **Webhook Secret**: Leave **blank for now** (we'll set this up later)

#### Additional Configuration:
- **Config**: Leave as `{}` (empty JSON object)

#### Metadata:
- Fields are auto-filled, no need to change

### 4.4 Save the Payment Gateway

1. **Click "Save"** button at the bottom
2. **You should see**:
   - ✅ Success message
   - ⚠️ Warning if gateway is not configured (ignore for now if keys are correct)

✅ **Step 4 Complete!** Payment gateway is now configured.

---

## Step 5: Verify Configuration

### 5.1 Check Payment Gateway Status

1. **Go back to Payment Gateways list** (click "Payment Gateways" in breadcrumb)
2. **You should see your gateway** with:
   - **Status**: ● Active (green dot)
   - **Mode**: TEST MODE (orange)
   - **Configuration**: ✓ Configured (green checkmark)

### 5.2 Test Gateway Configuration

Let's verify the gateway is working by testing it in Python shell:

```bash
python manage.py shell
```

Then run:

```python
from transactions.services import PaymentGatewayFactory
from transactions.models import PaymentGateway

# Check active gateway
gateway = PaymentGatewayFactory.get_active_gateway()
print(f"Active Gateway: {gateway}")

# Try to create service
try:
    service = PaymentGatewayFactory.create_service()
    print(f"✅ Payment service created successfully!")
    print(f"Service type: {type(service).__name__}")
    print(f"Test mode: {service.is_test_mode}")
except Exception as e:
    print(f"❌ Error: {e}")
```

**Expected Output:**
```
Active Gateway: Stripe - Active (Test)
✅ Payment service created successfully!
Service type: StripePaymentService
Test mode: True
```

✅ **Step 5 Complete!** Gateway is properly configured.

---

## Step 6: Test Payment Processing (Optional)

### 6.1 Create a Test Payment Intent

**Important Note:** Stripe doesn't natively support PHP (Philippine Peso). For testing, we'll use USD. In production, you can implement currency conversion or use PayMongo which supports PHP.

#### Option 1: Run the Test Script (Recommended)

**Easiest method** - just run the batch file:

```bash
run_step6_test.bat
```

Or manually:

```bash
# Activate virtual environment first
venv\Scripts\activate

# Run the test script
python test_payment_intent_step6.py
```

#### Option 2: Run in Python Shell (Interactive)

Open a **new terminal** (not Python shell), activate venv, then:

```bash
python manage.py shell
```

Then run:

```python
from transactions.services import PaymentGatewayFactory
from orders.models import Order
from decimal import Decimal

# Get payment service
service = PaymentGatewayFactory.create_service()
print(f"✅ Payment service created: {type(service).__name__}")

# Get a test order (or create one)
order = Order.objects.first()  # Use any existing order
if not order:
    print("No orders found. Creating a test order...")
    from accounts.models import User
    user = User.objects.filter(is_sales_rep=True).first()
    if not user:
        user = User.objects.first()
    
    if user:
        order = Order.objects.create(
            sales_rep=user,
            customer_name="Test Customer",
            customer_phone="1234567890",
            customer_address="Test Address",
            status='pending',
            payment_status='pending',
            subtotal=Decimal('100.00'),
            total_amount=Decimal('100.00'),
            delivery_method='pickup'
        )
        print(f"✅ Created test order: {order.order_number}")
    else:
        print("No users found. Cannot create test order.")
else:
    print(f"✅ Using existing order: {order.order_number}")

# Create payment intent
print("\n⚠️  Note: Stripe doesn't support PHP directly.")
print("Using USD for testing...")

try:
    result = service.create_payment_intent(
        order=order,
        amount=Decimal('10.00'),  # $10.00 USD for testing
        currency='USD',  # Use USD since Stripe doesn't support PHP
        metadata={
            'test': 'true',
            'original_currency': 'PHP',
            'original_amount': str(order.total_amount)
        }
    )
    print("\n✅ Payment Intent Created!")
    print(f"Payment Intent ID: {result['payment_intent_id']}")
    print(f"Client Secret: {result['client_secret'][:30]}...")
    print(f"Status: {result['status']}")
    print(f"\nFull Client Secret: {result['client_secret']}")
except Exception as e:
    print(f"❌ Error: {e}")
    import traceback
    traceback.print_exc()
```

**Expected Output:**
```
✅ Payment service created: StripePaymentService
✅ Using existing order: ORD-ABC12345

⚠️  Note: Stripe doesn't support PHP directly.
Using USD for testing...

✅ Payment Intent Created!
Payment Intent ID: pi_3Sae0YFPDvOzEmUZ08j9l4e3
Client Secret: pi_3Sae0YFPDvOzEmUZ08j9l4e3_se...
Status: requires_payment_method

Full Client Secret: pi_3Sae0YFPDvOzEmUZ08j9l4e3_secret_...
```

### 6.2 Test Payment Status Check

```python
# Check payment status
status = service.get_payment_status(result['payment_intent_id'])
print(f"Payment Status: {status['status']}")
```

✅ **Step 6 Complete!** Payment service is working!

---

## Troubleshooting

### Issue: "No active payment gateway found"

**Solution:**
- Go to Admin → Payment Gateways
- Make sure one gateway has "Is Active" checked
- Only one gateway can be active at a time

### Issue: "Payment gateway is not properly configured"

**Solution:**
- Check that API Key Secret is filled in
- Verify keys start with `sk_test_` (test mode) or `sk_live_` (live mode)
- Make sure you copied the full key (they're long!)

### Issue: "Stripe error: Invalid API Key"

**Solution:**
- Double-check you copied the correct key
- Make sure you're using TEST keys in TEST mode
- Regenerate keys in Stripe dashboard if needed

### Issue: Migration error

**Solution:**
```bash
# Check for migration conflicts
python manage.py showmigrations transactions

# If needed, create migration again
python manage.py makemigrations transactions --name add_payment_gateway
python manage.py migrate
```

---

## Quick Reference

### Admin URL:
```
http://127.0.0.1:8000/admin/transactions/paymentgateway/
```

### Useful Commands:
```bash
# Create migration
python manage.py makemigrations transactions

# Apply migration
python manage.py migrate transactions

# Install Stripe
pip install stripe==7.0.0

# Test in Python shell
python manage.py shell
```

### Stripe Dashboard:
```
https://dashboard.stripe.com/test/apikeys
```

---

## Next Steps

Once your gateway is configured:

1. ✅ **Gateway is active and working**
2. 🚀 **Ready to integrate payment processing** in your views
3. 🧪 **Can test payments** using Stripe test cards
4. 📝 **Can add more gateways** (PayMongo, PayPal, etc.) later

---

## Summary Checklist

- [ ] Migration created and applied
- [ ] Stripe package installed
- [ ] Stripe account created
- [ ] Test API keys obtained
- [ ] Payment gateway configured in admin
- [ ] Gateway status shows "Active" and "Configured"
- [ ] Payment service tested successfully

---

**Setup Complete!** 🎉

Your payment gateway is now configured and ready to use. You can now:
- Process payments through Stripe
- Switch between gateways in admin
- Test payment flows
- Add more payment gateways later

---

**Need Help?** Refer to:
- `PAYMENT_SERVICE_IMPLEMENTATION.md` - Technical details
- `PAYMENT_GATEWAYS_FREE_TESTING.md` - Testing information
- Stripe Documentation: https://stripe.com/docs
