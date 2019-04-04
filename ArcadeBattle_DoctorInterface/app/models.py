from distutils.command import register

from django.contrib.auth.models import User, Group
from django.db import models

# Create your models here.

class Person(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    photo_b64 = models.TextField()
    contact = models.CharField(max_length=200)

    def __str__(self):
        return self.user.first_name + " " + self.user.last_name