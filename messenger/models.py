from django.db import models

from user_management.models import User


class Message(models.Model):
    sender = models.ForeignKey(User, related_name='sent_messages', on_delete=models.CASCADE, to_field='username')
    recipient = models.ForeignKey(User, related_name='received_messages', on_delete=models.CASCADE, to_field='username')
    timestamp = models.DateTimeField(auto_now_add=True)
    content = models.TextField()
    def reply(self, user):
        self.replied_to = user
        self.save()
