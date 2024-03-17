from rest_framework import serializers

from customer_finance.models import AccountBalance, PaymentHistory
from user_management.models import User


class PaymentHistorySerializer(serializers.ModelSerializer):
    class Meta:
        model = PaymentHistory
        fields = '__all__'


class AccountBalanceSerializer(serializers.ModelSerializer):
    user = serializers.SlugRelatedField(slug_field='username', queryset=User.objects.all())
    payment_history = PaymentHistorySerializer(many=True, read_only=True)

    class Meta:
        model = AccountBalance
        fields = '__all__'
