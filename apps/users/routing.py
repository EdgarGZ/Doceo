# Django
from django.urls import path, re_path

from apps.users.consumers import NotificationConsumer

websocket_urlpatterns = [
    re_path(r'^ws/users/notifications/(?P<room_name>[^/]+)/$', NotificationConsumer),
]