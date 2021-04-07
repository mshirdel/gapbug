from django.db import models
from django.contrib.auth import get_user_model
from common.models import TimeStampModel


class Question(TimeStampModel):
    user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)
    title = models.CharField(max_length=400)
    body_md = models.TextField()
    body_html = models.TextField()
    vote = models.IntegerField()

    def update_number_of_votes(self):
        self.vote = self.vote_set.count()
        self.save()


class Vote(TimeStampModel):
    user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)
    question = models.ForeignKey(Question, on_delete=models.CASCADE)

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        self.question.update_number_of_votes()

    def delete(self, *args, **kwargs):
        super().delete(*args, **kwargs)
        self.question.update_number_of_votes()
