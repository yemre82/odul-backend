# Generated by Django 4.0.2 on 2022-03-06 12:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('questionnaire', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='category',
            name='current_field',
            field=models.IntegerField(default=0),
        ),
    ]
