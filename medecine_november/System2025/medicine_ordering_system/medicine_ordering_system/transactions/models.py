from django.db import models
from django.core.validators import MinValueValidator
from decimal import Decimal


class PaymentMethod(models.Model):
    """
    Available payment methods
    """
    name = models.CharField(max_length=50, unique=True)
    description = models.TextField(blank=True)
    is_active = models.BooleanField(default=True)
    processing_fee_percentage = models.DecimalField(max_digits=5, decimal_places=2, default=Decimal('0.00'))
    processing_fee_fixed = models.DecimalField(max_digits=10, decimal_places=2, default=Decimal('0.00'))
    
    def __str__(self):
        return self.name


class PaymentGateway(models.Model):
    """
    Payment gateway configuration - allows admin to configure and switch between gateways
    """
    GATEWAY_TYPES = [
        ('stripe', 'Stripe'),
        ('paymongo', 'PayMongo'),
        ('paypal', 'PayPal'),
        ('square', 'Square'),
        ('dragonpay', 'DragonPay'),
        ('cash_on_delivery', 'Cash on Delivery'),
    ]
    
    name = models.CharField(max_length=50, unique=True)
    gateway_type = models.CharField(max_length=50, choices=GATEWAY_TYPES)
    is_active = models.BooleanField(default=False, help_text='Only one gateway can be active at a time')
    is_test_mode = models.BooleanField(default=True, help_text='Use test/sandbox environment')
    
    # API Credentials (stored encrypted in production - using plain text for now)
    api_key_public = models.CharField(max_length=255, blank=True, help_text='Public/Test API Key')
    api_key_secret = models.CharField(max_length=255, blank=True, help_text='Secret/Private API Key')
    webhook_secret = models.CharField(max_length=255, blank=True, help_text='Webhook signing secret')
    
    # Additional configuration (JSON)
    config = models.JSONField(default=dict, blank=True, help_text='Additional gateway-specific configuration')
    
    # Metadata
    description = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    created_by = models.ForeignKey('accounts.User', on_delete=models.SET_NULL, null=True, blank=True, related_name='created_gateways')
    
    class Meta:
        ordering = ['-is_active', 'name']
        verbose_name = 'Payment Gateway'
        verbose_name_plural = 'Payment Gateways'
    
    def __str__(self):
        status = "Active" if self.is_active else "Inactive"
        mode = "Test" if self.is_test_mode else "Live"
        return f"{self.get_gateway_type_display()} - {status} ({mode})"
    
    def save(self, *args, **kwargs):
        # Ensure only one gateway is active at a time
        if self.is_active:
            PaymentGateway.objects.filter(is_active=True).exclude(pk=self.pk).update(is_active=False)
        super().save(*args, **kwargs)
    
    @property
    def is_configured(self):
        """Check if gateway has required credentials"""
        if self.gateway_type == 'cash_on_delivery':
            return True  # COD doesn't need API keys
        return bool(self.api_key_secret)
    
    @property
    def display_name(self):
        """Get display name for the gateway"""
        return self.get_gateway_type_display()


class Transaction(models.Model):
    """
    Payment transactions
    """
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('processing', 'Processing'),
        ('completed', 'Completed'),
        ('failed', 'Failed'),
        ('cancelled', 'Cancelled'),
        ('refunded', 'Refunded'),
    ]
    
    TRANSACTION_TYPES = [
        ('payment', 'Payment'),
        ('refund', 'Refund'),
        ('partial_refund', 'Partial Refund'),
    ]
    
    transaction_id = models.CharField(max_length=50, unique=True)
    order = models.ForeignKey('orders.Order', on_delete=models.CASCADE, related_name='transactions')
    payment_method = models.ForeignKey(PaymentMethod, on_delete=models.CASCADE)
    payment_gateway = models.ForeignKey(PaymentGateway, on_delete=models.SET_NULL, null=True, blank=True, related_name='transactions')
    
    # Transaction details
    transaction_type = models.CharField(max_length=20, choices=TRANSACTION_TYPES, default='payment')
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    
    # Amounts
    amount = models.DecimalField(max_digits=10, decimal_places=2, validators=[MinValueValidator(Decimal('0.01'))])
    processing_fee = models.DecimalField(max_digits=10, decimal_places=2, default=Decimal('0.00'))
    net_amount = models.DecimalField(max_digits=10, decimal_places=2, validators=[MinValueValidator(Decimal('0.00'))])
    
    # External payment gateway details
    gateway_transaction_id = models.CharField(max_length=100, blank=True)
    gateway_response = models.JSONField(null=True, blank=True)
    
    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True)
    processed_at = models.DateTimeField(null=True, blank=True)
    completed_at = models.DateTimeField(null=True, blank=True)
    
    # Additional information
    notes = models.TextField(blank=True)
    failure_reason = models.TextField(blank=True)
    
    class Meta:
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['transaction_id']),
            models.Index(fields=['order', 'status']),
            models.Index(fields=['status', 'created_at']),
        ]
    
    def __str__(self):
        return f"Transaction {self.transaction_id} - {self.order.order_number}"
    
    def save(self, *args, **kwargs):
        if not self.transaction_id:
            self.transaction_id = self.generate_transaction_id()
        self.net_amount = self.amount - self.processing_fee
        super().save(*args, **kwargs)
    
    def generate_transaction_id(self):
        import uuid
        return f"TXN-{uuid.uuid4().hex[:12].upper()}"
    
    @property
    def is_successful(self):
        return self.status == 'completed'


