from django.core.paginator import Paginator, PageNotAnInteger
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from event.serializers import *


# Create your views here.
class EventView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, *args, **kwargs):
        page = request.query_params.get('page', 1)
        limit = request.query_params.get('limit', 10)

        events = Event.objects.all().order_by('name')
        bicycle_limit = Paginator(events, limit)

        try:
            page_events = bicycle_limit.page(page)
        except PageNotAnInteger:
            page_events = bicycle_limit.page(bicycle_limit.num_pages)

        serializer = EventSerializer(page_events, many=True)

        return Response(
            {'data': serializer.data},
            status=status.HTTP_200_OK
        )

    def post(self, request, *args, **kwargs):
        if not request.user.is_superuser:
            return Response(
                {'error': 'Bạn không có quyền thực hiện hành động này'},
                status=status.HTTP_403_FORBIDDEN
            )

        data = request.data.copy()
        serializer = EventSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(
                {'data': serializer.data},
                status=status.HTTP_201_CREATED
            )
        else:
            return Response(
                {'data': serializer.errors},
                status=status.HTTP_400_BAD_REQUEST
            )

class EventPkView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, pk, *args, **kwargs):
        event = Event.objects.get(pk=pk)
        serializer = EventSerializer(event)
        return Response(
            {'data': serializer.data},
            status=status.HTTP_200_OK
        )

    def put(self, request, pk, *args, **kwargs):
        if not request.user.is_superuser:
            return Response(
                {'error': 'Bạn không có quyền thực hiện hành động này'},
                status=status.HTTP_403_FORBIDDEN
            )

        data = request.data.copy()
        try:
            event = Event.objects.get(pk=pk)
        except Event.DoesNotExist:
            return Response(
                {'error': 'Không có giá trị thỏa mãn'},
                status=status.HTTP_404_NOT_FOUND
            )

        serializer = EventSerializer(instance=event, data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(
                {'data': serializer.data},
                status=status.HTTP_200_OK
            )
        else:
            return Response(
                {'error': serializer.errors},
                status=status.HTTP_400_BAD_REQUEST
            )

    def delete(self, request, pk, *args, **kwargs):
        if not request.user.is_superuser:
            return Response(
                {'error': 'Bạn không có quyền thực hiện hành động này'},
                status=status.HTTP_403_FORBIDDEN
            )

        try:
            event = Event.objects.get(pk=pk)
        except Event.DoesNotExist:
            return Response(
                {'error': 'Không có giá trị thỏa mãn'},
                status=status.HTTP_404_NOT_FOUND
            )

        event.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
