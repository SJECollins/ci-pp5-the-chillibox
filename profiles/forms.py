from django import forms

from .models import UserProfile, Reviews


class ProfileForm(forms.ModelForm):
    """
    Profile form for user to add/edit details
    """
    class Meta:
        model = UserProfile
        exclude = ['user']


class DeleteAccountForm(forms.Form):
    """
    Simple form that provides a checkbox that signals deletion.
    """
    delete = forms.BooleanField(required=True)


class ReviewForm(forms.ModelForm):
    """
    Review form for user to edit review
    """
    class Meta:
        model = Reviews
        fields = ('content', 'rating',)
        widgets = {
            'content': forms.Textarea(attrs={'cols': 40, 'rows': 5}),
            'rating': forms.NumberInput(attrs={'min': 1, 'max': 5, 'step': 1})
        }
        labels = {
            'content': 'Your review:',
            'rating': 'Your rating (from 1 to 5):'
        }
