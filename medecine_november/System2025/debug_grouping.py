#!/usr/bin/env python
"""
Debug data grouping issue
"""
import os
import sys
import django

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'medicine_ordering_system.settings')
django.setup()

from orders.models import OrderItem
import pandas as pd

def debug_grouping():
    print("=== Debug Data Grouping ===")
    
    # Check all order items for medicine 3
    all_items = OrderItem.objects.filter(medicine_id=3)
    print(f"Total order items: {all_items.count()}")
    
    # Check by status
    for status in ['pending', 'confirmed', 'processing', 'shipped', 'delivered', 'cancelled']:
        count = all_items.filter(order__status=status).count()
        print(f"  {status}: {count}")
    
    # Check filtered items (as used in prepare_sales_data)
    filtered_items = OrderItem.objects.filter(
        medicine_id=3,
        order__status__in=['confirmed', 'processing', 'shipped', 'delivered']
    ).values('order__created_at', 'quantity').order_by('order__created_at')
    
    print(f"\nFiltered items count: {filtered_items.count()}")
    
    if filtered_items.exists():
        df = pd.DataFrame(list(filtered_items))
        df['order__created_at'] = pd.to_datetime(df['order__created_at'])
        
        print(f"DataFrame shape: {df.shape}")
        print(f"Date range: {df['order__created_at'].min()} to {df['order__created_at'].max()}")
        print(f"Quantity range: {df['quantity'].min()} to {df['quantity'].max()}")
        
        # Test daily grouping
        daily_data = df.groupby(df['order__created_at'].dt.to_period('D'))['quantity'].sum()
        daily_data.index = daily_data.index.to_timestamp()
        daily_data = daily_data.reset_index()
        daily_data.columns = ['date', 'quantity']
        
        print(f"\nDaily grouped data:")
        print(f"  Shape: {daily_data.shape}")
        print(f"  Non-zero values: {(daily_data['quantity'] > 0).sum()}/{len(daily_data)}")
        print(f"  Sample:")
        print(daily_data.head(10))
        
        # Test weekly grouping
        weekly_data = df.groupby(df['order__created_at'].dt.to_period('W'))['quantity'].sum()
        weekly_data.index = weekly_data.index.to_timestamp()
        weekly_data = weekly_data.reset_index()
        weekly_data.columns = ['date', 'quantity']
        
        print(f"\nWeekly grouped data:")
        print(f"  Shape: {weekly_data.shape}")
        print(f"  Non-zero values: {(weekly_data['quantity'] > 0).sum()}/{len(weekly_data)}")
        print(f"  Sample:")
        print(weekly_data.head(10))
        
        # Check if reindexing is causing the issue
        print(f"\nTesting reindexing:")
        date_range = pd.date_range(start=weekly_data['date'].min(), end=weekly_data['date'].max(), freq='W')
        reindexed = weekly_data.set_index('date').reindex(date_range, fill_value=0).reset_index()
        reindexed.columns = ['date', 'quantity']
        
        print(f"  After reindexing:")
        print(f"  Shape: {reindexed.shape}")
        print(f"  Non-zero values: {(reindexed['quantity'] > 0).sum()}/{len(reindexed)}")
        print(f"  Sample:")
        print(reindexed.head(10))

if __name__ == "__main__":
    debug_grouping()

