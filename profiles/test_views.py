import datetime
import pytz
from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User

from products.models import Category, Product
from checkout.models import Order, OrderLineItem
from .models import UserProfile, Reviews


class TestProfilesNotLoggedIn(TestCase):
    """
    Test profile views in case of user not logged in.
    """
    def setUp(self):
        """
        Setup for testing
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
        self.review_a = Reviews.objects.create(
            product=self.product_a,
            content='Test content',
            rating=5,
            added_on=datetime.datetime(2021, 12, 3, 0, 0, 0, tzinfo=pytz.utc),
            approved=True,
        )
        self.review_a.save()
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

    def test_profile_view(self):
        """
        Test get profile view if not logged in.
        Should redirect to login.
        """
        response = self.client.get('/profiles/profile/', follow=True)
        self.assertRedirects(response,
                             '/accounts/login/?next=/profiles/profile/',
                             status_code=302, target_status_code=200,
                             fetch_redirect_response=True)

    def test_update_profile(self):
        """
        Test update profile.
        """
        response = self.client.get('/profiles/edit_profile/')
        self.assertRedirects(response,
                             '/accounts/login/?next=/profiles/edit_profile/',
                             status_code=302, target_status_code=200,
                             fetch_redirect_response=True)

    def test_delete_account(self):
        """
        Test delete account.
        """
        response = self.client.get('/profiles/delete_account/')
        self.assertRedirects(response,
                             '/accounts/login/?next=/profiles/delete_account/',
                             status_code=302, target_status_code=200,
                             fetch_redirect_response=True)

    def test_review_list(self):
        """
        Test view reviews.
        """
        response = self.client.get('/profiles/review_list/', follow=True)
        self.assertRedirects(response,
                             '/accounts/login/?next=/profiles/review_list/',
                             status_code=302, target_status_code=200,
                             fetch_redirect_response=True)

    def test_edit_review(self):
        """
        Test edit reviews.
        """
        review = self.review_a.id
        response = self.client.get(reverse('profiles:edit_review',
                                   args=[review]))
        self.assertRedirects(
            response, '/accounts/login/?next=/profiles/edit_review/1',
            status_code=302, target_status_code=200,
            fetch_redirect_response=True)

    def test_delete_review(self):
        """
        Test delete review.
        """
        review = self.review_a.id
        response = self.client.get(reverse('profiles:delete_review',
                                   args=[review]))
        self.assertRedirects(
            response, '/accounts/login/?next=/profiles/delete_review/1',
            status_code=302, target_status_code=200,
            fetch_redirect_response=True)

    def test_order_history_view(self):
        """
        Test order history.
        """
        order_no = self.order.order_number
        response = self.client.get(reverse('profiles:order_history',
                                   args=[order_no]))
        self.assertRedirects(
            response, '/accounts/login/?next=/profiles/order_history/xyz',
            status_code=302, target_status_code=200,
            fetch_redirect_response=True)


class TestProfilesLoggedIn(TestCase):
    """
    Test profile views in case of user logged in.
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
        self.review_a = Reviews.objects.create(
            product=self.product_a,
            content='Test content',
            rating=5,
            added_on=datetime.datetime(2021, 12, 3, 0, 0, 0, tzinfo=pytz.utc),
            approved=True,
        )
        self.review_a.save()
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

    def test_profile_view(self):
        """
        Test get profile view if not logged in.
        Should redirect to login.
        """
        response = self.client.get('/profiles/profile/')
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'profiles/profile.html')
        self.assertTemplateUsed(response, 'includes/header.html')
        self.assertTemplateUsed(response, 'includes/footer.html')

    def test_update_profiles(self):
        """
        Test update profile.
        """
        response = self.client.get('/profiles/edit_profile/')
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'profiles/profile_form.html')
        self.assertTemplateUsed(response, 'includes/header.html')
        self.assertTemplateUsed(response, 'includes/footer.html')

    def test_delete_account(self):
        """
        Testing delete account
        """
        response = self.client.get('/profiles/delete_account/')
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'profiles/confirm_delete.html')
        self.assertTemplateUsed(response, 'includes/header.html')
        self.assertTemplateUsed(response, 'includes/footer.html')

    def test_review_list(self):
        """
        Test view reviews.
        """
        response = self.client.get('/profiles/review_list/')
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'profiles/review_list.html')
        self.assertTemplateUsed(response, 'includes/header.html')
        self.assertTemplateUsed(response, 'includes/footer.html')

    def test_edit_review(self):
        """
        Test edit reviews.
        """
        review = self.review_a.id
        response = self.client.get(reverse('profiles:edit_review',
                                   args=[review]))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'profiles/review_form.html')
        self.assertTemplateUsed(response, 'includes/header.html')
        self.assertTemplateUsed(response, 'includes/footer.html')

    def test_delete_review(self):
        """
        Test delete review.
        """
        review = self.review_a.id
        response = self.client.get(reverse('profiles:delete_review',
                                   args=[review]))
        self.assertTemplateUsed(response, 'profiles/delete_review.html')
        self.assertTemplateUsed(response, 'includes/header.html')
        self.assertTemplateUsed(response, 'includes/footer.html')

    def test_order_history_view(self):
        """
        Test order history.
        """
        order_no = self.order.order_number
        response = self.client.get(reverse('profiles:order_history',
                                   args=[order_no]))
        self.assertTemplateUsed(response, 'checkout/checkout_success.html')
        self.assertTemplateUsed(response, 'includes/header.html')
        self.assertTemplateUsed(response, 'includes/footer.html')


class TestDeleteAccount(TestCase):
    """
    Test DelectAcountView post
    """
    def setUp(self):
        """
        Setup for testing
        """
        self.user = User.objects.create_user(
            username='testuser',
            email='test@email.com',
            password='testpass1'
        )
        self.user.is_staff = True
        self.user.save()
        self.client.login(email='test@email.com', password='testpass1')

    def test_delete_account(self):
        """
        Testing delete account post
        """
        self.assertEqual(UserProfile.objects.count(), 1)
        response = self.client.post('/profiles/delete_account/')
        data = {
            'delete': True,
        }
        response = self.client.post(reverse('profiles:delete_account'), data)
        self.assertRedirects(
            response, '/',
            status_code=302, target_status_code=200,
            fetch_redirect_response=True)
        self.assertEqual(UserProfile.objects.count(), 0)
