from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from .forms import SignUpForm, LoginForm
from django.contrib.auth.decorators import login_required

@login_required(login_url='login')
def HomePage(request):
    return render(request, 'user.html')

def userhome(request):
    return render(request, 'home.html')

def SignupPage(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Your account has been created successfully.')
            return redirect('login')
        else:
            messages.error(request, 'There was an error creating your account. Please correct the errors below.')
    else:
        form = SignUpForm()
    return render(request, 'signup.html', {'form': form, 'messages': messages.get_messages(request)})  # Pass 'messages' context variable

def LoginPage(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('home')
            else:
                messages.error(request, 'Invalid username or password.')
    else:
        form = LoginForm()
    return render(request, 'login.html', {'form': form, 'messages': messages.get_messages(request)})  # Pass 'messages' context variable

def LogoutPage(request):
    logout(request)
    return redirect('login')