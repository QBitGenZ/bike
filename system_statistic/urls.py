from django.urls import path
from .views import UsageStatisticsAPIView,CountView, RevenueStatisticsAPIView

urlpatterns = [
    path('usage-statistics/', UsageStatisticsAPIView.as_view(), name='usage_statistics'),
    path('count/', CountView.as_view(), name='user-count'),
    path('revenue/', RevenueStatisticsAPIView.as_view(), name='user-revenue'),
]
