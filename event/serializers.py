from rest_framework import serializers

from event.models import Event, EventParticipation
from feedback.serializers import EventFeedbackSerializer
from resource.serializers import EventImageSerializer
from user_management.serializers import UserSerializer

class EventParticipationSerializer(serializers.ModelSerializer):
    user = UserSerializer()  

    class Meta:
        model = EventParticipation
        fields = ['user', 'joined_at', 'note']

class EventSerializer(serializers.ModelSerializer):
    event_images = EventImageSerializer(many=True, read_only=True)
    event_feedbacks = EventFeedbackSerializer(many=True, read_only=True)
    participations = EventParticipationSerializer(many=True, read_only=True)
    
    class Meta:
        model = Event
        fields = ['id', 'name', 'text', 'begin_at', 'end_at', 'event_images', 'event_feedbacks',
                  'created_at', 'address', 'poster', 'participations']

        extra_kwargs = {
            'id': {'read_only': True},
            'created_at': {'read_only':True}
        }