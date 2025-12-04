"""
Test script for payment gateway configuration
Run this to verify your payment gateway is working correctly
"""
import os
import sys
import django

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'medicine_ordering_system.settings')
django.setup()

from transactions.services import PaymentGatewayFactory
from transactions.models import PaymentGateway, Transaction, PaymentMethod
from orders.models import Order
from decimal import Decimal
import traceback

def print_section(title):
    """Print a formatted section header"""
    print("\n" + "="*60)
    print(f"  {title}")
    print("="*60)

def test_gateway_configuration():
    """Test 1: Check gateway configuration"""
    print_section("TEST 1: Gateway Configuration")
    
    try:
        # Get active gateway
        gateway = PaymentGatewayFactory.get_active_gateway()
        
        if gateway is None:
            print("❌ ERROR: No active payment gateway found!")
            print("\nSolution:")
            print("  1. Go to Django Admin → Transactions → Payment Gateways")
            print("  2. Make sure one gateway has 'Is Active' checked")
            return False
        
        print(f"✅ Active Gateway Found: {gateway.name}")
        print(f"   Gateway Type: {gateway.gateway_type}")
        print(f"   Status: {'Active' if gateway.is_active else 'Inactive'}")
        print(f"   Mode: {'TEST MODE' if gateway.is_test_mode else 'LIVE MODE'}")
        print(f"   Configured: {'Yes' if gateway.is_configured else 'No'}")
        
        if not gateway.is_configured:
            print("\n⚠️  WARNING: Gateway is not properly configured!")
            print("   Make sure API Key Secret is filled in.")
            return False
        
        if not gateway.is_test_mode:
            print("\n⚠️  WARNING: Gateway is in LIVE MODE!")
            print("   Real transactions will be processed. Make sure you want this.")
        
        return True
        
    except Exception as e:
        print(f"❌ ERROR: {str(e)}")
        traceback.print_exc()
        return False

def test_service_creation():
    """Test 2: Create payment service"""
    print_section("TEST 2: Payment Service Creation")
    
    try:
        service = PaymentGatewayFactory.create_service()
        
        if service is None:
            print("❌ ERROR: Could not create payment service!")
            return False
        
        print(f"✅ Payment Service Created Successfully!")
        print(f"   Service Type: {type(service).__name__}")
        print(f"   Test Mode: {service.is_test_mode}")
        print(f"   Configured: {service.is_configured()}")
        print(f"   Gateway: {service.gateway.name}")
        
        return True, service
        
    except Exception as e:
        print(f"❌ ERROR: {str(e)}")
        traceback.print_exc()
        return False, None

def test_payment_intent_creation(service):
    """Test 3: Create a payment intent"""
    print_section("TEST 3: Payment Intent Creation")
    
    try:
        # Get or create a test order
        order = Order.objects.first()
        
        if not order:
            print("⚠️  No orders found. Creating a test order...")
            # Create a minimal test order
            from accounts.models import User
            user = User.objects.filter(is_sales_rep=True).first()
            if not user:
                print("❌ ERROR: No sales rep user found. Cannot create test order.")
                return False
            
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
        
        print(f"Using order: {order.order_number}")
        print(f"Order amount: ₱{order.total_amount}")
        
        # Note: Stripe doesn't support PHP directly
        # For testing, we'll try with USD or skip if PHP is not supported
        print("\n⚠️  NOTE: Stripe doesn't natively support PHP (Philippine Peso)")
        print("   Testing with USD instead for payment intent creation...")
        
        # Use USD for testing (minimum $1.00)
        test_amount_usd = Decimal('10.00')  # $10.00 USD
        
        result = service.create_payment_intent(
            order=order,
            amount=test_amount_usd,
            currency='USD',  # Use USD for testing
            metadata={'test': 'true', 'original_currency': 'PHP', 'original_amount': str(order.total_amount)}
        )
        
        print(f"✅ Payment Intent Created Successfully!")
        print(f"   Payment Intent ID: {result['payment_intent_id']}")
        print(f"   Status: {result['status']}")
        
        if 'client_secret' in result:
            print(f"   Client Secret: {result['client_secret'][:30]}...")
        
        return True, result['payment_intent_id']
        
    except Exception as e:
        error_msg = str(e)
        if "currency" in error_msg.lower() or "php" in error_msg.lower():
            print(f"⚠️  WARNING: Currency limitation detected")
            print(f"   Error: {error_msg}")
            print(f"\n   Recommendation:")
            print(f"   - Stripe doesn't support PHP directly")
            print(f"   - Use USD for testing: currency='USD'")
            print(f"   - Or consider PayMongo for PHP support")
            return False, None
        else:
            print(f"❌ ERROR: {str(e)}")
            traceback.print_exc()
            return False, None

