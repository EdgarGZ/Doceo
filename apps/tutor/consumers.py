# Imports
from channels.generic.websocket import WebsocketConsumer
from asgiref.sync import async_to_sync
import json

# Models 
from apps.users.models import User


class NotificationConsumer(WebsocketConsumer):

    # Function to connect to the websocket
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
            print(self.user)
            async_to_sync(self.channel_layer.group_add)(
                self.group_name, 
                self.channel_name
            )
            self.accept()

    # Function to disconnet the Socket
    def disconnect(self, close_code):
        self.close()
        # pass

    def receive(self, text_data):
        text_data_json = json.loads(text_data)
        message = text_data_json['message']

        # Send message to room group
        async_to_sync(self.channel_layer.group_send)(
            self.group_name,
            {
                'type': 'notify',
                'message': message
            }
        )

    # Custom Notify Function which can be called from Views or api to send message to the frontend
    def notify(self, event):
        print(event)
        self.send(text_data=json.dumps(event["message"]))