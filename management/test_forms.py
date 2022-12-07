from django.test import TestCase

from .forms import StockForm


class TestStockForm(TestCase):
    def test_empty_fields(self):
        form = StockForm(data={
            'current_stock': '',
        })
        self.assertFalse(form.is_valid())
        self.assertEqual(form.errors['current_stock'][0],
                         'This field is required.')

    def test_valid_form(self):
        form = StockForm(data={
            'current_stock': '10',
        })
        self.assertTrue(form.is_valid())
