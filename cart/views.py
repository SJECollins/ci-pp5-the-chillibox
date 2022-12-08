from django.shortcuts import render, get_object_or_404, redirect, reverse, HttpResponse  # noqa
from django.contrib import messages
from django.views import View

from products.models import Product, Variant
from .models import HeldCart, HeldItems


class ViewCart(View):
    """
    View for cart.
    """
    def get(self, request):
        template_name = 'cart/cart.html'
        return render(request, template_name)


def add_to_cart(request, item_id):
    """
    Add to cart based on CI boutique_ado
    """
    product = get_object_or_404(Product, id=item_id)
    quantity = int(request.POST.get('quantity'))
    get_variant = request.POST.get('product_variant')
    variant = product.variants.get(id=get_variant)
    size = variant.size
    price = variant.price
    cart = request.session.get('cart', {})
    # If session_key is none, create and save a new one for HeldCart
    if not request.session.session_key:
        request.session.save()
    session_key = request.session.session_key
    # Get HeldCart to manage item quantities
    get_held_cart = HeldCart.objects.get_or_create(cart_key=session_key)
    held_cart = HeldCart.objects.get(cart_key=session_key)

    # If item's id already in cart update if same size or add a new size
    if item_id in list(cart.keys()):
        held_variant = held_cart.held_items.get(variant__id=get_variant)
        if size in cart[item_id]['items_by_size'].keys():
            cart[item_id]['items_by_size'][size] += quantity
            held_variant.qty += quantity
            held_variant.save()
            messages.success(request, f'Updated {size} {product.name} quantity\
                             to {cart[item_id]["items_by_size"][size]}')
        else:
            cart[item_id]['items_by_size'][size] = quantity
            held_variant.qty = quantity
            held_variant.save()
            messages.success(request, f'Added {size} {product.name} to cart')
    else:
        # Add the item to the cart, and create a new item in HeldItems
        cart[item_id] = {'items_by_size': {size: quantity}}
        held_item = HeldItems(
            cart=held_cart,
            product=product,
            variant=variant,
            qty=quantity,
        )
        held_item.save()
        messages.success(request, f'Added {size} {product.name} to cart')

    request.session['cart'] = cart
    return redirect('products:product', product.slug)


def adjust_cart(request, item_id):
    """
    Adjust cart based on CI boutique_ado
    """
    product = get_object_or_404(Product, id=item_id)
    new_quantity = int(request.POST.get('quantity'))
    get_variant = request.POST.get('product_variant')
    variant = product.variants.get(id=get_variant)
    size = variant.size
    price = variant.price
    cart = request.session.get('cart', {})
    held_cart = HeldCart.objects.get(cart_key=request.session.session_key)
    held_variant = held_cart.held_items.get(variant=variant)

    # Set quantities for items in cart and the held variant
    if new_quantity > cart[item_id]['items_by_size'][size]:
        cart[item_id]['items_by_size'][size] = new_quantity
        held_variant.qty = new_quantity
        messages.success(request, f'Increased {size} {product.name} quantity \
                         to {cart[item_id]["items_by_size"][size]}')
    elif new_quantity < cart[item_id]['items_by_size'][size]:
        cart[item_id]['items_by_size'][size] = new_quantity
        held_variant.qty = new_quantity
        messages.success(request, f'Reduced {size} {product.name} quantity to \
                         {cart[item_id]["items_by_size"][size]}')

    held_variant.save()
    request.session['cart'] = cart
    return redirect(reverse('cart:view_cart'))


def remove_item(request, item_id):
    """
    Remove item from cart based on CI boutique_ado
    """
    try:
        product = get_object_or_404(Product, id=item_id)
        get_variant = request.POST.get('product_variant')
        variant = product.variants.get(id=get_variant)
        size = variant.size
        price = variant.price
        cart = request.session.get('cart', {})
        held_cart = HeldCart.objects.get(cart_key=request.session.session_key)
        held_variant = held_cart.held_items.get(variant=variant)

        # Restock and delete the held variant when removed
        variant.current_stock += cart[item_id]['items_by_size'][size]
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


def clear_cart(request):
    if 'cart' in request.session:
        try:
            held_cart = get_object_or_404(HeldCart, cart_key=request.session.session_key)  # noqa
            for held_item in held_cart.held_items.all():
                variant = Variant.objects.get(id=held_item.variant.id)
                variant.current_stock += held_item.qty
                held_item.delete()
            if not held_cart.held_items.exists():
                held_cart.delete()
                del request.session['cart']
            messages.success(request, 'Your cart is empty.')
            return redirect('/')
        except Exception as e:
            messages.error(request, f'Error emptying cart: {e}')
            return HttpResponse(status=500)


class ViewHeld(View):
    """
    Temporary view for held cart and items - TO DELETE
    """
    def get(self, request):
        session_key = request.session.session_key
        held_items = HeldCart.objects.all()
        template_name = 'cart/view_held.html'
        context = {
            'held_items': held_items,
            'session_key': session_key,
            }
        return render(request, template_name, context)
