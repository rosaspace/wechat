import json
from channels.generic.websocket import AsyncWebsocketConsumer


class ChatConsumer(AsyncWebsocketConsumer):

    async def connect(self):
        # self.user_id = self.scope["url_route"]["kwargs"]["user_id"]
        self.room_name = "chat_room"
        self.room_group_name = f"chat_{self.room_name}"

        # Join room group
        await self.channel_layer.group_add(
            self.room_group_name, self.channel_name
        )
        await self.accept()

    async def disconnect(self, close_code):
        # Leave room group
        await self.channel_layer.group_discard(
            self.room_group_name, self.channel_name
        )
        print(f"Connection closed with code {close_code}")

    # Receive message from WebSocket
    async def receive(self, text_data):
        text_data_json = json.loads(text_data)
        message = text_data_json["message"]
        received = text_data_json.get("received")
        sender = text_data_json.get("sender")
        timestamp = text_data_json.get("timestamp")

        # Send message to room group
        await self.channel_layer.group_send(
            self.room_group_name,
            {
                "type": "chat_message",
                "message": message,
                "timestamp": timestamp,
                "received": received,
                "sender": sender,
            },
        )

    # Receive message from room group
    async def chat_message(self, event):
        message = event["message"]
        timestamp = event["timestamp"]
        received = event["received"]
        sender = event["sender"]

        # Send message to WebSocket
        await self.send(
            text_data=json.dumps({
                "message": message,
                "timestamp": timestamp,
                "received": received,
                "sender": sender,
            })
        )
