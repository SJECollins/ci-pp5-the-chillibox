import datetime
import pytz
from math import ceil
from django.test import TestCase
from unittest import mock
from django.contrib.auth.models import User

from products.models import Category, Product, Variant
from .models import Order, OrderLineItem


class TestOrder(TestCase):
    """
    Test order model.
    """
    def test_order(self):
        """ Testing order model """
        mocked = datetime.datetime(2022, 10, 10, 0, 0, 0, tzinfo=pytz.utc)
        with mock.patch('django.utils.timezone.now', mock.Mock(return_value=mocked)):  # noqa
            order = Order.objects.create(
                first_name='Test',
                last_name='User',
                email='test@email.com',
                phone_number='1234567',
                country='IE',
                postcode='12345',
                town_or_city='SomeTown',
                street_address1='1 First St',
                street_address2='Apt 1',
                county='A county',
                date=mocked,
                delivery_cost=4.50,
                order_total=2.99,
                grand_total=7.49,
            )
        self.assertEqual(str(order.first_name), 'Test')
        self.assertEqual(str(order.last_name), 'User')
        self.assertEqual(str(order.email), 'test@email.com')
        self.assertEqual(str(order.phone_number), '1234567')
        self.assertEqual(str(order.country), 'IE')
        self.assertEqual(str(order.postcode), '12345')
        self.assertEqual(str(order.town_or_city), 'SomeTown')
        self.assertEqual(str(order.street_address1), '1 First St')
        self.assertEqual(str(order.street_address2), 'Apt 1')
        self.assertEqual(str(order.county), 'A county')
        self.assertEqual(str(order.date), '2022-10-10 00:00:00+00:00')
        self.assertEqual(order.order_total, 2.99)
        self.assertEqual(order.delivery_cost, 4.50)
        self.assertEqual(order.grand_total, 7.49)


class TesOrderLineItem(TestCase):
    """
    Test OrderLineItem model.
    """
    def setUp(self):
        """ Setup for testing """
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
        self.order = Order.objects.create(
            first_name='Test',
            last_name='User',
            email='test@email.com',
            phone_number='1234567',
            country='IE',
            town_or_city='SomeTown',
            street_address1='1 First St',
        )
        self.order.save()

    def test_order_line_item(self):
        """ Testing OrderLineItem model """
        lineitem = OrderLineItem.objects.create(
            order=self.order,
            product=self.product_a,
            variant=self.variant_a,
            quantity=1,
        )
        lineitem.save()
        lineitem_string = f'Test product in {self.order.order_number}'
        self.assertEqual(str(lineitem.product), 'Test product')
        self.assertEqual(str(lineitem.variant), '250ml')
        self.assertEqual(lineitem.quantity, 1)
        self.assertEqual(lineitem.lineitem_total, 5.99)
        self.assertEqual(ceil(lineitem.order.order_total * 100) / 100, 5.99)
        self.assertEqual(lineitem.order.delivery_cost, 4.50)
        self.assertEqual(ceil(lineitem.order.grand_total * 100) / 100, 10.49)
