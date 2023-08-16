from django.forms import ModelForm
from .models import Report
from django import forms


class ReportForm(ModelForm):
    class Meta:
        model = Report
        fields = ['message', 'issue_image']
        
        
class UploadFileForm(forms.Form):
    file = forms.FileField()