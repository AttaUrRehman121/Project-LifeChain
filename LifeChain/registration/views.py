from django.shortcuts import redirect, render, HttpResponse
from django.views.decorators.csrf import csrf_protect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import models
from django.contrib.auth import authenticate, login as auth_login
from django.db import IntegrityError
from django.http import Http404
from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.hashers import make_password, check_password
from .models import UserProfile

@csrf_protect
def signup(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        email = request.POST.get('email')
        nationality = request.POST.get('nationality')
        role = request.POST.get('role')
        contact = request.POST.get('contact')
        address = request.POST.get('address')
        password = request.POST.get('password')

        if UserProfile.objects.filter(email=email).exists():
            messages.error(request, "Email is already registered.")
            return render(request, 'signup.html')
        
        if password != request.POST.get('password2'):
            messages.error(request, "Passwords do not match.")
            return render(request, 'signup.html')

        try:
            # Create a new user and hash the password
            user = UserProfile.objects.create(
                username=username,
                email=email,
                nationality=nationality,
                role=role,
                contact=contact,
                address=address,
                password=password,  # Ensure the password is hashed
            )
        except IntegrityError:
            messages.error(request, "An error occurred while creating the user. Please try again.")
            return render(request, 'signup.html')

        redirect('login')
            # Authenticate the user and log them in
    return render(request, 'signup.html')



def login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        try:
            user = UserProfile.objects.get(username=username)
            
            # Check hashed password
            request.session['username'] = user.username
            request.session['role'] = user.role

            if user.role == 'donor':
                    return redirect('donorpage')  
            elif user.role == 'recipient':
                    return redirect('recipientpage')
            else:
                messages.error(request, "Invalid username or password.")
                return redirect('login')

        except UserProfile.DoesNotExist:
            messages.error(request, "Invalid username or password.")
            return redirect('login')

    return render(request, 'login.html')

 