def test_payment_status_check(service, payment_intent_id):
    """Test 4: Check payment status"""
    print_section("TEST 4: Payment Status Check")
    
    try:
        status = service.get_payment_status(payment_intent_id)
        
        print(f"✅ Payment Status Retrieved!")
        print(f"   Status: {status['status']}")
        print(f"   Amount: ₱{status.get('amount', 'N/A')}")
        print(f"   Currency: {status.get('currency', 'N/A')}")
        
        return True
        
    except Exception as e:
        print(f"❌ ERROR: {str(e)}")
        traceback.print_exc()
        return False

def test_gateway_api_connection(service):
    """Test 5: Test gateway API connection"""
    print_section("TEST 5: Gateway API Connection")
    
    try:
        # Get or create a test order for connection test
        from accounts.models import User
        
        order = Order.objects.first()
        if not order:
            user = User.objects.filter(is_sales_rep=True).first()
            if not user:
                print("⚠️  No orders or users found. Skipping connection test.")
                return False
            
            order = Order.objects.create(
                sales_rep=user,
                customer_name="API Test Customer",
                customer_phone="1234567890",
                customer_address="Test Address",
                status='pending',
                payment_status='pending',
                subtotal=Decimal('10.00'),
                total_amount=Decimal('10.00'),
                delivery_method='pickup'
            )
        
        # This will test if we can connect to Stripe API
        # Use USD for testing since Stripe doesn't support PHP
        print("⚠️  NOTE: Using USD for API connection test (Stripe doesn't support PHP)")
        test_result = service.create_payment_intent(
            order=order,
            amount=Decimal('10.00'),
            currency='USD',  # Use USD for testing
            metadata={'test': 'connection_test'}
        )
        
        print(f"✅ API Connection Successful!")
        print(f"   Can communicate with Stripe API")
        print(f"   Payment Intent ID: {test_result['payment_intent_id']}")
        
        return True
        
    except Exception as e:
        error_msg = str(e)
        if "Invalid API Key" in error_msg or "authentication" in error_msg.lower() or "api key" in error_msg.lower():
            print(f"❌ ERROR: API Authentication Failed!")
            print(f"   Issue: {error_msg}")
            print("\nSolution:")
            print("  1. Check your API keys in Admin → Payment Gateways")
            print("  2. Make sure you're using TEST keys (sk_test_...) in TEST mode")
            print("  3. Verify keys are copied correctly (they're very long!)")
        else:
            print(f"❌ ERROR: {error_msg}")
            traceback.print_exc()
        return False

def run_all_tests():
    """Run all tests"""
    print("\n" + "="*60)
    print("  PAYMENT GATEWAY TEST SUITE")
    print("="*60)
    print("\nRunning tests to verify payment gateway configuration...")
    
    results = {}
    
    # Test 1: Gateway Configuration
    results['config'] = test_gateway_configuration()
    if not results['config']:
        print("\n❌ Configuration test failed. Please fix issues before continuing.")
        return
    
    # Test 2: Service Creation
    result, service = test_service_creation()
    results['service'] = result
    if not result or service is None:
        print("\n❌ Service creation failed. Please check gateway configuration.")
        return
    
    # Test 3: Payment Intent Creation
    result, payment_intent_id = test_payment_intent_creation(service)
    results['intent'] = result
    
    # Test 4: Payment Status Check (if intent was created)
    if result and payment_intent_id:
        results['status'] = test_payment_status_check(service, payment_intent_id)
    else:
        results['status'] = False
    
    # Test 5: API Connection
    results['api'] = test_gateway_api_connection(service)
    
    # Summary
    print_section("TEST SUMMARY")
    
    total_tests = len(results)
    passed_tests = sum(1 for v in results.values() if v)
    
    print(f"Tests Passed: {passed_tests}/{total_tests}")
    print()
    
    for test_name, passed in results.items():
        status = "✅ PASS" if passed else "❌ FAIL"
        print(f"  {status} - {test_name.replace('_', ' ').title()}")
    
    print()
    
    if passed_tests == total_tests:
        print("🎉 ALL TESTS PASSED! Your payment gateway is working correctly!")
    else:
        print("⚠️  Some tests failed. Please check the errors above.")
    
    print("\n" + "="*60)

if __name__ == '__main__':
    run_all_tests()

