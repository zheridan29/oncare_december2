"""
Comprehensive unit tests for the common module
"""

from django.test import TestCase, Client
from django.core.exceptions import ValidationError
from django.contrib.auth import get_user_model
from decimal import Decimal
from datetime import date, datetime
import json

from .models import Notification, FileUpload, SystemConfiguration
from accounts.models import User

User = get_user_model()


class NotificationModelTests(TestCase):
    """Test cases for Notification model"""
    
    def setUp(self):
        """Set up test data"""
        self.user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpass123',
            role='sales_rep'
        )
        self.notification_data = {
            'user': self.user,
            'title': 'New Order Received',
            'message': 'You have received a new order from John Doe',
            'notification_type': 'order_update',
            'priority': 'medium',
            'is_read': False,
            'action_url': '/orders/123/'
        }
    
    def test_notification_creation(self):
        """Test notification creation"""
        notification = Notification.objects.create(**self.notification_data)
        self.assertEqual(notification.user, self.user)
        self.assertEqual(notification.title, 'New Order Received')
        self.assertEqual(notification.message, 'You have received a new order from John Doe')
        self.assertEqual(notification.notification_type, 'order_update')
        self.assertEqual(notification.priority, 'medium')
        self.assertFalse(notification.is_read)
        self.assertEqual(notification.action_url, '/orders/123/')
        self.assertIsNotNone(notification.created_at)
    
    def test_notification_str_representation(self):
        """Test notification string representation"""
        notification = Notification.objects.create(**self.notification_data)
        expected_str = f"{notification.title} - {self.user.username}"
        self.assertEqual(str(notification), expected_str)
    
    def test_notification_priority_choices(self):
        """Test notification priority choices"""
        notification = Notification.objects.create(**self.notification_data)
        
        valid_priorities = ['low', 'medium', 'high', 'urgent']
        for priority in valid_priorities:
            notification.priority = priority
            notification.save()
            self.assertEqual(notification.priority, priority)
    
    def test_notification_type_choices(self):
        """Test notification type choices"""
        notification = Notification.objects.create(**self.notification_data)
        
        valid_types = ['order_update', 'stock_alert', 'prescription_ready', 'payment_confirmation', 'system_maintenance', 'promotion', 'security_alert']
        for notification_type in valid_types:
            notification.notification_type = notification_type
            notification.save()
            self.assertEqual(notification.notification_type, notification_type)


class FileUploadModelTests(TestCase):
    """Test cases for FileUpload model"""
    
    def setUp(self):
        """Set up test data"""
        self.user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpass123',
            role='sales_rep'
        )
        self.file_upload_data = {
            'file_type': 'prescription',
            'original_filename': 'prescription.pdf',
            'file_size': 1024000,  # 1MB
            'mime_type': 'application/pdf',
            'uploaded_by': self.user
        }
    
    def test_file_upload_creation(self):
        """Test file upload creation"""
        file_upload = FileUpload.objects.create(**self.file_upload_data)
        self.assertEqual(file_upload.uploaded_by, self.user)
        self.assertEqual(file_upload.original_filename, 'prescription.pdf')
        self.assertEqual(file_upload.file_size, 1024000)
        self.assertEqual(file_upload.mime_type, 'application/pdf')
        self.assertEqual(file_upload.file_type, 'prescription')
        self.assertFalse(file_upload.is_processed)
        self.assertIsNotNone(file_upload.uploaded_at)
    
    def test_file_upload_str_representation(self):
        """Test file upload string representation"""
        file_upload = FileUpload.objects.create(**self.file_upload_data)
        expected_str = f"{file_upload.original_filename} ({file_upload.file_type})"
        self.assertEqual(str(file_upload), expected_str)
    
    def test_file_upload_upload_type_choices(self):
        """Test file upload type choices"""
        file_upload = FileUpload.objects.create(**self.file_upload_data)
        
        valid_types = ['prescription', 'insurance', 'id', 'medical_record', 'invoice', 'report', 'other']
        for upload_type in valid_types:
            file_upload.file_type = upload_type
            file_upload.save()
            self.assertEqual(file_upload.file_type, upload_type)


class SystemConfigurationModelTests(TestCase):
    """Test cases for SystemConfiguration model"""
    
    def setUp(self):
        """Set up test data"""
        self.user = User.objects.create_user(
            username='admin',
            email='admin@example.com',
            password='testpass123',
            role='admin'
        )
        self.config_data = {
            'key': 'system_name',
            'value': 'OnCare Medicine Ordering System',
            'description': 'The name of the system displayed to users',
            'config_type': 'general',
            'data_type': 'string',
            'is_required': True,
            'updated_by': self.user
        }
    
    def test_system_configuration_creation(self):
        """Test system configuration creation"""
        config = SystemConfiguration.objects.create(**self.config_data)
        self.assertEqual(config.key, 'system_name')
        self.assertEqual(config.value, 'OnCare Medicine Ordering System')
        self.assertEqual(config.description, 'The name of the system displayed to users')
        self.assertEqual(config.config_type, 'general')
        self.assertEqual(config.data_type, 'string')
        self.assertTrue(config.is_required)
        self.assertEqual(config.updated_by, self.user)
        self.assertIsNotNone(config.updated_at)
    
    def test_system_configuration_str_representation(self):
        """Test system configuration string representation"""
        config = SystemConfiguration.objects.create(**self.config_data)
        expected_str = f"{config.key} = {config.value}"
        self.assertEqual(str(config), expected_str)
    
    def test_system_configuration_data_type_choices(self):
        """Test system configuration data type choices"""
        config = SystemConfiguration.objects.create(**self.config_data)
        
        valid_types = ['string', 'integer', 'float', 'boolean', 'json', 'url', 'email']
        for data_type in valid_types:
            config.data_type = data_type
            config.save()
            self.assertEqual(config.data_type, data_type)
    
    def test_system_configuration_category_choices(self):
        """Test system configuration category choices"""
        config = SystemConfiguration.objects.create(**self.config_data)
        
        valid_categories = ['general', 'inventory', 'orders', 'payments', 'notifications', 'security', 'analytics']
        for category in valid_categories:
            config.config_type = category
            config.save()
            self.assertEqual(config.config_type, category)
