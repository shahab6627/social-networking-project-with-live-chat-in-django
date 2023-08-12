from channels.generic.websocket import WebsocketConsumer 
import json
from .models import UserChat,  FriendRequest
from asgiref.sync import async_to_sync, sync_to_async
class ChatConsumer(WebsocketConsumer):
    groups = ["broadcast"]
    def connect(self):
        self.group_name = self.room_name = self.scope['url_route']['kwargs']['slug']
        
        print("connection")
        self.accept()
        print("connection created")
        print("group_name " , self.group_name)
        print("room name", self.room_name)
        print("channel name ", self.channel_name)
        async_to_sync(self.channel_layer.group_add)(
            self.group_name,
            self.channel_name
        )
        
    
    def receive(self, text_data=None, bytes_data=None):
        print("data received")
        data = json.loads(text_data)
        friend_rel = data['friends_rel']
        msg = data['msg']
        msg_from = data['message_from']
        msg_to = data['message_to']
        
        send_msg = UserChat.objects.create(message = msg, msg_from_id = msg_from, msg_to_id = msg_to, friends_rel_id = friend_rel)
        send_msg.save()
       
        async_to_sync(self.channel_layer.group_send)(self.group_name, {
            'type' : 'chat.sendmsg',
            'msg': msg,
            'msg_from':msg_from
        })

    def chat_sendmsg(self, event):
        self.send(text_data = json.dumps({
            'type': 'websocket.send',
            'msg':event['msg'],
            'msg_from':event['msg_from']
            }))
        
        