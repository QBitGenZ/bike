import uuid

from django.db import models


# Create your models here.
class Transaction(models.Model):
    id = models.UUIDField(primary_key=True, auto_created=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=255)
    address = models.CharField(max_length=500)

    def __str__(self):
        return self.name
