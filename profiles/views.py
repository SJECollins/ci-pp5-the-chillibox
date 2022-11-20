from django.shortcuts import render, get_object_or_404
from django.contrib.auth.mixins import LoginRequiredMixin
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


class UpdateProfile(LoginRequiredMixin, UpdateView):
    model = UserProfile
    form_class = ProfileForm
    template_name = 'profiles/profile_form.html'
    success_url = '/profiles/'

    def get_object(self):
        return self.request.user.userprofile
