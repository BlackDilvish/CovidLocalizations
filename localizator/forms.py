from django import forms
from django.core.validators import FileExtensionValidator

class FileForm(forms.Form):
    uplfile = forms.FileField(label='Select a file with localization')

class StatusForm(forms.Form):
    check = forms.BooleanField(required=False)
    #start_date = forms.DateField(required=False)
    #end_date = forms.DateField(required=False)

