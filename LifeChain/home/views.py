from django.contrib import messages
from django.shortcuts import render, redirect
from django.views.decorators.csrf import csrf_protect
from django.contrib.auth import login as auth_login, authenticate
from .models import Contact
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from django.http import HttpResponse, Http404
from functools import wraps
import logging
from donor.models import donor_Registered
from recipient.models import AllocatedDonorToRecipient, Recipient
from registration.models import UserProfile
from django.contrib.auth.decorators import login_required

# Set up logging
logger = logging.getLogger(__name__)

def handle_errors(view_func):
    """Decorator to handle any unexpected errors"""
    @wraps(view_func)
    def wrapper(request, *args, **kwargs):
        try:
            return view_func(request, *args, **kwargs)
        except Exception as e:
            logger.error(f"Unexpected error in {view_func.__name__}: {str(e)}", exc_info=True)
            return custom_500(request)
    return wrapper

# Create your views here.
@handle_errors
def health_check(request):
    """Simple health check that doesn't depend on anything"""
    return HttpResponse("OK", content_type="text/plain")

@handle_errors
def index(request):
    try:
        logger.info("Index view called successfully")
        return render(request, 'index.html')
    except Exception as e:
        logger.error(f"Error in index view: {str(e)}", exc_info=True)
        return custom_500(request)

@handle_errors
def test_view(request):
    """Simple test view to check if Django is working"""
    try:
        logger.info("Test view called successfully")
        return HttpResponse("Django is working! This is a test view.")
    except Exception as e:
        logger.error(f"Error in test view: {str(e)}", exc_info=True)
        return custom_500(request)

@csrf_exempt
@handle_errors
def contact(request):
    try:
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
    except Exception as e:
        logger.error(f"Error in contact view: {str(e)}", exc_info=True)
        return custom_500(request)
    
@handle_errors
def about(request):
    try:
        return render(request, 'about.html')
    except Exception as e:
        logger.error(f"Error in about view: {str(e)}", exc_info=True)
        return custom_500(request)

@login_required
@handle_errors
def profile_view(request):
    try:
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
    except Exception as e:
        logger.error(f"Error in profile view: {str(e)}", exc_info=True)
        return custom_500(request)

# Custom Error Handlers
def custom_404(request, exception=None):
    """Custom 404 error page"""
    logger.warning(f"404 error for URL: {request.path}")
    return render(request, '404-errorpage.html', status=404)

def custom_500(request, exception=None):
    """Custom 500 error page"""
    logger.error(f"500 error for URL: {request.path}", exc_info=True)
    return render(request, '500-errorpage.html', status=500)

def custom_403(request, exception=None):
    """Custom 403 error page"""
    logger.warning(f"403 error for URL: {request.path}")
    return render(request, '403-errorpage.html', status=403)

def custom_400(request, exception=None):
    """Custom 400 error page"""
    logger.warning(f"400 error for URL: {request.path}")
    return render(request, '400-errorpage.html', status=400)

def page_not_found_view(request, exception=None):
    """Legacy 404 handler for compatibility"""
    return custom_404(request, exception)