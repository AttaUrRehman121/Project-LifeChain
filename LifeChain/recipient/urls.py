from django.contrib import admin
from django.urls import path, include
from .views import recipientpage,  recipientprictiction, RecipientResultpage, eligible_donors,allocate_donor, verify_donor_email

urlpatterns = [
  path('',recipientpage, name= "recipientpage"),
  path('recipientprictiction/',recipientprictiction, name= "recipientprictiction"),
  path('recipientresultpage/',RecipientResultpage, name= "RecipientResultpage"),
  path('recipientprictiction/eligibleDonors/', eligible_donors, name='eligibleDdonors'),
  path('allocate_donor/<int:donor_id>/', allocate_donor, name='allocate_donor'),
  path('verify_donor/<slug:token>/', verify_donor_email, name='verify_donor_email')


]
