"""
Product Admin - 商品管理画面
"""
from django.contrib import admin
from shop.models import Category, Product


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    """カテゴリ管理"""
    list_display = ['name', 'slug', 'created_at']
    prepopulated_fields = {'slug': ('name',)}
    search_fields = ['name']


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    """商品管理"""
    list_display = ['name', 'category', 'price', 'stock', 'is_active', 'created_at']
    list_filter = ['is_active', 'category', 'created_at']
    list_editable = ['price', 'stock', 'is_active']
    prepopulated_fields = {'slug': ('name',)}
    search_fields = ['name', 'description']
    readonly_fields = ['created_at', 'updated_at']
    
    fieldsets = (
        ('基本情報', {
            'fields': ('name', 'slug', 'category', 'description')
        }),
        ('価格・在庫', {
            'fields': ('price', 'stock', 'is_active')
        }),
        ('画像', {
            'fields': ('image',)
        }),
        ('日時情報', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
