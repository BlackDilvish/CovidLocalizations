from django import forms

class FileForm(forms.Form):
    uplfile = forms.FileField(label='Select a file with localization')