from django.contrib import admin
from .models import Question, Comment


class QuestionAdmin(admin.ModelAdmin):
    list_display = ("title", "user")
    
admin.site.register(Question, QuestionAdmin)
admin.site.register(Comment)
