# Imports
from channels.generic.websocket import WebsocketConsumer
from asgiref.sync import async_to_sync
import json

# Models 
from apps.users.models import User, Usuario
from apps.tutorships.models import HorarioTutoria, NotificacionNuevoHorario


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
        # pass

    # Eventos Tutor

    def notify_new_tutorship(self, event):
        tutoreds = Usuario.objects.filter(is_tutorado=True)
        tutor = Usuario.objects.get(id=event["id"])
        tutorship = HorarioTutoria.objects.get(id=event["horario"])
        mensaje = f'{tutor.nombre} ha ofertado una nueva tutoria de {tutorship.area_especialidad}!.'
        for tutored in tutoreds:
            # NotificacionNuevoHorario.objects.create(tutor=tutor, tutorado=tutored, tutoria=tutorship, mensaje=mensaje)
            async_to_sync(self.channel_layer.group_send)(
                tutored.user.username,
                {
                    'type': 'notify',
                    'mensaje': f'{tutor.user.username} ha ofertado una nueva tutoria de {tutorship.area_especialidad}!. '
                }
            )

    acciones = {
        'notify_tutorship': notify_new_tutorship,
    }

    def receive(self, text_data):
        data = json.loads(text_data)
        self.acciones[data['accion']](self, data)

    def notify(self, event):
        self.send(text_data=json.dumps(event["mensaje"]))