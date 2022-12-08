import datetime
import pytz
from django.test import TestCase
from django.urls import reverse

from products.models import Category, Product, Variant


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
        self.variant_a = Variant.objects.create(
            product=self.product_a,
            size='small',
            price=2.99,
            current_stock=10,
            in_stock=True,
        )
        self.variant_a.save()

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
