from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.utils import timezone
from datetime import timedelta
from django.db.models import Count
from django.db.models.functions import TruncMonth, ExtractWeekDay
from usage.models import UsingHistory
from user_management.models import User
from event.models import Event
from bicycle.models import Bicycle
from datetime import datetime, timedelta
from django.db.models import Count, Sum


class UsageStatisticsAPIView(APIView):
    def get(self, request):
        # Lấy ngày hiện tại
        current_date = timezone.now()

        # Lấy start_date và end_date từ query parameters
        start_date_str = request.query_params.get('start_date')
        end_date_str = request.query_params.get('end_date')

        # Nếu không có start_date và end_date được truyền vào, mặc định là 12 tháng gần nhất
        if not start_date_str and not end_date_str:
            start_date = current_date - timedelta(days=365)
            end_date = current_date
        else:
            # Chuyển đổi start_date và end_date từ string sang datetime
            try:
                start_date = datetime.strptime(start_date_str, '%Y-%m-%d')
                end_date = datetime.strptime(end_date_str, '%Y-%m-%d')

                # Kiểm tra nếu start_date lớn hơn end_date, hoán đổi lại
                if start_date > end_date:
                    start_date, end_date = end_date, start_date
            except ValueError:
                return Response({'message': 'Invalid date format. Please provide dates in YYYY-MM-DD format.'}, status=status.HTTP_400_BAD_REQUEST)

        # Thực hiện thống kê số lượng sử dụng cho các tháng
        usage_history = UsingHistory.objects.filter(start_at__range=(start_date, end_date)).annotate(
            month=TruncMonth('start_at')
        ).values('month').annotate(count=Count('id')).order_by('-month')

        # Tạo một dict để lưu trữ số lượng sử dụng theo tháng
        usage_dict = {item['month'].strftime('%Y-%m'): item['count'] for item in usage_history}

        # Tạo dữ liệu response với số lượng sử dụng mặc định là 0 cho các tháng không có dữ liệu
        data = [{'month': month.strftime('%Y-%m'), 'count': usage_dict.get(month.strftime('%Y-%m'), 0)} for month in self.get_months(start_date, end_date)]

        return Response({'data': data}, status=status.HTTP_200_OK)

    def get_months(self, start_date, end_date):
        months = []
        while start_date <= end_date:
            months.append(start_date)
            # Tăng tháng lên 1, nếu tháng hiện tại là 12 thì chuyển sang năm mới
            if start_date.month == 12:
                start_date = start_date.replace(day=1, month=1, year=start_date.year + 1)
            else:
                start_date = start_date.replace(day=1, month=start_date.month + 1)
        return months

