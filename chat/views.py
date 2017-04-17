# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render, HttpResponse

from django.contrib.auth.models import User
from users.models import Friend
from chat.models import ChatMessage
import json
from django.http import JsonResponse
from django.core import serializers
from django.db.models import Q
from django.contrib.auth.decorators import login_required

# Create your views here.

@login_required
def home(request):

    
    friends = {}
    try:
        friend = Friend.objects.get(current_user=request.user)
        friends = friend.users.all()
    except:
        pass

    for friend in friends:
        if friend.pk < request.user.pk:
            friend.room = 'room-' + str(friend.pk) + '-' + str(request.user.pk)
        else:
            friend.room = 'room-' + str(request.user.pk) + '-' + str(friend.pk)

    friend_ids = []
    for friend in friends:
        friend_ids.append(friend.pk)
    friend_ids.append(request.user.pk)

    users = User.objects.filter(~Q(pk__in = friend_ids))

    args = {'users': users, 'friends': friends, 'current_user_id': request.user.pk}

    return render(request, 'chat/home.html', args)

def get_messages(request, room):

    query_data = ChatMessage.objects.filter(room=room).order_by('-created')[:20]

    messages = []

    for item in query_data:
        messages.append({
            "created": str(item.created),
            "message": item.message,
            "room": item.room,
            "username": item.user.username,
            "profile_photo": str(item.user.profile.profile_photo),
            "user_id": item.user.pk
        })
    

    return HttpResponse(json.dumps(messages))
