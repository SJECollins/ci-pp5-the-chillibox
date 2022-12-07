from django.test import TestCase

from .forms import OrderForm


class TestOrderForm(TestCase):
    def test_empty_fields(self):
        form = OrderForm(data={
            'first_name': '',
            'last_name': '',
            'email': '',
            'phone_number': '',
            'street_address1': '',
            'street_address2': '',
            'town_or_city': '',
            'postcode': '',
            'country': '',
            'county': '',
        })
        self.assertFalse(form.is_valid())
        self.assertEqual(form.errors['first_name'][0],
                         'This field is required.')
        self.assertEqual(form.errors['last_name'][0],
                         'This field is required.')
        self.assertEqual(form.errors['email'][0], 'This field is required.')
        self.assertEqual(form.errors['phone_number'][0],
                         'This field is required.')
        self.assertEqual(form.errors['street_address1'][0],
                         'This field is required.')
        self.assertEqual(form.errors['town_or_city'][0],
                         'This field is required.')
        self.assertEqual(form.errors['country'][0], 'This field is required.')

    def test_valid_form(self):
        form = OrderForm(data={
            'first_name': 'Test',
            'last_name': 'User',
            'email': 'test@email.com',
            'phone_number': '1234567',
            'street_address1': '1 First St',
            'street_address2': '',
            'town_or_city': 'SomeTown',
            'postcode': '',
            'country': 'IE',
            'county': '',
        })
        self.assertTrue(form.is_valid())
