from django import forms

from .models import Comment


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ('content', 'rating',)
        widgets = {
            'content': forms.Textarea(attrs={'cols': 40, 'rows': 5}),
        }
