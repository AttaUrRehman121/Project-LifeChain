from django.shortcuts import render

def dashboard(request):
    return render(request, 'custom_admin/dashboard.html')