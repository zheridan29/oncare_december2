#!/usr/bin/env python3
"""
Test data retrieval to find the real problem
"""

import os
import sys
import django

# Setup Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'medicine_ordering_system.settings')
django.setup()

from orders.models import OrderItem, Order

def test_data_retrieval():
    print("=== Testing Data Retrieval ===")
    
    # Test 1: Check total order items for medicine 3
    total_items = OrderItem.objects.filter(medicine_id=3).count()
    print(f"Total order items for medicine 3: {total_items}")
    
    # Test 2: Check order statuses
    order_statuses = Order.objects.values_list('status', flat=True).distinct()
    print(f"Order statuses in database: {list(order_statuses)}")
    
    # Test 3: Check orders with different status filters
    delivered_orders = OrderItem.objects.filter(
        medicine_id=3,
        order__status='delivered'
    ).count()
    print(f"Order items with 'delivered' status: {delivered_orders}")
    
    confirmed_orders = OrderItem.objects.filter(
        medicine_id=3,
        order__status='confirmed'
    ).count()
    print(f"Order items with 'confirmed' status: {confirmed_orders}")
    
    # Test 4: Check the exact filter used by forecasting service
    forecasting_filter = OrderItem.objects.filter(
        medicine_id=3,
        order__status__in=['confirmed', 'processing', 'shipped', 'delivered']
    ).count()
    print(f"Order items matching forecasting filter: {forecasting_filter}")
    
    # Test 5: Check if there are any orders with created_at dates
    sample_orders = OrderItem.objects.filter(medicine_id=3).select_related('order')[:5]
    print(f"\nSample order dates:")
    for item in sample_orders:
        print(f"  Order {item.order.order_number}: {item.order.created_at} (status: {item.order.status})")
    
    # Test 6: Check date range
    if OrderItem.objects.filter(medicine_id=3).exists():
        first_order = OrderItem.objects.filter(medicine_id=3).select_related('order').order_by('order__created_at').first()
        last_order = OrderItem.objects.filter(medicine_id=3).select_related('order').order_by('order__created_at').last()
        print(f"\nDate range:")
        print(f"  First order: {first_order.order.created_at}")
        print(f"  Last order: {last_order.order.created_at}")

if __name__ == "__main__":
    test_data_retrieval()
