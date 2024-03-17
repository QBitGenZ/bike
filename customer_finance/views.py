from django.core.paginator import Paginator, PageNotAnInteger
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from customer_finance.models import AccountBalance, PaymentHistory
from customer_finance.serializers import AccountBalanceSerializer, PaymentHistorySerializer
from user_management.models import User


# Create your views here.
class CustomerFinanceView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, *args, **kwargs):
        limit = request.query_params.get('limit', 10)
        page = request.query_params.get('page', 1)

        if not request.user.is_superuser:
            account = AccountBalance.objects.filter(user=request.user)
            serializer = AccountBalanceSerializer(account, many=True)
            return Response({'data': serializer.data}, status=status.HTTP_200_OK)
        else:
            account_balances = AccountBalance.objects.all().order_by('user')

            paginator = Paginator(account_balances, limit)

            try:
                account_balances_page = paginator.page(page)
            except PageNotAnInteger:
                account_balances_page = paginator.page(paginator.num_pages)

            serializer = AccountBalanceSerializer(account_balances_page, many=True)
            return Response({'data': serializer.data}, status=status.HTTP_200_OK)

    def post(self, request, *args, **kwargs):
        user = request.user.username
        data = request.data.copy()
        data['user'] = user

        serializer = AccountBalanceSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response({'data': serializer.data}, status=status.HTTP_201_CREATED)
        return Response({'error': serializer.errors}, status=status.HTTP_400_BAD_REQUEST)


class CustomerFinancePkView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, username, *args, **kwargs):
        if not request.user.is_superuser:
            return Response(
                {'error': 'Không có quyền thực hiện hành động này'},
                status=status.HTTP_403_FORBIDDEN
            )
        try:
            user = User.objects.get(username=username)
        except User.DoesNotExist:
            return Response(
                {'error': 'Không có dữ liệu thỏa mãn'},
                status=status.HTTP_404_NOT_FOUND
            )

        account = AccountBalance.objects.get(user=user)
        serializer = AccountBalanceSerializer(account, many=False)
        return Response(serializer.data, status=status.HTTP_200_OK)


class PaymentHistoryView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, *args, **kwargs):
        limit = request.query_params.get('limit', 10)
        page = request.query_params.get('page', 1)

        if request.user.is_superuser:
            history = PaymentHistory.objects.all()

            paginator = Paginator(history, limit)

            try:
                history_page = paginator.page(page)
            except PageNotAnInteger:
                history_page = paginator.page(paginator.num_pages)

            serializer = PaymentHistorySerializer(history_page, many=True)
            return Response({'data': serializer.data}, status=status.HTTP_200_OK)
        else:
            try:
                account = AccountBalance.objects.get(user=request.user)
            except AccountBalance.DoesNotExist:
                return Response({'error': 'Không có dữ liệu thỏa mãn'}, status=status.HTTP_404_NOT_FOUND)
            try:
                history = PaymentHistory.objects.filter(account=account)
            except PaymentHistory.DoesNotExist:
                return Response({'error': 'Không có dữ liệu thỏa mãn'}, status=status.HTTP_404_NOT_FOUND)

            paginator = Paginator(history, limit)

            try:
                history_page = paginator.page(page)
            except PageNotAnInteger:
                history_page = paginator.page(paginator.num_pages)

            serializer = PaymentHistorySerializer(history_page, many=True)
            return Response({'data': serializer.data}, status=status.HTTP_200_OK)




class PaymentHistoryPkView(APIView):
    permission_classes = [IsAuthenticated]
    def post(self, request, *args, **kwargs):
        try:
            account = AccountBalance.objects.get(user=request.user)
        except AccountBalance.DoesNotExist:
            return Response({'error': 'Không có dữ liệu thỏa mãn'}, status=status.HTTP_404_NOT_FOUND)

        data = request.data.copy()
        data['account'] = account.id
        serializer = PaymentHistorySerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response({'data':serializer.data}, status=status.HTTP_200_OK)
        else:
            return Response({'error':serializer.errors}, status=status.HTTP_400_BAD_REQUEST)

    def get(self, request, username, *args, **kwargs):
        limit = request.query_params.get('limit', 10)
        page = request.query_params.get('page', 1)

        if not request.user.is_superuser:
            return Response(
                {'error': 'Không có quyền thực hiện hành động này'},
                status=status.HTTP_403_FORBIDDEN
            )

        try:
            user = User.objects.get(username=username)
        except User.DoesNotExist:
            return Response({'error': 'Không có dữ liệu thỏa mãn'}, status=status.HTTP_404_NOT_FOUND)
        try:
            account = AccountBalance.objects.get(user=user)
        except AccountBalance.DoesNotExist:
            return Response({'error': 'Không có dữ liệu thỏa mãn'}, status=status.HTTP_404_NOT_FOUND)
        try:
            history = PaymentHistory.objects.filter(account=account).order_by('create_at')
        except PaymentHistory.DoesNotExist:
            return Response({'error': 'Không có dữ liệu thỏa mãn'}, status=status.HTTP_404_NOT_FOUND)

        paginator = Paginator(history, limit)

        try:
            history_page = paginator.page(page)
        except PageNotAnInteger:
            history_page = paginator.page(paginator.num_pages)

        serializer = PaymentHistorySerializer(history_page, many=True)
        return Response({'data': serializer.data}, status=status.HTTP_200_OK)