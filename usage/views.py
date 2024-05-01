from django.core.paginator import Paginator, PageNotAnInteger
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from django.utils import timezone

from usage.models import UsingHistory
from usage.serializers import UsingHistorySerializer
from bicycle.models import Bicycle, BicycleType
from bicycle.serializers import BicycleSerializer
from transaction_location.models import Transaction


# Create your views here.
class UsingHistoryView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, *args, **kwargs):
        limit = request.query_params.get('limit', 10)
        page = request.query_params.get('page', 1)
        limit = int(limit)
        page = int(page)

        objects = UsingHistory.objects.all().order_by('start_at')
        total_pages = len(objects) // limit + (1 if len(objects) % limit > 0 else 0)
        current_page_objects = objects[(page - 1) * limit:page * limit]

        serializer = UsingHistorySerializer(current_page_objects, many=True)
        return Response({
            'data': serializer.data,
            'meta': {
                'total_pages': total_pages,
                'current_page': page,
                'limit': limit,
                'total': objects.count()
            }
        }, status=status.HTTP_200_OK)

class UsingHistoryPkView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, username, *args, **kwargs):
        limit = request.query_params.get('limit', 10)
        page = request.query_params.get('page', 1)

        history = UsingHistory.objects.filter(user=username).order_by('start_at')
        paginator = Paginator(history, limit)

        try:
            history_page = paginator.page(page)
        except PageNotAnInteger:
            history_page = paginator.page(paginator.num_pages)

        serializer = UsingHistorySerializer(history_page, many=True)
        return Response({'data': serializer.data}, status=status.HTTP_200_OK)

class UsingView(APIView):
    permission_classes = [IsAuthenticated]
    
    def post(self, request, *args, **kwargs):
        data = request.data.copy()
        data['user'] = request.user.username
        data['start_at'] = timezone.now()
        
        previous_using = UsingHistory.objects.filter(user=request.user.username ,end_at__isnull=True, start_at__isnull=False)
        print(data['bicycle'])
        if previous_using:
            return Response({'error': 'Bạn phải trả xe trước'}, status=status.HTTP_406_NOT_ACCEPTABLE)
        else:
            serializer = UsingHistorySerializer(data=data)
            if serializer.is_valid():
                serializer.save()
                return Response({'data': serializer.data}, status=status.HTTP_201_CREATED)
            else:
                return Response({'error':serializer.errors}, status=status.HTTP_400_BAD_REQUEST)
    
    def put(self, request, *args, **kwargs):
        data = request.data.copy()
        data['user'] = request.user.username
        data['end_at'] = timezone.now()
        print(data['bicycle'])
        if not data.get('location'):
            return Response({'error': 'Vui lòng quét mã địa điểm giao dịch'}, status=status.HTTP_406_NOT_ACCEPTABLE)
        
        current_using = UsingHistory.objects.get(user=request.user.username ,end_at__isnull=True)
        
        if not current_using:
            return Response({'error': 'Bạn chưa mượn xe'}, status=status.HTTP_406_NOT_ACCEPTABLE)
        else:
            serializer = UsingHistorySerializer(instance=current_using[0], data=data, partial=True)
            try:
                bicycle = Bicycle.objects.get(pk=data['bicycle'])
            except Bicycle.DoesNotExist:
                return Response({'error': 'Không có giá trị thỏa mãn'}, status=status.HTTP_404_NOT_FOUND)
            try:
                transaction_location = Transaction.objects.get(pk=data['location'])
            except Transaction.DoesNotExist:
                return Response({'error': 'Không có giá trị thỏa mãn'}, status=status.HTTP_404_NOT_FOUND)
            
            price = 0.0

            try:
                type = BicycleType.objects.get(pk=bicycle.type)
                cost = (data['end_at'] - current_using.start_at).total_seconds()/3600 * type.price
            except BicycleType.DoesNotExist:
                print('Không có loại xe yêu cầu')
            
            
            bicycle_serializers = BicycleSerializer(instance=bicycle, data={'location': transaction_location.id}, partial=True)
            if bicycle_serializers.is_valid():
                bicycle_serializers.save()
            else:
                return Response({'error': bicycle_serializers.errors}, status=status.HTTP_400_BAD_REQUEST)
            
            if serializer.is_valid():
                serializer.save()
                return Response({'data': serializer.data, 'cost': cost}, status=status.HTTP_200_OK)
            else:
                return Response({'error':serializer.errors}, status=status.HTTP_400_BAD_REQUEST)
        
        
        
        
        