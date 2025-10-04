"""
Product Views - 商品表示関連
"""
from django.shortcuts import get_object_or_404
from django.views.generic import ListView, DetailView
from shop.models import Product, Category


class ProductListView(ListView):
    """商品一覧ビュー"""
    model = Product
    template_name = 'shop/product_list.html'
    context_object_name = 'products'
    paginate_by = 12

    def get_queryset(self):
        """販売中の商品を取得、カテゴリでフィルター"""
        queryset = Product.objects.filter(is_active=True)
        category_slug = self.kwargs.get('category_slug')
        if category_slug:
            queryset = queryset.filter(category__slug=category_slug)
        return queryset

    def get_context_data(self, **kwargs):
        """コンテキストにカテゴリ情報を追加"""
        context = super().get_context_data(**kwargs)
        context['categories'] = Category.objects.all()
        category_slug = self.kwargs.get('category_slug')
        if category_slug:
            context['current_category'] = get_object_or_404(Category, slug=category_slug)
        return context


class ProductDetailView(DetailView):
    """商品詳細ビュー"""
    model = Product
    template_name = 'shop/product_detail.html'
    context_object_name = 'product'
    slug_field = 'slug'
    slug_url_kwarg = 'slug'
