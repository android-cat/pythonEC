"""
Order Service - 注文関連のビジネスロジック
"""
from django.db import transaction
from shop.models import Order, OrderItem


class OrderService:
    """注文管理サービス"""
    
    @staticmethod
    @transaction.atomic
    def create_order_from_cart(user, cart, shipping_data):
        """
        カートから注文を作成
        在庫を減らし、カートをクリアする
        """
        # 注文を作成
        order = Order.objects.create(
            user=user,
            total_amount=cart.total_price,
            shipping_name=shipping_data['shipping_name'],
            shipping_postal_code=shipping_data['shipping_postal_code'],
            shipping_address=shipping_data['shipping_address'],
            shipping_phone=shipping_data['shipping_phone'],
        )
        
        # 注文商品を作成
        for item in cart.items.all():
            OrderItem.objects.create(
                order=order,
                product=item.product,
                quantity=item.quantity,
                price=item.product.price,
            )
            
            # 在庫を減らす
            item.product.stock -= item.quantity
            item.product.save()
        
        # カートをクリア
        cart.items.all().delete()
        
        return order
    
    @staticmethod
    @transaction.atomic
    def cancel_order(order):
        """
        注文をキャンセルし、在庫を戻す
        """
        if order.status in ['delivered', 'cancelled']:
            raise ValueError('配達済みまたはキャンセル済みの注文はキャンセルできません')
        
        # 在庫を戻す
        for item in order.items.all():
            item.product.stock += item.quantity
            item.product.save()
        
        # ステータスを更新
        order.status = 'cancelled'
        order.save()
        
        return order
    
    @staticmethod
    def update_order_status(order, new_status):
        """注文ステータスを更新"""
        valid_statuses = dict(Order.STATUS_CHOICES).keys()
        if new_status not in valid_statuses:
            raise ValueError(f'無効なステータス: {new_status}')
        
        order.status = new_status
        order.save()
        return order
