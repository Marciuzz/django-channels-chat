# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render, HttpResponse, redirect

from django.contrib.auth.models import User
from users.models import Friend, Friend_request
import json
from django.http import JsonResponse
from django.core import serializers
from django.db.models import Q
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from channels_chat import settings
import os
import time
from chat.models import Chat_room, ChatMessage, Chat_group, GroupChatMessage
from django.views.generic import TemplateView
from django.db.models import Q
from chat.forms import RoomEditForm, GroupRoomEditForm

# Create your views here.

@login_required
def home(request, roomID=None, group_roomID=None):

    friends = {}
    skip_user_ids = []
    requests_sent = {}
    requests_received = {}
    group_chats = {}

    try:
        friend = Friend.objects.get(current_user=request.user)
        friends = friend.users.all()
    except:
        pass

    for friend in friends:
        room = Chat_room.objects.get( (Q(user1=request.user) & Q(user2=friend)) | (Q(user2=request.user) & Q(user1=friend)) )
        friend.room = room.pk
        skip_user_ids.append(friend.pk)

    skip_user_ids.append(request.user.pk)
 
    try:
        reqests_obj = Friend_request.objects.get(current_user=request.user)
        requests_sent = reqests_obj.requests_sent.all()
        requests_received = reqests_obj.requests_received.all()
    except:
        pass
    
    for user in requests_sent:
        skip_user_ids.append(user.pk)

    for user in requests_received:
        skip_user_ids.append(user.pk)

    try:
        group_chats = Chat_group.objects.all()
    except:
        pass

    for group_chat in group_chats:
        group_chat.room = group_chat.pk

    users = User.objects.filter(~Q(pk__in = skip_user_ids))

    if roomID:
        args = {'users': users, 'friends': friends, 'current_user_id': request.user.pk, 'roomID': roomID, 'requests_received': requests_received, 'requests_sent': requests_sent, 'group_chats': group_chats}
    else:
        args = {'users': users, 'friends': friends, 'current_user_id': request.user.pk, 'roomID': "False", 'requests_received': requests_received, 'requests_sent': requests_sent, 'group_chats': group_chats}

    if group_roomID:
        args = {'users': users, 'friends': friends, 'current_user_id': request.user.pk, 'roomID': "False", 'group_roomID': group_roomID, 'requests_received': requests_received, 'requests_sent': requests_sent, 'group_chats': group_chats}
    else:
        args = {'users': users, 'friends': friends, 'current_user_id': request.user.pk, 'roomID': "False", 'group_roomID': "False", 'requests_received': requests_received, 'requests_sent': requests_sent, 'group_chats': group_chats}


    return render(request, 'chat/home.html', args)

def get_messages(request, room):

    targetroom = Chat_room.objects.get(pk=room)

    query_data = ChatMessage.objects.filter(room=targetroom).order_by('-created')[:20]

    messages = []
    
    for item in query_data:
        messages.append({
            "created": item.created.strftime("%Y-%m-%d %H:%M"),
            "message": item.message,
            "room": item.room.pk,
            "username": item.user.username,
            "profile_photo": str(item.user.profile.profile_photo),
            "user_id": item.user.pk,
            "content_type": item.content_type
        })

    return HttpResponse(json.dumps(messages))

def get_group_messages(request, group):

    messages = []

    if group == "global":
        try:
            targetgroup = Chat_group.objects.get(global_group=True)
        except:
            return HttpResponse(json.dumps(messages))
    else:
        targetgroup = Chat_group.objects.get(pk=group)

    query_data = GroupChatMessage.objects.filter(group=targetgroup).order_by('-created')[:20]

    for item in query_data:
        messages.append({
            "created": item.created.strftime("%Y-%m-%d %H:%M"),
            "message": item.message,
            "group": item.group.pk,
            "username": item.user.username,
            "profile_photo": str(item.user.profile.profile_photo),
            "user_id": item.user.pk,
            "content_type": item.content_type
        })

    return HttpResponse(json.dumps(messages))

@csrf_exempt
def upload_photo(request):

    image = request.FILES['image']
    room = request.POST['room']
    timestamp = int(time.time())

    filename = str(timestamp) + ".jpg"

    if not os.path.exists(os.path.join(settings.MEDIA_ROOT, "room_images", room)):
        os.makedirs(os.path.join(settings.MEDIA_ROOT, "room_images", room))

    with open(os.path.join(settings.MEDIA_ROOT, "room_images", room, filename), 'w+') as destination:
        for chunk in image.chunks():
            destination.write(chunk)

    return HttpResponse(json.dumps({
        'imagename': os.path.join(room, filename),
        'room': room
    }))

class RoomEditView(TemplateView):
    def get(self, request, room):
        if room =='0':
            return redirect('chat:home')
        else:
            room = Chat_room.objects.get(pk=room)
            form = RoomEditForm(instance=room)   
            args = {"form": form}
            return render(request, 'chat/edit_room.html', args);
        
    def post(self,request, room):
        room = Chat_room.objects.get(pk=room)
        form = RoomEditForm(request.POST, instance=room)
        if form.is_valid():
            form.save()
            return redirect('chat:home_with_id', roomID= str(room.pk))
        return redirect('chat:home')

class GroupChatCreateView(TemplateView):
    def get(self, request):
        form = GroupRoomEditForm()
        args = {"form": form}
        return render(request, 'chat/create_group_chat.html', args)
        
    def post(self,request):
        form = GroupRoomEditForm(request.POST)
        if form.is_valid():
            form.save()
            the_last_chat = Chat_group.objects.last()
            return redirect('chat:group_with_id', group_roomID=str(the_last_chat.pk))
        return redirect('chat:home')

class GroupRoomEditView(TemplateView):
    def get(self, request, room):
        if room =='0':
            return redirect('chat:home')
        else:
            room = Chat_group.objects.get(pk=room)
            form = GroupRoomEditForm(instance=room)
            friend = Friend.objects.get(current_user=request.user)
            friends = friend.users.all()
            args = {"form": form, 'friends': friends}
            return render(request, 'chat/edit_group_room.html', args);
        
    def post(self,request, room):
        room = Chat_group.objects.get(pk=room)
        form = GroupRoomEditForm(request.POST, instance=room)
        if form.is_valid():
            form.save()
            return redirect('chat:group_with_id', group_roomID= str(room.pk))
        return redirect('chat:home')
        
def remove_group_chat(self, room):
    currentRoom = Chat_group.objects.get(pk=room)
    currentRoom.delete()
    return redirect('chat:home')