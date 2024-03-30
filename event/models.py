import uuid

from django.db import models


# Create your models here.
class Event(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False, auto_created=True)
    name = models.CharField(max_length=255)
    text = models.TextField()
    poster = models.ImageField(upload_to='uploads/%Y/%m/%d/', null=True, blank=True)
    address = models.CharField(max_length=500)
    begin_at = models.DateTimeField()
    end_at = models.DateTimeField()
    created_at = models.DateTimeField(auto_now_add=True)
