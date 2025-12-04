"""
Signals for inventory management
"""
from django.db.models.signals import post_save, pre_save
from django.dispatch import receiver
from django.db.models import F
from .models import Medicine, StockMovement
from common.services import NotificationService
import logging

logger = logging.getLogger(__name__)


@receiver(pre_save, sender=Medicine)
def ensure_non_negative_stock(sender, instance, **kwargs):
    """
    Ensure stock is never negative before saving to database.
    This prevents database constraint violations.
    """
    if instance.current_stock < 0:
        logger.warning(f"Medicine {instance.name} has negative stock ({instance.current_stock}). Setting to 0.")
        instance.current_stock = 0


@receiver(post_save, sender=Medicine)
def check_stock_levels(sender, instance, created, **kwargs):
    """
    Check stock levels after medicine is saved and create notifications if low
    """
    try:
        # Only check if medicine is active and stock is low
        if instance.is_active and instance.current_stock <= instance.reorder_point:
            NotificationService.notify_low_stock(instance, instance.current_stock)
            
            # Create or update reorder alert if not exists
            from .models import ReorderAlert
            alert, created = ReorderAlert.objects.get_or_create(
                medicine=instance,
                is_processed=False,
                defaults={
                    'current_stock': instance.current_stock,
                    'reorder_point': instance.reorder_point,
                    'suggested_quantity': instance.reorder_point * 2,
                    'priority': 'urgent' if instance.current_stock == 0 else 'high' if instance.current_stock <= instance.reorder_point / 2 else 'medium'
                }
            )
            
            if not created:
                # Update existing alert
                alert.current_stock = instance.current_stock
                alert.priority = 'urgent' if instance.current_stock == 0 else 'high' if instance.current_stock <= instance.reorder_point / 2 else 'medium'
                alert.save()
    
    except Exception as e:
        logger.error(f"Error checking stock levels for {instance.name}: {e}")


@receiver(post_save, sender=StockMovement)
def update_medicine_stock(sender, instance, created, **kwargs):
    """
    Update medicine stock when stock movement is created
    """
    if created:
        try:
            medicine = instance.medicine
            
            # Update stock based on movement type
            # Ensure we always use the absolute value for calculations
            if instance.movement_type in ['in', 'return']:
                medicine.current_stock += abs(instance.quantity)
            elif instance.movement_type in ['out', 'damage', 'expired']:
                # Prevent negative stock - use max(0, ...) to ensure stock never goes below 0
                new_stock = medicine.current_stock - abs(instance.quantity)
                medicine.current_stock = max(0, new_stock)
            
            medicine.save()
            # Note: medicine.save() triggers the check_stock_levels signal
            # which already handles low stock notifications, so no need to
            # call notify_low_stock() again here
        
        except Exception as e:
            logger.error(f"Error updating stock for {instance.medicine.name}: {e}")

