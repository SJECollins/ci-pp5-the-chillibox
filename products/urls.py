from django.urls import path

from . import views


app_name = 'products'
urlpatterns = [
    path('', views.LatestProducts.as_view(), name='all'),
    path('category/<str:slug>', views.CategoryView.as_view(), name='category'),
]
