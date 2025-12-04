"""
Script to fix negative stock values in the database.

Run this script to set all negative stock values to 0.
Usage: python manage.py shell < fix_negative_stock.py
Or: python manage.py runscript fix_negative_stock (if django-extensions is installed)
"""

import os
import django

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'medicine_ordering_system.settings')
django.setup()

from inventory.models import Medicine
from django.db.models import F

def fix_negative_stock():
    """Fix all medicines with negative stock by setting them to 0"""
    
    # Find all medicines with negative stock
    negative_stock_medicines = Medicine.objects.filter(current_stock__lt=0)
    
    count = negative_stock_medicines.count()
    
    if count == 0:
        print("✅ No medicines with negative stock found!")
        return
    
    print(f"⚠️  Found {count} medicine(s) with negative stock:")
    print("-" * 80)
    
    # Display medicines with negative stock
    for medicine in negative_stock_medicines:
        print(f"  - {medicine.name} ({medicine.strength}): Current stock = {medicine.current_stock}")
    
    print("-" * 80)
    
    # Fix negative stock values
    fixed_count = 0
    for medicine in negative_stock_medicines:
        old_stock = medicine.current_stock
        medicine.current_stock = 0
        medicine.save(update_fields=['current_stock'])
        fixed_count += 1
        print(f"✅ Fixed {medicine.name}: {old_stock} → 0")
    
    print("-" * 80)
    print(f"✅ Successfully fixed {fixed_count} medicine(s) with negative stock!")

if __name__ == '__main__':
    fix_negative_stock()

