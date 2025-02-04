from multiprocessing import AuthenticationError
from django.contrib import messages
from django.shortcuts import render, redirect
from django.views.decorators.csrf import csrf_protect
from django.contrib.auth import login as auth_login, authenticate
from .models import Contact
from django.views.decorators.csrf import csrf_exempt

# Create your views here.
def index(request):
    return render(request, 'index.html')

@csrf_exempt
def contact(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        email = request.POST.get('email')
        phone_number = request.POST.get('phone_number')
        message = request.POST.get('message')

        # Save the contact data into the database
        contact = Contact(name=name, email=email, phone_number=phone_number, message=message)
        contact.save()

        # After saving the contact, show a success message
        messages.success(request, 'Your message has been sent successfully!')
        return redirect('contact')  # Redirect back to the contact page

    return render(request, 'contactUs.html')
    
def about(request):
    return render(request, 'about.html')

def profile_view(request):
    return render(request, 'profile.html')


# def login(request):
#     return render(request, 'login.html')


# def logout(request):
#     return render(request, 'profile.html')


