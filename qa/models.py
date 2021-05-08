from django.db import models
from django.db.models import Sum
from django.contrib.auth import get_user_model
from django.utils.text import slugify
from django.utils.translation import gettext as _
from django.urls import reverse
from common.models import TimeStampModel
from django.conf import settings


class Question(TimeStampModel):
    user = models.ForeignKey(settings.AUTH_USER_MODEL,
                             on_delete=models.CASCADE,
                             related_name='questions')
    title = models.CharField(max_length=400, db_index=True)
    body_md = models.TextField()
    body_html = models.TextField()
    vote = models.IntegerField(default=0)
    slug = models.SlugField(max_length=400, db_index=True, allow_unicode=True)

    def get_absolute_url(self):
        return reverse("qa:show", kwargs={"id": self.id, 'slug': self.slug})

    def save(self, *args, **kwargs):
        self.slug = slugify(self.title, allow_unicode=True)
        super().save(*args, **kwargs)

    class Meta:
        ordering = ('-created',)


class Answer(TimeStampModel):
    user = models.ForeignKey(settings.AUTH_USER_MODEL,
                             on_delete=models.CASCADE,
                             related_name='answers')
    question = models.ForeignKey(Question,
                                 on_delete=models.CASCADE)
    body_md = models.TextField()
    body_html = models.TextField()
    vote = models.IntegerField(default=0)

    class Meta:
        ordering = ('vote',)


class Vote(TimeStampModel):
    user = models.ForeignKey(settings.AUTH_USER_MODEL,
                             on_delete=models.CASCADE)
    rate = models.SmallIntegerField()

    class Meta:
        abstract = True


class QuestionVote(Vote):
    question = models.ForeignKey(Question,
                                 on_delete=models.CASCADE,
                                 related_name='number_of_votes')

    class Meta:
        unique_together = ['user', 'question']

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        qs = QuestionVote.objects.filter(question=self.question)
        self.question.vote = qs.aggregate(Sum('rate'))['rate__sum']
        self.question.save()


class AnswerVote(Vote):
    answer = models.ForeignKey(Answer,
                               on_delete=models.CASCADE,
                               related_name='number_of_votes')

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        qs = QuestionVote.objects.filter(answer=self.answer)
        self.answer.vote = qs.aggregate(Sum('rate'))['rate__sum']
        self.answer.save()
