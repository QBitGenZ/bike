from rest_framework import serializers
from feedback.models import *
from resource.serializers import FeedbackImageSerializer


class BicycleFeedbackSerializer(serializers.ModelSerializer):
    feedback_images = FeedbackImageSerializer(many=True, read_only=True)

    class Meta:
        model = Feedback
        fields = ['id', 'title', 'text', 'created_at', 'user', 'bicycle', 'feedback_images']

        extra_kwargs = {
            'id': {'read_only': True},
            'bicycle': {'required': True},
        }

        required_fields = ['title', 'text', 'bicycle','user']


class BicycleTypeFeedbackSerializer(serializers.ModelSerializer):
    feedback_images = FeedbackImageSerializer(many=True, read_only=True)

    class Meta:
        model = Feedback
        fields = ['id', 'title', 'text', 'created_at','user', 'bicycle_type', 'feedback_images']

        extra_kwargs = {
            'id': {'read_only': True},
            'bicycle_type': {'required': True},
        }

        required_fields = ['title', 'text', 'bicycle_type', 'user']


class EventFeedbackSerializer(serializers.ModelSerializer):
    feedback_images = FeedbackImageSerializer(many=True, read_only=True)

    class Meta:
        model = Feedback
        fields = ['id', 'title', 'text', 'created_at', 'user', 'event', 'feedback_images']

        extra_kwargs = {
            'id': {'read_only': True},
            'event': {'required': True}
        }

        required_fields = ['title', 'text', 'event', 'user']
