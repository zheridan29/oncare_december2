# Notification Filtering for Completed Orders

## Overview
Updated the notification system to automatically hide notifications for orders that are **delivered** and **paid**. When an order status is updated to delivered + paid, all related notifications are automatically marked as read and hidden from both the dashboard widget and notifications page.

## Changes Made

### 1. Automatic Notification Marking When Order Completed
- **File**: `orders/views.py` - `OrderStatusUpdateView.form_valid()`
- **Behavior**: When an order is updated to status='delivered' and payment_status='paid', all related notifications are automatically marked as read
- **Affects**: All users (sales representative and admin/pharmacist) who have notifications for that order

### 2. Notification List Page Filtering
- **File**: `common/views.py` - `NotificationListView.get_queryset()`
- **Behavior**: Notifications for delivered + paid orders are automatically excluded from the notifications list page
- **Method**: Parses `action_url` to extract order ID and filters out notifications for completed orders

### 3. Dashboard Widget API Filtering
- **File**: `common/views.py` - `NotificationAPIView.get()`
- **Behavior**: Notifications for delivered + paid orders are filtered out from the dashboard widget API response
- **Result**: These notifications won't appear in the dashboard widget

### 4. Unread Count Calculation
- **File**: `common/services.py` - `NotificationService.get_unread_count()`
- **Enhancement**: Added option to exclude completed order notifications from unread count
- **Default**: Excludes completed orders by default to provide accurate counts

### 5. Service Method for Marking Order Notifications as Read
- **File**: `common/services.py` - `NotificationService.mark_order_notifications_as_read()`
- **Functionality**: Marks all notifications related to a specific order as read for all users
- **Usage**: Called automatically when order becomes delivered + paid

## How It Works

### When Order Becomes Delivered + Paid:

1. **Order Status Update**: Admin/Pharmacist updates order to "Delivered" and "Paid"
2. **Automatic Notification Marking**: All notifications related to that order are automatically marked as read
   - Sales representative's notifications
   - Admin/Pharmacist notifications
   - All users who have notifications for that order
3. **Immediate Removal**: Notifications disappear from:
   - Dashboard widget (because they're now marked as read)
   - Notifications page (filtered out even if they were still unread)

### Notification Filtering Logic:

1. **Identifies Completed Orders**: Finds all orders with:
   - Status = `'delivered'`
   - Payment status = `'paid'`

2. **Filters Notifications**: Excludes notifications that:
   - Are of type `'order_update'` or `'payment_confirmation'`
   - Have an `action_url` containing the order ID pattern: `/orders/orders/{id}/`

3. **Applies to All Users**: Works for:
   - Sales representatives
   - Admin users
   - Pharmacist/Admin users

## User Experience

### For Admin/Pharmacist:
- Updates order status to "Delivered" and "Paid"
- Related notifications automatically disappear
- Dashboard widget and notifications page no longer show these notifications
- Cleaner notification list focused on active orders

### For Sales Representative:
- When their order is marked as delivered + paid by admin/pharmacist
- Their notifications for that order automatically disappear
- No manual action needed to clear them
- Dashboard widget stays clean and focused

## Technical Details

### Notification Marking Logic:
```python
# Called when order becomes delivered + paid
NotificationService.mark_order_notifications_as_read(order)

# Marks all notifications with action_url containing order ID
# Pattern: /orders/orders/{order.id}/
```

### Filtering Logic:
1. Extract order IDs from completed orders (delivered + paid)
2. Parse notification action_urls to extract order IDs
3. Match and exclude notifications for completed orders
4. Apply to both list view and API endpoint

### Performance Considerations:
- Uses sets for O(1) order ID lookup
- Only processes order-related notifications
- Filters applied at database level where possible
- Minimal impact on query performance

## Files Modified

1. `common/views.py`
   - `NotificationListView.get_queryset()` - Filter out completed orders
   - `NotificationAPIView.get()` - Filter out completed orders from API
   - Updated unread count to exclude completed orders

2. `common/services.py`
   - `get_unread_count()` - Added option to exclude completed orders
   - `mark_order_notifications_as_read()` - New method to mark notifications as read

3. `orders/views.py`
   - `OrderStatusUpdateView.form_valid()` - Auto-mark notifications when order completed

## Testing Checklist

- [ ] Update order to "Delivered" and "Paid" status
- [ ] Verify notifications disappear from dashboard widget
- [ ] Verify notifications disappear from notifications page
- [ ] Verify notifications are marked as read in database
- [ ] Verify sales representative notifications are also hidden
- [ ] Verify admin/pharmacist notifications are also hidden
- [ ] Verify unread count updates correctly
- [ ] Verify other notifications (stock alerts, etc.) still appear
- [ ] Verify order with "Delivered" but not "Paid" still shows notifications
- [ ] Verify order with "Paid" but not "Delivered" still shows notifications

