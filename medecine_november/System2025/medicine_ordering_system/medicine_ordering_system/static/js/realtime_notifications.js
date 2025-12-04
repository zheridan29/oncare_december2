/**
 * Real-time Notification System
 * Polls for new notifications and updates the UI automatically
 */

class RealtimeNotifications {
    constructor() {
        this.apiUrl = '/common/api/notifications/';
        this.pollInterval = 10000; // 10 seconds
        this.pollTimer = null;
        this.lastCheckTime = null;
        this.isPolling = false;
        this.notificationWidget = null;
        this.notificationCount = null;
        
        this.init();
    }
    
    init() {
        // Wait for DOM to be ready
        if (document.readyState === 'loading') {
            document.addEventListener('DOMContentLoaded', () => this.start());
        } else {
            this.start();
        }
    }
    
    start() {
        // Find notification elements
        this.notificationWidget = document.getElementById('notifications-widget');
        this.notificationCount = document.getElementById('notification-count');
        
        // Attach clear all handler
        this.attachClearAllHandler();
        
        // Initial load
        this.fetchNotifications();
        
        // Start polling
        this.startPolling();
        
        // Stop polling when page is hidden (to save resources)
        document.addEventListener('visibilitychange', () => {
            if (document.hidden) {
                this.stopPolling();
            } else {
                this.startPolling();
                this.fetchNotifications(); // Immediately check when page becomes visible
            }
        });
    }
    
    startPolling() {
        if (this.isPolling) return;
        
        this.isPolling = true;
        this.pollTimer = setInterval(() => {
            this.fetchNotifications(true);
        }, this.pollInterval);
    }
    
    stopPolling() {
        if (this.pollTimer) {
            clearInterval(this.pollTimer);
            this.pollTimer = null;
        }
        this.isPolling = false;
    }
    
    async fetchNotifications(incremental = false) {
        try {
            let url = this.apiUrl;
            // Dashboard widget only shows unread notifications
            const params = new URLSearchParams();
            params.append('unread_only', 'true');
            
            if (incremental && this.lastCheckTime) {
                params.append('last_check', this.lastCheckTime);
                params.append('limit', '5');
            } else {
                params.append('limit', '10');
            }
            
            url += '?' + params.toString();
            
            const response = await fetch(url, {
                method: 'GET',
                headers: {
                    'X-Requested-With': 'XMLHttpRequest',
                },
                credentials: 'same-origin'
            });
            
            if (!response.ok) {
                throw new Error(`HTTP error! status: ${response.status}`);
            }
            
            const data = await response.json();
            
            // Update last check time
            if (data.latest_check_time) {
                this.lastCheckTime = data.latest_check_time;
            }
            
            // Update notification count
            if (data.unread_count !== undefined) {
                this.updateNotificationCount(data.unread_count);
            }
            
            // Always update notifications widget to reflect current state
            if (!incremental) {
                // Full refresh - always update widget with all notifications (including updated read status)
                this.updateNotificationWidget(data.notifications || []);
            } else {
                // Incremental update - only update if there are new notifications
                if (data.notifications && data.notifications.length > 0) {
                    this.showNewNotifications(data.notifications);
                    // For incremental updates, we need to merge with existing or replace
                    // For now, replace to ensure consistency
                    this.updateNotificationWidget(data.notifications);
                }
            }
            
        } catch (error) {
            console.error('Error fetching notifications:', error);
            // Silently fail - don't disturb user experience
        }
    }
    
    updateNotificationCount(count) {
        if (!this.notificationCount) {
            // Try to find it dynamically
            this.notificationCount = document.getElementById('notification-count');
        }
        
        if (this.notificationCount) {
            if (count > 0) {
                this.notificationCount.textContent = count;
                this.notificationCount.style.display = 'inline-block';
                this.notificationCount.classList.add('bg-danger');
            } else {
                this.notificationCount.style.display = 'none';
            }
        }
    }
    
