from django.utils import timezone
from django.db import models
from django.db.models import Sum, Count
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
    accepted = models.BooleanField(default=False)
    views = models.IntegerField(default=0)
    content_modified_date = models.DateTimeField(null=True, blank=True)

    def get_absolute_url(self):
        return reverse("qa:show", kwargs={"id": self.id, 'slug': self.slug})

    def save(self, *args, **kwargs):
        self.slug = slugify(self.title, allow_unicode=True)
        super().save(*args, **kwargs)

    class Meta:
        ordering = ('-created',)


class QuestionHitCount(models.Model):
    question = models.ForeignKey(Question,
                                 on_delete=models.CASCADE,
                                 related_name='hitcount')
    created = models.DateTimeField(auto_now_add=True)
    fingerprint = models.TextField(max_length=256)

    def save(self, *args, **kwargs):
        hitcount = QuestionHitCount.objects.filter(
            question=self.question, fingerprint=self.fingerprint
        ).order_by('created')
        update_db = False
        if (hitcount):
            last_view = hitcount.last().created
            if ((timezone.now() - last_view).seconds % 60 > 15):
                update_db = True
        else:
            update_db = True
        if update_db:
            super().save(*args, **kwargs)
            qs = QuestionHitCount.objects.filter(question=self.question)
            self.question.views = qs.count()
            self.question.save()


class Answer(TimeStampModel):
    user = models.ForeignKey(settings.AUTH_USER_MODEL,
                             on_delete=models.CASCADE,
                             related_name='answers')
    question = models.ForeignKey(Question,
                                 on_delete=models.CASCADE)
    body_md = models.TextField()
    body_html = models.TextField()
    vote = models.IntegerField(default=0)
    accepted = models.BooleanField(default=False)
    accepted_date = models.DateTimeField(blank=True, null=True)

    class Meta:
        ordering = ('-accepted', '-vote',)


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

    class Meta:
        unique_together = ['user', 'answer']

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        qs = AnswerVote.objects.filter(answer=self.answer)
        self.answer.vote = qs.aggregate(Sum('rate'))['rate__sum']
        self.answer.save()
