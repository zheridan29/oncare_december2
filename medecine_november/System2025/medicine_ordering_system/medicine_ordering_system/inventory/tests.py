"""
Comprehensive unit tests for the inventory module
"""

from django.test import TestCase, Client
from django.core.exceptions import ValidationError
from django.contrib.auth import get_user_model
from decimal import Decimal
from datetime import date, datetime
import json

from .models import (
    Category, Manufacturer, Medicine, StockMovement, 
    ReorderAlert, MedicineImage
)
from accounts.models import User

User = get_user_model()


class CategoryModelTests(TestCase):
    """Test cases for Category model"""
    
    def setUp(self):
        """Set up test data"""
        self.category_data = {
            'name': 'Antibiotics',
            'description': 'Medicines that fight bacterial infections',
            'is_active': True
        }
    
    def test_category_creation(self):
        """Test category creation with valid data"""
        category = Category.objects.create(**self.category_data)
        self.assertEqual(category.name, 'Antibiotics')
        self.assertEqual(category.description, 'Medicines that fight bacterial infections')
        self.assertTrue(category.is_active)
        self.assertIsNotNone(category.created_at)
    
    def test_category_str_representation(self):
        """Test category string representation"""
        category = Category.objects.create(**self.category_data)
        self.assertEqual(str(category), 'Antibiotics')
    
    def test_category_hierarchy(self):
        """Test category parent-child relationships"""
        parent = Category.objects.create(name='Medicines', is_active=True)
        child = Category.objects.create(
            name='Antibiotics',
            parent_category=parent,
            is_active=True
        )
        self.assertEqual(child.parent_category, parent)
        self.assertIn(child, parent.category_set.all())


class ManufacturerModelTests(TestCase):
    """Test cases for Manufacturer model"""
    
    def setUp(self):
        """Set up test data"""
        self.manufacturer_data = {
            'name': 'Pfizer Inc.',
            'country': 'USA',
            'contact_email': 'contact@pfizer.com',
            'contact_phone': '+1-555-123-4567',
            'website': 'https://www.pfizer.com',
            'is_active': True
        }
    
    def test_manufacturer_creation(self):
        """Test manufacturer creation with valid data"""
        manufacturer = Manufacturer.objects.create(**self.manufacturer_data)
        self.assertEqual(manufacturer.name, 'Pfizer Inc.')
        self.assertEqual(manufacturer.country, 'USA')
        self.assertEqual(manufacturer.contact_email, 'contact@pfizer.com')
        self.assertEqual(manufacturer.contact_phone, '+1-555-123-4567')
        self.assertEqual(manufacturer.website, 'https://www.pfizer.com')
        self.assertTrue(manufacturer.is_active)
        self.assertIsNotNone(manufacturer.created_at)
    
    def test_manufacturer_str_representation(self):
        """Test manufacturer string representation"""
        manufacturer = Manufacturer.objects.create(**self.manufacturer_data)
        self.assertEqual(str(manufacturer), 'Pfizer Inc.')


