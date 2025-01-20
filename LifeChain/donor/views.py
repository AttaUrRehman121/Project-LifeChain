from django.shortcuts import render
from django.contrib.auth.decorators import login_required

# Create your views here.

# @login_required
def donorpage(request):
    return render(request, 'donorPage.html')

def donorpridict(request):
    return render(request, 'DonorPredict.html')

def DonorResultpage(request):
    return render(request, 'RecipientResultPage.html')