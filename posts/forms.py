from django import forms
from .models import Comment


class CommentForm(forms.Form):
    content_type = forms.CharField(widget=forms.HiddenInput)
    object_id = forms.IntegerField(widget=forms.HiddenInput)
    content = forms.CharField(
        label='',
        widget=forms.TextInput(attrs={
            'class': 'w3-input w3-border'
        })
    )