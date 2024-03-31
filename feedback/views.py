from django.core.paginator import Paginator, PageNotAnInteger
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from feedback.serializers import *

# Create your views here.
class BicycleFeedbackView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, *args, **kwargs):
        page = request.query_params.get('page', 1)
        limit = request.query_params.get('limit', 10)

        feedback = Feedback.objects.exclude(bicycle=None).order_by('created_at')
        feedback_limit = Paginator(feedback, limit)

        try:
            page_events = feedback_limit.page(page)
        except PageNotAnInteger:
            page_events = feedback_limit.page(feedback_limit.num_pages)

        serializer = BicycleFeedbackSerializer(page_events, many=True)

        return Response(
            {'data': serializer.data},
            status=status.HTTP_200_OK
        )

    def post(self, request, *args, **kwargs):
        data = request.data.copy()
        data['user'] = request.user.username

        serializer = BicycleFeedbackSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(
                {'data': serializer.data},
                status= status.HTTP_201_CREATED
            )
        else:
            return Response(
                {'error': serializer.errors},
                status=status.HTTP_400_BAD_REQUEST
            )



class BicycleFeedbackPkView(APIView):
    permission_classes = [IsAuthenticated]
    
    def get(self, request, pk, *args, **kwargs):
        try:
            feedback = Feedback.objects.get(pk=pk)
        except Feedback.DoesNotExist:
            return Response(
                {'error': 'Không có giá trị thỏa mãn'},
                status=status.HTTP_404_NOT_FOUND
            )
            

        serializer = BicycleFeedbackSerializer(instance=feedback, many=False)

        return Response(
            {'data': serializer.data},
            status=status.HTTP_200_OK
        )
    
    def put(self, request, pk, *args, **kwargs):
        data = request.data.copy()
        data['user'] = request.user.username

        try:
            instance = Feedback.objects.get(pk=pk, user=request.user)
        except Feedback.DoesNotExist:
            return Response(
                {'error': 'Không có giá trị thỏa mãn'},
                status=status.HTTP_404_NOT_FOUND
            )

        serializer = BicycleFeedbackSerializer(instance=instance, data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(
                {'data': serializer.data},
                status=status.HTTP_201_CREATED
            )
        else:
            return Response(
                {'error': serializer.errors},
                status=status.HTTP_400_BAD_REQUEST
            )

    def delete(self, request, pk, *args, **kwargs):
        try:
            instance = Feedback.objects.get(pk=pk, user=request.user)
        except Feedback.DoesNotExist:
            return Response(
                {'error': 'Không có giá trị thỏa mãn'},
                status=status.HTTP_404_NOT_FOUND
            )
        instance.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
    

class BicycleTypeFeedbackView(APIView):
    permission_classes = [IsAuthenticated]
    def get(self, request, *args, **kwargs):
        page = request.query_params.get('page', 1)
        limit = request.query_params.get('limit', 10)

        feedback = Feedback.objects.exclude(bicycle_type=None).order_by('created_at')
        feedback_limit = Paginator(feedback, limit)

        try:
            page_feedbacks = feedback_limit.page(page)
        except PageNotAnInteger:
            page_feedbacks = feedback_limit.page(feedback_limit.num_pages)

        serializer = BicycleTypeFeedbackSerializer(page_feedbacks, many=True)

        return Response(
            {'data': serializer.data},
            status=status.HTTP_200_OK
        )

    def post(self, request, *args, **kwargs):
        data = request.data.copy()
        data['user'] = request.user.username

        serializer = BicycleTypeFeedbackSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(
                {'data': serializer.data},
                status= status.HTTP_201_CREATED
            )
        else:
            return Response(
                {'error': serializer.errors},
                status=status.HTTP_400_BAD_REQUEST
            )

    
    
class BicycleTypeFeedbackPkView(APIView):
    permission_classes = [IsAuthenticated]
    def get(self, request, pk, *args, **kwargs):
        try:
            feedback = Feedback.objects.get(pk=pk)
        except Feedback.DoesNotExist:
            return Response(
                {'error': 'Không có giá trị thỏa mãn'},
                status=status.HTTP_404_NOT_FOUND
            )
            
        serializer = BicycleTypeFeedbackSerializer(instance=feedback)
        
        return Response(
            {'data': serializer.data},
            status=status.HTTP_200_OK
        )
    
    def put(self, request, pk, *args, **kwargs):
        data = request.data.copy()
        data['user'] = request.user.username

        try:
            instance = Feedback.objects.get(pk=pk, user=request.user)
        except Feedback.DoesNotExist:
            return Response(
                {'error': 'Không có giá trị thỏa mãn'},
                status=status.HTTP_404_NOT_FOUND
            )

        serializer = BicycleTypeFeedbackSerializer(instance=instance, data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(
                {'data': serializer.data},
                status=status.HTTP_201_CREATED
            )
        else:
            return Response(
                {'error': serializer.errors},
                status=status.HTTP_400_BAD_REQUEST
            )

    def delete(self, request, pk, *args, **kwargs):
        try:
            instance = Feedback.objects.get(pk=pk, user=request.user)
        except Feedback.DoesNotExist:
            return Response(
                {'error': 'Không có giá trị thỏa mãn'},
                status=status.HTTP_404_NOT_FOUND
            )
        instance.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)    


class EventFeedbackView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, *args, **kwargs):
        page = request.query_params.get('page', 1)
        limit = request.query_params.get('limit', 10)

        feedback = Feedback.objects.exclude(event=None).order_by('created_at')
        feedback_limit = Paginator(feedback, limit)

        try:
            page_feedbacks = feedback_limit.page(page)
        except PageNotAnInteger:
            page_feedbacks = feedback_limit.page(feedback_limit.num_pages)

        serializer = EventFeedbackSerializer(page_feedbacks, many=True)

        return Response(
            {'data': serializer.data},
            status=status.HTTP_200_OK
        )

    def post(self, request, *args, **kwargs):
        data = request.data.copy()
        data['user'] = request.user.username

        serializer = EventFeedbackSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(
                {'data': serializer.data},
                status= status.HTTP_201_CREATED
            )
        else:
            return Response(
                {'error': serializer.errors},
                status=status.HTTP_400_BAD_REQUEST
            )


