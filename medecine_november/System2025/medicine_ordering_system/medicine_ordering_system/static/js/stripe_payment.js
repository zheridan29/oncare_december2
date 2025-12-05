/**
 * Stripe Payment Integration for Order Payments
 */
class StripePaymentHandler {
    constructor() {
        this.stripe = null;
        this.elements = null;
        this.cardElement = null;
        this.paymentIntentId = null;
        this.clientSecret = null;
        this.orderId = null;
        
        // Initialize Stripe if public key is available
        this.initStripe();
    }
    
    initStripe() {
        // Get Stripe public key from page data
        const stripePublicKey = document.getElementById('stripe-public-key')?.dataset.publicKey;
        
        if (stripePublicKey && stripePublicKey !== 'None' && stripePublicKey !== '') {
            // Load Stripe.js
            if (typeof Stripe === 'undefined') {
                const script = document.createElement('script');
                script.src = 'https://js.stripe.com/v3/';
                script.onload = () => this.setupStripe(stripePublicKey);
                document.head.appendChild(script);
            } else {
                this.setupStripe(stripePublicKey);
            }
        }
    }
    
    setupStripe(publicKey) {
        try {
            this.stripe = Stripe(publicKey);
            console.log('Stripe initialized successfully');
        } catch (error) {
            console.error('Error initializing Stripe:', error);
        }
    }
    
    async createPaymentIntent(orderId) {
        try {
            const response = await fetch(`/orders/api/create-payment-intent/${orderId}/`, {
                method: 'POST',
                headers: {
                    'X-CSRFToken': this.getCsrfToken(),
                    'Content-Type': 'application/json',
                },
                credentials: 'same-origin'
            });
            
            if (!response.ok) {
                const error = await response.json();
                throw new Error(error.error || 'Failed to create payment intent');
            }
            
            const data = await response.json();
            
            if (data.success) {
                this.paymentIntentId = data.payment_intent_id;
                this.clientSecret = data.client_secret;
                this.orderId = orderId;
                return data;
            } else {
                throw new Error(data.error || 'Failed to create payment intent');
            }
        } catch (error) {
            console.error('Error creating payment intent:', error);
            throw error;
        }
    }
    
    async setupPaymentForm(orderId) {
        try {
            // Create payment intent
            const paymentData = await this.createPaymentIntent(orderId);
            
            if (!this.stripe) {
                throw new Error('Stripe is not initialized. Please refresh the page.');
            }
            
            // Create Stripe Elements
            this.elements = this.stripe.elements();
            
            // Create card element
            const style = {
                base: {
                    color: '#32325d',
                    fontFamily: '"Helvetica Neue", Helvetica, sans-serif',
                    fontSmoothing: 'antialiased',
                    fontSize: '16px',
                    '::placeholder': {
                        color: '#aab7c4'
                    }
                },
                invalid: {
                    color: '#fa755a',
                    iconColor: '#fa755a'
                }
            };
            
            this.cardElement = this.elements.create('card', { style: style });
            this.cardElement.mount('#card-element');
            
            // Handle real-time validation errors
            this.cardElement.on('change', (event) => {
                const displayError = document.getElementById('card-errors');
                if (event.error) {
                    displayError.textContent = event.error.message;
                    displayError.style.display = 'block';
                } else {
                    displayError.textContent = '';
                    displayError.style.display = 'none';
                }
            });
            
            // Show payment form
            document.getElementById('payment-form-container').style.display = 'block';
            
            return paymentData;
        } catch (error) {
            console.error('Error setting up payment form:', error);
            alert('Error: ' + error.message);
            throw error;
        }
    }
    
