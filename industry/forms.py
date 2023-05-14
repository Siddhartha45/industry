from django.forms import ModelForm, MultipleChoiceField, ClearableFileInput
from .models import Industry, IndustryPhoto
from django import forms


class IndustryForm(ModelForm):
    #industry_photo = forms.FileField(widget=MultipleFileInput(attrs={'multiple': True}), required=False)
    industry_name = forms.CharField(required=True)
    class Meta:
        model = Industry
        fields = "__all__"