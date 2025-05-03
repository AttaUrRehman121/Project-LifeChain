from django.contrib import admin
from django.urls import path, include

from . import views

urlpatterns = [
   
   path('', views.donorpage, name='donorpage'),
   path('donorpridict/', views.donorpridict, name='donorpridict'),
   path('donorresultpage/', views.DonorResultpage, name='DonorResultpage'),
   path('donor_Applicants/', views.donor_Applicants, name='donor_Applicants'),

   
   
]
