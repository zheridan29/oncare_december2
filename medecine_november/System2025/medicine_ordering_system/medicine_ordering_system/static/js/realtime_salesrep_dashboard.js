/**
 * Real-time Dashboard Updates for Sales Representative's "My Orders" Dashboard
 * Polls the API endpoint and updates dashboard statistics and order list in real-time
 */

class RealtimeSalesRepDashboard {
    constructor() {
        this.apiUrl = '/orders/api/sales-rep/dashboard/';
        this.pollInterval = 5000; // 5 seconds
        this.pollTimer = null;
        this.isPolling = false;
        
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
        // Check if we're on the sales rep order list page
        const dashboardElement = document.getElementById('sales-rep-orders-dashboard');
        if (!dashboardElement) {
            return; // Not on the sales rep dashboard page
        }
        
        // Initial fetch
        this.fetchDashboardData();
        
        // Start polling
        this.pollTimer = setInterval(() => this.fetchDashboardData(), this.pollInterval);
        
        // Re-fetch when window regains focus (e.g., tab switch)
        document.addEventListener('visibilitychange', () => {
            if (document.visibilityState === 'visible') {
                this.fetchDashboardData(); // Immediately check when page becomes visible
            }
        });
    }
    
    async fetchDashboardData() {
        if (this.isPolling) {
            return; // Prevent concurrent requests
        }
        
        try {
            this.isPolling = true;
            
            // Get current filter values from the page
            const statusFilter = document.getElementById('status')?.value || '';
            const dateFrom = document.getElementById('date_from')?.value || '';
            const dateTo = document.getElementById('date_to')?.value || '';
            const currentPage = this.getCurrentPage();
            
            // Build query string with filters
            const params = new URLSearchParams();
            if (statusFilter) params.append('status', statusFilter);
            if (dateFrom) params.append('date_from', dateFrom);
            if (dateTo) params.append('date_to', dateTo);
            if (currentPage > 1) params.append('page', currentPage);
            
            const url = this.apiUrl + (params.toString() ? '?' + params.toString() : '');
            
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
            
            // Update dashboard with new data
            this.updateDashboard(data);
            
        } catch (error) {
            console.error('Error fetching dashboard data:', error);
            // Silently fail - don't disturb user experience
        } finally {
            this.isPolling = false;
        }
    }
    
    getCurrentPage() {
        // Try to get current page from pagination
        const activePageLink = document.querySelector('.pagination .page-item.active .page-link');
        if (activePageLink) {
            const text = activePageLink.textContent.trim();
            const match = text.match(/Page (\d+)/);
            if (match) {
                return parseInt(match[1]);
            }
        }
        return 1;
    }
    
    updateDashboard(data) {
        if (!data || !data.statistics) {
            return;
        }
        
        // Update statistics cards
        this.updateStatisticsCards(data.statistics);
        
        // Update orders by status breakdown
        if (data.orders_by_status) {
            this.updateOrdersByStatus(data.orders_by_status);
        }
        
        // Update orders table - update individual rows to reflect status changes
        // This allows status updates even when filters are applied
        if (data.orders) {
            this.updateOrderRowsInPlace(data.orders);
        }
    }
    
    updateStatisticsCards(statistics) {
        // Update Total Orders
        const totalOrdersElement = document.getElementById('stat-total-orders');
        if (totalOrdersElement) {
            totalOrdersElement.textContent = statistics.total_orders || 0;
        }
        
        // Update Pending Orders
        const pendingOrdersElement = document.getElementById('stat-pending-orders');
        if (pendingOrdersElement) {
            pendingOrdersElement.textContent = statistics.pending_orders || 0;
        }
        
        // Update Processing Orders
        const processingOrdersElement = document.getElementById('stat-processing-orders');
        if (processingOrdersElement) {
            processingOrdersElement.textContent = statistics.processing_orders || 0;
        }
        
        // Update Delivered Orders
        const deliveredOrdersElement = document.getElementById('stat-delivered-orders');
        if (deliveredOrdersElement) {
            deliveredOrdersElement.textContent = statistics.delivered_orders || 0;
        }
        
        // Update Cancelled Orders
        const cancelledOrdersElement = document.getElementById('stat-cancelled-orders');
        if (cancelledOrdersElement) {
            cancelledOrdersElement.textContent = statistics.cancelled_orders || 0;
        }
        
        // Update Total Revenue
        const totalRevenueElement = document.getElementById('stat-total-revenue');
        if (totalRevenueElement && statistics.total_revenue !== undefined) {
            totalRevenueElement.textContent = '₱' + parseFloat(statistics.total_revenue).toFixed(2);
        }
    }
    
    updateOrdersByStatus(ordersByStatus) {
        // Update each status count in the breakdown
        for (const [statusCode, statusData] of Object.entries(ordersByStatus)) {
            const statusElement = document.getElementById(`status-count-${statusCode}`);
            if (statusElement) {
                statusElement.textContent = statusData.count || 0;
            }
        }
    }
    
