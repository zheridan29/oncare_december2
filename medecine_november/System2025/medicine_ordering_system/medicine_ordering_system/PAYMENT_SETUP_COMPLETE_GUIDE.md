# Complete Payment Integration Setup Guide

## Overview

This guide explains how to set up and configure the payment system for sales representatives, including both payment gateway (Stripe) and manual payment options.

---

## ✅ Implementation Status

All payment components have been implemented:

1. ✅ **Payment Utilities** (`orders/payment_utils.py`)
2. ✅ **Payment Views** (`orders/views.py`)
3. ✅ **Payment Forms** (`orders/forms.py`)
4. ✅ **Payment Templates** (`templates/orders/order_detail.html`)
5. ✅ **Stripe JavaScript** (`static/js/stripe_payment.js`)
6. ✅ **URL Routes** (`orders/urls.py`)

---

## 🔧 Setup Steps

### Step 1: Configure Manual Payment Details

Manual payment details are stored in SystemConfiguration. Set them up in Django Admin:

1. **Go to Django Admin**: http://127.0.0.1:8000/admin/
2. **Navigate to**: Common → System Configurations
3. **Add the following configurations**:

#### Configuration Entries to Create:

1. **Bank Name**
   - **Key**: `payment_bank_name`
   - **Value**: `OnCare Bank` (or your actual bank name)
   - **Config Type**: `payments`
   - **Data Type**: `string`

2. **Account Name**
   - **Key**: `payment_account_name`
   - **Value**: `OnCare Medicine Ordering System` (or your account name)
   - **Config Type**: `payments`
   - **Data Type**: `string`

3. **Account Number**
   - **Key**: `payment_account_number`
   - **Value**: Your bank account number (e.g., `1234567890`)
   - **Config Type**: `payments`
   - **Data Type**: `string`

4. **SWIFT Code** (Optional)
   - **Key**: `payment_swift_code`
   - **Value**: Your bank's SWIFT code
   - **Config Type**: `payments`
   - **Data Type**: `string`

5. **Payment Instructions**
   - **Key**: `payment_instructions`
   - **Value**: `Please include your order number in the payment reference.`
   - **Config Type**: `payments`
   - **Data Type**: `string`

### Step 2: Verify Payment Gateway Configuration

1. **Check Payment Gateway** in Admin:
   - Go to: Transactions → Payment Gateways
   - Verify one gateway is **Active** and **Configured**
   - Make sure it's in **Test Mode** for testing

2. **Test Payment Gateway**:
   ```bash
   python test_payment_gateway.py
   ```

### Step 3: Test the Payment System

1. **Create a Test Order**:
   - Log in as a sales representative
   - Create an order
   - Note the order ID

2. **Test Online Payment**:
   - Go to order detail page
   - Click "Pay Online" button
   - Use Stripe test card: `4242 4242 4242 4242`
   - Complete payment

3. **Test Manual Payment**:
   - Have admin confirm the order (change status to "confirmed")
   - Go to order detail page
   - Verify manual payment details are shown
   - Submit manual payment information

---

## 📋 How It Works

### Payment Gateway Flow (Online Payment)

1. **Sales Rep views order** → Sees "Pay Online" button
2. **Clicks button** → System creates payment intent
3. **Enters card details** → Stripe.js securely handles card input
4. **Submits payment** → Payment processed via Stripe
5. **Payment confirmed** → Order payment status updated to "paid"
6. **Notification sent** → Sales rep receives payment confirmation

### Manual Payment Flow (Bank Transfer)

1. **Order confirmed** → Pharmacist/admin confirms the order
2. **Sales Rep views order** → Sees "Manual Payment" section
3. **Views payment details** → OnCare bank account information displayed
4. **Makes bank transfer** → Sales rep transfers money to OnCare account
5. **Submits payment info** → Sales rep provides payment reference/proof
6. **Admin verifies** → Admin checks payment and updates status to "paid"
7. **Notification sent** → Sales rep receives payment confirmation

---

