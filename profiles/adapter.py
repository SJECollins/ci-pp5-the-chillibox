from django.conf import settings
from allauth.account.adapter import DefaultAccountAdapter


class MyAccountAdapter(DefaultAccountAdapter):
    """
    Remove cart from session on login as causing issues with HeldCarts
    Not ideal for UX as user may want to login during shopping, but Django
    cycles keys at login/logout for security.
    """
    def get_login_redirect_url(self, request):
        if 'cart' in request.session:
            del request.session['cart']
        path = "/profiles/profile/"
        return path
