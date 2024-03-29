import json
from django.shortcuts import render, redirect, reverse, get_object_or_404, HttpResponse  # noqa
from django.views.decorators.http import require_POST
from django.contrib import messages
from django.conf import settings
from django.views import View

import io
from django.http import FileResponse
from reportlab.pdfgen import canvas
from reportlab.lib.units import cm
from reportlab.lib.pagesizes import A4
from reportlab.platypus import Table, Image

import stripe

from cart.contexts import cart_contents

from products.models import Product, Variant
from profiles.models import UserProfile
from profiles.forms import ProfileForm

from cart.models import HeldCart, HeldItems

from .forms import OrderForm
from .models import Order, OrderLineItem


@require_POST
def cache_checkout_data(request):
    try:
        pid = request.POST.get('client_secret').split('_secret')[0]
        stripe.api_key = settings.STRIPE_SECRET_KEY
        stripe.PaymentIntent.modify(pid, metadata={
            'cart': json.dumps(request.session.get('cart', {})),
            'save_info': request.POST.get('save_info'),
            'username': request.user,
        })
        return HttpResponse(status=200)
    except Exception as e:
        messages.error(request, 'Sorry, your payment cannot be \
            processed right now. Please try again later.')
        return HttpResponse(content=e, status=400)


def checkout(request):
    """
    Checkout function
    Based on CI's boutique ado
    https://github.com/Code-Institute-Solutions/boutique_ado_v1
    Takes form data, attempts to prefill delivery information
    Creates order
    Reduces stock for ordered variants
    """
    stripe_public_key = settings.STRIPE_PUBLIC_KEY
    stripe_secret_key = settings.STRIPE_SECRET_KEY

    if request.method == 'POST':
        cart = request.session.get('cart', {})
        held_cart = HeldCart.objects.get(cart_key=request.session.session_key)

        form_data = {
            'first_name': request.POST['first_name'],
            'last_name': request.POST['last_name'],
            'email': request.POST['email'],
            'phone_number': request.POST['phone_number'],
            'country': request.POST['country'],
            'postcode': request.POST['postcode'],
            'town_or_city': request.POST['town_or_city'],
            'street_address1': request.POST['street_address1'],
            'street_address2': request.POST['street_address2'],
            'county': request.POST['county'],
        }

        order_form = OrderForm(form_data)
        if order_form.is_valid():
            order = order_form.save(commit=False)
            pid = request.POST.get('client_secret').split('_secret')[0]
            order.stripe_pid = pid
            order.original_cart = json.dumps(cart)
            order.save()
            for item_id, item_data in cart.items():
                try:
                    product = Product.objects.get(id=item_id)
                    if isinstance(item_data, int):
                        order_line_item = OrderLineItem(
                            order=order,
                            product=product,
                            quantity=item_data,
                        )
                        order_line_item.save()
                    else:
                        for size, quantity in item_data['items_by_size'].items():  # noqa
                            variant = product.variants.get(size=size)
                            held_variant = held_cart.held_items.get(variant=variant)  # noqa
                            order_line_item = OrderLineItem(
                                order=order,
                                product=product,
                                quantity=quantity,
                                variant=variant,
                            )
                            order_line_item.save()
                            variant.current_stock -= held_variant.qty
                            variant.save()
                            held_variant.delete()
                except Product.DoesNotExist:
                    messages.error(request, (
                        "One of the products in your cart wasn't found in our \
                        database. Please call us for assistance!")
                    )
                    order.delete()
                    return redirect(reverse('view_cart'))

            # Save the info to the user's profile if all is well
            request.session['save_info'] = 'save-info' in request.POST
            return redirect(reverse('checkout:checkout_success',
                            args=[order.order_number]))
        else:
            messages.error(request, 'There was an error with your form. \
                Please double check your information.')
    else:
        cart = request.session.get('cart', {})
        if not cart:
            messages.error(request, "There's nothing in your cart at the \
                moment")
            return redirect(reverse('home:index'))

        current_cart = cart_contents(request)
        total = current_cart['grand_total']
        stripe_total = round(total * 100)
        stripe.api_key = stripe_secret_key
        intent = stripe.PaymentIntent.create(
            amount=stripe_total,
            currency=settings.STRIPE_CURRENCY,
        )

        # Attempt to prefill the form with info from user profile
        if request.user.is_authenticated:
            try:
                profile = UserProfile.objects.get(user=request.user)
                order_form = OrderForm(initial={
                    'first_name': profile.first_name,
                    'last_name': profile.last_name,
                    'email': profile.user.email,
                    'phone_number': profile.phone_number,
                    'country': profile.country,
                    'postcode': profile.postcode,
                    'town_or_city': profile.town_or_city,
                    'street_address1': profile.street_address1,
                    'street_address2': profile.street_address2,
                    'county': profile.county,
                })
            except UserProfile.DoesNotExist:
                order_form = OrderForm()
        else:
            order_form = OrderForm()

    if not stripe_public_key:
        messages.warning(request, 'Stripe public key is missing. \
            Did you forget to set it in your environment?')

    template = 'checkout/checkout.html'
    context = {
        'order_form': order_form,
        'stripe_public_key': stripe_public_key,
        'client_secret': intent.client_secret,
    }

    return render(request, template, context)


