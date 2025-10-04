"""
Cart Views - カート関連
"""
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from shop.models import Product, CartItem
from shop.services.cart_service import CartService


def cart_view(request):
    """カート表示ビュー"""
    cart = CartService.get_or_create_cart(request)
    return render(request, 'shop/cart.html', {'cart': cart})


def add_to_cart(request, product_id):
    """カートに商品を追加"""
    product = get_object_or_404(Product, id=product_id)
    cart = CartService.get_or_create_cart(request)
    
    cart_item, created = CartItem.objects.get_or_create(
        cart=cart,
        product=product,
        defaults={'quantity': 1}
    )
    
    if not created:
        cart_item.quantity += 1
        cart_item.save()
    
    messages.success(request, f'{product.name}をカートに追加しました。')
    return redirect('shop:cart')


def update_cart_item(request, item_id):
    """カート商品の数量を更新"""
    cart_item = get_object_or_404(CartItem, id=item_id)
    quantity = int(request.POST.get('quantity', 1))
    
    if quantity > 0:
        cart_item.quantity = quantity
        cart_item.save()
        messages.success(request, '数量を更新しました。')
    else:
        cart_item.delete()
        messages.success(request, '商品をカートから削除しました。')
    
    return redirect('shop:cart')


def remove_from_cart(request, item_id):
    """カートから商品を削除"""
    cart_item = get_object_or_404(CartItem, id=item_id)
    cart_item.delete()
    messages.success(request, '商品をカートから削除しました。')
    return redirect('shop:cart')
