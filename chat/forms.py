from django import forms
from chat.models import Room
from django.forms import ModelForm

class RoomEditForm(ModelForm):

    class Meta:

        model = Room
        fields = (
            'title',
            'background_color',
        )
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control'}),
            'background_color': forms.TextInput(attrs={'class': 'form-control jscolor'}),      
        }