class MedicineModelTests(TestCase):
    """Test cases for Medicine model"""
    
    def setUp(self):
        """Set up test data"""
        self.category = Category.objects.create(
            name='Antibiotics',
            description='Antibacterial medicines',
            is_active=True
        )
        self.manufacturer = Manufacturer.objects.create(
            name='Pfizer Inc.',
            country='USA',
            is_active=True
        )
        self.medicine_data = {
            'name': 'Amoxicillin',
            'generic_name': 'Amoxicillin',
            'description': 'Broad-spectrum antibiotic',
            'category': self.category,
            'manufacturer': self.manufacturer,
            'dosage_form': 'Capsule',
            'strength': '500mg',
            'prescription_type': 'prescription',
            'unit_price': Decimal('25.50'),
            'cost_price': Decimal('15.00'),
            'current_stock': 100,
            'minimum_stock_level': 10,
            'maximum_stock_level': 1000,
            'reorder_point': 20,
            'weight': Decimal('0.5'),
            'dimensions': '2x1x0.5 cm',
            'storage_conditions': 'Store at room temperature',
            'ndc_number': '12345-678-90',
            'fda_approval_date': date(2020, 1, 1),
            'expiry_date': date(2025, 12, 31),
            'is_active': True,
            'is_available': True,
            'requires_prescription': True
        }
    
    def test_medicine_creation(self):
        """Test medicine creation with valid data"""
        medicine = Medicine.objects.create(**self.medicine_data)
        self.assertEqual(medicine.name, 'Amoxicillin')
        self.assertEqual(medicine.generic_name, 'Amoxicillin')
        self.assertEqual(medicine.category, self.category)
        self.assertEqual(medicine.manufacturer, self.manufacturer)
        self.assertEqual(medicine.unit_price, Decimal('25.50'))
        self.assertEqual(medicine.current_stock, 100)
        self.assertTrue(medicine.requires_prescription)
        self.assertIsNotNone(medicine.created_at)
        self.assertIsNotNone(medicine.updated_at)
    
    def test_medicine_str_representation(self):
        """Test medicine string representation"""
        medicine = Medicine.objects.create(**self.medicine_data)
        expected_str = f"{medicine.name} ({medicine.strength})"
        self.assertEqual(str(medicine), expected_str)
    
    def test_medicine_stock_properties(self):
        """Test medicine stock-related properties"""
        # Test normal stock
        medicine = Medicine.objects.create(**self.medicine_data)
        self.assertFalse(medicine.is_low_stock)
        self.assertFalse(medicine.is_out_of_stock)
        self.assertEqual(medicine.stock_status, "In Stock")
        
        # Test low stock
        medicine.current_stock = 15  # Below reorder point of 20
        medicine.save()
        self.assertTrue(medicine.is_low_stock)
        self.assertFalse(medicine.is_out_of_stock)
        self.assertEqual(medicine.stock_status, "Low Stock")
        
        # Test out of stock
        medicine.current_stock = 0
        medicine.save()
        self.assertFalse(medicine.is_low_stock)
        self.assertTrue(medicine.is_out_of_stock)
        self.assertEqual(medicine.stock_status, "Out of Stock")


class StockMovementModelTests(TestCase):
    """Test cases for StockMovement model"""
    
    def setUp(self):
        """Set up test data"""
        self.user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpass123',
            role='pharmacist_admin'
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
    
    def test_stock_movement_creation(self):
        """Test stock movement creation"""
        movement = StockMovement.objects.create(
            medicine=self.medicine,
            movement_type='in',
            quantity=50,
            reference_number='PO-001',
            notes='New stock received',
            created_by=self.user
        )
        self.assertEqual(movement.medicine, self.medicine)
        self.assertEqual(movement.movement_type, 'in')
        self.assertEqual(movement.quantity, 50)
        self.assertEqual(movement.reference_number, 'PO-001')
        self.assertEqual(movement.created_by, self.user)
        self.assertIsNotNone(movement.created_at)
    
    def test_stock_movement_str_representation(self):
        """Test stock movement string representation"""
        movement = StockMovement.objects.create(
            medicine=self.medicine,
            movement_type='out',
            quantity=10,
            created_by=self.user
        )
        expected_str = f"out - {self.medicine.name} - 10"
        self.assertEqual(str(movement), expected_str)


class ReorderAlertModelTests(TestCase):
    """Test cases for ReorderAlert model"""
    
    def setUp(self):
        """Set up test data"""
        self.user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpass123',
            role='pharmacist_admin'
        )
        self.category = Category.objects.create(name='Antibiotics', is_active=True)
        self.manufacturer = Manufacturer.objects.create(name='Pfizer Inc.', country='USA', is_active=True)
        self.medicine = Medicine.objects.create(
            name='Amoxicillin',
            category=self.category,
            manufacturer=self.manufacturer,
            unit_price=Decimal('25.50'),
            cost_price=Decimal('15.00'),
            current_stock=5,  # Below reorder point
            reorder_point=20
        )
    
    def test_reorder_alert_creation(self):
        """Test reorder alert creation"""
        alert = ReorderAlert.objects.create(
            medicine=self.medicine,
            current_stock=5,
            reorder_point=20,
            suggested_quantity=100,
            priority='high',
            is_processed=False
        )
        self.assertEqual(alert.medicine, self.medicine)
        self.assertEqual(alert.current_stock, 5)
        self.assertEqual(alert.reorder_point, 20)
        self.assertEqual(alert.suggested_quantity, 100)
        self.assertEqual(alert.priority, 'high')
        self.assertFalse(alert.is_processed)
        self.assertIsNotNone(alert.created_at)
    
    def test_reorder_alert_str_representation(self):
        """Test reorder alert string representation"""
        alert = ReorderAlert.objects.create(
            medicine=self.medicine,
            current_stock=5,
            reorder_point=20,
            suggested_quantity=100
        )
        expected_str = f"Reorder Alert: {self.medicine.name}"
        self.assertEqual(str(alert), expected_str)
