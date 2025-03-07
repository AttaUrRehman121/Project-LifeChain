from django.urls import path
from . import views

app_name = 'custom_admin'  

urlpatterns = [
    path('dashboard/', views.dashboard, name='dashboard'),
]