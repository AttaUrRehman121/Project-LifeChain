
from django.urls import path, include
from django.views.defaults import page_not_found
from .views import (
    contact, about, index, profile_view, test_view, health_check,
    custom_404, custom_500, custom_403, custom_400
)
from registration.views import signup


urlpatterns = [
    path('', index, name='index'),
    path('health/', health_check, name='health'),
    path('test/', test_view, name='test'),
    path('registration/', signup, name='signup'),
    path('contact/', contact, name='contact'),
    path('about/', about, name='about'),
    path('profile/', profile_view, name='profile_view'),
]

# Error handlers
handler404 = 'home.views.custom_404'
handler500 = 'home.views.custom_500'
handler403 = 'home.views.custom_403'
handler400 = 'home.views.custom_400'

# Catch-all pattern for invalid URLs (this will be the last pattern)
def catch_all(request, path):
    """Catch all invalid URLs and show 404 page"""
    return custom_404(request)

# Add this to the main URLs file (LifeChain/urls.py) as the last pattern
# path('<path:path>', catch_all, name='catch_all'),
