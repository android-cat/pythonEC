"""
Order Views - 注文関連
"""
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from shop.models import Order, OrderItem
from shop.forms import OrderForm
from shop.services.cart_service import CartService
from shop.services.order_service import OrderService


@login_required
def checkout(request):
    """チェックアウトビュー"""
    cart = CartService.get_or_create_cart(request)
    
    if not cart.items.exists():
        messages.warning(request, 'カートが空です。')
        return redirect('shop:cart')
    
    if request.method == 'POST':
        form = OrderForm(request.POST)
        if form.is_valid():
            # 注文を作成
            order = OrderService.create_order_from_cart(
                user=request.user,
                cart=cart,
                shipping_data=form.cleaned_data
            )
            
            messages.success(request, '注文が完了しました。')
            return redirect('shop:order_complete', order_id=order.id)
    else:
        form = OrderForm()
    
    return render(request, 'shop/checkout.html', {'form': form, 'cart': cart})


@login_required
def order_complete(request, order_id):
    """注文完了ビュー"""
    order = get_object_or_404(Order, id=order_id, user=request.user)
    return render(request, 'shop/order_complete.html', {'order': order})


@login_required
def order_history(request):
    """注文履歴ビュー"""
    orders = Order.objects.filter(user=request.user)
    return render(request, 'shop/order_history.html', {'orders': orders})


@login_required
def order_detail(request, order_id):
    """注文詳細ビュー"""
    order = get_object_or_404(Order, id=order_id, user=request.user)
    return render(request, 'shop/order_detail.html', {'order': order})
