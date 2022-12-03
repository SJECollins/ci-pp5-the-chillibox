from django.test import TestCase


class TestCart(TestCase):
    def test_cart_view(self):
        """
        Try to get cart view.
        """
        response = self.client.get('/cart/')
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'cart/cart.html')
        self.assertTemplateUsed(response, 'includes/header.html')
        self.assertTemplateUsed(response, 'includes/footer.html')
