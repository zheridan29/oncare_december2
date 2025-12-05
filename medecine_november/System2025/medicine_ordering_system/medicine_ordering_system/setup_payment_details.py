"""
Quick setup script for configuring payment details in SystemConfiguration
Run this to set up default payment details for manual payments
"""
import os
import sys
import django

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'medicine_ordering_system.settings')
django.setup()

from common.models import SystemConfiguration
from accounts.models import User

def setup_payment_details():
    """Setup default payment configuration"""
    
    print("="*60)
    print("  Payment Details Setup")
    print("="*60)
    print()
    
    # Payment configuration entries
    payment_configs = [
        {
            'key': 'payment_bank_name',
            'value': 'OnCare Bank',
            'config_type': 'payments',
            'data_type': 'string',
            'description': 'Bank name for manual payments'
        },
        {
            'key': 'payment_account_name',
            'value': 'OnCare Medicine Ordering System',
            'config_type': 'payments',
            'data_type': 'string',
            'description': 'Account holder name for manual payments'
        },
        {
            'key': 'payment_account_number',
            'value': '1234567890',  # Default - admin should update this
            'config_type': 'payments',
            'data_type': 'string',
            'description': 'Bank account number for manual payments'
        },
        {
            'key': 'payment_swift_code',
            'value': '',
            'config_type': 'payments',
            'data_type': 'string',
            'description': 'SWIFT/BIC code (optional)'
        },
        {
            'key': 'payment_instructions',
            'value': 'Please include your order number in the payment reference.',
            'config_type': 'payments',
            'data_type': 'string',
            'description': 'Instructions for manual payments'
        }
    ]
    
    # Get admin user for updated_by
    admin = User.objects.filter(is_superuser=True).first()
    
    created_count = 0
    updated_count = 0
    
    for config_data in payment_configs:
        key = config_data['key']
        existing = SystemConfiguration.objects.filter(key=key).first()
        
        if existing:
            print(f"⚠️  Configuration '{key}' already exists. Skipping...")
            print(f"   Current value: {existing.value}")
            print(f"   To update, go to Django Admin → Common → System Configurations")
            print()
        else:
            config = SystemConfiguration.objects.create(
                key=key,
                value=config_data['value'],
                config_type=config_data['config_type'],
                data_type=config_data['data_type'],
                description=config_data['description'],
                updated_by=admin
            )
            print(f"✅ Created configuration: {key}")
            print(f"   Value: {config.value}")
            created_count += 1
    
    print()
    print("="*60)
    print(f"  Setup Complete!")
    print("="*60)
    print(f"Created: {created_count} configurations")
    print(f"Already existed: {len(payment_configs) - created_count}")
    print()
    print("⚠️  IMPORTANT:")
    print("   1. Go to Django Admin → Common → System Configurations")
    print("   2. Update 'payment_account_number' with your actual bank account number")
    print("   3. Update 'payment_bank_name' if needed")
    print("   4. Add 'payment_swift_code' if you have one")
    print()
    print("✅ Payment details are now configured!")

if __name__ == '__main__':
    setup_payment_details()

