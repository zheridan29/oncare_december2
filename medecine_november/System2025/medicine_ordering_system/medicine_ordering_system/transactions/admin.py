from django.contrib import admin
from django.utils.html import format_html
from django.urls import reverse
from django.contrib import messages
from .models import PaymentMethod, PaymentGateway, Transaction, Refund, SalesReport


@admin.register(PaymentMethod)
class PaymentMethodAdmin(admin.ModelAdmin):
    list_display = ('name', 'description', 'is_active', 'processing_fee_percentage', 'processing_fee_fixed')
    list_filter = ('is_active',)
    search_fields = ('name', 'description')


@admin.register(PaymentGateway)
class PaymentGatewayAdmin(admin.ModelAdmin):
    list_display = ('name', 'gateway_type', 'status_display', 'mode_display', 'is_configured_display', 'created_at', 'updated_at')
    list_filter = ('gateway_type', 'is_active', 'is_test_mode')
    search_fields = ('name', 'gateway_type')
    readonly_fields = ('created_at', 'updated_at', 'created_by')
    
    fieldsets = (
        ('Basic Information', {
            'fields': ('name', 'gateway_type', 'description')
        }),
        ('Status', {
            'fields': ('is_active', 'is_test_mode')
        }),
        ('API Credentials', {
            'fields': ('api_key_public', 'api_key_secret', 'webhook_secret'),
            'description': 'Enter your API keys. For test mode, use test keys. For live mode, use live keys.'
        }),
        ('Additional Configuration', {
            'fields': ('config',),
            'description': 'Additional gateway-specific configuration in JSON format'
        }),
        ('Metadata', {
            'fields': ('created_at', 'updated_at', 'created_by'),
            'classes': ('collapse',)
        }),
    )
    
    def status_display(self, obj):
        if obj.is_active:
            return format_html('<span style="color: green; font-weight: bold;">● Active</span>')
        else:
            return format_html('<span style="color: gray;">○ Inactive</span>')
    status_display.short_description = 'Status'
    
    def mode_display(self, obj):
        if obj.is_test_mode:
            return format_html('<span style="color: orange;">TEST MODE</span>')
        else:
            return format_html('<span style="color: red; font-weight: bold;">LIVE MODE</span>')
    mode_display.short_description = 'Mode'
    
    def is_configured_display(self, obj):
        if obj.is_configured:
            return format_html('<span style="color: green;">✓ Configured</span>')
        else:
            return format_html('<span style="color: red;">✗ Not Configured</span>')
    is_configured_display.short_description = 'Configuration'
    
    def save_model(self, request, obj, form, change):
        if not change:  # If creating new object
            obj.created_by = request.user
        super().save_model(request, obj, form, change)
        
        # Show warning if switching to live mode
        if obj.is_active and not obj.is_test_mode:
            messages.warning(request, f'⚠️ Warning: {obj.name} is now in LIVE mode. Real transactions will be processed!')
        
        # Show info if gateway is not configured
        if obj.is_active and not obj.is_configured:
            messages.warning(request, f'⚠️ Warning: {obj.name} is not properly configured. Please add API credentials.')
    
    actions = ['activate_gateway', 'deactivate_gateway']
    
    def activate_gateway(self, request, queryset):
        """Activate selected gateway (deactivates others)"""
        if queryset.count() > 1:
            self.message_user(request, 'Please select only one gateway to activate.', messages.WARNING)
            return
        
        gateway = queryset.first()
        gateway.is_active = True
        gateway.save()
        
        self.message_user(
            request,
            f'{gateway.name} has been activated. Other gateways have been deactivated.',
            messages.SUCCESS
        )
    activate_gateway.short_description = 'Activate selected gateway'
    
    def deactivate_gateway(self, request, queryset):
        """Deactivate selected gateways"""
        updated = queryset.update(is_active=False)
        self.message_user(
            request,
            f'{updated} gateway(s) deactivated.',
            messages.SUCCESS
        )
    deactivate_gateway.short_description = 'Deactivate selected gateways'


@admin.register(Transaction)
class TransactionAdmin(admin.ModelAdmin):
    list_display = ('transaction_id', 'order_link', 'payment_method', 'payment_gateway', 'status', 'amount', 'created_at')
    list_filter = ('status', 'transaction_type', 'payment_method', 'payment_gateway', 'created_at')
    search_fields = ('transaction_id', 'order__order_number', 'gateway_transaction_id')
    readonly_fields = ('transaction_id', 'created_at', 'processed_at', 'completed_at')
    
    fieldsets = (
        ('Transaction Information', {
            'fields': ('transaction_id', 'order', 'payment_method', 'payment_gateway', 'transaction_type', 'status')
        }),
        ('Amounts', {
            'fields': ('amount', 'processing_fee', 'net_amount')
        }),
        ('Gateway Details', {
            'fields': ('gateway_transaction_id', 'gateway_response')
        }),
        ('Timestamps', {
            'fields': ('created_at', 'processed_at', 'completed_at')
        }),
        ('Additional Information', {
            'fields': ('notes', 'failure_reason')
        }),
    )
    
    def order_link(self, obj):
        if obj.order:
            url = reverse('admin:orders_order_change', args=[obj.order.pk])
            return format_html('<a href="{}">{}</a>', url, obj.order.order_number)
        return '-'
    order_link.short_description = 'Order'


@admin.register(Refund)
class RefundAdmin(admin.ModelAdmin):
    list_display = ('refund_id', 'transaction_link', 'order_link', 'amount', 'status', 'requested_at')
    list_filter = ('status', 'requested_at')
    search_fields = ('refund_id', 'transaction__transaction_id', 'order__order_number')
    readonly_fields = ('refund_id', 'requested_at', 'approved_at', 'processed_at')
    
    def transaction_link(self, obj):
        if obj.transaction:
            url = reverse('admin:transactions_transaction_change', args=[obj.transaction.pk])
            return format_html('<a href="{}">{}</a>', url, obj.transaction.transaction_id)
        return '-'
    transaction_link.short_description = 'Transaction'
    
    def order_link(self, obj):
        if obj.order:
            url = reverse('admin:orders_order_change', args=[obj.order.pk])
            return format_html('<a href="{}">{}</a>', url, obj.order.order_number)
        return '-'
    order_link.short_description = 'Order'


@admin.register(SalesReport)
class SalesReportAdmin(admin.ModelAdmin):
    list_display = ('period_type', 'period_start', 'period_end', 'total_revenue', 'total_orders', 'generated_at')
    list_filter = ('period_type', 'generated_at')
    readonly_fields = ('generated_at', 'generated_by')
    date_hierarchy = 'period_start'
