from django import forms
from django.contrib.auth.forms import AuthenticationForm

from .models import Choice, Question

class LoginForm(AuthenticationForm):
    """ログインフォーム"""
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs['class'] = 'form-control'
            field.widget.attrs['placeholder'] = field.label

class ChoiceForm(forms.Form):
    choice = forms.ModelChoiceField(
        queryset=Choice.objects.all(),
        widget=forms.RadioSelect,
        empty_label=None,
    )