class EventFeedbackPkView(APIView):
    permission_classes = [IsAuthenticated]
    
    def get(self, request, pk, *args, **kwargs):
        try:
            feedback = Feedback.objects.get(pk=pk)
        except Feedback.DoesNotExist:
            return Response(
                {'error': 'Không có giá trị thỏa mãn'},
                status=status.HTTP_404_NOT_FOUND
            )
            
        serializer = EventFeedbackSerializer(instance=feedback)
        
        return Response(
            {'data': serializer.data},
            status=status.HTTP_200_OK
        )
    
    def put(self, request, pk, *args, **kwargs):
        data = request.data.copy()
        data['user'] = request.user.username

        try:
            instance = Feedback.objects.get(pk=pk, user=request.user)
        except Feedback.DoesNotExist:
            return Response(
                {'error': 'Không có giá trị thỏa mãn'},
                status=status.HTTP_404_NOT_FOUND
            )

        serializer = EventFeedbackSerializer(instance=instance, data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(
                {'data': serializer.data},
                status=status.HTTP_201_CREATED
            )
        else:
            return Response(
                {'error': serializer.errors},
                status=status.HTTP_400_BAD_REQUEST
            )

    def delete(self, request, pk, *args, **kwargs):
        try:
            instance = Feedback.objects.get(pk=pk, user=request.user)
        except Feedback.DoesNotExist:
            return Response(
                {'error': 'Không có giá trị thỏa mãn'},
                status=status.HTTP_404_NOT_FOUND
            )
        instance.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)