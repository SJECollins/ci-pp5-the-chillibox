from django.conf import settings
from allauth.account.adapter import DefaultAccountAdapter


class MyAccountAdapter(DefaultAccountAdapter):
    """
    Remove cart from session on login as causing a collision
    Not great for UX though, considering another workaround
    Also provides path to user profile on login
    """
    def get_login_redirect_url(self, request):
        if 'cart' in request.session:
            del request.session['cart']
        path = "/profiles/profile/"
        return path
