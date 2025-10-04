"""
Product Model - 商品
"""
from django.db import models
from .category import Category


class Product(models.Model):
    """商品モデル"""
    name = models.CharField('商品名', max_length=200)
    slug = models.SlugField('スラッグ', unique=True)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, verbose_name='カテゴリ', related_name='products')
    description = models.TextField('説明')
    price = models.DecimalField('価格', max_digits=10, decimal_places=0)
    stock = models.IntegerField('在庫数', default=0)
    image = models.ImageField('画像', upload_to='products/', blank=True, null=True)
    is_active = models.BooleanField('販売中', default=True)
    created_at = models.DateTimeField('作成日時', auto_now_add=True)
    updated_at = models.DateTimeField('更新日時', auto_now=True)

    class Meta:
        verbose_name = '商品'
        verbose_name_plural = '商品'
        ordering = ['-created_at']

    def __str__(self):
        return self.name

    @property
    def is_in_stock(self):
        """在庫があるかチェック"""
        return self.stock > 0
