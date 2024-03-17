from django.urls import path

from feedback.views import EventFeedbackView, BicycleTypeFeedbackView, BicycleFeedbackView

urlpatterns = [
    path('events/', EventFeedbackView.as_view(), name='event_feedback' ),
    path('events/<uuid:pk>', EventFeedbackView.as_view(), name='event_feedback' ),
    path('bicycle-types/', BicycleTypeFeedbackView.as_view(), name='bicycle_type_feedback' ),
    path('bicycle-types/<uuid:pk>', BicycleTypeFeedbackView.as_view(), name='bicycle_type_feedback' ),
    path('bicycle/', BicycleFeedbackView.as_view(), name='bicycle_feedback' ),
    path('bicycle/<uuid:pk>', BicycleFeedbackView.as_view(), name='bicycle_feedback' ),
]