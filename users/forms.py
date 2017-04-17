from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from users.models import Profile


class RegistrationForm(UserCreationForm):

    email = forms.EmailField(required=True)
    class Meta:
        model = User
        fields = (
            'username',
            'email',
            'password1',
            'password2'
        )
    def save(self, commit=True):
        user = super(RegistrationForm, self).save(commit=True)
        user.email = self.cleaned_data['email']

        if commit:
            user.save()
            
        return user

class EditUserForm(UserChangeForm):

    class Meta:
        model = User
        fields = (
            'email',
            'username',
            'password'
        )

class EditProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ('profile_photo',)