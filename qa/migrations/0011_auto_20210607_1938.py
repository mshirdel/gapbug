# Generated by Django 3.1.8 on 2021-06-07 15:08

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ("qa", "0010_question_accepted"),
    ]

    operations = [
        migrations.AlterModelOptions(
            name="answer",
            options={"ordering": ("-accepted", "-vote")},
        ),
        migrations.CreateModel(
            name="QuestionHitCount",
            fields=[
                (
                    "id",
                    models.AutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("created", models.DateTimeField(auto_now_add=True)),
                ("fingerprint", models.TextField(max_length=256)),
                (
                    "question",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="hitcount",
                        to="qa.question",
                    ),
                ),
            ],
        ),
    ]
