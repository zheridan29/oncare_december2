"""
Common services for notifications and system utilities
"""

from django.db.models import Q
from django.utils import timezone
from django.urls import reverse
from .models import Notification
from accounts.models import User
from orders.models import Order
from inventory.models import Medicine, ReorderAlert
import logging

logger = logging.getLogger(__name__)


class NotificationService:
    """
    Service for creating and managing system notifications
    """
    
    @staticmethod
    def create_notification(user, notification_type, title, message, priority='medium', action_url='', **kwargs):
        """
        Create a notification for a user
        
        Args:
            user: User instance or user ID
            notification_type: Type of notification (from Notification.NOTIFICATION_TYPES)
            title: Notification title
            message: Notification message
            priority: Priority level (low, medium, high, urgent)
            action_url: URL to navigate to when notification is clicked
            **kwargs: Additional fields (expires_at, etc.)
        """
        try:
            if isinstance(user, int):
                user = User.objects.get(id=user)
            
            notification = Notification.objects.create(
                user=user,
                notification_type=notification_type,
                title=title,
                message=message,
                priority=priority,
                action_url=action_url or '',
                expires_at=kwargs.get('expires_at'),
            )
            
            logger.info(f"Notification created: {title} for user {user.username}")
            return notification
            
        except Exception as e:
            logger.error(f"Error creating notification: {e}")
            return None
    
    @staticmethod
    def notify_order_placed(order):
        """
        Create notifications when an order is placed
        Notifies: Sales Rep (confirmation), Pharmacist/Admin (new order alert)
        """
        notifications = []
        
        try:
            # Notification for Sales Rep (order confirmation)
            if order.sales_rep:
                NotificationService.create_notification(
                    user=order.sales_rep,
                    notification_type='order_update',
                    title=f'Order {order.order_number} Placed Successfully',
                    message=f'Your order for {order.customer_name} has been placed. Total: ₱{order.total_amount:,.2f}',
                    priority='medium',
                    action_url=reverse('orders:order_detail', args=[order.id]) if order.id else '',
                )
            
            # Notification for all Pharmacist/Admin users (new order alert)
            pharmacist_admins = User.objects.filter(
                Q(role='pharmacist_admin') | Q(role='admin'),
                is_active=True
            )
            
            for admin in pharmacist_admins:
                NotificationService.create_notification(
                    user=admin,
                    notification_type='order_update',
                    title=f'New Order: {order.order_number}',
                    message=f'New order from {order.customer_name} (₱{order.total_amount:,.2f}). Status: {order.get_status_display()}',
                    priority='high',
                    action_url=reverse('orders:order_detail', args=[order.id]) if order.id else '',
                )
            
            logger.info(f"Order placement notifications created for order {order.order_number}")
            
        except Exception as e:
            logger.error(f"Error creating order placement notifications: {e}")
    
    @staticmethod
    def notify_low_stock(medicine, current_stock=None):
        """
        Create notifications when medicine stock goes low
        Notifies: Pharmacist/Admin, Admin
        """
        if current_stock is None:
            current_stock = medicine.current_stock
        
        try:
            # Determine priority based on stock level
            if current_stock == 0:
                priority = 'urgent'
                status_text = 'out of stock'
            elif current_stock <= medicine.reorder_point:
                priority = 'high'
                status_text = 'low stock'
            else:
                return  # Not low enough to notify
            
            # Get all Pharmacist/Admin and Admin users
            admins = User.objects.filter(
                Q(role='pharmacist_admin') | Q(role='admin'),
                is_active=True
            )
            
            for admin in admins:
                NotificationService.create_notification(
                    user=admin,
                    notification_type='stock_alert',
                    title=f'Stock Alert: {medicine.name}',
                    message=f'{medicine.name} is {status_text}. Current stock: {current_stock}, Reorder point: {medicine.reorder_point}',
                    priority=priority,
                    action_url=reverse('inventory:medicine_detail', args=[medicine.id]) if medicine.id else '',
                )
            
            logger.info(f"Low stock notifications created for {medicine.name}")
            
        except Exception as e:
            logger.error(f"Error creating low stock notifications: {e}")
    
    @staticmethod
    def get_unread_count(user):
        """Get count of unread notifications for a user"""
        return Notification.objects.filter(user=user, is_read=False).count()
    
    @staticmethod
    def get_recent_notifications(user, limit=10):
        """Get recent notifications for a user"""
        return Notification.objects.filter(user=user).order_by('-created_at')[:limit]
    
    @staticmethod
    def mark_as_read(notification_id, user):
        """Mark a notification as read"""
        try:
            notification = Notification.objects.get(id=notification_id, user=user)
            if not notification.is_read:
                notification.is_read = True
                notification.read_at = timezone.now()
                notification.save()
            return True
        except Notification.DoesNotExist:
            return False
    
    @staticmethod
    def mark_all_as_read(user):
        """Mark all notifications as read for a user"""
        Notification.objects.filter(user=user, is_read=False).update(
            is_read=True,
            read_at=timezone.now()
        )

