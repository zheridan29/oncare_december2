# Payment Integration Implementation Plan

## Overview
Add payment functionality to sales representative order pages with two payment modes:
1. **Payment Gateway** (Stripe) - Online payment
2. **Manual Payment** - Show OnCare payment details only when order status is "confirmed"

## Implementation Steps

### 1. Store Manual Payment Details
- Use SystemConfiguration model to store bank account details
- Keys: `payment_bank_name`, `payment_account_number`, `payment_account_name`, etc.

### 2. Create Payment Views
- `OrderPaymentView` - Display payment options
- `CreatePaymentIntentView` - Create Stripe payment intent
- `ProcessPaymentView` - Handle payment processing
- `ManualPaymentSubmitView` - Submit manual payment proof

### 3. Update Order Detail View
- Add payment context (gateway availability, manual payment details)
- Check order status for showing manual payment option

### 4. Update Order Detail Template
- Add payment section for sales reps
- Show payment gateway option (Stripe)
- Show manual payment details only when status is "confirmed"
- Add payment processing forms

### 5. Create Payment Forms
- Payment method selection form
- Manual payment submission form

### 6. Add JavaScript
- Stripe.js integration
- Payment processing UI

### 7. Add URL Routes
- Payment endpoints in orders/urls.py

## Features

### Payment Gateway Flow
1. User selects "Pay Online"
2. System creates payment intent
3. User enters card details (Stripe.js)
4. Payment processed
5. Order payment status updated

### Manual Payment Flow
1. Order must be "confirmed" status
2. System displays OnCare payment details
3. User makes bank transfer/payment
4. User uploads proof of payment
5. Admin verifies and updates payment status

