from django import forms
from .models import Order


class OrderForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = ['full_name', 'address', 'phone_number', 'comment', 'amount']

from django import forms
from .models import Order

class ReceiptUploadForm(forms.ModelForm):
    payment_method = forms.ChoiceField(choices=Order.PAYMENT_METHODS, widget=forms.RadioSelect)
    receipt_file = forms.FileField(required=True)

    class Meta:
        model = Order
        fields = ['payment_method', 'receipt_file']
