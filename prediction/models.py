from django.db import models
from django.conf import settings
from djongo.storage import GridFSStorage

grid_fs_storage = GridFSStorage(collection='skincodedb', base_url=''.join([settings.BASE_URL, 'skincodedb/']))


class Prediction(models.Model):
    date = models.DateField()
    label = models.CharField(max_length=300)
    prediction = models.ImageField(null=True, blank=True)

    def __str__(self):
        return self.label