    async submitPayment() {
        if (!this.stripe || !this.clientSecret || !this.cardElement) {
            throw new Error('Payment form is not properly initialized');
        }
        
        const submitButton = document.getElementById('submit-payment-btn');
        const originalText = submitButton.innerHTML;
        
        try {
            // Disable submit button
            submitButton.disabled = true;
            submitButton.innerHTML = '<i class="fas fa-spinner fa-spin me-1"></i>Processing...';
            
            // Confirm payment with Stripe
            const { error, paymentIntent } = await this.stripe.confirmCardPayment(this.clientSecret, {
                payment_method: {
                    card: this.cardElement,
                    billing_details: {
                        // Add billing details if needed
                    }
                }
            });
            
            if (error) {
                // Show error to user
                const displayError = document.getElementById('card-errors');
                displayError.textContent = error.message;
                displayError.style.display = 'block';
                
                submitButton.disabled = false;
                submitButton.innerHTML = originalText;
                throw error;
            } else if (paymentIntent && paymentIntent.status === 'succeeded') {
                // Payment succeeded, notify backend
                await this.processPayment();
                return paymentIntent;
            } else {
                throw new Error('Payment failed. Please try again.');
            }
        } catch (error) {
            console.error('Error submitting payment:', error);
            submitButton.disabled = false;
            submitButton.innerHTML = originalText;
            throw error;
        }
    }
    
    async processPayment() {
        try {
            const response = await fetch(`/orders/api/process-payment/${this.orderId}/`, {
                method: 'POST',
                headers: {
                    'X-CSRFToken': this.getCsrfToken(),
                    'Content-Type': 'application/x-www-form-urlencoded',
                },
                body: `payment_intent_id=${encodeURIComponent(this.paymentIntentId)}`,
                credentials: 'same-origin'
            });
            
            if (!response.ok) {
                const error = await response.json();
                throw new Error(error.error || 'Failed to process payment');
            }
            
            const data = await response.json();
            
            if (data.success) {
                // Show success message and reload page
                alert('Payment processed successfully!');
                window.location.reload();
                return data;
            } else {
                throw new Error(data.message || 'Payment processing failed');
            }
        } catch (error) {
            console.error('Error processing payment:', error);
            alert('Error processing payment: ' + error.message);
            throw error;
        }
    }
    
    cancelPayment() {
        // Hide payment form
        document.getElementById('payment-form-container').style.display = 'none';
        
        // Unmount card element if it exists
        if (this.cardElement) {
            this.cardElement.unmount();
            this.cardElement = null;
        }
        
        // Reset state
        this.paymentIntentId = null;
        this.clientSecret = null;
        this.orderId = null;
    }
    
    getCsrfToken() {
        // Get CSRF token from cookie
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
        
        // Try from Django's csrftoken input
        const csrfInput = document.querySelector('input[name="csrfmiddlewaretoken"]');
        if (csrfInput) return csrfInput.value;
        
        // Try meta tag
        const metaTag = document.querySelector('meta[name="csrf-token"]');
        if (metaTag) return metaTag.getAttribute('content');
        
        return '';
    }
}

// Initialize payment handler when DOM is ready
document.addEventListener('DOMContentLoaded', function() {
    const paymentHandler = new StripePaymentHandler();
    
    // Handle "Pay Online" button click
    const payOnlineBtn = document.getElementById('pay-online-btn');
    if (payOnlineBtn) {
        payOnlineBtn.addEventListener('click', async function() {
            const orderId = this.dataset.orderId;
            
            try {
                // Hide button and show loading
                this.disabled = true;
                this.innerHTML = '<i class="fas fa-spinner fa-spin me-1"></i>Loading...';
                
                await paymentHandler.setupPaymentForm(orderId);
                
                // Hide button after form is shown
                this.style.display = 'none';
            } catch (error) {
                alert('Error: ' + error.message);
                this.disabled = false;
                this.innerHTML = '<i class="fas fa-credit-card me-1"></i>Pay Online';
            }
        });
    }
    
    // Handle payment form submission
    const paymentForm = document.getElementById('payment-form');
    if (paymentForm) {
        paymentForm.addEventListener('submit', async function(e) {
            e.preventDefault();
            
            try {
                await paymentHandler.submitPayment();
            } catch (error) {
                console.error('Payment error:', error);
                // Error is already shown in submitPayment method
            }
        });
    }
    
    // Handle cancel payment button
    const cancelPaymentBtn = document.getElementById('cancel-payment-btn');
    if (cancelPaymentBtn) {
        cancelPaymentBtn.addEventListener('click', function() {
            paymentHandler.cancelPayment();
            if (payOnlineBtn) {
                payOnlineBtn.style.display = 'inline-block';
                payOnlineBtn.disabled = false;
                payOnlineBtn.innerHTML = '<i class="fas fa-credit-card me-1"></i>Pay Online';
            }
        });
    }
});

