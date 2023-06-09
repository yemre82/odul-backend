# Generated by Django 4.0.2 on 2022-03-06 12:47

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import questionnaire.models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('max_field', models.IntegerField(default=1)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('started_at', models.DateTimeField()),
                ('ended_at', models.DateTimeField()),
            ],
        ),
        migrations.CreateModel(
            name='VotedField',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('voted_time', models.DateTimeField(auto_now=True)),
                ('is_voted', models.BooleanField(default=False)),
                ('category', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='questionnaire.category')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Field',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('total_vote', models.IntegerField(default=0)),
                ('image', models.ImageField(blank=True, default=questionnaire.models.get_default_profile_image, null=True, upload_to=questionnaire.models.get_profile_image_filepath)),
                ('category', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='questionnaire.category')),
            ],
        ),
    ]
