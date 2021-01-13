from django.db import models
from django.conf import settings



class Prediction(models.Model):
    url = models.CharField(max_length=200)
    date = models.DateField()
    label = models.CharField(max_length=300)
    #prediction = models.FileField()

    def __str__(self):
        return self.label


