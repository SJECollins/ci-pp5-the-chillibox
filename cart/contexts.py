from decimal import Decimal
from django.conf import settings
from django.shortcuts import get_object_or_404

from products.models import Product, ProductVariant


def cart_contents(request):

    cart_items = []
    total = 0
    product_count = 0
    cart = request.session.get('cart', {})

    for item_id, item_data in cart.items():
        if isinstance(item_data, int):
            product = get_object_or_404(Product, id=item_id)
            variant = get_object_or_404(ProductVariant, variants=product)
            total += item_data * variant.price
            product_count += item_data
            cart_items.append({
                'item_id': item_id,
                'quantity': item_data,
                'product': product,
                'variant': variant,
            })
        else:
            product = get_object_or_404(Product, pk=item_id)
            variant = get_object_or_404(ProductVariant, variants=product)
            for size, quantity in item_data['items_by_size'].items():
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
        'cart_items': cart_items,
        'total': total,
        'product_count': product_count,
        'delivery': delivery,
        'free_delivery_delta': free_delivery_delta,
        'free_delivery_threshold': settings.FREE_DELIVERY_THRESHOLD,
        'grand_total': grand_total,
    }

    return context
