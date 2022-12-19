import datetime
import pytz
from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User

from profiles.models import UserProfile
from products.models import Category, Product, Variant
from cart.models import HeldCart, HeldItems
from .models import Order, OrderLineItem


class TestCheckoutEmptyCart(TestCase):
    """
    Testing checkout views if cart is empty.
    """
    def test_checkout_view(self):
        """
        Try to get checkout view.
        Should redirect if no products in cart.
        """
        response = self.client.get('/checkout/')
        self.assertRedirects(response, '/', status_code=302,
                             target_status_code=200,
                             fetch_redirect_response=True)

    def test_checkout_success_view(self):
        """
        Try to get checkout success view with no order created.
        No order number so should render a 404.
        """
        response = self.client.get('/checkout/checkout_success/')
        self.assertEqual(response.status_code, 404)
        self.assertTemplateUsed(response, 'errors/404.html')
        self.assertTemplateUsed(response, 'includes/header.html')
        self.assertTemplateUsed(response, 'includes/footer.html')


class TestCheckoutCartFull(TestCase):
    """
    Testing checkout success if cart has items.
    """
    def setUp(self):
        """
        Set up.
        """
        self.category_a = Category.objects.create(
            name='Test Category',
            slug='test-cat'
        )
        self.category_a.save()
        self.product_a = Product.objects.create(
            category=self.category_a,
            name='Test Pepper',
            slug='test-pepper',
            added_on=datetime.datetime(2021, 12, 3, 0, 0, 0, tzinfo=pytz.utc),
        )
        self.product_a.save()
        self.variant_a = Variant.objects.create(
            product=self.product_a,
            size='small',
            price=2.99,
            current_stock=10,
            in_stock=True,
        )
        self.variant_a.save()
        self.held_cart = HeldCart.objects.create(
            cart_key=self.client.session.session_key,
            hold_time_start=datetime.datetime(2022, 12, 3, 0, 0, 0,
                                              tzinfo=pytz.utc),
        )
        self.held_cart.save()
        self.held_item = HeldItems.objects.create(
            cart=self.held_cart,
            product=self.product_a,
            variant=self.variant_a,
            qty=1,
        )
        self.held_item.save()
        self.order = Order.objects.create(
            order_number='xyz',
            first_name='Test',
            last_name='User',
            email='test@email.com',
            phone_number='1111111',
            country='IE',
            town_or_city='SomeTown',
            street_address1='1 First St',
            date=datetime.datetime(2022, 12, 3, 0, 0, 0, tzinfo=pytz.utc),
            order_total=2.99,
            grand_total=7.49,
        )
        self.order.save()
        self.order_line_item = OrderLineItem.objects.create(
            order=self.order,
            product=self.product_a,
            variant=self.variant_a,
            quantity=1,
            lineitem_total=2.99,
        )
        self.order_line_item.save()

    def test_checkout(self):
        """
        Try to view checkout with items in cart.
        """
        session = self.client.session
        session['cart'] = {
            '1': {'items_by_size': {'small': 1}}
        }
        session.save()
        response = self.client.get('/checkout/')
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'checkout/checkout.html')
        self.assertTemplateUsed(response, 'includes/header.html')
        self.assertTemplateUsed(response, 'includes/footer.html')

    def test_checkout_success_view(self):
        """
        Try to get checkout success view with order number
        """
        order_no = self.order.order_number
        response = self.client.get(
            reverse('checkout:checkout_success', args=[order_no]))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'checkout/checkout_success.html')
        self.assertTemplateUsed(response, 'includes/header.html')
        self.assertTemplateUsed(response, 'includes/footer.html')

    def test_checkout_post(self):
        """
        Test checkout post data
        """
        session = self.client.session
        session['cart'] = {
            '1': {'items_by_size': {'small': 1}}
        }
        session.save()
        data = {
            'first_name': 'Test',
            'last_name': 'User',
            'email': 'test@email.com',
            'phone_number': '1234567',
            'country': 'IE',
            'town_or_city': 'SomeTown',
            'street_address1': '1 First St',
            'street_address2': 'Apt 1',
            'county': 'A county',
            'postcode': '12345',
            'client_secret': 'thisisa_clientsecret',
        }
        response = self.client.post(reverse('checkout:checkout'), data,
                                    follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'checkout/checkout_success.html')
        self.assertTemplateUsed(response, 'includes/header.html')
        self.assertTemplateUsed(response, 'includes/footer.html')

    def test_view_pdf(self):
        """
        Test reportlab pdf function view
        """
        order_id = self.order.id
        response = self.client.get(
            reverse('checkout:order_pdf', args=[order_id]))
        self.assertEqual(response.status_code, 200)


