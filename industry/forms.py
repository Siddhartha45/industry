from django.forms import ModelForm
from .models import Industry, IndustryPhoto
from django import forms


class IndustryForm(ModelForm):
    industry_name = forms.CharField(required=True)
    
    def clean(self):
        cleaned_data = super().clean()

        for field_name in ['total_manpower', 'skillfull', 'unskilled', 'indigenous', 'foreign', 'male', 'female']:
            if field_name in cleaned_data and cleaned_data[field_name] is None:
                cleaned_data[field_name] = 0
    
    class Meta:
        model = Industry
        fields = "__all__"