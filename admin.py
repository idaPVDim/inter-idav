from django.contrib import admin

# Register my models here:
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser

class CustomUserAdmin(UserAdmin):
    model = CustomUser
    list_display = ['username', 'email', 'user_type', 'is_blocked', 'status']

admin.site.register(CustomUser, CustomUserAdmin)