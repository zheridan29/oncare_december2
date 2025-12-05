# Step 6.1: Create Test Payment Intent - Instructions

## Quick Run (Easiest Method)

### Option 1: Use the Batch File

1. **Double-click** `run_step6_test.bat`
   - This will automatically activate the venv and run the test

OR

2. **Run from Command Prompt/PowerShell:**
   ```bash
   run_step6_test.bat
   ```

---

### Option 2: Manual Steps

#### Step 1: Open a New Terminal

Open a **new** Command Prompt or PowerShell window (not the Python shell).

#### Step 2: Navigate to Project Directory

```bash
cd "C:\Users\Ace Z Gutierrez\Videos\Masteral November\medecine_november\System2025\medicine_ordering_system\medicine_ordering_system"
```

#### Step 3: Activate Virtual Environment

**For Command Prompt:**
```bash
venv\Scripts\activate.bat
```

**For PowerShell:**
```bash
venv\Scripts\Activate.ps1
```

If you get an execution policy error in PowerShell, run:
```powershell
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
```

#### Step 4: Run the Test Script

```bash
python test_payment_intent_step6.py
```

---

### Option 3: Run in Django Shell (Interactive)

If you prefer to run it interactively:

#### Step 1: Open a New Terminal

#### Step 2: Navigate and Activate Venv

```bash
cd "C:\Users\Ace Z Gutierrez\Videos\Masteral November\medecine_november\System2025\medicine_ordering_system\medicine_ordering_system"
venv\Scripts\activate
```

#### Step 3: Open Django Shell

```bash
python manage.py shell
```

#### Step 4: Copy and Paste This Code

```python
from transactions.services import PaymentGatewayFactory
from orders.models import Order
from decimal import Decimal

# Get payment service
service = PaymentGatewayFactory.create_service()
print(f"✅ Payment service created: {type(service).__name__}")

# Get a test order
order = Order.objects.first()
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
        print("❌ No users found. Cannot create test order.")
else:
    print(f"✅ Using existing order: {order.order_number}")
    print(f"   Customer: {order.customer_name}")
    print(f"   Amount: ₱{order.total_amount}")

# Create payment intent
print("\n⚠️  Note: Stripe doesn't support PHP directly.")
print("Using USD for testing...")

try:
    result = service.create_payment_intent(
        order=order,
        amount=Decimal('10.00'),  # $10.00 USD
        currency='USD',  # Use USD for testing
        metadata={
            'test': 'true',
            'original_currency': 'PHP',
            'original_amount': str(order.total_amount)
        }
    )
    
    print("\n✅ Payment Intent Created Successfully!")
    print(f"Payment Intent ID: {result['payment_intent_id']}")
    print(f"Client Secret: {result['client_secret'][:30]}...")
    print(f"Status: {result['status']}")
    print(f"\nFull Client Secret: {result['client_secret']}")
    
except Exception as e:
    print(f"\n❌ Error: {e}")
    import traceback
    traceback.print_exc()
```

---

## Expected Output

When successful, you should see:

```
============================================================
  Step 6.1: Create a Test Payment Intent
============================================================

1. Getting payment service...
   ✅ Payment service created: StripePaymentService

2. Getting test order...
   ✅ Using existing order: ORD-ABC12345
      Customer: Test Customer
      Amount: ₱100.00

3. Creating payment intent...
   ⚠️  Note: Stripe doesn't support PHP directly.
   Using USD for testing...

============================================================
  ✅ Payment Intent Created Successfully!
============================================================

Payment Intent ID: pi_3Sae0YFPDvOzEmUZ08j9l4e3
Client Secret: pi_3Sae0YFPDvOzEmUZ08j9l4e3_se...
Status: requires_payment_method
Amount: $10.00 USD

✅ Step 6.1 Complete! Payment intent created successfully.
```

---

## Troubleshooting

### Issue: "No active payment gateway found"

**Solution:**
- Go to Django Admin → Payment Gateways
- Make sure one gateway has "Is Active" checked

### Issue: "ModuleNotFoundError: No module named 'stripe'"

**Solution:**
```bash
pip install stripe==7.0.0
```

### Issue: "Execution Policy Error" (PowerShell)

**Solution:**
```powershell
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
```

Then try activating the venv again.

---

## Next Steps

After successful payment intent creation:

1. ✅ Payment intent is created
2. 🚀 Use the `client_secret` in your frontend
3. 🧪 Test with Stripe test cards
4. 📝 Check payment status using `get_payment_status()`

---

**Choose the method that's easiest for you!** The batch file (Option 1) is the simplest. 🎉

