from django.urls import path

from usage.views import UsingHistoryPkView, UsingHistoryView, UsingView

urlpatterns = [
    path('use/', UsingView.as_view(), name='use'),
    path('user/<str:username>/', UsingHistoryPkView.as_view(), name='using-history'),
    path('all/', UsingHistoryView.as_view(), name='using-history'),
]