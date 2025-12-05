# How to Test Your Payment Gateway

This guide will help you test your payment gateway configuration.

---

## Quick Test (5 minutes)

### Step 1: Run the Test Script

Open your terminal in the project directory and run:

```bash
python test_payment_gateway.py
```

This will run a comprehensive test suite that checks:
- ✅ Gateway configuration
- ✅ Service creation
- ✅ Payment intent creation
- ✅ Payment status retrieval
- ✅ API connection

**Expected Output:**
```
============================================================
  PAYMENT GATEWAY TEST SUITE
============================================================

Running tests to verify payment gateway configuration...

============================================================
  TEST 1: Gateway Configuration
============================================================
✅ Active Gateway Found: Stripe Test
   Gateway Type: stripe
   Status: Active
   Mode: TEST MODE
   Configured: Yes

============================================================
  TEST 2: Payment Service Creation
============================================================
✅ Payment Service Created Successfully!
   Service Type: StripePaymentService
   Test Mode: True
   Configured: True
   Gateway: Stripe Test

============================================================
  TEST 3: Payment Intent Creation
============================================================
Using order: ORD-ABC12345
Order amount: ₱100.00
✅ Payment Intent Created Successfully!
   Payment Intent ID: pi_3AbCdEfGhIjKlMnOpQrStUv
   Status: requires_payment_method
   Client Secret: pi_3AbCdEfGhIjKlMnOpQrStUv...

============================================================
  TEST 4: Payment Status Check
============================================================
✅ Payment Status Retrieved!
   Status: requires_payment_method
   Amount: ₱100.00
   Currency: PHP

============================================================
  TEST 5: Gateway API Connection
============================================================
✅ API Connection Successful!
   Can communicate with Stripe API
   Payment Intent ID: pi_3XyZ...

============================================================
  TEST SUMMARY
============================================================
Tests Passed: 5/5

  ✅ PASS - Config
  ✅ PASS - Service
  ✅ PASS - Intent
  ✅ PASS - Status
  ✅ PASS - Api

🎉 ALL TESTS PASSED! Your payment gateway is working correctly!
```

---

## Manual Testing in Python Shell

If you prefer to test manually:

### 1. Open Python Shell

```bash
python manage.py shell
```

### 2. Import Required Modules

```python
from transactions.services import PaymentGatewayFactory
from transactions.models import PaymentGateway
from orders.models import Order
from decimal import Decimal
```

### 3. Check Active Gateway

```python
# Get active gateway
gateway = PaymentGatewayFactory.get_active_gateway()
print(f"Active Gateway: {gateway}")
print(f"Type: {gateway.gateway_type}")
print(f"Test Mode: {gateway.is_test_mode}")
print(f"Configured: {gateway.is_configured}")
```

**Expected Output:**
```
Active Gateway: Stripe - Active (Test)
Type: stripe
Test Mode: True
Configured: True
```

### 4. Create Payment Service

```python
# Create payment service
service = PaymentGatewayFactory.create_service()
print(f"Service Type: {type(service).__name__}")
print(f"Configured: {service.is_configured()}")
```

**Expected Output:**
```
Service Type: StripePaymentService
Configured: True
```

### 5. Create a Payment Intent

```python
# Get an existing order (or create one)
order = Order.objects.first()
if order:
    print(f"Using order: {order.order_number}")
    print(f"Amount: ₱{order.total_amount}")
    
    # Create payment intent
    result = service.create_payment_intent(
        order=order,
        amount=order.total_amount,
        currency='PHP',
        metadata={'test': 'true'}
    )
    
    print(f"✅ Payment Intent Created!")
    print(f"ID: {result['payment_intent_id']}")
    print(f"Status: {result['status']}")
    print(f"Client Secret: {result['client_secret'][:30]}...")
else:
    print("No orders found. Create an order first.")
```

**Expected Output:**
```
Using order: ORD-ABC12345
Amount: ₱100.00
✅ Payment Intent Created!
ID: pi_3AbCdEfGhIjKlMnOpQrStUv
Status: requires_payment_method
Client Secret: pi_3AbCdEfGhIjKlMnOpQrStUv...
```

### 6. Check Payment Status

```python
# Check status using payment intent ID from above
payment_intent_id = result['payment_intent_id']
status = service.get_payment_status(payment_intent_id)

print(f"Payment Status: {status['status']}")
print(f"Amount: ₱{status['amount']}")
print(f"Currency: {status['currency']}")
```

