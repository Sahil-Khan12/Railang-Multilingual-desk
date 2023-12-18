from django.db import models
# Create your models here.

class Train(models.Model):
    Train_no = models.IntegerField(primary_key=True)
    Train_Name = models.CharField(max_length=150)
    Arival_time = models.CharField(max_length=50)
    Departure = models.CharField(max_length=100)
    Origin = models.CharField(max_length=100)
    Destination = models.CharField(max_length=100)
    Day = models.CharField(max_length=100)
    Delayed = models.BooleanField(default=False)

    def __str__(self):
        return self.Train_Name

class Logic1(models.Model):
    sno = models.AutoField(primary_key=True)
    quest = models.TextField()
    ans = models.TextField()