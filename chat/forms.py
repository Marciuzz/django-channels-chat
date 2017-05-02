from django import forms
from chat.models import Chat_room, Chat_group
from django.forms import ModelForm

class RoomEditForm(ModelForm):

    class Meta:

        model = Chat_room
        fields = (
            'title',
            'background_color',
        )
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control'}),
            'background_color': forms.TextInput(attrs={'class': 'form-control jscolor'}),      
        }

class GroupRoomEditForm(ModelForm):

    class Meta:

        model = Chat_group
        fields = (
            'title',
            'background_color',
            'users',
        )
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control'}),
            'background_color': forms.TextInput(attrs={'class': 'form-control jscolor'}),
            'users': forms.CheckboxSelectMultiple(attrs={'class': 'form-control'}),
        }