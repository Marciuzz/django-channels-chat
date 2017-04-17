# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
from django.contrib.auth.models import User
# Create your models here.


class ChatMessage(models.Model):

    # message
    message = models.CharField(max_length=255)

    # room
    room = models.CharField(max_length=255)

    #user
    user = models.ForeignKey(User, null=True)

    #timestamp
    created = models.DateTimeField(auto_now_add=True, null=True)

    #username
    username = models.CharField(max_length=255, null=True)

    #user image
    user_image = models.CharField(max_length=255, null=True)

    #type
    message_type = models.CharField(max_length=10, null=True)