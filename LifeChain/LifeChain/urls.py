from django.contrib import admin
from django.urls import path, include


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('home.urls')),
    path('registration/', include('registration.urls')),
    path('donor/', include('donor.urls')),
    path('recipient/', include('recipient.urls')),
]


handler404 = 'home.views.page_not_found_view'
