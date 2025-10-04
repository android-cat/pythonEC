"""
Test Order Form
注文フォームのテスト
"""
from django.test import TestCase
from shop.forms import OrderForm


class OrderFormTest(TestCase):
    """注文フォームのテストケース"""
    
    def test_order_form_valid_data(self):
        """正しいデータでフォームが有効になることを確認"""
        form_data = {
            'shipping_name': '山田太郎',
            'shipping_postal_code': '123-4567',
            'shipping_address': '東京都渋谷区テスト1-2-3',
            'shipping_phone': '090-1234-5678'
        }
        form = OrderForm(data=form_data)
        self.assertTrue(form.is_valid())
    
    def test_order_form_missing_name(self):
        """名前が欠落しているとエラー"""
        form_data = {
            'shipping_name': '',
            'shipping_postal_code': '123-4567',
            'shipping_address': '東京都渋谷区テスト1-2-3',
            'shipping_phone': '090-1234-5678'
        }
        form = OrderForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertIn('shipping_name', form.errors)
    
    def test_order_form_missing_postal_code(self):
        """郵便番号が欠落しているとエラー"""
        form_data = {
            'shipping_name': '山田太郎',
            'shipping_postal_code': '',
            'shipping_address': '東京都渋谷区テスト1-2-3',
            'shipping_phone': '090-1234-5678'
        }
        form = OrderForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertIn('shipping_postal_code', form.errors)
    
    def test_order_form_missing_address(self):
        """住所が欠落しているとエラー"""
        form_data = {
            'shipping_name': '山田太郎',
            'shipping_postal_code': '123-4567',
            'shipping_address': '',
            'shipping_phone': '090-1234-5678'
        }
        form = OrderForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertIn('shipping_address', form.errors)
    
    def test_order_form_missing_phone(self):
        """電話番号が欠落しているとエラー"""
        form_data = {
            'shipping_name': '山田太郎',
            'shipping_postal_code': '123-4567',
            'shipping_address': '東京都渋谷区テスト1-2-3',
            'shipping_phone': ''
        }
        form = OrderForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertIn('shipping_phone', form.errors)
    
    def test_order_form_widget_attributes(self):
        """フォームウィジェットに正しい属性が設定されていることを確認"""
        form = OrderForm()
        
        # クラス属性が設定されていることを確認
        self.assertIn('form-control', form.fields['shipping_name'].widget.attrs['class'])
        self.assertIn('form-control', form.fields['shipping_postal_code'].widget.attrs['class'])
        self.assertIn('form-control', form.fields['shipping_address'].widget.attrs['class'])
        self.assertIn('form-control', form.fields['shipping_phone'].widget.attrs['class'])
        
        # placeholder属性が設定されていることを確認
        self.assertIn('placeholder', form.fields['shipping_name'].widget.attrs)
        self.assertIn('placeholder', form.fields['shipping_postal_code'].widget.attrs)
        self.assertIn('placeholder', form.fields['shipping_address'].widget.attrs)
        self.assertIn('placeholder', form.fields['shipping_phone'].widget.attrs)
