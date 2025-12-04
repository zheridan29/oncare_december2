#!/usr/bin/env python
"""
Check data quality for forecasting
"""
import os
import sys
import django

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'medicine_ordering_system.settings')
django.setup()

from analytics.services import ARIMAForecastingService
from orders.models import OrderItem
from inventory.models import Medicine

def check_data_quality():
    print("=== Data Quality Analysis ===")
    
    # Check medicine 3 data
    medicine = Medicine.objects.get(id=3)
    print(f"Medicine: {medicine.name}")
    
    # Check raw order items
    order_items = OrderItem.objects.filter(medicine_id=3)
    print(f"Total order items: {order_items.count()}")
    
    if order_items.exists():
        total_quantity = sum(item.quantity for item in order_items)
        print(f"Total quantity sold: {total_quantity}")
        
        # Check by status
        for status in ['confirmed', 'processing', 'shipped', 'delivered']:
            count = order_items.filter(order__status=status).count()
            print(f"  {status}: {count} items")
    
    # Check prepared data
    service = ARIMAForecastingService()
    
    for period_type in ['daily', 'weekly', 'monthly']:
        try:
            data = service.prepare_sales_data(medicine_id=3, period_type=period_type)
            print(f"\n{period_type.upper()} Data:")
            print(f"  Shape: {data.shape}")
            print(f"  Min quantity: {data['quantity'].min()}")
            print(f"  Max quantity: {data['quantity'].max()}")
            print(f"  Mean quantity: {data['quantity'].mean():.2f}")
            print(f"  Std quantity: {data['quantity'].std():.2f}")
            print(f"  Non-zero values: {(data['quantity'] > 0).sum()}/{len(data)}")
            print(f"  Zero values: {(data['quantity'] == 0).sum()}/{len(data)}")
            
            # Show sample data
            non_zero = data[data['quantity'] > 0]
            if len(non_zero) > 0:
                print(f"  Sample non-zero data:")
                print(non_zero.head(5))
            else:
                print(f"  All values are zero!")
                
        except Exception as e:
            print(f"  Error with {period_type}: {e}")

if __name__ == "__main__":
    check_data_quality()

