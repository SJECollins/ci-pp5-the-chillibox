from django.test import TestCase

from .forms import StockForm


class TestStockForm(TestCase):
    """
    Tests for StockForm
    """
    def test_empty_fields(self):
        """
        Testing empty form
        """
        form = StockForm(data={
            'current_stock': '',
        })
        self.assertFalse(form.is_valid())
        self.assertEqual(form.errors['current_stock'][0],
                         'This field is required.')

    def test_valid_form(self):
        """
        Testing valid form
        """
        form = StockForm(data={
            'current_stock': '10',
        })
        self.assertTrue(form.is_valid())
