from django.urls import path

from . import views


app_name = 'profiles'
urlpatterns = [
     path('profile/', views.ProfileView.as_view(), name='profile'),
     path('edit_profile/', views.UpdateProfile.as_view(), name='edit_profile'),
     path('delete_account/', views.DeleteAccount.as_view(), name='delete_account'),
     path('order_history/<order_number>', views.OrderHistory.as_view(),
          name='order_history'),
     path('review_list/', views.ReviewList.as_view(), name='review_list'),
     path('edit_review/<pk>', views.EditReview.as_view(), name='edit_review'),
     path('delete_review/<pk>', views.DeleteReview.as_view(),
          name='delete_review'),
]
