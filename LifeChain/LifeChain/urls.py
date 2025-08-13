from django.contrib import admin
from django.urls import path, include
from home.views import custom_404

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('home.urls')),
    path('registration/', include('registration.urls')),
    path('donor/', include('donor.urls')),
    path('recipient/', include('recipient.urls')),
]

# Catch-all pattern for invalid URLs (must be last)
urlpatterns.append(path('<path:path>', custom_404, name='catch_all'))
