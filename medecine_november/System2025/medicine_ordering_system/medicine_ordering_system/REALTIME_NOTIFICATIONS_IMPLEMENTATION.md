# Real-time Notifications Implementation

## ✅ Completed Features

### 1. **Enhanced API Endpoint**
- Updated `NotificationAPIView` in `common/views.py` to support:
  - Incremental updates using `last_check` parameter
  - Returns unread count and recent notifications
  - POST method for marking notifications as read
  - Time-ago formatting for human-readable timestamps

### 2. **Real-time JavaScript Client**
- Created `static/js/realtime_notifications.js` with:
  - Automatic polling every 10 seconds
  - Incremental updates (only fetches new notifications)
  - Updates notification widget and count badge in real-time
  - Browser notifications support (with permission)
  - Visual alerts for new notifications
  - Auto-pause when page is hidden (saves resources)

### 3. **Template Updates**
- Updated `templates/common/notifications_widget.html`:
  - Added ID for JavaScript targeting
  - Added container ID for dynamic updates
  
- Updated `templates/base.html`:
  - Included real-time notifications script
  - Updated notification count badge ID

## 🔄 How It Works

### Polling Mechanism
1. **Initial Load**: Fetches last 10 notifications on page load
2. **Polling**: Checks for new notifications every 10 seconds
3. **Incremental Updates**: Only fetches notifications created after last check time
4. **UI Updates**: Automatically updates:
   - Notification widget on dashboards
   - Notification count badge in navigation
   - Shows visual alerts for new notifications

### Features
- **Efficient Polling**: Only fetches new notifications after initial load
- **Resource Friendly**: Stops polling when page is hidden
- **Browser Notifications**: Shows native browser notifications (if permission granted)
- **Visual Feedback**: Shows floating badge for new notifications
- **Click to Mark Read**: Notifications can be marked as read by clicking
- **Auto-refresh**: Notification list updates automatically

## 📊 API Endpoints

### GET `/common/api/notifications/`
Returns notifications with optional parameters:
- `limit`: Number of notifications to return (default: 10)
- `last_check`: ISO timestamp to get only new notifications

**Response:**
```json
{
  "notifications": [...],
  "unread_count": 5,
  "latest_check_time": "2024-12-03T...",
  "latest_notification_time": "2024-12-03T..."
}
```

### POST `/common/api/notifications/`
Mark notifications as read:
- `notification_id`: ID of notification to mark as read
- `mark_all`: Set to "true" to mark all as read

## 🎯 Usage

The real-time system works automatically once the page loads. No additional configuration needed!

### For Users:
1. Notifications appear automatically without page refresh
2. Click notifications to mark them as read
3. Browser notifications appear if permission is granted
4. Notification count updates in real-time

### For Developers:
- Polling interval can be adjusted in `realtime_notifications.js` (default: 10000ms)
- API endpoint can be customized in `common/views.py`
- Visual styling can be adjusted in the JavaScript

## 🔧 Customization

### Change Polling Interval
Edit `static/js/realtime_notifications.js`:
```javascript
this.pollInterval = 10000; // Change to desired milliseconds
```

### Adjust Notification Limit
Default is 10 notifications. Change in API call or JavaScript:
```javascript
url += '?limit=20'; // Fetch 20 notifications
```

### Browser Notification Permission
The script automatically requests permission on page load. Users can:
- Allow: See browser notifications for new alerts
- Block: Only see in-page notifications

## 🚀 Testing

1. **Create a new order** → Notification should appear within 10 seconds
2. **Reduce stock below reorder point** → Low stock alert appears automatically
3. **Check notification count** → Updates in navigation bar without refresh
4. **Click notification** → Marks as read and updates UI immediately

## 📝 Notes

- Polling pauses when browser tab is hidden (saves resources)
- Notifications are checked immediately when tab becomes visible
- Browser notifications require user permission (asked once)
- Visual badge appears for new notifications and auto-dismisses after 5 seconds

---

**No page refresh needed!** Notifications now update in real-time automatically.

