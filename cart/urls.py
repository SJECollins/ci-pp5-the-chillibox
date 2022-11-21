from django.urls import path

from . import views


app_name = 'cart'
urlpatterns = [
    path('', views.ViewCart.as_view(), name='view_cart'),
    path('add/<item_id>', views.add_to_cart, name='add_to_cart'),
    path('update/<item_id>', views.adjust_cart, name='adjust_cart'),
    path('remove/<item_id>', views.remove_item, name='remove_item'),
]
