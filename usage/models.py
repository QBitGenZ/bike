import uuid

from django.db import models

from bicycle.models import Bicycle
from user_management.models import User


# Create your models here.
class UsingHistory(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, auto_created=True, editable=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True, to_field='username')
    bicycle = models.ForeignKey(Bicycle, on_delete=models.CASCADE)
    start_at = models.DateTimeField()
    end_at = models.DateTimeField()
    distance = models.FloatField()

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['user', 'start_at', 'bicycle'], name='unique_using_history')
        ]

    def __str__(self):
        return str(self.user)


