from django.shortcuts import render, HttpResponse, redirect, get_object_or_404
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import *
from .helpers import send_forget_password_mail
from .utils import send_otp
import pyotp
from datetime import datetime
import uuid
from django.core.mail import send_mail
from django.conf import settings

# Create your views here.

@login_required(login_url='login')
def HomePage(request):
    return render(request, 'home.html')

def SignUpPage(request):
    if request.method == "POST":
        uname = request.POST.get('username')
        email = request.POST.get('email')
        password1 = request.POST.get('password1')
        password2 = request.POST.get('password2')
        
        if User.objects.filter(username=uname).exists():  # Checking if the username already exists
            return render(request, 'signup.html', {"error": "Username already exists."})
        
        if password1 != password2:  # Checking if passwords match
            return render(request, 'signup.html', {"error": "Password and Confirm password do not match."}) 
        else:
            my_user = User.objects.create_user(username=uname, email=email, password=password1)
            my_user.save()
            return redirect('login')
    
    return render(request, 'signup.html')

def LoginPage(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        pass1 = request.POST.get('pass')
        
        # Here using your custom backend
        user = authenticate(request, email=email, password=pass1)
        
        if user is not None:  # If there is a user
            my_otp = send_otp(request)
            send_mail(subject='OTP Verification',message=f" Your OTP is {my_otp} ",from_email='settings.EMAIL_HOST_USER',recipient_list=[email])
            request.session['email'] = email
            request.session['password'] = pass1
            return redirect('otp')
        else:
            return render(request, 'login.html', {"error": "Email or Password is incorrect !!"})
        
    return render(request, 'login.html')

def otp_view(request):
    error_message = None
    if request.method == 'POST':
        otp = request.POST.get('otp')
        email_r = request.session.get('email')  # Use get to avoid KeyError
        passw = request.session.get('password')
        
        otp_secret_key = request.session.get('otp_secret_key')
        otp_valid_date = request.session.get('otp_valid_date')
        
        if otp_secret_key and otp_valid_date is not None:
            valid_until = datetime.fromisoformat(otp_valid_date)

            if valid_until > datetime.now():
                print("OTP validation chal raha hai")
                totp = pyotp.TOTP(otp_secret_key, interval=120)
                if totp.verify(otp):
                    print('OTP verified successfully')
                    user = authenticate(request, email=email_r, password=passw)
                    if user is not None:  # Ensure user is authenticated
                        login(request, user)
                        
                        # Clear OTP session data
                        del request.session['otp_secret_key']
                        del request.session['otp_valid_date']
                        return redirect('home') 
                    else:
                        error_message = 'Authentication failed. Please try again.'
                else:
                    error_message = 'Invalid one-time password'
            else:
                error_message = 'One-time password has expired'
        else:
            error_message = 'Something went wrong with OTP session data'
    
    return render(request, 'otp.html', {'error_message': error_message})

def LogOut(request):
    logout(request)
    return redirect('login')

def About(request):
    return render(request, 'about.html')
