#!/usr/bin/env python
"""
Comprehensive Amoxicillin Historical Data Generator (2020-2024)
Creates realistic, dense data that works perfectly with ARIMA forecasting
"""
import os
import sys
import django
import sqlite3
import random
import numpy as np
from datetime import datetime, timedelta, date
from decimal import Decimal
import json

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'medicine_ordering_system.settings')
django.setup()

from django.db import connection
from django.utils import timezone
from accounts.models import User
from inventory.models import Medicine, Category, Manufacturer, StockMovement
from orders.models import Order, OrderItem, OrderStatusHistory
from transactions.models import Transaction, PaymentMethod

class AmoxicillinDataGenerator:
    def __init__(self):
        self.medicine_id = 3  # Amoxicillin 250mg
        self.medicine_name = "Amoxicillin 250mg"
        self.start_date = date(2020, 1, 1)
        self.end_date = date(2024, 12, 31)
        
        # Realistic parameters for Amoxicillin (antibiotic)
        self.base_daily_sales = 15  # Base daily sales
        self.seasonal_multipliers = {
            'winter': 1.3,  # Higher in winter (flu season)
            'spring': 0.9,  # Lower in spring
            'summer': 0.8,  # Lowest in summer
            'fall': 1.1    # Moderate in fall
        }
        
        # Growth trend (increasing demand over time)
        self.annual_growth_rate = 0.08  # 8% annual growth
        
        # Weekday patterns (more sales on weekdays)
        self.weekday_multipliers = {
            0: 0.7,  # Monday
            1: 0.9,  # Tuesday
            2: 1.0,  # Wednesday
            3: 1.1,  # Thursday
            4: 1.2,  # Friday
            5: 0.6,  # Saturday
            6: 0.4   # Sunday
        }
        
        # Stock management
        self.initial_stock = 5000
        self.reorder_point = 200
        self.reorder_quantity = 1000
        
    def get_database_path(self):
        """Get the SQLite database path"""
        from django.conf import settings
        return settings.DATABASES['default']['NAME']
    
    def get_season(self, date_obj):
        """Determine season based on date"""
        month = date_obj.month
        if month in [12, 1, 2]:
            return 'winter'
        elif month in [3, 4, 5]:
            return 'spring'
        elif month in [6, 7, 8]:
            return 'summer'
        else:
            return 'fall'
    
    def calculate_daily_sales(self, current_date):
        """Calculate realistic daily sales for a given date"""
        # Base sales
        sales = self.base_daily_sales
        
        # Apply seasonal multiplier
        season = self.get_season(current_date)
        sales *= self.seasonal_multipliers[season]
        
        # Apply weekday multiplier
        weekday = current_date.weekday()
        sales *= self.weekday_multipliers[weekday]
        
        # Apply annual growth trend
        years_elapsed = (current_date - self.start_date).days / 365.25
        growth_factor = (1 + self.annual_growth_rate) ** years_elapsed
        sales *= growth_factor
        
        # Add some randomness (±20%)
        sales *= random.uniform(0.8, 1.2)
        
        # Ensure minimum sales (at least 1 per day)
        return max(1, int(round(sales)))
    
    def get_available_users(self):
        """Get available users for orders"""
        db_path = self.get_database_path()
        conn = None
        try:
            conn = sqlite3.connect(db_path, timeout=30.0)
            cursor = conn.cursor()
            
            # Get sales rep
            cursor.execute("""
                SELECT id FROM accounts_user 
                WHERE role IN ('sales_rep', 'pharmacist_admin', 'admin') 
                LIMIT 1
            """)
            sales_rep = cursor.fetchone()
            if not sales_rep:
                raise Exception("No sales rep found")
            sales_rep_id = sales_rep[0]
            
            # Get customers
            cursor.execute("""
                SELECT id FROM accounts_user 
                WHERE role = 'customer'
                ORDER BY RANDOM()
                LIMIT 50
            """)
            customers = [row[0] for row in cursor.fetchall()]
            if not customers:
                # If no customers, use any users
                cursor.execute("SELECT id FROM accounts_user ORDER BY RANDOM() LIMIT 20")
                customers = [row[0] for row in cursor.fetchall()]
            
            return sales_rep_id, customers
            
        except Exception as e:
            print(f"Error getting users: {e}")
            return None, []
        finally:
            if conn:
                conn.close()
    
    def get_next_order_number(self):
        """Generate unique order number"""
        db_path = self.get_database_path()
        conn = None
        try:
            conn = sqlite3.connect(db_path, timeout=30.0)
            cursor = conn.cursor()
            
            # Get max order number
            cursor.execute("SELECT MAX(CAST(SUBSTR(order_number, 2) AS INTEGER)) FROM orders_order WHERE order_number LIKE 'O%'")
            result = cursor.fetchone()
            max_num = result[0] if result[0] else 0
            return f"O{max_num + 1:06d}"
            
        except Exception as e:
            print(f"Error generating order number: {e}")
            return f"O{random.randint(100000, 999999)}"
        finally:
            if conn:
                conn.close()
    
    def get_next_stock_movement_id(self):
        """Get next available stock movement ID"""
        db_path = self.get_database_path()
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
    
    def create_historical_orders(self):
        """Create historical orders with realistic patterns"""
        print(f"Creating historical orders for {self.medicine_name} from {self.start_date} to {self.end_date}")
        
        sales_rep_id, customers = self.get_available_users()
        if not sales_rep_id or not customers:
            print("❌ No users available for order creation")
            return False
        
        db_path = self.get_database_path()
        conn = None
        orders_created = 0
        current_stock = self.initial_stock
        
        try:
            conn = sqlite3.connect(db_path, timeout=30.0)
            cursor = conn.cursor()
            
            current_date = self.start_date
            stock_movement_id = self.get_next_stock_movement_id()
            
            while current_date <= self.end_date:
                # Calculate daily sales
                daily_sales = self.calculate_daily_sales(current_date)
                
                # Check if we have enough stock
                if current_stock < daily_sales:
                    # Reorder if below reorder point
                    if current_stock <= self.reorder_point:
                        reorder_qty = self.reorder_quantity
                        current_stock += reorder_qty
                        
                        # Create stock movement for reorder
                        cursor.execute("""
                            INSERT INTO inventory_stockmovement 
                            (id, medicine_id, movement_type, quantity, reference_number, notes, created_by_id, created_at)
                            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
                        """, (
                            stock_movement_id,
                            self.medicine_id,
                            'in',
                            reorder_qty,
                            f"REORDER-{current_date.strftime('%Y%m%d')}",
                            f"Automatic reorder - stock below reorder point",
                            sales_rep_id,
                            current_date.isoformat()
                        ))
                        stock_movement_id += 1
                        print(f"  📦 Reordered {reorder_qty} units on {current_date}")
                
                # Create orders for the day
                orders_today = max(1, daily_sales // 3)  # 3-5 orders per day
                remaining_sales = daily_sales
                
                for order_num in range(orders_today):
                    if remaining_sales <= 0:
                        break
                    
                    # Calculate order quantity (1-5 units per order)
                    order_qty = min(random.randint(1, 5), remaining_sales, current_stock)
                    if order_qty <= 0:
                        break
                    
                    # Create order
                    order_number = self.get_next_order_number()
                    customer_id = random.choice(customers)
                    
                    # Create order record
                    cursor.execute("""
                        INSERT INTO orders_order 
                        (order_number, customer_id, sales_rep_id, status, total_amount, 
                         delivery_address, delivery_instructions, created_at, updated_at)
                        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
                    """, (
                        order_number,
                        customer_id,
                        sales_rep_id,
                        'delivered',
                        order_qty * 15.50,  # Amoxicillin price
                        f"Customer Address {customer_id}",
                        "Standard delivery",
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
                        self.medicine_id,
                        order_qty,
                        15.50,
                        order_qty * 15.50,
                        f"Prescription for {self.medicine_name}",
                        current_date.isoformat()
                    ))
                    
                    # Create order status history
                    cursor.execute("""
                        INSERT INTO orders_orderstatushistory 
                        (order_id, status, notes, created_at)
                        VALUES (?, ?, ?, ?)
                    """, (
                        order_id,
                        'delivered',
                        'Order completed successfully',
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
                        self.medicine_id,
                        'out',
                        -order_qty,
                        order_number,
                        f"Sale - Order {order_number}",
                        sales_rep_id,
                        current_date.isoformat()
                    ))
                    stock_movement_id += 1
                
                # Progress reporting
                if current_date.day == 1:  # Monthly progress
                    print(f"  📅 {current_date.strftime('%Y-%m')}: {orders_created} orders, Stock: {current_stock}")
                
                current_date += timedelta(days=1)
            
            # Update medicine stock
            cursor.execute("""
                UPDATE inventory_medicine 
                SET current_stock = ? 
                WHERE id = ?
            """, (current_stock, self.medicine_id))
            
            conn.commit()
            print(f"✅ Created {orders_created} orders for {self.medicine_name}")
            print(f"   Final stock: {current_stock}")
            print(f"   Date range: {self.start_date} to {self.end_date}")
            
            return True
            
        except Exception as e:
            print(f"❌ Error creating orders: {e}")
            if conn:
                conn.rollback()
            return False
        finally:
            if conn:
                conn.close()
    
    def verify_data_quality(self):
        """Verify the generated data quality for forecasting"""
        print("\n=== Data Quality Verification ===")
        
        try:
            from analytics.services import ARIMAForecastingService
            service = ARIMAForecastingService()
            
            for period_type in ['daily', 'weekly', 'monthly']:
                try:
                    data = service.prepare_sales_data(self.medicine_id, period_type)
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
    
    def test_forecasting(self):
        """Test forecasting with the generated data"""
        print("\n=== Testing Forecasting ===")
        
        try:
            from analytics.services import ARIMAForecastingService
            service = ARIMAForecastingService()
            
            # Test weekly forecast
            try:
                forecast = service.generate_forecast(self.medicine_id, 'weekly', 4)
                print(f"✅ Weekly forecast successful:")
                print(f"   Forecast: {[round(x, 2) for x in forecast.forecasted_demand]}")
                print(f"   Data points: {forecast.training_data_points}")
                print(f"   ARIMA params: p={forecast.arima_p}, d={forecast.arima_d}, q={forecast.arima_q}")
            except Exception as e:
                print(f"❌ Weekly forecast failed: {e}")
            
            # Test monthly forecast
            try:
                forecast = service.generate_forecast(self.medicine_id, 'monthly', 4)
                print(f"✅ Monthly forecast successful:")
                print(f"   Forecast: {[round(x, 2) for x in forecast.forecasted_demand]}")
                print(f"   Data points: {forecast.training_data_points}")
            except Exception as e:
                print(f"❌ Monthly forecast failed: {e}")
                
        except Exception as e:
            print(f"❌ Error testing forecasting: {e}")

def main():
    print("=== Amoxicillin Historical Data Generator ===")
    print("Creating comprehensive data from 2020-2024 for ARIMA forecasting")
    
    generator = AmoxicillinDataGenerator()
    
    # Clear existing data for medicine 3
    print("\n🧹 Clearing existing data...")
    try:
        with connection.cursor() as cursor:
            # Delete existing orders and related data
            cursor.execute("DELETE FROM orders_orderitem WHERE medicine_id = 3")
            cursor.execute("DELETE FROM orders_orderstatushistory WHERE order_id IN (SELECT id FROM orders_order WHERE sales_rep_id IN (SELECT id FROM accounts_user WHERE role IN ('sales_rep', 'pharmacist_admin', 'admin')))")
            cursor.execute("DELETE FROM orders_order WHERE sales_rep_id IN (SELECT id FROM accounts_user WHERE role IN ('sales_rep', 'pharmacist_admin', 'admin'))")
            cursor.execute("DELETE FROM inventory_stockmovement WHERE medicine_id = 3")
            print("✅ Cleared existing data")
    except Exception as e:
        print(f"⚠️  Error clearing data: {e}")
    
    # Generate new data
    success = generator.create_historical_orders()
    
    if success:
        # Verify data quality
        generator.verify_data_quality()
        
        # Test forecasting
        generator.test_forecasting()
        
        print("\n🎉 Amoxicillin historical data generation completed successfully!")
        print("   The data is now ready for ARIMA forecasting with proper density and patterns.")
    else:
        print("\n❌ Data generation failed. Please check the errors above.")

if __name__ == "__main__":
    main()

