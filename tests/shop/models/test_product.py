"""
Test Product Model
商品モデルのテスト
"""
from decimal import Decimal
from django.test import TestCase
from shop.models import Category, Product


class ProductModelTest(TestCase):
    """商品モデルのテストケース"""
    
    def setUp(self):
        """テスト前の準備"""
        self.category = Category.objects.create(
            name='電子機器',
            slug='electronics'
        )
        self.product = Product.objects.create(
            name='ノートPC',
            slug='notebook-pc',
            category=self.category,
            description='高性能ノートパソコン',
            price=Decimal('89800'),
            stock=10,
            is_active=True
        )
    
    def test_product_creation(self):
        """商品が正しく作成されることを確認"""
        self.assertEqual(self.product.name, 'ノートPC')
        self.assertEqual(self.product.slug, 'notebook-pc')
        self.assertEqual(self.product.category, self.category)
        self.assertEqual(self.product.price, Decimal('89800'))
        self.assertEqual(self.product.stock, 10)
        self.assertTrue(self.product.is_active)
    
    def test_product_str(self):
        """__str__メソッドが正しく動作することを確認"""
        self.assertEqual(str(self.product), 'ノートPC')
    
    def test_is_in_stock_property(self):
        """在庫チェックプロパティが正しく動作することを確認"""
        self.assertTrue(self.product.is_in_stock)
        
        # 在庫を0にする
        self.product.stock = 0
        self.product.save()
        self.assertFalse(self.product.is_in_stock)
    
    def test_product_slug_unique(self):
        """スラッグがユニークであることを確認"""
        from django.db import IntegrityError
        with self.assertRaises(IntegrityError):
            Product.objects.create(
                name='ノートPC2',
                slug='notebook-pc',  # 重複
                category=self.category,
                description='テスト',
                price=Decimal('50000'),
                stock=5
            )
    
    def test_product_ordering(self):
        """商品が作成日時の降順でソートされることを確認"""
        product2 = Product.objects.create(
            name='タブレット',
            slug='tablet',
            category=self.category,
            description='タブレット端末',
            price=Decimal('49800'),
            stock=15
        )
        
        products = list(Product.objects.all())
        self.assertEqual(products[0], product2)  # 後に作成
        self.assertEqual(products[1], self.product)  # 先に作成
    
    def test_product_default_values(self):
        """デフォルト値が正しく設定されることを確認"""
        product = Product.objects.create(
            name='テスト商品',
            slug='test-product',
            category=self.category,
            description='テスト',
            price=Decimal('1000')
        )
        self.assertEqual(product.stock, 0)
        self.assertTrue(product.is_active)
        self.assertIsNone(product.image.name)
