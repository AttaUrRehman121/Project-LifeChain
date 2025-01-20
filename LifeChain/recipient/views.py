from django.shortcuts import render
from django.contrib.auth.decorators import login_required

# Create your views here.
# @login_required
def recipientpage(request):
    return render(request, 'recipientPage.html')


def recipientprictiction(request):
    return render(request, 'RecipientPrediction.html')


def RecipientResultpage(request):
    return render(request, 'RecipientResultPage.html')

