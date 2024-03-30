from django.urls import path
from .views import TransactionView, TransactionPkView

urlpatterns = [
    path('', TransactionView.as_view(), name='transaction'),
    path('<uuid:pk>/', TransactionPkView.as_view(), name='transaction'),
]