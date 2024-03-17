from rest_framework import serializers

from event.models import Event
from feedback.serializers import EventFeedbackSerializer
from resource.serializers import EventImageSerializer


class EventSerializer(serializers.ModelSerializer):
    event_images = EventImageSerializer(many=True, read_only=True)
    event_feedbacks = EventFeedbackSerializer(many=True, read_only=True)
    class Meta:
        model = Event
        fields = ['id', 'name', 'text', 'begin_at', 'end_at', 'event_images', 'event_feedbacks',
                  'created_at']

        extra_kwargs = {
            'id': {'read_only': True},
            'created_at': {'read_only':True}
        }

        required_fields = ['name', 'text', 'begin_at', 'end_at']