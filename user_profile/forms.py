from django import forms
from django.forms import widgets
from .models import Profile


class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ('title', 'about_me',)
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control'}),
            'about_me': forms.HiddenInput(attrs={'id': 'aboutMeEditor'})
        }
