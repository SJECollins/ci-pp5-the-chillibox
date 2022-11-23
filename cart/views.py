from django.shortcuts import render, get_object_or_404, redirect, reverse, HttpResponse
from django.contrib import messages
from django.views import View

from products.models import Product, Variant


class ViewCart(View):
    def get(self, request):
        template_name = 'cart/cart.html'
        return render(request, template_name)


def add_to_cart(request, item_id):
    product = get_object_or_404(Product, id=item_id)
    quantity = int(request.POST.get('quantity'))
    get_variant = request.POST.get('product_variant')
    variant = get_object_or_404(Variant, id=get_variant)
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


def adjust_cart(request, item_id):
    product = get_object_or_404(Product, id=item_id)
    quantity = int(request.POST.get('quantity'))
    get_variant = request.POST.get('product_variant')
    variant = get_object_or_404(Variant, id=get_variant)
    size = variant.size
    price = variant.price
    cart = request.session.get('cart', {})

    if quantity > 0:
        cart[item_id]['items_by_size'][size] = quantity
        messages.success(request, f'Updated {size} {product.name} quantity to {cart[item_id]["items_by_size"][size]}')
    else:
        del cart[item_id]['items_by_size'][size]
        if not cart[item_id]['items_by_size']:
            cart.pop(item_id)
        messages.success(request, f'Removed {size} {product.name} from cart')

    request.session['cart'] = cart
    return redirect(reverse('cart:view_cart'))


def remove_item(request, item_id):
    try:
        product = get_object_or_404(Product, id=item_id)
        get_variant = request.POST.get('product_variant')
        variant = get_object_or_404(Variant, id=get_variant)
        size = variant.size
        price = variant.price
        cart = request.session.get('cart', {})

        del cart[item_id]['items_by_size'][size]
        if not cart[item_id]['items_by_size']:
            cart.pop(item_id)
        messages.success(request, f'Removed {size} {product.name} from cart')

        request.session['cart'] = cart
        return redirect(reverse('cart:view_cart'))

    except Exception as e:
        messages.error(request, f'Error removing item: {e}')
        return HttpResponse(status=500)
