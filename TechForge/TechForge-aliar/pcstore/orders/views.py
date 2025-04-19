from django.shortcuts import get_object_or_404, render, redirect
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from products.models import Product
from .models import Cart, CartItem


@require_POST
def add_to_cart(request, product_id):
    try:
        product = get_object_or_404(Product, id=product_id)

        # Получаем или создаем корзину для текущей сессии
        session_key = request.session.session_key
        if not session_key:
            request.session.create()
            session_key = request.session.session_key

        cart, created = Cart.objects.get_or_create(session_key=session_key)
        cart_item, item_created = CartItem.objects.get_or_create(cart=cart, product=product)

        if not item_created:
            cart_item.quantity += 1
            cart_item.save()

        return JsonResponse({'success': True})
    except Exception as e:
        return JsonResponse({'success': False, 'error': str(e)}, status=500)

def view_cart(request):
    session_key = request.session.session_key
    if not session_key:
        # Если сессии нет, создаем пустую корзину
        cart = None
    else:
        cart = Cart.objects.filter(session_key=session_key).first()

    return render(request, 'orders/view_cart.html', {'cart': cart})

def clear_cart(request):
    session_key = request.session.session_key
    if session_key:
        cart = Cart.objects.filter(session_key=session_key).first()
        if cart:
            cart.items.all().delete()
    return redirect('orders:view_cart')