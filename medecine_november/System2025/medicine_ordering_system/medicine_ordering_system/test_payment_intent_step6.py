"""
Step 6.1: Create a Test Payment Intent
From PAYMENT_GATEWAY_SETUP_GUIDE.md
"""
import os
import sys
import django

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'medicine_ordering_system.settings')
django.setup()

from transactions.services import PaymentGatewayFactory
from orders.models import Order
from decimal import Decimal

print("="*60)
print("  Step 6.1: Create a Test Payment Intent")
print("="*60)
print()

# Get payment service
print("1. Getting payment service...")
try:
    service = PaymentGatewayFactory.create_service()
    print(f"   ✅ Payment service created: {type(service).__name__}")
except Exception as e:
    print(f"   ❌ Error creating service: {e}")
    sys.exit(1)

# Get a test order (or create one)
print("\n2. Getting test order...")
order = Order.objects.first()  # Use any existing order

if not order:
    print("   ⚠️  No orders found. Creating a test order...")
    from accounts.models import User
    
    user = User.objects.filter(is_sales_rep=True).first()
    if not user:
        # Try any user
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
        print(f"   ✅ Created test order: {order.order_number}")
    else:
        print("   ❌ No users found. Cannot create test order.")
        sys.exit(1)
else:
    print(f"   ✅ Using existing order: {order.order_number}")
    print(f"      Customer: {order.customer_name}")
    print(f"      Amount: ₱{order.total_amount}")

# Create payment intent
print("\n3. Creating payment intent...")
print("   ⚠️  Note: Stripe doesn't support PHP directly.")
print("   Using USD for testing...")

try:
    # Use USD for testing since Stripe doesn't support PHP
    test_amount = Decimal('10.00')  # $10.00 USD
    
    result = service.create_payment_intent(
        order=order,
        amount=test_amount,
        currency='USD',  # Use USD for testing
        metadata={
            'test': 'true',
            'original_currency': 'PHP',
            'original_amount': str(order.total_amount),
            'order_number': order.order_number
        }
    )
    
    print("\n" + "="*60)
    print("  ✅ Payment Intent Created Successfully!")
    print("="*60)
    print(f"\nPayment Intent ID: {result['payment_intent_id']}")
    print(f"Client Secret: {result['client_secret'][:30]}...")
    print(f"Status: {result['status']}")
    print(f"Amount: ${test_amount} USD")
    print(f"\nFull Client Secret: {result['client_secret']}")
    
    print("\n" + "="*60)
    print("  Payment Intent Details:")
    print("="*60)
    print(f"  - Payment Intent ID: {result['payment_intent_id']}")
    print(f"  - Status: {result['status']}")
    print(f"  - Requires Action: {result.get('requires_action', 'N/A')}")
    if 'response' in result:
        print(f"  - Payment Method Types: {result['response'].get('payment_method_types', [])}")
    
    print("\n✅ Step 6.1 Complete! Payment intent created successfully.")
    print("\nYou can now:")
    print("  - Use the client_secret in your frontend to collect payment")
    print("  - Check payment status using get_payment_status()")
    print("  - Test with Stripe test cards (e.g., 4242 4242 4242 4242)")
    
except Exception as e:
    print("\n" + "="*60)
    print("  ❌ Error Creating Payment Intent")
    print("="*60)
    print(f"\nError: {e}")
    print("\nTroubleshooting:")
    print("  - Check that your payment gateway is active in admin")
    print("  - Verify API keys are correct")
    print("  - Make sure you're using test keys in test mode")
    import traceback
    traceback.print_exc()
    sys.exit(1)

