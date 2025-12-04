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