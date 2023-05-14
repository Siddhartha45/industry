from django import forms
from .models import CustomUser
from django.core.validators import validate_email


class CustomUserForm(forms.Form):
    email = forms.EmailField()
    username = forms.CharField()
    fullname = forms.CharField()
    phone_no = forms.CharField()
    role = forms.ChoiceField(choices=CustomUser.ROLE_CHOICES)

    
    def clean_phone_no(self):
        phone_no = self.cleaned_data['phone_no']
        if len(phone_no) < 10 or len(phone_no) > 15:
            raise forms.ValidationError("Please enter correct phone number")
        return phone_no
        