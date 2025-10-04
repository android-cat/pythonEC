"""
Cart Models - カート関連
"""
from django.db import models
from django.contrib.auth.models import User
from .product import Product


class Cart(models.Model):
    """カートモデル"""
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='ユーザー', null=True, blank=True)
    session_key = models.CharField('セッションキー', max_length=40, null=True, blank=True)
    created_at = models.DateTimeField('作成日時', auto_now_add=True)
    updated_at = models.DateTimeField('更新日時', auto_now=True)

    class Meta:
        verbose_name = 'カート'
        verbose_name_plural = 'カート'

    def __str__(self):
        return f"Cart {self.id}"

    @property
    def total_price(self):
        """カート内商品の合計金額"""
        return sum(item.subtotal for item in self.items.all())

    @property
    def total_items(self):
        """カート内商品の合計数量"""
        return sum(item.quantity for item in self.items.all())


class CartItem(models.Model):
    """カート商品モデル"""
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE, verbose_name='カート', related_name='items')
    product = models.ForeignKey(Product, on_delete=models.CASCADE, verbose_name='商品')
    quantity = models.IntegerField('数量', default=1)
    created_at = models.DateTimeField('作成日時', auto_now_add=True)
    updated_at = models.DateTimeField('更新日時', auto_now=True)

    class Meta:
        verbose_name = 'カート商品'
        verbose_name_plural = 'カート商品'
        unique_together = ['cart', 'product']

    def __str__(self):
        return f"{self.product.name} x {self.quantity}"

    @property
    def subtotal(self):
        """小計"""
        return self.product.price * self.quantity
