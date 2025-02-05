from django.shortcuts import redirect, render, HttpResponse
from django.views.decorators.csrf import csrf_protect
from django.contrib.auth.decorators import login_required
from .models import UserProfile
from django.contrib.auth import authenticate, login as auth_login
from django.db import IntegrityError
from django.http import Http404
from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.hashers import make_password, check_password

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
        password2 = request.POST.get('password2')

        # Password validation
        lengthCriteria = len(password) >= 8
        uppercaseCriteria = any(char.isupper() for char in password)
        numberCriteria = any(char.isdigit() for char in password)
        specialCharCriteria = any(char in '!@#$%^&*(),.?":{}|<>' for char in password)
        
        if not (lengthCriteria and uppercaseCriteria and numberCriteria and specialCharCriteria):
            messages.error(request, "Password must be at least 8 characters long, contain an uppercase letter, a number, and a special character.")
            return render(request, 'signup.html')

        if UserProfile.objects.filter(email=email).exists():
            messages.error(request, "Email is already registered.")
            return render(request, 'signup.html')

        if UserProfile.objects.filter(username=username).exists():
            messages.error(request, "Username is already taken.")
            return render(request, 'signup.html')

        if password != password2:
            messages.error(request, "Passwords do not match.")
            return render(request, 'signup.html')

        try:
            user = UserProfile(
                username=username,
                email=email,
                nationality=nationality,
                role=role,
                contact=contact,
                address=address
            )
            user.set_password(password)  # Hash password
            user.save()

            messages.success(request, "Account created successfully. Please log in.")
            return redirect('login')
        except IntegrityError:
            messages.error(request, "An error occurred while creating the user. Please try again.")
            return render(request, 'signup.html')

    return render(request, 'signup.html')

@csrf_protect
def login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        try:
            user = UserProfile.objects.get(username=username)
        except UserProfile.DoesNotExist:
            messages.error(request, "Invalid username or password.")
            return redirect('login')

        if user.check_password(password):  # Check hashed password
            request.session['username'] = user.username
            request.session['role'] = user.role

            if user.role == 'donor':
                return redirect('donorpage')
            elif user.role == 'recipient':
                return redirect('recipientpage')
            else:
                messages.error(request, "Invalid role.")
                return redirect('login')
        else:
            messages.error(request, "Invalid username or password.")
            return redirect('login')

    return render(request, 'login.html')