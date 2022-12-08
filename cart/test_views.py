import datetime
import pytz
from django.test import TestCase
from django.urls import reverse

from products.models import Category, Product, Variant
from .models import HeldCart, HeldItems


class TestCart(TestCase):
    def test_cart_view(self):
        """
        Try to get cart view.
        """
        response = self.client.get('/cart/')
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'cart/cart.html')
        self.assertTemplateUsed(response, 'includes/header.html')
        self.assertTemplateUsed(response, 'includes/footer.html')


class TestCartFunctions(TestCase):
    def setUp(self):
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
        self.product_b = Product.objects.create(
            category=self.category_a,
            name='Test Second Pepper',
            slug='test-second-pepper',
            added_on=datetime.datetime(2021, 12, 3, 0, 0, 0, tzinfo=pytz.utc),
        )
        self.product_b.save()
        self.variant_a = Variant.objects.create(
            product=self.product_a,
            size='small',
            price=2.99,
            current_stock=10,
            in_stock=True,
        )
        self.variant_a.save()
        self.variant_b = Variant.objects.create(
            product=self.product_a,
            size='large',
            price=2.99,
            current_stock=10,
            in_stock=True,
        )
        self.variant_b.save()

    def test_add_to_cart(self):
        item_id = self.product_a.id
        slug = self.product_a.slug
        data = {
            'product_variant': self.variant_a.id,
            'quantity': 1,
        }
        cart_before = self.client.session.get('cart', {})
        self.assertEqual(len(cart_before), 0)
        response = self.client.post(reverse('cart:add_to_cart',
                                    args=[item_id]), data)
        self.assertRedirects(
            response, '/products/product/test-pepper',
            status_code=302, target_status_code=200,
            fetch_redirect_response=True,)
        cart_after = self.client.session.get('cart', {})
        self.assertEqual(len(cart_after), 1)

    def test_adjust_cart(self):
        item_id = self.product_a.id
        slug = self.product_a.slug
        data = {
            'product_variant': self.variant_a.id,
            'quantity': 1,
        }
        cart_before = self.client.session.get('cart', {})
        self.assertEqual(len(cart_before), 0)
        response = self.client.post(reverse('cart:add_to_cart',
                                    args=[item_id]), data)
        self.assertRedirects(
            response, '/products/product/test-pepper',
            status_code=302, target_status_code=200,
            fetch_redirect_response=True,)
        cart_after = self.client.session.get('cart', {})
        self.assertEqual(len(cart_after), 1)
        self.assertEqual(cart_after['1']['items_by_size']['small'], 1)
        data = {
            'product_variant': self.variant_a.id,
            'quantity': 4,
        }
        response = self.client.post(reverse('cart:adjust_cart',
                                    args=[item_id]), data)
        self.assertRedirects(
            response, '/cart/',
            status_code=302, target_status_code=200,
            fetch_redirect_response=True,)
        cart_after_again = self.client.session.get('cart', {})
        self.assertEqual(cart_after_again['1']['items_by_size']['small'], 4)

    def test_adjust_cart_down(self):
        item_id = self.product_a.id
        slug = self.product_a.slug
        data = {
            'product_variant': self.variant_a.id,
            'quantity': 4,
        }
        cart_before = self.client.session.get('cart', {})
        self.assertEqual(len(cart_before), 0)
        response = self.client.post(reverse('cart:add_to_cart',
                                    args=[item_id]), data)
        self.assertRedirects(
            response, '/products/product/test-pepper',
            status_code=302, target_status_code=200,
            fetch_redirect_response=True,)
        cart_after = self.client.session.get('cart', {})
        self.assertEqual(len(cart_after), 1)
        self.assertEqual(cart_after['1']['items_by_size']['small'], 4)
        data = {
            'product_variant': self.variant_a.id,
            'quantity': 2,
        }
        response = self.client.post(reverse('cart:adjust_cart',
                                    args=[item_id]), data)
        self.assertRedirects(
            response, '/cart/',
            status_code=302, target_status_code=200,
            fetch_redirect_response=True,)
        cart_after_again = self.client.session.get('cart', {})
        self.assertEqual(cart_after_again['1']['items_by_size']['small'], 2)

    def test_remove_item(self):
        item_id = self.product_a.id
        slug = self.product_a.slug
        data = {
            'product_variant': self.variant_a.id,
            'quantity': 1,
        }
        cart_before = self.client.session.get('cart', {})
        self.assertEqual(len(cart_before), 0)
        response = self.client.post(reverse('cart:add_to_cart',
                                    args=[item_id]), data)
        self.assertRedirects(
            response, '/products/product/test-pepper',
            status_code=302, target_status_code=200,
            fetch_redirect_response=True,)
        cart_after = self.client.session.get('cart', {})
        self.assertEqual(len(cart_after), 1)
        self.assertEqual(cart_after['1']['items_by_size']['small'], 1)
        response = self.client.post(reverse('cart:remove_item',
                                    args=[item_id]), data)
        self.assertRedirects(
            response, '/cart/',
            status_code=302, target_status_code=200,
            fetch_redirect_response=True,)
        cart_after_again = self.client.session.get('cart', {})
        self.assertEqual(len(cart_after_again), 0)

    def test_add_same_product(self):
        item_id = self.product_a.id
        slug = self.product_a.slug
        data = {
            'product_variant': self.variant_a.id,
            'quantity': 1,
        }
        cart_before = self.client.session.get('cart', {})
        self.assertEqual(len(cart_before), 0)
        response = self.client.post(reverse('cart:add_to_cart',
                                    args=[item_id]), data)
        self.assertRedirects(
            response, '/products/product/test-pepper',
            status_code=302, target_status_code=200,
            fetch_redirect_response=True,)
        cart_after = self.client.session.get('cart', {})
        self.assertEqual(len(cart_after), 1)
        self.assertEqual(cart_after['1']['items_by_size']['small'], 1)
        response = self.client.post(reverse('cart:add_to_cart',
                                    args=[item_id]), data)
        self.assertRedirects(
            response, '/products/product/test-pepper',
            status_code=302, target_status_code=200,
            fetch_redirect_response=True,)
        cart_after_again = self.client.session.get('cart', {})
        self.assertEqual(cart_after_again['1']['items_by_size']['small'], 2)

    def test_add_different_size(self):
        item_id = self.product_a.id
        slug = self.product_a.slug
        data = {
            'product_variant': self.variant_a.id,
            'quantity': 1,
        }
        cart_before = self.client.session.get('cart', {})
        self.assertEqual(len(cart_before), 0)
        response = self.client.post(reverse('cart:add_to_cart',
                                    args=[item_id]), data)
        self.assertRedirects(
            response, '/products/product/test-pepper',
            status_code=302, target_status_code=200,
            fetch_redirect_response=True,)
        cart_after = self.client.session.get('cart', {})
        self.assertEqual(len(cart_after), 1)
        new_data = {
            'product_variant': self.variant_b.id,
            'quantity': 1
        }
        response = self.client.post(reverse('cart:add_to_cart',
                                    args=[item_id]), new_data)
        self.assertRedirects(
            response, '/products/product/test-pepper',
            status_code=302, target_status_code=200,
            fetch_redirect_response=True,)
        cart_after_again = self.client.session.get('cart', {})
        self.assertEqual(len(cart_after_again), 1)
        self.assertEqual(cart_after_again['1']['items_by_size']['small'], 1)
        self.assertEqual(cart_after_again['1']['items_by_size']['large'], 1)

    def test_clear_cart(self):
        item_id = self.product_a.id
        slug = self.product_a.slug
        data = {
            'product_variant': self.variant_a.id,
            'quantity': 1,
        }
        cart_before = self.client.session.get('cart', {})
        self.assertEqual(len(cart_before), 0)
        response = self.client.post(reverse('cart:add_to_cart',
                                    args=[item_id]), data)
        self.assertRedirects(
            response, '/products/product/test-pepper',
            status_code=302, target_status_code=200,
            fetch_redirect_response=True,)
        cart_after = self.client.session.get('cart', {})
        self.assertEqual(len(cart_after), 1)
        new_data = {
            'product_variant': self.variant_b.id,
            'quantity': 1
        }
        response = self.client.post(reverse('cart:add_to_cart',
                                    args=[item_id]), new_data)
        self.assertRedirects(
            response, '/products/product/test-pepper',
            status_code=302, target_status_code=200,
            fetch_redirect_response=True,)
        cart_after_add_new = self.client.session.get('cart', {})
        self.assertEqual(len(cart_after_add_new), 1)
        self.assertEqual(cart_after_add_new['1']['items_by_size']['small'], 1)
        self.assertEqual(cart_after_add_new['1']['items_by_size']['large'], 1)
        response = self.client.get('/cart/clear_cart/')
        self.assertRedirects(
            response, '/',
            status_code=302, target_status_code=200,
            fetch_redirect_response=True,)
        cart_after_clear = self.client.session.get('cart', {})
        self.assertEqual(len(cart_after_clear), 0)
