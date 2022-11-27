from django.urls import path

from . import views


app_name = 'checkout'
urlpatterns = [
    path('', views.checkout, name='checkout'),
    path('checkout_success/<order_number>', views.checkout_success,
         name='checkout_success'),
    path('order_pdf/<pk>', views.order_pdf, name='order_pdf'),
]
