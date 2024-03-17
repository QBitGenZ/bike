from rest_framework import serializers
from bicycle.models import *
from feedback.serializers import BicycleFeedbackSerializer, BicycleTypeFeedbackSerializer
from resource.serializers import BicycleImageSerializer


class BicycleTypeSerializer(serializers.ModelSerializer):
    bicycle_type_feedbacks = BicycleTypeFeedbackSerializer(read_only=True, many=True)

    class Meta:
        model = BicycleType
        fields = ['id', 'name', 'description', 'image', 'bicycle_type_feedbacks']

        extra_kwargs = {
            'id': {'read_only': True}
        }


class BicycleSerializer(serializers.ModelSerializer):
    bicycle_images = BicycleImageSerializer(read_only=True, many=True)
    bicycle_feedbacks = BicycleFeedbackSerializer(read_only=True, many=True)

    class Meta:
        model = Bicycle
        fields = ['id', 'type', 'price', 'bicycle_images', 'bicycle_feedbacks']

        extra_kwargs = {
            'id': {'read_only': True},
            'bicycle_images': {'read_only': True}
        }

        required_fields = ['type', 'price']
