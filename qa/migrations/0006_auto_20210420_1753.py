# Generated by Django 3.1.7 on 2021-04-20 13:23

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('qa', '0005_auto_20210414_1529'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='question',
            options={'ordering': ('-created',)},
        ),
    ]
