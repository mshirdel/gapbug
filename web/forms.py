from django import forms


class FileUploadForm(forms.Form):
    file = forms.ImageField()
    key = forms.CharField()
