from django.shortcuts import render, get_object_or_404
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages
from django.contrib.messages.views import SuccessMessageMixin
from django.views import View, generic
from django.views.generic import UpdateView, DeleteView

from checkout.models import Order

from .models import UserProfile, Reviews
from .forms import ProfileForm


class ProfileView(LoginRequiredMixin, View):
    def get(self, request):
        profile = get_object_or_404(UserProfile, user=request.user)
        orders = profile.orders.all().order_by('-date')
        template_name = 'profiles/profile.html'
        context = {
            'profile': profile,
            'orders': orders,
            }
        return render(request, template_name, context)


class UpdateProfile(LoginRequiredMixin, SuccessMessageMixin, UpdateView):
    model = UserProfile
    form_class = ProfileForm
    template_name = 'profiles/profile_form.html'
    success_url = '/profiles/profile/'
    success_message = 'Your details were updated successfully.'

    def get_object(self):
        return self.request.user.userprofile


class ReviewList(LoginRequiredMixin, generic.ListView):
    model = Reviews
    template_name = 'profiles/review_list.html'
    paginate_by = 5

    def get_queryset(self):
        queryset = Reviews.objects.filter(reviewer=self.request.user.userprofile).order_by('-added_on')
        return queryset


class EditReview(LoginRequiredMixin, SuccessMessageMixin, UpdateView):
    model = Reviews
    fields = ('content', 'rating',)
    template_name = 'profiles/review_form.html'
    success_url = '/profiles/review_list/'
    success_message = 'Your review was updated'


class DeleteReview(LoginRequiredMixin, DeleteView):
    model = Reviews
    template_name = 'profiles/delete_review.html'
    success_url = '/profiles/review_list/'


class OrderHistory(LoginRequiredMixin, View):
    def get(self, request, order_number):
        order = get_object_or_404(Order, order_number=order_number)
        template_name = 'checkout/checkout_success.html'
        context = {
            'order': order,
        }
        return render(request, template_name, context)
