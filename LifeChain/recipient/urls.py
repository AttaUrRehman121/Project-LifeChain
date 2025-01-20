from django.contrib import admin
from django.urls import path, include
from .views import recipientpage,  recipientprictiction, RecipientResultpage

urlpatterns = [
  path('',recipientpage, name= "recipientpage"),
  path('recipientprictiction/',recipientprictiction, name= "recipientprictiction"),
  path('recipientresultpage/',RecipientResultpage, name= "RecipientResultpage"),
  
]
