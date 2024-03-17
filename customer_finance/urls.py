from django.urls import path

from customer_finance.views import CustomerFinanceView, PaymentHistoryView, PaymentHistoryPkView, CustomerFinancePkView

urlpatterns = [
    path('', CustomerFinanceView.as_view(), name='finance'),
    path('<str:username>/', CustomerFinancePkView.as_view(), name='finance'),
    path('history/', PaymentHistoryView.as_view(), name='finance_history'),
    path('history/<str:username>/', PaymentHistoryPkView.as_view(), name='finance_history'),
]