from django.db import models
from helpers.models import TrackingModel
from django.db.models.deletion import CASCADE

class Vendor(TrackingModel):
    name = models.CharField(max_length=255)
    address = models.TextField()
    phone = models.CharField(max_length=20)
    email = models.EmailField(unique=True)

    def __str__(self):
        return self.name
