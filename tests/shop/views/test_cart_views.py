"""
Test Cart Views
カートビューのテスト
"""
from decimal import Decimal
from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth.models import User
from shop.models import Category, Product, Cart, CartItem


class CartViewTest(TestCase):
    """カート表示ビューのテストケース"""
    
    def setUp(self):
        """テスト前の準備"""
        self.client = Client()
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
    
    def test_cart_view_status_code(self):
        """カートページが正常に表示されることを確認"""
        response = self.client.get(reverse('shop:cart'))
        self.assertEqual(response.status_code, 200)
    
    def test_cart_view_uses_correct_template(self):
        """正しいテンプレートが使用されていることを確認"""
        response = self.client.get(reverse('shop:cart'))
        self.assertTemplateUsed(response, 'shop/cart.html')
    
    def test_cart_view_with_items(self):
        """カートに商品がある場合のテスト"""
        # ゲストカートを作成
        session = self.client.session
        session.save()
        
        cart = Cart.objects.create(session_key=session.session_key)
        CartItem.objects.create(cart=cart, product=self.product, quantity=2)
        
        response = self.client.get(reverse('shop:cart'))
        self.assertEqual(response.context['cart'].id, cart.id)
        self.assertEqual(response.context['cart'].items.count(), 1)


class AddToCartTest(TestCase):
    """カート追加機能のテストケース"""
    
    def setUp(self):
        """テスト前の準備"""
        self.client = Client()
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
    
    def test_add_to_cart_creates_cart_item(self):
        """カートに商品が追加されることを確認"""
        response = self.client.post(
            reverse('shop:add_to_cart'),
            {'product_id': self.product.id, 'quantity': 2}
        )
        
        self.assertEqual(response.status_code, 302)  # リダイレクト
        
        # カートが作成されていることを確認
        cart = Cart.objects.first()
        self.assertIsNotNone(cart)
        
        # カートアイテムが作成されていることを確認
        cart_item = CartItem.objects.first()
        self.assertIsNotNone(cart_item)
        self.assertEqual(cart_item.product, self.product)
        self.assertEqual(cart_item.quantity, 2)
    
    def test_add_to_cart_increases_quantity(self):
        """既存のカートアイテムの数量が増えることを確認"""
        # 最初にカートに追加
        self.client.post(
            reverse('shop:add_to_cart'),
            {'product_id': self.product.id, 'quantity': 1}
        )
        
        # 再度追加
        self.client.post(
            reverse('shop:add_to_cart'),
            {'product_id': self.product.id, 'quantity': 2}
        )
        
        # カートアイテムが1つだけで数量が3になっていることを確認
        self.assertEqual(CartItem.objects.count(), 1)
        cart_item = CartItem.objects.first()
        self.assertEqual(cart_item.quantity, 3)
    
    def test_add_to_cart_invalid_product(self):
        """存在しない商品でエラーが発生することを確認"""
        response = self.client.post(
            reverse('shop:add_to_cart'),
            {'product_id': 9999, 'quantity': 1}
        )
        self.assertEqual(response.status_code, 404)


class UpdateCartItemTest(TestCase):
    """カートアイテム更新機能のテストケース"""
    
    def setUp(self):
        """テスト前の準備"""
        self.client = Client()
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
        
        # カートとカートアイテムを作成
        session = self.client.session
        session.save()
        
        self.cart = Cart.objects.create(session_key=session.session_key)
        self.cart_item = CartItem.objects.create(
            cart=self.cart,
            product=self.product,
            quantity=2
        )
    
    def test_update_cart_item_quantity(self):
        """カートアイテムの数量が更新されることを確認"""
        response = self.client.post(
            reverse('shop:update_cart_item', kwargs={'item_id': self.cart_item.id}),
            {'quantity': 5}
        )
        
        self.assertEqual(response.status_code, 302)  # リダイレクト
        
        self.cart_item.refresh_from_db()
        self.assertEqual(self.cart_item.quantity, 5)
    
    def test_update_cart_item_invalid_quantity(self):
        """無効な数量でエラーが発生することを確認"""
        response = self.client.post(
            reverse('shop:update_cart_item', kwargs={'item_id': self.cart_item.id}),
            {'quantity': 0}
        )
        
        # 数量が0以下の場合はバリデーションエラー
        self.cart_item.refresh_from_db()
        self.assertEqual(self.cart_item.quantity, 2)  # 変更されていない


class RemoveFromCartTest(TestCase):
    """カートから削除機能のテストケース"""
    
    def setUp(self):
        """テスト前の準備"""
        self.client = Client()
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
        
        # カートとカートアイテムを作成
        session = self.client.session
        session.save()
        
        self.cart = Cart.objects.create(session_key=session.session_key)
        self.cart_item = CartItem.objects.create(
            cart=self.cart,
            product=self.product,
            quantity=2
        )
    
    def test_remove_from_cart(self):
        """カートから商品が削除されることを確認"""
        response = self.client.post(
            reverse('shop:remove_from_cart', kwargs={'item_id': self.cart_item.id})
        )
        
        self.assertEqual(response.status_code, 302)  # リダイレクト
        
        # カートアイテムが削除されていることを確認
        self.assertFalse(CartItem.objects.filter(id=self.cart_item.id).exists())
