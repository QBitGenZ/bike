from django.core.paginator import Paginator, PageNotAnInteger
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from usage.models import UsingHistory
from usage.serializers import UsingHistorySerializer


# Create your views here.
class UsingHistoryView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, *args, **kwargs):
        limit = request.query_params.get('limit', 10)
        page = request.query_params.get('page', 1)

        history = UsingHistory.objects.all().order_by('start_at')
        paginator = Paginator(history, limit)

        try:
            history_page = paginator.page(page)
        except PageNotAnInteger:
            history_page = paginator.page(paginator.num_pages)

        serializer = UsingHistorySerializer(history_page, many=True)
        return Response({'data': serializer.data}, status=status.HTTP_200_OK)

    def post(self, request, *args, **kwargs):
        data = request.data.copy()
        data['user'] = request.user.username

        serializer = UsingHistorySerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response({'data': serializer.data}, status=status.HTTP_201_CREATED)
        else:
            return Response({'error':serializer.errors}, status=status.HTTP_400_BAD_REQUEST)


class UsingHistoryPkView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, username, *args, **kwargs):
        limit = request.query_params.get('limit', 10)
        page = request.query_params.get('page', 1)

        history = UsingHistory.objects.filter(user=username).order_by('start_at')
        paginator = Paginator(history, limit)

        try:
            history_page = paginator.page(page)
        except PageNotAnInteger:
            history_page = paginator.page(paginator.num_pages)

        serializer = UsingHistorySerializer(history_page, many=True)
        return Response({'data': serializer.data}, status=status.HTTP_200_OK)
