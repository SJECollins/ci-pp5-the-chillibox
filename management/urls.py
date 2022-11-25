from django.urls import path

from . import views


app_name = 'management'
urlpatterns = [
    path('', views.ProductDashboard.as_view(), name='dashboard'),
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
