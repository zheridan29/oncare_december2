from django import forms
from django.contrib.auth import get_user_model
from .models import Order, OrderItem, Cart, CartItem
from inventory.models import Medicine
from common.models import Address
from django.core.validators import RegexValidator

User = get_user_model()

class OrderForm(forms.ModelForm):
    """Form for creating and editing orders"""
    
    class Meta:
        model = Order
        fields = ['customer_name', 'customer_phone', 'customer_address', 'delivery_method', 'delivery_address', 'delivery_instructions', 'payment_status', 'customer_notes']
        widgets = {
            'customer_name': forms.TextInput(attrs={'class': 'form-control'}),
            'customer_phone': forms.TextInput(attrs={'class': 'form-control'}),
            'customer_address': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'delivery_method': forms.Select(attrs={'class': 'form-select'}),
            'delivery_address': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'delivery_instructions': forms.Textarea(attrs={'class': 'form-control', 'rows': 2}),
            'payment_status': forms.Select(attrs={'class': 'form-select'}),
            'customer_notes': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
        }


class OrderWithItemsForm(forms.ModelForm):
    """Form for creating orders with medicine selection"""
    
    # Medicine selection fields
    medicine_1 = forms.ModelChoiceField(
        queryset=Medicine.objects.none(),
        required=False,
        empty_label="Select Medicine",
        widget=forms.Select(attrs={'class': 'form-select'})
    )
    quantity_1 = forms.IntegerField(
        required=False,
        min_value=1,
        widget=forms.NumberInput(attrs={'class': 'form-control', 'min': 1, 'placeholder': 'Quantity'})
    )
    unit_1 = forms.CharField(
        required=False,
        initial='boxes',
        widget=forms.HiddenInput()  # Hidden since it's always 'boxes'
    )
    
    unit_2 = forms.CharField(
        required=False,
        initial='boxes',
        widget=forms.HiddenInput()  # Hidden since it's always 'boxes'
    )
    medicine_2 = forms.ModelChoiceField(
        queryset=Medicine.objects.none(),
        required=False,
        empty_label="Select Medicine",
        widget=forms.Select(attrs={'class': 'form-select'})
    )
    quantity_2 = forms.IntegerField(
        required=False,
        min_value=1,
        widget=forms.NumberInput(attrs={'class': 'form-control', 'min': 1, 'placeholder': 'Quantity'})
    )
    
    unit_3 = forms.CharField(
        required=False,
        initial='boxes',
        widget=forms.HiddenInput()  # Hidden since it's always 'boxes'
    )
    medicine_3 = forms.ModelChoiceField(
        queryset=Medicine.objects.none(),
        required=False,
        empty_label="Select Medicine",
        widget=forms.Select(attrs={'class': 'form-select'})
    )
    quantity_3 = forms.IntegerField(
        required=False,
        min_value=1,
        widget=forms.NumberInput(attrs={'class': 'form-control', 'min': 1, 'placeholder': 'Quantity'})
    )
    
    unit_4 = forms.CharField(
        required=False,
        initial='boxes',
        widget=forms.HiddenInput()  # Hidden since it's always 'boxes'
    )
    medicine_4 = forms.ModelChoiceField(
        queryset=Medicine.objects.none(),
        required=False,
        empty_label="Select Medicine",
        widget=forms.Select(attrs={'class': 'form-select'})
    )
    quantity_4 = forms.IntegerField(
        required=False,
        min_value=1,
        widget=forms.NumberInput(attrs={'class': 'form-control', 'min': 1, 'placeholder': 'Quantity'})
    )
    
    unit_5 = forms.CharField(
        required=False,
        initial='boxes',
        widget=forms.HiddenInput()  # Hidden since it's always 'boxes'
    )
    medicine_5 = forms.ModelChoiceField(
        queryset=Medicine.objects.none(),
        required=False,
        empty_label="Select Medicine",
        widget=forms.Select(attrs={'class': 'form-select'})
    )
    quantity_5 = forms.IntegerField(
        required=False,
        min_value=1,
        widget=forms.NumberInput(attrs={'class': 'form-control', 'min': 1, 'placeholder': 'Quantity'})
    )
    
    class Meta:
        model = Order
        fields = ['delivery_method', 'delivery_address', 'delivery_instructions', 'payment_status', 'customer_notes']
        widgets = {
            'delivery_method': forms.Select(attrs={'class': 'form-select'}),
            'delivery_address': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'delivery_instructions': forms.Textarea(attrs={'class': 'form-control', 'rows': 2}),
            'payment_status': forms.Select(attrs={'class': 'form-select'}),
            'customer_notes': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
        }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Set the queryset for medicine fields
        medicine_queryset = Medicine.objects.filter(is_active=True, is_available=True).order_by('name')
        self.fields['medicine_1'].queryset = medicine_queryset
        self.fields['medicine_2'].queryset = medicine_queryset
        self.fields['medicine_3'].queryset = medicine_queryset
        self.fields['medicine_4'].queryset = medicine_queryset
        self.fields['medicine_5'].queryset = medicine_queryset
    
    def clean(self):
        cleaned_data = super().clean()
        
        # Check if at least one medicine is selected
        medicines = []
        for i in range(1, 6):
            medicine = cleaned_data.get(f'medicine_{i}')
            quantity = cleaned_data.get(f'quantity_{i}')
            
            if medicine and quantity:
                medicines.append((medicine, quantity))
            elif medicine and not quantity:
                raise forms.ValidationError(f"Please enter quantity for {medicine.name}")
            elif not medicine and quantity:
                raise forms.ValidationError("Please select a medicine for the quantity entered")
        
        if not medicines:
            raise forms.ValidationError("Please select at least one medicine for the order")
        
        return cleaned_data

