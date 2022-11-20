from django.shortcuts import render, reverse
from django.views import View
from django.views.generic import CreateView, UpdateView, DeleteView, ListView
from django.contrib import messages
from django.contrib.messages.views import SuccessMessageMixin


from products.models import Category, SubCategory, Product, ProductVariant

"""
Revisit for messages and restrict login to superusers
"""


class ProductDashboard(View):
    """
    View for admin accessible management dashboard.
    """
    def get(self, request):
        categories = Category.objects.all()
        subcategories = SubCategory.objects.all()
        variants = ProductVariant.objects.all()
        products = Product.objects.all().order_by('category')
        template_name = 'management/dashboard.html'
        context = {
            'categories': categories,
            'subcategories': subcategories,
            'variants': variants,
            'products': products,
        }
        return render(request, template_name, context)


class AddCategory(SuccessMessageMixin, CreateView):
    """ Add Category view for management dashboard """
    model = Category
    fields = '__all__'
    template_name = 'management/dashboard_form.html'
    success_url = '/management/'
    success_message = '%(name)s was created'


class EditCategory(SuccessMessageMixin, UpdateView):
    """ Edit Category View for management dashboard """
    model = Category
    fields = '__all__'
    template_name = 'management/dashboard_form.html'
    success_url = '/management/'
    success_message = '%(name)s was updated'


class DeleteCategory(DeleteView):
    """ Delete Category View for management dashboard """
    model = Category
    template_name = 'management/confirm_delete.html'
    success_url = '/management/'


class AddSubCategory(SuccessMessageMixin, CreateView):
    """ Add Subcategory View for management dashboard """
    model = SubCategory
    fields = '__all__'
    template_name = 'management/dashboard_form.html'
    success_url = '/management/'
    success_message = '%(name)s was created'


class EditSubCategory(SuccessMessageMixin, UpdateView):
    """ Edit Subategory View for management dashboard """
    model = SubCategory
    fields = '__all__'
    template_name = 'management/dashboard_form.html'
    success_url = '/management/'
    success_message = '%(name)s was updated'


class DeleteSubCategory(DeleteView):
    """ Delete Subcategory View for management dashboard """
    model = SubCategory
    template_name = 'management/confirm_delete.html'
    success_url = '/management/'


class AddProductVariant(SuccessMessageMixin, CreateView):
    """ Add Variant View for management dashboard """
    model = ProductVariant
    fields = '__all__'
    template_name = 'management/dashboard_form.html'
    success_url = '/management/'
    success_message = '%(size)s was created'


class EditProductVariant(SuccessMessageMixin, UpdateView):
    """ Edit Variant View for management dashboard """
    model = ProductVariant
    fields = '__all__'
    template_name = 'management/dashboard_form.html'
    success_url = '/management/'
    success_message = '%(name)s was updated'


class DeleteProductVariant(DeleteView):
    """ Delete Variant View for management dashboard """
    model = ProductVariant
    template_name = 'management/confirm_delete.html'
    success_url = '/management/'


class AddProduct(SuccessMessageMixin, CreateView):
    """ Add Product View for management dashboard """
    model = Product
    fields = '__all__'
    template_name = 'management/dashboard_form.html'
    success_url = '/management/'
    success_message = '%(name)s was created'


class EditProduct(SuccessMessageMixin, UpdateView):
    """ Edit Product View for management dashboard """
    model = Product
    fields = '__all__'
    template_name = 'management/dashboard_form.html'
    success_url = '/management/'
    success_message = '%(name)s was updated'


class DeleteProduct(DeleteView):
    """ Delete Product View for management dashboard """
    model = Product
    template_name = 'management/confirm_delete.html'
    success_url = '/management/'
