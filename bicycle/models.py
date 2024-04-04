import uuid

from django.db import models
from transaction_location.models import Transaction


# Create your models here.
class BicycleType(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False, auto_created=True)
    name = models.CharField(max_length=255)
    description = models.TextField()
    image = models.ImageField(upload_to='uploads/%Y/%m/')
    price = models.FloatField()

    def __str__(self):
        return self.name


class Bicycle(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False, auto_created=True)
    type = models.ForeignKey(BicycleType, on_delete=models.CASCADE, related_name='bicycles')
    status = models.CharField(max_length=255)
    location = models.ForeignKey(Transaction, on_delete=models.CASCADE, related_name='location')

    def __str__(self):
        return self.id
    
