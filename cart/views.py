from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages

from products.models import Product, ProductVariant


def add_to_cart(request, item_id):
    product = get_object_or_404(Product, id=item_id)
    quantity = int(request.POST.get('quantity'))
    get_variant = request.POST.get('product_variant')
    variant = get_object_or_404(ProductVariant, id=get_variant)
    size = variant.size
    price = variant.price
    cart = request.session.get('cart', {})

    if item_id in list(cart.keys()):
        if size in cart[item_id]['items_by_size'].keys():
            cart[item_id]['items_by_size'][size] += quantity
            messages.success(request, f'Updated {size} {product.name} quantity to {cart[item_id]["items_by_size"][size]}')
        else:
            cart[item_id]['items_by_size'][size] = quantity
            messages.success(request, f'Added {size} {product.name} to cart')
    else:
        cart[item_id] = {'items_by_size': {size: quantity}}
        messages.success(request, f'Added {size} {product.name} to cart')

    request.session['cart'] = cart
    return redirect('products:product', product.slug)
