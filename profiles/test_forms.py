from django.test import TestCase

from .forms import ProfileForm, DeleteAccountForm, ReviewForm


class TestProfileForm(TestCase):
    """
    Testing the user profile form
    """
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
    """
    Testing delete account form
    """
    def test_delete_false(self):
        """
        Testing is not valid if delete is false
        """
        form = DeleteAccountForm(data={
            'delete': False,
        })
        self.assertFalse(form.is_valid())
        self.assertEqual(form.errors['delete'][0], 'This field is required.')

    def test_delete_true(self):
        """
        Testing valid form
        """
        form = DeleteAccountForm(data={
            'delete': True,
        })
        self.assertTrue(form.is_valid())


class TestReviewForm(TestCase):
    """
    Testing review form
    """
    def test_empty_fields(self):
        """
        Testing empty required fields
        """
        form = ReviewForm(data={
            'content': '',
            'rating': '',
        })
        self.assertFalse(form.is_valid())
        self.assertEqual(form.errors['content'][0], 'This field is required.')
        self.assertEqual(form.errors['rating'][0], 'This field is required.')

    def test_valid_form(self):
        """
        Testing valid form
        """
        form = ReviewForm(data={
            'content': 'Test content',
            'rating': 5,
        })
        self.assertTrue(form.is_valid())
