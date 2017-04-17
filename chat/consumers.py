from django.http import HttpResponse
from channels.handler import AsgiHandler
from channels import Group
from channels.sessions import channel_session
from channels.auth import channel_session_user, channel_session_user_from_http
from models import ChatMessage
from channels import Channel

import json
# def http_consumer(message):
#     # Make a standard HTTP response - accces ASGI path attribu directly
#     response = HttpResponse("Hello world! You asked for %s" % message.content['path'])
#     # Encode that response into message formant (ASGI)
#     for chunk in AsgiHandler.encode_response(response):
#         message.reply_channel.send(chunk)


#Connected to websocket.connect
# @channel_session
# def ws_connect(message):
#     # Accept the incoming connection
#     message.reply_channel.send({"accept": True})

#     # work out room name from path(ignore slashes)
#     room = message.content['path'].strip("/")

#     #save room in session and add us to the group
#     message.channel_session['room'] = room

#     Group("chat-%s" % room).add(message.reply_channel)



#Connected to websocket disconenct
# @channel_session
# def ws_disconnect(message):
#     Group("chat-%s" % message.channel_session['room']).discard(message.reply_channel)


# # connected to websocket.recieve
# @channel_session
# def ws_message(message):
#     # ASGI WebSocket packet-recieved and send-packet message types 
#     # both gave a "text" key for their textual data.
    
#     Group("chat-%s" % message.channel_session['room']).send({
#         "text": message['text'],
#     })
    
    #sending back to reply channel

    # message.reply_channel.send({
    #     "text": message.content["text"],
    # })




#Connected to websocket.connect
@channel_session_user_from_http
def ws_connect(message):
    print("ws_connect ws_connect")
    # work out room name from path (ignore slashes)
    #room = message.content['path'].strip("/")
   
    # save room in session and add us to the group
    #message.channel_session['room'] = room
    #Group("chat-%s" % room).add(message.reply_channel)
    # Accept the connection request
    message.reply_channel.send({'accept': True})


# connected to websocet.receive 
@channel_session
def ws_message(message):
    print("ws_message ws_message")
    # Stick the message onto the processing queue
    #cont = json.loads(message['text'])
    #message.channel_session['room'] = cont['room']

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
    
    content = json.dumps({
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
    ChatMessage.objects.create(
        room=room,
        message=message['message'],
        user=message.user,
        username=message.user.username,
        user_image=str(message.user.profile.profile_photo),
        message_type=message['message_type']
    )
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






















# #Connected to websocket.connect
# @channel_session_user_from_http
# def ws_connect(message):
#     #accept connection
#     message.reply_channel.send({"accept": True})
#     # add them to the right group
#     Group("chat-%s" % message.user.username[0]).add(message.reply_channel)

# # connected to websocket.receive
# @channel_session_user
# def ws_message(message):
#     Group("chat-%s" % message.user.username[0]).send({
#         "text": message['text'],
#     })

# # Connected to websocket.disconnect
# @channel_session_user
# def ws_disconnect(message):
#     Group("chat-%s" % message.user.username[0]).discard(message.reply_channel)







