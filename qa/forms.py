from django import forms
from django.utils.translation import gettext as _
from qa.models import Question, Comment
from django.apps import apps
from django.contrib.contenttypes.models import ContentType


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


class CommentCreateForm(forms.ModelForm):
    
    content_type = forms.ModelChoiceField(
        required=True, queryset=ContentType.objects.filter(model__in=["question", "answer"])
    )
    
    def clean(self):
        cd = super().clean()
        
        try:
            content_type = cd.get("content_type")
            DynamicModel = apps.get_model(content_type.app_label, content_type.model)
            DynamicModel.objects.get(id=cd.get("object_id"))
        except:
            raise forms.ValidationError(_(f"No question or answer with this {cd.get('object_id')}."))
        
        return cd
    
    class Meta:
        model = Comment
        fields = [
            "parent",   
            "content_type",
            "object_id",
            "text",
        ]
        

class CommentUpdateForm(forms.Form):
    
    text = forms.CharField(required=True, min_length=15, max_length=600, widget=forms.Textarea)        
    