from multiprocessing import AuthenticationError
from pyexpat.errors import messages
from django.shortcuts import redirect, render
from django.views.decorators.csrf import csrf_protect
from django.contrib.auth import login as auth_login



# Create your views here.
def index(request):
        return render(request, 'index.html')
    
def contact(request):
    return render(request, 'contactUs.html')
    
def about(request):
    return render(request, 'about.html')

def profile_view(request):
    return render(request, 'profile.html')


# def login(request):
#     return render(request, 'login.html')


# def logout(request):
#     return render(request, 'profile.html')



@csrf_protect
def login(request):
     if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        # Authenticate the user
        user = AuthenticationError(request, username=username, password=password)
        if user is not None:
            try:
                # Get the user's profile to check their role
                user_profile = UserProfile.objects.get(user=user)
                auth_login(request, user)
                if user_profile.role == 'donor':
                    return redirect('donorpage')  # Replace with actual donor page URL name
                elif user_profile.role == 'recipient':
                    return redirect('recipientpage')  # Replace with actual recipient page URL name
            except UserProfile.DoesNotExist:
                messages.error(request, "User profile not found. Please contact support.")
                return redirect('login')
        else:
            messages.error(request, "Invalid username or password.")
            return redirect('login')
        
        return render(request, 'login.html')