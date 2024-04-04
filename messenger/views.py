from django.db import models
from django.views import View
from rest_framework import status
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework.response import Response
from rest_framework.views import APIView

from messenger.models import Message
from messenger.serializers import MessageSerializer
from user_management.models import User


class UserMessageView(APIView):
    permission_classes = [IsAuthenticated, IsAdminUser]
    def get(self, request, format=None):
        # Lấy danh sách tất cả người dùng
        users = User.objects.all()

        # Tạo một danh sách để lưu kết quả
        user_messages = []


        for user in users:
            latest_message = Message.objects.filter(sender=user).order_by('-timestamp').first()


            user_message_info = {
                'user': user.username,  # hoặc bất kỳ trường nào khác của người dùng bạn muốn hiển thị
                'latest_message': MessageSerializer(latest_message).data if latest_message else None
            }

            user_messages.append(user_message_info)

        # Trả về danh sách người dùng kèm tin nhắn gần nhất của mỗi người dùng
        return Response({'data': user_messages}, status=status.HTTP_200_OK)

class UserMessagePkView(APIView):
    permission_classes = [IsAuthenticated, IsAdminUser]

    def get(self, request, username, *args, **kwargs):
        limit = request.query_params.get('limit', 10)
        page = request.query_params.get('page', 1)
        limit = int(limit)
        page = int(page)

        objects = Message.objects.filter(models.Q(sender=username) | models.Q(recipient=username)).filter(models.Q(sender=request.user.username) | models.Q(recipient=request.user.username)).order_by('-timestamp')
        total_pages = len(objects) // limit + (1 if len(objects) % limit > 0 else 0)
        current_page_objects = objects[(page - 1) * limit:page * limit]

        serializer = MessageSerializer(current_page_objects, many=True)
        return Response({
            'data': serializer.data,
            'meta': {
                'total_pages': total_pages,
                'current_page': page,
                'limit': limit,
                'total': objects.count()
            }
        }, status=status.HTTP_200_OK)

class SelfMessageView(APIView):
    permission_classes = [IsAuthenticated,]

    def get(self, request, *args, **kwargs):
        limit = request.query_params.get('limit', 10)
        page = request.query_params.get('page', 1)
        limit = int(limit)
        page = int(page)

        objects = Message.objects.filter(sender=request.user.username).order_by('-timestamp')
        total_pages = len(objects) // limit + (1 if len(objects) % limit > 0 else 0)
        current_page_objects = objects[(page - 1) * limit:page * limit]

        serializer = MessageSerializer(current_page_objects, many=True)
        return Response({
            'data': serializer.data,
            'meta': {
                'total_pages': total_pages,
                'current_page': page,
                'limit': limit,
                'total': objects.count()
            }
        }, status=status.HTTP_200_OK)