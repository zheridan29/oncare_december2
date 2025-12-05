# Real-Time Dashboard Updates for Sales Representative's "My Orders" Dashboard

## Overview

Implemented real-time updates for the Sales Representative's "My Orders" Dashboard (`/orders/orders/`) so that when a pharmacist/admin updates an order status, the dashboard automatically reflects the changes without requiring a page refresh.

## Problem

Previously, when a pharmacist/admin updated an order status (e.g., from "pending" to "processing" or "delivered"), the sales representative would need to manually refresh the page to see the updated status, order counts, and statistics.

## Solution

Implemented a real-time polling system that:
- Fetches dashboard statistics from an API endpoint every 5 seconds
- Updates all dashboard elements automatically when status changes are detected
- Updates individual order rows in the table to reflect status and payment status changes
- Works seamlessly even when filters are applied

## Implementation Details

### 1. API Endpoint

**File**: `orders/views.py`

Created a new API view `SalesRepDashboardAPIView` that returns:
- Order statistics (total, pending, processing, delivered, cancelled, total revenue)
- Orders by status breakdown
- Current page of orders (respecting filters and pagination)

**URL**: `/orders/api/sales-rep/dashboard/`

**Method**: GET

**Query Parameters**:
- `status` (optional): Filter by order status
- `date_from` (optional): Filter by date from
- `date_to` (optional): Filter by date to
- `page` (optional): Page number for pagination

**Response Format**:
```json
{
    "statistics": {
        "total_orders": 50,
        "pending_orders": 5,
        "processing_orders": 10,
        "delivered_orders": 30,
        "cancelled_orders": 5,
        "total_revenue": 50000.00
    },
    "orders_by_status": {
        "pending": {"name": "Pending", "count": 5},
        "processing": {"name": "Processing", "count": 10},
        ...
    },
    "orders": [
        {
            "id": 123,
            "order_number": "ORD-2025-00123",
            "status": "processing",
            "status_display": "Processing",
            "payment_status": "pending",
            "payment_status_display": "Pending",
            "items_count": 3,
            "total_amount": 1500.00,
            "created_at": "2025-01-15T10:30:00",
            "created_at_display": "Jan 15, 2025 10:30"
        },
        ...
    ],
    "pagination": {
        "current_page": 1,
        "total_pages": 3,
        "has_next": true,
        "has_previous": false
    }
}
```

### 2. JavaScript Real-Time Polling

**File**: `static/js/realtime_salesrep_dashboard.js`

Created a `RealtimeSalesRepDashboard` class that:
- Polls the API endpoint every 5 seconds
- Updates statistics cards automatically
- Updates "Orders by Status" breakdown
- Updates individual order rows in the table to reflect status changes
- Only runs on the sales rep order list page
- Respects current filters and pagination when fetching data
- Updates rows in place without disrupting the user's view

**Key Features**:
- Automatic initialization when the dashboard page loads
- Efficient row updates (only updates changed cells)
- Error handling (fails silently to not disturb user experience)
- Prevents concurrent API requests
- Smart row updating - only updates status, payment status, and action buttons

### 3. Template Updates

**File**: `templates/orders/order_list.html`

Added:
- ID attributes to all elements that need updating:
  - `stat-total-orders`
  - `stat-pending-orders`
  - `stat-processing-orders`
  - `stat-delivered-orders`
  - `stat-cancelled-orders`
  - `stat-total-revenue`
  - `status-count-{status_code}` for each status in the breakdown
  - `orders-table-tbody` for the orders table
- Main dashboard container ID: `sales-rep-orders-dashboard`
- Included the JavaScript file using `{% block extra_js %}` (only for sales reps)

### 4. URL Configuration

**File**: `orders/urls.py`

Added the new API endpoint:
```python
path('api/sales-rep/dashboard/', views.SalesRepDashboardAPIView.as_view(), name='api_sales_rep_dashboard'),
```

## How It Works

1. **Page Load**: When the sales rep's "My Orders" dashboard loads, the JavaScript file is included and initializes.

2. **Initial Fetch**: The dashboard immediately fetches the latest statistics from the API (respecting any active filters).

3. **Polling**: Every 5 seconds, the JavaScript automatically fetches updated statistics.

