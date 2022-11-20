
from django.shortcuts import render
from django.views import View

from products.models import Product


class IndexView(View):
    def get(self, request):
        latest_products = Product.objects.all().order_by('-added_on')[0:4]
        template_name = 'home/index.html'
        context = {
            'latest_products': latest_products,
        }
        return render(request, template_name, context)


def handle_403(request, exception, template_name="errors/403.html"):
    """
    Renders custom 403 page
    """
    response = render(request, template_name)
    response.status_code = 403
    return response


def handle_404(request, exception, template_name="errors/404.html"):
    """
    Renders custom 404 page
    """
    response = render(request, template_name)
    response.status_code = 404
    return response


def handle_405(request, exception, template_name="errors/405.html"):
    """
    Renders custom 405 page
    """
    response = render(request, template_name)
    response.status_code = 405
    return response


def handle_500(request):
    """
    Renders custom 500 page.
    """
    return render(request, 'errors/500.html')
