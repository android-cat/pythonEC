"""
Test Category Model
カテゴリモデルのテスト
"""
from django.test import TestCase
from shop.models import Category


class CategoryModelTest(TestCase):
    """カテゴリモデルのテストケース"""
    
    def setUp(self):
        """テスト前の準備"""
        self.category = Category.objects.create(
            name='電子機器',
            slug='electronics',
            description='電子機器のカテゴリ'
        )
    
    def test_category_creation(self):
        """カテゴリが正しく作成されることを確認"""
        self.assertEqual(self.category.name, '電子機器')
        self.assertEqual(self.category.slug, 'electronics')
        self.assertIsNotNone(self.category.created_at)
        self.assertIsNotNone(self.category.updated_at)
    
    def test_category_str(self):
        """__str__メソッドが正しく動作することを確認"""
        self.assertEqual(str(self.category), '電子機器')
    
    def test_category_slug_unique(self):
        """スラッグがユニークであることを確認"""
        from django.db import IntegrityError
        with self.assertRaises(IntegrityError):
            Category.objects.create(
                name='電子機器2',
                slug='electronics'  # 重複
            )
    
    def test_category_ordering(self):
        """カテゴリが名前順にソートされることを確認"""
        Category.objects.create(name='書籍', slug='books')
        Category.objects.create(name='衣料品', slug='clothing')
        
        categories = list(Category.objects.all())
        self.assertEqual(categories[0].name, '書籍')
        self.assertEqual(categories[1].name, '衣料品')
        self.assertEqual(categories[2].name, '電子機器')
