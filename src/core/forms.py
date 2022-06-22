from .models import _Post, _Comments
from django import forms

class PostForm(forms.ModelForm):
    class Meta:
        model = _Post
        fields = ['image', 'caption',]

class CommentForm(forms.ModelForm):
    class Meta:
        model = _Comments
        fields = ['comment',]




