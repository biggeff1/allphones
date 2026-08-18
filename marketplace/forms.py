from django import forms
from .models import InterestRequest

class InterestRequestForm(forms.ModelForm):
    class Meta:
        model = InterestRequest
        fields = ["full_name", "phone", "email", "message", "preferred_date", "preferred_time"]
        widgets = {
            "preferred_date": forms.DateInput(attrs={"type": "date"}),
            "preferred_time": forms.TimeInput(attrs={"type": "time"}),
        }

    def clean_phone(self):
        phone = self.cleaned_data["phone"].strip()
        if len(phone) < 8:
            raise forms.ValidationError("Numéro de téléphone invalide.")
        return phone
