import datetime
import pytz
from django.test import TestCase
from unittest import mock
from django.contrib.auth.models import User

from products.models import Category, Product, Variant
from .models import HeldCart, HeldItems


class TestHeldCart(TestCase):
    """
    Test HeldCart model.
    """
    def setUp(self):
        """ Setup for testing """
        self.user = User.objects.create_user(
            username='testuser',
            email='test@email.com',
            password='testpass1'
        )
        self.user.save()

    def test_held_cart(self):
        """
        Testing HeldCart model
        """
        mocked = datetime.datetime(2022, 10, 10, 0, 0, 0, tzinfo=pytz.utc)
        with mock.patch('django.utils.timezone.now', mock.Mock(return_value=mocked)):  # noqa
            held_cart = HeldCart.objects.create(
                cart_key='xyz',
                owner=self.user,
                hold_time_start=mocked,
            )
        self.assertEqual(str(held_cart.cart_key), 'xyz')
        self.assertEqual(str(held_cart.owner), self.user.username)
        self.assertEqual(str(held_cart.hold_time_start),
                         '2022-10-10 00:00:00+00:00')


class TestHeldItems(TestCase):
    """
    Test HeldItems model.
    """
    def setUp(self):
        """ Setup for testing """
        self.user = User.objects.create_user(
            username='testuser',
            email='test@email.com',
            password='testpass1'
        )
        self.user.save()
        self.held_cart = HeldCart.objects.create(
            cart_key='xyz',
            owner=self.user,
            hold_time_start=datetime.datetime(
                2012,
                12,
                12,
                0,
                0,
                0,
                tzinfo=pytz.utc)
        )
        self.held_cart.save()
        self.category = Category.objects.create(
            name='Test category',
            slug='test-category'
        )
        self.category.save()
        self.product_a = Product.objects.create(
            category=self.category,
            name='Test product',
            slug='test-product'
        )
        self.product_a.save()
        self.variant_a = Variant.objects.create(
            product=self.product_a,
            size='250ml',
            price=5.99,
            current_stock=5,
        )
        self.variant_a.save()

    def test_held_items(self):
        """
        Testing HeldItems model
        """
        mocked = datetime.datetime(2022, 10, 10, 0, 0, 0, tzinfo=pytz.utc)
        with mock.patch('django.utils.timezone.now', mock.Mock(return_value=mocked)):  # noqa
            held_item = HeldItems.objects.create(
                cart=self.held_cart,
                product=self.product_a,
                variant=self.variant_a,
                qty=1,
                added_on=mocked,
            )
        self.assertEqual(str(held_item.cart.cart_key), self.held_cart.cart_key)
        self.assertEqual(str(held_item.product), 'Test product')
        self.assertEqual(str(held_item.variant), '250ml')
        self.assertEqual(held_item.qty, 1)
        self.assertEqual(str(held_item.added_on), '2022-10-10 00:00:00+00:00')
        self.assertEqual(str(held_item.cart.hold_time_start),
                         '2022-10-10 00:00:00+00:00')
