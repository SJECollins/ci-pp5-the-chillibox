import datetime
import pytz
from django.test import TestCase
from unittest import mock
from django.contrib.auth.models import User

from products.models import Category, Product
from .models import UserProfile, Reviews


class TestUserProfile(TestCase):
    def test_user_profile(self):
        self.assertEqual(UserProfile.objects.count(), 0)
        user = User.objects.create_user(
            username='testuser',
            email='test@email.com',
            password='testpass1'
        )
        user.save()
        self.client.login(email='test@email.com', password='testpass1')
        self.assertEqual(UserProfile.objects.count(), 1)
        self.assertEqual(user.userprofile.user, user)
        self.assertEqual(user.userprofile.display_name, user.username)


class TestReviews(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username='testuser',
            email='test@email.com',
            password='testpass1'
        )
        self.user.is_staff = True
        self.user.save()
        self.client.login(email='test@email.com', password='testpass1')
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

    def test_reviews(self):
        mocked = datetime.datetime(2022, 10, 10, 0, 0, 0, tzinfo=pytz.utc)
        with mock.patch('django.utils.timezone.now', mock.Mock(return_value=mocked)):  # noqa
            review = Reviews.objects.create(
                reviewer=self.user.userprofile,
                product=self.product_a,
                content='Test review',
                rating=5,
                added_on=mocked,
                last_edited='2022-12-07',
            )
        review_string = 'Test review'
        self.assertEqual(review.reviewer, self.user.userprofile)
        self.assertEqual(review.product, self.product_a)
        self.assertEqual(str(review.content), 'Test review')
        self.assertEqual(review.rating, 5)
        self.assertEqual(str(review.added_on), '2022-10-10 00:00:00+00:00')
        self.assertEqual(str(review.last_edited),
                         str(datetime.datetime.today().strftime('%Y-%m-%d')))
        self.assertFalse(review.approved)
        self.assertEqual(str(review), review_string)
