from django.core.paginator import Paginator, PageNotAnInteger
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from bicycle.models import BicycleType, Bicycle
from bicycle.serializers import BicycleTypeSerializer, BicycleSerializer, GetBicycleSerializer


# Create your views here.
class BicycleTypeView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, *args, **kwargs):
        limit = request.query_params.get('limit', 10)
        page = request.query_params.get('page', 1)
        limit = int(limit)
        page = int(page)

        objects = BicycleType.objects.all().order_by('name')
        total_pages = len(objects) // limit + (1 if len(objects) % limit > 0 else 0)
        current_page_objects = objects[(page - 1) * limit:page * limit]

        serializer = BicycleTypeSerializer(current_page_objects, many=True)
        return Response({
            'data': serializer.data,
            'meta': {
                'total_pages': total_pages,
                'current_page': page,
                'limit': limit,
                'total': objects.count()
            }
        }, status=status.HTTP_200_OK)

    def post(self, request, *args, **kwargs):
        if not request.user.is_superuser:
            return Response(
                {'error': 'Bạn không có quyền thực hiện hành động này'},
                status=status.HTTP_403_FORBIDDEN
            )

        data = request.data.copy()
        serializer = BicycleTypeSerializer(data=data)
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


class BicycleTypePkView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, pk, *args, **kwargs):
        bicycle_type = BicycleType.objects.get(pk=pk)
        serializer = BicycleTypeSerializer(bicycle_type)
        return Response(
            {'data': serializer.data},
            status=status.HTTP_200_OK
        )

    def put(self, request, pk, *args, **kwargs):
        if not request.user.is_superuser:
            return Response(
                {'error': 'Bạn không có quyền thực hiện hành động này'},
                status=status.HTTP_403_FORBIDDEN
            )

        data = request.data.copy()
        try:
            type = BicycleType.objects.get(pk=pk)
        except BicycleType.DoesNotExist:
            return Response(
                {'error': 'Không có giá trị thỏa mãn'},
                status=status.HTTP_404_NOT_FOUND
            )

        serializer = BicycleTypeSerializer(instance=type, data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(
                {'data': serializer.data},
                status=status.HTTP_200_OK
            )
        else:
            return Response(
                {'error': serializer.errors},
                status=status.HTTP_400_BAD_REQUEST
            )

    def delete(self, request, pk, *args, **kwargs):
        if not request.user.is_superuser:
            return Response(
                {'error': 'Bạn không có quyền thực hiện hành động này'},
                status=status.HTTP_403_FORBIDDEN
            )

        try:
            type = BicycleType.objects.get(pk=pk)
        except BicycleType.DoesNotExist:
            return Response(
                {'error': 'Không có giá trị thỏa mãn'},
                status=status.HTTP_404_NOT_FOUND
            )

        type.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class BicycleView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, *args, **kwargs):
        limit = request.query_params.get('limit', 10)
        page = request.query_params.get('page', 1)
        limit = int(limit)
        page = int(page)

        objects = Bicycle.objects.all().order_by('id')
        total_pages = len(objects) // limit + (1 if len(objects) % limit > 0 else 0)
        current_page_objects = objects[(page - 1) * limit:page * limit]

        serializer = GetBicycleSerializer(current_page_objects, many=True)
        return Response({
            'data': serializer.data,
            'meta': {
                'total_pages': total_pages,
                'current_page': page,
                'limit': limit,
                'total': objects.count()
            }
        }, status=status.HTTP_200_OK)

    def post(self, request, *args, **kwargs):
        if not request.user.is_superuser:
            return Response(
                {'error': 'Bạn không có quyền thực hiện hành động này'},
                status=status.HTTP_403_FORBIDDEN
            )

        data = request.data.copy()
        serializer = BicycleSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(
                {'data': serializer.data},
                status=status.HTTP_201_CREATED
            )
        else:
            return Response(
                {'data': serializer.errors},
                status=status.HTTP_400_BAD_REQUEST
            )


class BicyclePkView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, pk, *args, **kwargs):
        bicycle = Bicycle.objects.get(pk=pk)
        serializer = GetBicycleSerializer(bicycle)
        return Response(
            {'data': serializer.data},
            status=status.HTTP_200_OK
        )

    def put(self, request, pk, *args, **kwargs):
        if not request.user.is_superuser:
            return Response(
                {'error': 'Bạn không có quyền thực hiện hành động này'},
                status=status.HTTP_403_FORBIDDEN
            )

        data = request.data.copy()
        try:
            bicycle = Bicycle.objects.get(pk=pk)
        except Bicycle.DoesNotExist:
            return Response(
                {'error': 'Không có giá trị thỏa mãn'},
                status=status.HTTP_404_NOT_FOUND
            )

        serializer = BicycleSerializer(instance=bicycle, data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(
                {'data': serializer.data},
                status=status.HTTP_200_OK
            )
        else:
            return Response(
                {'error': serializer.errors},
                status=status.HTTP_400_BAD_REQUEST
            )

    def delete(self, request, pk, *args, **kwargs):
        if not request.user.is_superuser:
            return Response(
                {'error': 'Bạn không có quyền thực hiện hành động này'},
                status=status.HTTP_403_FORBIDDEN
            )

        try:
            bicycle = Bicycle.objects.get(pk=pk)
        except Bicycle.DoesNotExist:
            return Response(
                {'error': 'Không có giá trị thỏa mãn'},
                status=status.HTTP_404_NOT_FOUND
            )

        bicycle.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
