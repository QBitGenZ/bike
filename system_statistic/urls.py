from django.urls import path
from .views import UsageStatisticsAPIView,CountView, RevenueStatisticsAPIView, WeeklyUsageAPIView, RevenueComparisonAPIView, TopUsedBicycleTypesAPIView

urlpatterns = [
    path('usage-statistics/', UsageStatisticsAPIView.as_view(), name='usage_statistics'),
    path('count/', CountView.as_view(), name='user-count'),
    path('revenue/', RevenueStatisticsAPIView.as_view(), name='user-revenue'),
    path('weeks/',WeeklyUsageAPIView.as_view(), name='weeks'),
    path('months/', RevenueComparisonAPIView.as_view(), name='months'),
    path('best-used/', TopUsedBicycleTypesAPIView.as_view(), name='top-used' )
]