class TestCheckoutLoggedIn(TestCase):
    """
    Test checkout for a logged in user.
    """
    def setUp(self):
        self.user = User.objects.create_user(
            username='testuser',
            email='test@email.com',
            password='testpass1'
        )
        self.user.is_staff = True
        self.user.save()
        self.client.login(email='test@email.com', password='testpass1')
        self.category_a = Category.objects.create(
            name='Test Category',
            slug='test-cat'
        )
        self.category_a.save()
        self.product_a = Product.objects.create(
            category=self.category_a,
            name='Test Pepper',
            slug='test-pepper',
            added_on=datetime.datetime(2021, 12, 3, 0, 0, 0, tzinfo=pytz.utc),
        )
        self.product_a.save()
        self.variant_a = Variant.objects.create(
            product=self.product_a,
            size='small',
            price=2.99,
            current_stock=10,
            in_stock=True,
        )
        self.variant_a.save()
        self.held_cart = HeldCart.objects.create(
            cart_key=self.client.session.session_key,
            hold_time_start=datetime.datetime(2022, 12, 3, 0, 0, 0,
                                              tzinfo=pytz.utc),
        )
        self.held_cart.save()
        self.held_item = HeldItems.objects.create(
            cart=self.held_cart,
            product=self.product_a,
            variant=self.variant_a,
            qty=1,
        )
        self.held_item.save()
        self.order = Order.objects.create(
            order_number='xyz',
            first_name='Test',
            last_name='User',
            email='test@email.com',
            phone_number='1111111',
            country='IE',
            town_or_city='SomeTown',
            street_address1='1 First St',
            date=datetime.datetime(2022, 12, 3, 0, 0, 0, tzinfo=pytz.utc),
            order_total=2.99,
            grand_total=7.49,
        )
        self.order.save()
        self.order_line_item = OrderLineItem.objects.create(
            order=self.order,
            product=self.product_a,
            variant=self.variant_a,
            quantity=1,
            lineitem_total=2.99,
        )
        self.order_line_item.save()

    def test_checkout_logged_in(self):
        """
        Testing checkout when logged in
        """
        profile = UserProfile.objects.get(user=self.user)
        profile.first_name = 'Test'
        profile.last_name = 'User'
        profile.phone_number = '1111111'
        profile.country = 'IE'
        profile.town_or_city = 'SomeTown'
        profile.street_address1 = '1 First St'
        profile.save()
        session = self.client.session
        session['cart'] = {
            '1': {'items_by_size': {'small': 1}}
        }
        session.save()
        response = self.client.get('/checkout/')
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'checkout/checkout.html')
        self.assertTemplateUsed(response, 'includes/header.html')
        self.assertTemplateUsed(response, 'includes/footer.html')

    def test_checkout_success_logged_in(self):
        """
        Try to get checkout success view with order number
        """
        session = self.client.session
        session['save_info'] = True
        session.save()
        order_no = self.order.order_number
        response = self.client.get(
            reverse('checkout:checkout_success', args=[order_no]))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'checkout/checkout_success.html')
        self.assertTemplateUsed(response, 'includes/header.html')
        self.assertTemplateUsed(response, 'includes/footer.html')
