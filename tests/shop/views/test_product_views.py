"""
Test Product Views
商品ビューのテスト
"""
from decimal import Decimal
from django.test import TestCase, Client
from django.urls import reverse
from shop.models import Category, Product


class ProductListViewTest(TestCase):
    """商品一覧ビューのテストケース"""
    
    def setUp(self):
        """テスト前の準備"""
        self.client = Client()
        self.category1 = Category.objects.create(
            name='電子機器',
            slug='electronics'
        )
        self.category2 = Category.objects.create(
            name='書籍',
            slug='books'
        )
        
        # 複数の商品を作成
        for i in range(15):
            Product.objects.create(
                name=f'商品{i+1}',
                slug=f'product-{i+1}',
                category=self.category1 if i < 10 else self.category2,
                description=f'商品{i+1}の説明',
                price=Decimal(f'{(i+1)*1000}'),
                stock=10
            )
    
    def test_product_list_view_status_code(self):
        """商品一覧ページが正常に表示されることを確認"""
        response = self.client.get(reverse('shop:product_list'))
        self.assertEqual(response.status_code, 200)
    
    def test_product_list_view_uses_correct_template(self):
        """正しいテンプレートが使用されていることを確認"""
        response = self.client.get(reverse('shop:product_list'))
        self.assertTemplateUsed(response, 'shop/product_list.html')
    
    def test_product_list_view_pagination(self):
        """ページネーションが機能していることを確認"""
        response = self.client.get(reverse('shop:product_list'))
        self.assertEqual(len(response.context['products']), 12)  # 1ページあたり12商品
        
        # 2ページ目
        response = self.client.get(reverse('shop:product_list') + '?page=2')
        self.assertEqual(len(response.context['products']), 3)  # 残り3商品
    
    def test_product_list_view_filter_by_category(self):
        """カテゴリでフィルタリングできることを確認"""
        response = self.client.get(reverse('shop:product_list'), {'category': 'electronics'})
        self.assertEqual(response.context['products'].count(), 10)
        
        for product in response.context['products']:
            self.assertEqual(product.category, self.category1)
    
    def test_product_list_view_context_has_categories(self):
        """コンテキストにカテゴリ一覧が含まれることを確認"""
        response = self.client.get(reverse('shop:product_list'))
        self.assertIn('categories', response.context)
        self.assertEqual(response.context['categories'].count(), 2)


class ProductDetailViewTest(TestCase):
    """商品詳細ビューのテストケース"""
    
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
    
    def test_product_detail_view_status_code(self):
        """商品詳細ページが正常に表示されることを確認"""
        response = self.client.get(
            reverse('shop:product_detail', kwargs={'slug': self.product.slug})
        )
        self.assertEqual(response.status_code, 200)
    
    def test_product_detail_view_uses_correct_template(self):
        """正しいテンプレートが使用されていることを確認"""
        response = self.client.get(
            reverse('shop:product_detail', kwargs={'slug': self.product.slug})
        )
        self.assertTemplateUsed(response, 'shop/product_detail.html')
    
    def test_product_detail_view_context(self):
        """コンテキストに商品が含まれることを確認"""
        response = self.client.get(
            reverse('shop:product_detail', kwargs={'slug': self.product.slug})
        )
        self.assertEqual(response.context['product'].id, self.product.id)
        self.assertEqual(response.context['product'].name, 'ノートPC')
    
    def test_product_detail_view_not_found(self):
        """存在しない商品でエラーが発生することを確認"""
        response = self.client.get(
            reverse('shop:product_detail', kwargs={'slug': 'nonexistent'})
        )
        self.assertEqual(response.status_code, 404)
