from django.shortcuts import render, get_object_or_404, redirect, reverse, HttpResponse
from django.contrib import messages
from django.views import View

from products.models import Product, Variant
from .models import HeldCart, HeldItems


class ViewCart(View):
    def get(self, request):
        template_name = 'cart/cart.html'
        return render(request, template_name)


def add_to_cart(request, item_id):
    product = get_object_or_404(Product, id=item_id)
    quantity = int(request.POST.get('quantity'))
    get_variant = request.POST.get('product_variant')
    variant = product.variants.get(id=get_variant)
    size = variant.size
    price = variant.price
    cart = request.session.get('cart', {})
    if not request.session.session_key:
        request.session.save()
    session_key = request.session.session_key
    held_cart = HeldCart.objects.get_or_create(cart_key=session_key)
    if request.user.is_authenticated:
        get_held_cart.owner = request.user
        get_held_cart.save()
    held_cart = HeldCart.objects.get(cart_key=session_key)

    if item_id in list(cart.keys()):
        held_variant = held_cart.held_items.get(variant__id=get_variant)
        if size in cart[item_id]['items_by_size'].keys():
            cart[item_id]['items_by_size'][size] += quantity
            held_variant.qty += quantity
            held_variant.save()
            messages.success(request, f'Updated {size} {product.name} quantity to {cart[item_id]["items_by_size"][size]}')
        else:
            cart[item_id]['items_by_size'][size] = quantity
            held_variant.qty = quantity
            held_variant.save()
            messages.success(request, f'Added {size} {product.name} to cart')
    else:
        cart[item_id] = {'items_by_size': {size: quantity}}
        held_item = HeldItems(
            cart=held_cart,
            product=product,
            variant=variant,
            qty=quantity,
        )
        held_item.save()
        messages.success(request, f'Added {size} {product.name} to cart')

    print(cart[item_id]['items_by_size'][size])
    print(cart[item_id]['items_by_size'])

    request.session['cart'] = cart
    return redirect('products:product', product.slug)


def adjust_cart(request, item_id):
    product = get_object_or_404(Product, id=item_id)
    new_quantity = int(request.POST.get('quantity'))
    get_variant = request.POST.get('product_variant')
    variant = product.variants.get(id=get_variant)
    size = variant.size
    price = variant.price
    cart = request.session.get('cart', {})
    held_cart = HeldCart.objects.get(cart_key=request.session.session_key)
    held_variant = held_cart.held_items.get(variant=variant)
    print(held_variant)
    print(held_variant.qty)

    if new_quantity > cart[item_id]['items_by_size'][size]:
        cart[item_id]['items_by_size'][size] = new_quantity
        held_variant.qty = new_quantity
        print(held_variant.qty)
        messages.success(request, f'Increased {size} {product.name} quantity to {cart[item_id]["items_by_size"][size]}')
    elif new_quantity < cart[item_id]['items_by_size'][size]:
        cart[item_id]['items_by_size'][size] = new_quantity
        held_variant.qty = new_quantity
        print(held_variant.qty)
        messages.success(request, f'Reduced {size} {product.name} quantity to {cart[item_id]["items_by_size"][size]}')

    held_variant.save()
    request.session['cart'] = cart
    return redirect(reverse('cart:view_cart'))


def remove_item(request, item_id):
    try:
        product = get_object_or_404(Product, id=item_id)
        get_variant = request.POST.get('product_variant')
        variant = product.variants.get(id=get_variant)
        size = variant.size
        price = variant.price
        cart = request.session.get('cart', {})
        held_cart = HeldCart.objects.get(cart_key=request.session.session_key)
        held_variant = held_cart.held_items.get(variant=variant)

        held_variant.delete()
        del cart[item_id]['items_by_size'][size]

        if not cart[item_id]['items_by_size']:
            cart.pop(item_id)
        messages.success(request, f'Removed {size} {product.name} from cart')

        request.session['cart'] = cart
        return redirect(reverse('cart:view_cart'))

    except Exception as e:
        messages.error(request, f'Error removing item: {e}')
        return HttpResponse(status=500)


class ViewHeld(View):
    def get(self, request):
        session_key = request.session.session_key
        held_items = HeldCart.objects.all()
        template_name = 'cart/view_held.html'
        context = {
            'held_items': held_items,
            'session_key': session_key,
            }
        return render(request, template_name, context)
