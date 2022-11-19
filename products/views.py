from django.shortcuts import render, get_object_or_404
from django.views import View

from .models import Category, SubCategory, ProductVariant, Product


class LatestProducts(View):
    def get(self, request):
        seedcat = Product.objects.filter(category__name='Seeds').order_by('-added_on')[0:4]  # noqa
        saucecat = Product.objects.filter(category__name='Sauces').order_by('-added_on')[0:4]  # noqa
        seedboxcat = Product.objects.filter(category__name='SeedBox').order_by('-added_on')[0:4]  # noqa
        sauceboxcat = Product.objects.filter(category__name='SauceBox').order_by('-added_on')[0:4]  # noqa
        template_name = 'products/latest_products.html'
        context = {
            'seedcat': seedcat,
            'saucecat': saucecat,
            'seedboxcat': seedboxcat,
            'sauceboxcat': sauceboxcat,
        }
        return render(request, template_name, context)


class CategoryView(View):
    def get(self, request, slug):
        category = get_object_or_404(Category, slug=slug)
        products = Product.objects.filter(category__slug=slug).all()
        template_name = 'products/category.html'
        context = {
            'category': category,
            'products': products,
        }
        return render(request, template_name, context)
