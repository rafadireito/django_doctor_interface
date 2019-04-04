import uuid
from distutils.command import register

from django.contrib.auth.models import User, Group
from django.db import models


class Person(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    photo_b64 = models.TextField()
    contact = models.CharField(max_length=200)
    nif =  models.IntegerField()
    birth_date = models.DateField()

    def __str__(self):
        return self.user.first_name + " " + self.user.last_name


class Patient(models.Model):
    person = models.OneToOneField(Person, on_delete=models.CASCADE)
    notes = models.TextField()

    def __str__(self):
        return self.person.user.first_name + " " + self.person.user.last_name


class Game(models.Model):
    name = models.CharField(max_length=200)
    photo_b64 = models.TextField()
    preview_link = models.TextField()

    def __str__(self):
        return self.name



class Gesture(models.Model):
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    image = models.TextField()
    repetitions = models.IntegerField()
    default_difficulty = models.IntegerField()
    decision_tree = models.CharField(max_length=1024)