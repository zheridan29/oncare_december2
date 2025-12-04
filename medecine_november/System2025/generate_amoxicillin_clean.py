#!/usr/bin/env python3
"""
Clean Amoxicillin Historical Data Generator (2020–2024)
Sales Representatives create orders with optional customer details.
This reflects the B2B medicine ordering system where sales reps manage orders.
"""

import os
import sys
import django
import random
import sqlite3
from datetime import datetime, timedelta, date
from decimal import Decimal

# Setup Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'medicine_ordering_system.settings')
django.setup()

from django.contrib.auth import get_user_model
from django.db import connection
from inventory.models import Medicine, StockMovement
from orders.models import Order, OrderItem, OrderStatusHistory

User = get_user_model()

def get_database_path():
    """Get the SQLite database path"""
    from django.conf import settings
    return settings.DATABASES['default']['NAME']

def get_available_sales_reps():
    """Get available sales representatives"""
    db_path = get_database_path()
    conn = None
    try:
        conn = sqlite3.connect(db_path, timeout=30.0)
        cursor = conn.cursor()
        
        cursor.execute("""
            SELECT id FROM accounts_user 
            WHERE role IN ('sales_rep', 'pharmacist_admin', 'admin') 
            ORDER BY RANDOM()
            LIMIT 3
        """)
        sales_reps = [row[0] for row in cursor.fetchall()]
        if not sales_reps:
            raise Exception("No sales representatives found")
        
        return sales_reps[0], sales_reps
        
    except Exception as e:
        print(f"Error getting sales reps: {e}")
        return None, []
    finally:
        if conn:
            conn.close()

def get_next_stock_movement_id():
    """Get next available stock movement ID"""
    db_path = get_database_path()
    conn = None
    try:
        conn = sqlite3.connect(db_path, timeout=30.0)
        cursor = conn.cursor()
        cursor.execute("SELECT MAX(id) FROM inventory_stockmovement")
        max_id = cursor.fetchone()[0] or 0
        return max_id + 1
    except Exception as e:
        print(f"Error getting stock movement ID: {e}")
        return random.randint(10000, 99999)
    finally:
        if conn:
            conn.close()

