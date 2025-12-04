"""
Comprehensive unit tests for the accounts module
"""

from django.test import TestCase, Client
from django.contrib.auth import get_user_model
from django.urls import reverse
from django.core.exceptions import ValidationError
from decimal import Decimal
from datetime import date, datetime
import json

from .models import User, SalesRepProfile, PharmacistAdminProfile, UserSession

User = get_user_model()


class UserModelTests(TestCase):
    """Test cases for User model"""
    
    def setUp(self):
        """Set up test data"""
        self.user_data = {
            'username': 'testuser',
            'email': 'test@example.com',
            'password': 'testpass123',
            'first_name': 'Test',
            'last_name': 'User',
            'role': 'sales_rep',
            'phone_number': '+1234567890',
            'date_of_birth': date(1990, 1, 1),
            'address': '123 Test St',
            'city': 'Test City',
            'state': 'Test State',
            'zip_code': '12345',
            'country': 'USA'
        }
    
    def test_user_creation(self):
        """Test user creation with valid data"""
        user = User.objects.create_user(**self.user_data)
        self.assertEqual(user.username, 'testuser')
        self.assertEqual(user.email, 'test@example.com')
        self.assertEqual(user.role, 'sales_rep')
        self.assertEqual(user.phone_number, '+1234567890')
        self.assertTrue(user.check_password('testpass123'))
    
    def test_user_str_representation(self):
        """Test user string representation"""
        user = User.objects.create_user(**self.user_data)
        expected_str = f"{user.username} ({user.get_role_display()})"
        self.assertEqual(str(user), expected_str)
    
    def test_user_role_properties(self):
        """Test user role property methods"""
        # Test sales rep
        user = User.objects.create_user(**self.user_data)
        self.assertTrue(user.is_sales_rep)
        self.assertFalse(user.is_pharmacist_admin)
        self.assertFalse(user.is_admin)
        self.assertFalse(user.can_manage_inventory)
        self.assertFalse(user.can_view_analytics)
        self.assertTrue(user.can_manage_orders)
        
        # Test pharmacist admin
        user.role = 'pharmacist_admin'
        user.save()
        self.assertFalse(user.is_sales_rep)
        self.assertTrue(user.is_pharmacist_admin)
        self.assertFalse(user.is_admin)
        self.assertTrue(user.can_manage_inventory)
        self.assertTrue(user.can_view_analytics)
        self.assertTrue(user.can_manage_orders)
        
        # Test admin
        user.role = 'admin'
        user.save()
        self.assertFalse(user.is_sales_rep)
        self.assertFalse(user.is_pharmacist_admin)
        self.assertTrue(user.is_admin)
        self.assertTrue(user.can_manage_inventory)
        self.assertTrue(user.can_view_analytics)
        self.assertTrue(user.can_manage_orders)
    
    def test_user_phone_validation(self):
        """Test phone number validation"""
        # Valid phone numbers
        valid_phones = ['+1234567890', '1234567890', '+44123456789']
        for i, phone in enumerate(valid_phones):
            user_data = self.user_data.copy()
            user_data['phone_number'] = phone
            user_data['username'] = f'testuser{i}'  # Make username unique
            user_data['email'] = f'test{i}@example.com'  # Make email unique
            user = User.objects.create_user(**user_data)
            self.assertEqual(user.phone_number, phone)
    
    def test_user_required_fields(self):
        """Test that required fields are enforced"""
        required_fields = ['username', 'email', 'password']
        for field in required_fields:
            user_data = self.user_data.copy()
            del user_data[field]
            with self.assertRaises((ValueError, TypeError)):
                User.objects.create_user(**user_data)


class SalesRepProfileModelTests(TestCase):
    """Test cases for SalesRepProfile model"""
    
    def setUp(self):
        """Set up test data"""
        self.user = User.objects.create_user(
            username='salesrep',
            email='sales@example.com',
            password='testpass123',
            role='sales_rep'
        )
    
    def test_sales_rep_profile_creation(self):
        """Test sales rep profile creation"""
        profile = SalesRepProfile.objects.create(
            user=self.user,
            employee_id='EMP001',
            territory='North Region',
            commission_rate=Decimal('5.50'),
            is_active=True
        )
        self.assertEqual(profile.user, self.user)
        self.assertEqual(profile.employee_id, 'EMP001')
        self.assertEqual(profile.territory, 'North Region')
        self.assertEqual(profile.commission_rate, Decimal('5.50'))
        self.assertTrue(profile.is_active)
    
    def test_sales_rep_profile_str_representation(self):
        """Test sales rep profile string representation"""
        profile = SalesRepProfile.objects.create(
            user=self.user,
            employee_id='EMP001'
        )
        expected_str = f"Sales Rep Profile for {self.user.username}"
        self.assertEqual(str(profile), expected_str)


class PharmacistAdminProfileModelTests(TestCase):
    """Test cases for PharmacistAdminProfile model"""
    
    def setUp(self):
        """Set up test data"""
        self.user = User.objects.create_user(
            username='pharmacist',
            email='pharmacist@example.com',
            password='testpass123',
            role='pharmacist_admin'
        )
    
    def test_pharmacist_admin_profile_creation(self):
        """Test pharmacist admin profile creation"""
        profile = PharmacistAdminProfile.objects.create(
            user=self.user,
            license_number='PH123456',
            license_expiry=date(2025, 12, 31),
            specialization='Clinical Pharmacy',
            years_of_experience=5,
            department='Pharmacy Department',
            is_available=True
        )
        self.assertEqual(profile.user, self.user)
        self.assertEqual(profile.license_number, 'PH123456')
        self.assertEqual(profile.license_expiry, date(2025, 12, 31))
        self.assertEqual(profile.specialization, 'Clinical Pharmacy')
        self.assertEqual(profile.years_of_experience, 5)
        self.assertEqual(profile.department, 'Pharmacy Department')
        self.assertTrue(profile.is_available)
    
    def test_pharmacist_admin_profile_str_representation(self):
        """Test pharmacist admin profile string representation"""
        profile = PharmacistAdminProfile.objects.create(
            user=self.user,
            license_number='PH123456',
            license_expiry=date(2025, 12, 31)
        )
        expected_str = f"Pharmacist/Admin Profile for {self.user.username}"
        self.assertEqual(str(profile), expected_str)


class UserSessionModelTests(TestCase):
    """Test cases for UserSession model"""
    
    def setUp(self):
        """Set up test data"""
        self.user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpass123'
        )
    
    def test_user_session_creation(self):
        """Test user session creation"""
        session = UserSession.objects.create(
            user=self.user,
            session_key='test_session_key_123',
            ip_address='192.168.1.1',
            user_agent='Mozilla/5.0 (Test Browser)',
            is_active=True
        )
        self.assertEqual(session.user, self.user)
        self.assertEqual(session.session_key, 'test_session_key_123')
        self.assertEqual(session.ip_address, '192.168.1.1')
        self.assertTrue(session.is_active)
    
    def test_user_session_str_representation(self):
        """Test user session string representation"""
        session = UserSession.objects.create(
            user=self.user,
            session_key='test_session_key_123',
            ip_address='192.168.1.1',
            user_agent='Mozilla/5.0 (Test Browser)'
        )
        expected_str = f"Session for {self.user.username} at {session.login_time}"
        self.assertEqual(str(session), expected_str)
