from django.db import models

# Create your models here.


class Prediction(models.Model):

    date_created = models.DateTimeField(auto_now_add=True, null=True)
