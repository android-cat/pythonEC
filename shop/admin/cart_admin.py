"""
Cart Admin - カート管理画面
"""
from django.contrib import admin
from shop.models import Cart, CartItem


class CartItemInline(admin.TabularInline):
    """カート商品インライン"""
    model = CartItem
    extra = 0
    readonly_fields = ['product', 'quantity', 'created_at']


@admin.register(Cart)
class CartAdmin(admin.ModelAdmin):
    """カート管理"""
    list_display = ['id', 'user', 'session_key', 'total_items', 'created_at']
    list_filter = ['created_at']
    search_fields = ['user__username', 'session_key']
    readonly_fields = ['created_at', 'updated_at']
    inlines = [CartItemInline]
    
    def total_items(self, obj):
        """カート内商品数"""
        return obj.total_items
    total_items.short_description = '商品数'
