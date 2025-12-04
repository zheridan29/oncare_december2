#!/usr/bin/env python3
"""
Verify the forecasting fix by writing results to a file
"""

import os
import sys
import django

# Setup Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'medicine_ordering_system.settings')
django.setup()

def verify_fix():
    try:
        from analytics.services import ARIMAForecastingService
        service = ARIMAForecastingService()
        
        # Test weekly data
        weekly_data = service.prepare_sales_data(3, 'weekly')
        non_zero_weekly = (weekly_data['quantity'] > 0).sum()
        
        # Test monthly data
        monthly_data = service.prepare_sales_data(3, 'monthly')
        non_zero_monthly = (monthly_data['quantity'] > 0).sum()
        
        # Write results to file
        with open('forecasting_fix_results.txt', 'w') as f:
            f.write("=== Forecasting Fix Verification ===\n")
            f.write(f"Weekly Data:\n")
            f.write(f"  Total periods: {len(weekly_data)}\n")
            f.write(f"  Non-zero periods: {non_zero_weekly} ({non_zero_weekly/len(weekly_data)*100:.1f}%)\n")
            f.write(f"  Min quantity: {weekly_data['quantity'].min()}\n")
            f.write(f"  Max quantity: {weekly_data['quantity'].max()}\n")
            f.write(f"  Mean quantity: {weekly_data['quantity'].mean():.2f}\n\n")
            
            f.write(f"Monthly Data:\n")
            f.write(f"  Total periods: {len(monthly_data)}\n")
            f.write(f"  Non-zero periods: {non_zero_monthly} ({non_zero_monthly/len(monthly_data)*100:.1f}%)\n")
            f.write(f"  Min quantity: {monthly_data['quantity'].min()}\n")
            f.write(f"  Max quantity: {monthly_data['quantity'].max()}\n")
            f.write(f"  Mean quantity: {monthly_data['quantity'].mean():.2f}\n\n")
            
            if non_zero_weekly > 0 and non_zero_monthly > 0:
                f.write("✅ SUCCESS: Weekly and monthly data now have non-zero values!\n")
            else:
                f.write("❌ FAILED: Weekly and monthly data still showing zeros\n")
        
        print("Verification complete. Check forecasting_fix_results.txt")
        
    except Exception as e:
        with open('forecasting_fix_error.txt', 'w') as f:
            f.write(f"Error: {e}\n")
            import traceback
            f.write(traceback.format_exc())
        print(f"Error occurred. Check forecasting_fix_error.txt: {e}")

if __name__ == "__main__":
    verify_fix()
