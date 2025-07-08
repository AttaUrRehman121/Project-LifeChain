from django.contrib import admin
from . import models


class UserProfileAdmin(admin.ModelAdmin):
    list_display = ('username', 'email', 'nationality', 'role', 'contact', 'address', 'is_active', 'date_joined')
    search_fields = ('username', 'email', 'nationality', 'role')
    list_filter = ('is_active', 'role')
    ordering = ('-date_joined',)


admin.site.register(models.UserProfile, UserProfileAdmin)
