from django.db.models import Count
from django.db.models.functions import TruncMonth, TruncYear
from django.http import JsonResponse
from django.views.decorators.http import require_GET
from rest_framework.response import Response
from rest_framework.views import APIView

from bicycle.models import Bicycle
from event.models import Event
from usage.models import UsingHistory
from django.db import models

from user_management.models import User


@require_GET
def usage_statistics(request):
    period = request.GET.get('period', 'month')
    start_date = request.GET.get('start_date')
    end_date = request.GET.get('end_date')

    try:
        usage_data = count_usage_by_period(period, start_date, end_date)
        return JsonResponse({'data': usage_data}, status=200)
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=400)


def count_usage_by_period(period='month', start_date=None, end_date=None):
    # Xác định trường trunc và format dựa trên period được chọn
    if period == 'month':
        trunc_field = 'start_at'
        trunc_type = TruncMonth
        date_format = '%Y-%m'
    elif period == 'year':
        trunc_field = 'start_at'
        trunc_type = TruncYear
        date_format = '%Y'
    else:
        trunc_field = 'start_at'
        trunc_type = None
        date_format = '%Y-%m-%d'

    # Xây dựng queryset
    queryset = UsingHistory.objects.all()
    if start_date:
        queryset = queryset.filter(start_at__gte=start_date)
    if end_date:
        queryset = queryset.filter(start_at__lte=end_date)

    # Thêm annotations để nhóm theo period và đếm số lượng
    if trunc_type:
        queryset = queryset.annotate(period=trunc_type(trunc_field)).values('period').annotate(count=Count('id'))
    else:
        queryset = queryset.annotate(
            period_date=models.DateTimeField().extra(select={'period_date': trunc_field})).values(
            'period_date').annotate(count=Count('id'))

    # Format dữ liệu thống kê
    usage_data = [(entry['period'].strftime(date_format), entry['count']) for entry in queryset]

    return usage_data


class CountView(APIView):
    def get(self, request):
        user_count = User.objects.count()
        event_count = Event.objects.count()
        bicycle_count = Bicycle.objects.count()

        # Trả về kết quả
        return Response(
            {'data':
                 {'user': user_count, 'event': event_count, 'bicycle': bicycle_count}
             }
            , status=200)
