"""
Factory for creating payment gateway service instances
"""
from typing import Optional
from django.core.exceptions import ImproperlyConfigured
import logging

from transactions.models import PaymentGateway
from .stripe_service import StripePaymentService
from .payment_service import BasePaymentService

logger = logging.getLogger(__name__)


class PaymentGatewayFactory:
    """
    Factory class to create payment gateway service instances
    """
    
    # Registry of available payment services
    _services = {
        'stripe': StripePaymentService,
        # Add more gateways here as they are implemented
        # 'paymongo': PayMongoPaymentService,
        # 'paypal': PayPalPaymentService,
    }
    
    @classmethod
    def get_active_gateway(cls) -> Optional[PaymentGateway]:
        """
        Get the currently active payment gateway
        
        Returns:
            PaymentGateway instance or None
        """
        try:
            return PaymentGateway.objects.filter(is_active=True).first()
        except Exception as e:
            logger.error(f"Error getting active gateway: {e}")
            return None
    
    @classmethod
    def create_service(cls, gateway: Optional[PaymentGateway] = None) -> Optional[BasePaymentService]:
        """
        Create a payment service instance
        
        Args:
            gateway: PaymentGateway instance (if None, uses active gateway)
            
        Returns:
            Payment service instance or None
        """
        if gateway is None:
            gateway = cls.get_active_gateway()
        
        if gateway is None:
            logger.warning("No active payment gateway found")
            return None
        
        if not gateway.is_configured:
            logger.error(f"Payment gateway {gateway.name} is not properly configured")
            raise ImproperlyConfigured(f"Payment gateway {gateway.name} is not properly configured")
        
        service_class = cls._services.get(gateway.gateway_type)
        if service_class is None:
            logger.error(f"Payment gateway type '{gateway.gateway_type}' is not supported")
            raise ImproperlyConfigured(f"Payment gateway type '{gateway.gateway_type}' is not supported")
        
        try:
            service = service_class(gateway)
            if not service.is_configured():
                logger.error(f"Payment gateway {gateway.name} service is not properly configured")
                raise ImproperlyConfigured(f"Payment gateway {gateway.name} service is not properly configured")
            return service
        except Exception as e:
            logger.error(f"Error creating payment service: {e}")
            raise
    
    @classmethod
    def register_service(cls, gateway_type: str, service_class):
        """
        Register a new payment service class
        
        Args:
            gateway_type: Gateway type identifier (e.g., 'paymongo')
            service_class: Service class that extends BasePaymentService
        """
        cls._services[gateway_type] = service_class
        logger.info(f"Registered payment service: {gateway_type}")
    
    @classmethod
    def get_available_gateways(cls) -> list:
        """
        Get list of available gateway types
        
        Returns:
            List of gateway type identifiers
        """
        return list(cls._services.keys())


