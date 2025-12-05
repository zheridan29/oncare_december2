"""
Abstract base class for payment gateway services
"""
from abc import ABC, abstractmethod
from decimal import Decimal
from typing import Dict, Optional, Any
from django.conf import settings
import logging

logger = logging.getLogger(__name__)


class PaymentError(Exception):
    """Custom exception for payment processing errors"""
    pass


class BasePaymentService(ABC):
    """
    Abstract base class that all payment gateway services must implement
    """
    
    def __init__(self, gateway_config):
        """
        Initialize payment service with gateway configuration
        
        Args:
            gateway_config: PaymentGateway model instance
        """
        self.gateway = gateway_config
        self.is_test_mode = gateway_config.is_test_mode
        self.api_key_public = gateway_config.api_key_public
        self.api_key_secret = gateway_config.api_key_secret
        self.config = gateway_config.config or {}
    
    @abstractmethod
    def create_payment_intent(self, order, amount: Decimal, currency: str = 'PHP', metadata: Optional[Dict] = None) -> Dict[str, Any]:
        """
        Create a payment intent/request with the gateway
        
        Args:
            order: Order instance
            amount: Payment amount
            currency: Currency code (default: PHP)
            metadata: Additional metadata to pass to gateway
            
        Returns:
            Dictionary with:
                - 'payment_intent_id': Gateway's payment intent ID
                - 'client_secret': Client secret for frontend (if applicable)
                - 'redirect_url': URL to redirect user for payment (if applicable)
                - 'requires_action': Boolean indicating if user action is needed
        """
        pass
    
    @abstractmethod
    def confirm_payment(self, payment_intent_id: str, payment_method_id: Optional[str] = None) -> Dict[str, Any]:
        """
        Confirm/complete a payment
        
        Args:
            payment_intent_id: Payment intent ID from gateway
            payment_method_id: Payment method ID (if applicable)
            
        Returns:
            Dictionary with:
                - 'status': Payment status (succeeded, failed, etc.)
                - 'transaction_id': Gateway transaction ID
                - 'response': Full gateway response
        """
        pass
    
    @abstractmethod
    def get_payment_status(self, payment_intent_id: str) -> Dict[str, Any]:
        """
        Get current status of a payment
        
        Args:
            payment_intent_id: Payment intent ID from gateway
            
        Returns:
            Dictionary with payment status information
        """
        pass
    
    @abstractmethod
    def create_refund(self, transaction_id: str, amount: Optional[Decimal] = None, reason: Optional[str] = None) -> Dict[str, Any]:
        """
        Create a refund
        
        Args:
            transaction_id: Gateway transaction ID to refund
            amount: Refund amount (None for full refund)
            reason: Refund reason
            
        Returns:
            Dictionary with refund information
        """
        pass
    
    @abstractmethod
    def verify_webhook_signature(self, payload: bytes, signature: str, secret: str) -> bool:
        """
        Verify webhook signature from gateway
        
        Args:
            payload: Raw webhook payload
            signature: Signature header from gateway
            secret: Webhook secret
            
        Returns:
            Boolean indicating if signature is valid
        """
        pass
    
    @abstractmethod
    def handle_webhook_event(self, event_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Handle webhook event from gateway
        
        Args:
            event_data: Parsed webhook event data
            
        Returns:
            Dictionary with handling result
        """
        pass
    
    def get_required_config(self) -> list:
        """
        Get list of required configuration keys for this gateway
        
        Returns:
            List of required configuration key names
        """
        return []
    
    def is_configured(self) -> bool:
        """
        Check if gateway is properly configured
        
        Returns:
            Boolean indicating if gateway is configured
        """
        required = self.get_required_config()
        if not required:
            return True
        
        for key in required:
            if not getattr(self, key, None):
                return False
        return True
    
    def validate_amount(self, amount: Decimal) -> bool:
        """
        Validate payment amount
        
        Args:
            amount: Amount to validate
            
        Returns:
            Boolean indicating if amount is valid
        """
        if amount <= 0:
            return False
        # Add gateway-specific minimum/maximum validation if needed
        return True
    
    def format_amount(self, amount: Decimal, currency: str = 'PHP') -> int:
        """
        Format amount according to gateway requirements (usually in smallest currency unit)
        
        Args:
            amount: Amount in decimal format
            currency: Currency code
            
        Returns:
            Amount in smallest currency unit (e.g., cents, centavos)
        """
        # Most gateways use smallest currency unit (cents, centavos, etc.)
        return int(amount * 100)
    
    def parse_amount(self, amount: int, currency: str = 'PHP') -> Decimal:
        """
        Parse amount from gateway format (smallest currency unit) to decimal
        
        Args:
            amount: Amount in smallest currency unit
            currency: Currency code
            
        Returns:
            Amount as Decimal
        """
        return Decimal(amount) / 100