def generate_amoxicillin_history():
    print("=== Amoxicillin Historical Data Generator ===")
    print("Creating data from 2020-2024 for ARIMA forecasting")
    
    # 1. Get medicine
    try:
        amoxicillin = Medicine.objects.get(id=3)  # Amoxicillin 250mg
        print(f"✅ Found medicine: {amoxicillin.name}")
    except Medicine.DoesNotExist:
        print("❌ Amoxicillin not found in inventory. Please run generate_medicines.py first.")
        return

    # 2. Get sales representatives
    primary_sales_rep, sales_reps = get_available_sales_reps()
    if not primary_sales_rep or not sales_reps:
        print("❌ No sales representatives available for order creation")
        return

    # 3. Clear existing data for medicine 3
    print("\n🧹 Clearing existing data...")
    try:
        with connection.cursor() as cursor:
            cursor.execute("DELETE FROM orders_orderitem WHERE medicine_id = 3")
            sales_reps_str = ','.join(map(str, sales_reps))
            cursor.execute(f"DELETE FROM orders_orderstatushistory WHERE order_id IN (SELECT id FROM orders_order WHERE sales_rep_id IN ({sales_reps_str}))")
            cursor.execute(f"DELETE FROM orders_order WHERE sales_rep_id IN ({sales_reps_str})")
            cursor.execute("DELETE FROM inventory_stockmovement WHERE medicine_id = 3")
            print("✅ Cleared existing data")
    except Exception as e:
        print(f"⚠️  Error clearing data: {e}")

    # 4. Define historical date range (2020–2024)
    start_date = date(2020, 1, 1)
    end_date = date(2024, 12, 31)
    
    # 5. Generate orders with realistic patterns
    current_date = start_date
    orders_created = 0
    current_stock = 5000  # Initial stock
    stock_movement_id = get_next_stock_movement_id()
    order_counter = 0
    random.seed(42)  # for reproducibility

    print(f"\n📅 Generating orders from {start_date} to {end_date}")
    
    db_path = get_database_path()
    conn = None
    
    try:
        conn = sqlite3.connect(db_path, timeout=30.0)
        cursor = conn.cursor()
        
        print(f"📊 Starting data generation...")
        print(f"   Database: {db_path}")
        print(f"   Primary sales rep ID: {primary_sales_rep}")
        print(f"   Sales reps available: {len(sales_reps)}")
        
        while current_date <= end_date:
            # Calculate daily sales (realistic pattern)
            base_sales = 15  # Base daily sales
            
            # Seasonal multiplier (higher in winter)
            month = current_date.month
            if month in [12, 1, 2]:
                seasonal_mult = 1.3
            elif month in [6, 7, 8]:
                seasonal_mult = 0.8
            else:
                seasonal_mult = 1.0
            
            # Weekday multiplier (more sales on weekdays)
            weekday = current_date.weekday()
            weekday_mult = 0.7 if weekday == 6 else 1.0  # Lower on Sunday
            
            # Growth trend (8% annual growth)
            years_elapsed = (current_date - start_date).days / 365.25
            growth_factor = (1 + 0.08) ** years_elapsed
            
            daily_sales = int(base_sales * seasonal_mult * weekday_mult * growth_factor * random.uniform(0.8, 1.2))
            daily_sales = max(1, daily_sales)
            
            # Check if we need to reorder
            if current_stock < daily_sales and current_stock <= 200:
                reorder_qty = 1000
                current_stock += reorder_qty
                
                # Create stock movement for reorder
                cursor.execute("""
                    INSERT INTO inventory_stockmovement 
                    (id, medicine_id, movement_type, quantity, reference_number, notes, created_by_id, created_at)
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?)
                """, (
                    stock_movement_id,
                    3,
                    'in',
                    reorder_qty,
                    f"REORDER-{current_date.strftime('%Y%m%d')}",
                    f"Automatic reorder - stock below reorder point",
                    primary_sales_rep,
                    current_date.isoformat()
                ))
                stock_movement_id += 1
            
            # Create orders for the day (limit to reasonable number)
            orders_today = min(max(1, daily_sales // 3), 8)  # Max 8 orders per day
            remaining_sales = daily_sales
            
            for order_num in range(orders_today):
                if remaining_sales <= 0 or current_stock <= 0:
                    break
                
                order_qty = min(random.randint(1, 5), remaining_sales, current_stock)
                if order_qty <= 0:
                    break
                
                # Safety check to prevent infinite loops
                if orders_created > 10000:  # Max 10k orders total
                    print(f"⚠️  Reached maximum order limit (10,000). Stopping generation.")
                    break
                
                # Create order
                order_counter += 1
                order_number = f"O{current_date.strftime('%Y%m%d')}{order_counter:04d}"
                sales_rep_id = random.choice(sales_reps)  # Random sales rep for variety
                
                # Create order record (sales rep creates order with optional customer details)
                cursor.execute("""
                    INSERT INTO orders_order 
                    (order_number, sales_rep_id, customer_name, customer_phone, customer_address, 
                     status, payment_status, subtotal, tax_amount, shipping_cost, discount_amount, 
                     total_amount, delivery_method, delivery_address, delivery_instructions, 
                     prescription_required, prescription_verified, customer_notes, internal_notes, 
                     created_at, updated_at)
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                """, (
                    order_number,
                    sales_rep_id,
                    f"Customer-{order_counter:06d}",  # Sales rep assigned customer name
                    f"555-{order_counter:04d}",      # Sales rep assigned phone
                    f"Delivery Address {order_counter}",  # Sales rep assigned address
                    'delivered',
                    'paid',
                    order_qty * 15.50,  # subtotal
                    0.00,  # tax_amount
                    0.00,  # shipping_cost
                    0.00,  # discount_amount
                    order_qty * 15.50,  # total_amount
                    'delivery',  # delivery_method
                    f"Delivery Address {order_counter}",
                    "Standard delivery",
                    False,  # prescription_required
                    True,   # prescription_verified
                    f"Customer notes for order {order_number}",  # customer_notes
                    f"Sales rep {sales_rep_id} created this order",  # internal_notes
                    current_date.isoformat(),
                    current_date.isoformat()
                ))
                
                order_id = cursor.lastrowid
                
                # Create order item
                cursor.execute("""
                    INSERT INTO orders_orderitem 
                    (order_id, medicine_id, quantity, unit_price, total_price, 
                     prescription_notes, created_at)
                    VALUES (?, ?, ?, ?, ?, ?, ?)
                """, (
                    order_id,
                    3,
                    order_qty,
                    15.50,
                    order_qty * 15.50,
                    f"Prescription for {amoxicillin.name}",
                    current_date.isoformat()
                ))
                
                # Create order status history
                cursor.execute("""
                    INSERT INTO orders_orderstatushistory 
                    (order_id, old_status, new_status, old_payment_status, new_payment_status, 
                     notes, changed_by_id, changed_at)
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?)
                """, (
                    order_id,
                    'pending',  # old_status
                    'delivered',  # new_status
                    'pending',  # old_payment_status
                    'paid',  # new_payment_status
                    'Order completed successfully',
                    sales_rep_id,
                    current_date.isoformat()
                ))
                
                # Update stock
                current_stock -= order_qty
                remaining_sales -= order_qty
                orders_created += 1
                
                # Create stock movement for sale
                cursor.execute("""
                    INSERT INTO inventory_stockmovement 
                    (id, medicine_id, movement_type, quantity, reference_number, notes, created_by_id, created_at)
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?)
                """, (
                    stock_movement_id,
                    3,
                    'out',
                    -order_qty,
                    order_number,
                    f"Sale - Order {order_number}",
                    sales_rep_id,
                    current_date.isoformat()
                ))
                stock_movement_id += 1
            
            # Break outer loop if we hit the limit
            if orders_created > 10000:
                break
            
            # Progress reporting
            if current_date.day == 1:  # Monthly progress
                print(f"  📅 {current_date.strftime('%Y-%m')}: {orders_created} orders, Stock: {current_stock}")
            
            current_date += timedelta(days=1)
        
        # Update medicine stock
        cursor.execute("""
            UPDATE inventory_medicine 
            SET current_stock = ? 
            WHERE id = ?
        """, (current_stock, 3))
        
        conn.commit()
        print(f"\n✅ Generated {orders_created} orders for {amoxicillin.name}")
        print(f"   Final stock: {current_stock}")
        print(f"   Date range: {start_date} to {end_date}")
        
        # Verify data was inserted
        cursor.execute("SELECT COUNT(*) FROM orders_orderitem WHERE medicine_id = 3")
        count = cursor.fetchone()[0]
        print(f"   Verified: {count} order items in database")
        
    except Exception as e:
        print(f"❌ Error creating orders: {e}")
        import traceback
        traceback.print_exc()
        if conn:
            conn.rollback()
    finally:
        if conn:
            conn.close()

def verify_data_quality():
    """Verify the generated data quality for forecasting"""
    print("\n=== Data Quality Verification ===")
    
    try:
        from analytics.services import ARIMAForecastingService
        service = ARIMAForecastingService()
        
        for period_type in ['daily', 'weekly', 'monthly']:
            try:
                data = service.prepare_sales_data(3, period_type)  # Medicine ID 3
                non_zero = (data['quantity'] > 0).sum()
                total = len(data)
                
                print(f"{period_type.upper()} Data:")
                print(f"  Total periods: {total}")
                print(f"  Non-zero periods: {non_zero} ({non_zero/total*100:.1f}%)")
                print(f"  Min quantity: {data['quantity'].min()}")
                print(f"  Max quantity: {data['quantity'].max()}")
                print(f"  Mean quantity: {data['quantity'].mean():.2f}")
                print(f"  Std quantity: {data['quantity'].std():.2f}")
                
                if non_zero >= service.min_data_points.get(period_type, 30):
                    print(f"  ✅ Sufficient data for {period_type} forecasting")
                else:
                    print(f"  ⚠️  Insufficient data for {period_type} forecasting")
                
            except Exception as e:
                print(f"  ❌ Error verifying {period_type} data: {e}")
    
    except Exception as e:
        print(f"❌ Error in verification: {e}")

if __name__ == "__main__":
    generate_amoxicillin_history()
    
    # Verify data quality
    verify_data_quality()
    
    print("\n🎉 Amoxicillin historical data generation completed!")
    print("   The data is now ready for ARIMA forecasting with proper density and patterns.")
