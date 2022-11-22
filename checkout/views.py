import json
from django.shortcuts import render
from django.views import View
from django.contrib import messages

from cart.contexts import cart_contents

from products.models import Product, ProductVariant
from profiles.models import UserProfile


from .forms import OrderForm
from .models import Order, OrderLineItem


class Checkout(View):
    def get(self, request):
        template_name = 'checkout/checkout.html'
        context = {
            'order_form': OrderForm(),
        }
        return render(request, template_name, context)

    def post(self, request):
        template_name = 'checkout/checkout.html'
        context = {
            'order_form': OrderForm(),
        }
        return render(request, template_name, context)

        order_form = OrderForm(data=request.POST)

        if order_form.is_valid():
            order = order_form.save(commit=False)
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
                        for size, quantity in item_data['items_by_size'].items():
                            variant = ProductVariant.objects.get(size=size)
                            order_line_item = OrderLineItem(
                                order=order,
                                product=product,
                                quantity=quantity,
                                variant=variant,
                            )
                            order_line_item.save()
                except Product.DoesNotExist:
                    messages.error(request, (
                        "One of the products in your cart wasn't found in our database. "
                        "Please contact us for assistance.")
                    )
                    order.delete()
                    return redirect(reverse('view_cart'))

                # Save the info to the user's profile if all is well
                request.session['save_info'] = 'save-info' in request.POST
                return redirect(reverse('checkout_success', args=[order.order_number]))
            else:
                messages.error(request, 'There was an error with your form. \
                    Please double check your information.')
        else:
            cart = request.session.get('cart', {})
            if not cart:
                messages.error(request, "Your cart is empty.")
                return redirect(reverse('products'))

            current_cart = cart_contents(request)
            total = current_cart['grand_total']

        # Attempt to prefill the form with any info the user maintains in their profile
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
