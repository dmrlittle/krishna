from django.shortcuts import render, redirect
from django.contrib.auth import authenticate
from django.contrib.auth import login as auth_login, logout as auth_logout
from django.contrib.auth.models import User
from accounts.models import UserProfile
from accounts.forms import SignupForm, LoginForm

def login(request):
    if request.user.is_authenticated: 
        return redirect('chat:pilot')
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email'].lower().strip()
            password = form.cleaned_data['password']
            user = authenticate(email=email, password=password)
            if user is not None:
                auth_login(request, user)
                return redirect('chat:pilot')
    else:
        form = LoginForm()
    
    context = {'form':form }
    return render(request, 'accounts/login.html', context)

def signup(request):
    if request.method == 'POST':
        form = SignupForm(request.POST)
        if form.is_valid():
            firstname = form.cleaned_data['firstname']
            surname = form.cleaned_data['surname']
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']
            p=User.objects.create_user(username=f'{firstname} {surname}', first_name=firstname, last_name=surname, email=email, password=password)
            userprofile = UserProfile(user=p)
            userprofile.save()
            return redirect('accounts:login')
    else:
        form = SignupForm()
        
    context = {'form':form }
    return render(request, 'accounts/signup.html', context)

def logout(request):
    auth_logout(request)
    return redirect('accounts:login')