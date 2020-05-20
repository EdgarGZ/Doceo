# Channels
from channels.auth import AuthMiddlewareStack
from channels.routing import ProtocolTypeRouter, URLRouter

# Websockets routing
# import apps.users.routing
# from apps.tutor.routing import websocket_urlpatterns
from apps.tutor.routing import websocket_tutor_urlpatterns
from apps.tutored.routing import websocket_tutored_urlpatterns

application = ProtocolTypeRouter({
    'websocket': AuthMiddlewareStack(
        URLRouter([
            # apps.users.routing.websocket_urlpatterns
            websocket_tutor_urlpatterns,
            websocket_tutored_urlpatterns,
        ])
    ),
})