from django import forms

from .models import Comment


class CommentForm(forms.ModelForm):
    """
    Comment form for use on recipe page
    Specify text area
    """
    class Meta:
        model = Comment
        fields = ('content',)
        widgets = {
            'content': forms.Textarea(attrs={'cols': 40, 'rows': 5}),
        }
