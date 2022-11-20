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
        template_name = 'products/product_admin.html'
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
    template_name = 'products/form.html'
    success_url = '/products/product_admin/'


class EditCategory(UpdateView):
    """ Edit Category View for management dashboard """
    model = Category
    fields = '__all__'
    template_name = 'products/form.html'
    success_url = '/products/product_admin/'


class DeleteCategory(DeleteView):
    """ Delete Category View for management dashboard """
    model = Category
    template_name = 'products/confirm_delete.html'
    success_url = '/products/product_admin/'


class AddSubCategory(CreateView):
    """ Add Subcategory View for management dashboard """
    model = SubCategory
    fields = '__all__'
    template_name = 'products/form.html'
    success_url = '/products/product_admin/'


class EditSubCategory(UpdateView):
    """ Edit Subategory View for management dashboard """
    model = SubCategory
    fields = '__all__'
    template_name = 'products/form.html'
    success_url = '/products/product_admin/'


class DeleteSubCategory(DeleteView):
    """ Delete Subcategory View for management dashboard """
    model = SubCategory
    template_name = 'products/confirm_delete.html'
    success_url = '/products/product_admin/'


class AddProductVariant(CreateView):
    """ Add Variant View for management dashboard """
    model = ProductVariant
    fields = '__all__'
    template_name = 'products/form.html'
    success_url = '/products/product_admin/'


class EditProductVariant(UpdateView):
    """ Edit Variant View for management dashboard """
    model = ProductVariant
    fields = '__all__'
    template_name = 'products/form.html'
    success_url = '/products/product_admin/'


class DeleteProductVariant(DeleteView):
    """ Delete Variant View for management dashboard """
    model = ProductVariant
    template_name = 'products/confirm_delete.html'
    success_url = '/products/product_admin/'


class AddProduct(CreateView):
    """ Add Product View for management dashboard """
    model = Product
    fields = '__all__'
    template_name = 'products/form.html'
    success_url = '/products/product_admin/'


class EditProduct(UpdateView):
    """ Edit Product View for management dashboard """
    model = Product
    fields = '__all__'
    template_name = 'products/form.html'

    def get_success_url(self):
        return reverse('products:product', args=(self.object.slug,))


class DeleteProduct(DeleteView):
    """ Delete Product View for management dashboard """
    model = Product
    template_name = 'products/confirm_delete.html'
    success_url = '/products/product_admin/'
