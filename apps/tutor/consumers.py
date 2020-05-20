# Imports
from channels.generic.websocket import WebsocketConsumer
from asgiref.sync import async_to_sync
import json

# Models 
from apps.users.models import User, Usuario
from apps.tutorships.models import HorarioTutoria


class TutorNotificationConsumer(WebsocketConsumer):

    def connect(self):
        # Checking if the User is logged in
        if self.scope["user"].is_anonymous:
            # Reject the connection
            self.close()
        else:
            # print(self.scope["user"])   # Can access logged in user details by using self.scope.user, Can only be used if AuthMiddlewareStack is used in the routing.py
            self.room_name = self.scope['url_route']['kwargs']['room_name']
            self.group_name = self.room_name  # Setting the group name as the pk of the user primary key as it is unique to each user. The group name is used to communicate with the user.
            self.user = User.objects.get(username=self.room_name)
            async_to_sync(self.channel_layer.group_add)(
                self.group_name, 
                self.channel_name
            )
            self.accept()

    def disconnect(self, close_code):
        self.close()

    def notify_new_tutorship(self, event):
        tutoreds = Usuario.objects.filter(is_tutorado=True)
        mensaje = f'{ event["user"] } ha ofertado una nueva tutoria de { event["subarea_especialidad"] } del area { event["area_especialidad"] } para el proximo { event["dia"] }!.'
        for tutored in tutoreds:
            async_to_sync(self.channel_layer.group_send)(
                tutored.user.username,
                {
                    'type': 'notify',
                    'message': mensaje
                }
            )

    acciones = {
        'notify_tutorship': notify_new_tutorship,
    }

    def receive(self, web_socket_data):
        """ 
            When an action is sent by the websocket this is te first function
            that is called.
            The web socket data is mapped int the acciones dict that contains custom
            actions that will do something. That function is called to do its work.

            Input:
                - web_socket_data
            Output:
                - None
        """
        data = json.loads(web_socket_data)
        self.acciones[data['accion']](self, data)

    def notify(self, event):
        self.send(text_data=json.dumps(event["message"]))