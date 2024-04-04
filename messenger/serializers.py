from rest_framework import serializers

from .models import Message


class MessageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Message
        fields = '__all__'

        extra_kwargs = {
            'id': {'read_only': True},
            'timestamp': {'read_only': True},
        }