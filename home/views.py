
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