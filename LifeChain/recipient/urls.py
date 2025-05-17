from django.contrib import admin
from django.urls import path, include
from .views import recipientpage,  recipientprictiction, RecipientResultpage, eligible_donors

urlpatterns = [
  path('',recipientpage, name= "recipientpage"),
  path('recipientprictiction/',recipientprictiction, name= "recipientprictiction"),
  path('recipientresultpage/',RecipientResultpage, name= "RecipientResultpage"),
  path('eligibleDonors/', eligible_donors, name='eligibleDdonors'),
  
    
]
