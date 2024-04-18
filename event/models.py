import uuid

from django.db import models
from user_management.models import User


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
    
class EventParticipation(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, to_field='username')
    event = models.ForeignKey(Event, on_delete=models.CASCADE)
    joined_at = models.DateTimeField(auto_now_add=True)
    note = models.TextField(blank=True)

    class Meta:
        unique_together = ['user', 'event']  # Mỗi user chỉ được tham gia sự kiện này một lần

    def __str__(self):
        return f"{self.user.username} - {self.event.name}"