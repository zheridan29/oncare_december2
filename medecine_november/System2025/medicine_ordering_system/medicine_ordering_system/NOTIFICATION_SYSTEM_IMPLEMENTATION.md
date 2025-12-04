# Notification System & Order Units Implementation

## ✅ Completed Features

### 1. **Enhanced Notification System**
- Created `NotificationService` in `common/services.py` for centralized notification management
- Automatic notifications when orders are placed
- Automatic low stock alerts when inventory falls below reorder point
- Notification display widget for dashboards

### 2. **Order Units Feature**
- Added `unit` field to `OrderItem` model with choices:
  - Pieces
  - Boxes
  - Bottles
  - Strips
  - Units
  - Packets
- Updated order forms to include unit selection
- Updated order creation view to handle units

### 3. **Admin Stock Level Management**
- Enhanced `MedicineAdmin` in `inventory/admin.py` with:
  - Stock status badge display
  - Bulk actions for checking low stock
  - Set default reorder points action
  - Manual stock level editing in admin interface

### 4. **Dashboard Notifications Display**
- Added notifications widget to:
  - Orders Dashboard
  - Inventory Dashboard
  - Admin Dashboard
- Notification count in navigation bar
- Real-time notification display with priority indicators

### 5. **Automatic Stock Monitoring**
- Created signals in `inventory/signals.py`:
  - `check_stock_levels` - checks stock after medicine save
  - `update_medicine_stock` - updates stock from movements
- Automatic notification generation when stock goes low

## 📁 Files Modified

### Models
- `orders/models.py` - Added `unit` field to `OrderItem`
- `common/models.py` - Notification model (already existed, enhanced usage)

### Services
- `common/services.py` - New notification service with methods:
  - `create_notification()` - Create any notification
  - `notify_order_placed()` - Order placement notifications
  - `notify_low_stock()` - Low stock alerts
  - `get_unread_count()` - Get notification counts
  - `get_recent_notifications()` - Get recent notifications

### Views
- `orders/views.py` - Updated `OrderCreateView` to:
  - Handle unit fields
  - Send notifications on order creation
  - Check stock and notify when low
- `inventory/views.py` - Added notifications to dashboard context
- `oncare_admin/views.py` - Added notifications to admin dashboard

### Admin
- `inventory/admin.py` - Complete admin interface with:
  - Stock status display
  - Bulk actions for stock management
  - Enhanced medicine editing interface

### Templates
- `templates/common/notifications_widget.html` - Reusable notification widget
- `templates/orders/dashboard.html` - Added notification widget
- `templates/inventory/dashboard.html` - Added notification widget
- `templates/orders/order_form.html` - Added unit selection fields

### Forms
- `orders/forms.py` - Added unit fields (`unit_1` through `unit_5`)

### Signals
- `inventory/signals.py` - Automatic stock monitoring and notifications
- `inventory/apps.py` - Registered signals

## 🔄 Migration Required

Run the following commands to apply database changes:

```bash
python manage.py makemigrations
python manage.py migrate
```

## 🎯 Usage

### For Administrators

1. **Setting Stock Levels:**
   - Go to Admin Panel → Medicines
   - Edit any medicine
   - Set `reorder_point` and `minimum_stock_level` manually
   - Save - notifications will automatically trigger when stock goes low

2. **Bulk Stock Management:**
   - Select multiple medicines in admin
   - Use "Check and notify low stock" action
   - Use "Set reorder points to minimum stock levels" action

### For Sales Representatives

1. **Creating Orders with Units:**
   - Create new order
   - Select medicine
   - Enter quantity
   - Choose unit (boxes, pieces, etc.)
   - Complete order - notification sent automatically

2. **Viewing Notifications:**
   - Check dashboard for recent notifications
   - Click notification bell icon in navigation
   - View all notifications page

### For Pharmacists/Admins

1. **Receiving Notifications:**
   - New order notifications appear in dashboard
   - Low stock alerts appear automatically
   - Click notification to view details

2. **Stock Management:**
   - Dashboard shows low stock count
   - Click to view medicines needing reorder
   - Use admin panel to adjust reorder points

## 📊 Notification Types

- **order_update** - Order placed, status changed
- **stock_alert** - Low stock, out of stock
- **prescription_ready** - Prescription verified
- **payment_confirmation** - Payment received
- **system_maintenance** - System updates
- **promotion** - Promotional messages
- **security_alert** - Security notifications

## 🎨 Notification Priorities

- **Urgent** - Red badge (out of stock)
- **High** - Orange badge (critical low stock)
- **Medium** - Blue badge (regular notifications)
- **Low** - Gray badge (informational)

## 🔔 Automatic Notifications

The system automatically sends notifications for:

1. **Order Placement:**
   - Sales Rep receives confirmation
   - All Pharmacist/Admin users receive new order alert

2. **Low Stock:**
   - Triggered when `current_stock <= reorder_point`
   - All Pharmacist/Admin users notified
   - Priority based on stock level (urgent if out of stock)

## 🚀 Next Steps

1. Run migrations: `python manage.py migrate`
2. Test notification system by creating orders
3. Test low stock alerts by reducing medicine stock
4. Customize notification messages in `common/services.py`
5. Add email/SMS notifications (optional future enhancement)

---

**Note:** Ensure `inventory.signals` is imported in `inventory/apps.py` for automatic stock monitoring to work.

