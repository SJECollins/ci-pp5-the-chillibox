import datetime
import pytz
from django.test import TestCase
from django.urls import reverse

from products.models import Category, Product, Variant
from profiles.models import Reviews


class TestManagementViewsNotLoggedIn(TestCase):
    """
    Test views when user is not logged in.
    """
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
        self.review_a = Reviews.objects.create(
            product=self.product_a,
            content='Test content',
            rating=5,
            added_on=datetime.datetime(2021, 12, 3, 0, 0, 0, tzinfo=pytz.utc),
            approved=True,
        )
        self.review_a.save()

    def test_dashboard(self):
        """
        Test get management dashboard if not logged in.
        Should redirect to login.
        """
        response = self.client.get('/management/', follow=True)
        self.assertRedirects(response, '/accounts/login/?next=/management/',
                             status_code=302, target_status_code=200,
                             fetch_redirect_response=True)

    def test_add_variant(self):
        """
        Test adding variant if not logged in.
        """
        slug = self.product_a.slug
        response = self.client.get(
            reverse('management:add_variant', args=[slug]))
        self.assertRedirects(
            response, '/accounts/login/?next=/management/add_variant/test-pepper',  # noqa
            status_code=302, target_status_code=200,
            fetch_redirect_response=True)

    def test_edit_variant(self):
        """
        Test editing variant if not logged in.
        """
        id = self.product_a.id
        response = self.client.get(
            reverse('management:edit_variant', args=[id]))
        self.assertRedirects(
            response, '/accounts/login/?next=/management/edit_variant/1',
            status_code=302, target_status_code=200,
            fetch_redirect_response=True)

    def test_delete_variant(self):
        """
        Test deleting variant if not logged in.
        """
        id = self.product_a.id
        response = self.client.get(
            reverse('management:delete_variant', args=[id]))
        self.assertRedirects(
            response, '/accounts/login/?next=/management/delete_variant/1',
            status_code=302, target_status_code=200,
            fetch_redirect_response=True)

    def test_add_product(self):
        """
        Testing adding product if not logged in.
        """
        response = self.client.get('/management/add_product/')
        self.assertRedirects(
            response, '/accounts/login/?next=/management/add_product/',
            status_code=302, target_status_code=200,
            fetch_redirect_response=True)

    def test_edit_product(self):
        """
        Testing editing product if not logged in.
        """
        id = self.product_a.id
        response = self.client.get(
            reverse('management:edit_product', args=[id]))
        self.assertRedirects(
            response, '/accounts/login/?next=/management/edit_product/1',
            status_code=302, target_status_code=200,
            fetch_redirect_response=True)

    def test_delete_product(self):
        """
        Test deleting product if not logged in.
        """
        id = self.product_a.id
        response = self.client.get(
            reverse('management:delete_product', args=[id]))
        self.assertRedirects(
            response, '/accounts/login/?next=/management/delete_product/1',
            status_code=302, target_status_code=200,
            fetch_redirect_response=True)

    def test_user_reviews(self):
        """
        Test viewing user reviews if not logged in.
        """
        response = self.client.get('/management/user_reviews/')
        self.assertRedirects(
            response, '/accounts/login/?next=/management/user_reviews/',
            status_code=302, target_status_code=200,
            fetch_redirect_response=True)

    def test_remove_review(self):
        """
        Test removing user reviews if not logged in.
        """
        review = self.review_a.id
        response = self.client.get(reverse('management:remove_review',
                                   args=[review]))
        self.assertRedirects(
            response, '/accounts/login/?next=/management/remove_review/1',
            status_code=302, target_status_code=200,
            fetch_redirect_response=True)

    def test_update_stock(self):
        """
        Test updating stock if not logged in.
        """
        id = self.variant_a.id
        response = self.client.get(reverse('management:update_stock',
                                   args=[id]))
        self.assertRedirects(
            response, '/accounts/login/',
            status_code=302, target_status_code=200,
            fetch_redirect_response=True)
