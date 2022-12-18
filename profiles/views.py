from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages
from django.contrib.messages.views import SuccessMessageMixin
from django.views import View, generic
from django.views.generic import UpdateView, DeleteView
from django.contrib.auth.models import User
from django.contrib.auth import logout

from checkout.models import Order
from recipes.models import SubmittedRecipe

from .models import UserProfile, Reviews
from .forms import ProfileForm, DeleteAccountForm


class ProfileView(LoginRequiredMixin, View):
    """
    Profile view
    Generic view
    With LoginRequiredMixin as only registered user's have
    profiles, so redirects to login for users not logged in
    """
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
    """
    Update Profile view
    UpdateView - form_class included to exclude "user" field from form
    LoginRequiredMixin as only registered user's have profiles so redirects to
    login for users not logged in
    SuccessMessageMixin so success message displayed when successfully
    submitted
    """
    model = UserProfile
    form_class = ProfileForm
    template_name = 'profiles/profile_form.html'
    success_url = '/profiles/profile/'
    success_message = 'Your details were updated successfully.'

    def get_object(self):
        return self.request.user.userprofile


class DeleteAccount(LoginRequiredMixin, View):
    """
    Deletes the currently signed-in user
    LoginRequiredMixin as only registered user may need to delete account
    """
    def get(self, request, *args, **kwargs):
        """
        Get the confirm delete template with DeleteAccountForm
        """
        form = DeleteAccountForm()
        template_name = 'profiles/confirm_delete.html'
        context = {
            'form': form,
        }
        return render(request, template_name, context)

    def post(self, request, *args, **kwargs):
        """
        Deletes user
        Redirects to index
        """
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
    """
    Review list view
    Generic list view, paginated
    Queryset filtered to return reviews by user, ordered by most recent
    """
    model = Reviews
    template_name = 'profiles/review_list.html'
    paginate_by = 5

    def get_queryset(self):
        queryset = Reviews.objects.filter(reviewer=self.request.user.userprofile).order_by('-added_on')  # noqa
        return queryset


class EditReview(LoginRequiredMixin, SuccessMessageMixin, UpdateView):
    """
    Edit review view
    UpdateView - only two fields required so specified in view
    LoginRequiredMixin as only registered user's can edit reviews so redirects
    to login for users not logged in
    SuccessMessageMixin so success message displayed when successfully
    submitted
    """
    model = Reviews
    fields = ('content', 'rating',)
    template_name = 'profiles/review_form.html'
    success_url = '/profiles/review_list/'
    success_message = 'Your review was updated'


class DeleteReview(LoginRequiredMixin, DeleteView):
    """
    Delete review view
    DeleteView used
    LoginRequiredView as only registered user's and staff can delete reviews
    """
    model = Reviews
    template_name = 'profiles/delete_review.html'
    success_url = '/profiles/review_list/'


class OrderHistory(LoginRequiredMixin, View):
    """
    Order history view
    Generic view
    LoginRequiredView as only registered user's can view their order history
    from their profile
    Gets order using checkout success template
    """
    def get(self, request, order_number):
        order = get_object_or_404(Order, order_number=order_number)
        template_name = 'checkout/checkout_success.html'
        context = {
            'order': order,
        }
        return render(request, template_name, context)


class UserRecipeList(generic.ListView):
    """
    User recipe list
    Genergic list view, paginated
    Queryset filtered to return user's own submitted recipes order by date
    submitted on
    """
    model = SubmittedRecipe
    template_name = 'profiles/user_recipes.html'
    paginate_by = 10

    def get_queryset(self):
        queryset = SubmittedRecipe.objects.filter(user=self.request.user).order_by('-submitted_on')  # noqa
        return queryset