    updateNotificationWidget(notifications) {
        if (!this.notificationWidget) {
            // Try to find it dynamically
            this.notificationWidget = document.getElementById('notifications-widget');
        }
        
        if (!this.notificationWidget) return;
        
        // Update widget header count
        const widgetCount = this.notificationWidget.querySelector('#widget-notification-count');
        const unreadCount = notifications.filter(n => !n.is_read).length;
        if (widgetCount) {
            if (unreadCount > 0) {
                widgetCount.textContent = unreadCount;
                widgetCount.style.display = 'inline-block';
            } else {
                widgetCount.style.display = 'none';
            }
        } else if (unreadCount > 0) {
            // Create badge if it doesn't exist
            const header = this.notificationWidget.querySelector('.card-header h5');
            if (header) {
                const badge = document.createElement('span');
                badge.id = 'widget-notification-count';
                badge.className = 'badge bg-danger ms-2';
                badge.textContent = unreadCount;
                header.appendChild(badge);
            }
        }
        
        const container = this.notificationWidget.querySelector('#notifications-container') ||
                         this.notificationWidget.querySelector('.card-body');
        
        if (!container) return;
        
        if (notifications.length === 0) {
            container.innerHTML = `
                <div class="text-center py-4 text-muted">
                    <i class="fas fa-bell-slash fa-3x mb-3"></i>
                    <p>No notifications at this time</p>
                </div>
            `;
            this.updateClearAllButton(false);
            return;
        }
        
        // Build HTML for notifications
        let html = '';
        notifications.forEach(notification => {
            const priorityClass = this.getPriorityClass(notification.priority);
            const icon = this.getNotificationIcon(notification.notification_type);
            const readClass = notification.is_read ? '' : 'border-start border-3 border-' + priorityClass;
            
            html += `
                <div class="list-group-item ${readClass} px-3 py-2 notification-item" data-notification-id="${notification.id}">
                    <div class="d-flex justify-content-between align-items-start">
                        <div class="flex-grow-1">
                            <div class="d-flex align-items-center mb-1">
                                <i class="${icon} me-2"></i>
                                <strong class="me-2">${this.escapeHtml(notification.title)}</strong>
                                ${!notification.is_read ? '<span class="badge bg-primary">New</span>' : ''}
                                ${notification.priority === 'urgent' ? '<span class="badge bg-danger ms-1">Urgent</span>' : ''}
                                ${notification.priority === 'high' ? '<span class="badge bg-warning ms-1">High</span>' : ''}
                            </div>
                            <p class="text-muted small mb-1">${this.escapeHtml(notification.message)}</p>
                            <small class="text-muted">
                                <i class="fas fa-clock me-1"></i>${notification.time_ago || 'Just now'}
                            </small>
                        </div>
                        ${notification.action_url ? `
                            <a href="${notification.action_url}" class="btn btn-sm btn-outline-primary ms-2">
                                <i class="fas fa-arrow-right"></i>
                            </a>
                        ` : ''}
                    </div>
                </div>
            `;
        });
        
        // Always replace the container content to ensure fresh state
        // This ensures server-rendered HTML is replaced with fresh API data
        container.innerHTML = '';
        let listGroup = document.createElement('div');
        listGroup.className = 'list-group list-group-flush';
        listGroup.innerHTML = html;
        container.appendChild(listGroup);
        
        // Add click handlers for marking as read
        this.attachClickHandlers();
        
        // Show/hide clear all button based on notifications
        this.updateClearAllButton(notifications.length > 0);
    }
    
    updateClearAllButton(show) {
        const clearAllBtn = document.getElementById('clear-all-notifications-btn');
        if (clearAllBtn) {
            if (show) {
                clearAllBtn.style.display = '';
            } else {
                clearAllBtn.style.display = 'none';
            }
        }
    }
    
    showNewNotifications(notifications) {
        // Show browser notification for new items (if permission granted)
        if ('Notification' in window && Notification.permission === 'granted') {
            notifications.forEach(notification => {
                if (!notification.is_read) {
                    new Notification(notification.title, {
                        body: notification.message,
                        icon: '/static/images/favicon.ico',
                        tag: `notification-${notification.id}`
                    });
                }
            });
        }
        
        // Show visual indicator on page
        this.showNotificationBadge(notifications.length);
    }
    
