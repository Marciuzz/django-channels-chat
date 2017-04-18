# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
from django.contrib.auth.models import User
# Create your models here.

class Room(models.Model):

    background_color = models.CharField(max_length=10, default="ffffff")
    title = models.CharField(max_length=30, default="chat-room")
    user1 = models.ForeignKey(User, null=True, related_name="user1")
    user2 = models.ForeignKey(User, null=True, related_name="user2")

class ChatMessage(models.Model):

    message = models.CharField(max_length=255)
    room = models.ForeignKey(Room, null=True)
    user = models.ForeignKey(User, null=True)
    created = models.DateTimeField(auto_now_add=True, null=True)
    username = models.CharField(max_length=255, null=True)
    user_image = models.CharField(max_length=255, null=True)
    message_type = models.CharField(max_length=10, null=True)

