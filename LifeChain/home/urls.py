from django.contrib import admin
from django.urls import path, include
from .views import contact, about, index, profile_view
from registration.views import signup
from django.conf import settings


urlpatterns = [
    path('', index, name='index'),
    path('registration/', signup, name='signup'),
    path('contact/', contact, name='contact'),
    path('about/', about, name='about'),
    path('profile/', profile_view, name='profile_view'), 
]