    showNotificationBadge(count) {
        // Create or update floating badge
        let badge = document.getElementById('new-notifications-badge');
        if (!badge) {
            badge = document.createElement('div');
            badge.id = 'new-notifications-badge';
            badge.className = 'position-fixed top-0 end-0 m-3';
            badge.style.zIndex = '9999';
            document.body.appendChild(badge);
        }
        
        badge.innerHTML = `
            <div class="alert alert-success alert-dismissible fade show shadow" role="alert">
                <i class="fas fa-bell me-2"></i>
                <strong>${count} new notification${count > 1 ? 's' : ''}!</strong>
                <button type="button" class="btn-close" data-bs-dismiss="alert" aria-label="Close"></button>
            </div>
        `;
        
        // Auto-dismiss after 5 seconds
        setTimeout(() => {
            if (badge && badge.parentNode) {
                const alert = badge.querySelector('.alert');
                if (alert) {
                    const bsAlert = new bootstrap.Alert(alert);
                    bsAlert.close();
                }
            }
        }, 5000);
    }
    
    attachClickHandlers() {
        // Mark as read when clicked
        document.querySelectorAll('.notification-item').forEach(item => {
            item.addEventListener('click', async (e) => {
                if (e.target.tagName === 'A') return; // Don't mark as read if clicking a link
                
                const notificationId = item.dataset.notificationId;
                if (notificationId && !item.querySelector('.badge')) {
                    // Only mark as read if not already read
                    await this.markAsRead(notificationId);
                    item.querySelector('.badge')?.remove();
                    item.classList.remove('border-start', 'border-3');
                }
            });
        });
    }
    
    async markAsRead(notificationId) {
        try {
            // Update UI immediately (optimistic update)
            const notificationItem = document.querySelector(`[data-notification-id="${notificationId}"]`);
            if (notificationItem) {
                // Remove "New" badge if present
                const badge = notificationItem.querySelector('.badge.bg-primary');
                if (badge) {
                    badge.remove();
                }
                // Remove border indicating unread status
                notificationItem.classList.remove('border-start', 'border-3', 'border-danger', 'border-warning', 'border-info');
            }
            
            // Call API to mark as read
            const formData = new FormData();
            formData.append('notification_id', notificationId);
            
            const csrfToken = this.getCsrfToken();
            const response = await fetch('/common/api/notifications/mark-read/', {
                method: 'POST',
                body: formData,
                headers: {
                    'X-CSRFToken': csrfToken,
                    'X-Requested-With': 'XMLHttpRequest',
                },
                credentials: 'same-origin'
            });
            
            if (response.ok) {
                const data = await response.json();
                
                // Force a full refresh (not incremental) to get updated notification state
                this.lastCheckTime = null;
                // Add a small delay to ensure database update is reflected
                await new Promise(resolve => setTimeout(resolve, 100));
                await this.fetchNotifications(false);
            } else {
                // Revert optimistic update on error
                if (notificationItem) {
                    notificationItem.classList.add('border-start', 'border-3', 'border-info');
                    const titleElement = notificationItem.querySelector('strong');
                    if (titleElement && !notificationItem.querySelector('.badge.bg-primary')) {
                        const badge = document.createElement('span');
                        badge.className = 'badge bg-primary';
                        badge.textContent = 'New';
                        titleElement.parentElement.insertBefore(badge, titleElement.nextSibling);
                    }
                }
                console.error('Error marking notification as read:', response.statusText);
            }
        } catch (error) {
            console.error('Error marking notification as read:', error);
        }
    }
    
    getPriorityClass(priority) {
        const classes = {
            'urgent': 'danger',
            'high': 'warning',
            'medium': 'info',
            'low': 'secondary'
        };
        return classes[priority] || 'info';
    }
    
    getNotificationIcon(type) {
        const icons = {
            'order_update': 'fas fa-shopping-cart text-primary',
            'stock_alert': 'fas fa-exclamation-triangle text-warning',
            'prescription_ready': 'fas fa-file-medical text-success',
            'payment_confirmation': 'fas fa-credit-card text-info',
            'system_maintenance': 'fas fa-tools text-secondary',
            'promotion': 'fas fa-gift text-danger',
            'security_alert': 'fas fa-shield-alt text-danger'
        };
        return icons[type] || 'fas fa-info-circle text-secondary';
    }
    
