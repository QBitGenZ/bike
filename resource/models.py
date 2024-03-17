import uuid

from django.db import models

from bicycle.models import Bicycle
from event.models import Event
from feedback.models import Feedback


# Create your models here.
class Image(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False, auto_created=True)
    image = models.ImageField(upload_to='uploads/%Y/%m/')
    alt = models.CharField(max_length=255)

    bicycle = models.ForeignKey(Bicycle, on_delete=models.CASCADE, null=True, blank=True,
                                related_name='bicycle_images')

    feedback = models.ForeignKey(Feedback, on_delete=models.CASCADE, null=True, blank=True,
                                 related_name='feedback_images')

    event = models.ForeignKey(Event, on_delete=models.CASCADE, null=True, blank=True,
                              related_name='event_images')

    def __str__(self):
        return self.alt

