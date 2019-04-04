from distutils.command import register

from django.contrib.auth.models import User, Group
from django.db import models

# Create your models here.

class Person(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    photo_b64 = models.TextField()
    contact = models.CharField(max_length=200)
    nif =  models.IntegerField()
    birth_date = models.DateField()


    def __str__(self):
        return self.user.first_name + " " + self.user.last_name


class Gestures(models.Model):
    #gestureID é auto gerado
    '''
    VAI TER DE SER FOREIGN KEY

    --> pacientID = models.ForeignKey(Pacient, on_delete=models.CASCADE)

    '''
    pacientID = models.IntegerField()
    name = models.CharField(max_length=100)
    image = models.CharField(max_length=1024)
    repetitions = models.IntegerField()
    default_difficulty = models.IntegerField()
    decision_tree = models.CharField(max_length=1024)