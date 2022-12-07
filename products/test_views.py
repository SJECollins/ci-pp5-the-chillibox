import datetime
import pytz
from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User

from profiles.models import Reviews
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

    def test_category_view_with_filterkey(self):
        """
        Test category view with slug and filterkey.
        """
        slug = self.category_a.slug
        data = {
            'filter_subcat': 'mild',
        }
        response = self.client.get(
            reverse('products:category', args=[slug]), data)
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

    def test_post_review(self):
        """
        Test ProductDetail view when posting review
        """
        self.assertEqual(Reviews.objects.count(), 0)
        slug = self.product_a.slug
        data = {
            'content': 'Test content',
            'rating': 5,
        }
        response = self.client.post(reverse('products:product', args=[slug]),
                                    data)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(Reviews.objects.count(), 1)
        self.assertTemplateUsed(response, 'products/product_detail.html')
        self.assertTemplateUsed(response, 'includes/header.html')
        self.assertTemplateUsed(response, 'includes/footer.html')

    def test_empty_review(self):
        """
        Test ProductDetail view when attempt to post empty review
        """
        self.assertEqual(Reviews.objects.count(), 0)
        slug = self.product_a.slug
        data = {
            'content': '',
            'rating': '',
        }
        response = self.client.post(reverse('products:product', args=[slug]),
                                    data)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(Reviews.objects.count(), 0)
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

    def test_current_stock_default(self):
        data = {
            'product_variant': 'default',
        }
        response = self.client.get(reverse('products:current_stock'), data)
        self.assertEqual(response.status_code, 200)

    def test_current_stock_with_variant(self):
        data = {
            'product_variant': self.variant_a.id,
        }
        response = self.client.get(reverse('products:current_stock'), data)
        self.assertEqual(response.status_code, 200)


class TestPostReviewLoggedIn(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username='testuser',
            email='test@email.com',
            password='testpass1'
        )
        self.user.is_staff = False
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

    def test_logged_in_review(self):
        self.assertEqual(Reviews.objects.count(), 0)
        slug = self.product_a.slug
        data = {
            'content': 'Test content',
            'rating': 5,
        }
        response = self.client.post(reverse('products:product', args=[slug]),
                                    data)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(Reviews.objects.count(), 1)
        self.assertTemplateUsed(response, 'products/product_detail.html')
        self.assertTemplateUsed(response, 'includes/header.html')
        self.assertTemplateUsed(response, 'includes/footer.html')
