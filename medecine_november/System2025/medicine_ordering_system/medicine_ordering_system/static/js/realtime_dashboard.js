/**
 * Real-time Dashboard Updates for Pharmacist/Admin Order Fulfillment Dashboard
 * Polls the API endpoint and updates dashboard statistics in real-time
 */

class RealtimeDashboard {
    constructor() {
        this.apiUrl = '/orders/api/pharmacist/dashboard/';
        this.pollInterval = 5000; // 5 seconds
        this.pollTimer = null;
        this.lastCheckTime = null;
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
        // Check if we're on the pharmacist dashboard page
        const dashboardElement = document.getElementById('pharmacist-dashboard');
        if (!dashboardElement) {
            return; // Not on the dashboard page
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
            
            const response = await fetch(this.apiUrl, {
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
        
        // Update recent orders table
        if (data.recent_orders) {
            this.updateRecentOrders(data.recent_orders);
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
        
        // Update Ready Orders
        const readyOrdersElement = document.getElementById('stat-ready-orders');
        if (readyOrdersElement) {
            readyOrdersElement.textContent = statistics.ready_orders || 0;
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
    
    updateRecentOrders(recentOrders) {
        const tbody = document.getElementById('recent-orders-tbody');
        if (!tbody) {
            return;
        }
        
        // Clear existing rows
        tbody.innerHTML = '';
        
        if (recentOrders.length === 0) {
            tbody.innerHTML = `
                <tr>
                    <td colspan="7" class="text-center py-4">
                        <i class="fas fa-inbox fa-3x text-muted mb-3"></i>
                        <p class="text-muted">No orders found</p>
                    </td>
                </tr>
            `;
            return;
        }
        
        // Build new rows
        recentOrders.forEach(order => {
            const row = this.createOrderRow(order);
            tbody.appendChild(row);
        });
    }
    
    createOrderRow(order) {
        const row = document.createElement('tr');
        
        // Status badge color
        const statusBadgeClass = this.getStatusBadgeClass(order.status);
        const paymentBadgeClass = this.getPaymentBadgeClass(order.payment_status);
        
        row.innerHTML = `
            <td>
                <a href="/orders/pharmacist/orders/${order.id}/" class="text-decoration-none">
                    ${order.order_number}
                </a>
            </td>
            <td>${this.escapeHtml(order.customer_name)}</td>
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
            <td>₱${parseFloat(order.total_amount).toFixed(2)}</td>
            <td>${order.created_at_display}</td>
            <td>
                <a href="/orders/pharmacist/orders/${order.id}/" class="btn btn-sm btn-outline-primary">
                    <i class="fas fa-eye"></i> View
                </a>
                <a href="/orders/orders/${order.id}/status/" class="btn btn-sm btn-outline-warning">
                    <i class="fas fa-edit"></i> Update
                </a>
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

// Initialize real-time dashboard when script loads
if (document.getElementById('pharmacist-dashboard')) {
    new RealtimeDashboard();
}


