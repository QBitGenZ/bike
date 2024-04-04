from django.urls import path
from .views import UserMessageView, UserMessagePkView,SelfMessageView

urlpatterns = [
    path('', UserMessageView.as_view(), name='message'),
    path('<str:username>/', UserMessagePkView.as_view(), name=''),
    path('self/', SelfMessageView.as_view(), name='my-message')
]