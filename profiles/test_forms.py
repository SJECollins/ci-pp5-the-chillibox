from django.test import TestCase

from .forms import ProfileForm, DeleteAccountForm, ReviewForm


class TestProfileForm(TestCase):
    def test_profile_form(self):
        form = ProfileForm(data={
            'first_name': 'Test',
            'last_name': 'User',
            'display_name': 'Test User',
            'phone_number': '1234567',
            'street_address1': '1 First St',
            'street_address2': 'Apt 1',
            'town_or_city': 'SomeTown',
            'county': 'A County',
            'country': 'IE',
            'postcode': '12345',
        })
        self.assertTrue(form.is_valid())


class TestDeleteAccount(TestCase):
    def test_delete_false(self):
        form = DeleteAccountForm(data={
            'delete': False,
        })
        self.assertFalse(form.is_valid())
        self.assertEqual(form.errors['delete'][0], 'This field is required.')

    def test_delete_true(self):
        form = DeleteAccountForm(data={
            'delete': True,
        })
        self.assertTrue(form.is_valid())


class TestReviewForm(TestCase):
    def test_empty_fields(self):
        form = ReviewForm(data={
            'content': '',
            'rating': '',
        })
        self.assertFalse(form.is_valid())
        self.assertEqual(form.errors['content'][0], 'This field is required.')
        self.assertEqual(form.errors['rating'][0], 'This field is required.')

    def test_valid_form(self):
        form = ReviewForm(data={
            'content': 'Test content',
            'rating': 5,
        })
        self.assertTrue(form.is_valid())
