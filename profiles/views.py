from django.shortcuts import render, get_object_or_404
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages
from django.contrib.messages.views import SuccessMessageMixin
from django.views import View
from django.views.generic import UpdateView

from .models import UserProfile
from .forms import ProfileForm


class ProfileView(LoginRequiredMixin, View):
    def get(self, request):
        profile = get_object_or_404(UserProfile, user=request.user)
        template_name = 'profiles/profile.html'
        context = {'profile': profile, }
        return render(request, template_name, context)


class UpdateProfile(LoginRequiredMixin, SuccessMessageMixin, UpdateView):
    model = UserProfile
    form_class = ProfileForm
    template_name = 'profiles/profile_form.html'
    success_url = '/profiles/'
    success_message = 'Your details were updated successfully.'

    def get_object(self):
        return self.request.user.userprofile
