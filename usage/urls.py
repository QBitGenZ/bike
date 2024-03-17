from django.urls import path

from usage.views import UsingHistoryPkView, UsingHistoryView

urlpatterns = [
    path('<str:username>/', UsingHistoryPkView.as_view(), name='using-history'),
    path('', UsingHistoryView.as_view(), name='using-history'),
]