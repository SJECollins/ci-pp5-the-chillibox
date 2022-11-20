from django.shortcuts import render, reverse
from django.views import View
from django.views.generic import CreateView, UpdateView, DeleteView, ListView


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


class AddCategory(CreateView):
    """ Add Category view for management dashboard """
    model = Category
    fields = '__all__'
    template_name = 'management/dashboard_form.html'
    success_url = '/management/dashboard/'


class EditCategory(UpdateView):
    """ Edit Category View for management dashboard """
    model = Category
    fields = '__all__'
    template_name = 'management/dashboard_form.html'
    success_url = '/management/dashboard/'


class DeleteCategory(DeleteView):
    """ Delete Category View for management dashboard """
    model = Category
    template_name = 'management/confirm_delete.html'
    success_url = '/management/dashboard/'


class AddSubCategory(CreateView):
    """ Add Subcategory View for management dashboard """
    model = SubCategory
    fields = '__all__'
    template_name = 'management/dashboard_form.html'
    success_url = '/management/dashboard/'


class EditSubCategory(UpdateView):
    """ Edit Subategory View for management dashboard """
    model = SubCategory
    fields = '__all__'
    template_name = 'management/dashboard_form.html'
    success_url = '/management/dashboard/'


class DeleteSubCategory(DeleteView):
    """ Delete Subcategory View for management dashboard """
    model = SubCategory
    template_name = 'management/confirm_delete.html'
    success_url = '/management/dashboard/'


class AddProductVariant(CreateView):
    """ Add Variant View for management dashboard """
    model = ProductVariant
    fields = '__all__'
    template_name = 'management/dashboard_form.html'
    success_url = '/management/dashboard/'


class EditProductVariant(UpdateView):
    """ Edit Variant View for management dashboard """
    model = ProductVariant
    fields = '__all__'
    template_name = 'management/dashboard_form.html'
    success_url = '/management/dashboard/'


class DeleteProductVariant(DeleteView):
    """ Delete Variant View for management dashboard """
    model = ProductVariant
    template_name = 'management/confirm_delete.html'
    success_url = '/management/dashboard/'


class AddProduct(CreateView):
    """ Add Product View for management dashboard """
    model = Product
    fields = '__all__'
    template_name = 'management/dashboard_form.html'
    success_url = '/management/dashboard/'


class EditProduct(UpdateView):
    """ Edit Product View for management dashboard """
    model = Product
    fields = '__all__'
    template_name = 'management/dashboard_form.html'

    def get_success_url(self):
        return reverse('products:product', args=(self.object.slug,))


class DeleteProduct(DeleteView):
    """ Delete Product View for management dashboard """
    model = Product
    template_name = 'management/confirm_delete.html'
    success_url = '/management/dashboard/'
