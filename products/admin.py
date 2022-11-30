from django.contrib import admin

from .models import Category, Variant, Product


class VariantAdminInline(admin.TabularInline):
    model = Variant


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    inlines = (VariantAdminInline,)

    list_filter = ('category', 'subcategory',)
    list_display = ('name', 'category', 'subcategory',)
    search_fields = ('name', 'category', 'subcategory',)


admin.site.register(Category)
