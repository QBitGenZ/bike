from django.urls import path
from .views import usage_statistics,CountView

urlpatterns = [
    path('usage-statistics/', usage_statistics, name='usage_statistics'),
    path('count/', CountView.as_view(), name='user-count')
]
