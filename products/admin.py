from django.contrib import admin

from .models import Category, SubCategory, ProductVariant, Product


@admin.register(ProductVariant)
class ProductVariantAdmin(admin.ModelAdmin):
    list_filter = ('size',)
    list_display = ('size', 'price',)
    search_fields = ('size',)


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_filter = ('category', 'subcategory', 'in_stock',)
    list_display = ('name', 'category', 'subcategory', 'current_stock',
                    'in_stock')
    search_fields = ('name', 'category', 'subcategory',)


admin.site.register(Category)
admin.site.register(SubCategory)
