"""
Direct SQL script to fix negative stock values in the database.
This bypasses Django ORM to directly update the database.

Run this with: python fix_negative_stock_sql.py
"""

import os
import django

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'medicine_ordering_system.settings')
django.setup()

from django.db import connection

def fix_negative_stock_direct():
    """Fix all medicines with negative stock using direct SQL update"""
    
    with connection.cursor() as cursor:
        # Find medicines with negative stock
        cursor.execute("""
            SELECT id, name, current_stock 
            FROM inventory_medicine 
            WHERE current_stock < 0
        """)
        
        negative_medicines = cursor.fetchall()
        
        if not negative_medicines:
            print("✅ No medicines with negative stock found!")
            return
        
        print(f"⚠️  Found {len(negative_medicines)} medicine(s) with negative stock:")
        print("-" * 80)
        
        for med_id, name, stock in negative_medicines:
            print(f"  - ID {med_id}: {name} - Current stock = {stock}")
        
        print("-" * 80)
        
        # Fix all negative stock values directly using SQL
        cursor.execute("""
            UPDATE inventory_medicine 
            SET current_stock = 0 
            WHERE current_stock < 0
        """)
        
        rows_updated = cursor.rowcount
        connection.commit()
        
        print(f"✅ Successfully fixed {rows_updated} medicine(s) with negative stock!")
        print("   All negative stock values have been set to 0.")

if __name__ == '__main__':
    fix_negative_stock_direct()

