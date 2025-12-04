"""
Comprehensive unit tests for the orders module
"""

from django.test import TestCase, Client
from django.core.exceptions import ValidationError
from django.contrib.auth import get_user_model
from decimal import Decimal
from datetime import date, datetime
import json

from .models import Order, OrderItem, OrderStatusHistory, Cart, CartItem
from inventory.models import Category, Manufacturer, Medicine
from accounts.models import User

User = get_user_model()


class OrderModelTests(TestCase):
    """Test cases for Order model"""
    
    def setUp(self):
        """Set up test data"""
        self.user = User.objects.create_user(
            username='salesrep',
            email='sales@example.com',
            password='testpass123',
            role='sales_rep'
        )
        self.category = Category.objects.create(name='Antibiotics', is_active=True)
        self.manufacturer = Manufacturer.objects.create(name='Pfizer Inc.', country='USA', is_active=True)
        self.medicine = Medicine.objects.create(
            name='Amoxicillin',
            category=self.category,
            manufacturer=self.manufacturer,
            unit_price=Decimal('25.50'),
            cost_price=Decimal('15.00'),
            current_stock=100
        )
        self.order_data = {
            'sales_rep': self.user,
            'customer_name': 'John Doe',
            'customer_phone': '+1234567890',
            'customer_address': '123 Main St, City, State 12345',
            'subtotal': Decimal('51.00'),
            'tax_amount': Decimal('5.10'),
            'shipping_cost': Decimal('10.00'),
            'total_amount': Decimal('66.10'),
            'delivery_method': 'delivery',
            'delivery_address': '123 Main St, City, State 12345',
            'prescription_required': True,
            'customer_notes': 'Please deliver in the morning'
        }
    
    def test_order_creation(self):
        """Test order creation with valid data"""
        order = Order.objects.create(**self.order_data)
        self.assertEqual(order.sales_rep, self.user)
        self.assertEqual(order.customer_name, 'John Doe')
        self.assertEqual(order.customer_phone, '+1234567890')
        self.assertEqual(order.subtotal, Decimal('51.00'))
        self.assertEqual(order.total_amount, Decimal('66.10'))
        self.assertEqual(order.status, 'pending')
        self.assertEqual(order.payment_status, 'pending')
        self.assertTrue(order.prescription_required)
        self.assertIsNotNone(order.order_number)
        self.assertIsNotNone(order.created_at)
        self.assertIsNotNone(order.updated_at)
    
    def test_order_str_representation(self):
        """Test order string representation"""
        order = Order.objects.create(**self.order_data)
        expected_str = f"Order {order.order_number} - {order.customer_name}"
        self.assertEqual(str(order), expected_str)
    
    def test_order_number_generation(self):
        """Test automatic order number generation"""
        order = Order.objects.create(**self.order_data)
        self.assertTrue(order.order_number.startswith('ORD-'))
        self.assertEqual(len(order.order_number), 12)  # ORD- + 8 hex chars


class OrderItemModelTests(TestCase):
    """Test cases for OrderItem model"""
    
    def setUp(self):
        """Set up test data"""
        self.user = User.objects.create_user(
            username='salesrep',
            email='sales@example.com',
            password='testpass123',
            role='sales_rep'
        )
        self.category = Category.objects.create(name='Antibiotics', is_active=True)
        self.manufacturer = Manufacturer.objects.create(name='Pfizer Inc.', country='USA', is_active=True)
        self.medicine = Medicine.objects.create(
            name='Amoxicillin',
            category=self.category,
            manufacturer=self.manufacturer,
            unit_price=Decimal('25.50'),
            cost_price=Decimal('15.00'),
            current_stock=100
        )
        self.order = Order.objects.create(
            sales_rep=self.user,
            customer_name='John Doe',
            customer_phone='+1234567890',
            customer_address='123 Main St',
            subtotal=Decimal('51.00'),
            total_amount=Decimal('51.00')
        )
    
    def test_order_item_creation(self):
        """Test order item creation"""
        order_item = OrderItem.objects.create(
            order=self.order,
            medicine=self.medicine,
            quantity=2,
            unit_price=self.medicine.unit_price,
            total_price=self.medicine.unit_price * 2
        )
        self.assertEqual(order_item.order, self.order)
        self.assertEqual(order_item.medicine, self.medicine)
        self.assertEqual(order_item.quantity, 2)
        self.assertEqual(order_item.unit_price, self.medicine.unit_price)
        self.assertEqual(order_item.total_price, Decimal('51.00'))
        self.assertIsNotNone(order_item.created_at)
    
    def test_order_item_str_representation(self):
        """Test order item string representation"""
        order_item = OrderItem.objects.create(
            order=self.order,
            medicine=self.medicine,
            quantity=2,
            unit_price=self.medicine.unit_price,
            total_price=self.medicine.unit_price * 2
        )
        expected_str = f"{self.medicine.name} x {order_item.quantity} in Order {self.order.order_number}"
        self.assertEqual(str(order_item), expected_str)


class CartModelTests(TestCase):
    """Test cases for Cart model"""
    
    def setUp(self):
        """Set up test data"""
        self.user = User.objects.create_user(
            username='salesrep',
            email='sales@example.com',
            password='testpass123',
            role='sales_rep'
        )
        self.category = Category.objects.create(name='Antibiotics', is_active=True)
        self.manufacturer = Manufacturer.objects.create(name='Pfizer Inc.', country='USA', is_active=True)
        self.medicine = Medicine.objects.create(
            name='Amoxicillin',
            category=self.category,
            manufacturer=self.manufacturer,
            unit_price=Decimal('25.50'),
            cost_price=Decimal('15.00'),
            current_stock=100
        )
    
    def test_cart_creation(self):
        """Test cart creation"""
        cart = Cart.objects.create(sales_rep=self.user)
        self.assertEqual(cart.sales_rep, self.user)
        self.assertIsNotNone(cart.created_at)
        self.assertIsNotNone(cart.updated_at)
    
    def test_cart_str_representation(self):
        """Test cart string representation"""
        cart = Cart.objects.create(sales_rep=self.user)
        expected_str = f"Cart for {self.user.username}"
        self.assertEqual(str(cart), expected_str)
