# Django
from django.urls import path, re_path, include

from apps.users.consumers import NotificationConsumer

websocket_urlpatterns = [
    re_path(r'^ws/tutor/notifications/(?P<room_name>[^/]+)/$', NotificationConsumer),
]