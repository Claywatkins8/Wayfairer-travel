from django.db import models

from django.contrib.auth.models import User

# Create your models here.

class Profile(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    current_city = models.CharField(max_length=100)
    # image = models.ImageField()


class City(models.Model):
    name = models.CharField(max_length=100)
    country = models.CharField(max_length=100)
    # image = models.ImageField()


class Post(models.Model):
    title = models.CharField(max_length=100)
    content = models.TextField(max_length=1500)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    city = models.ForeignKey(City, on_delete=models.CASCADE)