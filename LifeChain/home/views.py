from django.contrib import messages
from django.shortcuts import render, redirect
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
import logging
# from .models import Contact  # Temporarily commented out

# Set up logging
logger = logging.getLogger(__name__)

# Create your views here.
def health_check(request):
    """Simple health check that doesn't depend on anything"""
    return HttpResponse("OK", content_type="text/plain")

def simple_test(request):
    """Very simple test that doesn't depend on anything"""
    return HttpResponse("Simple test working!")

def index(request):
    try:
        logger.info("Index view called successfully")
        # Temporarily disable template rendering to isolate the issue
        # return render(request, 'index.html')
        return HttpResponse("Index page working! (Template rendering temporarily disabled)")
    except Exception as e:
        logger.error(f"Error in index view: {str(e)}", exc_info=True)
        return HttpResponse("Error rendering index page. Please try again.", status=500)

def test_view(request):
    """Simple test view to check if Django is working"""
    try:
        logger.info("Test view called successfully")
        return HttpResponse("Django is working! This is a test view.")
    except Exception as e:
        logger.error(f"Error in test view: {str(e)}", exc_info=True)
        return HttpResponse("Error in test view. Please try again.", status=500)

@csrf_exempt
def contact(request):
    try:
        if request.method == 'POST':
            # Temporarily disabled database operations
            # name = request.POST.get('name')
            # email = request.POST.get('email')
            # phone_number = request.POST.get('phone_number')
            # message = request.POST.get('message')

            # # Save the contact data into the database
            # contact = Contact(name=name, email=email, phone_number=phone_number, message=message)
            # contact.save()

            # # After saving the contact, show a success message
            # messages.success(request, 'Your message has been sent successfully!')
            # return redirect('contact')  # Redirect back to the contact page

            return HttpResponse("Contact form submitted successfully! (Database temporarily disabled)")

        # return render(request, 'contactUs.html')
        return HttpResponse("Contact page working! (Template rendering temporarily disabled)")
    except Exception as e:
        logger.error(f"Error in contact view: {str(e)}", exc_info=True)
        return HttpResponse("Error in contact view. Please try again.", status=500)
    
def about(request):
    try:
        # Temporarily disable template rendering to isolate the issue
        # return render(request, 'about.html')
        return HttpResponse("About page working! (Template rendering temporarily disabled)")
    except Exception as e:
        logger.error(f"Error in about view: {str(e)}", exc_info=True)
        return HttpResponse("Error in about view. Please try again.", status=500)

def profile_view(request):
    try:
        # Temporarily disabled database operations
        # # Import models here to avoid circular imports
        # from donor.models import donor_Registered
        # from recipient.models import AllocatedDonorToRecipient, Recipient
        
        # user = request.user

        # # Donor section
        # donor = donor_Registered.objects.filter(user=user).first()
        # donor_allocation = None
        # if donor:
        #     donor_allocation = AllocatedDonorToRecipient.objects.filter(donor=donor).last()

        # # Recipient section
        # recipient = Recipient.objects.filter(user=user).first()
        # recipient_allocations = []
        # if recipient:
        #     recipient_allocations = AllocatedDonorToRecipient.objects.filter(recipient=recipient)

        # return render(request, 'profile.html', {
        #     'user': user,
        #     'donor': donor,
        #     'donor_allocation': donor_allocation,
        #     'recipient': recipient,
        #     'recipient_allocations': recipient_allocations,
        # })
        
        return HttpResponse("Profile view working! (Database temporarily disabled)")
    except Exception as e:
        logger.error(f"Error in profile view: {str(e)}", exc_info=True)
        return HttpResponse("Error in profile view. Please try again.", status=500)

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