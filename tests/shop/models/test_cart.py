"""
Test Cart Models
カートモデルのテスト
"""
from decimal import Decimal
from django.test import TestCase
from django.contrib.auth.models import User
from shop.models import Category, Product, Cart, CartItem


class CartModelTest(TestCase):
    """カートモデルのテストケース"""
    
    def setUp(self):
        """テスト前の準備"""
        self.user = User.objects.create_user(
            username='testuser',
            password='testpass123'
        )
        self.category = Category.objects.create(
            name='電子機器',
            slug='electronics'
        )
        self.product1 = Product.objects.create(
            name='ノートPC',
            slug='notebook-pc',
            category=self.category,
            description='高性能ノートパソコン',
            price=Decimal('89800'),
            stock=10
        )
        self.product2 = Product.objects.create(
            name='マウス',
            slug='mouse',
            category=self.category,
            description='ワイヤレスマウス',
            price=Decimal('2980'),
            stock=50
        )
    
    def test_cart_creation_for_user(self):
        """ユーザー用カートが正しく作成されることを確認"""
        cart = Cart.objects.create(user=self.user)
        self.assertEqual(cart.user, self.user)
        self.assertIsNone(cart.session_key)
    
    def test_cart_creation_for_guest(self):
        """ゲスト用カートが正しく作成されることを確認"""
        cart = Cart.objects.create(session_key='test_session_123')
        self.assertIsNone(cart.user)
        self.assertEqual(cart.session_key, 'test_session_123')
    
    def test_cart_str(self):
        """__str__メソッドが正しく動作することを確認"""
        cart = Cart.objects.create(user=self.user)
        self.assertEqual(str(cart), f"Cart {cart.id}")
    
    def test_total_price_property(self):
        """合計金額プロパティが正しく計算されることを確認"""
        cart = Cart.objects.create(user=self.user)
        
        # カートに商品を追加
        CartItem.objects.create(cart=cart, product=self.product1, quantity=2)
        CartItem.objects.create(cart=cart, product=self.product2, quantity=3)
        
        expected_total = (self.product1.price * 2) + (self.product2.price * 3)
        self.assertEqual(cart.total_price, expected_total)
    
    def test_total_items_property(self):
        """合計商品数プロパティが正しく計算されることを確認"""
        cart = Cart.objects.create(user=self.user)
        
        CartItem.objects.create(cart=cart, product=self.product1, quantity=2)
        CartItem.objects.create(cart=cart, product=self.product2, quantity=3)
        
        self.assertEqual(cart.total_items, 5)
    
    def test_empty_cart_properties(self):
        """空のカートのプロパティが正しく動作することを確認"""
        cart = Cart.objects.create(user=self.user)
        self.assertEqual(cart.total_price, 0)
        self.assertEqual(cart.total_items, 0)


class CartItemModelTest(TestCase):
    """カート商品モデルのテストケース"""
    
    def setUp(self):
        """テスト前の準備"""
        self.user = User.objects.create_user(
            username='testuser',
            password='testpass123'
        )
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
            stock=10
        )
        self.cart = Cart.objects.create(user=self.user)
    
    def test_cart_item_creation(self):
        """カート商品が正しく作成されることを確認"""
        cart_item = CartItem.objects.create(
            cart=self.cart,
            product=self.product,
            quantity=2
        )
        self.assertEqual(cart_item.cart, self.cart)
        self.assertEqual(cart_item.product, self.product)
        self.assertEqual(cart_item.quantity, 2)
    
    def test_cart_item_str(self):
        """__str__メソッドが正しく動作することを確認"""
        cart_item = CartItem.objects.create(
            cart=self.cart,
            product=self.product,
            quantity=2
        )
        self.assertEqual(str(cart_item), 'ノートPC x 2')
    
    def test_subtotal_property(self):
        """小計プロパティが正しく計算されることを確認"""
        cart_item = CartItem.objects.create(
            cart=self.cart,
            product=self.product,
            quantity=3
        )
        expected_subtotal = self.product.price * 3
        self.assertEqual(cart_item.subtotal, expected_subtotal)
    
    def test_unique_together_constraint(self):
        """同じカートに同じ商品を重複追加できないことを確認"""
        CartItem.objects.create(
            cart=self.cart,
            product=self.product,
            quantity=1
        )
        
        from django.db import IntegrityError
        with self.assertRaises(IntegrityError):
            CartItem.objects.create(
                cart=self.cart,
                product=self.product,
                quantity=1
            )
    
    def test_default_quantity(self):
        """デフォルト数量が1であることを確認"""
        cart_item = CartItem.objects.create(
            cart=self.cart,
            product=self.product
        )
        self.assertEqual(cart_item.quantity, 1)
