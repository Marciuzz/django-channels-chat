from django.http import HttpResponse
from channels.handler import AsgiHandler
from channels import Group
from channels.sessions import channel_session
from channels.auth import channel_session_user, channel_session_user_from_http
from models import ChatMessage, Room
from channels import Channel
import json


#Connected to websocket.connect
@channel_session_user_from_http
def ws_connect(message):
    print("ws_connect")

    message.reply_channel.send({'accept': True})


# connected to websocet.receive 
@channel_session
def ws_message(message):

    print("ws_message")
    
    payload = json.loads(message['text'])
    payload['reply_channel'] = message.content['reply_channel']
    Channel("chat.receive").send(payload)

    
# connected to websocket.disconnect
@channel_session
def ws_disconnect(message):
    print("LEAVE CHAT") 
    #Group("chat-%s" % message.channel_session['room']).discard(message.reply_channel)
    Group("chat-1-2").discard(message.reply_channel)

@channel_session
def chat_join(message):
    room = message['room']
    Group("chat-%s" % room).add(message['reply_channel'])
    
    roomObj = Room.objects.get(pk=room)

    content = json.dumps({
        "room_background": roomObj.background_color,
        "room_title": roomObj.title,
        "room": room,
        "msg_type": "joined"
    })
    message.reply_channel.send({
        "text": content
    })
    
    print("JOIN CHAT")

def chat_leave(message):
    print("LEAVE CHAT") 
    room = message['room']
    print(room)
    Group("chat-%s" % room).discard(message.reply_channel)

@channel_session_user
def chat_send(message):
    print("SEND CHAT")
    room = message['room']
    roomObj = Room.objects.get(pk=room)

    ChatMessage.objects.create(
        room=roomObj,
        message=message['message'],
        user=message.user,
        username=message.user.username,
        user_image=str(message.user.profile.profile_photo),
        message_type=message['message_type']
    )
    print("chat message created succesfuullt")
    content = json.dumps({
        "msg_type": message['message_type'],
        "message": message['message'],
        "room": room,
        "username": str(message.user),
        "user_id": message.user.id,
        "user_image": str(message.user.profile.profile_photo)
    })

    # Broadcast to listening sockets
    Group("chat-%s" % room).send({
        "text": content
    })
