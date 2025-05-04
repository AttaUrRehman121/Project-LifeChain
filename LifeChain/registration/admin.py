from django.contrib import admin
from . import models

# Customizing the UserProfile admin interface
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ('username', 'email', 'nationality', 'role', 'contact', 'address', 'is_active', 'date_joined')
    search_fields = ('username', 'email', 'nationality', 'role')
    list_filter = ('is_active', 'role')
    ordering = ('-date_joined',)

# Register the model with the custom admin
admin.site.register(models.UserProfile, UserProfileAdmin)
