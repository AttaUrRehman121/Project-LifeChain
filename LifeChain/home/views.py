from django.contrib import messages
from django.shortcuts import render, redirect
from django.views.decorators.csrf import csrf_protect
from django.contrib.auth import login as auth_login, authenticate
from .models import Contact
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from django.http import HttpResponse
from donor.models import donor_Registered
from recipient.models import AllocatedDonorToRecipient, Recipient
from registration.models import UserProfile
from django.contrib.auth.decorators import login_required

# Create your views here.
def index(request):
    try:
        return render(request, 'index.html')
    except Exception as e:
        return HttpResponse(f"Error rendering index: {str(e)}", status=500)

def test_view(request):
    """Simple test view to check if Django is working"""
    return HttpResponse("Django is working! This is a test view.")

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

@login_required
def profile_view(request):
    user = request.user

    # Donor section
    donor = donor_Registered.objects.filter(user=user).first()
    donor_allocation = None
    if donor:
        donor_allocation = AllocatedDonorToRecipient.objects.filter(donor=donor).last()

    # Recipient section
    recipient = Recipient.objects.filter(user=user).first()
    recipient_allocations = []
    if recipient:
        recipient_allocations = AllocatedDonorToRecipient.objects.filter(recipient=recipient)

    return render(request, 'profile.html', {
        'user': user,
        'donor': donor,
        'donor_allocation': donor_allocation,
        'recipient': recipient,
        'recipient_allocations': recipient_allocations,
    })

def page_not_found_view(request, exception):
    return render(request, '404-errorpage.html', status=404)