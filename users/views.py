# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render, redirect, HttpResponse
from django.views.generic import TemplateView
from users.forms import RegistrationForm, EditProfileForm, EditUserForm, LoginForm, ChangePassswordForm
from django.contrib.auth.forms import AuthenticationForm, PasswordChangeForm
from django.contrib.auth import update_session_auth_hash, login
from django.contrib.auth.models import User
from models import Friend
from chat.models import Room
from django.db.models import Q


# Create your views here.


class RegisterView(TemplateView):

    def get(self, request):
        form = RegistrationForm()
        args = {'form': form}
        return render(request, 'users/register.html', args)

    def post(self, request):
        form = RegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('/')
        return redirect('/users/register')



class EditProfileView(TemplateView):
    def get(self, request):
        user_form = EditUserForm(instance=request.user)
        profile_form = EditProfileForm(instance=request.user.profile)
        args = {'user_form': user_form, 'profile_form': profile_form}
        return render(request, 'users/edit_profile.html', args)

    def post(self, request):
        user_form = EditUserForm(request.POST, instance=request.user)
        profile_form = EditProfileForm(request.POST, request.FILES, instance=request.user.profile)
        
        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            return redirect('/users/view')
        return HttpResponse("Something went wrong")

class ChangePasswordView(TemplateView):
    def get(self, request):
        form = ChangePassswordForm(user=request.user)
        args = {'form': form}
        return render(request, 'users/change-password.html', args)
    def post(self, request):
        form = PasswordChangeForm(data=request.POST, user=request.user);
        if form.is_valid():
            form.save()
            update_session_auth_hash(request, form.user)
            return redirect('/users/view/')
        else:
            return redirect('/users/change-password')

def view_profile(request):
    user = request.user
    args = {'user': user}
    return render(request, 'users/profile.html', args)

def home(request):
    return render(request, 'users/home.html', {})

def change_friends(request, action, pk):
    if not request.user.is_authenticated():
        return redirect('/')
    elif int(pk) == int(request.user.pk):
        return redirect('/')
    else:
        new_user = User.objects.get(pk=pk)
        if action == 'add':
            
            if Room.objects.filter((Q(user1=request.user) & Q(user2=new_user)) | (Q(user2=request.user) & Q(user1=new_user)) ).exists():
                pass
            else:
                room = Room(user1=request.user, user2=new_user)
                room.save()
            
            Friend.make_friend(request.user, new_user)
        elif action == 'loose':
            Friend.lose_friend(request.user, new_user)
        return redirect('/')

class LoginView(TemplateView):
    def get(self, request):
        form = LoginForm()
        args = {'form': form}

        return render(request, 'users/login.html', args)

    def post(self, request):
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            login(request, form.get_user())
            return redirect('/')
        else:
            return redirect('/users/login')