class OrderItemForm(forms.ModelForm):
    """Form for adding items to orders"""
    
    class Meta:
        model = OrderItem
        fields = ['medicine', 'quantity']
        widgets = {
            'medicine': forms.Select(attrs={'class': 'form-select'}),
            'quantity': forms.NumberInput(attrs={'class': 'form-control', 'min': 1}),
        }

class CartAddForm(forms.ModelForm):
    """Form for adding items to cart"""
    
    class Meta:
        model = CartItem
        fields = ['medicine', 'quantity']
        widgets = {
            'medicine': forms.Select(attrs={'class': 'form-select'}),
            'quantity': forms.NumberInput(attrs={'class': 'form-control', 'min': 1}),
        }

class OrderStatusUpdateForm(forms.ModelForm):
    """Form for updating order status"""
    
    class Meta:
        model = Order
        fields = ['status', 'payment_status', 'internal_notes']
        widgets = {
            'status': forms.Select(attrs={'class': 'form-select'}),
            'payment_status': forms.Select(attrs={'class': 'form-select'}),
            'internal_notes': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
        }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['status'].choices = Order.STATUS_CHOICES
        self.fields['payment_status'].choices = Order.PAYMENT_STATUS_CHOICES

class PrescriptionUploadForm(forms.ModelForm):
    """Form for uploading prescriptions"""
    
    class Meta:
        model = Order
        fields = ['prescription_image', 'customer_notes']
        widgets = {
            'prescription_image': forms.FileInput(attrs={'class': 'form-control', 'accept': '.jpg,.jpeg,.png,.pdf'}),
            'customer_notes': forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'placeholder': 'Additional notes about the prescription'}),
        }

class PrescriptionVerifyForm(forms.ModelForm):
    """Form for verifying prescriptions"""
    
    class Meta:
        model = Order
        fields = ['prescription_verified', 'internal_notes', 'verified_by']
        widgets = {
            'prescription_verified': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'internal_notes': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'verified_by': forms.Select(attrs={'class': 'form-select'}),
        }

class OrderCancelForm(forms.ModelForm):
    """Form for cancelling orders"""
    
    class Meta:
        model = Order
        fields = ['internal_notes']
        widgets = {
            'internal_notes': forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'placeholder': 'Please provide a reason for cancelling this order'}),
        }


class ManualPaymentForm(forms.Form):
    """Form for submitting manual payment proof"""
    payment_reference = forms.CharField(
        max_length=100,
        required=True,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Enter payment reference number or transaction ID'
        }),
        help_text='Reference number from your bank transfer or payment receipt'
    )
    payment_date = forms.DateField(
        required=True,
        widget=forms.DateInput(attrs={
            'class': 'form-control',
            'type': 'date'
        }),
        help_text='Date when payment was made'
    )
    payment_proof = forms.FileField(
        required=False,
        widget=forms.FileInput(attrs={
            'class': 'form-control',
            'accept': '.jpg,.jpeg,.png,.pdf,.JPG,.JPEG,.PNG,.PDF'
        }),
        help_text='Upload payment receipt or screenshot - Only images (JPG, PNG) and PDF files are allowed (optional)'
    )
    notes = forms.CharField(
        required=False,
        widget=forms.Textarea(attrs={
            'class': 'form-control',
            'rows': 3,
            'placeholder': 'Additional notes about the payment (optional)'
        })
    )
    
    def clean_payment_proof(self):
        """Validate that uploaded file is an image or PDF"""
        proof_file = self.cleaned_data.get('payment_proof')
        
        if proof_file:
            # Get file extension
            file_name = proof_file.name.lower()
            allowed_extensions = ['.jpg', '.jpeg', '.png', '.pdf']
            file_extension = None
            
            for ext in allowed_extensions:
                if file_name.endswith(ext):
                    file_extension = ext
                    break
            
            if not file_extension:
                raise forms.ValidationError(
                    'Invalid file type. Only image files (JPG, PNG) and PDF files are allowed.'
                )
            
            # Validate file size (max 10MB)
            max_size = 10 * 1024 * 1024  # 10MB in bytes
            if proof_file.size > max_size:
                raise forms.ValidationError(
                    f'File size exceeds the maximum allowed size of 10MB. '
                    f'Your file size is {proof_file.size / (1024 * 1024):.2f}MB.'
                )
            
            # Validate MIME type
            allowed_mime_types = [
                'image/jpeg',
                'image/jpg',
                'image/png',
                'application/pdf',
            ]
            
            if hasattr(proof_file, 'content_type') and proof_file.content_type:
                if proof_file.content_type not in allowed_mime_types:
                    raise forms.ValidationError(
                        f'Invalid file type. Only image files (JPG, PNG) and PDF files are allowed. '
                        f'File type detected: {proof_file.content_type}'
                    )
        
        return proof_file

