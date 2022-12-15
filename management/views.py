from django.shortcuts import render, reverse, get_object_or_404, redirect
from django.http import HttpResponse
from django.views import View, generic
from django.views.generic import CreateView, UpdateView, DeleteView, ListView
from django.contrib import messages
from django.contrib.messages.views import SuccessMessageMixin

from profiles.models import Reviews
from products.models import Category, Product, Variant
from recipes.models import Recipe, Comment, SubmittedRecipe

from .mixins import StaffRequiredMixin
from .forms import StockForm


class ProductDashboard(StaffRequiredMixin, View):
    """
    View for admin accessible management dashboard.
    """
    def get(self, request):
        products = Product.objects.all().order_by('category', 'subcategory')
        template_name = 'management/dashboard.html'
        context = {
            'products': products,
        }
        return render(request, template_name, context)


class AddVariant(StaffRequiredMixin, SuccessMessageMixin, CreateView):
    """ Add Variant View for management dashboard """
    model = Variant
    fields = ('size', 'price', 'current_stock',)
    template_name = 'management/dashboard_form.html'
    success_url = '/management/'
    success_message = '%(size)s was created'

    def form_valid(self, form):
        product = get_object_or_404(Product, slug=self.kwargs['slug'])
        form.instance.product = product
        return super(AddVariant, self).form_valid(form)


class EditVariant(StaffRequiredMixin, SuccessMessageMixin, UpdateView):
    """ Edit Variant View for management dashboard """
    model = Variant
    fields = '__all__'
    template_name = 'management/dashboard_form.html'
    success_url = '/management/'
    success_message = '%(size)s was updated'


class DeleteVariant(StaffRequiredMixin, DeleteView):
    """ Delete Variant View for management dashboard """
    model = Variant
    template_name = 'management/confirm_delete.html'
    success_url = '/management/'


class AddProduct(StaffRequiredMixin, SuccessMessageMixin, CreateView):
    """ Add Product View for management dashboard """
    model = Product
    fields = '__all__'
    template_name = 'management/dashboard_form.html'
    success_url = '/management/'
    success_message = '%(name)s was created'


class EditProduct(StaffRequiredMixin, SuccessMessageMixin, UpdateView):
    """ Edit Product View for management dashboard """
    model = Product
    fields = '__all__'
    template_name = 'management/dashboard_form.html'
    success_url = '/management/'
    success_message = '%(name)s was updated'


class DeleteProduct(StaffRequiredMixin, DeleteView):
    """ Delete Product View for management dashboard """
    model = Product
    template_name = 'management/confirm_delete.html'
    success_url = '/management/'


class ReviewDashboard(StaffRequiredMixin, View):
    """
    View for admin accessible review dashboard.
    """
    def get(self, request):
        reviews = Reviews.objects.all().order_by('-added_on')
        template_name = 'management/user_reviews.html'
        context = {
            'reviews': reviews,
        }
        return render(request, template_name, context)


class RemoveReview(StaffRequiredMixin, DeleteView):
    model = Reviews
    template_name = 'management/confirm_delete.html'
    success_url = '/management/user_reviews'


def approve_review(request, pk):
    if request.user.is_staff:
        review = get_object_or_404(Reviews, pk=pk)
        review.approved = True
        review.save()
        return redirect('management:user_reviews')
    else:
        return redirect('account_login')


def update_stock(request, pk):
    if request.user.is_staff:
        variant = Variant.objects.get(pk=pk)
        form = StockForm(request.POST or None, instance=variant)
        if form.is_valid():
            form.save()
            messages.success(request, f'{variant.size} stock updated.')
            return HttpResponse(status=204)
        else:
            form = StockForm(request.POST or None, instance=variant)
        context = {
            'variant': variant,
            'form': form,
        }
        return render(request, 'management/update_stock.html', context)
    else:
        return redirect('account_login')


class RecipeList(StaffRequiredMixin, generic.ListView):
    model = Recipe
    template_name = 'management/recipes.html'
    paginate_by = 10

    def get_queryset(self):
        queryset = Recipe.objects.order_by('-published', '-created')
        return queryset


def publish_recipe(request, pk):
    if request.user.is_staff:
        recipe = get_object_or_404(Recipe, pk=pk)
        recipe.published = True
        recipe.save()
        return redirect('management:recipes')
    else:
        return redirect('account_login')


class CommentList(StaffRequiredMixin, generic.ListView):
    model = Comment
    template_name = 'management/recipe_comments.html'
    paginate_by = 10

    def get_queryset(self):
        queryset = Comment.objects.order_by('-approved')
        return queryset


def approve_comment(request, pk):
    if request.user.is_staff:
        comment = get_object_or_404(Comment, pk=pk)
        comment.approved = True
        comment.save()
        return redirect('management:recipe_comments')
    else:
        return redirect('account_login')


class UserRecipeList(StaffRequiredMixin, generic.ListView):
    model = SubmittedRecipe
    template_name = 'management/user_recipes.html'
    paginate_by = 10

    def get_queryset(self):
        queryset = SubmittedRecipe.objects.order_by('-submitted_on')
        return queryset


def publish_submitted_recipe(request, pk):
    if request.user.is_staff:
        recipe = get_object_or_404(SubmittedRecipe, pk=pk)
        recipe.published = True
        recipe.save()
        return redirect('management:user_recipes')
    else:
        return redirect('account_login')
