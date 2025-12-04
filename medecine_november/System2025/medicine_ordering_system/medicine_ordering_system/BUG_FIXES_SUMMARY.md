# Bug Fixes Summary

## Date: 2025-01-XX

All three reported bugs have been verified and fixed.

---

## Bug 1: API Endpoint URL Pattern Mismatch ✅ FIXED

### Issue:
The API endpoint `api/notifications/mark-read/` mapped to `NotificationMarkReadView` which expected a `pk` URL parameter in its `post(request, pk)` method signature. However, the URL pattern (`path('api/notifications/mark-read/', ...)`) doesn't provide `pk`, causing a `TypeError` at runtime.

### Root Cause:
- URL pattern: `path('api/notifications/mark-read/', views.NotificationMarkReadView.as_view(), ...)`
- View method: `def post(self, request, pk):`
- The view required `pk` in URL but the API endpoint didn't provide it

### Solution:
Modified `NotificationMarkReadView.post()` to accept optional `pk` parameter:
- If `pk` is provided in URL (regular view): Uses it directly
- If `pk` is None (API endpoint): Reads `notification_id` from POST data

### Files Changed:
- `common/views.py` (lines 38-65)

### Code Changes:
```python
def post(self, request, pk=None):
    """
    Mark notification as read.
    Can be called with pk in URL (for regular views) or via POST data (for API).
    """
    # If pk is provided in URL (regular view)
    if pk is not None:
        notification = get_object_or_404(Notification, pk=pk, user=request.user)
        notification.is_read = True
        notification.save()
        return JsonResponse({'status': 'success'})
    
    # If called as API endpoint, get notification_id from POST data
    notification_id = request.POST.get('notification_id')
    if hasattr(request, 'data'):  # Handle DRF requests
        notification_id = notification_id or request.data.get('notification_id')
    
    if notification_id:
        try:
            notification = get_object_or_404(Notification, pk=int(notification_id), user=request.user)
            notification.is_read = True
            notification.save()
            return JsonResponse({'status': 'success', 'message': 'Notification marked as read'})
        except (ValueError, TypeError):
            return JsonResponse({'status': 'error', 'message': 'Invalid notification_id'}, status=400)
        except Http404:
            return JsonResponse({'status': 'error', 'message': 'Notification not found'}, status=404)
    else:
        return JsonResponse({'status': 'error', 'message': 'notification_id is required'}, status=400)
```

---

## Bug 1a: Exception Handler Bug ✅ FIXED

### Issue:
The exception handler on line 62 attempted to catch `Notification.DoesNotExist`, but `get_object_or_404()` raises `Http404` instead. This meant when a notification was not found, the `Http404` exception would propagate uncaught, causing the view to crash with an unhandled exception instead of returning the intended JSON error response.

### Root Cause:
- `get_object_or_404()` raises `Http404` exception, not `Notification.DoesNotExist`
- Exception handler was catching the wrong exception type
- Uncaught `Http404` would cause the view to crash

### Solution:
1. Added `Http404` to imports from `django.http`
2. Changed exception handler to catch `Http404` instead of `Notification.DoesNotExist`
3. Separated exception handling for clearer error messages:
   - `ValueError`/`TypeError` for invalid notification_id format → 400 Bad Request
   - `Http404` for notification not found → 404 Not Found

### Files Changed:
- `common/views.py` (line 4: imports, lines 62-65: exception handling)

### Code Changes:
```python
# Added to imports
from django.http import JsonResponse, Http404

# Fixed exception handling
try:
    notification = get_object_or_404(Notification, pk=int(notification_id), user=request.user)
    notification.is_read = True
    notification.save()
    return JsonResponse({'status': 'success', 'message': 'Notification marked as read'})
except (ValueError, TypeError):
    return JsonResponse({'status': 'error', 'message': 'Invalid notification_id'}, status=400)
except Http404:
    return JsonResponse({'status': 'error', 'message': 'Notification not found'}, status=404)
```

---

## Bug 2: Missing Admin Action Method ✅ FIXED

### Issue:
The `ReorderAlertAdmin` class declared `actions = ['mark_as_processed']` but the method `mark_as_processed()` was never defined in the class. This would cause Django to raise an `ImproperlyConfigured` exception when the admin loads.

### Root Cause:
- Admin class declared action: `actions = ['mark_as_processed']`
- Method was never implemented
- Django requires admin actions to be actual methods on the class

### Solution:
Added the `mark_as_processed()` method to `ReorderAlertAdmin` class that:
- Marks selected reorder alerts as processed
- Sets `processed_at` timestamp
- Sets `processed_by` to the current user
- Provides user feedback via messages

### Files Changed:
- `inventory/admin.py` (lines 41-52)

### Code Changes:
```python
def mark_as_processed(self, request, queryset):
    """Mark selected reorder alerts as processed"""
    from django.utils import timezone
    
    updated = queryset.filter(is_processed=False).update(
        is_processed=True,
        processed_at=timezone.now(),
        processed_by=request.user
    )
    
    self.message_user(
        request,
        f'{updated} reorder alert(s) marked as processed.',
        messages.SUCCESS
    )
mark_as_processed.short_description = 'Mark selected alerts as processed'
```

---

## Bug 3: Duplicate Notification Calls ✅ FIXED

### Issue:
When a `StockMovement` is created, `medicine.save()` at line 62 triggers the `check_stock_levels` signal which calls `notify_low_stock()` at line 22. Then lines 65-66 redundantly called `notify_low_stock()` again if stock is low, creating duplicate notifications.

### Root Cause:
- `update_medicine_stock()` signal handler calls `medicine.save()`
- `medicine.save()` triggers `check_stock_levels()` signal
- `check_stock_levels()` already calls `notify_low_stock()`
- The signal handler then called `notify_low_stock()` again (redundant)

### Solution:
Removed the redundant `notify_low_stock()` call from the `update_medicine_stock()` signal handler. Added a comment explaining that `medicine.save()` already triggers the stock level check via signals.

### Files Changed:
- `inventory/signals.py` (lines 62-65)

### Code Changes:
**Before:**
```python
medicine.save()

# Check for low stock after update
if medicine.current_stock <= medicine.reorder_point:
    NotificationService.notify_low_stock(medicine, medicine.current_stock)
```

**After:**
```python
medicine.save()
# Note: medicine.save() triggers the check_stock_levels signal
# which already handles low stock notifications, so no need to
# call notify_low_stock() again here
```

---

## Testing Recommendations

1. **Bug 1 Test:**
   - Test API endpoint: `POST /common/api/notifications/mark-read/` with `notification_id` in POST data
   - Test regular view: `POST /common/notifications/<pk>/mark-read/`

2. **Bug 2 Test:**
   - Access Django admin
   - Go to ReorderAlert admin page
   - Select alerts and use "Mark selected alerts as processed" action
   - Verify alerts are marked as processed

3. **Bug 3 Test:**
   - Create a StockMovement that results in low stock
   - Verify only one notification is sent (not duplicate)
   - Check notification log/table

---

## Verification

All fixes have been:
- ✅ Applied to source code
- ✅ Verified no linter errors
- ✅ Documented with comments
- ✅ Follow Django best practices

---

**All bugs fixed and ready for testing!** 🎉

