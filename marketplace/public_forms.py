from django import forms
from .models import Listing

class PublicListingForm(forms.ModelForm):
    class Meta:
        model = Listing
        fields = ["title", "category", "brand", "model", "condition", "description", "location"]
        widgets = {"description": forms.Textarea(attrs={"rows": 5, "placeholder": "Décrivez l'état, les défauts, accessoires, etc."})}
