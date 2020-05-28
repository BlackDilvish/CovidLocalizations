from django import forms
from django.core.validators import FileExtensionValidator

class FileForm(forms.Form):
    uplfile = forms.FileField(label='Select a file with localization')

