
from django.urls import path, include
from .views import contact, about, index, profile_view
from registration.views import signup


urlpatterns = [
    path('', index, name='index'),
    path('registration/', signup, name='signup'),
    path('contact/', contact, name='contact'),
    path('about/', about, name='about'),
    path('profile/', profile_view, name='profile_view'),
      
]

handler404 = 'home.views.page_not_found_view'
