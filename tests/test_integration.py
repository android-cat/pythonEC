"""
Integration Tests
統合テスト - 完全な購入フローをテスト
"""
from decimal import Decimal
from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth.models import User
from shop.models import Category, Product, Cart, CartItem, Order


class PurchaseFlowIntegrationTest(TestCase):
    """購入フロー統合テスト"""
    
    def setUp(self):
        """テスト前の準備"""
        self.client = Client()
        self.user = User.objects.create_user(
            username='testuser',
            password='testpass123',
            email='test@example.com'
        )
        
        # カテゴリと商品を作成
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
    
    def test_complete_purchase_flow_authenticated_user(self):
        """認証済みユーザーの完全な購入フロー"""
        # 1. ログイン
        self.client.login(username='testuser', password='testpass123')
        
        # 2. 商品一覧を表示
        response = self.client.get(reverse('shop:product_list'))
        self.assertEqual(response.status_code, 200)
        
        # 3. 商品詳細を表示
        response = self.client.get(
            reverse('shop:product_detail', kwargs={'slug': self.product1.slug})
        )
        self.assertEqual(response.status_code, 200)
        
        # 4. カートに商品を追加
        response = self.client.post(
            reverse('shop:add_to_cart'),
            {'product_id': self.product1.id, 'quantity': 2}
        )
        self.assertEqual(response.status_code, 302)
        
        # 5. 別の商品もカートに追加
        response = self.client.post(
            reverse('shop:add_to_cart'),
            {'product_id': self.product2.id, 'quantity': 3}
        )
        self.assertEqual(response.status_code, 302)
        
        # 6. カートを表示
        response = self.client.get(reverse('shop:cart'))
        self.assertEqual(response.status_code, 200)
        cart = response.context['cart']
        self.assertEqual(cart.items.count(), 2)
        
        # 7. チェックアウトページを表示
        response = self.client.get(reverse('shop:checkout'))
        self.assertEqual(response.status_code, 200)
        
        # 8. 注文を作成
        initial_stock1 = self.product1.stock
        initial_stock2 = self.product2.stock
        
        response = self.client.post(reverse('shop:checkout'), {
            'shipping_name': '山田太郎',
            'shipping_postal_code': '123-4567',
            'shipping_address': '東京都渋谷区テスト1-2-3',
            'shipping_phone': '090-1234-5678'
        })
        
        # 注文完了ページにリダイレクト
        self.assertEqual(response.status_code, 302)
        
        # 9. 注文が作成されたことを確認
        order = Order.objects.filter(user=self.user).first()
        self.assertIsNotNone(order)
        self.assertEqual(order.items.count(), 2)
        
        # 在庫が減っていることを確認
        self.product1.refresh_from_db()
        self.product2.refresh_from_db()
        self.assertEqual(self.product1.stock, initial_stock1 - 2)
        self.assertEqual(self.product2.stock, initial_stock2 - 3)
        
        # カートが空になっていることを確認
        cart.refresh_from_db()
        self.assertEqual(cart.items.count(), 0)
        
        # 10. 注文履歴を表示
        response = self.client.get(reverse('shop:order_history'))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.context['orders']), 1)
        
        # 11. 注文詳細を表示
        response = self.client.get(
            reverse('shop:order_detail', kwargs={'order_id': order.id})
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context['order'].id, order.id)
    
    def test_guest_to_user_cart_migration(self):
        """ゲストカートがログイン後にユーザーカートに移行される"""
        # 1. ゲストとして商品をカートに追加
        response = self.client.post(
            reverse('shop:add_to_cart'),
            {'product_id': self.product1.id, 'quantity': 2}
        )
        self.assertEqual(response.status_code, 302)
        
        # ゲストカートが作成されていることを確認
        session_key = self.client.session.session_key
        guest_cart = Cart.objects.filter(session_key=session_key).first()
        self.assertIsNotNone(guest_cart)
        self.assertEqual(guest_cart.items.count(), 1)
        
        # 2. ログイン
        response = self.client.post(reverse('accounts:login'), {
            'username': 'testuser',
            'password': 'testpass123'
        })
        
        # 3. カートを表示
        response = self.client.get(reverse('shop:cart'))
        self.assertEqual(response.status_code, 200)
        
        # ユーザーカートに商品がマージされていることを確認
        user_cart = Cart.objects.filter(user=self.user).first()
        self.assertIsNotNone(user_cart)
        self.assertEqual(user_cart.items.count(), 1)
        
        # ゲストカートは削除されている
        self.assertFalse(Cart.objects.filter(session_key=session_key).exists())
    
    def test_cart_quantity_update_flow(self):
        """カート内の商品数量を更新するフロー"""
        # ログイン
        self.client.login(username='testuser', password='testpass123')
        
        # カートに商品を追加
        self.client.post(
            reverse('shop:add_to_cart'),
            {'product_id': self.product1.id, 'quantity': 2}
        )
        
        cart = Cart.objects.get(user=self.user)
        cart_item = cart.items.first()
        
        # 数量を更新
        response = self.client.post(
            reverse('shop:update_cart_item', kwargs={'item_id': cart_item.id}),
            {'quantity': 5}
        )
        self.assertEqual(response.status_code, 302)
        
        # 数量が更新されていることを確認
        cart_item.refresh_from_db()
        self.assertEqual(cart_item.quantity, 5)
    
    def test_remove_item_from_cart_flow(self):
        """カートから商品を削除するフロー"""
        # ログイン
        self.client.login(username='testuser', password='testpass123')
        
        # カートに2つの商品を追加
        self.client.post(
            reverse('shop:add_to_cart'),
            {'product_id': self.product1.id, 'quantity': 2}
        )
        self.client.post(
            reverse('shop:add_to_cart'),
            {'product_id': self.product2.id, 'quantity': 1}
        )
        
        cart = Cart.objects.get(user=self.user)
        self.assertEqual(cart.items.count(), 2)
        
        # 1つ目の商品を削除
        cart_item = cart.items.first()
        response = self.client.post(
            reverse('shop:remove_from_cart', kwargs={'item_id': cart_item.id})
        )
        self.assertEqual(response.status_code, 302)
        
        # 商品が削除されていることを確認
        cart.refresh_from_db()
        self.assertEqual(cart.items.count(), 1)
    
    def test_checkout_with_empty_cart_redirects(self):
        """空のカートでチェックアウトしようとするとリダイレクト"""
        self.client.login(username='testuser', password='testpass123')
        
        response = self.client.get(reverse('shop:checkout'))
        self.assertEqual(response.status_code, 302)
        self.assertIn('cart', response.url)
    
    def test_order_total_calculation_in_flow(self):
        """購入フロー全体での合計金額の計算"""
        self.client.login(username='testuser', password='testpass123')
        
        # カートに商品を追加
        self.client.post(
            reverse('shop:add_to_cart'),
            {'product_id': self.product1.id, 'quantity': 1}
        )
        self.client.post(
            reverse('shop:add_to_cart'),
            {'product_id': self.product2.id, 'quantity': 2}
        )
        
        # 期待される合計金額
        expected_total = (self.product1.price * 1) + (self.product2.price * 2)
        
        # カートページで合計金額を確認
        response = self.client.get(reverse('shop:cart'))
        cart = response.context['cart']
        self.assertEqual(cart.total_price, expected_total)
        
        # 注文を作成
        self.client.post(reverse('shop:checkout'), {
            'shipping_name': 'テスト',
            'shipping_postal_code': '111-1111',
            'shipping_address': 'テスト住所',
            'shipping_phone': '090-0000-0000'
        })
        
        # 注文の合計金額を確認
        order = Order.objects.get(user=self.user)
        self.assertEqual(order.total_amount, expected_total)
