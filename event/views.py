from django.utils import timezone
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
        limit = request.query_params.get('limit', 10)
        page = request.query_params.get('page', 1)
        event_status = request.query_params.get('status', 'all')
        limit = int(limit)
        page = int(page)

        objects = Event.objects.all().order_by('name')
        
        now = timezone.now()

        if event_status == 'happening':
            objects = objects.filter(begin_at__lte=now, end_at__gte=now)
        elif event_status == 'upcoming':
            objects = objects.filter(begin_at__gt=now)
        elif event_status == 'past':
            objects = objects.filter(end_at__lt=now)
        
        total_pages = len(objects) // limit + (1 if len(objects) % limit > 0 else 0)
        current_page_objects = objects[(page - 1) * limit:page * limit]

        serializer = EventSerializer(current_page_objects, many=True)
        return Response({
            'data': serializer.data,
            'meta': {
                'total_pages': total_pages,
                'current_page': page,
                'limit': limit,
                'total': objects.count()
            }
        }, status=status.HTTP_200_OK)

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
    
class EventParticipationView(APIView):
    permission_classes = [IsAuthenticated]
    
    def get(self, request, event_id):
        limit = request.query_params.get('limit', 10)
        page = request.query_params.get('page', 1)
        limit = int(limit)
        page = int(page)

        objects = EventParticipation.objects.filter(user=request.user).select_related('event').order_by('event')
        total_pages = len(objects) // limit + (1 if len(objects) % limit > 0 else 0)
        current_page_objects = objects[(page - 1) * limit:page * limit]
        serializer = EventParticipationSerializer(current_page_objects, many=True)
        
        return Response({
            'data': serializer.data,
            'meta': {
                'total_pages': total_pages,
                'current_page': page,
                'limit': limit,
                'total': objects.count()
            }
        }, status=status.HTTP_200_OK)

    def post(self, request, event_id):
        try:
            event = Event.objects.get(pk=event_id)
        except Event.DoesNotExist:
            return Response(
                {'error': 'Sự kiện không tồn tại'},
                status=status.HTTP_404_NOT_FOUND
            )

        
        data = {'event': event.id, 'user': request.user.username}
        serializer = EventParticipationJoinSerializer(data=data)

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

    def delete(self, request, event_id):
        try:
            event = Event.objects.get(pk=event_id)
            participation = EventParticipation.objects.get(event=event, user=request.user)
        except (Event.DoesNotExist, EventParticipation.DoesNotExist):
            return Response(
                {'error': 'Không thể hủy tham gia sự kiện'},
                status=status.HTTP_404_NOT_FOUND
            )

        participation.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
