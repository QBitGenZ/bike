from django.urls import path

from event.views import EventView, EventPkView, EventParticipationView

urlpatterns = [
    path('', EventView.as_view(), name='event'),
    path('<uuid:pk>/', EventPkView.as_view(), name='event'),
    path('<uuid:event_id>/participate/', EventParticipationView.as_view(), name='event_participate'),
]