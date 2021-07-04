from django import forms
from qa.models import Question


class QuestionForm(forms.ModelForm):
    class Meta:
        model = Question
        fields = ['title', 'body_html', 'tags']


class SearchForm(forms.Form):
    q = forms.CharField()
