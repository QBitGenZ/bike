import uuid

from django.db import models
from django.db.models import OneToOneField, ForeignKey

from user_management.models import User


# Create your models here.
class AccountBalance(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, auto_created=True, editable=False)
    user = OneToOneField(User, on_delete=models.CASCADE, to_field="username")
    balance = models.FloatField()

    def __str__(self):
        return self.user.username


class PaymentHistory(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, auto_created=True, editable=False)
    account = ForeignKey(AccountBalance, on_delete=models.CASCADE, related_name="payment_history")
    create_at = models.DateTimeField(auto_now_add=True)
    money = models.FloatField()
    text = models.TextField()

    class Meta:
        unique_together = ('account', 'create_at')
