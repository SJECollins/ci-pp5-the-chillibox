from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages
from django.contrib.messages.views import SuccessMessageMixin
from django.views import View, generic
from django.views.generic import UpdateView, DeleteView
from django.contrib.auth.models import User
from django.contrib.auth import logout

from checkout.models import Order

from .models import UserProfile, Reviews
from .forms import ProfileForm, DeleteAccountForm


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


class DeleteAccount(LoginRequiredMixin, View):
    """
    Deletes the currently signed-in user.
    """
    def get(self, request, *args, **kwargs):
        form = DeleteAccountForm()
        template_name = 'profiles/confirm_delete.html'
        context = {
            'form': form,
        }
        return render(request, template_name, context)

    def post(self, request, *args, **kwargs):
        template_name = 'profiles/confirm_delete.html'
        form = DeleteAccountForm(request.POST)
        if form.is_valid():
            user = request.user
            logout(request)
            user.delete()
            messages.success(request, 'You account was deleted.')
            return redirect('/')
        context = {
            'form': form,
        }
        return render(request, template_name, context)


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
