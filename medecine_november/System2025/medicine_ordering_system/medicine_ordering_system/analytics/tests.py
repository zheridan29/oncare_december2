"""
Comprehensive unit tests for the analytics module
"""

from django.test import TestCase, Client
from django.core.exceptions import ValidationError
from django.contrib.auth import get_user_model
from decimal import Decimal
from datetime import date, datetime, timedelta
import json
import pandas as pd
import numpy as np
from unittest.mock import patch, MagicMock

from .models import (
    DemandForecast, InventoryOptimization, SalesTrend, 
    CustomerAnalytics, SystemMetrics
)
from .services import ARIMAForecastingService, SupplyChainOptimizer
from inventory.models import Category, Manufacturer, Medicine
from accounts.models import User
from orders.models import Order, OrderItem

User = get_user_model()


class DemandForecastModelTests(TestCase):
    """Test cases for DemandForecast model"""
    
    def setUp(self):
        """Set up test data"""
        self.category = Category.objects.create(name='Antibiotics', is_active=True)
        self.manufacturer = Manufacturer.objects.create(name='Pfizer Inc.', country='USA', is_active=True)
        self.medicine = Medicine.objects.create(
            name='Amoxicillin',
            category=self.category,
            manufacturer=self.manufacturer,
            unit_price=Decimal('25.50'),
            cost_price=Decimal('15.00'),
            current_stock=100
        )
        self.forecast_data = {
            'medicine': self.medicine,
            'forecast_period': 'weekly',
            'forecast_horizon': 4,
            'arima_p': 1,
            'arima_d': 1,
            'arima_q': 1,
            'aic': 150.5,
            'bic': 160.2,
            'rmse': 5.2,
            'mae': 4.1,
            'mape': 12.5,
            'forecasted_demand': [10, 12, 8, 15],
            'confidence_intervals': {
                'lower': [5, 7, 3, 10],
                'upper': [15, 17, 13, 20]
            },
            'training_data_start': date(2024, 1, 1),
            'training_data_end': date(2024, 12, 31),
            'training_data_points': 52
        }
    
    def test_demand_forecast_creation(self):
        """Test demand forecast creation"""
        forecast = DemandForecast.objects.create(**self.forecast_data)
        self.assertEqual(forecast.medicine, self.medicine)
        self.assertEqual(forecast.forecast_period, 'weekly')
        self.assertEqual(forecast.forecast_horizon, 4)
        self.assertEqual(forecast.arima_p, 1)
        self.assertEqual(forecast.arima_d, 1)
        self.assertEqual(forecast.arima_q, 1)
        self.assertEqual(forecast.aic, 150.5)
        self.assertEqual(forecast.bic, 160.2)
        self.assertEqual(forecast.rmse, 5.2)
        self.assertEqual(forecast.mae, 4.1)
        self.assertEqual(forecast.mape, 12.5)
        self.assertEqual(forecast.forecasted_demand, [10, 12, 8, 15])
        self.assertTrue(forecast.is_active)
        self.assertIsNotNone(forecast.created_at)
    
    def test_demand_forecast_str_representation(self):
        """Test demand forecast string representation"""
        forecast = DemandForecast.objects.create(**self.forecast_data)
        expected_str = f"Demand Forecast for {self.medicine.name} - {forecast.forecast_period}"
        self.assertEqual(str(forecast), expected_str)
    
    def test_demand_forecast_model_quality_property(self):
        """Test demand forecast model quality property"""
        # Test good quality
        forecast = DemandForecast.objects.create(**self.forecast_data)
        self.assertEqual(forecast.model_quality, "Good")  # MAPE = 12.5
        
        # Test excellent quality
        forecast.mape = 5.0
        forecast.save()
        self.assertEqual(forecast.model_quality, "Excellent")
        
        # Test fair quality
        forecast.mape = 25.0
        forecast.save()
        self.assertEqual(forecast.model_quality, "Fair")
        
        # Test poor quality
        forecast.mape = 35.0
        forecast.save()
        self.assertEqual(forecast.model_quality, "Poor")


