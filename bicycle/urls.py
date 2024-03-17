from django.urls import path

from bicycle.views import *

urlpatterns = [
    path('', BicycleView.as_view(), name='bicycle'),
    path('<uuid:pk>/', BicyclePkView.as_view(), name='bicycle'),
    path('types/', BicycleTypeView.as_view(), name='bicycle_type'),
    path('types/<uuid:pk>/', BicycleTypePkView.as_view(), name='bicycle_type'),
]