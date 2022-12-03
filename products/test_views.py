import datetime
import pytz
from django.test import TestCase
from django.urls import reverse

from .models import Category, Product, Variant


class TestProductsWithoutProducts(TestCase):
    """
    Test product views without categories or products.
    """
    def test_latest_products_view(self):
        """
        Test view for latest products
        """
        response = self.client.get('/products/')
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'products/latest_products.html')
        self.assertTemplateUsed(response, 'includes/header.html')
        self.assertTemplateUsed(response, 'includes/footer.html')

    def test_category_view(self):
        """
        No category slug, should return 404.
        """
        response = self.client.get('/products/category/')
        self.assertEqual(response.status_code, 404)
        self.assertTemplateUsed(response, 'errors/404.html')
        self.assertTemplateUsed(response, 'includes/header.html')
        self.assertTemplateUsed(response, 'includes/footer.html')

    def test_product_detail_view(self):
        """
        No product slug, should return 404.
        """
        response = self.client.get('/products/product/')
        self.assertEqual(response.status_code, 404)
        self.assertTemplateUsed(response, 'errors/404.html')
        self.assertTemplateUsed(response, 'includes/header.html')
        self.assertTemplateUsed(response, 'includes/footer.html')

    def test_product_search_view(self):
        """
        Test product search
        """
        query = {'q': 'test'}
        response = self.client.get('/products/search_results/', query)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'products/search_results.html')
        self.assertTemplateUsed(response, 'includes/header.html')
        self.assertTemplateUsed(response, 'includes/footer.html')


class TestProductsWithProducts(TestCase):
    """
    Test product views with categories and products.
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

    def test_latest_products_view(self):
        """
        Test view for latest products
        """
        response = self.client.get('/products/')
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'products/latest_products.html')
        self.assertTemplateUsed(response, 'includes/header.html')
        self.assertTemplateUsed(response, 'includes/footer.html')

    def test_category_view(self):
        """
        Test category view with slug.
        """
        slug = self.category_a.slug
        response = self.client.get(
            reverse('products:category', args=[slug]))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'products/category.html')
        self.assertTemplateUsed(response, 'includes/header.html')
        self.assertTemplateUsed(response, 'includes/footer.html')

    def test_product_detail_view(self):
        """
        Test product view with slug.
        """
        slug = self.product_a.slug
        response = self.client.get(
            reverse('products:product', args=[slug]))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'products/product_detail.html')
        self.assertTemplateUsed(response, 'includes/header.html')
        self.assertTemplateUsed(response, 'includes/footer.html')

    def test_product_search_view(self):
        """
        Test product search
        """
        query = {'q': 'test'}
        response = self.client.get('/products/search_results/', query)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'products/search_results.html')
        self.assertTemplateUsed(response, 'includes/header.html')
        self.assertTemplateUsed(response, 'includes/footer.html')
