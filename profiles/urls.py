from django.urls import path

from . import views


app_name = 'profiles'
urlpatterns = [
    path('profile/', views.ProfileView.as_view(), name='profile'),
    path('edit_profile/', views.UpdateProfile.as_view(), name='edit_profile'),
    path('order_history/<order_number>', views.OrderHistory.as_view(), name='order_history'),
]
