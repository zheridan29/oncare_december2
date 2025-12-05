"""
Stripe payment gateway service implementation
"""
from decimal import Decimal
from typing import Dict, Optional, Any
import stripe
from django.conf import settings
import logging

from .payment_service import BasePaymentService, PaymentError

logger = logging.getLogger(__name__)


class StripePaymentService(BasePaymentService):
    """
    Stripe payment gateway service implementation
    """
    
    def __init__(self, gateway_config):
        super().__init__(gateway_config)
        
        # Set Stripe API key
        stripe.api_key = self.api_key_secret
        
        # Set test mode if applicable
        if self.is_test_mode:
            logger.info("Stripe service initialized in TEST mode")
        else:
            logger.info("Stripe service initialized in LIVE mode")
    
    def get_required_config(self) -> list:
        """Get required configuration keys for Stripe"""
        return ['api_key_secret']
    
    def create_payment_intent(
        self,
        order,
        amount: Decimal,
        currency: str = 'PHP',
        metadata: Optional[Dict] = None
    ) -> Dict[str, Any]:
        """
        Create a Stripe Payment Intent
        """
        try:
            if not self.validate_amount(amount):
                raise PaymentError("Invalid payment amount")
            
            # Prepare metadata
            payment_metadata = {
                'order_id': str(order.id),
                'order_number': order.order_number,
            }
            if metadata:
                payment_metadata.update(metadata)
            
            # Create payment intent
            intent = stripe.PaymentIntent.create(
                amount=self.format_amount(amount, currency),
                currency=currency.lower(),
                metadata=payment_metadata,
                description=f"Order {order.order_number}",
                automatic_payment_methods={
                    'enabled': True,
                },
            )
            
            logger.info(f"Created Stripe Payment Intent: {intent.id} for Order {order.order_number}")
            
            return {
                'payment_intent_id': intent.id,
                'client_secret': intent.client_secret,
                'status': intent.status,
                'requires_action': intent.status == 'requires_payment_method',
                'response': intent.to_dict(),
            }
            
        except stripe.error.StripeError as e:
            logger.error(f"Stripe error creating payment intent: {e}")
            raise PaymentError(f"Stripe error: {str(e)}")
        except Exception as e:
            logger.error(f"Unexpected error creating payment intent: {e}")
            raise PaymentError(f"Payment processing error: {str(e)}")
    
    def confirm_payment(
        self,
        payment_intent_id: str,
        payment_method_id: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        Confirm a Stripe Payment Intent
        """
        try:
            intent = stripe.PaymentIntent.retrieve(payment_intent_id)
            
            # If payment method is provided, confirm the intent
            if payment_method_id and intent.status == 'requires_payment_method':
                intent = stripe.PaymentIntent.confirm(
                    payment_intent_id,
                    payment_method=payment_method_id,
                )
            
            return {
                'status': intent.status,
                'transaction_id': intent.id,
                'response': intent.to_dict(),
            }
            
        except stripe.error.StripeError as e:
            logger.error(f"Stripe error confirming payment: {e}")
            raise PaymentError(f"Stripe error: {str(e)}")
        except Exception as e:
            logger.error(f"Unexpected error confirming payment: {e}")
            raise PaymentError(f"Payment confirmation error: {str(e)}")
    
    def get_payment_status(self, payment_intent_id: str) -> Dict[str, Any]:
        """
        Get payment status from Stripe
        """
        try:
            intent = stripe.PaymentIntent.retrieve(payment_intent_id)
            
            return {
                'status': intent.status,
                'amount': self.parse_amount(intent.amount, intent.currency),
                'currency': intent.currency.upper(),
                'transaction_id': intent.id,
                'response': intent.to_dict(),
            }
            
        except stripe.error.StripeError as e:
            logger.error(f"Stripe error getting payment status: {e}")
            raise PaymentError(f"Stripe error: {str(e)}")
    
    def create_refund(
        self,
        transaction_id: str,
        amount: Optional[Decimal] = None,
        reason: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        Create a refund in Stripe
        """
        try:
            refund_params = {
                'payment_intent': transaction_id,
            }
            
            if amount:
                refund_params['amount'] = self.format_amount(amount)
            
            if reason:
                refund_params['reason'] = reason
            
            refund = stripe.Refund.create(**refund_params)
            
            logger.info(f"Created Stripe refund: {refund.id} for Payment Intent {transaction_id}")
            
            return {
                'refund_id': refund.id,
                'status': refund.status,
                'amount': self.parse_amount(refund.amount),
                'response': refund.to_dict(),
            }
            
        except stripe.error.StripeError as e:
            logger.error(f"Stripe error creating refund: {e}")
            raise PaymentError(f"Stripe error: {str(e)}")
    
    def verify_webhook_signature(self, payload: bytes, signature: str, secret: str) -> bool:
        """
        Verify Stripe webhook signature
        """
        try:
            stripe.Webhook.construct_event(
                payload,
                signature,
                secret
            )
            return True
        except ValueError:
            logger.error("Invalid Stripe webhook payload")
            return False
        except stripe.error.SignatureVerificationError:
            logger.error("Invalid Stripe webhook signature")
            return False
        except Exception as e:
            logger.error(f"Error verifying Stripe webhook signature: {e}")
            return False
    
    def handle_webhook_event(self, event_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Handle Stripe webhook event
        """
        event_type = event_data.get('type')
        event_object = event_data.get('data', {}).get('object', {})
        
        logger.info(f"Handling Stripe webhook event: {event_type}")
        
        result = {
            'event_type': event_type,
            'processed': False,
            'transaction_id': None,
            'status': None,
        }
        
        if event_type == 'payment_intent.succeeded':
            result.update({
                'processed': True,
                'transaction_id': event_object.get('id'),
                'status': 'completed',
            })
        elif event_type == 'payment_intent.payment_failed':
            result.update({
                'processed': True,
                'transaction_id': event_object.get('id'),
                'status': 'failed',
            })
        elif event_type == 'charge.refunded':
            result.update({
                'processed': True,
                'transaction_id': event_object.get('payment_intent'),
                'status': 'refunded',
            })
        
        return result


