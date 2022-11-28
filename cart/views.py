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
            variant.current_stock -= quantity
            messages.success(request, f'Updated {size} {product.name} quantity to {cart[item_id]["items_by_size"][size]}')
        else:
            cart[item_id]['items_by_size'][size] = quantity
            variant.current_stock -= quantity
            messages.success(request, f'Added {size} {product.name} to cart')
    else:
        cart[item_id] = {'items_by_size': {size: quantity}}
        variant.current_stock -= quantity
        messages.success(request, f'Added {size} {product.name} to cart')

    print(cart[item_id]['items_by_size'][size])
    print(cart[item_id]['items_by_size'])
    variant.save()
    request.session['cart'] = cart
    return redirect('products:product', product.slug)


def adjust_cart(request, item_id):
    product = get_object_or_404(Product, id=item_id)
    new_quantity = int(request.POST.get('quantity'))
    get_variant = request.POST.get('product_variant')
    variant = get_object_or_404(Variant, id=get_variant)
    size = variant.size
    price = variant.price
    cart = request.session.get('cart', {})

    if new_quantity > cart[item_id]['items_by_size'][size]:
        difference = new_quantity - cart[item_id]['items_by_size'][size]
        cart[item_id]['items_by_size'][size] = new_quantity
        variant.current_stock -= difference
        messages.success(request, f'Increased {size} {product.name} quantity to {cart[item_id]["items_by_size"][size]}')
    elif new_quantity < cart[item_id]['items_by_size'][size]:
        difference = cart[item_id]['items_by_size'][size] - new_quantity
        cart[item_id]['items_by_size'][size] = new_quantity
        variant.current_stock += difference
        messages.success(request, f'Reduced {size} {product.name} quantity to {cart[item_id]["items_by_size"][size]}')

    variant.save()
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

        variant.current_stock += int(cart[item_id]['items_by_size'][size])
        del cart[item_id]['items_by_size'][size]

        if not cart[item_id]['items_by_size']:
            cart.pop(item_id)
        messages.success(request, f'Removed {size} {product.name} from cart')

        variant.save()
        request.session['cart'] = cart
        return redirect(reverse('cart:view_cart'))

    except Exception as e:
        messages.error(request, f'Error removing item: {e}')
        return HttpResponse(status=500)