def checkout_success(request, order_number):
    """
    Based on CI's boutique ado
    https://github.com/Code-Institute-Solutions/boutique_ado_v1
    Handle successful checkouts
    Saves registered user's data
    Deletes session cart and session key
    """
    save_info = request.session.get('save_info')
    order = get_object_or_404(Order, order_number=order_number)

    if request.user.is_authenticated:
        profile = UserProfile.objects.get(user=request.user)
        # Attach the user's profile to the order
        order.user_profile = profile
        order.save()

        # Save the user's info
        if save_info:
            profile_data = {
                'first_name': order.first_name,
                'last_name': order.last_name,
                'phone_number': order.phone_number,
                'country': order.country,
                'postcode': order.postcode,
                'town_or_city': order.town_or_city,
                'street_address1': order.street_address1,
                'street_address2': order.street_address2,
                'county': order.county,
            }
            user_profile_form = ProfileForm(profile_data, instance=profile)
            if user_profile_form.is_valid():
                user_profile_form.save()

    messages.success(request, f'Order successfully processed! \
        Your order number is {order_number}. A confirmation \
        email will be sent to {order.email}.')

    if 'cart' in request.session:
        held_cart = HeldCart.objects.get(cart_key=request.session.session_key)
        held_cart.delete()
        del request.session['cart']

    template = 'checkout/checkout_success.html'
    context = {
        'order': order,
    }

    return render(request, template, context)


def order_pdf(request, pk):
    """
    Function to create pdf of the order using reportlab
    """
    buffer = io.BytesIO()
    c = canvas.Canvas(buffer, pagesize=A4)
    c.translate(0, 29.7 * cm)
    c.setFont('Helvetica', 12)

    order = Order.objects.get(pk=pk)

    # Heading
    logo = 'static/images/chilli-logo-colour.png'
    textobject = c.beginText(7.5 * cm, -3 * cm)
    c.drawImage(logo, 2 * cm, -3 * cm, mask='auto')
    textobject.textLine('Your order from The Chillibox')
    c.drawText(textobject)

    # User address
    textobject = c.beginText(1.5 * cm, -4.5 * cm)
    textobject.textLine('Delivering to: ')
    textobject.textLine('')
    textobject.textLine(order.first_name + ' ' + order.last_name)
    textobject.textLine(order.phone_number)
    textobject.textLine(order.street_address1)
    if order.street_address2:
        textobject.textLine(order.street_address2)
    textobject.textLine(order.town_or_city)
    if order.county:
        textobject.textLine(order.county)
    textobject.textLine(str(order.country))
    if order.postcode:
        textobject.textLine(order.postcode)
    c.drawText(textobject)

    # Order details
    textobject = c.beginText(1.5 * cm, -9.5 * cm)
    textobject.textLine('Order Summary:')
    textobject.textLine('')
    textobject.textLine('   Order #: ' + order.order_number)
    textobject.textLine('   Ordered on: ' + order.date.strftime('%d %b %Y'))
    textobject.textLine('   Delivery cost: €' + str(order.delivery_cost))
    textobject.textLine('   Grand Total: €' + str(order.grand_total))
    c.drawText(textobject)

    # Order Items
    textobject = c.beginText(1.5 * cm, -13.5 * cm)
    textobject.textLine('Your Items: ')
    c.drawText(textobject)

    # Table of ordered items
    data = []
    for item in order.lineitems.all():
        data.append([
            item.product,
            item.variant,
            item.quantity,
            item.variant.price
        ])
    table = Table(data, colWidths=[6 * cm, 6 * cm, 2 * cm, 2 * cm])
    tw, th, = table.wrapOn(c, 15 * cm, 19 * cm)
    table.drawOn(c, 1.5 * cm, -14 * cm - th)

    c.showPage()
    c.save()
    buffer.seek(0)

    return FileResponse(buffer, as_attachment=True, filename='order.pdf')
