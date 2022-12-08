from django.test import TestCase
from django.urls import reverse


class TestHome(TestCase):
    def test_get_index(self):
        """
        Get index page. Test correct templates used.
        """
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'home/index.html')
        self.assertTemplateUsed(response, 'includes/header.html')
        self.assertTemplateUsed(response, 'includes/footer.html')
        self.assertTemplateUsed(response, 'cart/cart_canvas.html')

    def test_get_contact(self):
        """
        Get contact page. Test correct templates used.
        """
        response = self.client.get('/contact/')
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'home/contact.html')
        self.assertTemplateUsed(response, 'includes/header.html')
        self.assertTemplateUsed(response, 'includes/footer.html')
        self.assertTemplateUsed(response, 'cart/cart_canvas.html')


class TestContactForm(TestCase):
    """
    Test view for submitted form.
    """
    def test_submit_contact(self):
        """
        Submitting a contact message should redirect to same page
        """
        data = {
            'contact_name': 'TestingContact',
            'contact_email': 'testing@contact.com',
            'contact_message': 'This is a test message for the contact form!'
        }
        response = self.client.post(reverse('home:contact'), data)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'home/contact.html')
        self.assertTemplateUsed(response, 'includes/header.html')
        self.assertTemplateUsed(response, 'includes/footer.html')
        self.assertTemplateUsed(response, 'cart/cart_canvas.html')