**Expected Output:**
```
Payment Status: requires_payment_method
Amount: ₱100.00
Currency: PHP
```

---

## Test with Stripe Test Cards

Once your payment gateway is working, you can test with Stripe test cards:

### Test Cards

| Card Number | Result |
|------------|--------|
| `4242 4242 4242 4242` | Success |
| `4000 0000 0000 0002` | Card Declined |
| `4000 0025 0000 3155` | Requires Authentication |

**Test Card Details:**
- **Expiry**: Any future date (e.g., 12/25)
- **CVC**: Any 3 digits (e.g., 123)
- **ZIP**: Any 5 digits (e.g., 12345)

### How to Test Payment Flow

1. Create a payment intent (as shown above)
2. Use the `client_secret` from the result
3. Integrate Stripe.js on your frontend
4. Use test card `4242 4242 4242 4242` to test successful payment
5. Check payment status using `get_payment_status()`

---

## Troubleshooting

### ❌ Error: "No active payment gateway found"

**Solution:**
```python
# Check if any gateways exist
from transactions.models import PaymentGateway
gateways = PaymentGateway.objects.all()
print(f"Gateways found: {gateways.count()}")
for gw in gateways:
    print(f"  - {gw.name}: Active={gw.is_active}, Configured={gw.is_configured}")

# Activate a gateway
if gateways.exists():
    gateway = gateways.first()
    gateway.is_active = True
    gateway.save()
    print(f"✅ Activated: {gateway.name}")
```

### ❌ Error: "Payment gateway is not properly configured"

**Solution:**
1. Go to Django Admin → Payment Gateways
2. Check that "API Key Secret" is filled in
3. Make sure you're using TEST keys (sk_test_...) in TEST mode
4. Verify keys are copied correctly (they're very long!)

### ❌ Error: "Invalid API Key"

**Solution:**
1. Check your Stripe dashboard: https://dashboard.stripe.com/test/apikeys
2. Make sure you're in **Test Mode** (orange toggle)
3. Copy the keys again
4. Make sure keys start with:
   - `pk_test_` for Publishable key
   - `sk_test_` for Secret key
5. Update in Admin → Payment Gateways

### ❌ Error: "No orders found"

**Solution:**
```python
# Create a test order
from orders.models import Order
from accounts.models import User
from decimal import Decimal

# Get a sales rep user
user = User.objects.filter(is_sales_rep=True).first()
if not user:
    print("No sales rep found. Create a user with role 'sales_rep' first.")
else:
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
```

---

## What Each Test Checks

### Test 1: Gateway Configuration
- ✅ Active gateway exists
- ✅ Gateway is properly configured
- ✅ Test/Live mode is set correctly

### Test 2: Service Creation
- ✅ Payment service can be created
- ✅ Service is properly configured
- ✅ Service has correct type

### Test 3: Payment Intent Creation
- ✅ Can create payment intents
- ✅ API communication works
- ✅ Returns valid payment intent ID

### Test 4: Payment Status Check
- ✅ Can retrieve payment status
- ✅ Status information is correct
- ✅ Amount and currency are accurate

### Test 5: API Connection
- ✅ Can connect to Stripe API
- ✅ Authentication works
- ✅ API keys are valid

---

## Success Indicators

You'll know everything is working when:

✅ **All 5 tests pass**  
✅ **Payment intents can be created**  
✅ **Payment status can be retrieved**  
✅ **No error messages appear**  
✅ **Stripe dashboard shows test payment intents**

---

## Next Steps After Testing

Once tests pass:

1. ✅ **Gateway is ready** - You can integrate payment processing
2. 🚀 **Create payment views** - Build checkout pages
3. 🧪 **Test with Stripe test cards** - Use test card `4242 4242 4242 4242`
4. 📱 **Add webhooks** - For automatic payment confirmations
5. 🔄 **Test different scenarios** - Failed payments, refunds, etc.

---

## Quick Command Reference

```bash
# Run full test suite
python test_payment_gateway.py

# Open Python shell for manual testing
python manage.py shell

# Check gateway in admin
# http://127.0.0.1:8000/admin/transactions/paymentgateway/
```

---

**Happy Testing!** 🎉

If all tests pass, your payment gateway is ready to use!


