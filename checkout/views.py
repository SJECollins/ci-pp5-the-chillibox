from django.shortcuts import render
from django.views import View


class Checkout(View):
    def get(self, request):
        template_name = 'checkout/checkout.html'
        context = {

        }
        return render(request, template_name, context)
