from django import forms
from .models import Snippet
from django.forms import ModelForm, Textarea

class SnippetForm(forms.ModelForm):
    text = forms.CharField(widget=forms.Textarea())
    class Meta:
        model = Snippet
        fields = ["text" , ]
