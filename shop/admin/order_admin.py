"""
Order Admin - 注文管理画面
"""
from django.contrib import admin
from shop.models import Order, OrderItem


class OrderItemInline(admin.TabularInline):
    """注文商品インライン"""
    model = OrderItem
    extra = 0
    readonly_fields = ['product', 'quantity', 'price', 'subtotal']
    
    def subtotal(self, obj):
        """小計"""
        return f"¥{obj.subtotal:,}"
    subtotal.short_description = '小計'


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    """注文管理"""
    list_display = ['id', 'user', 'status', 'total_amount_formatted', 'created_at']
    list_filter = ['status', 'created_at']
    list_editable = ['status']
    search_fields = ['user__username', 'shipping_name', 'shipping_phone']
    readonly_fields = ['created_at', 'updated_at', 'total_amount']
    inlines = [OrderItemInline]
    
    fieldsets = (
        ('注文情報', {
            'fields': ('user', 'status', 'total_amount')
        }),
        ('配送先情報', {
            'fields': ('shipping_name', 'shipping_postal_code', 'shipping_address', 'shipping_phone')
        }),
        ('日時情報', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
    
    def total_amount_formatted(self, obj):
        """合計金額（フォーマット済み）"""
        return f"¥{obj.total_amount:,}"
    total_amount_formatted.short_description = '合計金額'
    total_amount_formatted.admin_order_field = 'total_amount'
