from django.shortcuts import render, reverse, get_object_or_404
from django.views import View
from django.views.generic import CreateView, UpdateView, DeleteView, ListView
from django.contrib import messages
from django.contrib.messages.views import SuccessMessageMixin

from .mixins import StaffRequiredMixin


from products.models import Category, SubCategory, Product, Variant

"""
Revisit for messages and restrict login to superusers
"""


class ProductDashboard(StaffRequiredMixin, View):
    """
    View for admin accessible management dashboard.
    """
    def get(self, request):
        seeds = Product.objects.filter(category__slug='seeds')
        sauces = Product.objects.filter(category__slug='sauces')
        seedboxes = Product.objects.filter(category__slug='seedbox')
        sauceboxes = Product.objects.filter(category__slug='saucebox')
        template_name = 'management/dashboard.html'
        context = {
            'seeds': seeds,
            'sauces': sauces,
            'seedboxes': seedboxes,
            'sauceboxes': sauceboxes,
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
