"""
Test Order Views
注文ビューのテスト
"""
from decimal import Decimal
from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth.models import User
from shop.models import Category, Product, Cart, CartItem, Order, OrderItem


class CheckoutViewTest(TestCase):
    """チェックアウトビューのテストケース"""
    
    def setUp(self):
        """テスト前の準備"""
        self.client = Client()
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
    
    def test_checkout_requires_login(self):
        """チェックアウトにはログインが必要"""
        response = self.client.get(reverse('shop:checkout'))
        self.assertEqual(response.status_code, 302)  # ログインページへリダイレクト
        self.assertIn('/accounts/login/', response.url)
    
    def test_checkout_view_with_authenticated_user(self):
        """ログイン済みユーザーはチェックアウトページを表示できる"""
        self.client.login(username='testuser', password='testpass123')
        
        # カートに商品を追加
        cart = Cart.objects.create(user=self.user)
        CartItem.objects.create(cart=cart, product=self.product, quantity=2)
        
        response = self.client.get(reverse('shop:checkout'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'shop/checkout.html')
    
    def test_checkout_with_empty_cart_redirects(self):
        """空のカートでチェックアウトするとリダイレクト"""
        self.client.login(username='testuser', password='testpass123')
        
        response = self.client.get(reverse('shop:checkout'))
        self.assertEqual(response.status_code, 302)
        self.assertIn('cart', response.url)
    
    def test_checkout_post_creates_order(self):
        """チェックアウト送信で注文が作成される"""
        self.client.login(username='testuser', password='testpass123')
        
        # カートに商品を追加
        cart = Cart.objects.create(user=self.user)
        CartItem.objects.create(cart=cart, product=self.product, quantity=2)
        
        # チェックアウト
        response = self.client.post(reverse('shop:checkout'), {
            'shipping_name': '山田太郎',
            'shipping_postal_code': '123-4567',
            'shipping_address': '東京都渋谷区テスト1-2-3',
            'shipping_phone': '090-1234-5678'
        })
        
        # 注文完了ページにリダイレクト
        self.assertEqual(response.status_code, 302)
        
        # 注文が作成されていることを確認
        order = Order.objects.first()
        self.assertIsNotNone(order)
        self.assertEqual(order.user, self.user)
        self.assertEqual(order.shipping_name, '山田太郎')
        
        # カートが空になっていることを確認
        self.assertEqual(cart.items.count(), 0)


class OrderHistoryViewTest(TestCase):
    """注文履歴ビューのテストケース"""
    
    def setUp(self):
        """テスト前の準備"""
        self.client = Client()
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
    
    def test_order_history_requires_login(self):
        """注文履歴にはログインが必要"""
        response = self.client.get(reverse('shop:order_history'))
        self.assertEqual(response.status_code, 302)
        self.assertIn('/accounts/login/', response.url)
    
    def test_order_history_view_with_orders(self):
        """注文履歴が正しく表示される"""
        self.client.login(username='testuser', password='testpass123')
        
        # 注文を作成
        order = Order.objects.create(
            user=self.user,
            status='pending',
            total_amount=Decimal('89800'),
            shipping_name='テスト',
            shipping_postal_code='111-1111',
            shipping_address='テスト住所',
            shipping_phone='090-0000-0000'
        )
        OrderItem.objects.create(
            order=order,
            product=self.product,
            quantity=1,
            price=self.product.price
        )
        
        response = self.client.get(reverse('shop:order_history'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'shop/order_history.html')
        self.assertEqual(len(response.context['orders']), 1)
    
    def test_order_history_shows_only_user_orders(self):
        """他のユーザーの注文は表示されない"""
        self.client.login(username='testuser', password='testpass123')
        
        # 別のユーザーを作成
        other_user = User.objects.create_user(
            username='otheruser',
            password='otherpass123'
        )
        
        # 自分の注文
        Order.objects.create(
            user=self.user,
            status='pending',
            total_amount=Decimal('89800'),
            shipping_name='テスト',
            shipping_postal_code='111-1111',
            shipping_address='テスト住所',
            shipping_phone='090-0000-0000'
        )
        
        # 他のユーザーの注文
        Order.objects.create(
            user=other_user,
            status='pending',
            total_amount=Decimal('50000'),
            shipping_name='他のユーザー',
            shipping_postal_code='222-2222',
            shipping_address='他の住所',
            shipping_phone='090-9999-9999'
        )
        
        response = self.client.get(reverse('shop:order_history'))
        self.assertEqual(len(response.context['orders']), 1)


class OrderDetailViewTest(TestCase):
    """注文詳細ビューのテストケース"""
    
    def setUp(self):
        """テスト前の準備"""
        self.client = Client()
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
            status='pending',
            total_amount=Decimal('89800'),
            shipping_name='テスト',
            shipping_postal_code='111-1111',
            shipping_address='テスト住所',
            shipping_phone='090-0000-0000'
        )
        OrderItem.objects.create(
            order=self.order,
            product=self.product,
            quantity=1,
            price=self.product.price
        )
    
    def test_order_detail_requires_login(self):
        """注文詳細にはログインが必要"""
        response = self.client.get(
            reverse('shop:order_detail', kwargs={'order_id': self.order.id})
        )
        self.assertEqual(response.status_code, 302)
        self.assertIn('/accounts/login/', response.url)
    
    def test_order_detail_view(self):
        """注文詳細が正しく表示される"""
        self.client.login(username='testuser', password='testpass123')
        
        response = self.client.get(
            reverse('shop:order_detail', kwargs={'order_id': self.order.id})
        )
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'shop/order_detail.html')
        self.assertEqual(response.context['order'].id, self.order.id)
    
    def test_order_detail_other_user_forbidden(self):
        """他のユーザーの注文は表示できない"""
        other_user = User.objects.create_user(
            username='otheruser',
            password='otherpass123'
        )
        self.client.login(username='otheruser', password='otherpass123')
        
        response = self.client.get(
            reverse('shop:order_detail', kwargs={'order_id': self.order.id})
        )
        self.assertEqual(response.status_code, 404)
