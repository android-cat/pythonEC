"""
Test Order Service
注文サービスのテスト
"""
from decimal import Decimal
from django.test import TestCase
from django.contrib.auth.models import User
from shop.models import Category, Product, Cart, CartItem, Order, OrderItem
from shop.services import OrderService


class OrderServiceTest(TestCase):
    """注文サービスのテストケース"""
    
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
    
    def test_create_order_from_cart(self):
        """カートから注文を作成する機能をテスト"""
        # カートを準備
        cart = Cart.objects.create(user=self.user)
        CartItem.objects.create(cart=cart, product=self.product1, quantity=2)
        CartItem.objects.create(cart=cart, product=self.product2, quantity=3)
        
        # 配送先情報
        shipping_data = {
            'shipping_name': '山田太郎',
            'shipping_postal_code': '123-4567',
            'shipping_address': '東京都渋谷区テスト1-2-3',
            'shipping_phone': '090-1234-5678'
        }
        
        # 初期在庫を記録
        initial_stock1 = self.product1.stock
        initial_stock2 = self.product2.stock
        
        # 注文作成
        order = OrderService.create_order_from_cart(
            user=self.user,
            cart=cart,
            shipping_data=shipping_data
        )
        
        # 注文が作成されたことを確認
        self.assertIsNotNone(order)
        self.assertEqual(order.user, self.user)
        self.assertEqual(order.status, 'pending')
        self.assertEqual(order.shipping_name, '山田太郎')
        
        # 注文商品が作成されたことを確認
        self.assertEqual(order.items.count(), 2)
        
        order_item1 = order.items.get(product=self.product1)
        self.assertEqual(order_item1.quantity, 2)
        self.assertEqual(order_item1.price, self.product1.price)
        
        order_item2 = order.items.get(product=self.product2)
        self.assertEqual(order_item2.quantity, 3)
        self.assertEqual(order_item2.price, self.product2.price)
        
        # 在庫が減っていることを確認
        self.product1.refresh_from_db()
        self.product2.refresh_from_db()
        self.assertEqual(self.product1.stock, initial_stock1 - 2)
        self.assertEqual(self.product2.stock, initial_stock2 - 3)
        
        # カートが空になっていることを確認
        self.assertEqual(cart.items.count(), 0)
    
    def test_create_order_calculates_total_correctly(self):
        """注文の合計金額が正しく計算されることを確認"""
        cart = Cart.objects.create(user=self.user)
        CartItem.objects.create(cart=cart, product=self.product1, quantity=1)
        CartItem.objects.create(cart=cart, product=self.product2, quantity=2)
        
        expected_total = (self.product1.price * 1) + (self.product2.price * 2)
        
        shipping_data = {
            'shipping_name': 'テスト',
            'shipping_postal_code': '111-1111',
            'shipping_address': 'テスト住所',
            'shipping_phone': '090-0000-0000'
        }
        
        order = OrderService.create_order_from_cart(
            user=self.user,
            cart=cart,
            shipping_data=shipping_data
        )
        
        self.assertEqual(order.total_amount, expected_total)
    
    def test_cancel_order(self):
        """注文キャンセル機能をテスト"""
        # 注文を作成
        order = Order.objects.create(
            user=self.user,
            status='pending',
            total_amount=Decimal('100000'),
            shipping_name='テスト',
            shipping_postal_code='111-1111',
            shipping_address='テスト住所',
            shipping_phone='090-0000-0000'
        )
        
        OrderItem.objects.create(
            order=order,
            product=self.product1,
            quantity=2,
            price=self.product1.price
        )
        
        # 初期在庫を記録
        initial_stock = self.product1.stock
        
        # 注文をキャンセル
        cancelled_order = OrderService.cancel_order(order)
        
        # ステータスが'cancelled'になっていることを確認
        self.assertEqual(cancelled_order.status, 'cancelled')
        
        # 在庫が戻っていることを確認
        self.product1.refresh_from_db()
        self.assertEqual(self.product1.stock, initial_stock + 2)
    
    def test_cancel_delivered_order_raises_error(self):
        """配達済み注文のキャンセルでエラーが発生することを確認"""
        order = Order.objects.create(
            user=self.user,
            status='delivered',
            total_amount=Decimal('100000'),
            shipping_name='テスト',
            shipping_postal_code='111-1111',
            shipping_address='テスト住所',
            shipping_phone='090-0000-0000'
        )
        
        with self.assertRaises(ValueError):
            OrderService.cancel_order(order)
    
    def test_cancel_already_cancelled_order_raises_error(self):
        """既にキャンセル済みの注文を再度キャンセルするとエラー"""
        order = Order.objects.create(
            user=self.user,
            status='cancelled',
            total_amount=Decimal('100000'),
            shipping_name='テスト',
            shipping_postal_code='111-1111',
            shipping_address='テスト住所',
            shipping_phone='090-0000-0000'
        )
        
        with self.assertRaises(ValueError):
            OrderService.cancel_order(order)
    
    def test_update_order_status(self):
        """注文ステータス更新機能をテスト"""
        order = Order.objects.create(
            user=self.user,
            status='pending',
            total_amount=Decimal('100000'),
            shipping_name='テスト',
            shipping_postal_code='111-1111',
            shipping_address='テスト住所',
            shipping_phone='090-0000-0000'
        )
        
        # ステータスを更新
        updated_order = OrderService.update_order_status(order, 'processing')
        self.assertEqual(updated_order.status, 'processing')
        
        updated_order = OrderService.update_order_status(order, 'shipped')
        self.assertEqual(updated_order.status, 'shipped')
    
    def test_update_order_status_with_invalid_status(self):
        """無効なステータスでエラーが発生することを確認"""
        order = Order.objects.create(
            user=self.user,
            status='pending',
            total_amount=Decimal('100000'),
            shipping_name='テスト',
            shipping_postal_code='111-1111',
            shipping_address='テスト住所',
            shipping_phone='090-0000-0000'
        )
        
        with self.assertRaises(ValueError):
            OrderService.update_order_status(order, 'invalid_status')
