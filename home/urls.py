from django.urls import path

from . import views

app_name = 'home'
urlpatterns = [
    path('', views.IndexView.as_view(), name='index'),
    path('contact/', views.ContactView.as_view(), name='contact'),
    path('privacy/', views.PrivacyPolicyView.as_view(), name='privacy'),
    path('faq/', views.FaqView.as_view(), name='faq')
]
