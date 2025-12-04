#!/usr/bin/env python3
"""
Test script to verify the forecasting fix
"""

import os
import sys
import django

# Setup Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'medicine_ordering_system.settings')
django.setup()

from analytics.services import ARIMAForecastingService

def test_forecasting_fix():
    print("=== Testing Forecasting Fix ===")
    
    try:
        service = ARIMAForecastingService()
        
        # Test daily data
        print("\n📊 Testing Daily Data:")
        daily_data = service.prepare_sales_data(3, 'daily')
        non_zero_daily = (daily_data['quantity'] > 0).sum()
        print(f"  Total periods: {len(daily_data)}")
        print(f"  Non-zero periods: {non_zero_daily} ({non_zero_daily/len(daily_data)*100:.1f}%)")
        print(f"  Min quantity: {daily_data['quantity'].min()}")
        print(f"  Max quantity: {daily_data['quantity'].max()}")
        print(f"  Mean quantity: {daily_data['quantity'].mean():.2f}")
        
        # Test weekly data
        print("\n📊 Testing Weekly Data:")
        weekly_data = service.prepare_sales_data(3, 'weekly')
        non_zero_weekly = (weekly_data['quantity'] > 0).sum()
        print(f"  Total periods: {len(weekly_data)}")
        print(f"  Non-zero periods: {non_zero_weekly} ({non_zero_weekly/len(weekly_data)*100:.1f}%)")
        print(f"  Min quantity: {weekly_data['quantity'].min()}")
        print(f"  Max quantity: {weekly_data['quantity'].max()}")
        print(f"  Mean quantity: {weekly_data['quantity'].mean():.2f}")
        
        # Test monthly data
        print("\n📊 Testing Monthly Data:")
        monthly_data = service.prepare_sales_data(3, 'monthly')
        non_zero_monthly = (monthly_data['quantity'] > 0).sum()
        print(f"  Total periods: {len(monthly_data)}")
        print(f"  Non-zero periods: {non_zero_monthly} ({non_zero_monthly/len(monthly_data)*100:.1f}%)")
        print(f"  Min quantity: {monthly_data['quantity'].min()}")
        print(f"  Max quantity: {monthly_data['quantity'].max()}")
        print(f"  Mean quantity: {monthly_data['quantity'].mean():.2f}")
        
        # Test forecasting
        print("\n🔮 Testing Forecasting:")
        try:
            weekly_forecast = service.generate_forecast(3, 'weekly', 4)
            print(f"✅ Weekly forecast successful:")
            print(f"   Forecast: {[round(x, 2) for x in weekly_forecast.forecasted_demand]}")
            print(f"   Data points: {weekly_forecast.training_data_points}")
        except Exception as e:
            print(f"❌ Weekly forecast failed: {e}")
        
        try:
            monthly_forecast = service.generate_forecast(3, 'monthly', 4)
            print(f"✅ Monthly forecast successful:")
            print(f"   Forecast: {[round(x, 2) for x in monthly_forecast.forecasted_demand]}")
            print(f"   Data points: {monthly_forecast.training_data_points}")
        except Exception as e:
            print(f"❌ Monthly forecast failed: {e}")
            
        print("\n🎉 Forecasting fix test completed!")
        
    except Exception as e:
        print(f"❌ Error in test: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    test_forecasting_fix()
