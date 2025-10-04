"""
Test Cart Service
カートサービスのテスト
"""
from decimal import Decimal
from django.test import TestCase, RequestFactory
from django.contrib.auth.models import User
from django.contrib.sessions.middleware import SessionMiddleware
from shop.models import Category, Product, Cart, CartItem
from shop.services import CartService


class CartServiceTest(TestCase):
    """カートサービスのテストケース"""
    
    def setUp(self):
        """テスト前の準備"""
        self.factory = RequestFactory()
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
    
    def _add_session_to_request(self, request):
        """リクエストにセッションを追加"""
        middleware = SessionMiddleware(lambda x: None)
        middleware.process_request(request)
        request.session.save()
    
    def test_get_or_create_cart_for_authenticated_user(self):
        """認証済みユーザーのカート取得/作成をテスト"""
        request = self.factory.get('/')
        request.user = self.user
        self._add_session_to_request(request)
        
        cart = CartService.get_or_create_cart(request)
        
        self.assertIsNotNone(cart)
        self.assertEqual(cart.user, self.user)
        self.assertIsNone(cart.session_key)
        
        # 同じリクエストで再度呼び出すと同じカートを取得
        cart2 = CartService.get_or_create_cart(request)
        self.assertEqual(cart.id, cart2.id)
    
    def test_get_or_create_cart_for_guest(self):
        """ゲストユーザーのカート取得/作成をテスト"""
        request = self.factory.get('/')
        request.user = User()  # AnonymousUser
        self._add_session_to_request(request)
        
        cart = CartService.get_or_create_cart(request)
        
        self.assertIsNotNone(cart)
        self.assertIsNone(cart.user)
        self.assertIsNotNone(cart.session_key)
        self.assertEqual(cart.session_key, request.session.session_key)
    
    def test_clear_cart(self):
        """カートクリア機能をテスト"""
        cart = Cart.objects.create(user=self.user)
        CartItem.objects.create(cart=cart, product=self.product, quantity=2)
        
        self.assertEqual(cart.items.count(), 1)
        
        CartService.clear_cart(cart)
        
        self.assertEqual(cart.items.count(), 0)
    
    def test_merge_guest_cart_to_user(self):
        """ゲストカートをユーザーカートにマージする機能をテスト"""
        # ゲストカートを作成
        guest_cart = Cart.objects.create(session_key='guest_session_123')
        CartItem.objects.create(cart=guest_cart, product=self.product, quantity=2)
        
        # リクエストを作成
        request = self.factory.get('/')
        request.user = self.user
        request.session = {'session_key': 'guest_session_123'}
        request.session.session_key = 'guest_session_123'
        
        # マージ実行
        CartService.merge_guest_cart_to_user(request, self.user)
        
        # ゲストカートが削除されていることを確認
        self.assertFalse(Cart.objects.filter(session_key='guest_session_123').exists())
        
        # ユーザーカートに商品がマージされていることを確認
        user_cart = Cart.objects.get(user=self.user)
        self.assertEqual(user_cart.items.count(), 1)
        self.assertEqual(user_cart.items.first().quantity, 2)
    
    def test_merge_guest_cart_adds_to_existing_user_cart(self):
        """既存のユーザーカートにゲストカートの商品を追加"""
        # ユーザーカートを作成
        user_cart = Cart.objects.create(user=self.user)
        CartItem.objects.create(cart=user_cart, product=self.product, quantity=1)
        
        # ゲストカートを作成（同じ商品）
        guest_cart = Cart.objects.create(session_key='guest_session_123')
        CartItem.objects.create(cart=guest_cart, product=self.product, quantity=3)
        
        # リクエストを作成
        request = self.factory.get('/')
        request.user = self.user
        request.session = {'session_key': 'guest_session_123'}
        request.session.session_key = 'guest_session_123'
        
        # マージ実行
        CartService.merge_guest_cart_to_user(request, self.user)
        
        # 数量が加算されていることを確認
        user_cart.refresh_from_db()
        cart_item = user_cart.items.get(product=self.product)
        self.assertEqual(cart_item.quantity, 4)  # 1 + 3
