"""
Context Processors - コンテキストプロセッサ
"""
from shop.models import Cart


def cart_context(request):
    """
    カート情報をコンテキストに追加
    全てのテンプレートでカート情報を利用可能にする
    """
    cart = None
    if request.user.is_authenticated:
        try:
            cart = Cart.objects.get(user=request.user)
        except Cart.DoesNotExist:
            pass
    elif request.session.session_key:
        try:
            cart = Cart.objects.get(session_key=request.session.session_key)
        except Cart.DoesNotExist:
            pass
    
    return {
        'cart': cart,
        'cart_total_items': cart.total_items if cart else 0,
    }
