"""
Utility functions for payment processing
"""
from common.models import SystemConfiguration
from transactions.services import PaymentGatewayFactory
from decimal import Decimal


def get_manual_payment_details():
    """
    Get manual payment details (bank account, etc.) from SystemConfiguration
    
    Returns:
        dict: Payment details including bank name, account number, account name, etc.
    """
    payment_details = {}
    
    try:
        # Get payment configuration
        configs = SystemConfiguration.objects.filter(config_type='payments')
        
        for config in configs:
            key = config.key
            value = config.get_typed_value()
            
            if key.startswith('payment_'):
                # Remove 'payment_' prefix for cleaner keys
                clean_key = key.replace('payment_', '')
                payment_details[clean_key] = value
        
        # Set defaults if not configured
        if not payment_details.get('bank_name'):
            payment_details['bank_name'] = 'OnCare Bank'
        if not payment_details.get('account_name'):
            payment_details['account_name'] = 'OnCare Medicine Ordering System'
        if not payment_details.get('account_number'):
            payment_details['account_number'] = 'Please configure in System Settings'
        if not payment_details.get('swift_code'):
            payment_details['swift_code'] = ''
        if not payment_details.get('instructions'):
            payment_details['instructions'] = 'Please include your order number in the payment reference.'
        
    except Exception as e:
        # Return defaults if there's an error
        payment_details = {
            'bank_name': 'OnCare Bank',
            'account_name': 'OnCare Medicine Ordering System',
            'account_number': 'Please configure in System Settings',
            'swift_code': '',
            'instructions': 'Please include your order number in the payment reference.',
        }
    
    return payment_details


def is_payment_gateway_available():
    """
    Check if payment gateway is available and configured
    
    Returns:
        bool: True if payment gateway is available
    """
    try:
        gateway = PaymentGatewayFactory.get_active_gateway()
        if gateway and gateway.is_configured:
            service = PaymentGatewayFactory.create_service()
            return service is not None
        return False
    except Exception:
        return False


def convert_php_to_usd(php_amount):
    """
    Convert PHP amount to USD for payment processing
    This is a simple conversion - in production, use real-time exchange rates
    
    Args:
        php_amount: Decimal amount in PHP
        
    Returns:
        Decimal: Amount in USD
    """
    # Default exchange rate: 1 PHP = 0.018 USD (approximate)
    # In production, fetch from an API or use a more accurate rate
    exchange_rate = Decimal('0.018')
    return (php_amount * exchange_rate).quantize(Decimal('0.01'))


def get_payment_context(order):
    """
    Get payment context for an order
    
    Args:
        order: Order instance
        
    Returns:
        dict: Payment context including gateway availability, payment details, etc.
    """
    context = {
        'payment_gateway_available': is_payment_gateway_available(),
        'manual_payment_details': get_manual_payment_details(),
        'can_pay_online': order.payment_status == 'pending' and order.status != 'cancelled',
        # Show manual payment for any status as long as payment is pending and order is not cancelled
        'show_manual_payment': order.payment_status == 'pending' and order.status != 'cancelled',
        'order_amount_usd': convert_php_to_usd(order.total_amount) if is_payment_gateway_available() else None,
    }
    
    return context

