"""
Order Form - 注文フォーム
"""
from django import forms
from shop.models import Order


class OrderForm(forms.ModelForm):
    """注文フォーム"""
    
    class Meta:
        model = Order
        fields = ['shipping_name', 'shipping_postal_code', 'shipping_address', 'shipping_phone']
        widgets = {
            'shipping_name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': '山田 太郎'
            }),
            'shipping_postal_code': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': '123-4567'
            }),
            'shipping_address': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 3,
                'placeholder': '東京都渋谷区...'
            }),
            'shipping_phone': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': '090-1234-5678'
            }),
        }
