from rest_framework import serializers

from resource.models import Image


class BicycleImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Image
        fields = ['id', 'image', 'alt', 'bicycle']

        extra_kwargs = {
            'id': {'read_only': True},
            'bicycle': {'required': True},
        }


class FeedbackImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Image
        fields = ['id', 'image', 'alt', 'feedback']

        extra_kwargs = {
            'id': {'read_only': True},
            'feedback': {'required': True},
        }


class EventImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Image
        fields = ['id', 'image', 'alt', 'event']

        extra_kwargs = {
            'id': {'read_only': True},
            'event': {'required': True},
        }
