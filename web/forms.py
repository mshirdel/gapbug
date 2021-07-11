from django import forms


class FileUploadForm(forms.Form):
    file = forms.FileField()
    key = forms.CharField()