4. **Update**: When new data is received, it updates:
   - All 6 statistics cards (Total Orders, Pending, Processing, Delivered, Cancelled, Total Revenue)
   - Orders by Status breakdown (all status counts)
   - Individual order rows in the table (status badges, payment status badges, action buttons)

5. **Smart Row Updates**: The system finds existing rows by order ID and updates only the status, payment status, and action buttons, preserving the order's position in the list.

## Update Frequency

- **Polling Interval**: 5 seconds (5000ms)
- **Immediate Update**: When page becomes visible (tab switch back)
- **Automatic**: No user interaction required

## User Experience

- **Seamless**: Updates happen in the background without disrupting the user
- **Fast**: Status changes appear within 5 seconds of a pharmacist/admin update
- **No Refresh Needed**: Users never need to manually refresh the page
- **Filter-Aware**: Works correctly even when filters are applied
- **Non-Disruptive**: Row updates preserve the user's current view and scroll position

## Example Scenario

1. **10:00:00 AM**: Sales rep views the "My Orders" dashboard
   - Order #123: Status "Pending", Payment Status "Pending"
   - Pending Orders: 5

2. **10:00:15 AM**: Pharmacist/admin updates Order #123 status to "Processing"
   - Order status changed in database
   - Notification sent to sales rep

3. **10:00:20 AM**: Dashboard automatically updates (within 5 seconds)
   - Order #123 status badge changes from "Pending" (yellow) to "Processing" (blue)
   - Pending Orders: 4 (automatically updated)
   - Processing Orders: 11 (automatically updated)
   - Status breakdown updated
   - Edit/Cancel buttons disappear from Order #123 row (since it's no longer pending)

**No page refresh required!**

## Technical Considerations

### Performance
- Efficient polling (only when dashboard is visible)
- Minimal API response size
- Fast DOM updates (only updates changed cells)
- Prevents concurrent requests

### Error Handling
- Silently handles network errors
- Doesn't interrupt user workflow
- Continues polling even after errors

### Security
- Requires authentication (LoginRequiredMixin)
- Checks user permissions (sales rep only)
- Filters orders by sales_rep to ensure users only see their own orders
- Uses CSRF protection for API requests

### Filter Handling
- Respects current filters when fetching data
- Updates rows that match current filter criteria
- Doesn't add/remove rows that would disrupt filtered view
- Statistics always reflect all orders (not filtered)

## Files Modified

1. **`orders/views.py`**
   - Added `SalesRepDashboardAPIView` class

2. **`orders/urls.py`**
   - Added API endpoint URL pattern

3. **`templates/orders/order_list.html`**
   - Added ID attributes to updatable elements
   - Added dashboard container ID
   - Included JavaScript file (only for sales reps)

4. **`static/js/realtime_salesrep_dashboard.js`** (NEW)
   - Created real-time dashboard polling system for sales reps

## Testing

To test the real-time updates:

1. Open the sales rep's "My Orders" dashboard in one browser tab/window
2. Log in as a pharmacist/admin in another tab/window
3. Navigate to an order and update its status (e.g., from "Pending" to "Processing")
4. Watch the sales rep's dashboard - it should update within 5 seconds automatically:
   - Status badge changes color and text
   - Statistics cards update
   - Status breakdown updates
   - Action buttons update (edit/cancel buttons may appear/disappear)

## Differences from Pharmacist Dashboard

The sales rep dashboard implementation differs from the pharmacist dashboard in:
- **Filter-Aware Updates**: Respects and maintains current filters when updating
- **Row-Level Updates**: Updates individual rows instead of replacing the entire table
- **Pagination Support**: Works correctly with paginated results
- **Revenue Tracking**: Includes total revenue calculation in statistics
- **Own Orders Only**: Only shows orders belonging to the logged-in sales rep

## Future Enhancements

Potential improvements:
- WebSocket support for instant updates (instead of polling)
- Configurable polling interval
- Visual indicators when updates occur (subtle animation/highlight)
- Sound notification when order status changes (optional)
- Real-time notifications integration (show toast when status changes)

---

**Implementation Date**: December 2025  
**System**: OnCare Medicine Ordering System  
**Module**: Orders - Sales Representative Dashboard


