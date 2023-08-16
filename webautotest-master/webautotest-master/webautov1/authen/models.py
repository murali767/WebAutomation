from django.db import models

# Create your models here.
class command_db(models.Model):
    command=models.CharField(max_length=1000)
class current_db(models.Model):
    current=models.CharField(max_length=1000)
class main_db(models.Model):
    email=models.CharField(max_length=100)
    messages=models.CharField(max_length=100000,default='')
    current=models.CharField(max_length=1000)
    count=models.IntegerField(default=0)
