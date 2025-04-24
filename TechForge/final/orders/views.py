from django.shortcuts import get_object_or_404, render, redirect
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from django.contrib import messages
from products.models import Product
from .models import Cart, CartItem


def get_user_cart(request):
    if request.user.is_authenticated:
        cart, created = Cart.objects.get_or_create(user=request.user)
    else:
        session_key = request.session.session_key
        if not session_key:
            request.session.create()
            session_key = request.session.session_key
        cart, created = Cart.objects.get_or_create(session_key=session_key)
    return cart


@require_POST
@csrf_exempt
def add_to_cart(request, product_id):
    try:
        product = get_object_or_404(Product, id=product_id)
        cart = get_user_cart(request)
        cart_item, created = cart.get_or_create_cart_item(product)

        if not created:
            cart_item.increase_quantity()
        else:
            cart_item.quantity = 1
            cart_item.save()

        return JsonResponse({
            'success': True,
            'cart_total': cart.total_price,
            'cart_items_count': cart.total_quantity,
            'item_quantity': cart_item.quantity,
            'item_total': cart_item.total_price
        })
    except Exception as e:
        return JsonResponse({'success': False, 'error': str(e)}, status=500)


@require_POST
@csrf_exempt
def remove_from_cart(request, item_id):
    try:
        cart_item = get_object_or_404(CartItem, id=item_id)
        cart = cart_item.cart

        if not (request.user.is_authenticated and cart.user == request.user) and \
                not (not request.user.is_authenticated and cart.session_key == request.session.session_key):
            return JsonResponse({'success': False, 'error': 'Access is denied'}, status=403)

        cart_item.delete()

        return JsonResponse({
            'success': True,
            'cart_total': cart.total_price,
            'cart_items_count': cart.total_quantity
        })
    except Exception as e:
        return JsonResponse({'success': False, 'error': str(e)}, status=500)


@require_POST
@csrf_exempt
def update_quantity(request, item_id, action):
    try:
        cart_item = get_object_or_404(CartItem, id=item_id)
        cart = cart_item.cart


        if not (request.user.is_authenticated and cart.user == request.user) and \
                not (not request.user.is_authenticated and cart.session_key == request.session.session_key):
            return JsonResponse({'success': False, 'error': 'Access is denied'}, status=403)

        if action == 'increase':
            cart_item.increase_quantity()
        elif action == 'decrease':
            cart_item.decrease_quantity()
        else:
            return JsonResponse({'success': False, 'error': 'Wrong action'}, status=400)

        return JsonResponse({
            'success': True,
            'new_quantity': cart_item.quantity,
            'item_total': cart_item.total_price,
            'cart_total': cart.total_price,
            'cart_items_count': cart.total_quantity
        })
    except Exception as e:
        return JsonResponse({'success': False, 'error': str(e)}, status=500)


def view_cart(request):
    cart = get_user_cart(request)
    context = {
        'cart': cart,
        'cart_items': cart.items.select_related('product').all() if cart else []
    }
    return render(request, 'orders/view_cart.html', context)


@login_required
def clear_cart(request):
    cart = get_user_cart(request)
    cart.items.all().delete()
    messages.success(request, 'The cart was successfully emptied')
    return redirect('orders:view_cart')


def merge_carts(session_cart, user_cart):
    if session_cart and user_cart:
        for item in session_cart.items.all():
            user_item, created = user_cart.items.get_or_create(
                product=item.product,
                defaults={'quantity': item.quantity}
            )
            if not created:
                user_item.quantity += item.quantity
                user_item.save()
        session_cart.delete()