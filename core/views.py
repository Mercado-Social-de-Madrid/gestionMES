# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import messages
from django.contrib.auth import authenticate, login, update_session_auth_hash
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import PasswordChangeForm
from django.shortcuts import render, redirect

# Create your views here.
from core.forms.password import PasswordForm
from core.forms.profile import ProfileForm
from core.forms.signup import SignUpForm


def register(request):

    form = SignUpForm()
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=raw_password)

            login(request, user)
            return redirect('dashboard')
        else:
            print(form.errors)

    return render(request, 'registration/signup.html', {'form': form})


def dashboard(request):

    return render(request, 'user/dashboard.html', {'user': request.user})


def edit_profile(request):
    if request.method == 'POST':
        profile_form = ProfileForm(request.POST, instance=request.user)
        if profile_form.is_valid():
            profile_form.save()
        else:
            print(profile_form.errors)
    else:
        profile_form = ProfileForm(instance=request.user)
    password_form = PasswordForm(user=request.user)

    return render(request, 'user/profile.html',
                  {'profile_form': profile_form,
                   'password_form':password_form,
                   'profile_tab': True
                   })

def profile_password(request):
    if request.method == 'POST':
        password_form = PasswordForm(data=request.POST, user=request.user)

        if password_form.is_valid():
            user = password_form.save()
            update_session_auth_hash(request, user)  # Important!
            messages.success(request, 'Contraseña actualizada correctamente')
            return redirect('edit_profile')
        else:
            print(password_form.errors)
    else:
        password_form = PasswordForm(user=request.user)

    profile_form = ProfileForm(instance=request.user)
    return render(request, 'user/profile.html', {
            'profile_form': profile_form,
            'password_form':password_form,
            'password_tab':True
            })
