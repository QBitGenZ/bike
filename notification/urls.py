from django.urls import path

from notification.views import NotificationView

urlpatterns = [
    path('', NotificationView.as_view(), name='notification'),
    path('<uuid:pk>/', NotificationView.as_view(), name='notification'),
]