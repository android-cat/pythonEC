"""
Test Order Models
注文モデルのテスト
"""
from decimal import Decimal
from django.test import TestCase
from django.contrib.auth.models import User
from shop.models import Category, Product, Order, OrderItem


class OrderModelTest(TestCase):
    """注文モデルのテストケース"""
    
    def setUp(self):
        """テスト前の準備"""
        self.user = User.objects.create_user(
            username='testuser',
            password='testpass123'
        )
        self.order = Order.objects.create(
            user=self.user,
            status='pending',
            total_amount=Decimal('100000'),
            shipping_name='山田太郎',
            shipping_postal_code='123-4567',
            shipping_address='東京都渋谷区テスト1-2-3',
            shipping_phone='090-1234-5678'
        )
    
    def test_order_creation(self):
        """注文が正しく作成されることを確認"""
        self.assertEqual(self.order.user, self.user)
        self.assertEqual(self.order.status, 'pending')
        self.assertEqual(self.order.total_amount, Decimal('100000'))
        self.assertEqual(self.order.shipping_name, '山田太郎')
    
    def test_order_str(self):
        """__str__メソッドが正しく動作することを確認"""
        expected = f"Order #{self.order.id} - testuser"
        self.assertEqual(str(self.order), expected)
    
    def test_order_status_choices(self):
        """注文ステータスが正しく設定できることを確認"""
        statuses = ['pending', 'processing', 'shipped', 'delivered', 'cancelled']
        
        for status in statuses:
            self.order.status = status
            self.order.save()
            self.order.refresh_from_db()
            self.assertEqual(self.order.status, status)
    
    def test_order_default_status(self):
        """デフォルトステータスが'pending'であることを確認"""
        order = Order.objects.create(
            user=self.user,
            total_amount=Decimal('50000'),
            shipping_name='テスト',
            shipping_postal_code='111-1111',
            shipping_address='テスト住所',
            shipping_phone='090-0000-0000'
        )
        self.assertEqual(order.status, 'pending')
    
    def test_order_ordering(self):
        """注文が作成日時の降順でソートされることを確認"""
        order2 = Order.objects.create(
            user=self.user,
            total_amount=Decimal('50000'),
            shipping_name='テスト',
            shipping_postal_code='111-1111',
            shipping_address='テスト住所',
            shipping_phone='090-0000-0000'
        )
        
        orders = list(Order.objects.all())
        self.assertEqual(orders[0], order2)  # 後に作成
        self.assertEqual(orders[1], self.order)  # 先に作成


class OrderItemModelTest(TestCase):
    """注文商品モデルのテストケース"""
    
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
        self.order = Order.objects.create(
            user=self.user,
            total_amount=Decimal('179600'),
            shipping_name='山田太郎',
            shipping_postal_code='123-4567',
            shipping_address='東京都渋谷区テスト1-2-3',
            shipping_phone='090-1234-5678'
        )
    
    def test_order_item_creation(self):
        """注文商品が正しく作成されることを確認"""
        order_item = OrderItem.objects.create(
            order=self.order,
            product=self.product,
            quantity=2,
            price=Decimal('89800')
        )
        self.assertEqual(order_item.order, self.order)
        self.assertEqual(order_item.product, self.product)
        self.assertEqual(order_item.quantity, 2)
        self.assertEqual(order_item.price, Decimal('89800'))
    
    def test_order_item_str(self):
        """__str__メソッドが正しく動作することを確認"""
        order_item = OrderItem.objects.create(
            order=self.order,
            product=self.product,
            quantity=2,
            price=Decimal('89800')
        )
        self.assertEqual(str(order_item), 'ノートPC x 2')
    
    def test_subtotal_property(self):
        """小計プロパティが正しく計算されることを確認"""
        order_item = OrderItem.objects.create(
            order=self.order,
            product=self.product,
            quantity=3,
            price=Decimal('89800')
        )
        expected_subtotal = Decimal('89800') * 3
        self.assertEqual(order_item.subtotal, expected_subtotal)
    
    def test_price_snapshot(self):
        """注文時の価格がスナップショットとして保存されることを確認"""
        original_price = self.product.price
        
        order_item = OrderItem.objects.create(
            order=self.order,
            product=self.product,
            quantity=1,
            price=original_price
        )
        
        # 商品価格を変更
        self.product.price = Decimal('50000')
        self.product.save()
        
        # 注文商品の価格は変わらない
        order_item.refresh_from_db()
        self.assertEqual(order_item.price, original_price)
