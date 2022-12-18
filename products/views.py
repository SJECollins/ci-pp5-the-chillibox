from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse
from django.views import View
from django.views.generic import ListView
from django.db.models import Q, Avg
from django.db.models.functions import Round

from profiles.forms import ReviewForm
from profiles.models import Reviews

from .models import Category, Variant, Product


class LatestProducts(View):
    """
    Latest product view
    Generic view
    """
    def get(self, request):
        seedcat = Product.objects.filter(category__name='Seeds').order_by('-added_on')[0:4]  # noqa
        saucecat = Product.objects.filter(category__name='Sauces').order_by('-added_on')[0:4]  # noqa
        seedboxcat = Product.objects.filter(category__name='Seedboxes').order_by('-added_on')[0:4]  # noqa
        sauceboxcat = Product.objects.filter(category__name='Sauceboxes').order_by('-added_on')[0:4]  # noqa
        template_name = 'products/latest_products.html'
        context = {
            'seedcat': seedcat,
            'saucecat': saucecat,
            'seedboxcat': seedboxcat,
            'sauceboxcat': sauceboxcat,
        }
        return render(request, template_name, context)


class CategoryView(View):
    """
    Category view
    Generic view
    """
    def get(self, request, slug, *args, **kwargs):
        """
        Filterkey in get to filter queryset
        """
        category = get_object_or_404(Category, slug=slug)
        products_list = Product.objects.filter(category__slug=slug).all()
        template_name = 'products/category.html'
        filterkey = self.request.GET.get('filter_subcat')
        if filterkey is None or filterkey == 'default':
            products = products_list
        else:
            products = products_list.filter(subcategory=filterkey.title())

        context = {
            'category': category,
            'products': products,
            'current_filterkey': filterkey,
        }
        return render(request, template_name, context)


class ProductDetail(View):
    """
    Product detail view
    Generic view
    Using ReviewForm from profiles app for review on product page
    Reviews filter returns approved reviews for current product
    Avg_rating is rounded average of those reviews
    """
    def get(self, request, slug):
        product = get_object_or_404(Product, slug=slug)
        reviews = product.reviews.filter(approved=True).order_by('-added_on')
        avg_rating = reviews.aggregate(rounded=Round(Avg('rating')))
        template_name = 'products/product_detail.html'
        context = {
            'product': product,
            'reviews': reviews,
            'avg_rating': avg_rating,
            'reviewed': False,
            'review_form': ReviewForm(),
        }
        return render(request, template_name, context)

    def post(self, request, slug, *args, **kwargs):
        product = get_object_or_404(Product, slug=slug)
        reviews = product.reviews.filter(approved=True).order_by('-added_on')
        avg_rating = reviews.aggregate(rounded=Round(Avg('rating')))
        template_name = 'products/product_detail.html'

        review_form = ReviewForm(data=request.POST)

        if review_form.is_valid():
            if request.user.is_authenticated:
                review_form.instance.reviewer = request.user.userprofile
                review = review_form.save(commit=False)
                review.product = product
                review.save()
            else:
                review = review_form.save(commit=False)
                review.product = product
                review.save()
        else:
            review_form = ReviewForm()

        context = {
            'product': product,
            'reviews': reviews,
            'avg_rating': avg_rating,
            'reviewed': True,
            'review_form': review_form,
        }

        return render(request, template_name, context)


class SearchResults(ListView):
    """
    Search results view
    Generic list view using Product model
    Using Q to query by name or description
    """
    model = Product
    template_name = 'products/search_results.html'

    def get_queryset(self):
        query = self.request.GET.get('q')
        product_list = Product.objects.filter(
            Q(name__icontains=query) | Q(description__icontains=query)
        )
        return product_list


def current_stock(request):
    """
    Current stock function
    Returns current stock when variant selected on product detail page
    """
    variant_id = request.GET.get('product_variant')
    if variant_id == 'default':
        return HttpResponse('')
    else:
        variant = Variant.objects.get(id=variant_id)
        current_stock = variant.fulfillable_qty
        return HttpResponse(current_stock)
