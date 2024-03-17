from django.urls import path

from resource.views import BicycleImageView, EventImageView, FeedbackImageView

urlpatterns = [
    path('bicycles/', BicycleImageView.as_view(), name='bicycle_image'),
    path('bicycles/<uuid:pk>', BicycleImageView.as_view(), name='bicycle_image'),
    path('events/', EventImageView.as_view(), name='event_image'),
    path('events/<uuid:pk>', EventImageView.as_view(), name='event_image'),
    path('feedbacks/', FeedbackImageView.as_view(), name='feedback_image'),
    path('feedbacks/<uuid:pk>', FeedbackImageView.as_view(), name='feedback_image'),
]