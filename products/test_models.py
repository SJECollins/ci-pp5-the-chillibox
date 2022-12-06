import datetime
import pytz
from django.test import TestCase
from unittest import mock

from .models import Category, Product, Variant


class TestCategory(TestCase):
    """
    Test category model
    """
    def test_category(self):
        category = Category.objects.create(
            name='Test category',
            slug='test-category',
        )
        category_string = 'Test category'
        self.assertEqual(str(category.name), 'Test category')
        self.assertEqual(str(category.slug), 'test-category')
        self.assertEqual(str(category), category_string)


class TestProduct(TestCase):
    """
    Test product model.
    """
    def setUp(self):
        self.category = Category.objects.create(
            name='Test category',
            slug='test-category'
        )
        self.category.save()
        self.product_a = Product.objects.create(
            category=self.category,
            name='Test box contents',
            slug='test-box-contents'
        )
        self.product_a.save()

    def test_product(self):
        product = Product.objects.create(
            category=self.category,
            subcategory='Mild',
            name='Test product',
            slug='test-product',
            description='Test description',
            excerpt='Test excerpt',
            ingredients='Test ingredients',
            growth_time='Test growth',
            heat_level='Test heat',
            origin='Test origin',
            added_on='2022-12-06',
        )
        product.box_contents.add(self.product_a)
        product_string = 'Test product'
        self.assertEqual(product.category, self.category)
        self.assertEqual(str(product.subcategory), 'Mild')
        self.assertEqual(str(product.name), 'Test product')
        self.assertEqual(str(product.slug), 'test-product')
        self.assertEqual(str(product.description), 'Test description')
        self.assertEqual(str(product.excerpt), 'Test excerpt')
        self.assertEqual(str(product.ingredients), 'Test ingredients')
        self.assertEqual(str(product.growth_time), 'Test growth')
        self.assertEqual(str(product.heat_level), 'Test heat')
        self.assertEqual(str(product.origin), 'Test origin')
        self.assertEqual(str(product.box_contents.all()[0]), self.product_a.name)
        self.assertEqual(str(product.added_on), '2022-12-06')
        self.assertEqual(str(product), product_string)


class TestVariant(TestCase):
    """
    Test variant model
    """
    def setUp(self):
        self.category = Category.objects.create(
            name='Test category',
            slug='test-category'
        )
        self.category.save()
        self.product_a = Product.objects.create(
            category=self.category,
            name='Test box contents',
            slug='test-box-contents'
        )
        self.product_a.save()

    def test_variant(self):
        variant = Variant.objects.create(
            product=self.product_a,
            size='250ml',
            price=5.99,
            current_stock=0,
        )
        variant_string = '250ml'
        self.assertEqual(variant.product, self.product_a)
        self.assertEqual(str(variant.size), '250ml')
        self.assertEqual(variant.price, 5.99)
        self.assertEqual(str(variant.current_stock), '0')
        self.assertFalse(variant.in_stock)
        self.assertEqual(str(variant), variant_string)
