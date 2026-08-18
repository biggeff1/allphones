from django import forms
from .models import DepositRequest, InterestRequest

class InterestRequestForm(forms.ModelForm):
    class Meta:
        model = InterestRequest
        fields = ["full_name", "phone", "email", "message", "preferred_date", "preferred_time"]
        widgets = {"preferred_date": forms.DateInput(attrs={"type": "date"}), "preferred_time": forms.TimeInput(attrs={"type": "time"})}
    def clean_phone(self):
        phone = self.cleaned_data["phone"].strip()
        if len(phone) < 8: raise forms.ValidationError("Numéro de téléphone invalide.")
        return phone

class DepositRequestForm(forms.ModelForm):
    class Meta:
        model = DepositRequest
        fields = ["full_name", "phone", "email", "category", "brand", "model", "condition", "description", "expected_price", "currency"]
    def clean_phone(self):
        phone = self.cleaned_data["phone"].strip()
        if len(phone) < 8: raise forms.ValidationError("Numéro de téléphone invalide.")
        return phone
