from django.urls import path

from . import views


app_name = 'management'
urlpatterns = [
    path('', views.ProductDashboard.as_view(), name='dashboard'),
    path('add_category/', views.AddCategory.as_view(),
         name='add_category'),
    path('edit_category/<pk>', views.EditCategory.as_view(),
         name='edit_category'),
    path('delete_category/<pk>', views.DeleteCategory.as_view(),
         name='delete_category'),
    path('add_subcategory/', views.AddSubCategory.as_view(),
         name='add_subcategory'),
    path('edit_subcategory/<pk>', views.EditSubCategory.as_view(),
         name='edit_subcategory'),
    path('delete_subcategory/<pk>', views.DeleteSubCategory.as_view(),
         name='delete_subcategory'),
    path('add_variant/<slug>', views.AddVariant.as_view(),
         name='add_variant'),
    path('edit_variant/<pk>', views.EditVariant.as_view(),
         name='edit_variant'),
    path('delete_variant/<pk>', views.DeleteVariant.as_view(),
         name='delete_variant'),
    path('add_product/', views.AddProduct.as_view(), name='add_product'),
    path('edit_product/<pk>', views.EditProduct.as_view(),
         name='edit_product'),
    path('delete_product/<pk>', views.DeleteProduct.as_view(),
         name='delete_product'),
]