## 🎯 Features

### For Sales Representatives:

✅ **Pay Online** - Secure credit/debit card payment via Stripe  
✅ **Manual Payment** - Bank transfer option with payment details  
✅ **Payment Proof Upload** - Upload payment receipt/screenshot  
✅ **Payment Status Tracking** - See payment status on order page  
✅ **Notifications** - Receive payment confirmations  

### For Admin/Pharmacist:

✅ **Manual Payment Verification** - Review submitted payment proofs  
✅ **Payment Status Update** - Manually update payment status  
✅ **Payment Notifications** - Get notified of payment submissions  

---

## 🔍 Payment Details Display Logic

### Payment Gateway Option Shows When:
- ✅ Payment gateway is configured and active
- ✅ Order payment status is "pending"
- ✅ Order status is not "cancelled"

### Manual Payment Details Show When:
- ✅ Order status is "confirmed"
- ✅ Order payment status is "pending"

---

## 📝 System Configuration Keys

Use these keys in SystemConfiguration for manual payment details:

| Key | Description | Example Value |
|-----|-------------|---------------|
| `payment_bank_name` | Bank name | `OnCare Bank` |
| `payment_account_name` | Account holder name | `OnCare Medicine Ordering System` |
| `payment_account_number` | Bank account number | `1234567890` |
| `payment_swift_code` | SWIFT/BIC code (optional) | `ONCBUS33` |
| `payment_instructions` | Payment instructions | `Please include order number in reference` |

---

## 🧪 Testing

### Test Online Payment:

1. **Create an order** as sales rep
2. **Go to order detail page**
3. **Click "Pay Online"**
4. **Use test card**:
   - Card: `4242 4242 4242 4242`
   - Expiry: Any future date
   - CVC: Any 3 digits
   - ZIP: Any 5 digits
5. **Complete payment**
6. **Verify** payment status updates to "paid"

### Test Manual Payment:

1. **Create an order** as sales rep
2. **Admin confirms order** (changes status to "confirmed")
3. **Sales rep views order detail**
4. **Verify** manual payment details are displayed
5. **Submit payment information**
6. **Admin verifies** and updates payment status

---

## 🔗 URLs

### Payment Endpoints:

- **Create Payment Intent**: `/orders/api/create-payment-intent/<order_id>/`
- **Process Payment**: `/orders/api/process-payment/<order_id>/`
- **Submit Manual Payment**: `/orders/orders/<order_id>/manual-payment/`

---

## ⚠️ Important Notes

1. **Currency Conversion**: Stripe doesn't support PHP directly, so payments are converted to USD. The conversion rate can be configured in `payment_utils.py`.

2. **Test Mode**: Make sure payment gateway is in **Test Mode** when testing.

3. **Manual Payment**: Only available when order status is **"confirmed"**.

4. **Payment Details**: Configure in Django Admin → Common → System Configurations.

---

## 🐛 Troubleshooting

### Issue: "Payment gateway not available"

**Solution**:
- Check Payment Gateway is active in Admin
- Verify API keys are configured
- Test gateway with `test_payment_gateway.py`

### Issue: "Manual payment details not showing"

**Solution**:
- Verify order status is "confirmed"
- Check SystemConfiguration entries exist
- Verify keys start with `payment_`

### Issue: "Stripe payment not working"

**Solution**:
- Check browser console for errors
- Verify Stripe.js is loading
- Check public key is correct
- Verify payment gateway is in test mode

---

## 📚 Next Steps

After setup:

1. ✅ Configure manual payment details in SystemConfiguration
2. ✅ Test payment gateway with test cards
3. ✅ Test manual payment flow
4. ✅ Train sales representatives on payment process
5. ✅ Set up webhooks for automatic payment confirmations (optional)

---

## 🎉 Setup Complete!

Your payment system is now fully integrated! Sales representatives can:
- Pay online using credit/debit cards
- Use manual bank transfer with payment details
- Submit payment proofs
- Track payment status

**Happy Payments!** 💳💰

