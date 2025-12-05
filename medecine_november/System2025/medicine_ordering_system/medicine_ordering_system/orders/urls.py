from django.urls import path, include
from . import views

app_name = 'orders'

urlpatterns = [
    # Dashboard
    path('', views.OrderDashboardView.as_view(), name='dashboard'),
    
    # Order management
    path('orders/', views.OrderListView.as_view(), name='order_list'),
    path('orders/create/', views.OrderCreateView.as_view(), name='order_create'),
    path('orders/<int:pk>/', views.OrderDetailView.as_view(), name='order_detail'),
    path('orders/<int:pk>/edit/', views.OrderEditView.as_view(), name='order_edit'),
    path('orders/<int:pk>/cancel/', views.OrderCancelView.as_view(), name='order_cancel'),
    
    # Cart management
    path('cart/', views.CartView.as_view(), name='cart'),
    path('cart/add/', views.CartAddView.as_view(), name='cart_add'),
    path('cart/remove/', views.CartRemoveView.as_view(), name='cart_remove'),
    path('cart/update/', views.CartUpdateView.as_view(), name='cart_update'),
    path('cart/clear/', views.CartClearView.as_view(), name='cart_clear'),
    
    # Order status management
    path('orders/<int:pk>/status/', views.OrderStatusUpdateView.as_view(), name='order_status_update'),
    path('orders/<int:pk>/prescription/', views.PrescriptionUploadView.as_view(), name='prescription_upload'),
    path('orders/<int:pk>/prescription/verify/', views.PrescriptionVerifyView.as_view(), name='prescription_verify'),
    
    # Pharmacist/Admin Order Management URLs
    path('pharmacist/dashboard/', views.OrderFulfillmentDashboardView.as_view(), name='pharmacist_dashboard'),
    path('pharmacist/orders/', views.PharmacistOrderListView.as_view(), name='pharmacist_order_list'),
    path('pharmacist/orders/<int:pk>/', views.PharmacistOrderDetailView.as_view(), name='pharmacist_order_detail'),
    
    # API endpoints
    path('api/orders/', views.OrderListAPIView.as_view(), name='api_order_list'),
    path('api/orders/<int:pk>/', views.OrderDetailAPIView.as_view(), name='api_order_detail'),
    path('api/cart/', views.CartAPIView.as_view(), name='api_cart'),
    path('api/cart/add/', views.CartAddAPIView.as_view(), name='api_cart_add'),
    path('api/cart/remove/', views.CartRemoveAPIView.as_view(), name='api_cart_remove'),
    path('api/cart/update/', views.CartUpdateAPIView.as_view(), name='api_cart_update'),
    path('api/pharmacist/dashboard/', views.PharmacistDashboardAPIView.as_view(), name='api_pharmacist_dashboard'),
    path('api/sales-rep/dashboard/', views.SalesRepDashboardAPIView.as_view(), name='api_sales_rep_dashboard'),
    
    # Payment endpoints
    path('api/create-payment-intent/<int:order_id>/', views.CreatePaymentIntentView.as_view(), name='create_payment_intent'),
    path('api/process-payment/<int:order_id>/', views.ProcessPaymentView.as_view(), name='process_payment'),
    path('orders/<int:order_id>/manual-payment/', views.ManualPaymentSubmitView.as_view(), name='manual_payment_submit'),
    
    # Payment verification endpoints (Pharmacist/Admin)
    path('orders/<int:order_id>/verify-gateway-payment/', views.VerifyGatewayPaymentView.as_view(), name='verify_gateway_payment'),
    path('orders/<int:order_id>/verify-manual-payment/', views.VerifyManualPaymentView.as_view(), name='verify_manual_payment'),
    
    # Payment details page (Pharmacist/Admin)
    path('pharmacist/orders/<int:pk>/payment-details/', views.PaymentDetailsView.as_view(), name='payment_details'),
]
