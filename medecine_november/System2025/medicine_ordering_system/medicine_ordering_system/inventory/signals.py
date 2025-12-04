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
            if instance.movement_type in ['in', 'return']:
                medicine.current_stock += abs(instance.quantity)
            elif instance.movement_type in ['out', 'damage', 'expired']:
                medicine.current_stock = max(0, medicine.current_stock - abs(instance.quantity))
            
            medicine.save()
            
            # Check for low stock after update
            if medicine.current_stock <= medicine.reorder_point:
                NotificationService.notify_low_stock(medicine, medicine.current_stock)
        
        except Exception as e:
            logger.error(f"Error updating stock for {instance.medicine.name}: {e}")

