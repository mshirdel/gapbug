from django import forms


class QuestionForm(forms.Form):
    title = forms.CharField(max_length=400)
    body_html = forms.CharField()
