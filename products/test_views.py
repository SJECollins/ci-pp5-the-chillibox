from django.test import TestCase

from .models import Category, Product, Variant


class TestProduct(TestCase):
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
