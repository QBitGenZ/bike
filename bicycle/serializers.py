from rest_framework import serializers
from bicycle.models import *
from feedback.serializers import BicycleFeedbackSerializer, BicycleTypeFeedbackSerializer
from resource.serializers import BicycleImageSerializer
from transaction_location.serializers import TransactionSerializer


class BicycleTypeSerializer(serializers.ModelSerializer):
    bicycle_type_feedbacks = BicycleTypeFeedbackSerializer(read_only=True, many=True)

    class Meta:
        model = BicycleType
        fields = ['id', 'name', 'description', 'price', 'image', 'bicycle_type_feedbacks']

        extra_kwargs = {
            'id': {'read_only': True}
        }


class BicycleSerializer(serializers.ModelSerializer):
    bicycle_images = BicycleImageSerializer(read_only=True, many=True)
    bicycle_feedbacks = BicycleFeedbackSerializer(read_only=True, many=True)

    class Meta:
        model = Bicycle
        fields = ['id', 'type', 'bicycle_images', 'bicycle_feedbacks', 'status', 'location']

        extra_kwargs = {
            'id': {'read_only': True},
            'bicycle_images': {'read_only': True}
        }

class GetBicycleSerializer(serializers.ModelSerializer):
    type = serializers.CharField(source='type.name', read_only=True)
    location = serializers.CharField(source='location.name', read_only=True)

    class Meta:
        model = Bicycle
        fields = ['id', 'type', 'status', 'location']