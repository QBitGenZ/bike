import uuid

from django.db import models

from bicycle.models import Bicycle, BicycleType
from event.models import Event
from user_management.models import User


# Create your models here.
class Feedback(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False, auto_created=True)
    title = models.CharField(max_length=255)
    text = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='feedback_user',
                             to_field='username')

    bicycle = models.ForeignKey(Bicycle, on_delete=models.CASCADE, null=True, blank=True,
                                related_name='bicycle_feedbacks')
    bicycle_type = models.ForeignKey(BicycleType, on_delete=models.CASCADE, null=True, blank=True,
                                     related_name='bicycle_type_feedbacks')

    event = models.ForeignKey(Event, on_delete=models.CASCADE, null=True, blank=True,
                              related_name='event_feedbacks')

    def __str__(self):
        return self.title
