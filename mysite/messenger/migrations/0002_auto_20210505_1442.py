# Generated by Django 3.2 on 2021-05-05 12:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('messenger', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='profile',
            name='firends',
        ),
        migrations.AddField(
            model_name='profile',
            name='firends',
            field=models.JSONField(null=True),
        ),
    ]