class InventoryOptimizationModelTests(TestCase):
    """Test cases for InventoryOptimization model"""
    
    def setUp(self):
        """Set up test data"""
        self.category = Category.objects.create(name='Antibiotics', is_active=True)
        self.manufacturer = Manufacturer.objects.create(name='Pfizer Inc.', country='USA', is_active=True)
        self.medicine = Medicine.objects.create(
            name='Amoxicillin',
            category=self.category,
            manufacturer=self.manufacturer,
            unit_price=Decimal('25.50'),
            cost_price=Decimal('15.00'),
            current_stock=100
        )
        self.forecast = DemandForecast.objects.create(
            medicine=self.medicine,
            forecast_period='weekly',
            forecast_horizon=4,
            arima_p=1,
            arima_d=1,
            arima_q=1,
            aic=150.5,
            bic=160.2,
            rmse=5.2,
            mae=4.1,
            mape=12.5,
            forecasted_demand=[10, 12, 8, 15],
            confidence_intervals={'lower': [5, 7, 3, 10], 'upper': [15, 17, 13, 20]},
            training_data_start=date(2024, 1, 1),
            training_data_end=date(2024, 12, 31),
            training_data_points=52
        )
        self.optimization_data = {
            'medicine': self.medicine,
            'demand_forecast': self.forecast,
            'service_level': Decimal('95.00'),
            'lead_time_days': 7,
            'holding_cost_percentage': Decimal('20.00'),
            'optimal_reorder_point': 25,
            'optimal_order_quantity': 50,
            'optimal_maximum_stock': 75,
            'safety_stock': 15,
            'expected_holding_cost': Decimal('250.00'),
            'expected_stockout_cost': Decimal('100.00'),
            'total_expected_cost': Decimal('350.00')
        }
    
    def test_inventory_optimization_creation(self):
        """Test inventory optimization creation"""
        optimization = InventoryOptimization.objects.create(**self.optimization_data)
        self.assertEqual(optimization.medicine, self.medicine)
        self.assertEqual(optimization.demand_forecast, self.forecast)
        self.assertEqual(optimization.service_level, Decimal('95.00'))
        self.assertEqual(optimization.lead_time_days, 7)
        self.assertEqual(optimization.optimal_reorder_point, 25)
        self.assertEqual(optimization.optimal_order_quantity, 50)
        self.assertEqual(optimization.optimal_maximum_stock, 75)
        self.assertEqual(optimization.safety_stock, 15)
        self.assertTrue(optimization.is_active)
        self.assertIsNotNone(optimization.calculated_at)
    
    def test_inventory_optimization_str_representation(self):
        """Test inventory optimization string representation"""
        optimization = InventoryOptimization.objects.create(**self.optimization_data)
        expected_str = f"Inventory Optimization for {self.medicine.name}"
        self.assertEqual(str(optimization), expected_str)


class SalesTrendModelTests(TestCase):
    """Test cases for SalesTrend model"""
    
    def setUp(self):
        """Set up test data"""
        self.category = Category.objects.create(name='Antibiotics', is_active=True)
        self.manufacturer = Manufacturer.objects.create(name='Pfizer Inc.', country='USA', is_active=True)
        self.medicine = Medicine.objects.create(
            name='Amoxicillin',
            category=self.category,
            manufacturer=self.manufacturer,
            unit_price=Decimal('25.50'),
            cost_price=Decimal('15.00'),
            current_stock=100
        )
        self.trend_data = {
            'medicine': self.medicine,
            'period_type': 'weekly',
            'period_date': date(2024, 1, 1),
            'quantity_sold': 10,
            'revenue': Decimal('255.00'),
            'average_price': Decimal('25.50'),
            'growth_rate': 5.5,
            'seasonal_factor': 1.2,
            'trend_direction': 'up'
        }
    
    def test_sales_trend_creation(self):
        """Test sales trend creation"""
        trend = SalesTrend.objects.create(**self.trend_data)
        self.assertEqual(trend.medicine, self.medicine)
        self.assertEqual(trend.period_type, 'weekly')
        self.assertEqual(trend.period_date, date(2024, 1, 1))
        self.assertEqual(trend.quantity_sold, 10)
        self.assertEqual(trend.revenue, Decimal('255.00'))
        self.assertEqual(trend.average_price, Decimal('25.50'))
        self.assertEqual(trend.growth_rate, 5.5)
        self.assertEqual(trend.seasonal_factor, 1.2)
        self.assertEqual(trend.trend_direction, 'up')
        self.assertIsNotNone(trend.created_at)
    
    def test_sales_trend_str_representation(self):
        """Test sales trend string representation"""
        trend = SalesTrend.objects.create(**self.trend_data)
        expected_str = f"Sales Trend - {self.medicine.name} - {trend.period_date}"
        self.assertEqual(str(trend), expected_str)


class ARIMAForecastingServiceTests(TestCase):
    """Test cases for ARIMAForecastingService"""
    
    def setUp(self):
        """Set up test data"""
        self.service = ARIMAForecastingService()
        self.category = Category.objects.create(name='Antibiotics', is_active=True)
        self.manufacturer = Manufacturer.objects.create(name='Pfizer Inc.', country='USA', is_active=True)
        self.medicine = Medicine.objects.create(
            name='Amoxicillin',
            category=self.category,
            manufacturer=self.manufacturer,
            unit_price=Decimal('25.50'),
            cost_price=Decimal('15.00'),
            current_stock=100
        )
    
    def test_service_initialization(self):
        """Test service initialization"""
        self.assertIsInstance(self.service, ARIMAForecastingService)
        self.assertIn('daily', self.service.min_data_points)
        self.assertIn('weekly', self.service.min_data_points)
        self.assertIn('monthly', self.service.min_data_points)
    
    def test_calculate_model_metrics(self):
        """Test model metrics calculation"""
        actual = np.array([10, 12, 8, 15])
        predicted = np.array([11, 13, 9, 14])
        
        metrics = self.service.calculate_model_metrics(actual, predicted)
        self.assertIn('rmse', metrics)
        self.assertIn('mae', metrics)
        self.assertIn('mape', metrics)
        self.assertIsInstance(metrics['rmse'], float)
        self.assertIsInstance(metrics['mae'], float)
        self.assertIsInstance(metrics['mape'], float)
