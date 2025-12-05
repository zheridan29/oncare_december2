# Payment Service Implementation Guide

## Overview

A configurable payment service system has been implemented that allows administrators to choose and configure payment gateways through the Django admin interface.

---

## What Has Been Created

### 1. **PaymentGateway Model** (`transactions/models.py`)
- Stores payment gateway configuration (Stripe, PayMongo, PayPal, etc.)
- Admin can configure API keys, test/live mode
- Only one gateway can be active at a time
- Supports multiple gateway types

### 2. **Payment Service Abstraction Layer**
- **`BasePaymentService`** (`transactions/services/payment_service.py`)
  - Abstract base class for all payment gateways
  - Defines standard interface for payment operations
  - Easy to add new gateways

### 3. **Stripe Implementation**
- **`StripePaymentService`** (`transactions/services/stripe_service.py`)
  - Full Stripe integration
  - Payment intent creation
  - Payment confirmation
  - Refund processing
  - Webhook handling

### 4. **Payment Factory**
- **`PaymentGatewayFactory`** (`transactions/services/payment_factory.py`)
  - Creates payment service instances
  - Manages active gateway
  - Easy gateway switching

### 5. **Admin Interface**
- Payment Gateway configuration in Django admin
- Visual indicators for active/inactive, test/live mode
- API key management
- Gateway activation/deactivation

---

## How to Use

### Step 1: Install Stripe (for testing)

```bash
pip install stripe==7.0.0
```

### Step 2: Create Migration

```bash
python manage.py makemigrations transactions
python manage.py migrate
```

### Step 3: Configure Payment Gateway in Admin

1. Go to Django Admin → Transactions → Payment Gateways
2. Click "Add Payment Gateway"
3. Fill in:
   - **Name**: "Stripe Test" (or any name)
   - **Gateway Type**: Select "Stripe"
   - **Is Active**: ✅ (check to activate)
   - **Is Test Mode**: ✅ (check for test mode)
   - **API Key Public**: Your Stripe test publishable key (pk_test_...)
   - **API Key Secret**: Your Stripe test secret key (sk_test_...)
   - **Webhook Secret**: Your Stripe webhook secret (whsec_...)
4. Click "Save"

**Note**: Only one gateway can be active at a time. Activating a new gateway will automatically deactivate others.

---

## Configuration Guide

### For Stripe (Test Mode)

1. **Sign up** at https://stripe.com (free)
2. **Get Test API Keys**:
   - Go to Stripe Dashboard → Developers → API keys
   - Copy "Publishable key" → Paste in "API Key Public"
   - Copy "Secret key" → Paste in "API Key Secret"
3. **Get Webhook Secret** (optional for now):
   - Go to Developers → Webhooks
   - Create endpoint
   - Copy signing secret → Paste in "Webhook Secret"

### For PayMongo (Future)

When implemented, configuration will be similar:
- Sign up at https://paymongo.com
- Get API keys from dashboard
- Configure in admin interface

---

## Code Usage Examples

### Creating a Payment Intent

```python
from transactions.services import PaymentGatewayFactory
from orders.models import Order
from decimal import Decimal

# Get active payment service
payment_service = PaymentGatewayFactory.create_service()

# Create payment intent for an order
order = Order.objects.get(id=123)
amount = order.total_amount

result = payment_service.create_payment_intent(
    order=order,
    amount=amount,
    currency='PHP'
)

# Result contains:
# - payment_intent_id: Gateway's payment intent ID
# - client_secret: For frontend (Stripe)
# - redirect_url: URL to redirect user (if needed)
# - requires_action: Boolean
```

### Checking Payment Status

```python
payment_service = PaymentGatewayFactory.create_service()
status = payment_service.get_payment_status(payment_intent_id='pi_xxx')

# Status contains:
# - status: Payment status
# - amount: Payment amount
# - currency: Currency code
```

### Processing Refund

```python
payment_service = PaymentGatewayFactory.create_service()
refund = payment_service.create_refund(
    transaction_id='pi_xxx',
    amount=Decimal('100.00'),
    reason='Customer requested'
)
```

---

## Adding New Payment Gateways

To add a new payment gateway (e.g., PayMongo):

1. **Create Service Class** (`transactions/services/paymongo_service.py`):
```python
from .payment_service import BasePaymentService

class PayMongoPaymentService(BasePaymentService):
    def create_payment_intent(self, order, amount, currency='PHP', metadata=None):
        # Implement PayMongo payment creation
        pass
    
    # Implement other required methods...
```

2. **Register in Factory** (`transactions/services/payment_factory.py`):
```python
from .paymongo_service import PayMongoPaymentService

_services = {
    'stripe': StripePaymentService,
    'paymongo': PayMongoPaymentService,  # Add here
}
```

3. **Add to Model Choices** (`transactions/models.py`):
```python
GATEWAY_TYPES = [
    ('stripe', 'Stripe'),
    ('paymongo', 'PayMongo'),  # Add here
    # ...
]
```

That's it! The gateway will now be available in admin.

---

## Admin Features

### Visual Indicators

- **Status**: Green dot = Active, Gray dot = Inactive
- **Mode**: Orange = Test Mode, Red = Live Mode
- **Configuration**: Green check = Configured, Red X = Not Configured

### Actions

- **Activate Gateway**: Select a gateway and click "Activate selected gateway"
- **Deactivate Gateway**: Select gateways and click "Deactivate selected gateways"

### Safety Features

- Only one gateway can be active at a time
- Warnings when switching to live mode
- Warnings when gateway is not configured
- Test mode indicator clearly displayed

---

## Next Steps

1. **Create Migration**:
   ```bash
   python manage.py makemigrations transactions
   python manage.py migrate
   ```

2. **Install Stripe**:
   ```bash
   pip install stripe==7.0.0
   ```

3. **Configure Gateway**:
   - Go to admin
   - Add Stripe gateway with test keys
   - Activate it

4. **Test Payment Flow** (Future):
   - Create payment views
   - Create checkout templates
   - Test payment processing

---

## File Structure

```
transactions/
├── models.py                    # PaymentGateway model added
├── admin.py                     # PaymentGateway admin interface
├── services/
│   ├── __init__.py
│   ├── payment_service.py      # Abstract base class
│   ├── stripe_service.py       # Stripe implementation
│   └── payment_factory.py      # Gateway factory
└── webhooks/
    └── __init__.py             # (Future webhook handlers)
```

---

## Security Notes

⚠️ **Important**:
- API keys are stored in database (consider encryption for production)
- Never commit API keys to version control
- Use environment variables for sensitive data
- Test mode keys are safe to use in development
- Live mode keys should be carefully protected

---

## Testing

### Test Mode (Stripe)

Use Stripe test cards:
- **Success**: `4242 4242 4242 4242`
- **Decline**: `4000 0000 0000 0002`
- **3D Secure**: `4000 0025 0000 3155`

Any future expiry date, any 3-digit CVC.

---

**Status**: ✅ Payment service infrastructure created  
**Ready for**: Gateway configuration and testing  
**Next**: Create payment views and checkout flow


