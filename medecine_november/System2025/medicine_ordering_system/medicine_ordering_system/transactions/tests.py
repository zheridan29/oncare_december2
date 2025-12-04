"""
Comprehensive unit tests for the transactions module
"""

from django.test import TestCase, Client
from django.core.exceptions import ValidationError
from django.contrib.auth import get_user_model
from decimal import Decimal
from datetime import date, datetime
import json

from .models import PaymentMethod, Transaction, Refund, SalesReport
from accounts.models import User
from orders.models import Order

User = get_user_model()


class PaymentMethodModelTests(TestCase):
    """Test cases for PaymentMethod model"""
    
    def setUp(self):
        """Set up test data"""
        self.payment_method_data = {
            'name': 'Credit Card',
            'description': 'Credit card payments via Stripe',
            'is_active': True,
            'processing_fee_percentage': Decimal('2.9'),
            'processing_fee_fixed': Decimal('0.30')
        }
    
    def test_payment_method_creation(self):
        """Test payment method creation"""
        payment_method = PaymentMethod.objects.create(**self.payment_method_data)
        self.assertEqual(payment_method.name, 'Credit Card')
        self.assertEqual(payment_method.description, 'Credit card payments via Stripe')
        self.assertTrue(payment_method.is_active)
        self.assertEqual(payment_method.processing_fee_percentage, Decimal('2.9'))
        self.assertEqual(payment_method.processing_fee_fixed, Decimal('0.30'))
    
    def test_payment_method_str_representation(self):
        """Test payment method string representation"""
        payment_method = PaymentMethod.objects.create(**self.payment_method_data)
        self.assertEqual(str(payment_method), 'Credit Card')


class TransactionModelTests(TestCase):
    """Test cases for Transaction model"""
    
    def setUp(self):
        """Set up test data"""
        self.user = User.objects.create_user(
            username='salesrep',
            email='sales@example.com',
            password='testpass123',
            role='sales_rep'
        )
        self.payment_method = PaymentMethod.objects.create(
            name='Credit Card',
            description='Credit card payments',
            is_active=True
        )
        self.order = Order.objects.create(
            sales_rep=self.user,
            customer_name='John Doe',
            customer_phone='+1234567890',
            customer_address='123 Main St',
            subtotal=Decimal('100.00'),
            total_amount=Decimal('100.00')
        )
        self.transaction_data = {
            'order': self.order,
            'payment_method': self.payment_method,
            'transaction_type': 'payment',
            'status': 'pending',
            'amount': Decimal('100.00'),
            'processing_fee': Decimal('2.90'),
            'net_amount': Decimal('97.10'),
            'gateway_transaction_id': 'txn_123456789',
            'notes': 'Test transaction'
        }
    
    def test_transaction_creation(self):
        """Test transaction creation"""
        transaction = Transaction.objects.create(**self.transaction_data)
        self.assertEqual(transaction.order, self.order)
        self.assertEqual(transaction.payment_method, self.payment_method)
        self.assertEqual(transaction.transaction_type, 'payment')
        self.assertEqual(transaction.status, 'pending')
        self.assertEqual(transaction.amount, Decimal('100.00'))
        self.assertEqual(transaction.processing_fee, Decimal('2.90'))
        self.assertEqual(transaction.net_amount, Decimal('97.10'))
        self.assertEqual(transaction.gateway_transaction_id, 'txn_123456789')
        self.assertIsNotNone(transaction.transaction_id)
        self.assertIsNotNone(transaction.created_at)
    
    def test_transaction_str_representation(self):
        """Test transaction string representation"""
        transaction = Transaction.objects.create(**self.transaction_data)
        expected_str = f"Transaction {transaction.transaction_id} - {self.order.order_number}"
        self.assertEqual(str(transaction), expected_str)
    
    def test_transaction_id_generation(self):
        """Test automatic transaction ID generation"""
        transaction = Transaction.objects.create(**self.transaction_data)
        self.assertTrue(transaction.transaction_id.startswith('TXN-'))
        self.assertEqual(len(transaction.transaction_id), 16)  # TXN- + 12 hex chars
