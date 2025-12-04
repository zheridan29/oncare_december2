from django.contrib import admin
from django.db.models import Q, F
from django.utils.html import format_html
from django.urls import reverse
from django.contrib import messages
from .models import Medicine, Category, Manufacturer, StockMovement, ReorderAlert, MedicineImage


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'parent_category', 'is_active', 'created_at']
    list_filter = ['is_active', 'created_at']
    search_fields = ['name', 'description']
    ordering = ['name']


@admin.register(Manufacturer)
class ManufacturerAdmin(admin.ModelAdmin):
    list_display = ['name', 'country', 'contact_email', 'is_active', 'created_at']
    list_filter = ['is_active', 'country', 'created_at']
    search_fields = ['name', 'country', 'contact_email']


@admin.register(StockMovement)
class StockMovementAdmin(admin.ModelAdmin):
    list_display = ['medicine', 'movement_type', 'quantity', 'created_by', 'created_at']
    list_filter = ['movement_type', 'created_at']
    search_fields = ['medicine__name', 'reference_number']
    readonly_fields = ['created_at']
    date_hierarchy = 'created_at'


@admin.register(ReorderAlert)
class ReorderAlertAdmin(admin.ModelAdmin):
    list_display = ['medicine', 'current_stock', 'reorder_point', 'priority', 'is_processed', 'created_at']
    list_filter = ['is_processed', 'priority', 'created_at']
    search_fields = ['medicine__name']
    readonly_fields = ['created_at', 'processed_at']
    actions = ['mark_as_processed']
    
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


@admin.register(MedicineImage)
class MedicineImageAdmin(admin.ModelAdmin):
    list_display = ['medicine', 'is_primary', 'created_at']
    list_filter = ['is_primary', 'created_at']
    search_fields = ['medicine__name']


@admin.register(Medicine)
class MedicineAdmin(admin.ModelAdmin):
    list_display = [
        'name', 'category', 'current_stock', 'reorder_point', 'stock_status_badge',
        'unit_price', 'is_active', 'is_available'
    ]
    list_filter = ['is_active', 'is_available', 'category', 'prescription_type']
    search_fields = ['name', 'generic_name', 'ndc_number']
    readonly_fields = ['created_at', 'updated_at', 'stock_status_badge']
    
    fieldsets = (
        ('Basic Information', {
            'fields': ('name', 'generic_name', 'description', 'category', 'manufacturer')
        }),
        ('Medicine Details', {
            'fields': ('dosage_form', 'strength', 'prescription_type', 'requires_prescription')
        }),
        ('Pricing', {
            'fields': ('unit_price', 'cost_price')
        }),
        ('Inventory Management', {
            'fields': (
                'current_stock', 
                'minimum_stock_level', 
                'maximum_stock_level', 
                'reorder_point',
                'stock_status_badge'
            ),
            'description': 'Set stock levels manually. Low stock alerts will be triggered when current_stock <= reorder_point'
        }),
        ('Physical Attributes', {
            'fields': ('weight', 'dimensions', 'storage_conditions')
        }),
        ('Regulatory', {
            'fields': ('ndc_number', 'fda_approval_date', 'expiry_date')
        }),
        ('Status', {
            'fields': ('is_active', 'is_available')
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
    
    actions = ['check_and_notify_low_stock', 'set_default_reorder_points']
    
    def stock_status_badge(self, obj):
        """Display stock status with color coding"""
        if obj.is_out_of_stock:
            color = 'red'
            status = 'Out of Stock'
        elif obj.is_low_stock:
            color = 'orange'
            status = 'Low Stock'
        else:
            color = 'green'
            status = 'In Stock'
        
        return format_html(
            '<span style="color: {}; font-weight: bold;">{}</span>',
            color, status
        )
    stock_status_badge.short_description = 'Stock Status'
    
    def check_and_notify_low_stock(self, request, queryset):
        """Check selected medicines and send low stock notifications"""
        from common.services import NotificationService
        
        notified_count = 0
        for medicine in queryset:
            if medicine.current_stock <= medicine.reorder_point:
                NotificationService.notify_low_stock(medicine, medicine.current_stock)
                notified_count += 1
        
        self.message_user(
            request,
            f'Low stock notifications sent for {notified_count} medicine(s).',
            messages.SUCCESS
        )
    check_and_notify_low_stock.short_description = 'Check and notify low stock'
    
    def set_default_reorder_points(self, request, queryset):
        """Set default reorder points based on minimum stock levels"""
        updated = queryset.update(reorder_point=F('minimum_stock_level'))
        self.message_user(
            request,
            f'Reorder points set to minimum stock levels for {updated} medicine(s).',
            messages.SUCCESS
        )
    set_default_reorder_points.short_description = 'Set reorder points to minimum stock levels'
