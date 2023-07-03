from django.conf import settings
from django.contrib.auth import login, authenticate, logout
from django.shortcuts import render, redirect
from . import forms

def signup_page(request):
    form = forms.SignupForm()
    message = ''
    if request.method == 'POST':
        form = forms.SignupForm(request.POST)
        if form.is_valid():
            user = form.save()
            message = 'Votre compte a bien été créé.'
            login(request, user)
            return redirect('appreview:home')  # Redirection vers la vue "home"
    return render(
        request, 'authentication/signup.html', context={'form': form, 'message': message})

def login_page(request):
    form = forms.LoginForm()
    message = ''
    if request.method == 'POST':
        form = forms.LoginForm(request.POST)
        if form.is_valid():
            user = authenticate(
                username=form.cleaned_data['username'],
                password=form.cleaned_data['password'],
            )
            if user is not None:
                login(request, user)
                message = f'Bonjour, {user.username}! Vous êtes connecté.'
                return redirect('appreview:home')  # Redirection vers la vue "home"
            else:
                message = 'Identifiants invalides.'
    return render(
        request, 'authentication/login.html', context={'form': form, 'message': message})

def logout_page(request):
    logout(request)
    return redirect('login')
