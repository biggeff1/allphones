from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

class RegisterForm(UserCreationForm):
    email = forms.EmailField(required=False)
    class Meta:
        model = User
        fields = ("username", "email", "password1", "password2")

class MultipleFileInput(forms.FileInput):
    allow_multiple_selected = True

class MultipleImageForm(forms.Form):
    images = forms.FileField(required=False, widget=MultipleFileInput(attrs={"accept": "image/*", "capture": "environment"}))
    def clean_images(self):
        files = self.files.getlist("images")
        if len(files) > 10:
            raise forms.ValidationError("Maximum 10 photos par annonce.")
        for image in files:
            if image.size > 5 * 1024 * 1024:
                raise forms.ValidationError("Chaque photo doit faire au maximum 5 Mo.")
            if not image.content_type or not image.content_type.startswith("image/"):
                raise forms.ValidationError("Seules les images sont acceptées.")
        return files
