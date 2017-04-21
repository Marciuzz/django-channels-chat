# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render, HttpResponse, redirect

from django.contrib.auth.models import User
from users.models import Friend
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
from chat.forms import RoomEditForm

# Create your views here.

@login_required
def home(request, roomID=None):

    friends = {}
    try:
        friend = Friend.objects.get(current_user=request.user)
        friends = friend.users.all()
    except:
        pass

    for friend in friends:
        room = Chat_room.objects.get( (Q(user1=request.user) & Q(user2=friend)) | (Q(user2=request.user) & Q(user1=friend)) )
        friend.room = room.pk

    friend_ids = []
    for friend in friends:
        friend_ids.append(friend.pk)
    friend_ids.append(request.user.pk)

    users = User.objects.filter(~Q(pk__in = friend_ids))
    if roomID:
        args = {'users': users, 'friends': friends, 'current_user_id': request.user.pk, 'roomID': roomID}
    else:
        args = {'users': users, 'friends': friends, 'current_user_id': request.user.pk, 'roomID': "False"}

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