    escapeHtml(text) {
        const div = document.createElement('div');
        div.textContent = text;
        return div.innerHTML;
    }
    
    async clearAllNotifications() {
        try {
            const csrfToken = this.getCsrfToken();
            const formData = new FormData();
            formData.append('csrfmiddlewaretoken', csrfToken);
            
            const response = await fetch('/common/notifications/clear-all/', {
                method: 'POST',
                headers: {
                    'X-CSRFToken': csrfToken,
                    'X-Requested-With': 'XMLHttpRequest',
                },
                body: formData,
                credentials: 'same-origin'
            });
            
            if (!response.ok) {
                throw new Error(`HTTP error! status: ${response.status}`);
            }
            
            const data = await response.json();
            
            if (data.status === 'success') {
                // Optimistically update the UI immediately for instant feedback
                this.updateNotificationCount(0);
                
                // Clear the notification widget immediately
                const container = document.getElementById('notifications-container');
                if (container) {
                    container.innerHTML = `
                        <div class="text-center py-4 text-muted">
                            <i class="fas fa-bell-slash fa-3x mb-3"></i>
                            <p>No notifications at this time</p>
                        </div>
                    `;
                }
                
                // Hide the clear all button immediately
                this.updateClearAllButton(false);
                
                // Reset last check time so next poll will fetch fresh data
                this.lastCheckTime = null;
                
                // Don't refresh immediately - let the normal polling cycle handle it
                // This ensures the database transaction has time to commit
                // The widget is already cleared, so it will stay empty until the next poll
                
                // Schedule a delayed refresh after database has time to commit (2 seconds)
                setTimeout(async () => {
                    try {
                        await this.fetchNotifications(false);
                    } catch (error) {
                        console.error('Error refreshing notifications after clear all:', error);
                        // Widget is already cleared, so we're good even if refresh fails
                    }
                }, 2000);
            } else {
                console.error('Error clearing notifications:', data.message);
                alert('Error clearing notifications. Please try again.');
            }
        } catch (error) {
            console.error('Error clearing all notifications:', error);
            alert('Error clearing notifications. Please try again.');
        }
    }
    
    getCsrfToken() {
        // Get CSRF token from cookie (Django's default method)
        const name = 'csrftoken';
        let cookieValue = null;
        if (document.cookie && document.cookie !== '') {
            const cookies = document.cookie.split(';');
            for (let i = 0; i < cookies.length; i++) {
                const cookie = cookies[i].trim();
                if (cookie.substring(0, name.length + 1) === (name + '=')) {
                    cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                    break;
                }
            }
        }
        
        if (cookieValue) return cookieValue;
        
        // Try from Django's csrftoken input (if form exists)
        const csrfInput = document.querySelector('input[name="csrfmiddlewaretoken"]');
        if (csrfInput) return csrfInput.value;
        
        // Try meta tag as fallback
        const metaTag = document.querySelector('meta[name="csrf-token"]');
        if (metaTag) return metaTag.getAttribute('content');
        
        return '';
    }
    
    attachClearAllHandler() {
        const clearAllBtn = document.getElementById('clear-all-notifications-btn');
        if (clearAllBtn) {
            clearAllBtn.addEventListener('click', async (e) => {
                e.preventDefault();
                
                // Confirm action
                if (!confirm('Are you sure you want to mark all notifications as read?')) {
                    return;
                }
                
                // Disable button during request
                clearAllBtn.disabled = true;
                const originalText = clearAllBtn.innerHTML;
                clearAllBtn.innerHTML = '<i class="fas fa-spinner fa-spin me-1"></i>Clearing...';
                
                await this.clearAllNotifications();
                
                // Re-enable button
                clearAllBtn.disabled = false;
                clearAllBtn.innerHTML = originalText;
            });
        }
    }
}

// Request notification permission on page load
if ('Notification' in window && Notification.permission === 'default') {
    Notification.requestPermission();
}

// Initialize real-time notifications when script loads
const realtimeNotifications = new RealtimeNotifications();

