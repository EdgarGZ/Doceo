# Django
from django.urls import path, re_path, include

from apps.tutor.consumers import TutorNotificationConsumer

websocket_tutor_urlpatterns = re_path(r'^ws/tutor/notifications/(?P<room_name>[^/]+)/$', TutorNotificationConsumer)