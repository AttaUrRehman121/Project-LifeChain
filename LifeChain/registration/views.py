from django.shortcuts import render, redirect
from django.views.decorators.csrf import csrf_protect
from django.contrib.auth import authenticate, login as auth_login, logout as auth_logout
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .models import UserProfile
from django.db import IntegrityError
from django.contrib import messages
from registration.models import UserProfile
from django.db import IntegrityError
@csrf_protect

def signup(request):
    if request.method == 'POST':
        username = request.POST.get('username', '').strip()
        email = request.POST.get('email', '').strip().lower()
        nationality = request.POST.get('nationality', '').strip()
        role = request.POST.get('role', '').strip()
        contact = request.POST.get('contact', '').strip()
        address = request.POST.get('address', '').strip()
        password = request.POST.get('password', '')
        password2 = request.POST.get('password2', '')

        # Password criteria
        lengthCriteria = len(password) >= 8
        uppercaseCriteria = any(char.isupper() for char in password)
        numberCriteria = any(char.isdigit() for char in password)
        specialCharCriteria = any(char in '!@#$%^&*(),.?":{}|<>' for char in password)

        if not (lengthCriteria and uppercaseCriteria and numberCriteria and specialCharCriteria):
            messages.error(request, "Password must be at least 8 characters, include an uppercase letter, a number, and a special character.")
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
            user = UserProfile.objects.create_user(
                username=username,
                email=email,
                password=password,
                nationality=nationality,
                role=role,
                contact=contact,
                address=address
            )
            messages.success(request, "Account created successfully. Please log in.")
            return redirect('login')
        except IntegrityError as e:
            messages.error(request, "An error occurred while creating the user.")
            return render(request, 'signup.html')

    return render(request, 'signup.html')

@csrf_protect
def login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request, username=username, password=password)

        if user is not None:
            auth_login(request, user)

            
            if user.role == 'donor':
                return redirect('donorpage')
            elif user.role == 'recipient':
                return redirect('recipientpage')
            
        else:
            messages.error(request, "Invalid username or password.")
            return render(request, 'login.html')

    return render(request, 'login.html')

@login_required
def logout(request):
    auth_logout(request)
    messages.success(request, "You have been logged out successfully.")
    return redirect('/')
