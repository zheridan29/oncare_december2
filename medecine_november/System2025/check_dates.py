#!/usr/bin/env python3
"""
Check the dates in the generated data
"""

import os
import sys
import django

# Setup Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'medicine_ordering_system.settings')
django.setup()

from orders.models import OrderItem
from django.db.models import Count

def check_dates():
    print("=== Checking Order Dates ===")
    
    # Get sample dates
    dates = OrderItem.objects.filter(medicine_id=3).values('order__created_at__date').annotate(count=Count('id')).order_by('order__created_at__date')[:10]
    
    print("Sample dates:")
    for d in dates:
        print(f"  {d['order__created_at__date']}: {d['count']} orders")
    
    # Get total unique dates
    total_dates = OrderItem.objects.filter(medicine_id=3).values('order__created_at__date').distinct().count()
    print(f"\nTotal unique dates: {total_dates}")
    
    # Get date range
    first_order = OrderItem.objects.filter(medicine_id=3).select_related('order').order_by('order__created_at').first()
    last_order = OrderItem.objects.filter(medicine_id=3).select_related('order').order_by('order__created_at').last()
    
    if first_order and last_order:
        print(f"Date range: {first_order.order.created_at.date()} to {last_order.order.created_at.date()}")

if __name__ == "__main__":
    check_dates()
