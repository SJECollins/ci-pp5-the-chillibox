from datetime import datetime, timedelta
from decimal import Decimal
from django.conf import settings
from django.shortcuts import get_object_or_404

from products.models import Product, Variant
from .models import HeldCart


def cart_contents(request):
    """
    Function for cart contents, to make available across site.
    Based on CI's Boutique ado
    https://github.com/Code-Institute-Solutions/boutique_ado_v1
    """

    cart_items = []
    total = 0
    product_count = 0
    checkout_time = 0
    cart = request.session.get('cart', {})
    cart_key = request.session.session_key
    try:
        held_cart = HeldCart.objects.get(cart_key=cart_key)
        hold_start_time = held_cart.hold_time_start
        checkout_time = (hold_start_time + timedelta(hours=2)).strftime('%H:%M')  # noqa
        if held_cart.check_time():
            if 'cart' in request.session:
                del request.session['cart']
                request.session.cycle_key()
    except HeldCart.DoesNotExist:
        checkout_time is None

    for item_id, item_data in cart.items():
        if isinstance(item_data, int):
            product = get_object_or_404(Product, id=item_id)
            total += item_data * price
            product_count += item_data
            cart_items.append({
                'item_id': item_id,
                'quantity': item_data,
                'product': product,
            })
        else:
            product = get_object_or_404(Product, pk=item_id)
            for size, quantity in item_data['items_by_size'].items():
                variant = product.variants.get(size=size)
                total += quantity * variant.price
                product_count += quantity
                cart_items.append({
                    'item_id': item_id,
                    'quantity': quantity,
                    'product': product,
                    'variant': variant,
                    'size': size,
                })

    if total < settings.FREE_DELIVERY_THRESHOLD:
        delivery = Decimal(settings.STANDARD_DELIVERY_COST)
        free_delivery_delta = settings.FREE_DELIVERY_THRESHOLD - total
    else:
        delivery = 0
        free_delivery_delta = 0

    grand_total = delivery + total

    context = {
        'checkout_time': checkout_time,
        'cart_items': cart_items,
        'total': total,
        'product_count': product_count,
        'delivery': delivery,
        'free_delivery_delta': free_delivery_delta,
        'free_delivery_threshold': settings.FREE_DELIVERY_THRESHOLD,
        'grand_total': grand_total,
    }

    return context
