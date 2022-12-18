from django.contrib import admin

from .models import Category, Variant, Product


class VariantAdminInline(admin.TabularInline):
    """
    We want variant as a tabular inline for product
    """
    model = Variant


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    """
    Registering product with admin, with variant as inline
    """
    inlines = (VariantAdminInline,)

    list_filter = ('category', 'subcategory',)
    list_display = ('name', 'category', 'subcategory',)
    search_fields = ('name', 'category', 'subcategory',)


# Register category with admin
admin.site.register(Category)
