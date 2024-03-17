from datetime import datetime
from rest_framework import serializers

from usage.models import UsingHistory


class UsingHistorySerializer(serializers.ModelSerializer):
    class Meta:
        model = UsingHistory
        fields = ['id', 'start_at', 'end_at', 'distance', 'user', 'bicycle']

        extra_kwargs = {
            'id': {'read_only': True}
        }