class RevenueStatisticsAPIView(APIView):
    def get(self, request):
        # Lấy ngày hiện tại
        current_date = datetime.now()

        # Lấy start_date và end_date từ query parameters
        start_date_str = request.query_params.get('start_date')
        end_date_str = request.query_params.get('end_date')

        # Nếu không có start_date và end_date được truyền vào, mặc định là 12 tháng gần nhất
        if not start_date_str and not end_date_str:
            start_date = current_date - timedelta(days=365)
            end_date = current_date
        else:
            # Chuyển đổi start_date và end_date từ string sang datetime
            try:
                start_date = datetime.strptime(start_date_str, '%Y-%m-%d')
                end_date = datetime.strptime(end_date_str, '%Y-%m-%d')

                # Kiểm tra nếu start_date lớn hơn end_date, hoán đổi lại
                if start_date > end_date:
                    start_date, end_date = end_date, start_date
            except ValueError:
                return Response({'message': 'Invalid date format. Please provide dates in YYYY-MM-DD format.'}, status=status.HTTP_400_BAD_REQUEST)

        # Tạo danh sách các tháng cần thống kê
        months_to_check = [start_date.replace(day=1) + timedelta(days=31*i) for i in range((end_date - start_date).days // 31 + 1)]

        # Thực hiện thống kê doanh thu cho các tháng
        revenue_history = UsingHistory.objects.filter(start_at__range=(start_date, end_date)).annotate(
            month=TruncMonth('start_at')
        ).values('month').annotate(revenue=Sum('bicycle__type__price')).order_by('-month')

        # Tạo một dict để lưu trữ doanh thu theo tháng
        revenue_dict = {item['month'].strftime('%Y-%m'): item['revenue'] for item in revenue_history}

        # Tạo dữ liệu response với doanh thu mặc định là 0 cho các tháng không có dữ liệu
        data = [{'month': month.strftime('%Y-%m'), 'revenue': revenue_dict.get(month.strftime('%Y-%m'), 0)} for month in months_to_check]

        return Response({'data': data}, status=status.HTTP_200_OK)

class CountView(APIView):
    def get(self, request):
        user_count = User.objects.count()
        event_count = Event.objects.count()
        bicycle_count = Bicycle.objects.count()
        using_hitory = UsingHistory.objects.count()

        # Trả về kết quả
        return Response(
            {'data':
                 {'user': user_count, 'event': event_count, 'bicycle': bicycle_count, 'using': using_hitory},
             }
            , status=200)

class WeeklyUsageAPIView(APIView):
    def get(self, request):
        # Thực hiện thống kê số lượt sử dụng cho từng ngày trong tuần
        usage_history = UsingHistory.objects.annotate(
            week_day=ExtractWeekDay('start_at')
        ).values('week_day').annotate(count=Count('id')).order_by('week_day')

        # Tạo một dict để lưu trữ số lượt sử dụng theo ngày trong tuần
        usage_dict = {item['week_day']: item['count'] for item in usage_history}

        # Danh sách các ngày trong tuần từ thứ 2 đến chủ nhật
        days_of_week = ['Thứ hai', 'Thứ ba', 'Thứ tư', 'Thứ năm', 'Thứ sáu', 'Thứ bảy', 'Chủ nhật']

        # Tạo dữ liệu response với tên của ngày trong tuần thay vì số
        data = [{'day_of_week': days_of_week[day - 1], 'count': usage_dict.get(day, 0)} for day in range(1, 8)]

        return Response({'data': data}, status=status.HTTP_200_OK)
    
class RevenueComparisonAPIView(APIView):
    def get(self, request):
        # Lấy ngày hiện tại
        current_date = datetime.now()

        # Lấy tháng và năm của tháng đầu tiên của năm nay và năm trước
        current_year = current_date.year
        last_year = current_year - 1

        # Tính toán khoảng thời gian từ tháng đầu tiên của năm nay đến thời điểm hiện tại
        current_year_start = datetime(current_year, 1, 1)
        current_year_end = timezone.datetime(current_year, 12, 31)
        last_year_start = datetime(last_year, 1, 1)
        last_year_end = current_year_start - timedelta(days=1)  # Kết thúc tháng trước

        # Thực hiện thống kê doanh thu cho năm nay
        current_year_revenue = self.get_revenue_in_period(current_year_start, current_year_end)

        # Thực hiện thống kê doanh thu cho năm trước
        last_year_revenue = self.get_revenue_in_period(last_year_start, last_year_end)

        # Tạo dữ liệu response
        data = {
            'current_year': current_year_revenue,
            'last_year': last_year_revenue
        }

        return Response(data, status=status.HTTP_200_OK)

    def get_revenue_in_period(self, start_date, end_date):
        # Lấy danh sách các tháng từ start_date đến end_date
        months = self.get_months(start_date, end_date)

        # Lấy ngày hiện tại
        current_date = datetime.now()

        # Lấy tháng và năm của tháng hiện tại
        current_year = current_date.year
        current_month = current_date.month

        # Nếu end_date vượt qua tháng hiện tại của năm nay, cập nhật end_date thành tháng hiện tại
        if end_date.year == current_year and end_date.month > current_month:
            end_date = datetime(current_year, current_month, 1)

        # Thực hiện thống kê doanh thu trong khoảng thời gian cho trước
        revenue_history = UsingHistory.objects.filter(start_at__range=(start_date, end_date)).annotate(
            month=TruncMonth('start_at')
        ).values('month').annotate(revenue=Sum('bicycle__type__price')).order_by('month')

        # Tạo một dict để lưu trữ doanh thu theo tháng
        revenue_dict = {item['month'].strftime('%Y-%m'): item['revenue'] for item in revenue_history}

        # Tạo dữ liệu response với doanh thu mặc định là 0 cho các tháng không có dữ liệu
        data = [{'month': month.strftime('%Y-%m'), 'revenue': revenue_dict.get(month.strftime('%Y-%m'), 0)} for month in months]

        return data


    def get_months(self, start_date, end_date):
        months = []
        while start_date <= end_date:
            months.append(start_date)
            # Tăng tháng lên 1, nếu tháng hiện tại là 12 thì chuyển sang năm mới
            if start_date.month == 12:
                start_date = start_date.replace(day=1, month=1, year=start_date.year + 1)
            else:
                start_date = start_date.replace(day=1, month=start_date.month + 1)
        return months