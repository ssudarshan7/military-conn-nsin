from django.db import models
from django.contrib.auth.models import User
# Create your models here.

class Category(models.Model):
    categoryName = models.CharField(max_length=100)

class CustomUser(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    address = models.CharField(max_length=100)
    university = models.CharField(max_length=100)
    regiment = models.CharField(max_length=40)

    


class Events(models.Model):
   eventID = models.IntegerField(primary_key = True)    
   eventname = models.CharField(max_length = 200)
   eventcity = models.CharField(max_length=50)





