"""
Cart Service - カート関連のビジネスロジック
"""
from shop.models import Cart


class CartService:
    """カート管理サービス"""
    
    @staticmethod
    def get_or_create_cart(request):
        """
        カートを取得または作成
        ログインユーザーはuser_id、ゲストはsession_keyで識別
        """
        if request.user.is_authenticated:
            cart, created = Cart.objects.get_or_create(user=request.user)
        else:
            if not request.session.session_key:
                request.session.create()
            session_key = request.session.session_key
            cart, created = Cart.objects.get_or_create(session_key=session_key)
        return cart
    
    @staticmethod
    def merge_guest_cart_to_user(request, user):
        """
        ゲストカートをログインユーザーのカートにマージ
        ログイン時に使用
        """
        if request.session.session_key:
            try:
                guest_cart = Cart.objects.get(session_key=request.session.session_key)
                user_cart, created = Cart.objects.get_or_create(user=user)
                
                # ゲストカートの商品をユーザーカートにマージ
                for item in guest_cart.items.all():
                    user_item, created = user_cart.items.get_or_create(
                        product=item.product,
                        defaults={'quantity': item.quantity}
                    )
                    if not created:
                        user_item.quantity += item.quantity
                        user_item.save()
                
                # ゲストカートを削除
                guest_cart.delete()
                
            except Cart.DoesNotExist:
                pass
    
    @staticmethod
    def clear_cart(cart):
        """カートを空にする"""
        cart.items.all().delete()
