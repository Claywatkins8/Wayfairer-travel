from django.db import models

from django.contrib.auth.models import AbstractUser

# Create your models here.

class User(AbstractUser):
    join_date = models.DateField()
    current_city = models.CharField(max_length=100)
    # image = models.ImageField()


class City(models.Model):
    name = models.CharField(max_length:100)
    country = models.CharField(max_length:100)
    # image = models.ImageField()


