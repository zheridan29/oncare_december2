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
    def get_unread_count(user, exclude_completed_orders=True):
        """
        Get count of unread notifications for a user.
        
        Args:
            user: User to get unread count for
            exclude_completed_orders: If True, exclude notifications for delivered + paid orders
        """
        queryset = Notification.objects.filter(user=user, is_read=False)
        
        if exclude_completed_orders:
            # Exclude notifications for delivered and paid orders
            from orders.models import Order
            import re
            
            completed_order_ids = set(Order.objects.filter(
                status='delivered',
                payment_status='paid'
            ).values_list('id', flat=True))
            
            if completed_order_ids:
                # Get order-related notifications
                order_notifications = queryset.filter(
                    notification_type__in=['order_update', 'payment_confirmation'],
                    action_url__isnull=False
                )
                
                # Filter out notifications for completed orders
                excluded_ids = []
                for notification in order_notifications.only('id', 'action_url'):
                    if notification.action_url:
                        match = re.search(r'/orders/orders/(\d+)', notification.action_url)
                        if match:
                            order_id = int(match.group(1))
                            if order_id in completed_order_ids:
                                excluded_ids.append(notification.id)
                
                if excluded_ids:
                    queryset = queryset.exclude(id__in=excluded_ids)
        
        return queryset.count()
    
    @staticmethod
    def get_recent_notifications(user, limit=10, unread_only=False):
        """Get recent notifications for a user
        
        Args:
            user: User to get notifications for
            limit: Maximum number of notifications to return
            unread_only: If True, only return unread notifications
        """
        queryset = Notification.objects.filter(user=user)
        if unread_only:
            queryset = queryset.filter(is_read=False)
        return queryset.order_by('-created_at')[:limit]
    
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
    
    @staticmethod
    def notify_order_status_change(order, old_status, new_status, changed_by_user=None):
        """
        Create notifications when order status changes.
        Notifies: Sales Rep (if exists), Pharmacist/Admin (if status is important)
        
        Args:
            order: Order instance
            old_status: Previous status value
            new_status: New status value
            changed_by_user: User who made the change (optional, to avoid notifying them)
        """
        try:
            # Get status display names
            status_display_map = dict(Order.STATUS_CHOICES)
            old_status_display = status_display_map.get(old_status, old_status.title())
            new_status_display = status_display_map.get(new_status, new_status.title())
            
            # Determine priority based on status
            priority_map = {
                'pending': 'medium',
                'confirmed': 'high',
                'processing': 'medium',
                'ready_for_pickup': 'high',
                'shipped': 'high',
                'delivered': 'urgent',
                'cancelled': 'high',
                'returned': 'high',
            }
            priority = priority_map.get(new_status, 'medium')
            
            # Build action URL - try pharmacist detail first, fallback to regular detail
            try:
                action_url = reverse('orders:pharmacist_order_detail', args=[order.id])
            except:
                try:
                    action_url = reverse('orders:order_detail', args=[order.id])
                except:
                    action_url = ''
            
            # Notify Sales Rep about status change
            if order.sales_rep and (changed_by_user is None or order.sales_rep.id != changed_by_user.id):
                NotificationService.create_notification(
                    user=order.sales_rep,
                    notification_type='order_update',
                    title=f'Order {order.order_number} Status Updated',
                    message=f'Order status changed from {old_status_display} to {new_status_display}. Customer: {order.customer_name}',
                    priority=priority,
                    action_url=action_url,
                )
            
            # Notify Pharmacist/Admin (except the one who made the change)
            if changed_by_user:
                pharmacist_admins = User.objects.filter(
                    Q(role='pharmacist_admin') | Q(role='admin'),
                    is_active=True
                ).exclude(id=changed_by_user.id)
            else:
                pharmacist_admins = User.objects.filter(
                    Q(role='pharmacist_admin') | Q(role='admin'),
                    is_active=True
                )
            
            # Only notify for significant status changes
            significant_statuses = ['confirmed', 'ready_for_pickup', 'shipped', 'delivered', 'cancelled', 'returned']
            if new_status in significant_statuses:
                for admin in pharmacist_admins:
                    NotificationService.create_notification(
                        user=admin,
                        notification_type='order_update',
                        title=f'Order {order.order_number} Status: {new_status_display}',
                        message=f'Order from {order.sales_rep.get_full_name() if order.sales_rep else "System"} for {order.customer_name} is now {new_status_display}. Changed from {old_status_display}.',
                        priority=priority,
                        action_url=action_url,
                    )
            
            logger.info(f"Status change notifications created for order {order.order_number}: {old_status} -> {new_status}")
            
        except Exception as e:
            logger.error(f"Error creating status change notifications: {e}")
    
    @staticmethod
    def notify_order_status_change(order, old_status, new_status, changed_by_user=None):
        """
        Create notifications when order status changes.
        Notifies: Sales Rep (if exists), Pharmacist/Admin (if status is important)
        
        Args:
            order: Order instance
            old_status: Previous status value
            new_status: New status value  
            changed_by_user: User who made the change (optional, to avoid notifying them)
        """
        try:
            # Get status display names
            status_display_map = dict(Order.STATUS_CHOICES)
            old_status_display = status_display_map.get(old_status, old_status.title())
            new_status_display = status_display_map.get(new_status, new_status.title())
            
            # Determine priority based on status
            priority_map = {
                'pending': 'medium',
                'confirmed': 'high',
                'processing': 'medium',
                'ready_for_pickup': 'high',
                'shipped': 'high',
                'delivered': 'urgent',
                'cancelled': 'high',
                'returned': 'high',
            }
            priority = priority_map.get(new_status, 'medium')
            
            # Build action URL - try pharmacist detail first, fallback to regular detail
            try:
                action_url = reverse('orders:pharmacist_order_detail', args=[order.id])
            except:
                try:
                    action_url = reverse('orders:order_detail', args=[order.id])
                except:
                    action_url = ''
            
            # Notify Sales Rep about status change
            if order.sales_rep and (changed_by_user is None or order.sales_rep.id != changed_by_user.id):
                NotificationService.create_notification(
                    user=order.sales_rep,
                    notification_type='order_update',
                    title=f'Order {order.order_number} Status Updated',
                    message=f'Order status changed from {old_status_display} to {new_status_display}. Customer: {order.customer_name}',
                    priority=priority,
                    action_url=action_url,
                )
            
            # Notify other Pharmacist/Admin users (except the one who made the change)
            # Only notify for significant status changes
            significant_statuses = ['confirmed', 'ready_for_pickup', 'shipped', 'delivered', 'cancelled', 'returned']
            if new_status in significant_statuses:
                pharmacist_admins = User.objects.filter(
                    Q(role='pharmacist_admin') | Q(role='admin'),
                    is_active=True
                )
                
                # Exclude the user who made the change
                if changed_by_user:
                    pharmacist_admins = pharmacist_admins.exclude(id=changed_by_user.id)
                
                for admin in pharmacist_admins:
                    NotificationService.create_notification(
                        user=admin,
                        notification_type='order_update',
                        title=f'Order {order.order_number} Status: {new_status_display}',
                        message=f'Order from {order.sales_rep.get_full_name() if order.sales_rep else "System"} for {order.customer_name} is now {new_status_display}. Changed from {old_status_display}.',
                        priority=priority,
                        action_url=action_url,
                    )
            
            logger.info(f"Status change notifications created for order {order.order_number}: {old_status} -> {new_status}")
            
        except Exception as e:
            logger.error(f"Error creating status change notifications: {e}")
    
    @staticmethod
    def mark_order_notifications_as_read(order):
        """
        Mark all notifications related to a specific order as read for all users.
        This is called when an order becomes delivered and paid.
        """
        from django.utils import timezone
        import re
        
        try:
            # Get all unread order-related notifications
            all_order_notifications = Notification.objects.filter(
                notification_type__in=['order_update', 'payment_confirmation'],
                is_read=False,
                action_url__isnull=False
            )
            
            # Mark notifications that match the order URL
            marked_count = 0
            order_id_str = str(order.id)
            
            for notification in all_order_notifications:
                if notification.action_url:
                    # Extract order ID from action_url using regex
                    # URL pattern: /orders/orders/{id}/ or /orders/orders/{id}
                    match = re.search(r'/orders/orders/(\d+)', notification.action_url)
                    if match:
                        url_order_id = match.group(1)
                        if url_order_id == order_id_str:
                            notification.is_read = True
                            notification.read_at = timezone.now()
                            notification.save()
                            marked_count += 1
            
            logger.info(f"Marked {marked_count} notifications as read for order {order.order_number}")
            return marked_count
            
        except Exception as e:
            logger.error(f"Error marking order notifications as read: {e}")
            return 0

