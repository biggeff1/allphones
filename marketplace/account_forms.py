from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

class RegisterForm(UserCreationForm):
    email = forms.EmailField(required=False)
    class Meta:
        model = User
        fields = ("username", "email", "password1", "password2")

class MultipleImageForm(forms.Form):
    images = forms.FileField(
        required=False,
        widget=forms.ClearableFileInput(attrs={"accept": "image/*", "multiple": True, "capture": "environment"}),
    )
