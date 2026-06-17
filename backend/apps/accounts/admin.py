from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User

class CustomUserAdmin(UserAdmin):
    model = User
    list_display = ['email', 'username', 'nationality', 'phone', 'is_staff', 'is_active']
    fieldsets = UserAdmin.fieldsets + (
        ('Profile Information', {'fields': ('nationality', 'phone')}),
    )
    add_fieldsets = UserAdmin.add_fieldsets + (
        ('Profile Information', {'fields': ('nationality', 'phone')}),
    )

admin.site.register(User, CustomUserAdmin)
