from django.db import models

from user.models import CustomUser

# Create your models here.


class Category(models.Model):
    name = models.CharField(blank=False, max_length=100)
    max_field = models.IntegerField(blank=False)

    def __str__(self):
        return self.name


def get_profile_image_filepath(self, filename):
    return f'field/images/{self.pk}/{"profile_image.png"}'


def get_default_profile_image():
    return "codingwithmitch/no-pp.png"


class Field(models.Model):
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    name = models.CharField(blank=False, max_length=100)
    total_vote = models.IntegerField(blank=False, default=0)
    image = models.ImageField(
        max_length=100,
        upload_to=get_profile_image_filepath,
        null=True, blank=True,
        default=get_default_profile_image)

    def __str__(self):
        return self.name


class VotedField(models.Model):
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    voted_time = models.DateTimeField(auto_now=True)

    def __str__(self):
        return str(self.category)
