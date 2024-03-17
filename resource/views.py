from django.shortcuts import render
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from resource.models import Image
from resource.serializers import BicycleImageSerializer, EventImageSerializer, FeedbackImageSerializer


# Create your views here.
class BicycleImageView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        data = request.data.copy()

        serializer = BicycleImageSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(
                {'data': serializer.data},
                status= status.HTTP_201_CREATED
            )
        else:
            return Response(
                {'error': serializer.errors},
                status=status.HTTP_400_BAD_REQUEST
            )

    def delete(self, request, pk, *args, **kwargs):
        try:
            instance = Image.objects.get(pk=pk)
        except Image.DoesNotExist:
            return Response(
                {'error': 'Không có giá trị thỏa mãn'},
                status=status.HTTP_404_NOT_FOUND
            )
        instance.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

class EventImageView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        data = request.data.copy()

        serializer = EventImageSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(
                {'data': serializer.data},
                status= status.HTTP_201_CREATED
            )
        else:
            return Response(
                {'error': serializer.errors},
                status=status.HTTP_400_BAD_REQUEST
            )


    def delete(self, request, pk, *args, **kwargs):
        try:
            instance = Image.objects.get(pk=pk)
        except Image.DoesNotExist:
            return Response(
                {'error': 'Không có giá trị thỏa mãn'},
                status=status.HTTP_404_NOT_FOUND
            )
        instance.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

class FeedbackImageView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        data = request.data.copy()

        serializer = FeedbackImageSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(
                {'data': serializer.data},
                status= status.HTTP_201_CREATED
            )
        else:
            return Response(
                {'error': serializer.errors},
                status=status.HTTP_400_BAD_REQUEST
            )


    def delete(self, request, pk, *args, **kwargs):
        try:
            instance = Image.objects.get(pk=pk)
        except Image.DoesNotExist:
            return Response(
                {'error': 'Không có giá trị thỏa mãn'},
                status=status.HTTP_404_NOT_FOUND
            )
        instance.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)