from django.urls import path

from feedback.views import EventFeedbackView, BicycleTypeFeedbackView, BicycleFeedbackView, EventFeedbackPkView, BicycleTypeFeedbackPkView, BicycleFeedbackPkView

urlpatterns = [
    path('events/', EventFeedbackView.as_view(), name='event_feedback' ),
    path('events/<uuid:pk>', EventFeedbackPkView.as_view(), name='event_feedback' ),
    path('bicycle-types/', BicycleTypeFeedbackView.as_view(), name='bicycle_type_feedback' ),
    path('bicycle-types/<uuid:pk>', BicycleTypeFeedbackPkView.as_view(), name='bicycle_type_feedback' ),
    path('bicycles/', BicycleFeedbackView.as_view(), name='bicycle_feedback' ),
    path('bicycles/<uuid:pk>', BicycleFeedbackPkView.as_view(), name='bicycle_feedback' ),
]