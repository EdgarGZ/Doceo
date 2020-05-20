# Django
from django.urls import path, re_path, include

from apps.tutored.consumers import NotificationConsumer

websocket_tutored_urlpatterns = re_path(r'^ws/tutored/notifications/(?P<room_name>[^/]+)/$', NotificationConsumer)