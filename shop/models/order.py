"""
Order Models - 注文関連
"""
from django.db import models
from django.contrib.auth.models import User
from .product import Product


class Order(models.Model):
    """注文モデル"""
    STATUS_CHOICES = [
        ('pending', '注文受付'),
        ('processing', '処理中'),
        ('shipped', '発送済み'),
        ('delivered', '配達完了'),
        ('cancelled', 'キャンセル'),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='ユーザー', related_name='orders')
    status = models.CharField('ステータス', max_length=20, choices=STATUS_CHOICES, default='pending')
    total_amount = models.DecimalField('合計金額', max_digits=10, decimal_places=0)
    
    # 配送先情報
    shipping_name = models.CharField('お名前', max_length=100)
    shipping_postal_code = models.CharField('郵便番号', max_length=10)
    shipping_address = models.TextField('住所')
    shipping_phone = models.CharField('電話番号', max_length=20)
    
    created_at = models.DateTimeField('注文日時', auto_now_add=True)
    updated_at = models.DateTimeField('更新日時', auto_now=True)

    class Meta:
        verbose_name = '注文'
        verbose_name_plural = '注文'
        ordering = ['-created_at']

    def __str__(self):
        return f"Order #{self.id} - {self.user.username}"


class OrderItem(models.Model):
    """注文商品モデル"""
    order = models.ForeignKey(Order, on_delete=models.CASCADE, verbose_name='注文', related_name='items')
    product = models.ForeignKey(Product, on_delete=models.CASCADE, verbose_name='商品')
    quantity = models.IntegerField('数量')
    price = models.DecimalField('単価', max_digits=10, decimal_places=0)

    class Meta:
        verbose_name = '注文商品'
        verbose_name_plural = '注文商品'

    def __str__(self):
        return f"{self.product.name} x {self.quantity}"

    @property
    def subtotal(self):
        """小計"""
        return self.price * self.quantity
