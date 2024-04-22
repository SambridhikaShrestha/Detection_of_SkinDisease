from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.models import User  # Import the User model
from .forms import SignUpForm, LoginForm
from django.contrib.auth.decorators import login_required
from rest_framework.response import Response
from rest_framework.authtoken.models import Token
from rest_framework.views import APIView
from .serializers import UserSerializer
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated


@login_required(login_url='login')

def HomePage(request):
    return render(request, 'user.html')

def userhome(request):
    return render(request, 'home.html')

class RegisterUser(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    
    def get(self, request):
        user_objs = User.objects.all()
        serializer = UserSerializer(user_objs, many=True)
        print(request.user)
        return Response({'status' : 200, 'payload': serializer.data})
        
    def post(self, request):
        serializer = UserSerializer(data=request.data)
        
        if not serializer.is_valid():  # Corrected the typo here
            return Response({'status': 403, 'errors': serializer.errors, 'message': 'Something went wrong'})
        
        serializer.save()
        
        user = User.objects.get(username=serializer.data['username'])
        token_obj, _ = Token.objects.get_or_create(user=user) 
        
        return Response({'status': 200, 'payload': serializer.data, 'token': str(token_obj), 'message': 'Your data is saved'})

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
                form.add_error(None, 'Invalid username or password.')  # Adding non-field error
    else:
        form = LoginForm()
    return render(request, 'login.html', {'form': form})  

def LogoutPage(request):
    logout(request)
    return redirect('userhome')