class Refund(models.Model):
    """
    Refund transactions
    """
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('approved', 'Approved'),
        ('processed', 'Processed'),
        ('rejected', 'Rejected'),
    ]
    
    refund_id = models.CharField(max_length=50, unique=True)
    transaction = models.ForeignKey(Transaction, on_delete=models.CASCADE, related_name='refunds')
    order = models.ForeignKey('orders.Order', on_delete=models.CASCADE, related_name='refunds')
    
    # Refund details
    amount = models.DecimalField(max_digits=10, decimal_places=2, validators=[MinValueValidator(Decimal('0.01'))])
    reason = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    
    # Processing
    requested_by = models.ForeignKey('accounts.User', on_delete=models.CASCADE, related_name='requested_refunds')
    approved_by = models.ForeignKey('accounts.User', on_delete=models.SET_NULL, null=True, blank=True, related_name='approved_refunds')
    processed_by = models.ForeignKey('accounts.User', on_delete=models.SET_NULL, null=True, blank=True, related_name='processed_refunds')
    
    # Timestamps
    requested_at = models.DateTimeField(auto_now_add=True)
    approved_at = models.DateTimeField(null=True, blank=True)
    processed_at = models.DateTimeField(null=True, blank=True)
    
    # External gateway details
    gateway_refund_id = models.CharField(max_length=100, blank=True)
    gateway_response = models.JSONField(null=True, blank=True)
    
    class Meta:
        ordering = ['-requested_at']
    
    def __str__(self):
        return f"Refund {self.refund_id} - {self.order.order_number}"
    
    def save(self, *args, **kwargs):
        if not self.refund_id:
            self.refund_id = self.generate_refund_id()
        super().save(*args, **kwargs)
    
    def generate_refund_id(self):
        import uuid
        return f"REF-{uuid.uuid4().hex[:12].upper()}"


class SalesReport(models.Model):
    """
    Daily/Weekly/Monthly sales reports
    """
    PERIOD_CHOICES = [
        ('daily', 'Daily'),
        ('weekly', 'Weekly'),
        ('monthly', 'Monthly'),
        ('yearly', 'Yearly'),
    ]
    
    period_type = models.CharField(max_length=10, choices=PERIOD_CHOICES)
    period_start = models.DateField()
    period_end = models.DateField()
    
    # Sales metrics
    total_orders = models.PositiveIntegerField(default=0)
    total_revenue = models.DecimalField(max_digits=12, decimal_places=2, default=Decimal('0.00'))
    total_transactions = models.PositiveIntegerField(default=0)
    total_refunds = models.DecimalField(max_digits=12, decimal_places=2, default=Decimal('0.00'))
    net_revenue = models.DecimalField(max_digits=12, decimal_places=2, default=Decimal('0.00'))
    
    # Payment method breakdown
    cash_orders = models.PositiveIntegerField(default=0)
    card_orders = models.PositiveIntegerField(default=0)
    online_orders = models.PositiveIntegerField(default=0)
    
    # Additional metrics
    average_order_value = models.DecimalField(max_digits=10, decimal_places=2, default=Decimal('0.00'))
    new_customers = models.PositiveIntegerField(default=0)
    returning_customers = models.PositiveIntegerField(default=0)
    
    # Timestamps
    generated_at = models.DateTimeField(auto_now_add=True)
    generated_by = models.ForeignKey('accounts.User', on_delete=models.SET_NULL, null=True, blank=True)
    
    class Meta:
        unique_together = ['period_type', 'period_start', 'period_end']
        ordering = ['-period_start']
    
    def __str__(self):
        return f"{self.period_type.title()} Report - {self.period_start} to {self.period_end}"
