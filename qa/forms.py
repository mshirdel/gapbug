from django import forms
from django.utils.translation import gettext as _
from qa.models import Question


class QuestionForm(forms.ModelForm):
    class Meta:
        model = Question
        fields = ["title", "body_html", "tags"]

    def clean_tags(self):
        selected_tags = self.cleaned_data["tags"]
        if len(selected_tags) > 5:
            raise forms.ValidationError(_("You can only select 5 tags"))
        else:
            return self.cleaned_data["tags"]


class SearchForm(forms.Form):
    q = forms.CharField()
