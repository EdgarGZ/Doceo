# Imports
from channels.generic.websocket import WebsocketConsumer
from asgiref.sync import async_to_sync
import json

# Models 
from apps.users.models import User
from apps.tutorships.models import HorarioTutoria


class NotificationConsumer(WebsocketConsumer):

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

    def notify_schedule_tutorship(self, event):
        tutoria = HorarioTutoria.objects.get(id=event["referencia"])
        mensaje = f'{ event["user"] } quiere pedirte una tutoria de { event["tutoship_area"] } para el proximo { tutoria.dia } de este mes!.'
        async_to_sync(self.channel_layer.group_send)(
            tutoria.tutor.usuario.user.username,
            {
                'type': 'notify',
                'message': mensaje
            }
        )

    def notify_tutored_accepted_tutorship(self, event):
        tutorado = User.objects.get(username=event['tutored'])
        tutor = User.objects.get(username=self.room_name)
        mensaje = f'{ tutor.username } ha aceptado tu solicitud para tomar la tutoría { event["tutorship"] }!.'
        async_to_sync(self.channel_layer.group_send)(
            tutorado.username,
            {
                'type': 'notify',
                'message': mensaje
            }
        )

    acciones = {
        'notify_schedule_tutorship': notify_schedule_tutorship,
        'notify_tutored_accepted_tutorship': notify_tutored_accepted_tutorship
    }

    def receive(self, text_data):
        data = json.loads(text_data)
        self.acciones[data['accion']](self, data)

    def notify(self, event):
        self.send(text_data=json.dumps(event["message"]))