# Generated by Django 3.1.12 on 2021-07-16 12:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('qa', '0015_auto_20210716_1443'),
    ]

    operations = [
        migrations.AlterField(
            model_name='comment',
            name='vote',
            field=models.SmallIntegerField(default=0),
        ),
    ]