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


from django.core.mail import send_mail
import secrets
from .models import UserProfile
from django.urls import reverse


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


def verify_email(request, token):
    profile = UserProfile.objects.filter(verification_token=token).first()
    if profile:
        profile.email_verified = True
        profile.save()
        messages.success(request, 'Your email has been verified successfully. You can now login.')
    else:
        messages.error(request, 'Invalid verification token.')
    return redirect('login')


def SignupPage(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.save()
            verification_token = secrets.token_hex(20)
            UserProfile.objects.create(user=user, verification_token=verification_token)
            send_mail(
                'Email Verification',
                f'Click the following link to verify your email: http://127.0.0.1:8000/verify/{verification_token}',
                'skinchecker15@gmail.com',
                [user.email],
                fail_silently=False,
            )
            # Redirect to verification instructions page
            return redirect('verification_instructions')
        else:
            messages.error(request, 'There was an error creating your account. Please correct the errors below.')
    else:
        form = SignUpForm()
    return render(request, 'signup.html', {'form': form})



def LoginPage(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(request, username=username, password=password)
            if user is not None:
                # Check if user has a UserProfile and if the email is verified
                if hasattr(user, 'userprofile') and user.userprofile.email_verified:
                    login(request, user)
                    return redirect('home')
                else:
                    # Check if the message has already been added
                    if not any(message.message == 'Please verify your email to login.' for message in messages.get_messages(request)):
                        messages.error(request, 'Please verify your email to login.')
                    return render(request, 'login.html', {'form': form})  # Render login page again with error message
            else:
                form.add_error(None, 'Invalid username or password.')  # Adding non-field error
    else:
        form = LoginForm()
    return render(request, 'login.html', {'form': form})



def LogoutPage(request):
    logout(request)
    return redirect('userhome')


def VerificationInstructions(request):
    return render(request, 'verification_instructions.html')