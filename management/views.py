from django.shortcuts import render, reverse
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
        categories = Category.objects.all()
        subcategories = SubCategory.objects.all()
        variants = Variant.objects.all()
        products = Product.objects.all().order_by('category')
        template_name = 'management/dashboard.html'
        context = {
            'categories': categories,
            'subcategories': subcategories,
            'variants': variants,
            'products': products,
        }
        return render(request, template_name, context)


class AddCategory(StaffRequiredMixin, SuccessMessageMixin, CreateView):
    """ Add Category view for management dashboard """
    model = Category
    fields = '__all__'
    template_name = 'management/dashboard_form.html'
    success_url = '/management/'
    success_message = '%(name)s was created'


class EditCategory(StaffRequiredMixin, SuccessMessageMixin, UpdateView):
    """ Edit Category View for management dashboard """
    model = Category
    fields = '__all__'
    template_name = 'management/dashboard_form.html'
    success_url = '/management/'
    success_message = '%(name)s was updated'


class DeleteCategory(StaffRequiredMixin, DeleteView):
    """ Delete Category View for management dashboard """
    model = Category
    template_name = 'management/confirm_delete.html'
    success_url = '/management/'


class AddSubCategory(StaffRequiredMixin, SuccessMessageMixin, CreateView):
    """ Add Subcategory View for management dashboard """
    model = SubCategory
    fields = '__all__'
    template_name = 'management/dashboard_form.html'
    success_url = '/management/'
    success_message = '%(name)s was created'


class EditSubCategory(StaffRequiredMixin, SuccessMessageMixin, UpdateView):
    """ Edit Subategory View for management dashboard """
    model = SubCategory
    fields = '__all__'
    template_name = 'management/dashboard_form.html'
    success_url = '/management/'
    success_message = '%(name)s was updated'


class DeleteSubCategory(StaffRequiredMixin, DeleteView):
    """ Delete Subcategory View for management dashboard """
    model = SubCategory
    template_name = 'management/confirm_delete.html'
    success_url = '/management/'


class AddVariant(StaffRequiredMixin, SuccessMessageMixin, CreateView):
    """ Add Variant View for management dashboard """
    model = Variant
    fields = '__all__'
    template_name = 'management/dashboard_form.html'
    success_url = '/management/'
    success_message = '%(size)s was created'


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
