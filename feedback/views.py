from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from feedback.serializers import *


# Create your views here.
class BicycleFeedbackView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        data = request.data.copy()
        data['user'] = request.user.username

        serializer = BicycleFeedbackSerializer(data=data)
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

    def put(self, request, pk, *args, **kwargs):
        data = request.data.copy()
        data['user'] = request.user.username

        try:
            instance = Feedback.objects.get(pk=pk, user=request.user)
        except Feedback.DoesNotExist:
            return Response(
                {'error': 'Không có giá trị thỏa mãn'},
                status=status.HTTP_404_NOT_FOUND
            )

        serializer = BicycleFeedbackSerializer(instance=instance, data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(
                {'data': serializer.data},
                status=status.HTTP_201_CREATED
            )
        else:
            return Response(
                {'error': serializer.errors},
                status=status.HTTP_400_BAD_REQUEST
            )

    def delete(self, request, pk, *args, **kwargs):
        try:
            instance = Feedback.objects.get(pk=pk, user=request.user)
        except Feedback.DoesNotExist:
            return Response(
                {'error': 'Không có giá trị thỏa mãn'},
                status=status.HTTP_404_NOT_FOUND
            )
        instance.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

class BicycleTypeFeedbackView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        data = request.data.copy()
        data['user'] = request.user.username

        serializer = BicycleTypeFeedbackSerializer(data=data)
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

    def put(self, request, pk, *args, **kwargs):
        data = request.data.copy()
        data['user'] = request.user.username

        try:
            instance = Feedback.objects.get(pk=pk, user=request.user)
        except Feedback.DoesNotExist:
            return Response(
                {'error': 'Không có giá trị thỏa mãn'},
                status=status.HTTP_404_NOT_FOUND
            )

        serializer = BicycleTypeFeedbackSerializer(instance=instance, data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(
                {'data': serializer.data},
                status=status.HTTP_201_CREATED
            )
        else:
            return Response(
                {'error': serializer.errors},
                status=status.HTTP_400_BAD_REQUEST
            )

    def delete(self, request, pk, *args, **kwargs):
        try:
            instance = Feedback.objects.get(pk=pk, user=request.user)
        except Feedback.DoesNotExist:
            return Response(
                {'error': 'Không có giá trị thỏa mãn'},
                status=status.HTTP_404_NOT_FOUND
            )
        instance.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class EventFeedbackView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        data = request.data.copy()
        data['user'] = request.user.username

        serializer = EventFeedbackSerializer(data=data)
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

    def put(self, request, pk, *args, **kwargs):
        data = request.data.copy()
        data['user'] = request.user.username

        try:
            instance = Feedback.objects.get(pk=pk, user=request.user)
        except Feedback.DoesNotExist:
            return Response(
                {'error': 'Không có giá trị thỏa mãn'},
                status=status.HTTP_404_NOT_FOUND
            )

        serializer = EventFeedbackSerializer(instance=instance, data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(
                {'data': serializer.data},
                status=status.HTTP_201_CREATED
            )
        else:
            return Response(
                {'error': serializer.errors},
                status=status.HTTP_400_BAD_REQUEST
            )

    def delete(self, request, pk, *args, **kwargs):
        try:
            instance = Feedback.objects.get(pk=pk, user=request.user)
        except Feedback.DoesNotExist:
            return Response(
                {'error': 'Không có giá trị thỏa mãn'},
                status=status.HTTP_404_NOT_FOUND
            )
        instance.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

