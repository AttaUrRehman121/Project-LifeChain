from django.shortcuts import redirect, render, HttpResponse
from django.views.decorators.csrf import csrf_protect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import models
from django.contrib.auth import authenticate, login as auth_login
from django.db import IntegrityError
from django.http import Http404
from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.hashers import make_password
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

        try:
            # Create a new user and hash the password
            user = UserProfile.objects.create(
                username=username,
                email=email,
                nationality=nationality,
                role=role,
                contact=contact,
                address=address,
                password=make_password(password),  # Ensure the password is hashed
            )

            # Authenticate the user and log them in
            user_auth = authenticate(request, username=username, password=password)
            if user_auth is not None:
                auth_login(request, user_auth)
                # Redirect based on the user's role
                if user.role == 'donor':
                    return redirect('donorPage.html')  # Replace with actual donor page URL name
                elif user.role == 'recipient':
                    return redirect('recipientPage.html')  # Replace with actual recipient page URL name
            else:
                messages.error(request, "Login failed after sign-up.")
                return redirect('login')

        except Exception as e:
            messages.error(request, f"An error occurred: {str(e)}")
            return render(request, 'signup.html')

    return render(request, 'signup.html')


