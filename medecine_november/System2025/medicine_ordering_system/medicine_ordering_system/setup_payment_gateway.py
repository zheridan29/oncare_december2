"""
Quick setup script to verify payment gateway configuration
Run this after completing the setup steps
"""
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'medicine_ordering_system.settings')
django.setup()

def check_payment_gateway_setup():
    """Check if payment gateway is properly set up"""
    print("=" * 60)
    print("Payment Gateway Setup Verification")
    print("=" * 60)
    
    # Check if Stripe is installed
    print("\n1. Checking Stripe installation...")
    try:
        import stripe
        print(f"   ✅ Stripe installed (version {stripe.__version__})")
    except ImportError:
        print("   ❌ Stripe not installed. Run: pip install stripe==7.0.0")
        return False
    
    # Check PaymentGateway model
    print("\n2. Checking PaymentGateway model...")
    try:
        from transactions.models import PaymentGateway
        gateway_count = PaymentGateway.objects.count()
        print(f"   ✅ PaymentGateway model exists ({gateway_count} gateway(s) configured)")
    except Exception as e:
        print(f"   ❌ Error: {e}")
        return False
    
    # Check active gateway
    print("\n3. Checking active payment gateway...")
    try:
        from transactions.services import PaymentGatewayFactory
        
        gateway = PaymentGatewayFactory.get_active_gateway()
        if gateway:
            print(f"   ✅ Active Gateway: {gateway.name}")
            print(f"      Type: {gateway.get_gateway_type_display()}")
            print(f"      Mode: {'TEST' if gateway.is_test_mode else 'LIVE'}")
            print(f"      Configured: {'Yes' if gateway.is_configured else 'No'}")
            
            if not gateway.is_configured:
                print("   ⚠️  Warning: Gateway is not properly configured!")
                print("      Please add API credentials in Django admin.")
        else:
            print("   ⚠️  No active gateway found.")
            print("      Please configure and activate a gateway in Django admin.")
    except Exception as e:
        print(f"   ❌ Error: {e}")
        return False
    
    # Test service creation
    print("\n4. Testing payment service creation...")
    try:
        from transactions.services import PaymentGatewayFactory
        
        service = PaymentGatewayFactory.create_service()
        if service:
            print(f"   ✅ Payment service created: {service.__class__.__name__}")
        else:
            print("   ⚠️  Could not create payment service")
    except Exception as e:
        print(f"   ⚠️  Could not create payment service: {e}")
        print("      Make sure gateway is properly configured in admin.")
    
    print("\n" + "=" * 60)
    print("Setup Check Complete!")
    print("=" * 60)
    print("\nNext Steps:")
    print("1. Go to Django Admin → Payment Gateways")
    print("2. Add Stripe gateway with your test API keys")
    print("3. Activate the gateway")
    print("4. Run this script again to verify")
    
    return True

if __name__ == '__main__':
    check_payment_gateway_setup()