    updateOrderRowsInPlace(orders) {
        const tbody = document.getElementById('orders-table-tbody');
        if (!tbody) {
            return;
        }
        
        // Create a map of orders by ID for quick lookup
        const ordersMap = {};
        orders.forEach(order => {
            ordersMap[order.id] = order;
        });
        
        // Update existing rows that match orders from the API
        const rows = tbody.querySelectorAll('tr');
        rows.forEach(row => {
            const orderLink = row.querySelector('a[href*="/orders/orders/"]');
            if (orderLink) {
                const href = orderLink.getAttribute('href');
                const match = href.match(/\/orders\/orders\/(\d+)/);
                if (match) {
                    const orderId = parseInt(match[1]);
                    const updatedOrder = ordersMap[orderId];
                    
                    if (updatedOrder) {
                        // Update the row with new status and payment status
                        this.updateOrderRow(row, updatedOrder);
                        // Remove from map so we know it's already updated
                        delete ordersMap[orderId];
                    }
                }
            }
        });
        
        // Note: We don't add new orders or remove orders here to avoid disrupting
        // the user's filtered/paginated view. Statistics cards already show the updated counts.
    }
    
    updateOrderRow(row, order) {
        // Update status badge
        const statusCell = row.cells[2]; // Status is in 3rd column (index 2)
        if (statusCell) {
            const statusBadgeClass = this.getStatusBadgeClass(order.status);
            statusCell.innerHTML = `
                <span class="badge bg-${statusBadgeClass}">
                    ${this.escapeHtml(order.status_display)}
                </span>
            `;
        }
        
        // Update payment status badge
        const paymentCell = row.cells[3]; // Payment status is in 4th column (index 3)
        if (paymentCell) {
            const paymentBadgeClass = this.getPaymentBadgeClass(order.payment_status);
            paymentCell.innerHTML = `
                <span class="badge bg-${paymentBadgeClass}">
                    ${this.escapeHtml(order.payment_status_display)}
                </span>
            `;
        }
        
        // Update action buttons based on order status
        const actionsCell = row.cells[6]; // Actions is in 7th column (index 6)
        if (actionsCell) {
            const isPending = order.status === 'pending';
            const editButtons = isPending ? `
                <a href="/orders/orders/${order.id}/edit/" class="btn btn-sm btn-outline-warning">
                    <i class="fas fa-edit"></i> Edit
                </a>
                <a href="/orders/orders/${order.id}/cancel/" class="btn btn-sm btn-outline-danger">
                    <i class="fas fa-times"></i> Cancel
                </a>
            ` : '';
            
            actionsCell.innerHTML = `
                <a href="/orders/orders/${order.id}/" class="btn btn-sm btn-outline-primary">
                    <i class="fas fa-eye"></i> View
                </a>
                ${editButtons}
            `;
        }
    }
    
    createOrderRow(order) {
        const row = document.createElement('tr');
        
        // Status badge color
        const statusBadgeClass = this.getStatusBadgeClass(order.status);
        const paymentBadgeClass = this.getPaymentBadgeClass(order.payment_status);
        
        // Check if order is pending to show edit/cancel buttons
        const isPending = order.status === 'pending';
        const editButtons = isPending ? `
            <a href="/orders/orders/${order.id}/edit/" class="btn btn-sm btn-outline-warning">
                <i class="fas fa-edit"></i> Edit
            </a>
            <a href="/orders/orders/${order.id}/cancel/" class="btn btn-sm btn-outline-danger">
                <i class="fas fa-times"></i> Cancel
            </a>
        ` : '';
        
        row.innerHTML = `
            <td>
                <a href="/orders/orders/${order.id}/" class="text-decoration-none">
                    #${order.id}
                </a>
            </td>
            <td>${order.created_at_display}</td>
            <td>
                <span class="badge bg-${statusBadgeClass}">
                    ${this.escapeHtml(order.status_display)}
                </span>
            </td>
            <td>
                <span class="badge bg-${paymentBadgeClass}">
                    ${this.escapeHtml(order.payment_status_display)}
                </span>
            </td>
            <td>${order.items_count} item${order.items_count !== 1 ? 's' : ''}</td>
            <td>₱${parseFloat(order.total_amount).toFixed(2)}</td>
            <td>
                <a href="/orders/orders/${order.id}/" class="btn btn-sm btn-outline-primary">
                    <i class="fas fa-eye"></i> View
                </a>
                ${editButtons}
            </td>
        `;
        
        return row;
    }
    
    getStatusBadgeClass(status) {
        const statusMap = {
            'pending': 'warning',
            'confirmed': 'info',
            'processing': 'info',
            'ready_for_pickup': 'success',
            'shipped': 'info',
            'delivered': 'dark',
            'cancelled': 'danger',
            'returned': 'warning'
        };
        return statusMap[status] || 'secondary';
    }
    
    getPaymentBadgeClass(paymentStatus) {
        const paymentMap = {
            'paid': 'success',
            'pending': 'warning',
            'failed': 'danger',
            'refunded': 'secondary',
            'partially_refunded': 'info'
        };
        return paymentMap[paymentStatus] || 'secondary';
    }
    
    escapeHtml(text) {
        const div = document.createElement('div');
        div.textContent = text;
        return div.innerHTML;
    }
    
    stop() {
        if (this.pollTimer) {
            clearInterval(this.pollTimer);
            this.pollTimer = null;
        }
    }
}

// Initialize real-time dashboard when script loads (only for sales reps)
if (document.getElementById('sales-rep-orders-dashboard')) {
    new RealtimeSalesRepDashboard();
}

